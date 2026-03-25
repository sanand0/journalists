# Verification SOP: hidden homemaker work

Verifies `02-hidden-homemaker-work.svg`.

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

- The base population is **women whose principal activity status is `attended domestic duties only`**.
- Even inside that homemaker-coded group, **8.4%** still show up as workers in the **current week**.
- The hidden work is mostly **own-account** or **unpaid family** work, not formal salaried work.
- The pattern is strongly rural.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `8.4% still show up as working in the current week`
   - `44.5% are own-account workers and 44.4% are unpaid family workers`
   - `59.3% of the broad homemaker group but 86.0% of the hidden weekly workers`
2. Open `v3/outputs/hidden_work_national_benchmark.csv` and confirm the one-row benchmark.
3. Open `v3/outputs/hidden_work_weekly_work_composition.csv` and confirm the composition rows.
4. Open `v3/outputs/hidden_work_rural_urban.csv` and confirm the rural concentration calculation.

## Source files to open

- `v3/insights.md`
  - Narrative summary and the concentration framing.
- `v3/outputs/hidden_work_national_benchmark.csv`
  - Confirms the headline benchmark: `8.4%` worked in the current week; `13.4%` reported subsidiary work.
- `v3/outputs/hidden_work_weekly_work_composition.csv`
  - Exact work-status mix behind the stacked bar.
- `v3/outputs/hidden_work_rural_urban.csv`
  - Lets you verify the `59%` vs `86%` rural concentration note.
- `v3/analyze.py`
  - The `hidden_domestic` view defines the base population.

## Base population definition

The analysis creates a `hidden_domestic` view for:

- `Sex = female`
- `Principal Activity Status = attended domestic duties only`

Inside that view:

- `worked_week = 1` means `CWS Status` starts with `worked...`
- `subsidiary = 1` means `Subsidiary Work Engagement = yes`

That distinction matters: **the card uses the weekly-work measure, not the subsidiary-work measure**.

## One-row benchmark to check

In `hidden_work_national_benchmark.csv`, verify the single row:

- `sample_n = 58203`
- `total_m = 136.211`
- `worked_week_pct = 8.4`
- `subsidiary_pct = 13.4`

## Composition behind the stacked bar

Check `hidden_work_weekly_work_composition.csv`.

| Card element | CSV row | Exact share |
|---|---|---:|
| `44.5% own-account` | `worked in h.h. enterprise (self-employed): own account worker` | `44.5%` |
| `44.4% unpaid family` | `worked as helper in h.h. enterprise (unpaid family worker)` | `44.4%` |
| grey casual/public-work segment | `other casual` + `MGNREG` | `4.7% + 3.9% = 8.6%` |
| `2.2% formal` | `worked as regular salaried/wage employee` | `2.2%` |

Very small rows that are **not called out on the card** but do exist in the CSV:

- `worked as casual wage labour in public works other than MGNREG works` -> `0.2%`
- `worked in h.h. enterprise (self-employed): employer` -> `0.2%`

That is why the displayed bar is an editorial simplification rather than a label for every tiny category.

## Rural concentration check

Use `hidden_work_rural_urban.csv`.

Broad homemaker group:

- rural total = `80.837` million-equivalent
- urban total = `55.374` million-equivalent
- rural share of broad homemaker group = `59.3%`

Hidden weekly workers:

- rural working_m = `9.875`
- urban working_m = `1.611`
- rural share of hidden weekly workers = `86.0%`

That is the source for the card note:

- `Rural women are 86% of hidden workers despite being 59% of the homemaker group`

## Common ways to mis-verify this card

- Confusing **principal activity** with **current week status**.
- Checking the `13.4%` subsidiary-work figure instead of the `8.4%` current-week-work figure.
- Expecting the stacked bar labels to sum perfectly to 100 after rounding. The CSV has additional tiny `0.2%` rows and rounded shares.
- Treating `formal` as all paid work. On this card, `formal` is only the regular salaried row.

## If you want to rerun the tables

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

Then reopen the same three CSVs and compare them to the card.

## Pre-publication checklist

- [ ] The base population is women with principal status `attended domestic duties only`.
- [ ] The big stat is the `8.4%` current-week-work figure, not the `13.4%` subsidiary-work figure.
- [ ] The composition labels match the CSV rows exactly.
- [ ] The rural note is checked using `hidden_work_rural_urban.csv`, not guessed from the SVG.
- [ ] The copy still makes clear that this is hidden work across PLFS lenses, not a contradiction in one single variable.
