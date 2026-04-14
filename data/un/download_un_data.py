#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.28.1",
#   "orjson>=3.10.18",
#   "rich>=14.1.0",
#   "tenacity>=9.1.2",
#   "typer>=0.16.1",
# ]
# ///
"""Download UN Data SDMX CSV slices with persistent resume state."""

from __future__ import annotations

import asyncio
import csv
import gzip
import logging
import re
import sqlite3
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import httpx
import orjson
import typer
from rich.logging import RichHandler
from tenacity import AsyncRetrying, RetryError, retry_if_exception_type, stop_after_attempt, wait_exponential

BASE_URL = "https://data.un.org/ws/rest"
CATALOG_URL = f"{BASE_URL}/dataflow"
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"
APP = typer.Typer(no_args_is_help=True, add_completion=False)
TODAY = date.today().isoformat()


@dataclass(slots=True)
class Dataflow:
    agency_id: str
    flow_id: str
    version: str
    name: str

    @property
    def flow_key(self) -> str:
        return f"{self.agency_id}:{self.flow_id}:{self.version}"

    @property
    def slug(self) -> str:
        return slugify(self.name or self.flow_id)


def slugify(value: str) -> str:
    """Return a filesystem-safe slug."""
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "unnamed"


def utc_now() -> str:
    """Return a stable UTC timestamp string."""
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def data_url(flow: Dataflow, year: int) -> str:
    """Build the CSV download URL for a single year slice."""
    return (
        f"{BASE_URL}/data/{flow.agency_id},{flow.flow_id},{flow.version}/ALL"
        f"?startPeriod={year}&endPeriod={year}"
    )


def setup_logging(log_path: Path, verbose: bool) -> None:
    """Configure console and file logging."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.DEBUG if verbose else logging.INFO)

    console = RichHandler(rich_tracebacks=True, markup=False, show_path=False)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    root.addHandler(console)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    root.addHandler(file_handler)


def connect_db(path: Path) -> sqlite3.Connection:
    """Open the state database and apply schema migrations."""
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS dataflows (
            flow_key TEXT PRIMARY KEY,
            agency_id TEXT NOT NULL,
            flow_id TEXT NOT NULL,
            version TEXT NOT NULL,
            name TEXT NOT NULL,
            slug TEXT NOT NULL,
            latest_nonempty_year INTEGER,
            first_checked_at TEXT,
            last_checked_at TEXT
        );

        CREATE TABLE IF NOT EXISTS jobs (
            flow_key TEXT NOT NULL,
            year INTEGER NOT NULL,
            status TEXT NOT NULL,
            file_path TEXT,
            bytes_written INTEGER,
            line_count INTEGER,
            checksum_hint TEXT,
            started_at TEXT,
            finished_at TEXT,
            fetched_at TEXT,
            error_message TEXT,
            PRIMARY KEY (flow_key, year)
        );
        """
    )
    return conn


def write_catalog_files(data_dir: Path, flows: list[Dataflow]) -> None:
    """Persist the catalog in JSON and CSV formats."""
    catalog_dir = data_dir / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    json_path = catalog_dir / "dataflows.json"
    csv_path = catalog_dir / "dataflows.csv"

    json_path.write_bytes(
        orjson.dumps(
            [
                {
                    "agency_id": flow.agency_id,
                    "flow_id": flow.flow_id,
                    "version": flow.version,
                    "name": flow.name,
                    "flow_key": flow.flow_key,
                    "slug": flow.slug,
                }
                for flow in flows
            ],
            option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS,
        )
    )

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["agency_id", "flow_id", "version", "name", "flow_key", "slug"],
        )
        writer.writeheader()
        for flow in flows:
            writer.writerow(
                {
                    "agency_id": flow.agency_id,
                    "flow_id": flow.flow_id,
                    "version": flow.version,
                    "name": flow.name,
                    "flow_key": flow.flow_key,
                    "slug": flow.slug,
                }
            )


def save_dataflows(conn: sqlite3.Connection, flows: list[Dataflow]) -> None:
    """Upsert dataflow metadata into the state database."""
    with conn:
        conn.executemany(
            """
            INSERT INTO dataflows(flow_key, agency_id, flow_id, version, name, slug)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(flow_key) DO UPDATE SET
                agency_id = excluded.agency_id,
                flow_id = excluded.flow_id,
                version = excluded.version,
                name = excluded.name,
                slug = excluded.slug
            """,
            [
                (flow.flow_key, flow.agency_id, flow.flow_id, flow.version, flow.name, flow.slug)
                for flow in flows
            ],
        )


def write_probe_file(data_dir: Path, rows: list[dict[str, Any]]) -> None:
    """Write recent availability probe results to CSV."""
    probe_path = data_dir / "catalog" / "recent_availability.csv"
    probe_path.parent.mkdir(parents=True, exist_ok=True)
    with probe_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "flow_key",
                "agency_id",
                "flow_id",
                "version",
                "name",
                "latest_nonempty_year",
                "probe_years_checked",
                "checked_at",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


async def request_json(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    """Fetch a JSON document with retries."""
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        retry=retry_if_exception_type(httpx.HTTPError),
        reraise=True,
    ):
        with attempt:
            response = await client.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            return response.json()
    raise RuntimeError("unreachable")


async def fetch_catalog(client: httpx.AsyncClient) -> list[Dataflow]:
    """Download and parse the live dataflow catalog."""
    payload = await request_json(client, CATALOG_URL)
    flows: list[Dataflow] = []
    for entry in payload.get("references", {}).values():
        flows.append(
            Dataflow(
                agency_id=entry["agencyID"],
                flow_id=entry["id"],
                version=entry["version"],
                name=entry.get("name", entry["id"]),
            )
        )
    return sorted(flows, key=lambda item: (item.agency_id, item.flow_id))


async def probe_year_has_data(client: httpx.AsyncClient, flow: Dataflow, year: int) -> bool:
    """Return True when the given year slice contains at least one data row."""
    logger = logging.getLogger("probe")
    try:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(4),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type(httpx.RequestError),
            reraise=True,
        ):
            with attempt:
                async with client.stream(
                    "GET",
                    data_url(flow, year),
                    headers={"Accept": CSV_ACCEPT},
                ) as response:
                    if response.status_code >= 500:
                        logger.debug(
                            "Treating server error as empty probe result for %s year=%s status=%s",
                            flow.flow_key,
                            year,
                            response.status_code,
                        )
                        return False
                    response.raise_for_status()
                    line_count = 0
                    async for chunk in response.aiter_text():
                        line_count += chunk.count("\n")
                        if line_count >= 2:
                            return True
                    return False
    except (RetryError, httpx.HTTPError) as exc:
        logger.warning("Probe failed for %s year=%s error=%s", flow.flow_key, year, exc)
    return False


async def probe_latest_year(
    client: httpx.AsyncClient,
    conn: sqlite3.Connection,
    flow: Dataflow,
    start_year: int,
    end_year: int,
) -> dict[str, Any]:
    """Find the newest year with data by checking recent years first."""
    latest_nonempty_year: int | None = None
    years_checked = 0
    for year in range(end_year, start_year - 1, -1):
        years_checked += 1
        if await probe_year_has_data(client, flow, year):
            latest_nonempty_year = year
            break

    checked_at = utc_now()
    with conn:
        conn.execute(
            """
            UPDATE dataflows
            SET latest_nonempty_year = ?, first_checked_at = COALESCE(first_checked_at, ?), last_checked_at = ?
            WHERE flow_key = ?
            """,
            (latest_nonempty_year, checked_at, checked_at, flow.flow_key),
        )

    return {
        "flow_key": flow.flow_key,
        "agency_id": flow.agency_id,
        "flow_id": flow.flow_id,
        "version": flow.version,
        "name": flow.name,
        "latest_nonempty_year": latest_nonempty_year,
        "probe_years_checked": years_checked,
        "checked_at": checked_at,
    }


def choose_years(
    conn: sqlite3.Connection,
    flow: Dataflow,
    start_year: int,
    end_year: int,
    latest_only: bool,
) -> list[int]:
    """Build the list of years to fetch, newest first."""
    row = conn.execute(
        "SELECT latest_nonempty_year, last_checked_at FROM dataflows WHERE flow_key = ?",
        (flow.flow_key,),
    ).fetchone()
    if row and row["last_checked_at"] and row["latest_nonempty_year"] is None:
        fallback_start = max(end_year - 2, start_year)
        return list(range(end_year, fallback_start - 1, -1))
    newest = row["latest_nonempty_year"] if row else None
    upper = newest if newest is not None else end_year
    if latest_only:
        return [upper]
    return list(range(upper, start_year - 1, -1))


def output_path(data_dir: Path, flow: Dataflow, year: int) -> Path:
    """Return the target output path for a year slice."""
    folder = data_dir / "downloads" / flow.agency_id.lower() / flow.slug / "by-year"
    filename = (
        f"{flow.agency_id.lower()}__{flow.slug}__period-{year}"
        f"__fetched-{TODAY}.csv.gz"
    )
    return folder / filename


def existing_output_path(data_dir: Path, flow: Dataflow, year: int) -> Path | None:
    """Return an existing output file for the flow/year regardless of fetch date."""
    folder = data_dir / "downloads" / flow.agency_id.lower() / flow.slug / "by-year"
    pattern = f"{flow.agency_id.lower()}__{flow.slug}__period-{year}__fetched-*.csv.gz"
    matches = sorted(folder.glob(pattern))
    return matches[-1] if matches else None


def sync_existing_file_to_db(
    conn: sqlite3.Connection,
    data_dir: Path,
    flow: Dataflow,
    year: int,
) -> Path | None:
    """Record an on-disk file as completed when DB state is missing or stale."""
    existing = existing_output_path(data_dir, flow, year)
    if not existing:
        return None

    row = conn.execute(
        "SELECT status, file_path FROM jobs WHERE flow_key = ? AND year = ?",
        (flow.flow_key, year),
    ).fetchone()
    if row and row["status"] == "done" and row["file_path"] == str(existing):
        return existing

    with conn:
        conn.execute(
            """
            INSERT INTO jobs(flow_key, year, status, file_path, finished_at, fetched_at, error_message)
            VALUES (?, ?, 'done', ?, ?, ?, NULL)
            ON CONFLICT(flow_key, year) DO UPDATE SET
                status = 'done',
                file_path = excluded.file_path,
                finished_at = excluded.finished_at,
                fetched_at = excluded.fetched_at,
                error_message = NULL
            """,
            (flow.flow_key, year, str(existing), utc_now(), TODAY),
        )
    return existing


def job_is_complete(
    conn: sqlite3.Connection,
    data_dir: Path,
    flow: Dataflow,
    year: int,
    *,
    force: bool,
) -> bool:
    """Return True when a slice should be skipped because it already exists."""
    if force:
        return False

    if not force and sync_existing_file_to_db(conn, data_dir, flow, year):
        return True

    row = conn.execute(
        "SELECT status, file_path FROM jobs WHERE flow_key = ? AND year = ?",
        (flow.flow_key, year),
    ).fetchone()
    if not row:
        return False
    if row["status"] == "empty":
        return True
    if row["status"] == "done" and row["file_path"] and Path(row["file_path"]).exists():
        return True
    return False


def mark_job_started(conn: sqlite3.Connection, flow: Dataflow, year: int) -> None:
    """Persist that a slice download started."""
    with conn:
        conn.execute(
            """
            INSERT INTO jobs(flow_key, year, status, started_at, error_message)
            VALUES (?, ?, 'running', ?, NULL)
            ON CONFLICT(flow_key, year) DO UPDATE SET
                status = 'running',
                started_at = excluded.started_at,
                error_message = NULL
            """,
            (flow.flow_key, year, utc_now()),
        )


def mark_job_finished(
    conn: sqlite3.Connection,
    flow: Dataflow,
    year: int,
    *,
    status: str,
    file_path: Path | None = None,
    bytes_written: int | None = None,
    line_count: int | None = None,
    error_message: str | None = None,
) -> None:
    """Persist final job status."""
    checksum_hint = f"bytes:{bytes_written}" if bytes_written is not None else None
    with conn:
        conn.execute(
            """
            UPDATE jobs
            SET status = ?,
                file_path = ?,
                bytes_written = ?,
                line_count = ?,
                checksum_hint = ?,
                finished_at = ?,
                fetched_at = ?,
                error_message = ?
            WHERE flow_key = ? AND year = ?
            """,
            (
                status,
                str(file_path) if file_path else None,
                bytes_written,
                line_count,
                checksum_hint,
                utc_now(),
                TODAY,
                error_message,
                flow.flow_key,
                year,
            ),
        )


async def download_one(
    client: httpx.AsyncClient,
    conn: sqlite3.Connection,
    data_dir: Path,
    flow: Dataflow,
    year: int,
    *,
    force: bool,
) -> str:
    """Download one year slice and update state."""
    logger = logging.getLogger("download")
    existing = existing_output_path(data_dir, flow, year)
    if existing and not force:
        sync_existing_file_to_db(conn, data_dir, flow, year)
        logger.info("Skipping existing file for %s year=%s file=%s", flow.flow_key, year, existing)
        return "skipped"

    if job_is_complete(conn, data_dir, flow, year, force=force):
        logger.debug("Skipping completed slice %s %s", flow.flow_key, year)
        return "skipped"

    target = output_path(data_dir, flow, year)
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target.with_suffix(target.suffix + ".part")
    if temp_path.exists():
        temp_path.unlink()

    mark_job_started(conn, flow, year)
    logger.info("Downloading %s year=%s", flow.flow_key, year)

    try:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=1, max=20),
            retry=retry_if_exception_type(httpx.HTTPError),
            reraise=True,
        ):
            with attempt:
                bytes_written = 0
                line_count = 0
                async with client.stream(
                    "GET",
                    data_url(flow, year),
                    headers={"Accept": CSV_ACCEPT},
                ) as response:
                    response.raise_for_status()
                    with gzip.open(temp_path, "wb") as handle:
                        async for chunk in response.aiter_bytes():
                            bytes_written += len(chunk)
                            line_count += chunk.count(b"\n")
                            handle.write(chunk)

                if line_count <= 1:
                    temp_path.unlink(missing_ok=True)
                    mark_job_finished(
                        conn,
                        flow,
                        year,
                        status="empty",
                        bytes_written=bytes_written,
                        line_count=line_count,
                    )
                    logger.info("Empty slice %s year=%s", flow.flow_key, year)
                    return "empty"

                temp_path.replace(target)
                mark_job_finished(
                    conn,
                    flow,
                    year,
                    status="done",
                    file_path=target,
                    bytes_written=bytes_written,
                    line_count=line_count,
                )
                logger.info(
                    "Saved %s year=%s rows~=%s file=%s",
                    flow.flow_key,
                    year,
                    max(line_count - 1, 0),
                    target,
                )
                return "done"
    except RetryError as exc:
        error = str(exc.last_attempt.exception())
    except Exception as exc:  # noqa: BLE001
        error = str(exc)

    temp_path.unlink(missing_ok=True)
    mark_job_finished(conn, flow, year, status="error", error_message=error)
    logger.error("Failed %s year=%s error=%s", flow.flow_key, year, error)
    return "error"


async def bounded_probe(
    client: httpx.AsyncClient,
    conn: sqlite3.Connection,
    flow: Dataflow,
    start_year: int,
    end_year: int,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    """Run a single latest-year probe within a semaphore."""
    async with semaphore:
        return await probe_latest_year(client, conn, flow, start_year, end_year)


async def bounded_download(
    client: httpx.AsyncClient,
    conn: sqlite3.Connection,
    data_dir: Path,
    flow: Dataflow,
    year: int,
    semaphore: asyncio.Semaphore,
    *,
    force: bool,
) -> str:
    """Run one download within a semaphore."""
    async with semaphore:
        return await download_one(client, conn, data_dir, flow, year, force=force)


async def build_catalog(
    data_dir: Path,
    conn: sqlite3.Connection,
    *,
    verbose: bool,
) -> list[Dataflow]:
    """Fetch the live dataflow catalog and persist it locally."""
    timeout = httpx.Timeout(connect=30.0, read=120.0, write=120.0, pool=120.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        flows = await fetch_catalog(client)
    write_catalog_files(data_dir, flows)
    save_dataflows(conn, flows)
    logging.getLogger("catalog").info("Catalog contains %s dataflows", len(flows))
    if verbose:
        for flow in flows:
            logging.getLogger("catalog").debug("%s %s", flow.flow_key, flow.name)
    return flows


def load_dataflows_from_db(conn: sqlite3.Connection) -> list[Dataflow]:
    """Load cached dataflows from the state database."""
    rows = conn.execute(
        """
        SELECT agency_id, flow_id, version, name
        FROM dataflows
        ORDER BY agency_id, flow_id
        """
    ).fetchall()
    return [
        Dataflow(
            agency_id=row["agency_id"],
            flow_id=row["flow_id"],
            version=row["version"],
            name=row["name"],
        )
        for row in rows
    ]


def filter_flows(flows: list[Dataflow], match: str | None) -> list[Dataflow]:
    """Filter dataflows by substring match against key and name."""
    if not match:
        return flows
    needle = match.lower()
    return [
        flow
        for flow in flows
        if needle in flow.flow_key.lower() or needle in flow.name.lower() or needle in flow.slug
    ]


def summarize_jobs(conn: sqlite3.Connection) -> dict[str, int]:
    """Return aggregate job counts by status."""
    rows = conn.execute(
        "SELECT status, COUNT(*) AS count FROM jobs GROUP BY status ORDER BY status"
    ).fetchall()
    return {row["status"]: row["count"] for row in rows}


@APP.command()
def catalog(
    data_dir: Path = typer.Option(Path("data"), help="Base directory for catalog, logs, state, and downloads."),
    verbose: bool = typer.Option(False, "--verbose", help="Emit debug logging."),
) -> None:
    """Fetch and save the live UN Dataflow catalog."""
    setup_logging(data_dir / "logs" / "download.log", verbose)
    conn = connect_db(data_dir / "state" / "downloads.sqlite3")
    flows = asyncio.run(build_catalog(data_dir, conn, verbose=verbose))
    typer.echo(f"Saved catalog for {len(flows)} dataflows to {data_dir / 'catalog'}")


@APP.command()
def probe(
    data_dir: Path = typer.Option(Path("data"), help="Base directory for outputs."),
    start_year: int = typer.Option(1900, min=1800, help="Oldest year to consider."),
    end_year: int = typer.Option(date.today().year, help="Newest year to consider."),
    concurrency: int = typer.Option(2, min=1, max=32, help="Concurrent probe requests."),
    match: str | None = typer.Option(None, help="Only probe matching flows."),
    refresh_catalog: bool = typer.Option(True, help="Refresh the live dataflow catalog first."),
    verbose: bool = typer.Option(False, "--verbose", help="Emit debug logging."),
) -> None:
    """Probe each dataflow to find its newest non-empty year."""
    setup_logging(data_dir / "logs" / "download.log", verbose)
    conn = connect_db(data_dir / "state" / "downloads.sqlite3")

    flows = (
        asyncio.run(build_catalog(data_dir, conn, verbose=verbose))
        if refresh_catalog
        else load_dataflows_from_db(conn)
    )
    flows = filter_flows(flows, match)
    if not flows:
        typer.echo("No matching dataflows found.")
        raise typer.Exit(1)

    timeout = httpx.Timeout(connect=30.0, read=120.0, write=120.0, pool=120.0)

    async def runner() -> list[dict[str, Any]]:
        semaphore = asyncio.Semaphore(concurrency)
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            tasks = [
                bounded_probe(client, conn, flow, start_year, end_year, semaphore)
                for flow in flows
            ]
            return await asyncio.gather(*tasks)

    results = asyncio.run(runner())
    write_probe_file(data_dir, results)
    typer.echo(f"Probed {len(results)} dataflows; wrote {data_dir / 'catalog' / 'recent_availability.csv'}")


@APP.command()
def download(
    data_dir: Path = typer.Option(Path("data"), help="Base directory for outputs."),
    start_year: int = typer.Option(1900, min=1800, help="Oldest year to download."),
    end_year: int = typer.Option(date.today().year, help="Newest year to consider."),
    concurrency: int = typer.Option(2, min=1, max=16, help="Concurrent downloads."),
    probe_concurrency: int = typer.Option(2, min=1, max=32, help="Concurrent probe requests."),
    match: str | None = typer.Option(None, help="Only download matching flows."),
    refresh_catalog: bool = typer.Option(True, help="Refresh the live dataflow catalog first."),
    probe_latest: bool = typer.Option(True, help="Probe for the latest non-empty year before downloading."),
    latest_only: bool = typer.Option(False, help="Download only the latest non-empty year per flow."),
    force: bool = typer.Option(False, "--force", help="Re-download even when matching output files already exist."),
    max_jobs: int | None = typer.Option(None, min=1, help="Cap the number of slices downloaded in this run."),
    verbose: bool = typer.Option(False, "--verbose", help="Emit debug logging."),
) -> None:
    """Download data newest-first into resumable year slices."""
    setup_logging(data_dir / "logs" / "download.log", verbose)
    conn = connect_db(data_dir / "state" / "downloads.sqlite3")

    flows = (
        asyncio.run(build_catalog(data_dir, conn, verbose=verbose))
        if refresh_catalog
        else load_dataflows_from_db(conn)
    )
    flows = filter_flows(flows, match)
    if not flows:
        typer.echo("No matching dataflows found.")
        raise typer.Exit(1)

    timeout = httpx.Timeout(connect=30.0, read=300.0, write=300.0, pool=300.0)

    async def runner() -> dict[str, int]:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            if probe_latest:
                probe_semaphore = asyncio.Semaphore(probe_concurrency)
                probe_results = await asyncio.gather(
                    *[
                        bounded_probe(client, conn, flow, start_year, end_year, probe_semaphore)
                        for flow in flows
                    ]
                )
                write_probe_file(data_dir, probe_results)

            work: list[tuple[Dataflow, int]] = []
            for flow in flows:
                for year in choose_years(conn, flow, start_year, end_year, latest_only):
                    if not job_is_complete(conn, data_dir, flow, year, force=force):
                        work.append((flow, year))

            work.sort(key=lambda item: item[1], reverse=True)
            if max_jobs is not None:
                work = work[:max_jobs]

            logging.getLogger("download").info("Prepared %s slices", len(work))
            download_semaphore = asyncio.Semaphore(concurrency)
            results = await asyncio.gather(
                *[
                    bounded_download(
                        client,
                        conn,
                        data_dir,
                        flow,
                        year,
                        download_semaphore,
                        force=force,
                    )
                    for flow, year in work
                ]
            )
            summary = {"done": 0, "empty": 0, "error": 0, "skipped": 0}
            for result in results:
                summary[result] = summary.get(result, 0) + 1
            return summary

    summary = asyncio.run(runner())
    aggregate = summarize_jobs(conn)
    typer.echo(f"Run summary: {summary}")
    typer.echo(f"All job statuses: {aggregate}")


if __name__ == "__main__":
    APP()
