# Verification SOP: MGNREG pay comparison

Verifies `06-mgnreg-pays-less.svg`.

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

- The main chart is about **rural men**.
- It uses **person-day diary wages**, not monthly earnings and not principal-status occupation.
- The card compares three hourly wage groups:
  - other casual work
  - MGNREG
  - other public works
- The women note at the bottom is secondary, and the state-variation warning is important context.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `57.02 per hour in other casual work, 45.17 in MGNREG, and 41.41 in other public works`
   - `41.66 per hour in other casual work versus 41.19 in MGNREG`
   - `women see an MGNREG premium in Andhra Pradesh and Chhattisgarh`
2. Open `v3/outputs/casual_person_day_rural.csv`.
3. Check the `male` rows for the three bar values and the `female` rows for the note.
4. Open `v3/outputs/casual_mgnreg_state_compare.csv` to verify the `wide variation` note.

## Source files to open

- `v3/insights.md`
  - Summary language and the state-variation context.
- `v3/outputs/casual_person_day_rural.csv`
  - Exact bar values used in the card.
- `v3/outputs/casual_mgnreg_state_compare.csv`
  - Supports the `state figures show wide variation` sentence.
- `v3/analyze.py`
  - Confirms the hourly measure is `SUM(w * day_wage) / SUM(w * day_hours)`.

## Exact rows to check in `casual_person_day_rural.csv`

### Rural men (main bars)

- `sex = male`, `status_group = other_casual`
  - `weighted_ratio_hourly = 57.02`
  - `avg_day_hours = 7.81`
  - `avg_day_wage = 464.71`
- `sex = male`, `status_group = mgnreg`
  - `weighted_ratio_hourly = 45.17`
  - `avg_day_hours = 5.64`
  - `avg_day_wage = 245.2`
- `sex = male`, `status_group = other_public_works`
  - `weighted_ratio_hourly = 41.41`
  - `avg_day_hours = 6.55`
  - `avg_day_wage = 255.14`

### Rural women (bottom note)

- `sex = female`, `status_group = other_casual` -> `weighted_ratio_hourly = 41.66`
- `sex = female`, `status_group = mgnreg` -> `weighted_ratio_hourly = 41.19`

## Card text -> source check

| Card element | Source value | Verification note |
|---|---:|---|
| `₹57/hr` | `57.02` | Rounded from 57.02. |
| `₹45/hr` | `45.17` | Rounded from 45.17. |
| `₹41/hr` | `41.41` | Rounded from 41.41. |
| `a quarter more than MGNREG` | `26.2%` more | The deck uses an everyday phrase; the exact gap is about 26.2%. |
| women note `₹41/hr` vs `₹42/hr` | `41.19` vs `41.66` | Rounded from 41.19 and 41.66. |

## Critical technical note

This CSV has **two hourly measures**:

- `weighted_ratio_hourly`
- `median_person_day_hourly`

The card uses **`weighted_ratio_hourly`**, not the median column.

If a reviewer checks the median column by mistake, the card will look wrong.

## State-variation note: exact rows to cite

In `casual_mgnreg_state_compare.csv`, female rows show why the note says state variation is wide.

Examples to quote/check:

- Andhra Pradesh: MGNREG minus other casual = `9.98`
- Chhattisgarh: `9.75`
- Tamil Nadu: `-9.95`
- Rajasthan: `-14.58`
- Meghalaya: `-15.7`
- Kerala: `-19.28`

That is the factual basis for `though state figures show wide variation`.

## Common ways to mis-verify this card

- Using `median_person_day_hourly` instead of `weighted_ratio_hourly`.
- Using all-India or urban rows instead of `sector = rural`.
- Treating this as a principal-occupation wage comparison rather than a diary-based person-day comparison.
- Ignoring the female note and assuming the headline applies equally to women.

## If you want to rerun the tables

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

## Pre-publication checklist

- [ ] The three bars come from the `male` rows in `casual_person_day_rural.csv`.
- [ ] The bottom note comes from the `female` rows in the same file.
- [ ] The review uses `weighted_ratio_hourly`, not the median column.
- [ ] The state-variation warning is backed by `casual_mgnreg_state_compare.csv`.
- [ ] The headline is not broadened into a claim that MGNREG always pays less in every state or for every subgroup.
