# Verification SOP — Migration Deaths Concentration (Card 07)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match SM_DTH_MIGR --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Source: UN SDG Global Database indicator **SM_DTH_MIGR** (Number of deaths and disappearances of migrants, disaggregated by sex, age and migration status). Primary data from IOM Missing Migrants Project.

## What this card is saying

Of 7,672 documented migration deaths globally in 2025, five transit areas account for 56.8%: Iran (1,387), Libya (1,125), Yemen (809), Myanmar (570), and Tunisia (469). The top 10 areas account for 77.3%. These are minimum counts of documented deaths — actual totals are higher. India ranks 31st with 17 recorded deaths; for South Asian migrants, the deadliness of the *route* matters far more than the country of origin.

## Fastest way to verify

Open `v3/outputs/migration_deaths_rank.csv`. Sort by `deaths_2025` descending. Check that Iran, Libya, Yemen, Myanmar, Tunisia are the top 5. Sum their deaths — should equal 4,360. Divide by global total (7,672) to confirm 56.83%.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/migration_deaths_rank.csv` | All areas by documented death count, ranked |
| `v3/outputs/migration_deaths_summary.csv` | Global total, top-5 total, top-10 total with shares |
| `v3/outputs/migration_deaths_concentration.csv` | Concentration statistics: top-N shares |

## Exact rows

`migration_deaths_rank.csv` — top 10:

| rank | area | deaths_2025 | cumulative_share |
|------|------|-------------|-----------------|
| 1 | Iran | 1,387 | 18.08% |
| 2 | Libya | 1,125 | 32.74% |
| 3 | Yemen | 809 | 43.28% |
| 4 | Myanmar | 570 | 50.71% |
| 5 | Tunisia | 469 | 56.83% |
| 6–10 | (next 5 combined) | 1,570 | 77.29% |
| 31 | India | 17 | — |

`migration_deaths_summary.csv`:

| global_total | top5_deaths | top5_share | top10_deaths | top10_share |
|---|---|---|---|---|
| 7,672 | 4,360 | 56.83% | 5,930 | 77.29% |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| "4,360 deaths in 2025" | 1387+1125+809+570+469 = 4,360 | Sum of top 5 |
| "56.8% of 7,672" | 4360/7672 = 56.83% | Rounds to 56.8% |
| "77.3% in just 10 areas" | 5930/7672 = 77.29% | Rounds to 77.3% |
| Iran: 1,387 | Source row | Exact match |
| Libya: 1,125 | Source row | Exact match |
| Yemen: 809 | Source row | Exact match |
| Myanmar: 570 | Source row | Exact match |
| Tunisia: 469 | Source row | Exact match |
| India: rank 31, 17 deaths | rank=31, deaths=17 | Exact match |

## Common ways to mis-verify

- **Minimum counts only**: SM_DTH_MIGR records *documented* deaths reported to the IOM Missing Migrants project. Unknown sea disappearances, desert deaths, and unrecovered bodies are not counted. The actual toll is much higher.
- **Transit vs. origin**: Iran, Libya, Yemen etc. are *transit areas* where deaths occur — not necessarily the migrants' country of origin. India's 17 deaths are deaths of people in transit in/near India, not deaths of Indian nationals abroad.
- **"Next 5"**: The 1,570 figure for ranks 6–10 is a derived sum. Verify by summing the five individual rows in the rank CSV.
- **Year definiton**: Confirm the UN SDG data uses calendar year 2025. IOM may use different aggregation periods.
- **Duplicate geographies**: Some migration corridors span multiple UN area codes. Check whether Libya appears as a single row or split (e.g. "Libya" vs. "North Africa").

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match SM_DTH_MIGR --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/migration_deaths_rank.csv`.

## Pre-publication checklist

- [ ] Confirm global total = 7,672 in source
- [ ] Confirm Iran = 1,387, Libya = 1,125, Yemen = 809, Myanmar = 570, Tunisia = 469
- [ ] Sum top 5 = 4,360; divide by 7,672 → 56.83% (rounds to 56.8% ✓)
- [ ] Sum top 10; divide by 7,672 → 77.29% (rounds to 77.3% ✓)
- [ ] Confirm India rank = 31, deaths = 17
- [ ] Note "minimum documented counts" caveat is visible on card ✓
- [ ] Verify data period is 2025
