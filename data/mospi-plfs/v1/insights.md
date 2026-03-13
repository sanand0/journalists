# PLFS v1 Insights

## Reproduce

- Run `./v1/analyze.py` for the main CSVs in `v1/outputs/`.
- Run `./v1/run.sh` for the additional exploratory CSVs in `v1/out/`.

## Caveats Up Front

- All rates below use the PLFS `Person Subsample Multiplier`.
- The multiplier appears to be thousand-scaled, so the `*_m` columns in `v1/outputs/` should be read as approximate million-equivalents, not raw counts.
- I trust the percentages more than the weighted headcounts.
- These are descriptive findings, not causal claims.

## Strongest Story Leads

### 1. Marriage creates a much sharper labour-market cliff for young graduate women than education seems to offset

Source: [outputs/graduate_marriage_cliff.csv](outputs/graduate_marriage_cliff.csv)

- Among graduate women aged 15-24 who are currently married, `60.9%` are in `attended domestic duties only`.
- The comparable share is `14.2%` for never-married graduate women and `0.3%` for currently married graduate men.
- Currently married graduate women 15-24 are much less likely to be in regular salaried work (`4.2%`) than never-married graduate women (`14.6%`) or currently married graduate men (`21.3%`).
- The pattern persists at ages 25-34: `57.5%` of currently married female graduates are in domestic duties, versus `17.2%` of never-married female graduates.

Why this matters:

- This is not a generic "women work less" finding. It suggests marriage status is a sharper divider than graduation status for young women’s labour-market attachment.

### 2. Self-funded training is not converting into jobs for many women, especially married women

Sources:
[outputs/recent_training_outcomes_by_funding_and_sex.csv](outputs/recent_training_outcomes_by_funding_and_sex.csv)
[outputs/female_self_funded_training_by_marital_status.csv](outputs/female_self_funded_training_by_marital_status.csv)

- Among women who completed training in the last 365 days and paid for it themselves, `23.5%` are in domestic duties and only `18.8%` are in regular salaried work.
- Government-funded female trainees do better: `29.9%` regular salaried versus `11.8%` in domestic duties.
- The married/unmarried split is stark for self-funded female trainees:
- Ages 15-24, never married: `50.5%` students, `13.4%` regular salaried, `9.8%` domestic duties.
- Ages 15-24, currently married: `19.8%` students, `1.5%` regular salaried, `34.3%` domestic duties.
- Ages 25-34, never married: `45.5%` regular salaried, `11.1%` domestic duties.
- Ages 25-34, currently married: `14.2%` regular salaried, `43.8%` domestic duties.

Why this matters:

- The obscure angle is not "training helps." It is that self-financed skilling appears to hit a conversion wall for married women.

### 3. A sizable share of women coded as homemakers are still workers when you use the PLFS secondary lenses

Sources:
[outputs/domestic_duties_hidden_work.csv](outputs/domestic_duties_hidden_work.csv)
[outputs/female_domestic_duties_cws_work.csv](outputs/female_domestic_duties_cws_work.csv)

- `13.4%` of women whose principal status is `attended domestic duties only` still report subsidiary work.
- Within that group, current weekly status still includes roughly `5.112` million-equivalent own-account workers and `5.100` million-equivalent unpaid family workers.
- Smaller but still real pockets show up as casual labour and even regular salaried work.

Why this matters:

- This is a hidden-labour story. PLFS can label someone a homemaker on the principal-status axis while still capturing economic work on the subsidiary or weekly-status axis.

### 4. “Regular salaried” work in PLFS hides very informal jobs

Sources:
[outputs/regular_salaried_benefits_by_enterprise.csv](outputs/regular_salaried_benefits_by_enterprise.csv)
[outputs/regular_salaried_benefits_by_contract.csv](outputs/regular_salaried_benefits_by_contract.csv)

- Workers in private households employing maids, watchmen, cooks, and similar staff are counted as regular salaried workers, yet `98.9%` report no social security and `82.3%` no paid leave.
- Male proprietary enterprises account for about `34.201` million-equivalent regular salaried jobs, but `90.0%` of those workers report no social security and `78.9%` no paid leave.
- Across contract types, the no-written-contract segment is the most exposed: `84.0%` have no social security and `75.1%` no paid leave.

Why this matters:

- A lot of commentary treats "regular salaried" as shorthand for formal work. In this dataset, that shortcut is wrong.

### 5. Once young people leave school, the stated reason splits sharply by gender

Sources:
[out/dropout_reasons_young_people.csv](out/dropout_reasons_young_people.csv)
[out/dropout_reasons_married_young_women_detail.csv](out/dropout_reasons_married_young_women_detail.csv)

- Among 18-24 currently married women who attended school earlier but are not attending now, `72.7%` cite domestic chores.
- Among 18-24 currently married men in the same broad dropout pool, `88.6%` cite supplementing household income.
- Even among never-married 18-24s, women lean toward domestic chores (`44.8%`) while men overwhelmingly cite income (`76.0%`).

Why this matters:

- This is a cleanly phrased, data-verifiable gender-role split in stated dropout reasons, not just a vague employment gap.

### 6. “Students” in rural farm households are often also workers

Sources:
[out/student_subwork_benchmarks.csv](out/student_subwork_benchmarks.csv)
[out/student_subwork_farm_households.csv](out/student_subwork_farm_households.csv)

- Among all students aged 18-24, `9.4%` report subsidiary work.
- Among rural farm-household students aged 18-24, that nearly doubles to `17.5%`.
- The rate climbs to `34.0%` for scheduled tribe male students in rural farm households and `28.4%` for scheduled tribe female students.

Why this matters:

- “Student” is not always a clean non-worker category in agrarian households. That matters for how labour and education are discussed together.

## Secondary Leads Worth More Work

### 7. Technical credentials do not prevent very high job-search rates among youth

Source: [outputs/youth_technical_education_outcomes.csv](outputs/youth_technical_education_outcomes.csv)

- Among 15-24s with a technical degree in engineering/technology, `33.9%` are seeking work.
- Among 15-24s with a graduate-level engineering/technology diploma or certificate, the search rate is `44.4%`.
- These groups still do relatively well on regular salaried employment, which makes the coexistence of high job-search and high formal-job entry notable.

Why I am not leading with it:

- It could be a real placement-gap story, but it could also partly reflect recent completion timing. It needs external validation before publication.

### 8. Tiny firms wipe out much of the graduate premium even inside salaried work

Source: [out/salaried_microfirm_graduates.csv](out/salaried_microfirm_graduates.csv)

- Among urban male graduates in regular salaried work, median earnings are `35,000` in firms with `20+` workers but only `15,000` in firms with fewer than `6`.
- In the same comparison, the no-social-security rate jumps from `7.0%` to `78.7%`.
- Urban female graduates show a similar drop: median earnings fall from `30,000` in `20+` worker firms to `12,000` in firms with fewer than `6`, while the no-social-security rate rises from `8.6%` to `71.3%`.

Why I am not leading with it:

- It is a strong niche labour-market finding, but it needs state or industry context before it becomes a publication-ready story rather than a striking cross-tab.
