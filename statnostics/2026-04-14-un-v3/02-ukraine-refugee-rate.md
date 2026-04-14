# Verification SOP — Ukraine Refugee Rate (Card 02)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script to generate all source CSVs:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match SM_POP_REFG --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

The source data is UN SDG Global Database indicator **SM_POP_REFG_OR** (Refugee population by country or territory of origin per 100,000 population). The analysis script reads raw UN SDG API JSON and produces CSVs in `v3/outputs/`.

## What this card is saying

Ukraine has the sixth-highest refugee-origin rate in the world: 11,970 refugees per 100,000 people (approximately 12% of its population). This places it *above* Afghanistan (9,820 per 100,000 — rank 8), which receives far more news coverage as a refugee source country. The top spots are held by Western Sahara (22,512), Venezuela (18,469), Syria (17,632), and South Sudan (16,352). The card highlights that war in a middle-income country can displace a comparable share of the population to long-running conflicts in lower-income countries.

## Fastest way to verify

Open `v3/outputs/refugee_rate.csv` and sort by `value` descending. Confirm Ukraine appears in positions 4–8 and Afghanistan appears 1–3 rows below Ukraine in the top-10 list. Confirm the per-100,000 values match those on the card.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/refugee_rate.csv` | Refugees per 100,000 by country of origin, all reporting areas |
| `v3/analyze_un_data.py` | Indicator SM_POP_REFG_OR, top-N filtering logic |

## Exact rows

Open `v3/outputs/refugee_rate.csv`, sort by `value` descending, take top 8:

| Rank | Country | Refugees per 100,000 |
|---|---|---|
| 1 | Western Sahara | 22,512 |
| 2 | Venezuela | 18,469 |
| 3 | Syrian Arab Republic | 17,632 |
| 4 | South Sudan | 16,352 |
| 5 | Eritrea | 13,442 |
| 6 | Ukraine | 11,970 |
| 7 | Central African Republic | 11,025 |
| 8 | Afghanistan | 9,820 |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| Ukraine: 11,970 per 100K | 11,970 | Exact match |
| Afghanistan: 9,820 per 100K | 9,820 | Exact match |
| "~12% of population" | 11,970 / 100,000 ≈ 11.97% | Rounded to "≈12%" |
| Ukraine above Afghanistan | Rank 6 vs Rank 8 | Both in global top 10 |

## Common ways to mis-verify

- **"Refugees" definition**: This indicator counts UNHCR-recognised refugees (and asylum seekers in some versions). It does not count internally displaced persons (IDPs). Ukraine's IDP count is far larger; the 11,970 figure is only those who crossed international borders.
- **Population base**: The per-100,000 rate depends on the denominator (population estimate). Verify the analysis uses 2024 UN population estimates for consistency.
- **Western Sahara**: Western Sahara has an extremely small resident population, making its rate artificially high relative to absolute refugee numbers. The card correctly shows the rate, not the absolute count.
- **Year**: Confirm the analysis uses the most recently reported year (likely 2023 or 2024 data).

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match SM_POP_REFG --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/refugee_rate.csv`.

## Pre-publication checklist

- [ ] Confirm Ukraine value = 11,970 per 100,000 in source CSV
- [ ] Confirm Afghanistan value = 9,820 per 100,000 in source CSV
- [ ] Confirm Ukraine ranks above Afghanistan (closer to #1)
- [ ] Confirm "~12%" is a correct rounding of 11,970/100,000
- [ ] Confirm the 8 countries listed on the card are the true top 8 (no omitted countries between them)
- [ ] Confirm data year is stated and consistent across all 8 rows
