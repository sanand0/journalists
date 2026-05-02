#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas>=2.2",
#   "pyarrow>=15",
#   "XlsxWriter>=3.2",
# ]
# ///
"""Step 1 — Download the citizen-survey ZIP from Harvard Dataverse, then convert to parquet + xlsx.

Downloads the ZIP file (skip if already present), extracts the .dta file inside, and
writes a Parquet copy plus an Excel workbook (Summary / Preview / Variables / Data sheets).

Usage
-----
    uv run 01_download_and_prepare.py
    uv run 01_download_and_prepare.py [--zip PATH] [--out-dir DIR]
    uv run 01_download_and_prepare.py --force          # re-download and reconvert even if outputs exist
    uv run 01_download_and_prepare.py --force-download  # re-download ZIP only, skip reconvert if outputs exist
    uv run 01_download_and_prepare.py --force-convert   # skip re-download, reconvert from existing ZIP

Examples
--------
    uv run 01_download_and_prepare.py
    uv run 01_download_and_prepare.py --out-dir /tmp/out
    uv run 01_download_and_prepare.py --force
"""

from __future__ import annotations

import argparse
import io
import sys
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import xlsxwriter

HERE = Path(__file__).parent

DOWNLOAD_URL  = "https://dataverse.harvard.edu/api/access/datafile/13322834"
DEFAULT_ZIP   = HERE / "FINAL DATA-CITIZEN_SURVEY_ALL_DATA-FINAL_SKS_09.05.2025.zip"

PREVIEW_COLUMNS = [
    "state_code", "state_name", "district_code", "district_name",
    "block_code", "block_name", "village_code", "village_name",
    "cs_id", "consent", "date_of_interview", "residence",
    "a2b_age", "uhc_index",
]


# ── helpers ────────────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)



def download_zip(url: str, dest: Path) -> None:
    """Download *url* to *dest*, showing a progress bar. Atomic via a temp file.

    Harvard Dataverse returns 403 without a browser-like User-Agent, so we send
    one explicitly and stream the response manually.
    """
    tmp = dest.with_suffix(".tmp")
    log("Downloading from Harvard Dataverse…")
    log(f"  URL : {url}")
    log(f"  Dest: {dest}")

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; citizen-survey-downloader/1.0)"},
    )

    started = time.time()
    last_print = 0.0
    chunk = 65_536  # 64 KB

    try:
        with urllib.request.urlopen(req) as resp, open(tmp, "wb") as fh:
            total = int(resp.headers.get("Content-Length") or 0)
            downloaded = 0
            while True:
                buf = resp.read(chunk)
                if not buf:
                    break
                fh.write(buf)
                downloaded += len(buf)
                now = time.time()
                if now - last_print >= 0.25:
                    elapsed = now - started or 1e-9
                    speed = downloaded / elapsed / 1_048_576
                    mb = downloaded / 1_048_576
                    if total:
                        pct = min(downloaded / total * 100, 100)
                        tot = total / 1_048_576
                        print(f"\r  Download: {pct:5.1f}%  {mb:.1f}/{tot:.1f} MB  {speed:.2f} MB/s   ",
                              end="", flush=True)
                    else:
                        print(f"\r  Download: {mb:.1f} MB  {speed:.2f} MB/s   ",
                              end="", flush=True)
                    last_print = now
        print()  # newline after progress line
    except Exception:
        print()
        tmp.unlink(missing_ok=True)
        raise

    tmp.rename(dest)
    size_mb = dest.stat().st_size / 1_048_576
    log(f"Download complete — {size_mb:.1f} MB saved to {dest.name}")


def find_dta_in_zip(zip_path: Path) -> tuple[str, bytes, list[str]]:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        dta_files = [n for n in names if n.lower().endswith(".dta")]
        if not dta_files:
            raise FileNotFoundError(f"No .dta file found inside {zip_path}")
        dta_name = dta_files[0]
        return dta_name, zf.read(dta_name), names


def load_stata(dta_bytes: bytes) -> tuple[pd.DataFrame, dict[str, str]]:
    reader = pd.io.stata.StataReader(io.BytesIO(dta_bytes))
    labels = reader.variable_labels()
    df = reader.read(convert_categoricals=False)
    return df, labels


def safe_width(values: Iterable[object], min_w: int = 10, max_w: int = 40) -> int:
    return min(max(max(len(str(v)) for v in values if v is not None) + 2, min_w), max_w)


def write_df_sheet(
    wb: xlsxwriter.Workbook,
    name: str,
    frame: pd.DataFrame,
    hdr_fmt,
    sample_rows: int = 50,
) -> None:
    ws = wb.add_worksheet(name)
    ws.freeze_panes(1, 0)
    for ci, col in enumerate(frame.columns):
        ws.write(0, ci, col, hdr_fmt)
    sample = frame.head(sample_rows)
    for ci, col in enumerate(frame.columns):
        ws.set_column(ci, ci, safe_width([col] + sample.iloc[:, ci].fillna("").tolist()))
    for ri, row in enumerate(frame.itertuples(index=False, name=None), start=1):
        for ci, val in enumerate(row):
            if not pd.isna(val):
                ws.write(ri, ci, val)


def write_excel(
    df: pd.DataFrame,
    xlsx_path: Path,
    *,
    source_zip: Path,
    dta_name: str,
    zip_members: Sequence[str],
) -> None:
    preview_cols = [c for c in PREVIEW_COLUMNS if c in df.columns] or list(df.columns[:14])
    preview_df = df[preview_cols].head(10)
    variables_df = pd.DataFrame({
        "variable_name": df.columns,
        "label": [df.attrs.get("variable_labels", {}).get(c, "") for c in df.columns],
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_null_count": [int(df[c].notna().sum()) for c in df.columns],
    })

    wb = xlsxwriter.Workbook(str(xlsx_path), {"constant_memory": True})
    try:
        hdr = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#1F4E78",
                             "align": "center", "valign": "vcenter", "border": 1})
        lbl = wb.add_format({"bold": True, "bg_color": "#D9EAF7", "border": 1})

        # Summary sheet
        ws = wb.add_worksheet("Summary")
        ws.freeze_panes(1, 0)
        for ci, title in enumerate(["Metric", "Value"]):
            ws.write(0, ci, title, hdr)
        rows = [
            ("Source ZIP", source_zip.name),
            ("Source dataset inside ZIP", dta_name),
            ("Rows", int(df.shape[0])),
            ("Columns", int(df.shape[1])),
            ("Other files in ZIP", ", ".join(n for n in zip_members if n != dta_name)),
        ]
        for ri, (metric, value) in enumerate(rows, start=1):
            ws.write(ri, 0, metric, lbl)
            ws.write(ri, 1, value)
        ws.set_column(0, 0, 28)
        ws.set_column(1, 1, 100)

        write_df_sheet(wb, "Preview",   preview_df,   hdr)
        write_df_sheet(wb, "Variables", variables_df, hdr)

        # Data sheet (full dataset, constant-memory row-by-row)
        ws = wb.add_worksheet("Data")
        ws.freeze_panes(1, 0)
        for ci, col in enumerate(df.columns):
            ws.write(0, ci, col, hdr)
        sample = df.head(50)
        for ci, col in enumerate(df.columns):
            ws.set_column(ci, ci, safe_width([col] + sample.iloc[:, ci].fillna("").tolist()))
        total = len(df)
        for ri, row in enumerate(df.itertuples(index=False, name=None), start=1):
            for ci, val in enumerate(row):
                if not pd.isna(val):
                    ws.write(ri, ci, val)
            if ri % 5000 == 0:
                log(f"Excel rows written: {ri:,} / {total:,}")
    finally:
        wb.close()


# ── main ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--zip", type=Path, default=DEFAULT_ZIP,
                   help="Path to save / load the survey ZIP file")
    p.add_argument("--out-dir", type=Path, default=HERE,
                   help="Directory to write outputs (default: same folder as this script)")
    p.add_argument("--url", default=DOWNLOAD_URL,
                   help="Harvard Dataverse download URL (default: hardcoded datafile 13322834)")
    p.add_argument("--force", action="store_true",
                   help="Re-download the ZIP and reconvert even if all outputs already exist")
    p.add_argument("--force-download", action="store_true",
                   help="Re-download the ZIP even if it already exists (but skip reconvert if outputs present)")
    p.add_argument("--force-convert", action="store_true",
                   help="Reconvert from the existing ZIP even if parquet + xlsx already exist (no re-download)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. Download ────────────────────────────────────────────────────────────
    need_download = args.force or args.force_download or not args.zip.exists()

    if need_download:
        download_zip(args.url, args.zip)
    else:
        size_mb = args.zip.stat().st_size / 1_048_576
        log(f"ZIP already present — skipping download ({args.zip.name}, {size_mb:.1f} MB)")
        log("  Pass --force-download to re-download.")

    if not args.zip.exists():
        print(f"ERROR: ZIP not found after download step: {args.zip}", file=sys.stderr)
        return 1

    # ── 2. Convert ─────────────────────────────────────────────────────────────
    stem        = args.out_dir / args.zip.stem
    parquet_out = stem.with_suffix(".parquet")
    xlsx_out    = stem.with_suffix(".xlsx")

    need_convert = args.force or args.force_convert or not (parquet_out.exists() and xlsx_out.exists())

    if not need_convert:
        print("Converted outputs already exist — skipping conversion.")
        print(f"  Parquet : {parquet_out}")
        print(f"  Excel   : {xlsx_out}")
        print("Pass --force-convert (or --force) to reconvert.")
        print("\nNext step: run  uv run 02_verify_cards.py")
        return 0

    started = time.time()
    log(f"Reading ZIP: {args.zip.name}")
    dta_name, dta_bytes, zip_members = find_dta_in_zip(args.zip)

    log(f"Loading Stata dataset: {dta_name}")
    df, variable_labels = load_stata(dta_bytes)
    df.attrs["variable_labels"] = variable_labels
    log(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")

    log(f"Writing Parquet: {parquet_out.name}")
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, parquet_out, compression="snappy")

    log(f"Writing Excel: {xlsx_out.name}")
    write_excel(df, xlsx_out, source_zip=args.zip, dta_name=dta_name, zip_members=zip_members)

    elapsed = time.time() - started
    log("Done")
    print(
        f"\nSummary\n-------\n"
        f"Rows    : {df.shape[0]:,}\n"
        f"Columns : {df.shape[1]}\n"
        f"Parquet : {parquet_out}\n"
        f"Excel   : {xlsx_out}\n"
        f"Elapsed : {elapsed:.1f}s"
    )
    print("\nNext step: run  uv run 02_verify_cards.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
