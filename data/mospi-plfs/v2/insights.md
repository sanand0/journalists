# PLFS v2 Insights

## Reproduce

- Run `./v2/analyze.py` to regenerate the CSVs in `v2/outputs/`.
- Run `./v2/run.sh` as a thin wrapper around the same script.

## Read This First

- The file covers `415,549` PLFS person records from `2024-01-03` to `2024-12-31`. See [outputs/dataset_profile.csv](outputs/dataset_profile.csv).
- I use the PLFS `Person Subsample Multiplier` for shares and rankings. Its raw scale does not look like literal people counts, so percentages are safer than weighted headcounts.
- These are descriptive patterns, not causal claims.
- In this memo, a `strict formal` job means a regular salaried job with all three of these: a written contract, paid leave, and at least one social-security benefit. That is a conservative proxy, not an official PLFS category.

## Strongest Leads

### 1. Marriage still looks like a labour-market cliff for educated women

Sources:
[outputs/marriage_weighted_model.csv](outputs/marriage_weighted_model.csv)
[outputs/marriage_gradplus_state_compare.csv](outputs/marriage_gradplus_state_compare.csv)
[outputs/marriage_control_cells_household_type.csv](outputs/marriage_control_cells_household_type.csv)
[outputs/marriage_control_cells_social_group.csv](outputs/marriage_control_cells_social_group.csv)

- Even after controlling for state, sector, education band, social group, household type, and religion, currently married women aged `25-34` are `27.5` percentage points more likely to be in `domestic duties only`.
- In the same model, they are `16.7` points less likely to be in regular salaried work.
- The pattern is large and easy to see in many states. Among female graduates aged `25-34`, the domestic-only share is `68.8%` for the married group in Andhra Pradesh and `11.9%` for the never-married group. In Tamil Nadu it is `66.1%` versus `13.5%`.
- This is not just a class-composition story. Even inside urban graduate women from regular-wage households, the domestic-only rate is `55.8%` for the married group and `7.1%` for the never-married group.

Why this matters:

- Graduation does not appear to protect many women from a sharp post-marriage drop in paid work.

### 2. A lot of rural women counted as homemakers still show up as workers when PLFS asks a different way

Sources:
[outputs/hidden_work_rural_urban.csv](outputs/hidden_work_rural_urban.csv)
[outputs/hidden_work_rural_female_state.csv](outputs/hidden_work_rural_female_state.csv)
[outputs/hidden_work_rural_female_social_group.csv](outputs/hidden_work_rural_female_social_group.csv)
[outputs/hidden_work_rural_female_household_type.csv](outputs/hidden_work_rural_female_household_type.csv)
[outputs/hidden_work_rural_female_district.csv](outputs/hidden_work_rural_female_district.csv)

- Among women whose principal activity is `attended domestic duties only`, `12.2%` of the rural group still appear as working in the current week. In urban India, the comparable rate is `2.9%`.
- The hidden-work rate is especially high in Jammu and Kashmir (`42.9%`) and Madhya Pradesh (`34.8%`).
- It is also concentrated in more disadvantaged rural settings: `18.4%` for scheduled-tribe women, versus `7.9%` for the `others` group.
- Household type matters too. Rural women in farm households show a `19.4%` hidden-work rate, versus `6.1%` in regular-wage households.
- Some district rates are startling even after a minimum-sample screen of `n >= 100`: Chhatarpur in Madhya Pradesh is `64.0%`, Shivpuri `61.8%`, and Anantnag in Jammu and Kashmir `56.1%`.

Why this matters:

- The dataset can classify a woman as a homemaker on one PLFS lens while still recording real economic work on another. That is a hidden-labour story, not a small technical quirk.

### 3. Only about one in three regular salaried jobs passes a basic formality test

Sources:
[outputs/strict_formality_benchmark.csv](outputs/strict_formality_benchmark.csv)
[outputs/strict_formality_nonformal_concentration.csv](outputs/strict_formality_nonformal_concentration.csv)
[outputs/strict_formality_by_enterprise.csv](outputs/strict_formality_by_enterprise.csv)
[outputs/strict_formality_by_workplace.csv](outputs/strict_formality_by_workplace.csv)

- Among all regular salaried jobs, `44.2%` have a written contract, `52.4%` have paid leave, and `45.4%` have some social security.
- Only `34.9%` have all three at once.
- The pay gap between the two buckets is huge. Median monthly earnings are `32,000` in the strict-formal bucket and `12,000` in the rest of regular salaried work.
- A majority of nonformal regular jobs are concentrated in male proprietorships (`54.3%`). Another `8.6%` sit inside private households employing domestic staff and similar workers.
- Jobs at the employer's dwelling are almost never formal by this test: `0.1%` in rural areas and `0.6%` in urban areas.

Why this matters:

- Public debate often uses `regular salaried` as shorthand for `formal`. In this data, that shortcut is badly misleading.

### 4. Tiny firms erase much of the graduate premium

Sources:
[outputs/graduate_microfirm_penalty.csv](outputs/graduate_microfirm_penalty.csv)
[outputs/strict_formality_by_workers_count.csv](outputs/strict_formality_by_workers_count.csv)

- Among urban female graduates in regular salaried work, median monthly earnings are `34,000` in firms with `20+` workers and only `12,000` in firms with fewer than `6`.
- Among urban male graduates, the same comparison is `38,500` versus `15,000`.
- Job quality collapses too. For urban female graduates, the no-social-security rate jumps from `9.7%` in `20+` worker firms to `67.4%` in firms with fewer than `6`.
- For urban male graduates, it jumps from `6.7%` to `74.1%`.

Why this matters:

- The same degree buys very different labour-market outcomes depending on employer size. This is a strong way to show how much of the graduate premium depends on where the job sits, not just on education itself.

### 5. Public-works jobs narrow the daily gender gap, but mostly by paying everyone less

Sources:
[outputs/casual_pay_rural_gender_benchmarks.csv](outputs/casual_pay_rural_gender_benchmarks.csv)
[outputs/casual_diary_pay_primary_activity.csv](outputs/casual_diary_pay_primary_activity.csv)

- In rural MGNREG work, women’s weighted median daily wage is `250`, slightly above the male median of `243`.
- But the hourly picture is less equal: women are at `41.63` per hour and men at `50.00`, so women earn only `83.3%` of the male hourly rate.
- Ordinary rural casual labour is both less equal and higher paid: women are at `300` per day versus `400` for men, and `43.75` per hour versus `50.00`.
- Other public works outside MGNREG show the smallest hourly gap of the three categories, but at a low pay level for both sexes.

Why this matters:

- The public-works story is more nuanced than `women and men are paid the same`. Daily rates look compressed, but hourly pay still trails, and the wage floor itself is low.

### 6. Students in farm households are much more likely to also be workers

Sources:
[outputs/student_subwork_benchmark.csv](outputs/student_subwork_benchmark.csv)
[outputs/student_subwork_farmhousehold_breakdown.csv](outputs/student_subwork_farmhousehold_breakdown.csv)

- Among all students aged `18-24`, `5.0%` report subsidiary work.
- Among students outside rural farm households, the rate is only `2.9%`.
- Among students in rural farm households, it jumps to `10.4%`.
- The highest rates are among scheduled-tribe students in rural farm households: `23.7%` for men and `22.4%` for women.

Why this matters:

- In agrarian households, `student` is often not a clean non-worker category. That matters for how education and youth labour are discussed together.

## Clean Secondary Lead

### 7. Once school stops, the stated reason still splits almost perfectly by gender

Source:
[outputs/school_exit_reasons_youth.csv](outputs/school_exit_reasons_youth.csv)

- Among `18-24` currently married women who attended school earlier but are not attending now, `72.7%` cite domestic chores.
- Among `18-24` currently married men in the same broad dropout pool, `88.6%` cite supplementing household income.
- Even among never-married `18-24` youth, women lean toward domestic chores (`44.8%`) while men overwhelmingly cite income (`76.0%`).

Why this matters:

- It is a very simple, very legible gender-role split, and it survives even before marriage in the never-married group.
