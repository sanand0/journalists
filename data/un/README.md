# UN Data

This directory contains a resumable downloader for `https://data.un.org` plus the downloaded outputs and catalog metadata.

The README starts with the data itself: what is available, how the files are structured, and what the content looks like. The downloader usage comes after that.

## Data Overview

Source:
- UN Data SDMX REST API at `https://data.un.org/ws/rest/`

Live catalog endpoint:
- `https://data.un.org/ws/rest/dataflow`

Catalog snapshot currently stored locally:
- [data/catalog/dataflows.csv](/home/vscode/code/journalists/data/un/data/catalog/dataflows.csv)
- [data/catalog/dataflows.json](/home/vscode/code/journalists/data/un/data/catalog/dataflows.json)

As of April 14, 2026, the live catalog contained 15 dataflows across 6 agencies.

### Live Dataflows

The table below combines the live catalog with the local recent-year probe in [data/catalog/recent_availability.csv](/home/vscode/code/journalists/data/un/data/catalog/recent_availability.csv).

`latest_nonempty_year` means the newest year found in the local `2020` to `2026` probe window.
Blank values mean the probe did not find a non-empty year in that window, or the upstream API returned only failures in that range.

| Agency | Flow ID | Version | Name | Local latest_nonempty_year |
| --- | --- | --- | --- | --- |
| `ESTAT` | `DF_SEEA_AEA` | `1.3` | Air emission accounts | `2022` |
| `ESTAT` | `DF_SEEA_ENERGY` | `1.3` | Physical energy flow accounts | `2022` |
| `ESTAT` | `NASEC_IDCFINA_A` | `1.9` | Annual financial accounts | `2024` |
| `ESTAT` | `NASEC_IDCFINA_Q` | `1.9` | Quarterly financial accounts | `2025` |
| `ESTAT` | `NASEC_IDCNFSA_A` | `1.9` | Annual non-financial accounts | |
| `ESTAT` | `NASEC_IDCNFSA_Q` | `1.9` | Quarterly non-financial accounts | `2020` |
| `ESTAT` | `NA_MAIN` | `1.9` | NA Main Aggregates | `2025` |
| `IAEG` | `DF_UNDATA_MDG` | `1.2` | SDMX-MDGs | |
| `IAEG-SDGs` | `DF_SDG_GLH` | `1.24` | SDG Harmonized Global Dataflow | `2026` |
| `UIS` | `DF_UNData_UIS` | `1.1` | SDMX_UIS_UNData | |
| `UNSD` | `DF_UNDATA_COUNTRYDATA` | `1.4` | SDMX-CountryData | |
| `UNSD` | `DF_UNDATA_ENERGY` | `1.2` | UNSD Energy Statistics | `2024` |
| `UNSD` | `DF_UNData_EnergyBalance` | `1.0` | Energy Balance DataFlow | `2023` |
| `UNSD` | `DF_UNData_UNFCC` | `1.0` | SDMX_GHG_UNDATA | `2021` |
| `WB` | `DF_UNDATA_WDI` | `1.0` | WB World Development Indicators | `2024` |

## Data Structure

Downloaded files are:
- gzipped CSV files
- one API flow per file
- one requested year window per file
- stored under `data/downloads/{agency}/{flow-slug}/by-year/`

Filename pattern:

```text
{agency}__{flow-slug}__period-{year}__fetched-{date}.csv.gz
```

Example:

```text
data/downloads/iaeg-sdgs/sdg-harmonized-global-dataflow/by-year/iaeg-sdgs__sdg-harmonized-global-dataflow__period-2026__fetched-2026-04-13.csv.gz
```

Important nuance:
- the filename `period-{year}` reflects the API query window, not necessarily the internal time grain
- a file downloaded for `period-2025` may still contain `TIME_PERIOD` values like `2025-Q1` and `2025-Q2`

### Row Model

Each row is an SDMX observation. In practice that means:
- many leading columns are coded dimensions
- there is usually one explicit time column, typically `TIME_PERIOD`
- there is one observation value column, typically `OBS_VALUE`
- additional columns carry unit, status, source, or quality metadata

Columns are not uniform across flows. The exact schema varies by dataset.

Common columns seen across files:
- `DATAFLOW`: source flow identifier, for example `IAEG-SDGs:DF_SDG_GLH(1.24)`
- `FREQ`: frequency code such as `A` or `Q`
- `TIME_PERIOD`: observation period such as `2026` or `2025-Q1`
- `OBS_VALUE`: numeric observation value
- `OBS_STATUS`: status flag
- `UNIT_MULT`: power-of-ten scaling factor

Common dimension columns seen in different flows:
- `REF_AREA`
- `SERIES`
- `SEX`
- `AGE`
- `ACTIVITY`
- `PRODUCT`
- `REF_SECTOR`
- `COUNTERPART_AREA`
- `UNIT_MEASURE`

Important interpretation note:
- values are still mostly coded, not fully human-decoded
- for example `REF_AREA`, `UNIT_MEASURE`, `ACTIVITY`, and `SERIES` often contain SDMX codes rather than descriptive labels
- this repository currently stores the observation files, not a full local expansion of all code lists and DSD metadata

## Content Examples

### SDG Harmonized Global Dataflow

Representative file:
- [iaeg-sdgs__sdg-harmonized-global-dataflow__period-2026__fetched-2026-04-13.csv.gz](/home/vscode/code/journalists/data/un/data/downloads/iaeg-sdgs/sdg-harmonized-global-dataflow/by-year/iaeg-sdgs__sdg-harmonized-global-dataflow__period-2026__fetched-2026-04-13.csv.gz)

Observed structure:
- annual observations
- country or area in `REF_AREA`
- indicator in `SERIES`
- observation value in `OBS_VALUE`
- source freshness in `DATA_LAST_UPDATE`

Header and sample rows:

```csv
DATAFLOW,FREQ,REPORTING_TYPE,SERIES,REF_AREA,SEX,AGE,URBANISATION,INCOME_WEALTH_QUANTILE,EDUCATION_LEV,OCCUPATION,CUST_BREAKDOWN,COMPOSITE_BREAKDOWN,DISABILITY_STATUS,ACTIVITY,PRODUCT,TIME_PERIOD,OBS_VALUE,OBS_STATUS,UNIT_MULT,UNIT_MEASURE,BASE_PER,NATURE,TIME_DETAIL,COMMENT_OBS,TIME_COVERAGE,UPPER_BOUND,LOWER_BOUND,SOURCE_DETAIL,COMMENT_TS,GEO_INFO_URL,GEO_INFO_TYPE,CUST_BREAKDOWN_LB,DATA_LAST_UPDATE
IAEG-SDGs:DF_SDG_GLH(1.24),A,G,ER_BDY_KMGBFT14,1,_T,_T,_T,_T,_T,_T,_T,_T,_T,_T,_T,2026,158,A,0,NUMBER,,N,2026,,,,,CHM / WESR,,,,,2026-03-24T00:00:00
IAEG-SDGs:DF_SDG_GLH(1.24),A,G,ER_BDY_KMGBFT14,1,_T,_T,_T,_T,_T,_T,_T,KMGBFT14_ACHIEVED,_T,_T,_T,2026,50,A,0,NUMBER,,N,2026,,,,,CHM / WESR,,,,,2026-03-24T00:00:00
```

Current local row count:
- `9359` rows in the 2026 slice

### ESTAT NA Main Aggregates

Representative file:
- [estat__na-main-aggregates__period-2025__fetched-2026-04-13.csv.gz](/home/vscode/code/journalists/data/un/data/downloads/estat/na-main-aggregates/by-year/estat__na-main-aggregates__period-2025__fetched-2026-04-13.csv.gz)

Observed structure:
- quarterly observations inside a file fetched for a yearly query window
- national accounts dimensions such as `REF_SECTOR`, `INSTR_ASSET`, `ACTIVITY`, `EXPENDITURE`, `PRICES`
- values in `OBS_VALUE`

Header and sample rows:

```csv
DATAFLOW,FREQ,ADJUSTMENT,REF_AREA,COUNTERPART_AREA,REF_SECTOR,COUNTERPART_SECTOR,ACCOUNTING_ENTRY,STO,INSTR_ASSET,ACTIVITY,EXPENDITURE,UNIT_MEASURE,PRICES,TRANSFORMATION,TIME_PERIOD,OBS_VALUE,OBS_STATUS,CONF_STATUS,COMMENT_OBS,EMBARGO_DATE,REF_PERIOD_DETAIL,REPYEARSTART,REPYEAREND,TIME_FORMAT,TIME_PER_COLLECT,REF_YEAR_PRICE,DECIMALS,TABLE_IDENTIFIER,TITLE,TITLE_COMPL,UNIT_MULT,LAST_UPDATE,COMPILING_ORG,COMMENT_DSET,COMMENT_TS,PRE_BREAK_VALUE,DATA_COMP,CURRENCY,DISS_ORG
ESTAT:NA_MAIN(1.9),Q,N,AR,W0,S1,S1,D,P3,_Z,_Z,_T,XDC,Q,N,2025-Q1,163248,A,F,,,C,,,P3M,S,2004,0,,,,6,,6O0,,,,,,
ESTAT:NA_MAIN(1.9),Q,N,AR,W0,S1,S1,D,P3,_Z,_Z,_T,XDC,Q,N,2025-Q2,172202,A,F,,,C,,,P3M,S,2004,0,,,,6,,6O0,,,,,,
```

Current local row count:
- `3235` rows in the 2025 slice

### ESTAT Quarterly Financial Accounts

Representative file:
- [estat__quarterly-financial-accounts__period-2025__fetched-2026-04-13.csv.gz](/home/vscode/code/journalists/data/un/data/downloads/estat/quarterly-financial-accounts/by-year/estat__quarterly-financial-accounts__period-2025__fetched-2026-04-13.csv.gz)

Observed structure:
- quarterly accounting observations
- dimensions include `CONSOLIDATION`, `ACCOUNTING_ENTRY`, `STO`, `INSTR_ASSET`, `VALUATION`, `CURRENCY_DENOM`

Header and sample rows:

```csv
DATAFLOW,FREQ,ADJUSTMENT,REF_AREA,COUNTERPART_AREA,REF_SECTOR,COUNTERPART_SECTOR,CONSOLIDATION,ACCOUNTING_ENTRY,STO,INSTR_ASSET,MATURITY,EXPENDITURE,UNIT_MEASURE,CURRENCY_DENOM,VALUATION,PRICES,TRANSFORMATION,CUST_BREAKDOWN,TIME_PERIOD,OBS_VALUE,OBS_STATUS,CONF_STATUS,COMMENT_OBS,EMBARGO_DATE,REF_PERIOD_DETAIL,REPYEARSTART,REPYEAREND,TIME_FORMAT,TIME_PER_COLLECT,CUST_BREAKDOWN_LB,REF_YEAR_PRICE,DECIMALS,TABLE_IDENTIFIER,TITLE,TITLE_COMPL,UNIT_MULT,LAST_UPDATE,COMPILING_ORG,COMMENT_DSET,OBS_EDP_WBB,COLL_PERIOD,COMMENT_TS,GFS_ECOFUNC,GFS_TAXCAT,PRE_BREAK_VALUE,DATA_COMP,CURRENCY,DISS_ORG
ESTAT:NASEC_IDCFINA_Q(1.9),Q,N,AT,W0,S1,S1,N,A,F,F,_Z,_Z,XDC,_T,S,V,N,_T,2025-Q1,40740,P,F,,,,,,P3M,,,,2,,,,6,,,,,,,,,,,,
ESTAT:NASEC_IDCFINA_Q(1.9),Q,N,AT,W0,S1,S1,N,A,F,F,_Z,_Z,XDC,_T,S,V,N,_T,2025-Q2,20496,P,F,,,,,,P3M,,,,2,,,,6,,,,,,,,,,,,
```

Current local row count:
- `130424` rows in the 2025 slice

### ESTAT Annual Financial Accounts

Representative file:
- [estat__annual-financial-accounts__period-2024__fetched-2026-04-13.csv.gz](/home/vscode/code/journalists/data/un/data/downloads/estat/annual-financial-accounts/by-year/estat__annual-financial-accounts__period-2024__fetched-2026-04-13.csv.gz)

Observed structure:
- annual accounting observations
- similar coded sector and instrument dimensions as the quarterly variant

Header and sample rows:

```csv
DATAFLOW,FREQ,ADJUSTMENT,REF_AREA,COUNTERPART_AREA,REF_SECTOR,COUNTERPART_SECTOR,CONSOLIDATION,ACCOUNTING_ENTRY,STO,INSTR_ASSET,MATURITY,EXPENDITURE,UNIT_MEASURE,CURRENCY_DENOM,VALUATION,PRICES,TRANSFORMATION,CUST_BREAKDOWN,TIME_PERIOD,OBS_VALUE,OBS_STATUS,CONF_STATUS,COMMENT_OBS,EMBARGO_DATE,REF_PERIOD_DETAIL,REPYEARSTART,REPYEAREND,TIME_FORMAT,TIME_PER_COLLECT,CUST_BREAKDOWN_LB,REF_YEAR_PRICE,DECIMALS,TABLE_IDENTIFIER,TITLE,TITLE_COMPL,UNIT_MULT,LAST_UPDATE,COMPILING_ORG,COMMENT_DSET,OBS_EDP_WBB,COLL_PERIOD,COMMENT_TS,GFS_ECOFUNC,GFS_TAXCAT,PRE_BREAK_VALUE,DATA_COMP,CURRENCY,DISS_ORG
ESTAT:NASEC_IDCFINA_A(1.9),A,N,HK,W1,S1,S1,N,A,F,F,_Z,_Z,XDC,_T,S,V,N,_T,2024,479850,A,F,,,,--01-01,,P1Y,,,,6,,,,6,,1B0,,,,,,,,,,1B0
ESTAT:NASEC_IDCFINA_A(1.9),A,N,HK,W1,S1,S1,N,L,F,F,_Z,_Z,XDC,_T,S,V,N,_T,2024,967114,A,F,,,,--01-01,,P1Y,,,,6,,,,6,,1B0,,,,,,,,,,1B0
```

Current local row count:
- `20` rows in the 2024 slice

## On-Disk Layout

By default the repository writes under `data/`:

```text
data/
  catalog/
    dataflows.csv
    dataflows.json
    recent_availability.csv
  downloads/
    {agency}/
      {flow-slug}/
        by-year/
          {agency}__{flow-slug}__period-{year}__fetched-{date}.csv.gz
  logs/
    download.log
  state/
    downloads.sqlite3
```

## Data Caveats

- the upstream UN API is inconsistent for some flows and years and often returns HTTP `500`
- some catalog entries work for older slices but fail for recent slices
- coded SDMX values are stored as-is; this repository does not yet build a fully decoded local warehouse of code lists
- a file named for a year window may still contain quarterly values in `TIME_PERIOD`

## Data Downloader

`download_un_data.py` downloads data from the UN Data SDMX REST API into resumable year-sliced `csv.gz` files.

The script is designed to:
- discover the live dataflow catalog from `https://data.un.org/ws/rest/dataflow`
- prioritize recent data first
- save data in an organized directory structure
- resume cleanly across runs
- skip existing output files by default
- only re-download existing data when `--force` is passed

## Requirements

- `uv`
- network access to `https://data.un.org`

The script is self-contained and uses PEP 723 metadata, so no separate virtualenv or `requirements.txt` is needed.

## How To Run

Show top-level help:

```bash
uv run download_un_data.py --help
```

Fetch the live catalog only:

```bash
uv run download_un_data.py catalog
```

Probe dataflows to find the newest non-empty year:

```bash
uv run download_un_data.py probe --start-year 2020 --end-year 2026
```

Run a recent-first download batch:

```bash
uv run download_un_data.py download --start-year 2020 --end-year 2026 --max-jobs 12
```

## Commands

### `catalog`

Fetches the live UN dataflow catalog and writes:
- `data/catalog/dataflows.json`
- `data/catalog/dataflows.csv`

Example:

```bash
uv run download_un_data.py catalog --data-dir data
```

Arguments:
- `--data-dir PATH`: base directory for outputs, logs, and state. Default: `data`
- `--verbose`: enable debug logging

### `probe`

Checks dataflows breadth-first from newest to oldest year and records the newest year that appears to have data.

Writes:
- `data/catalog/recent_availability.csv`

Example:

```bash
uv run download_un_data.py probe --data-dir data --start-year 2020 --end-year 2026 --concurrency 2
```

Arguments:
- `--data-dir PATH`: base directory for outputs. Default: `data`
- `--start-year INTEGER`: oldest year to consider. Default: `1900`
- `--end-year INTEGER`: newest year to consider. Default: current year
- `--concurrency INTEGER`: concurrent probe requests. Default: `2`
- `--match TEXT`: only probe flows whose key, name, or slug contains this text
- `--refresh-catalog / --no-refresh-catalog`: refresh live catalog before probing. Default: refresh
- `--verbose`: enable debug logging

### `download`

Downloads year slices newest-first into `csv.gz` files.

Examples:

Download a broad recent-first batch:

```bash
uv run download_un_data.py download --data-dir data --start-year 2020 --end-year 2026 --max-jobs 12
```

Download only the newest known year for one flow:

```bash
uv run download_un_data.py download --data-dir data --match DF_SDG_GLH --latest-only --max-jobs 1
```

Re-use existing catalog/probe state without refreshing:

```bash
uv run download_un_data.py download --data-dir data --no-refresh-catalog --no-probe-latest --max-jobs 10
```

Force a re-download even if matching output files already exist:

```bash
uv run download_un_data.py download --data-dir data --match DF_SDG_GLH --latest-only --max-jobs 1 --force
```

Arguments:
- `--data-dir PATH`: base directory for outputs. Default: `data`
- `--start-year INTEGER`: oldest year to download. Default: `1900`
- `--end-year INTEGER`: newest year to consider. Default: current year
- `--concurrency INTEGER`: concurrent downloads. Default: `2`
- `--probe-concurrency INTEGER`: concurrent probe requests before download. Default: `2`
- `--match TEXT`: only download matching flows
- `--refresh-catalog / --no-refresh-catalog`: refresh live catalog first. Default: refresh
- `--probe-latest / --no-probe-latest`: probe newest non-empty year before downloading. Default: probe
- `--latest-only / --no-latest-only`: only download the latest non-empty year per flow. Default: off
- `--force`: re-download even when matching output files already exist
- `--max-jobs INTEGER`: cap the number of year slices in the current run
- `--verbose`: enable debug logging

## Resume And Re-download Behavior

Default behavior:
- if a matching output file already exists for a flow/year, the script will skip it
- it will skip even if the SQLite job record is missing or stale
- it will not attempt a network request for that slice

Override behavior:
- pass `--force` to re-download slices even when output files already exist

This means on-disk files are treated as the source of truth for already-downloaded slices.

## Useful Examples

Run a safe incremental batch:

```bash
uv run download_un_data.py download --data-dir data --start-year 2020 --end-year 2026 --max-jobs 20 --concurrency 2 --probe-concurrency 2
```

Target a specific family of flows:

```bash
uv run download_un_data.py download --data-dir data --match UNSD --start-year 2020 --end-year 2026 --max-jobs 10
```

Probe only a single flow:

```bash
uv run download_un_data.py probe --data-dir data --match DF_SDG_GLH --start-year 2024 --end-year 2026
```

Check job status counts:

```bash
sqlite3 data/state/downloads.sqlite3 'select status,count(*) from jobs group by status order by status;'
```

Count rows in a downloaded file:

```bash
qsv count data/downloads/iaeg-sdgs/sdg-harmonized-global-dataflow/by-year/iaeg-sdgs__sdg-harmonized-global-dataflow__period-2026__fetched-2026-04-13.csv.gz
```
