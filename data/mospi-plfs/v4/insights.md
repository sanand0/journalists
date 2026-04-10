# PLFS v4 Insights

## Reproduce

- Run `./v4/analyze.py` to regenerate the CSVs in `v4/outputs/`.
- Run `./v4/run.sh` if you want the wrapper entrypoint instead.

## Read This First

- The file covers `415,549` PLFS person records from `2024-01-03` to `2024-12-31`. See [outputs/dataset_profile.csv](outputs/dataset_profile.csv).
- `v4` carries forward the full `v3` output set and adds new tables on household role, long job-search duration, profession quality, technical-credential quality, and a stricter hidden-work district screen.
- I use the PLFS `Person Subsample Multiplier` for weighted shares and rankings. Its raw scale still does not look like literal people counts, so percentages are more trustworthy than weighted totals.
- These are descriptive patterns, not causal claims.
- In this memo, a `strict formal` job means a regular salaried job with all three of these: a written contract, paid leave, and at least one social-security benefit. That is a conservative proxy, not an official PLFS category.

## Strongest New v4 Leads

### 1. Where a married woman sits inside the household matters a lot for work

Sources:
[outputs/married_graduate_household_role_grouped.csv](outputs/married_graduate_household_role_grouped.csv)
[outputs/married_graduate_household_role_detail.csv](outputs/married_graduate_household_role_detail.csv)
[outputs/married_graduate_household_role_model.csv](outputs/married_graduate_household_role_model.csv)
[outputs/married_graduate_household_role_gender_compare.csv](outputs/married_graduate_household_role_gender_compare.csv)

- Among currently married graduate women aged `25-34`, those listed as the `spouse of head` or `spouse of married child` have a `57.2%` domestic-only rate and only a `13.8%` regular-salaried rate.
- The comparable figures for women listed as `self` or `married child` are much better: `43.1%` domestic-only and `30.7%` regular salaried.
- Children matter, but they are not the whole story. In the grouped table, the `wife role in extended household` group is more likely to live with a child under `5` (`67.2%` versus `48.7%`), yet the role gap survives after controls.
- In the weighted model, that `spouse-role` position is associated with `+18.7` points on domestic-only status and `-17.6` points on regular salaried work, even after controlling for `child under 5`, state, sector, social group, household type, and religion.

Why this matters:

- The marriage cliff is not just about marriage in the abstract. Household structure looks like part of the mechanism.

### 2. For many educated women still looking for work, this is not a short search. It is a years-long wait

Sources:
[outputs/graduate_jobseeker_duration_25_34.csv](outputs/graduate_jobseeker_duration_25_34.csv)
[outputs/graduate_women_jobseeker_duration_marital_25_34.csv](outputs/graduate_women_jobseeker_duration_marital_25_34.csv)

- Among graduate job seekers aged `25-34`, `37.4%` of urban women and `34.2%` of rural women report being unemployed for `more than 3 years`.
- The comparable figures for men are lower: `31.3%` in urban India and `22.9%` in rural India.
- The sharpest subgroup is urban currently married graduate women aged `25-34`. Fully `50.2%` report job-search duration of `more than 3 years`.
- Urban never-married graduate women in the same age band are also struggling, but much less severely: `29.6%` report `more than 3 years`.

Why this matters:

- The women still trying to enter or re-enter paid work are often not just between jobs. Many look stuck outside the labour market for very long periods.

### 3. Teaching and nursing jobs look far less secure than the middle-class stereotype suggests

Sources:
[outputs/selected_professions_quality_21_34.csv](outputs/selected_professions_quality_21_34.csv)

- Among regular salaried workers aged `21-34`, software developers have a median monthly salary of `42,500` and a `76.6%` strict-formal rate.
- Young primary teachers are nowhere near that benchmark: median `12,175`, strict formal `42.2%`.
- Secondary teachers look only somewhat better: median `16,000`, strict formal `38.0%`.
- Nursing and midwifery associate professionals are worse still: median `10,000`, strict formal `35.7%`.
- The weakest bucket is `Other Teaching Professionals`, with median `8,000` and only `9.3%` strict formal.

Why this matters:

- Jobs many families treat as stable or respectable female pathways often do not look stable in the PLFS job-quality fields.

### 4. Inside teaching, young women get worse jobs than young men

Sources:
[outputs/selected_professions_gender_gaps_21_34.csv](outputs/selected_professions_gender_gaps_21_34.csv)

- Among young primary teachers, women have a median salary of `10,000` and a strict-formal rate of `36.3%`.
- Men in the same occupation have a median of `20,000` and a strict-formal rate of `53.5%`.
- Among young secondary teachers, women are at `15,000` and `28.9%` strict formal, versus `18,000` and `46.3%` for men.
- In the broad `Other Teaching Professionals` bucket, women are at `6,000` median and `5.2%` strict formal, versus `12,000` and `11.9%` for men.

Why this matters:

- Even inside the same supposedly stable professions, women often seem to be landing weaker versions of the job.

### 5. Technical education is not one ladder. Degrees and diplomas lead to very different job quality

Sources:
[outputs/technical_credential_quality_21_34.csv](outputs/technical_credential_quality_21_34.csv)
[outputs/technical_credential_top_jobs_21_34.csv](outputs/technical_credential_top_jobs_21_34.csv)

- Young people with an engineering degree have much stronger labour outcomes than those with a below-graduate engineering diploma.
- For engineering degrees, `59.4%` are in regular salaried work, `43.2%` are in a strict-formal job, median regular salary is `35,475`, and only `4.1%` of regular jobs sit in firms with fewer than `10` workers.
- For below-graduate engineering diplomas, the comparable figures are `47.4%`, `23.3%`, `18,000`, and `14.9%`.
- The medical ladder shows the same split. Young medical degree holders have median regular pay of `25,000`; below-graduate medical diploma holders are at `15,000`.
- The top-job table makes this concrete. Engineering degrees mostly feed into software and engineering roles. Below-graduate engineering diplomas much more often feed into mechanics, repair, and some retail. Below-graduate medicine diplomas feed mainly into nursing and technician roles.

Why this matters:

- `Technical education` sounds like one category in public debate. In the data it behaves like several very different pipelines.

### 6. Hidden homemaker work still shows up strongly even after a stricter district filter

Sources:
[outputs/hidden_work_district_strict_overview.csv](outputs/hidden_work_district_strict_overview.csv)
[outputs/hidden_work_district_strict_state_summary.csv](outputs/hidden_work_district_strict_state_summary.csv)
[outputs/hidden_work_district_strict.csv](outputs/hidden_work_district_strict.csv)

- After raising the threshold to rural districts with `sample_n >= 100` and a reasonably large homemaker base, `24` districts still pass the screen.
- Their average hidden-work rate is `21.4%`.
- `45.8%` of those districts still show hidden-work rates of at least `20%`.
- `33.3%` still show rates of at least `30%`.
- The strongest districts in this stricter cut are Chhatarpur in Madhya Pradesh (`64.0%`), Araria in Bihar (`51.3%`), Sambhal in Uttar Pradesh (`38.4%`), and Madhubani in Bihar (`37.1%`).

Why this matters:

- The hidden-work result is not just a soft national average. It survives a harder local test, though district rank-ordering still needs caution.

## Strongest Retained Leads From v3

### 7. Marriage still looks like a labour-market cliff for educated women

Sources:
[outputs/marriage_weighted_model.csv](outputs/marriage_weighted_model.csv)
[outputs/marriage_gradplus_state_compare.csv](outputs/marriage_gradplus_state_compare.csv)
[outputs/marriage_control_cells_household_type.csv](outputs/marriage_control_cells_household_type.csv)
[outputs/marriage_control_cells_social_group.csv](outputs/marriage_control_cells_social_group.csv)

- Even after controls, currently married women aged `25-34` are `27.5` points more likely to be in `domestic duties only`.
- In the same model they are `16.7` points less likely to be in regular salaried work.
- Among graduate women aged `25-34`, the married-versus-never-married domestic-only gap is very large across many states.

Why this matters:

- Education alone does not protect many women from a sharp post-marriage exit from paid work.

### 8. A child in the household makes the marriage cliff steeper for graduate women

Sources:
[outputs/household_key_quality.csv](outputs/household_key_quality.csv)
[outputs/child_proxy_women_25_34_under5.csv](outputs/child_proxy_women_25_34_under5.csv)
[outputs/child_proxy_women_25_34_under2.csv](outputs/child_proxy_women_25_34_under2.csv)
[outputs/child_proxy_married_graduate_model.csv](outputs/child_proxy_married_graduate_model.csv)

- Among currently married graduate women aged `25-34`, living with a child under `5` is associated with `60.5%` domestic-only status, versus `47.9%` without that child proxy.
- Their regular-salaried rate falls from `21.9%` to `11.4%`.
- In the weighted model, the under-`5` child proxy is associated with `+13.0` points on domestic-only status and `-8.6` points on regular salaried work.

Why this matters:

- Care burden appears to sit on top of the marriage effect, not outside it.

### 9. Hidden homemaker work is mostly family-enterprise labour

Sources:
[outputs/hidden_work_national_benchmark.csv](outputs/hidden_work_national_benchmark.csv)
[outputs/hidden_work_weekly_work_composition.csv](outputs/hidden_work_weekly_work_composition.csv)
[outputs/hidden_work_state_mass.csv](outputs/hidden_work_state_mass.csv)
[outputs/hidden_work_concentration_benchmarks.csv](outputs/hidden_work_concentration_benchmarks.csv)
[outputs/hidden_work_strong_subgroup_state.csv](outputs/hidden_work_strong_subgroup_state.csv)

- Among women whose principal activity is `attended domestic duties only`, `8.4%` still show up as working in the current week.
- This hidden weekly work is overwhelmingly family-enterprise labour. `44.5%` are own-account workers and `44.4%` are unpaid family workers.
- Bihar, Madhya Pradesh, and Uttar Pradesh remain major concentration points.

Why this matters:

- A large amount of women’s work disappears if you look only at the principal-status label.

### 10. `Regular salaried` is still not a safe shorthand for `formal`

Sources:
[outputs/strict_formality_benchmark.csv](outputs/strict_formality_benchmark.csv)
[outputs/nonformal_regular_top_occupations.csv](outputs/nonformal_regular_top_occupations.csv)
[outputs/strict_formality_nonformal_concentration.csv](outputs/strict_formality_nonformal_concentration.csv)
[outputs/strict_formality_by_workplace.csv](outputs/strict_formality_by_workplace.csv)

- Among all regular salaried jobs, only `34.9%` pass the strict-formal test.
- Median monthly earnings are `32,000` in the strict-formal bucket and `12,000` in the rest.
- The biggest nonformal regular jobs are familiar occupations such as shop salespersons, cleaners/helpers, drivers, and cooks.

Why this matters:

- The headline employment category hides a very large job-quality split.

### 11. Graduate mismatch still looks more rural-and-retail than white-collar India imagines

Sources:
[outputs/graduate_worker_occupation_buckets.csv](outputs/graduate_worker_occupation_buckets.csv)
[outputs/graduate_worker_top_occupations.csv](outputs/graduate_worker_top_occupations.csv)
[outputs/graduate_regular_selected_occupations.csv](outputs/graduate_regular_selected_occupations.csv)

- Among graduate workers with a principal occupation, `13.5%` are in farm-and-animal work and `10.9%` are in sales work.
- Only `6.9%` fall into the combined software-and-engineering bucket used here.
- The single biggest occupation among graduate workers is `Market Gardeners & Crop Growers`. `Shop Salespersons` are close behind.

Why this matters:

- The mismatch story is not mainly about extreme distress jobs. It is about graduates landing in everyday farm and retail work.

### 12. Tiny firms erase much of the graduate premium

Sources:
[outputs/graduate_microfirm_penalty.csv](outputs/graduate_microfirm_penalty.csv)
[outputs/strict_formality_by_workers_count.csv](outputs/strict_formality_by_workers_count.csv)

- Among urban female graduates in regular salaried work, median monthly pay is `34,000` in firms with `20+` workers and only `12,000` in firms with fewer than `6`.
- Among urban male graduates, the same comparison is `38,500` versus `15,000`.
- Social-security coverage collapses in small firms for both sexes.

Why this matters:

- A lot of the graduate premium is really an employer-quality premium.

### 13. MGNREG is still not the higher-paying casual-work option in this diary data

Sources:
[outputs/casual_person_day_rural.csv](outputs/casual_person_day_rural.csv)
[outputs/casual_person_day_rural_6_8h.csv](outputs/casual_person_day_rural_6_8h.csv)
[outputs/casual_mgnreg_state_compare.csv](outputs/casual_mgnreg_state_compare.csv)

- On the person-day comparison, rural men earn `57.02` per hour in other casual work and `45.17` in MGNREG.
- Rural women are closer, but MGNREG still does not look clearly superior in the aggregate.
- The state table shows that the answer varies sharply by state.

Why this matters:

- Public works may compress some gaps without being the better-paying casual option.

## Strong Secondary Leads

### 14. Students in rural farm households are much more likely to also be workers

Sources:
[outputs/student_subwork_benchmark.csv](outputs/student_subwork_benchmark.csv)
[outputs/student_subwork_farmhousehold_breakdown.csv](outputs/student_subwork_farmhousehold_breakdown.csv)

- Among all students aged `18-24`, `5.0%` report subsidiary work.
- Among students outside rural farm households, the rate is `2.9%`.
- Among students in rural farm households, it jumps to `10.4%`.
- The highest rates are among scheduled-tribe students in rural farm households.

Why this matters:

- In agrarian households, `student` is often not a clean non-worker category.

### 15. Technical education is no guarantee of a smooth labour-market entry

Sources:
[outputs/technical_education_search_benchmark.csv](outputs/technical_education_search_benchmark.csv)
[outputs/engineering_education_benchmark.csv](outputs/engineering_education_benchmark.csv)
[outputs/technical_education_low_skill_jobs.csv](outputs/technical_education_low_skill_jobs.csv)

- Young technical-education holders still show high job-search rates.
- Even engineering degrees do not eliminate the search problem for the youngest urban groups.
- Lower-tier credential holders are much more likely to land in weak job buckets than engineering degree holders.

Why this matters:

- The problem is not just access to training. It is also job quality after training.

### 16. Once school stops, the stated reason still splits sharply by gender

Sources:
[outputs/school_exit_reasons_youth.csv](outputs/school_exit_reasons_youth.csv)

- Among `18-24` currently married women who attended school earlier but are not attending now, `72.7%` cite domestic chores.
- Among comparable men, `88.6%` cite supplementing household income.
- Even among never-married youth, the same split remains visible.

Why this matters:

- It is one of the cleanest gender-role divides anywhere in the file.

## Shortlist For Story-Grade Use

- If the audience is broad, the cleanest `v4` package is:
  `household role after marriage`, `years-long job search for educated women`, `teacher/nurse precarity`, and `technical degrees versus diplomas`.
- If the story is specifically about women’s work, the strongest chain is:
  `marriage cliff` -> `child proxy` -> `household role` -> `long-duration search` -> `hidden homemaker work`.
- If the story is about job quality rather than participation, the best chain is:
  `regular salaried is not formal` -> `teacher and nurse precarity` -> `microfirm penalty` -> `technical-credential ladder`.
