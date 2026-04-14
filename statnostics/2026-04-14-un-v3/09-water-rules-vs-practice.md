# Verification SOP — Water Rules vs. Practice (Card 09)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match ER_WAT_PRDU --latest-only --max-jobs 1
uv run download_un_data.py download --match ER_WAT_PART --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Source: Two UN SDG indicators joined:
- **ER_WAT_PRDU**: Degree to which water-related national frameworks clearly specify the roles and responsibilities of all institutions (procedure score — 10 = clearly defined, 5 = not clearly defined)
- **ER_WAT_PART**: Degree of integrated water resources management implementation, focusing specifically on participation of water users in decision-making (participation score — 1=low, 2=moderate, 3=high)

## What this card is saying

Of 104 reporting areas with data for both indicators, 91 (87.5%) have clearly defined procedures for water-user participation in law. However, only 28 of those 104 (26.9%) achieve high actual participation in practice (score 3). The rulebook dramatically outpaces reality. Notably, Nepal is an outlier: it lacks clearly defined rules yet achieves high participation in practice — suggesting community water governance can work bottom-up even without legal frameworks. India does **not** appear in this dataset's local water slice (no matching data row for India combining both indicators).

## Fastest way to verify

Open `v3/outputs/water_participation_summary.csv`. Check: total_areas=104, clearly_defined_count=91, high_participation_count=28. Compute: 91/104=87.5%, 28/104=26.9%.

Open `v3/outputs/water_participation_country_scores.csv` and filter:
- Nepal: procedure_score=5 (not clearly defined), participation_score=3 (high) → the "surprise" country
- Bangladesh: procedure_score=10, participation_score=1 (low)
- Indonesia: procedure_score=10, participation_score=3 (high)
- Pakistan: procedure_score=10, participation_score=1 (low)
- Viet Nam: procedure_score=10, participation_score=3 (high)

Confirm India has no row or is filtered out of the dataset.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/water_participation_summary.csv` | Totals: areas with data, clearly defined count, high participation count |
| `v3/outputs/water_participation_country_scores.csv` | All 104 countries with their procedure and participation scores |
| `v3/outputs/water_participation_india_peers.csv` | South/Southeast Asian peers — note India is absent |
| `v3/outputs/water_participation_clear_but_low_cases.csv` | The 14 areas with clearly defined rules but low participation (the "stuck" group) |

## Exact rows

`water_participation_summary.csv`:

| total_areas | clearly_defined_count | clearly_defined_pct | high_participation_count | high_participation_pct | clear_but_low_count |
|---|---|---|---|---|---|
| 104 | 91 | 87.50% | 28 | 26.92% | 14 |

Key country rows from `water_participation_country_scores.csv`:

| country | procedure_score | participation_score | notes |
|---------|----------------|--------------------|----|
| Nepal | 5 | 3 | Not clearly defined, yet HIGH participation — the "surprise" |
| Bangladesh | 10 | 1 | Clear rules, LOW participation |
| Indonesia | 10 | 3 | Clear rules, HIGH participation |
| Pakistan | 10 | 1 | Clear rules, LOW participation |
| Viet Nam | 10 | 3 | Clear rules, HIGH participation |
| India | — | — | **Not in this dataset** |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| "87.5% have clearly defined rules" | 91/104 = 87.50% | Exact match |
| "Only 26.9% achieve high participation" | 28/104 = 26.92% | Rounds to 26.9% ✓ |
| "104 areas with data" | total_areas = 104 | Exact match |
| Nepal surprise callout | procedure=5, participation=3 | Exact match |
| Bangladesh: clear rules, LOW | procedure=10, participation=1 | Exact match |
| Indonesia: clear rules, HIGH | procedure=10, participation=3 | Exact match |
| Pakistan: clear rules, LOW | procedure=10, participation=1 | Exact match |
| Viet Nam: clear rules, HIGH | procedure=10, participation=3 | Exact match |

## Common ways to mis-verify

- **India not in dataset**: India has no matching row in the combined ER_WAT_PRDU × ER_WAT_PART dataset. This is worth confirming — India may have data for one indicator but not the other, or may be under a different area code. Do not infer India's water governance status from this card.
- **Score scale**: Procedure score is binary in practice (10 = clearly defined, 5 = not). Participation score is 1/2/3. Do not average these or treat them as commensurable scales.
- **"Clearly defined" threshold**: The card uses procedure_score=10 as the threshold for "clearly defined". Verify whether the UN source uses exactly this cutoff or a different threshold in its methodology.
- **28 vs. 14**: 28 areas have HIGH participation overall. 14 areas have clearly defined rules but LOW participation (the "stuck" group). These are different subsets — do not confuse them.
- **Nepal is an outlier, not a model**: Nepal's combination of no clear rules but high participation may reflect traditional community irrigation systems (like the *kulo* system). This is a legitimate surprise worth flagging but should not be generalized.

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match ER_WAT_PRDU --latest-only --max-jobs 1
uv run download_un_data.py download --match ER_WAT_PART --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/water_participation_summary.csv`.

## Pre-publication checklist

- [ ] Confirm total_areas = 104
- [ ] Confirm clearly_defined_count = 91; 91/104 = 87.5% ✓
- [ ] Confirm high_participation_count = 28; 28/104 = 26.9% ✓
- [ ] Confirm Nepal: procedure_score=5, participation_score=3 (the "surprise" case)
- [ ] Confirm Bangladesh, Pakistan: procedure=10, participation=1 (clear rules, low practice)
- [ ] Confirm Indonesia, Viet Nam: procedure=10, participation=3 (clear rules, high practice)
- [ ] Confirm India is NOT in this dataset — note this in any editorial context
- [ ] Verify data period is 2025
- [ ] Check that procedure score scale is 10/5 (not 1–10 continuous)
