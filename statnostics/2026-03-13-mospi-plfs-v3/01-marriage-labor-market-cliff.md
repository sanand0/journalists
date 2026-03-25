# Verification SOP: marriage labour-market cliff

Verifies `01-marriage-labor-market-cliff.svg`.

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

- The card is about **women aged 25-34 with a college degree**.
- The chart itself uses a very specific control cell: **urban women, graduate+, regular wage/salary households**.
- Within that cell, the card shows a steep shift from **current-week regular salaried work** to **current-week domestic duties only** when comparing **never married** and **currently married** women.
- The wording must stay **descriptive**. It should not be rewritten as proof that marriage *causes* the shift.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `This is not just a class-composition story`
   - `55.8% for the married group and 7.1% for the never-married group`
   - `27.5 percentage points more likely`
2. Open `v3/outputs/marriage_control_cells_household_type.csv`.
3. Filter to:
   - `sector = urban`
   - `edu_band = graduate+`
   - `household_type = regular wage/salary earning`
4. Confirm the exact row values below.

## Source files to open

- `v3/insights.md`
  - Use this to verify the narrative framing and the caution that the finding is descriptive.
- `v3/outputs/marriage_control_cells_household_type.csv`
  - This is the **exact row behind the slope chart**.
- `v3/outputs/marriage_weighted_model.csv`
  - Use this to justify the softer wording `is linked to` in the deck.
- `v3/outputs/marriage_gradplus_state_compare.csv`
  - Use this as a robustness check showing that the pattern appears in multiple states.
- `v3/analyze.py`
  - The export for the household-type control cell is in the block that writes `marriage_control_cells_household_type.csv`.

## Exact row behind the chart

Spreadsheet row filter in `marriage_control_cells_household_type.csv`:

- `sector`: `urban`
- `edu_band`: `graduate+`
- `household_type`: `regular wage/salary earning`

Exact row values:

- `married_n`: `2201`
- `never_married_n`: `1003`
- `domestic_married_pct`: `55.8`
- `domestic_never_married_pct`: `7.1`
- `salaried_married_pct`: `25.1`
- `salaried_never_married_pct`: `57.3`
- `domestic_gap_pts`: `48.8`
- `salaried_gap_pts`: `-32.2`

## Card text -> source check

| Card element | Source value | Verification note |
|---|---:|---|
| `57% in salaried work` (never married) | `57.3%` | Rounded down from 57.3 to a whole number. |
| `7% in domestic duties` (never married) | `7.1%` | Rounded from 7.1. |
| `25% in salaried work` (married) | `25.1%` | Rounded from 25.1. |
| `56% in domestic duties` (married) | `55.8%` | Rounded from 55.8. |
| Scope note `Urban women, college degree+, in salaried households` | same row filter | This note is not decorative; it is the exact subgroup definition for the chart. |

## How the deck is supported

The deck says marriage `is linked to` leaving paid work for domestic duties. That wording is supported by `marriage_weighted_model.csv`:

- `outcome = domestic_only` -> `married_effect_points = 27.52`
- `outcome = regular_salaried` -> `married_effect_points = -16.65`
- controls = `state + sector + education band + social group + household type + religion`

That file is the reason the deck uses **linked to** rather than a purely visual comparison sentence.

## Robustness check for a sceptical editor

If someone says the chart is just one narrow urban household slice, open `marriage_gradplus_state_compare.csv` and verify that the broader graduate pattern is still large in multiple states:

- Andhra Pradesh: domestic `68.8%` married vs `11.9%` never married
- Tamil Nadu: domestic `66.1%` married vs `13.5%` never married

This does **not** replace the chart row; it is a robustness file.

## Important technical note

The chart compares two **Current Weekly Status** outcomes, not a lifetime occupation field:

- `domestic duties only`
- `worked as regular salaried/wage employee`

So if a reviewer checks the wrong PLFS status lens, the numbers will not match.

## Common ways to mis-verify this card

- Using **all women** instead of women aged 25-34.
- Using **all graduates** instead of the exact `urban + graduate+ + regular wage/salary household` control cell.
- Using **principal activity** instead of **CWS Status** for the slope-chart endpoints.
- Treating the `after marriage` arrow as if the survey tracks the same women over time. It does not; this is a cross-sectional comparison of currently married vs never married groups.
- Rewriting the headline/deck in a causal way.

## If you want to rerun the tables

From the downloaded `mospi-plfs/` workspace root:

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

Then reopen the same CSVs and confirm the row still matches the card.

## Pre-publication checklist

- [ ] The chart row is filtered to `urban / graduate+ / regular wage/salary earning`.
- [ ] The displayed percentages are rounded correctly from 57.3, 7.1, 25.1, and 55.8.
- [ ] The deck still says `linked to`, not `caused by`.
- [ ] The footnote still says `Descriptive, not causal`.
- [ ] No one has replaced the subgroup note with a broader claim about all Indian women.
