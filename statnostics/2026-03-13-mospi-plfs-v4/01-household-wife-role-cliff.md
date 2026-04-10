# Verification SOP — Wife Role Cliff (Card 01)

## If you do not have the `data/` folder

Clone the journalists repo and run the v4 analysis script to generate all source CSVs:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
./download_plfs.sh   # fetches plfs.parquet
uv run v4/analyze.py      # generates v4/outputs/ CSVs
```

The source data is the PLFS 2024 microdata. The `download_plfs.sh` script fetches a clean parquet extract from [Vonter/india-plf-survey](https://github.com/Vonter/india-plf-survey/releases). The `v4/analyze.py` script applies all filters and produces the `v4/outputs/*.csv` files cited below.

## What this card is saying

Among currently married graduate women aged 25–34, those whose household position is recorded as "spouse of head" (indicating they live in extended/joint families headed by someone else) are far more likely to report being engaged exclusively in domestic duties (57.2%) and far less likely to hold a regular salaried job (13.8%) compared to those recorded as the household head themselves or as a daughter (43.1% domestic-only, 30.7% regular salaried). The card presents a descriptive comparison by household role, not a causal claim, though it notes that regression analysis controlling for child presence, state, and social group yields similar differences (+19 pts domestic-only, −18 pts regular salaried for wife/spouse role).

## Fastest way to verify

Search for "household role" or "wife role" in `v4/insights.md`.

Open `v4/outputs/married_graduate_household_role_grouped.csv` and look for the two rows: `wife_role_in_extended_household` and `self_or_child_role`.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v4/outputs/married_graduate_household_role_grouped.csv` | Two-row summary: wife-role vs self/daughter, with domestic_only_pct and regular_salaried_pct |
| `v4/outputs/married_graduate_household_role_model.csv` | Regression/model output showing adjusted effect sizes |
| `v4/analyze.py` | Section creating household_role_grouped — filter: currently married, graduate+, aged 25–34 |

## Exact rows

Open `v4/outputs/married_graduate_household_role_grouped.csv`:

| Field | wife_role_in_extended_household | self_or_child_role |
|---|---|---|
| sample_n | 4,947 | 451 |
| domestic_only_pct | 57.2 | 43.1 |
| regular_salaried_pct | 13.8 | 30.7 |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| 57.2% domestic-only (wife role) | 57.2 | Exact match |
| 13.8% regular salaried (wife role) | 13.8 | Exact match |
| 43.1% domestic-only (self/daughter) | 43.1 | Exact match |
| 30.7% regular salaried (self/daughter) | 30.7 | Exact match |
| +19 pts domestic-only | model coefficient | Rounded from regression output |
| −18 pts regular salaried | model coefficient | Rounded from regression output |

## Common ways to mis-verify

- Don't compare this CSV with the detail CSV (`married_graduate_household_role_detail.csv`) — that has more granular role categories not grouped the same way.
- The n=4,947 for wife role is weighted survey count, not unweighted — do not expect it to match raw respondent counts.
- The +19/−18 pt annotation comes from regression outputs in the model CSV, not directly from the grouped CSV.

## If you want to rerun

```bash
cd journalists/data/mospi-plfs
uv run v4/analyze.py
```

Then open `v4/outputs/married_graduate_household_role_grouped.csv`.

## Pre-publication checklist

- [ ] Confirm 57.2 in married_graduate_household_role_grouped.csv matches card
- [ ] Confirm 13.8 and 30.7 match card
- [ ] Confirm sample sizes n=4,947 and n=451 match CSV
- [ ] Confirm annotation "+19 pts / −18 pts" sourced from model output
- [ ] Population filter: currently married, graduate+, aged 25–34
