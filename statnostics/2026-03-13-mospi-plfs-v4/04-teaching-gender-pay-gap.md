# Verification SOP — Teaching Gender Pay Gap (Card 04)

## If you do not have the `data/` folder

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
./download_plfs.sh
uv run v4/analyze.py
```

## What this card is saying

Among regular salaried primary school teachers aged 21–34, men earn a median of ₹20,000/month while women earn ₹10,000 — exactly half. For secondary education teachers, men earn ₹18,000 vs women ₹15,000. For other teaching professionals, men earn ₹12,000 vs women ₹6,000 (again 2x). The formal employment gap is also large: only 36.3% of women primary teachers have strictly formal jobs vs 53.5% of men.

## Fastest way to verify

Open `v4/outputs/selected_professions_gender_gaps_21_34.csv` and filter for teaching occupation rows.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v4/outputs/selected_professions_gender_gaps_21_34.csv` | Sex x occupation: median_salary, strict_formal_pct |
| `v4/analyze.py` | Section creating gender_gaps — filter: regular salaried, aged 21–34, by sex |

## Exact rows

`selected_professions_gender_gaps_21_34.csv` (teaching rows):

| sex | occupation | median_salary | strict_formal_pct |
|---|---|---|---|
| female | Primary School and Early Childhood Teachers | 10000.0 | 36.3 |
| male | Primary School and Early Childhood Teachers | 20000.0 | 53.5 |
| female | Secondary Education Teachers | 15000.0 | 28.9 |
| male | Secondary Education Teachers | 18000.0 | 46.3 |
| female | Other Teaching Professionals | 6000.0 | 5.2 |
| male | Other Teaching Professionals | 12000.0 | 11.9 |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| Women primary ₹10,000 | 10000.0 | Exact match |
| Men primary ₹20,000 | 20000.0 | Exact match |
| Women secondary ₹15,000 | 15000.0 | Exact match |
| Men secondary ₹18,000 | 18000.0 | Exact match |
| Women other ₹6,000 | 6000.0 | Exact match |
| Men other ₹12,000 | 12000.0 | Exact match |
| 36% women formal | 36.3 | Rounded to nearest % |
| 54% men formal | 53.5 | Rounded to nearest % |

## Common ways to mis-verify

- The annotation says "36%" and "54%" which are rounded from 36.3% and 53.5% — this is intentional rounding for annotation text.
- "Other Teaching Professionals" in the CSV refers to a different ISCO category than primary or secondary teachers — do not conflate.
- Formal% here is strict_formal_pct (all three conditions: contract + leave + security), not just written_contract_pct.

## If you want to rerun

```bash
cd journalists/data/mospi-plfs
uv run v4/analyze.py
```

Then open `v4/outputs/selected_professions_gender_gaps_21_34.csv`.

## Pre-publication checklist

- [ ] Confirm women primary ₹10,000 and men primary ₹20,000 in CSV
- [ ] Confirm women secondary ₹15,000 and men ₹18,000
- [ ] Confirm women other ₹6,000 and men ₹12,000
- [ ] Confirm strict_formal_pct: 36.3 (women primary) and 53.5 (men primary)
- [ ] Population: regular salaried, aged 21–34, teaching occupations
