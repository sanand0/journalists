# Verification SOP — Long Job Search (Card 02)

## If you do not have the `data/` folder

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
./download_plfs.sh
uv run v4/analyze.py
```

## What this card is saying

Among graduate women aged 25–34 in urban areas who are currently married and actively seeking work, 50.2% have been searching for more than 3 years. This is substantially higher than the equivalent share for rural married graduate women (38.8%), urban never-married graduate women (29.6%), and urban graduate men (31.3%). The card highlights the specific burden of an extended job search facing urban married graduate women.

## Fastest way to verify

Open `v4/outputs/graduate_women_jobseeker_duration_marital_25_34.csv` — filter for sector=urban, marital_status=currently married, and read the y3plus_pct column (50.2).

For the comparison groups, open `v4/outputs/graduate_jobseeker_duration_25_34.csv` — filter for sex=male, sector=urban to get men (31.3%); and `graduate_women_jobseeker_duration_marital_25_34.csv` for rural married (38.8%) and urban never-married (29.6%).

## Source files to open

| File | What it contains |
|------|-----------------|
| `v4/outputs/graduate_women_jobseeker_duration_marital_25_34.csv` | Duration by sector x marital status for graduate women jobseekers |
| `v4/outputs/graduate_jobseeker_duration_25_34.csv` | Duration by sex x sector for all graduate jobseekers |
| `v4/analyze.py` | Section creating these CSVs — filter: graduate+, aged 25–34, currently seeking work |

## Exact rows

`graduate_women_jobseeker_duration_marital_25_34.csv`:
- sector=urban, marital_status=currently married → y3plus_pct=50.2
- sector=rural, marital_status=currently married → y3plus_pct=38.8
- sector=urban, marital_status=never married → y3plus_pct=29.6

`graduate_jobseeker_duration_25_34.csv`:
- sex=male, sector=urban → y3plus_pct=31.3

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| 50.2% urban married | 50.2 | Exact match |
| 38.8% rural married | 38.8 | Exact match |
| 31.3% urban men | 31.3 | Exact match |
| 29.6% urban never-married | 29.6 | Exact match |

## Common ways to mis-verify

- Do not use the overall female graduate jobseeker file without filtering by marital status — it gives a different (blended) figure.
- The "3+ years" column is y3plus_pct, not the sum of y1_to_2 + y2_to_3.
- Men's figure (31.3%) comes from a different CSV than the women's figures.

## If you want to rerun

```bash
cd journalists/data/mospi-plfs
uv run v4/analyze.py
```

Then open both `v4/outputs/graduate_women_jobseeker_duration_marital_25_34.csv` and `v4/outputs/graduate_jobseeker_duration_25_34.csv`.

## Pre-publication checklist

- [ ] Confirm 50.2 in graduate_women_jobseeker_duration_marital_25_34.csv (urban + currently married)
- [ ] Confirm 38.8 (rural + currently married), 29.6 (urban + never married)
- [ ] Confirm 31.3 from graduate_jobseeker_duration_25_34.csv (male, urban)
- [ ] Population filter: graduate+, aged 25–34, currently seeking work (unemployed or seeking)
