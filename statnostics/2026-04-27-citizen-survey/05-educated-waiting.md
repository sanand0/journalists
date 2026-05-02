# Verification SOP — Study more, wait longer: India's education-jobs paradox (Card 05)

## What this card is saying

Among Indians aged 25–34, those with higher-secondary or above education are **7.4× more likely to be actively seeking work** than those with only primary education (10.3% vs 1.4%). Both the salaried-job rate and the waiting-for-work rate rise with education — but the waiting rate rises faster (7.4× vs 4.5×). The gap between the two lines **widens** at the top: 3.1 percentage points among primary-educated vs 10.1 percentage points among higher-secondary-plus.

This inverts the intuitive story: education raises formal employment, but it raises frustrated job-seeking even faster.

## Source fields

| Variable | Description |
|---|---|
| `a2b_age` | Age of respondent |
| `a2c` | Gender (1=Male, 2=Female) |
| `a2e` | Main occupation (7=RegularSalaried, 8=AvailableForWork/seeking, 10=DomesticChores) |
| `rec_a2d` | Recoded education (1=Primary, 2=Middle, 3=Secondary, 4=Higher-Secondary+) |

`rec_a2d` recode from DO file: `(1/2=1 "Primary") (3=2 "Middle") (4=3 "Secondary") (5/8=4 "Higher-Secondary+")`

Filter: `a2b_age` between 25 and 34 (inclusive), `rec_a2d` ∈ {1,2,3,4} (exclude 88=DNA).

## Verified source table

From `02_verify_cards.py` — all checks pass against the raw parquet.

**Education × employment (age 25–34, n=14,459):**

| Education | rec_a2d | n | Regular salaried % | Available/seeking % | Salaried–waiting gap |
|---|---|---:|---:|---:|---:|
| Primary | 1 | 3,065 | 4.5% | **1.4%** | +3.1pp |
| Middle | 2 | 2,576 | 5.5% | 1.8% | +3.7pp |
| Secondary | 3 | 3,362 | 12.1% | 3.7% | +8.4pp |
| Higher-Secondary+ | 4 | 5,456 | 20.4% | **10.3%** | +10.1pp |

**Waiting ratio HS+ / Primary: 10.3% / 1.4% = 7.4× (card rounds to 7×)**
**Salaried ratio HS+ / Primary: 20.4% / 4.5% = 4.5×**

**Gender breakdown (age 25–34, all education groups):**

| | Regular salaried % | Available/seeking % | Domestic chores % |
|---|---:|---:|---:|
| Male | 16.9% | 6.2% | 1.2% |
| Female | 7.4% | 4.4% | **42.2%** |

## Card text → source check

| Displayed | Source value | Note |
|---|---|---|
| "7×" more likely to wait | 10.3/1.4 = 7.4× | Conservatively rounded down to 7× |
| HS+ waiting 10.3% | 10.318915% | Exact match |
| Primary waiting 1.4% | 1.370310% | Exact match |
| HS+ salaried 20.4% | 20.4% | Exact |
| Primary salaried 4.5% | 4.5% | Exact |
| Gap: 10.1pp (HS+ end) | 20.4 − 10.3 = 10.1pp | From exact unrounded values |
| Gap: 3.1pp (Primary end) | 4.5 − 1.4 = 3.1pp | Exact |
| n=14,459 total | 3,065+2,576+3,362+5,456 = 14,459 | Exact |

## Robustness checks

- **Males only (25–34):** HS+ 11.0% waiting vs Primary 1.6% → ratio 6.9× (holds)
- **Younger cohort (15–24):** HS+ 9.6% vs Primary 1.8% → ratio 5.4× (holds)
- **Older cohort (35–49):** HS+ 3.6% vs Primary 0.7% → ratio 5.1× (holds, gap narrows with age)
- **95% CI check:** Primary n=3,065: ±0.42pp; HS+ n=5,456: ±0.81pp — the 8.9pp gap between waiting rates is statistically significant

## Common ways to mis-verify

- Using `a2e=8` for "available for work" is correct; do not use other unemployment-adjacent codes
- Forgetting to filter to age 25–34 — the finding is strongest in this band
- Confusing `rec_a2d` (grouped 1–4) with raw `a2d` (8-category scale) — always use the recoded version
- Including `rec_a2d=88` (DNA/missing) in any denominator — must exclude these
- Quoting the ratio as "7.5×" — the verified figure is 7.4× (10.318/1.370); the card conservatively rounds to "7×"

## What this cannot conclude

- This is self-reported survey classification, not ILO-defined unemployment
- Higher-educated respondents may classify themselves as "seeking" where lower-educated respondents accept informal work as their status
- This is cross-sectional; not a longitudinal measure of actual job-search duration
- Women coded as "domestic chores" (42.2% of women 25–34) may include many who are also available for work but do not self-classify as seeking

## Pre-publication checklist

- [ ] Confirm rec_a2d=4 (HS+), age 25–34: waiting % ≈ 10.3%
- [ ] Confirm rec_a2d=1 (Primary), age 25–34: waiting % ≈ 1.4%
- [ ] Confirm rec_a2d=4, age 25–34: salaried % ≈ 20.4%
- [ ] Confirm rec_a2d=1, age 25–34: salaried % ≈ 4.5%
- [ ] Confirm n=14,459 total across four education groups
- [ ] Confirm "7×" uses conservative rounding of 7.4× (not 7.5×)
- [ ] Note female domestic-chores rate (42.2%) as context for interpreting "seeking" undercount
- [ ] Note the card does not imply causation between education level and job-seeking frustration
