# Verification SOP: school-exit reasons split by gender

Verifies `07-school-dropout-gender-split.svg`.

## If you do not have the `data/` folder

These steps are meant to work even if you only received this cards folder.

Before verifying any card, download the original `mospi-plfs` analysis workspace used to make these graphics. The upstream repository is:

- `https://github.com/sanand0/journalists`
- analysis folder: `data/mospi-plfs/`
- latest story-ready analysis: `data/mospi-plfs/v3/`

The most direct way to get it is:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
```

If you downloaded only the `mospi-plfs/` folder as a zip or archive, start from that folder instead.

If `plfs.parquet` is not already present, fetch it and regenerate the v3 tables before checking the card:

```bash
./download_plfs.sh
./v3/analyze.py
```

Inside `mospi-plfs/`, you should have `README.md`, `download_plfs.sh`, `v3/analyze.py`, `v3/insights.md`, and `v3/outputs/`.

`README.md` in that workspace says `plfs.parquet` is a processed person-level PLFS 2024 file downloaded from the public `Vonter/india-plf-survey` repository. In the rest of this SOP, all source paths are relative to the downloaded `mospi-plfs/` workspace root, not to this `statnostics/` folder.

## What this card is saying

- The card is about **people aged 18-24 who attended school earlier but are not currently attending**.
- The main comparison is within the **currently married** subgroup.
- Women overwhelmingly cite **domestic chores**; men overwhelmingly cite **supplementing household income**.
- The bottom note adds a secondary robustness check for **never-married** youth.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `72.7% cite domestic chores`
   - `88.6% cite supplementing household income`
   - `women lean toward domestic chores (44.8%) while men overwhelmingly cite income (76.0%)`
2. Open `v3/outputs/school_exit_reasons_youth.csv`.
3. Filter to `age_band = 18-24`, then compare the `currently married` female and male rows.
4. Use the `never married` rows in the same age band to verify the bottom note.

## Source files to open

- `v3/insights.md`
  - Summary language and the secondary never-married comparison.
- `v3/outputs/school_exit_reasons_youth.csv`
  - Exact values used in the card.
- `v3/analyze.py`
  - Confirms the CSV is built from `Current Attendance Status LIKE 'attended but currently not attending%'`.

## Exact rows to check in `school_exit_reasons_youth.csv`

### Currently married, age 18-24 (main stat blocks)

- `sex = female`, `age_band = 18-24`, `marital_status = currently married`
  - `n = 8402`
  - `total_m = 21.11`
  - `weighted_domestic_chore_pct = 72.7`
  - `weighted_income_pct = 13.8`
- `sex = male`, `age_band = 18-24`, `marital_status = currently married`
  - `n = 2438`
  - `total_m = 6.156`
  - `weighted_domestic_chore_pct = 1.5`
  - `weighted_income_pct = 88.6`

### Never married, age 18-24 (bottom note)

- `sex = female`, `age_band = 18-24`, `marital_status = never married`
  - `weighted_domestic_chore_pct = 44.8`
  - `weighted_income_pct = 28.2`
- `sex = male`, `age_band = 18-24`, `marital_status = never married`
  - `weighted_domestic_chore_pct = 1.7`
  - `weighted_income_pct = 76.0`

## Card text -> source check

| Card element | Source value | Verification note |
|---|---:|---|
| women `73%` | `72.7%` | Rounded from 72.7. |
| men `89%` | `88.6%` | Rounded from 88.6. |
| women reason `domestic duties at home` | `attended but currently not attending - to attend domestic chores` | Editorial paraphrase of the attendance-status code. |
| men reason `earning household income` | `attended but currently not attending - to supplement household income` | Editorial paraphrase. |
| bottom note on never-married youth | women `44.8%`, men `76.0%` | Supports `same split appears, though less extreme`. |

## Exact filter behind this CSV

The export query defines the base pool as:

- `Age BETWEEN 15 AND 24`
- `Current Attendance Status LIKE 'attended but currently not attending%'`

So the card's phrase `left school` is reader-friendly shorthand for **attended earlier, not attending now**.

## Common ways to mis-verify this card

- Checking all youth instead of the `18-24` band.
- Missing the `currently married` filter for the main comparison.
- Assuming the reason labels come from a generic survey field; they come from specific `Current Attendance Status` strings.
- Treating `left school` as a formal administrative dropout definition rather than the PLFS attendance-status wording.

## If you want to rerun the tables

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

## Pre-publication checklist

- [ ] The main comparison uses the `currently married` 18-24 female and male rows.
- [ ] The displayed stats are rounded from 72.7 and 88.6.
- [ ] The bottom note is checked against the `never married` 18-24 rows.
- [ ] The copy does not imply a causal reason beyond what respondents/state categories report.
- [ ] The editor understands that `left school` is a paraphrase of `attended but currently not attending`.
