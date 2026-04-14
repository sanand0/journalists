# Verification SOP — India Productivity Growth (Card 04)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script to generate all source CSVs:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match SL_EMP_PCAP --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

The source data is UN SDG Global Database indicator **SL_EMP_PCAP** (Annual growth rate of real GDP per employed person, %). The analysis script reads raw UN SDG API JSON and produces CSVs in `v3/outputs/`.

## What this card is saying

In the most recently reported year, real GDP per employed person in India grew by 5.12% — ranking it 11th globally among 181 reporting areas. The global median growth rate is 1.71%. India's rate is approximately 3× the median. Among South/Southeast Asian countries shown, India ranks third (behind Viet Nam at 5.74% and Bhutan at 5.44%) but well ahead of Bangladesh (2.36%) and Pakistan (0.26%). This is a labour productivity measure: the same worker is producing more output per year.

## Fastest way to verify

Open `v3/outputs/productivity_growth.csv`. Find the row where `area = "India"` and confirm `value ≈ 5.12`. Calculate the global median of the `value` column — confirm ≈ 1.71. Sort descending to confirm India's rank ≈ 11 of 181.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/productivity_growth.csv` | Annual GDP per employed person growth rate by country |
| `v3/analyze_un_data.py` | Indicator SL_EMP_PCAP, filtering and median calculation |

## Exact rows

Open `v3/outputs/productivity_growth.csv`, filter to Asia/shown countries, sort by `value` descending:

| Country | Growth rate (%) | Global rank |
|---|---|---|
| Viet Nam | 5.74 | ~9 |
| Bhutan | 5.44 | ~10 |
| **India** | **5.12** | **11** |
| China | 4.90 | ~13 |
| Nepal | 4.03 | ~20 |
| Sri Lanka | 3.99 | ~21 |
| Indonesia | 3.43 | ~26 |
| Bangladesh | 2.36 | ~50 |
| Pakistan | 0.26 | ~130 |

Global median across 181 areas: **1.71%**

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| India: 5.12% | 5.12 | Exact match |
| "3× the global median" | 5.12 / 1.71 ≈ 2.99 | Rounded to "3×" |
| "rank 11 of 181" | Sort descending, find India's position | Should be 11 |
| Global median: 1.71% | Median of `value` column | Derived |
| Viet Nam: 5.74% | 5.74 | Exact match |
| Pakistan: 0.26% | 0.26 | Exact match |

## Common ways to mis-verify

- **"Real" vs nominal**: This indicator uses *real* GDP growth (inflation-adjusted). Do not confuse with nominal GDP per capita growth rates from other sources.
- **Per employed person, not per capita**: The denominator is employed persons, not total population. A country with rising employment can show lower per-worker growth even if total output rises.
- **Year lag**: GDP productivity data for the most recent year is often preliminary. Confirm the analysis uses the latest finalized year, not a provisional estimate.
- **"3×" claim**: 5.12 / 1.71 = 2.99. The card rounds this to "3×". Verify this rounding is defensible (it is — within 0.5% of true value).

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match SL_EMP_PCAP --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/productivity_growth.csv`.

## Pre-publication checklist

- [ ] Confirm India value = 5.12% in source CSV
- [ ] Confirm global median = 1.71% (median of all rows in the file)
- [ ] Confirm India rank = 11 of 181 (or verify count of rows with value > 5.12)
- [ ] Confirm 5.12 / 1.71 ≥ 2.9 (displayed as "3×")
- [ ] Confirm all 9 country values shown on card match source CSV
- [ ] Confirm data year is consistent across all rows shown
