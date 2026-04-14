# Verification SOP — Seed & Crop Diversity (Card 06)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match ER_CBD_SMTA --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Source: UN SDG Global Database indicator **ER_CBD_SMTA** (Number of Standard Material Transfer Agreements, SMTAs, concluded under the International Treaty on Plant Genetic Resources for Food and Agriculture, by country).

## What this card is saying

India is the #2 recipient of Standard Material Transfer Agreements (SMTAs) globally, with 12,095 in 2025 — more than 5× China's 2,334, and accounting for 66.7% of all SMTAs heading to Southern Asia. Germany leads with 16,566. Meanwhile, 56 of 151 treaty members (37.09%) have signed the International Treaty on Plant Genetic Resources for Food and Agriculture but have not yet established a domestic framework to make their participation operational.

## Fastest way to verify

Open `v3/outputs/seed_smta_country_rank.csv`. Sort by `smta_count` descending. India should be rank 2 with 12,095. Germany should be rank 1 with 16,566. Filter for `subregion = "Southern Asia"` and sum `smta_count` — India's share of that subtotal should be ~66.7%.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/seed_smta_country_rank.csv` | All countries by SMTA count, ranked highest to lowest |
| `v3/outputs/seed_smta_india_peers.csv` | India plus top comparison countries (Germany, China) |
| `v3/outputs/seed_treaty_summary.csv` | Treaty membership and framework status counts |

## Exact rows

`seed_smta_country_rank.csv` — top 10 rows by smta_count:

| rank | country | area_code | smta_count |
|------|---------|-----------|-----------|
| 1 | Germany | 276 | 16,566 |
| 2 | India | 356 | 12,095 |
| 3 | Italy | 380 | 8,267 |
| 4 | France | 250 | 4,489 |
| 5 | Mexico | 484 | 4,234 |
| 6 | Spain | 724 | 3,076 |
| 7 | Netherlands | 528 | 2,896 |
| 8 | United States of America | 840 | 2,829 |
| 9 | Canada | 124 | 2,515 |
| 10 | China | 156 | 2,334 |

`seed_treaty_summary.csv`:

| treaty_members | framework_members | signed_but_no_framework | share_no_framework |
|---|---|---|---|
| 151 | 95 | 56 | 37.09% |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| India: 12,095 SMTAs | 12,095 | Exact match |
| Germany: 16,566 | 16,566 | Exact match |
| India rank #2 | rank_high_to_low = 2 | Exact match |
| "5× more than China" | 12,095 / 2,334 = 5.18× | Displayed as "5×", rounds correctly |
| "66.7% of Southern Asia" | 12,095 / (sum of subregion=Southern Asia) | Verify ratio in CSV |
| "56 of 151 members" | 56 signed_but_no_framework, 151 total | Exact match |

## Common ways to mis-verify

- **SMTA direction**: SMTAs are counted per *receiving* country. India's 12,095 are agreements where Indian institutions or researchers received crop genetic material — not where India sent material.
- **Treaty vs. framework**: "151 treaty members" = parties to the ITPGRFA. "No domestic framework" means they have ratified but not enacted the national legislation needed to participate in the multilateral system.
- **Year**: Confirm data is for the 2025 reporting period. Earlier years show different rankings.
- **Subregion totals**: Southern Asia may include Bangladesh, Nepal, Pakistan, Sri Lanka, etc. Verify which UN M49 subregion codes are included before computing the 66.7% share.

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match ER_CBD_SMTA --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/seed_smta_country_rank.csv`.

## Pre-publication checklist

- [ ] Confirm India smta_count = 12,095 in source CSV
- [ ] Confirm Germany smta_count = 16,566 (rank 1)
- [ ] Confirm India rank_high_to_low = 2
- [ ] Compute India/China ratio: 12,095 / 2,334 ≥ 5.0
- [ ] Verify India's share of Southern Asia SMTAs = 66.7% (±0.5%)
- [ ] Confirm treaty_members = 151, signed_but_no_framework = 56
- [ ] Verify data period is 2025
- [ ] Check no duplicate country rows in ranking CSV
