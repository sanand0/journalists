# Verification SOP — Livestock No Backup (Card 03)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script to generate all source CSVs:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match ER_GRF_ANIM --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

The source data is UN SDG Global Database indicator **ER_GRF_ANIMRCNTN** (Proportion of local breeds for which sufficient genetic resources have been stored to allow reconstitution of the breed in case of extinction). The analysis script reads raw UN SDG API JSON and produces CSVs in `v3/outputs/`.

## What this card is saying

The UN tracks two things per country: how many **local livestock breeds** are recorded and how many have **enough stored genetic material** to be reconstituted if extinct (stored semen, embryos, etc.). In 80 of 118 reporting areas (67.8%), the answer to the second question is zero — not a single local breed has adequate backup material. India has 297 local breeds but only 44 are backed up (14.8%). China leads with 872 breeds but only 96 backed up (11.0%). Sri Lanka has 20 breeds and zero backed up.

## Fastest way to verify

Open `v3/outputs/livestock_backup.csv`. The column `breeds_total` gives local breed count; `breeds_backed_up` gives the reconstitution-ready count. Calculate `areas_with_zero = count where breeds_backed_up == 0`. Confirm = 80 of 118 reporting areas.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/livestock_backup.csv` | Country-level: local breeds total, backed up, share |
| `v3/analyze_un_data.py` | Indicator ER_GRF_ANIMRCNTN, aggregation logic |

## Exact rows

Open `v3/outputs/livestock_backup.csv`:

| Country | Local breeds | Backed up | Share |
|---|---|---|---|
| China | 872 | 96 | 11.0% |
| India | 297 | 44 | 14.8% |
| Indonesia | 173 | 9 | 5.2% |
| Sri Lanka | 20 | 0 | 0.0% |

Global summary:

| Metric | Value |
|---|---|
| Total reporting areas | 118 |
| Areas with zero breeds backed up | 80 |
| Share | 67.8% |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| "80 of 118 reporting areas have ZERO breeds backed up" | 80/118 | Exact match |
| "67.8% of all reporting areas" | 80/118 = 67.8% | Derived |
| China: 872 breeds, 96 backed up, 11.0% | CSV values | Exact match |
| India: 297 breeds, 44 backed up, 14.8% | CSV values | Exact match |
| Indonesia: 173 breeds, 9 backed up, 5.2% | CSV values | Exact match |
| Sri Lanka: 20 breeds, 0 backed up, 0.0% | CSV values | Exact match |

## Common ways to mis-verify

- **"Backed up" definition**: The indicator counts breeds where stored genetic material is *sufficient for full reconstitution* — not merely whether any sample exists. A country may have partial samples that don't qualify.
- **Local breeds only**: This indicator tracks *local* breeds (not cosmopolitan/international breeds like Holstein or Merino). Do not compare with FAO Domestic Animal Diversity Information System (DAD-IS) total breed counts.
- **Reporting area vs country**: Some "reporting areas" are territories, not sovereign nations. The 118 total may differ from UN member country count.
- **India 14.8% vs 44/297**: 44/297 = 14.82% — confirm this rounds to 14.8% in the source, not 15%.

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match ER_GRF_ANIM --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/livestock_backup.csv`.

## Pre-publication checklist

- [ ] Confirm total reporting areas = 118
- [ ] Confirm areas with zero backed-up breeds = 80 (67.8%)
- [ ] Confirm India: 297 total, 44 backed up, 14.8%
- [ ] Confirm China: 872 total, 96 backed up, 11.0%
- [ ] Confirm Indonesia: 173 total, 9 backed up, 5.2%
- [ ] Confirm Sri Lanka: 20 total, 0 backed up
- [ ] Confirm "backed up" means sufficient for full reconstitution (not partial storage)
