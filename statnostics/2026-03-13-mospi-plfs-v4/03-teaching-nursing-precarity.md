# Verification SOP — Teaching/Nursing Precarity (Card 03)

## If you do not have the `data/` folder

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
./download_plfs.sh
uv run v4/analyze.py
```

## What this card is saying

Among regular salaried workers aged 21–34, software developers earn a median ₹42,500/month and 76.6% hold strictly formal jobs (written contract + paid leave + social security). By contrast, primary school teachers earn ₹12,175/month median — less than a third of that — and only 42.2% are in strictly formal employment. Nursing and midwifery professionals fare even worse: ₹10,000 median, 35.7% strictly formal. This card challenges the perception that teaching and nursing offer stable, well-protected jobs.

## Fastest way to verify

Open `v4/outputs/selected_professions_quality_21_34.csv` and look at the four rows for: Software and Application Developers and Analysts; Primary School and Early Childhood Teachers; Secondary Education Teachers; Nursing and Midwifery Associate Professionals.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v4/outputs/selected_professions_quality_21_34.csv` | Occupation-level: median_salary, strict_formal_pct, sample_n |
| `v4/analyze.py` | Section creating selected_professions_quality — filter: regular salaried, aged 21–34 |

## Exact rows

| Occupation | median_salary | strict_formal_pct |
|---|---|---|
| Software and Application Developers and Analysts | 42500.0 | 76.6 |
| Primary School and Early Childhood Teachers | 12175.0 | 42.2 |
| Secondary Education Teachers | 16000.0 | 38.0 |
| Nursing and Midwifery Associate Professionals | 10000.0 | 35.7 |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| ₹42,500 software | 42500.0 | Exact match |
| ₹12,175 primary teachers | 12175.0 | Exact match |
| ₹16,000 secondary teachers | 16000.0 | Exact match |
| ₹10,000 nursing | 10000.0 | Exact match |
| 76.6% formal (software) | 76.6 | Exact match |
| 42.2% formal (primary) | 42.2 | Exact match |
| 38.0% formal (secondary) | 38.0 | Exact match |
| 35.7% formal (nursing) | 35.7 | Exact match |

## Common ways to mis-verify

- The "Nursing and Midwifery Associate Professionals" row in the CSV is associate professionals (paraprofessionals), not the "Nursing Professionals" category — make sure you use the right row.
- 'Strictly formal' in the CSV column `strict_formal_pct` = written contract AND paid leave AND any social security — not just one or two of these.
- ₹12,175 is the median (50th percentile) of the salary distribution, not the mean.

## If you want to rerun

```bash
cd journalists/data/mospi-plfs
uv run v4/analyze.py
```

Then open `v4/outputs/selected_professions_quality_21_34.csv`.

## Pre-publication checklist

- [ ] Confirm ₹12,175 primary teachers median salary in CSV
- [ ] Confirm ₹42,500 software developers median salary
- [ ] Confirm strict_formal_pct values for all 4 occupations
- [ ] Population filter: regular salaried workers, aged 21–34
- [ ] Verify 'Nursing and Midwifery Associate Professionals' (not 'Professionals')
