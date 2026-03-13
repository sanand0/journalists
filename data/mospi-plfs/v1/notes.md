# PLFS v1 Notes

## Reproduce

- Run `./v1/analyze.py` to regenerate the main exports in `v1/outputs/`.
- Run `./v1/run.sh` to regenerate the exploratory exports in `v1/out/`.
- Parallel exploration also left auxiliary SQL artifacts in `v1/generate_outputs.sql` and `v1/export.sql`.

## Method and weighting notes

- `Person ID` is unique across all `415,549` parquet rows.
- Survey dates span `2024-01-03` to `2024-12-31`.
- I used `Person Subsample Multiplier` for weighted shares and rankings.
- The raw sum of that multiplier is `964,260,005,421`. That scale does not look like direct people counts. The `*_m` columns in `v1/outputs/` assume the multiplier is thousand-scaled and divide by `1e9`, so those headcounts are approximate.
- I trust the percentages more than the headcounts.
- `candidate_lifts.csv` uses a minimum cell threshold of `n >= 250` and weighted size `>= 5,000,000` before ranking subgroup lifts.

## Design quirks that matter analytically

- `Principal Activity Status`, `Subsidiary Work Engagement`, and `CWS Status` are not interchangeable. Some of the most interesting findings come from the tension between those lenses.
- Many columns are structurally null by design. Training fields only apply to the trained subset; contract/leave/social-security fields mostly apply to salaried workers.
- `Sector` and workplace are not redundant. An urban-sector worker can still have a workplace label beginning with `rural - ...`, and vice versa.
- `Visit` is constant at `1` in this file, so it is not useful for subgroup analysis.

## Data quality observations

- `Day 7` diary fields are strings and need casting; the main script handles that explicitly.
- Daily hours parse cleanly and run from `0` to `20`; daily wages parse cleanly and run from `0` to `3000`.
- The diary appears to use `0` rather than `NULL` for inactivity, so any future wage/hour work should treat zeros carefully.
- There are `48` records with age `100+`; the maximum age is `112`.
- Only `3` records exceed `112` total weekly work hours; all three look like plausible but extreme long-hour cases rather than obvious join corruption.
- The transgender sample is only `15` records. I avoided treating it as publication-grade evidence.

## Interesting leads that did not make the top line

- `v1/out/salaried_microfirm_graduates.csv` is strong: among urban male graduates in regular salaried work, median earnings drop from `35,000` in firms with `20+` workers to `15,000` in firms with `<6` workers, and the no-social-security rate jumps from `7.0%` to `78.7%`. Urban female graduates show a similar fall from `30,000` to `12,000`, with no-social-security rising from `8.6%` to `71.3%`.
- `v1/out/unemployment_duration_by_age_band.csv` suggests long-duration unemployment is especially severe for urban women job seekers aged `25-34` (`37.4%` report `3+` years) and even worse for ages `35-44` (`57.5%`), but the `35-44` sample is too small to lead with.
- `v1/outputs/youth_technical_education_outcomes.csv` shows surprisingly high job-search rates even among technical credential holders. That looks real, but it needs external reporting on course timing and placement patterns before publication.
- `v1/outputs/candidate_lifts.csv` throws off religion-specific spikes such as Sikh women in the `domestic_plus` category and Jain women in `domestic_only`. Those may be real, but they are too exposed to regional concentration to use without state-level context.
- `v1/out/unpaid_family_farm_workers.csv` and `v1/out/student_subwork_farm_households.csv` both suggest a larger disguised-labour story in agrarian households, especially among scheduled tribe youth.

## Follow-up ideas

- Push the strongest findings down to `State/UT` and district level.
- Separate household-type effects from social-group and religion effects with multivariate models.
- Build a stricter “formal salaried” definition combining contract, paid leave, social security, enterprise type, and workers-count fields.
- Compare usual-status and current-week transitions by sex, marital status, and education.
- Reconstruct diary-based hourly earnings for casual work and compare MGNREG/public-works days with other casual-labour days.

## Key output locations

- `v1/outputs/`: main tables from `v1/analyze.py`
- `v1/out/`: exploratory tables from `v1/run.sh`
