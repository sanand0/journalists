# Verification SOP — Youth Strategy Gap (Card 08)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match SL_CPA_YEMP --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Source: UN SDG Global Database indicator **SL_CPA_YEMP** (Proportion of countries with national policies for youth employment). The indicator uses a 4-point scale: 0=no strategy, 1=under development, 2=developed but not yet operational, 3=operationalized.

## What this card is saying

Only 72 of 185 reporting areas (38.92%) have a youth employment strategy that is actually operational (score 3). A further 67 areas (36.22%) have a written strategy sitting idle — developed but not yet operational (score 2). India scores 2: it has a plan on paper but has not operationalized it. China scores 3 (operational). Bangladesh is still under development (score 1).

## Fastest way to verify

Open `v3/outputs/youth_employment_strategy_summary.csv`. Check counts per score level. Sum all counts — should equal 185. Score 3 count (72) divided by 185 = 38.92% ≈ 39%. Open `v3/outputs/youth_employment_strategy_india_peers.csv` and confirm India score = 2.0.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/youth_employment_strategy_summary.csv` | Count and share of areas per score level |
| `v3/outputs/youth_employment_strategy_india_peers.csv` | India and regional peers with their scores |

## Exact rows

`youth_employment_strategy_summary.csv`:

| score | label | count | share |
|-------|-------|-------|-------|
| 3.0 | Operationalized | 72 | 38.92% |
| 2.0 | Developed, not operational | 67 | 36.22% |
| 1.0 | Under development | 40 | 21.62% |
| 0.0 | No strategy | 6 | 3.24% |
| **Total** | | **185** | 100% |

`youth_employment_strategy_india_peers.csv`:

| country | area_code | score | label | rank |
|---------|-----------|-------|-------|------|
| China | 156 | 3.0 | Operationalized | — |
| India | 356 | 2.0 | Developed, not operational | 100 |
| Indonesia | 360 | 2.0 | Developed, not operational | — |
| Pakistan | 586 | 2.0 | Developed, not operational | — |
| Bangladesh | 50 | 1.0 | Under development | — |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| "Only 39% of governments" | 72/185 = 38.92% | Rounds to 39% ✓ |
| "185 reporting areas" | Total count = 185 | Exact match |
| "67 more have a written plan sitting idle" | Score 2 count = 67 | Exact match |
| "India is one of them" | India score = 2.0 | Exact match |
| China: Operational | Score 3 | Exact match |
| India: Plan only | Score 2 | Exact match |
| Bangladesh: Under development | Score 1 | Exact match |
| India rank 100 | rank = 100 of 185 | Verify in CSV |

## Common ways to mis-verify

- **Score interpretation**: Score 2 ("developed but not operational") means the country has a written youth employment strategy document but has not yet implemented or activated it. Do not interpret it as "having some active measures" — the UN definition is binary: it either runs or it doesn't.
- **"39%"**: 72/185 = 38.919%, which rounds to 39%. Some sources may show 38.9% — both are correct; the card uses whole-number rounding.
- **India rank**: India's rank of 100 is within the sorted list of all 185 reporting areas. The sort order may vary by how ties (areas with same score) are broken. Verify the exact rank in the CSV.
- **Year**: Confirm data is from 2025 reporting period. Earlier periods may show India at a different score if the strategy was more recently developed.
- **Operational vs. effective**: Score 3 means a strategy is operationalized in policy terms — it does not measure whether the strategy is achieving employment outcomes. China scoring 3 does not imply its youth unemployment rate is low.

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match SL_CPA_YEMP --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/youth_employment_strategy_summary.csv`.

## Pre-publication checklist

- [ ] Confirm total reporting areas = 185
- [ ] Score 3 (operational) count = 72; 72/185 = 38.92% ≈ 39% ✓
- [ ] Score 2 (plan only) count = 67
- [ ] India score = 2.0 ("Developed but not operational")
- [ ] China score = 3.0 (Operational)
- [ ] Bangladesh score = 1.0 (Under development)
- [ ] Indonesia score = 2.0, Pakistan score = 2.0 — confirm in peers CSV
- [ ] Verify data period is 2025
- [ ] Confirm India's rank in the sorted list (displayed on card as reference, not on visual)
