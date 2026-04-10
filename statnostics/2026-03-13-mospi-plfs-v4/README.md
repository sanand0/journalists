# PLFS 2024 Data Cards — v4

5 SVG data cards for the **Periodic Labour Force Survey Annual Report 2024** (v4 analysis).

These cards surface findings about labour market outcomes across gender, marital status, household role, occupation, and educational credential among young Indians aged 21–34.

## Upstream sources

| Resource | Path |
|----------|------|
| Key insights | `../../data/mospi-plfs/v4/insights.md` |
| Output CSVs | `../../data/mospi-plfs/v4/outputs/` |
| Analysis script | `../../data/mospi-plfs/v4/analyze.py` |

## Cards

| # | SVG | SOP | Claim |
|---|-----|-----|-------|
| 01 | [01-household-wife-role-cliff.svg](01-household-wife-role-cliff.svg) | [SOP](01-household-wife-role-cliff.md) | Married graduate women listed as 'spouse of head' are 4× less likely to hold regular jobs vs those listed as 'self' |
| 02 | [02-years-long-job-search.svg](02-years-long-job-search.svg) | [SOP](02-years-long-job-search.md) | 50.2% of urban married graduate women have been searching for work for 3+ years |
| 03 | [03-teaching-nursing-precarity.svg](03-teaching-nursing-precarity.svg) | [SOP](03-teaching-nursing-precarity.md) | Primary teachers earn ₹12,175/month median — less than a third of a software developer's ₹42,500 |
| 04 | [04-teaching-gender-pay-gap.svg](04-teaching-gender-pay-gap.svg) | [SOP](04-teaching-gender-pay-gap.md) | Women primary teachers earn ₹10,000/month median vs ₹20,000 for men in the same role |
| 05 | [05-degree-vs-diploma.svg](05-degree-vs-diploma.svg) | [SOP](05-degree-vs-diploma.md) | Engineering degree holders earn ₹35,475 median vs ₹18,000 for below-grad diploma holders |

## Usage

To view cards locally, serve via HTTP (SVGs use web fonts):

```bash
cd statnostics/2026-03-13-mospi-plfs-v4
python -m http.server 8080
# then open http://localhost:8080/
```

Or open `index.html` (if present) for a gallery view.

## Data notes

- All figures are from PLFS Annual Survey 2024 microdata
- Weights are applied throughout (column `mult` or equivalent multiplier)
- "Strictly formal" = written contract + paid leave + any social security benefit
- Age filter for card 01–02: 25–34; for cards 03–05: 21–34
