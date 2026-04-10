# Verification SOP — Degree vs Diploma (Card 05)

## If you do not have the `data/` folder

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
./download_plfs.sh
uv run v4/analyze.py
```

## What this card is saying

Among those with technical engineering credentials aged 21–34 in the regular salaried workforce, those with an engineering degree earn ₹35,475/month median vs ₹18,000 for those with a below-graduate engineering diploma — nearly double. Degree-holders also have more than double the strictly formal job rate (43.2% vs 23.3%), a higher salaried employment rate (59.4% vs 47.4%), and far lower micro-firm share (4.1% vs 14.9%). The comparison highlights a sharp credential cliff in labour market outcomes.

## Fastest way to verify

Open `v4/outputs/technical_credential_quality_21_34.csv`. Look for the rows:
- `technical degree in engineering/technology`
- `diploma or certificate (below graduate level) in engineering/technology`

## Source files to open

| File | What it contains |
|------|-----------------|
| `v4/outputs/technical_credential_quality_21_34.csv` | Credential-level outcomes: salaried%, strict_formal%, median_salary, micro-firm% |
| `v4/analyze.py` | Section creating technical_credential_quality — filter: aged 21–34, technical education |

## Exact rows

`technical_credential_quality_21_34.csv`:

| credential | regular_pct | strict_formal_pct | median_regular_salary | micro_small_regular_pct |
|---|---|---|---|---|
| technical degree in engineering/technology | 59.4 | 43.2 | 35475.0 | 4.1 |
| diploma or certificate (below graduate level) in engineering/technology | 47.4 | 23.3 | 18000.0 | 14.9 |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| Degree salaried 59.4% | 59.4 | Exact match |
| Diploma salaried 47.4% | 47.4 | Exact match |
| Degree strict formal 43.2% | 43.2 | Exact match |
| Diploma strict formal 23.3% | 23.3 | Exact match |
| Degree median salary ₹35,475 | 35475.0 | Exact match |
| Diploma median salary ₹18,000 | 18000.0 | Exact match |
| Degree micro-firm 4.1% | 4.1 | Exact match |
| Diploma micro-firm 14.9% | 14.9 | Exact match |

## Common ways to mis-verify

- There are multiple diploma rows in the CSV (graduate-level and below-graduate-level, in engineering and other subjects). Use specifically `diploma or certificate (below graduate level) in engineering/technology` — not the graduate-level diploma or the other-subjects diploma.
- The `regular_pct` column represents salaried job rate (the card shows this as "SALARIED JOBS %").
- `micro_small_regular_pct` refers to workers in micro/small enterprises — these are workers in very small firms, not the firm size itself.

## If you want to rerun

```bash
cd journalists/data/mospi-plfs
uv run v4/analyze.py
```

Then open `v4/outputs/technical_credential_quality_21_34.csv`.

## Pre-publication checklist

- [ ] Confirm ₹35,475 for engineering degree (median_regular_salary)
- [ ] Confirm ₹18,000 for below-grad diploma
- [ ] Confirm strict_formal_pct: 43.2 (degree) vs 23.3 (diploma)
- [ ] Confirm micro_small_regular_pct: 4.1 (degree) vs 14.9 (diploma)
- [ ] Credential filter: specifically "below graduate level" engineering diploma, not graduate-level
