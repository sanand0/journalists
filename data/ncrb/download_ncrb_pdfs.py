#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.28",
#   "lxml>=5.3",
#   "typer>=0.15",
# ]
# ///
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urljoin, urlparse

import httpx
import typer
from lxml import html

APP = typer.Typer(no_args_is_help=True)
BASE_URL = "https://www.ncrb.gov.in"
INDEX_URL = f"{BASE_URL}/crime-in-india-year-wise.html?keyword=&year=2024"
STATE_PATH = Path("download_state.json")
MANIFEST_PATH = Path("manifest.ndjson")
LOG_PATH = Path("download.log")
OUT_DIR = Path("pdfs")
USER_AGENT = "ncrb-pdf-downloader/1.0 (+research archiving)"


@dataclass(frozen=True)
class PdfItem:
    year: int
    url: str
    filename: str
    source: str
    title: str = ""
    expected_bytes: int | None = None


def log(message: str) -> None:
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {message}"
    print(line, flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def slugify(value: str) -> str:
    value = unquote(value)
    value = value.replace("&", " and ")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return re.sub(r"-{2,}", "-", value) or "report"


def part_label(url: str, title: str) -> str:
    text = unquote(f"{url} {title}").lower()
    roman_match = re.search(r"part\s*[-_ ]*(i{1,3}|iv|v)\b", text)
    if roman_match:
        return f"part-{roman_match.group(1)}"
    volume_match = re.search(r"vol(?:ume)?\s*[-_ ]*(\d+|i{1,3}|iv|v)\b", text)
    if volume_match:
        return f"volume-{volume_match.group(1)}"
    basename = Path(urlparse(url).path).stem
    return slugify(basename)[:80]


def output_name(year: int, url: str, title: str, index: int) -> str:
    label = part_label(url, title)
    if label in {"report", "pdf"}:
        label = f"report-{index:02d}"
    return f"crime-in-india-{year}-{label}.pdf"


def load_state() -> dict[str, dict]:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, dict]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def append_manifest(item: PdfItem, path: Path, sha256: str, bytes_written: int) -> None:
    row = asdict(item) | {
        "path": str(path),
        "sha256": sha256,
        "bytes": bytes_written,
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def fetch_html(client: httpx.Client, url: str) -> html.HtmlElement:
    response = client.get(url)
    response.raise_for_status()
    return html.fromstring(response.text)


def discover_years(client: httpx.Client) -> list[int]:
    doc = fetch_html(client, INDEX_URL)
    years = {
        int(value)
        for value in doc.xpath("//option/@value | //a[contains(@href, 'year=')]/text()")
        if re.fullmatch(r"\d{4}", value.strip())
    }
    return sorted(years, reverse=True)


def pdf_links_from_page(client: httpx.Client, year: int) -> list[tuple[str, str]]:
    url = f"{BASE_URL}/crime-in-india-year-wise.html?year={year}&keyword="
    try:
        doc = fetch_html(client, url)
    except httpx.HTTPError as exc:
        log(f"WARN year={year} page_fetch_failed url={url} error={exc}")
        return []
    links: list[tuple[str, str]] = []
    for link in doc.xpath("//table[contains(concat(' ', normalize-space(@class), ' '), ' c-table ')]//tbody//a[contains(translate(@href, 'PDF', 'pdf'), '.pdf')]"):
        href = link.get("href", "")
        row = link.xpath("ancestor::tr[1]")
        text = " ".join(row[0].itertext()).strip() if row else " ".join(link.itertext()).strip()
        full = urljoin(BASE_URL, href)
        if "ncrb.gov.in" in urlparse(full).netloc:
            links.append((full, text))
    return links


def generated_candidates(year: int) -> Iterable[tuple[str, str]]:
    romans = ["I", "II", "III", "IV"]
    for index, roman in enumerate(romans, start=1):
        yield (
            f"{BASE_URL}/uploads/files/{index}CrimeinIndia{year}Part{roman}.pdf",
            f"Crime in India {year} Part {roman}",
        )
    for index in range(1, 5):
        yield (
            f"{BASE_URL}/uploads/files/{index}CrimeinIndia{year}Part{index}.pdf",
            f"Crime in India {year} Part {index}",
        )
    for vol in range(1, 4):
        yield (
            f"{BASE_URL}/uploads/nationalcrimerecordsbureau/custom/CII%20{year}%20Volume%20{vol}.pdf",
            f"Crime in India {year} Volume {vol}",
        )


def seeded_candidates() -> dict[int, list[tuple[str, str]]]:
    return {
        2024: [
            (f"{BASE_URL}/uploads/files/CrimeinIndia2024-VolumeI.pdf", "Crime in India 2024 Volume I"),
            (f"{BASE_URL}/uploads/files/2CrimeinIndia2024-VolumeII.pdf", "Crime in India 2024 Volume II"),
            (f"{BASE_URL}/uploads/files/3CrimeinIndia2024-VolumeIII.pdf", "Crime in India 2024 Volume III"),
            (f"{BASE_URL}/uploads/files/4HSSirmessageCII-2024.pdf", "Crime in India 2024 Message Home Secretary"),
            (f"{BASE_URL}/uploads/files/5FOREWORD-CII-2024.pdf", "Crime in India 2024 Foreword Director NCRB"),
            (f"{BASE_URL}/uploads/files/6CIIDisclaimerLimitations2024.pdf", "Crime in India 2024 Disclaimer Limitations"),
            (f"{BASE_URL}/uploads/files/CIIMethodology2024.pdf", "Crime in India 2024 Methodology"),
            (f"{BASE_URL}/uploads/files/8WordofCaution2024.pdf", "Crime in India 2024 Word of Caution"),
            (f"{BASE_URL}/uploads/files/9ACII2024Snapshots-StateandUTs.pdf", "Crime in India 2024 Snapshots State UTs"),
            (f"{BASE_URL}/uploads/files/12Population2024.pdf", "Crime in India 2024 Annexure Population"),
            (f"{BASE_URL}/uploads/files/13Glossary2024.pdf", "Crime in India 2024 Glossary"),
            (f"{BASE_URL}/uploads/files/14OFFICERS-2024.pdf", "Crime in India 2024 Officers Associated"),
            (f"{BASE_URL}/uploads/files/15Feedback-2024.pdf", "Crime in India 2024 Feedback Form"),
        ],
        2023: [
            (f"{BASE_URL}/uploads/files/1CrimeinIndia2023PartI.pdf", "Crime in India 2023 Part I"),
            (f"{BASE_URL}/uploads/files/2CrimeinIndia2023PartII.pdf", "Crime in India 2023 Part II"),
            (f"{BASE_URL}/uploads/files/3CrimeinIndia2023PartIII.pdf", "Crime in India 2023 Part III"),
        ],
        2019: [
            (
                f"{BASE_URL}/uploads/nationalcrimerecordsbureau/custom/1653730573_CII%202019%20Volume%201.pdf",
                "Crime in India 2019 Volume 1",
            ),
        ],
        2018: [
            (
                f"{BASE_URL}/uploads/nationalcrimerecordsbureau/custom/1653734481_Crime%20in%20India%202018%20-%20Volume%201_3_0_0.pdf",
                "Crime in India 2018 Volume 1",
            ),
        ],
        1953: [
            (
                f"{BASE_URL}/uploads/nationalcrimerecordsbureau/post/1686379857GENERALSITUATIONINTHECOUNTRY.pdf",
                "Crime in India 1953 General Situation in the Country",
            ),
        ],
    }


def probe_pdf(client: httpx.Client, url: str) -> int | None:
    try:
        response = client.head(url, follow_redirects=True)
        if response.status_code == 405:
            response = client.get(url, headers={"Range": "bytes=0-0"}, follow_redirects=True)
    except httpx.HTTPError:
        return None
    content_type = response.headers.get("content-type", "").lower()
    if response.status_code >= 400 or "text/html" in content_type:
        return None
    length = response.headers.get("content-length")
    return int(length) if length and length.isdigit() else None


def build_inventory(client: httpx.Client, years: list[int]) -> list[PdfItem]:
    seeds = seeded_candidates()
    items: list[PdfItem] = []
    seen: set[str] = set()
    used_names: set[str] = set()
    for year in years:
        candidates = pdf_links_from_page(client, year)
        candidates.extend(seeds.get(year, []))
        candidates.extend(generated_candidates(year))
        year_count = 0
        for url, title in candidates:
            if url in seen:
                continue
            seen.add(url)
            size = probe_pdf(client, url)
            if size is None:
                continue
            year_count += 1
            filename = output_name(year, url, title, year_count)
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            dedupe_index = 2
            while filename in used_names:
                filename = f"{stem}-{dedupe_index}{suffix}"
                dedupe_index += 1
            used_names.add(filename)
            items.append(PdfItem(year, url, filename, "official-ncrb", title, size))
        log(f"DISCOVER year={year} pdfs={year_count}")
    return items


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_pdf(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 5:
        return False
    with path.open("rb") as f:
        return f.read(5) == b"%PDF-"


def download_one(client: httpx.Client, item: PdfItem, state: dict[str, dict], dry_run: bool) -> str:
    target = OUT_DIR / item.filename
    state_key = item.url
    if state.get(state_key, {}).get("status") == "done" and is_pdf(target):
        return "skipped"
    if dry_run:
        log(f"DRYRUN year={item.year} target={target} url={item.url}")
        return "dry-run"
    OUT_DIR.mkdir(exist_ok=True)
    temp = target.with_suffix(target.suffix + ".part")
    log(f"DOWNLOAD year={item.year} target={target.name} url={item.url}")
    with client.stream("GET", item.url, follow_redirects=True) as response:
        response.raise_for_status()
        with temp.open("wb") as f:
            for chunk in response.iter_bytes(1024 * 1024):
                f.write(chunk)
    if not is_pdf(temp):
        temp.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded content is not a PDF: {item.url}")
    temp.replace(target)
    digest = sha256_file(target)
    bytes_written = target.stat().st_size
    state[state_key] = {
        "status": "done",
        "path": str(target),
        "sha256": digest,
        "bytes": bytes_written,
    }
    save_state(state)
    append_manifest(item, target, digest, bytes_written)
    log(f"DONE year={item.year} target={target.name} bytes={bytes_written} sha256={digest[:16]}")
    return "downloaded"


@APP.command()
def describe() -> None:
    """Print machine-readable CLI metadata."""
    print(
        json.dumps(
            {
                "commands": {
                    "run": {
                        "options": {
                            "--start-year": "Newest year to include. Defaults to website-discovered max year.",
                            "--end-year": "Oldest year to include. Defaults to website-discovered min year.",
                            "--dry-run": "Discover and log without writing PDFs.",
                            "--output-json": "Emit final summary as JSON.",
                        }
                    }
                },
                "outputs": [str(OUT_DIR), str(STATE_PATH), str(MANIFEST_PATH), str(LOG_PATH)],
            },
            indent=2,
        )
    )


@APP.command()
def run(
    start_year: int | None = typer.Option(None),
    end_year: int | None = typer.Option(None),
    dry_run: bool = typer.Option(False),
    output_json: bool = typer.Option(False),
) -> None:
    """Download official NCRB Crime in India PDFs into a flat pdfs/ directory."""
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,*/*"}
    with httpx.Client(headers=headers, timeout=30.0, follow_redirects=True) as client:
        years = discover_years(client)
        if start_year is not None:
            years = [year for year in years if year <= start_year]
        if end_year is not None:
            years = [year for year in years if year >= end_year]
        if not years:
            raise typer.BadParameter("No years matched the requested range.")
        log(f"START years={min(years)}-{max(years)} count={len(years)} dry_run={dry_run}")
        inventory = build_inventory(client, years)
        state = load_state()
        counts = {"downloaded": 0, "skipped": 0, "dry-run": 0, "failed": 0}
        for item in inventory:
            try:
                result = download_one(client, item, state, dry_run)
                counts[result] += 1
            except Exception as exc:
                counts["failed"] += 1
                log(f"ERROR year={item.year} url={item.url} error={exc}")
        summary = {
            "years": [min(years), max(years)],
            "inventory": len(inventory),
            "counts": counts,
            "output_dir": str(OUT_DIR),
            "manifest": str(MANIFEST_PATH),
            "log": str(LOG_PATH),
        }
        log(f"SUMMARY {json.dumps(summary, sort_keys=True)}")
        if output_json:
            print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        APP()
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        raise
