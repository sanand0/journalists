# Verification SOP — Parliament Below Both Medians (Card 05)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script to generate all source CSVs:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match "SG_GEN_PARL|SG_PLT_RPTY" --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

The source data is two UN SDG Global Database indicators:
- **SG_GEN_PARL**: Proportion of seats held by women in national parliaments (%)
- **SG_PLT_RPTY**: Proportion of seats held by youth in national parliament (ratio)

The analysis script produces CSVs in `v3/outputs/`.

## What this card is saying

India's national parliament scores below the global median on both representation metrics simultaneously. Women hold 13.84% of parliamentary seats (global median: 27.68%), placing India 151st of 156 countries. Youth representation is measured as a ratio of 0.32 (global median: 0.65), placing India 138th of 156. Both metrics are in the bottom quartile globally. The card does not make causal claims — it documents the gap between India's current parliament and the global central tendency.

## Fastest way to verify

1. Open `v3/outputs/parliament_women.csv`. Find row `area = "India"`, confirm `value ≈ 13.84`. Compute median of all `value` rows, confirm ≈ 27.68. Sort ascending, find India's rank (151 of 156).
2. Open `v3/outputs/parliament_youth.csv`. Find row `area = "India"`, confirm `value ≈ 0.32`. Compute median, confirm ≈ 0.65. Find India's rank (138 of 156).

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/parliament_women.csv` | Women's share of parliamentary seats, all countries (%) |
| `v3/outputs/parliament_youth.csv` | Youth representation ratio, all countries |
| `v3/analyze_un_data.py` | Indicators SG_GEN_PARL and SG_PLT_RPTY, rank and median logic |

## Exact values

From `v3/outputs/parliament_women.csv`:

| Metric | Value |
|---|---|
| India value | 13.84% |
| Global median | 27.68% |
| India rank | 151 of 156 |

From `v3/outputs/parliament_youth.csv`:

| Metric | Value |
|---|---|
| India value | 0.32 |
| Global median | 0.65 |
| India rank | 138 of 156 |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| Women: 13.84% | 13.84 | Exact match |
| Women median: 27.68% | Median of parliament_women.csv | Derived |
| Women rank: 151 of 156 | Sort ascending, count rows below India | Should be 151 |
| Youth ratio: 0.32 | 0.32 | Exact match |
| Youth median: 0.65 | Median of parliament_youth.csv | Derived |
| Youth rank: 138 of 156 | Sort ascending, count rows below India | Should be 138 |

## Common ways to mis-verify

- **"Youth ratio" definition**: SG_PLT_RPTY is not simply "% of MPs under 45." It is the proportion of MPs aged under 45 *divided by* the proportion of the voting-age population aged under 45 — a representation ratio. A value of 1.0 means perfect proportionality; 0.32 means youth are represented at about one-third of their population share. Do not report this as "32% of MPs are young."
- **156 countries**: Not all UN members report both indicators. The 156 count is the number with data for *both* indicators in the same reference year. Confirm this is the common-year pool used for ranking.
- **"Women median 27.68%"**: This is the median across countries, not a weighted average. A country with one female MP and a country with 200 female MPs count equally. Do not confuse with global *average* (which tends to be higher due to large-population outliers).
- **Lower house vs total parliament**: Some indicators use lower/single house seats; others use combined. Confirm the analysis consistently uses one definition for India.

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match "SG_GEN_PARL|SG_PLT_RPTY" --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/parliament_women.csv` and `v3/outputs/parliament_youth.csv`.

## Pre-publication checklist

- [ ] Confirm India women's share = 13.84% in parliament_women.csv
- [ ] Confirm global women's median = 27.68% (median of all rows)
- [ ] Confirm India women's rank = 151 of 156 (ascending sort)
- [ ] Confirm India youth ratio = 0.32 in parliament_youth.csv
- [ ] Confirm global youth median = 0.65 (median of all rows)
- [ ] Confirm India youth rank = 138 of 156 (ascending sort)
- [ ] Confirm "youth ratio" is correctly defined in note (not "% of MPs under 45")
- [ ] Confirm both indicators use the same reference year
