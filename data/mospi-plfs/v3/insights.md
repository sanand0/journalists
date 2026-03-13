# PLFS v3 Insights

## Reproduce

- Run `./v3/analyze.py` to regenerate the CSVs in `v3/outputs/`.
- Run `./v3/run.sh` if you want the wrapper entrypoint instead.

## Read This First

- The file covers `415,549` PLFS person records from `2024-01-03` to `2024-12-31`. See [outputs/dataset_profile.csv](outputs/dataset_profile.csv).
- I use the PLFS `Person Subsample Multiplier` for shares and rankings. Its raw scale still does not look like literal people counts, so percentages are safer than weighted headcounts.
- These are descriptive patterns, not causal claims.
- In this memo, a `strict formal` job means a regular salaried job with all three of these: a written contract, paid leave, and at least one social-security benefit. That is a conservative proxy, not an official PLFS category.
- `v3` keeps the strongest `v2` findings and adds new tests inspired by outside reporting and policy work on occupation mismatch, women’s work, and care burdens. See [notes.md](notes.md).

## Strongest Leads

### 1. Marriage still looks like a labour-market cliff for educated women

Sources:
[outputs/marriage_weighted_model.csv](outputs/marriage_weighted_model.csv)
[outputs/marriage_gradplus_state_compare.csv](outputs/marriage_gradplus_state_compare.csv)
[outputs/marriage_control_cells_household_type.csv](outputs/marriage_control_cells_household_type.csv)
[outputs/marriage_control_cells_social_group.csv](outputs/marriage_control_cells_social_group.csv)

- Even after controlling for state, sector, education band, social group, household type, and religion, currently married women aged `25-34` are `27.5` percentage points more likely to be in `domestic duties only`.
- In the same model, they are `16.7` points less likely to be in regular salaried work.
- The pattern is large in many states. Among female graduates aged `25-34`, the domestic-only share is `68.8%` for the married group in Andhra Pradesh and `11.9%` for the never-married group. In Tamil Nadu it is `66.1%` versus `13.5%`.
- This is not just a class-composition story. Even inside urban graduate women from regular-wage households, the domestic-only rate is `55.8%` for the married group and `7.1%` for the never-married group.

Why this matters:

- Graduation does not appear to protect many women from a sharp post-marriage drop in paid work.

### 2. Hidden homemaker work is mostly family-enterprise work, not formal employment

Sources:
[outputs/hidden_work_national_benchmark.csv](outputs/hidden_work_national_benchmark.csv)
[outputs/hidden_work_weekly_work_composition.csv](outputs/hidden_work_weekly_work_composition.csv)
[outputs/hidden_work_state_mass.csv](outputs/hidden_work_state_mass.csv)
[outputs/hidden_work_concentration_benchmarks.csv](outputs/hidden_work_concentration_benchmarks.csv)
[outputs/hidden_work_strong_subgroup_state.csv](outputs/hidden_work_strong_subgroup_state.csv)

- Among women whose principal activity is `attended domestic duties only`, `8.4%` still show up as working in the current week. `13.4%` report subsidiary work.
- This hidden weekly work is overwhelmingly family-enterprise labour. `44.5%` are own-account workers and `44.4%` are unpaid family workers. Regular salaried work is only `2.2%`.
- The pattern is heavily concentrated rather than evenly spread. Rural women are `59.3%` of the broad homemaker group but `86.0%` of the hidden weekly workers.
- Farm households are another concentration point. Women from self-employed-in-agriculture households are only `20.3%` of the broad homemaker group but `46.6%` of the hidden weekly workers.
- Bihar, Madhya Pradesh, and Uttar Pradesh add up to `58.1%` of all hidden weekly workers in [outputs/hidden_work_state_mass.csv](outputs/hidden_work_state_mass.csv).
- In one especially strong subgroup, rural women aged `25-44` with up-to-primary schooling in self-employed farm households, the hidden weekly-work rate reaches `72.4%` in Madhya Pradesh and `57.4%` in Bihar.

Why this matters:

- This is not a tiny measurement quirk. A lot of women counted as homemakers are doing real economic work, and most of that work is family-enterprise labour that disappears if you only look at the principal-status label.

### 3. A child in the household makes the marriage cliff steeper for graduate women

Sources:
[outputs/household_key_quality.csv](outputs/household_key_quality.csv)
[outputs/child_proxy_women_25_34_under5.csv](outputs/child_proxy_women_25_34_under5.csv)
[outputs/child_proxy_women_25_34_under2.csv](outputs/child_proxy_women_25_34_under2.csv)
[outputs/child_proxy_married_graduate_model.csv](outputs/child_proxy_married_graduate_model.csv)
[outputs/child_proxy_married_graduate_sex_compare_under2.csv](outputs/child_proxy_married_graduate_sex_compare_under2.csv)

- The household key checks out cleanly in [outputs/household_key_quality.csv](outputs/household_key_quality.csv): all `101,957` constructed household keys match reported household size exactly.
- Among currently married graduate women aged `25-34`, living with a child under `5` is associated with much more domestic-only status (`60.5%` versus `47.9%`) and much less regular salaried work (`11.4%` versus `21.9%`).
- The sharper under-`2` proxy makes the gap even bigger: domestic-only rises to `64.1%`, while regular salaried drops to `9.7%`.
- In a weighted model for currently married graduate women `25-34`, a child under `5` in the household is associated with `+13.0` points on domestic-only status and `-8.6` points on regular salaried work, even after controls.
- The same pattern does not show up for married graduate men. With a child under `2`, their regular-salaried rate is `49.1%`; without one, it is `50.9%`.

Why this matters:

- This is only a household child proxy, not a literal `own child` field. Even so, it is a strong sign that care burden is part of the same story as the marriage cliff.

### 4. Only about one in three regular salaried jobs passes a basic formality test, and the biggest nonformal jobs are easy to recognize

Sources:
[outputs/strict_formality_benchmark.csv](outputs/strict_formality_benchmark.csv)
[outputs/nonformal_regular_top_occupations.csv](outputs/nonformal_regular_top_occupations.csv)
[outputs/strict_formality_nonformal_concentration.csv](outputs/strict_formality_nonformal_concentration.csv)
[outputs/strict_formality_by_workplace.csv](outputs/strict_formality_by_workplace.csv)

- Among all regular salaried jobs, `44.2%` have a written contract, `52.4%` have paid leave, and `45.4%` have some social security.
- Only `34.9%` have all three at once.
- Median monthly earnings are `32,000` in the strict-formal bucket and `12,000` in the rest of regular salaried work.
- The biggest nonformal regular occupations are not abstract categories. They are shop salespersons (`6.496` weighted million-equivalent), cleaners/helpers (`4.898`), drivers (`3.007`), truck and bus drivers (`2.699`), and cooks (`2.637`).
- `Shop Salespersons` alone account for `11.5%` of all nonformal regular jobs in [outputs/nonformal_regular_top_occupations.csv](outputs/nonformal_regular_top_occupations.csv).
- Male proprietorships still dominate the enterprise picture, accounting for `54.3%` of all nonformal regular jobs.

Why this matters:

- `Regular salaried` is not a safe shorthand for `formal`, and the jobs driving the gap are concrete, familiar occupations.

### 5. Graduate mismatch looks more rural-and-retail than white-collar India imagines

Sources:
[outputs/graduate_worker_occupation_buckets.csv](outputs/graduate_worker_occupation_buckets.csv)
[outputs/graduate_worker_top_occupations.csv](outputs/graduate_worker_top_occupations.csv)
[outputs/graduate_regular_selected_occupations.csv](outputs/graduate_regular_selected_occupations.csv)

- Among all graduate workers with a principal occupation, `13.5%` are in farm-and-animal work and `10.9%` are in sales work. Only `6.9%` are in the combined software-and-engineering bucket used here.
- Among younger graduates aged `21-34`, the gap is even clearer: `14.5%` are in farm-and-animal work, `11.6%` in sales, and `9.7%` in software-and-engineering.
- The single biggest occupation among graduate workers is `Market Gardeners & Crop Growers` at `5.491` weighted million-equivalent workers. `Shop Salespersons` come next at `4.850`.
- This is not just a rural self-employment story. Inside graduate regular salaried work, `1.054` weighted million-equivalent workers are shop salespersons, with a median monthly earning of only `12,000` and a `78.7%` no-social-security rate.
- For comparison, graduate software developers have a median of `45,000` and only `1.1%` without social security.

Why this matters:

- The clean mismatch story is not `graduates are all becoming labourers`. It is that a lot of graduate work is still landing in basic farm and retail roles rather than the white-collar jobs people assume.

### 6. Tiny firms erase much of the graduate premium

Sources:
[outputs/graduate_microfirm_penalty.csv](outputs/graduate_microfirm_penalty.csv)
[outputs/strict_formality_by_workers_count.csv](outputs/strict_formality_by_workers_count.csv)

- Among urban female graduates in regular salaried work, median monthly earnings are `34,000` in firms with `20+` workers and only `12,000` in firms with fewer than `6`.
- Among urban male graduates, the same comparison is `38,500` versus `15,000`.
- Job quality collapses too. For urban female graduates, the no-social-security rate jumps from `9.7%` in `20+` worker firms to `67.4%` in firms with fewer than `6`.
- For urban male graduates, it jumps from `6.7%` to `74.1%`.

Why this matters:

- The same degree buys very different labour-market outcomes depending on employer size. A big part of the graduate premium is really an employer-quality premium.

### 7. MGNREG is not the higher-paying casual-work option in this diary data

Sources:
[outputs/casual_person_day_rural.csv](outputs/casual_person_day_rural.csv)
[outputs/casual_person_day_rural_6_8h.csv](outputs/casual_person_day_rural_6_8h.csv)
[outputs/casual_mgnreg_state_compare.csv](outputs/casual_mgnreg_state_compare.csv)

- On a cleaner person-day comparison, rural men earn `57.02` per hour in other casual work, `45.17` in MGNREG, and `41.41` in other public works.
- For rural women, the aggregate gap is smaller but still not flattering to MGNREG: `41.66` per hour in other casual work versus `41.19` in MGNREG.
- When the comparison is restricted to `6-8` hour days, the gap becomes clearer. Rural women earn `41.19` per hour in other casual work and `36.59` in MGNREG. Rural men earn `56.32` and `35.17` respectively.
- The female near-parity result is partly a state mix story. In [outputs/casual_mgnreg_state_compare.csv](outputs/casual_mgnreg_state_compare.csv), women see an MGNREG premium in Andhra Pradesh and Chhattisgarh, but big deficits in Kerala, Meghalaya, Rajasthan, and Tamil Nadu.

Why this matters:

- The public-works story is not `MGNREG pays better`. At best it can compress some gender gaps. In the aggregate, especially for men, it is plainly the lower-paying casual option.

## Strong Secondary Leads

### 8. Students in farm households are much more likely to also be workers

Sources:
[outputs/student_subwork_benchmark.csv](outputs/student_subwork_benchmark.csv)
[outputs/student_subwork_farmhousehold_breakdown.csv](outputs/student_subwork_farmhousehold_breakdown.csv)

- Among all students aged `18-24`, `5.0%` report subsidiary work.
- Among students outside rural farm households, the rate is only `2.9%`.
- Among students in rural farm households, it jumps to `10.4%`.
- The highest rates are among scheduled-tribe students in rural farm households: `23.7%` for men and `22.4%` for women.

Why this matters:

- In agrarian households, `student` is often not a clean non-worker category.

### 9. Technical education is no guarantee of a smooth labour-market entry

Sources:
[outputs/technical_education_search_benchmark.csv](outputs/technical_education_search_benchmark.csv)
[outputs/engineering_education_benchmark.csv](outputs/engineering_education_benchmark.csv)
[outputs/technical_education_low_skill_jobs.csv](outputs/technical_education_low_skill_jobs.csv)

- Among people with any technical education, job-search rates are still very high for the young: `31.2%` for rural women aged `15-24`, `26.4%` for urban men `15-24`, and `24.4%` for urban women `15-24`.
- Even engineering degrees do not eliminate the search problem. Among urban men aged `15-24` with an engineering degree, `32.2%` are still in `sought work`.
- The below-graduate engineering diploma route looks weaker on job quality. `9.7%` of regular salaried workers with that credential fall into the low-skill-plus-sales bucket used here, versus only `0.6%` for engineering degree holders.

Why this matters:

- The technical-education pipeline problem seems to have two faces: some young people cannot land a job at all, and some lower-level credential holders land weak jobs.

### 10. Once school stops, the stated reason still splits almost perfectly by gender

Source:
[outputs/school_exit_reasons_youth.csv](outputs/school_exit_reasons_youth.csv)

- Among `18-24` currently married women who attended school earlier but are not attending now, `72.7%` cite domestic chores.
- Among `18-24` currently married men in the same broad dropout pool, `88.6%` cite supplementing household income.
- Even among never-married `18-24` youth, women lean toward domestic chores (`44.8%`) while men overwhelmingly cite income (`76.0%`).

Why this matters:

- It is one of the cleanest, most legible gender-role splits anywhere in the file.
