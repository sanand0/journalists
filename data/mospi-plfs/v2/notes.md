# PLFS v2 Notes

## Reproduce

- Run `./v2/analyze.py` to regenerate all exported tables in `v2/outputs/`.
- Run `./v2/run.sh` if you want the wrapper entrypoint instead.

## Method Notes

- `Person ID` is unique across all `415,549` rows.
- Survey dates span `2024-01-03` to `2024-12-31`.
- I use `Person Subsample Multiplier` for weighted shares. Its raw sum is `964,260,005,421`, which does not look like literal people counts. Treat `*_m` columns as approximate scale markers, not hard population counts.
- Percentages are much more trustworthy than weighted headcounts.
- The strongest hidden-work finding comes from the gap between `Principal Activity Status` and `CWS Status`. That is intentional, not a coding mistake.
- The `strict formal` definition is deliberately conservative: written contract + paid leave + some social security, restricted to principal-status regular salaried workers.
- `strict_formality_benchmark.csv` uses unweighted medians for monthly salaried earnings. The weighted shares around those medians still use PLFS weights.
- `casual_pay_rural_gender_benchmarks.csv` uses diary-based weighted medians for daily and hourly wages, based on primary activity spells with positive hours and positive wages.

## Data Quality and Debugging Notes

- `Day 7` diary columns arrive as strings and need explicit casting. The script handles that.
- The diary uses many `0` values. I treat `hours > 0` and `wage > 0` as the usable pay records.
- `casual_diary_pay_quality.csv` shows that MGNREG and public-works wage spells have clean positive-hour, positive-wage records after filtering.
- There are `48` records with age `100+`; the maximum age is `112`.
- The transgender sample is too small for publication-grade claims. Some weighted outputs round that group down to `0.0`.
- `Sector` and `Principal Workplace Location` do not always line up cleanly. The workplace field still carries useful signal, but it is not a perfect rural/urban substitute.
- There is a blank workplace category in `strict_formality_by_workplace.csv` with about `1.121` weighted million-equivalent regular salaried jobs. I did not build a story around that unknown bucket.
- I fixed one bug during this pass: the first draft of `student_subwork_benchmark.csv` mislabeled the comparison group. The current file correctly separates `all_students`, `other_students`, and `rural_farm_household_students`.

## Findings I Consider Real but Did Not Lead With

- The marriage cliff is strongest and cleanest for graduates, but it also shows up for some secondary and below-secondary groups. It is just much less consistent there.
- The hidden-work story is strongest in rural India. Urban homemakers also show some hidden work, but the rate is only `2.9%`, which makes the national average less revealing than the rural split.
- The most dramatic hidden-work districts are still moderate-sized samples. I kept a minimum threshold of `n >= 100`, but district rankings still need caution.
- `strict_formality_nonformal_concentration.csv` suggests the largest reservoir of low-quality regular jobs is male proprietorships, not just domestic work or private households.
- The MGNREG result is subtle: women look near-parity by day rate, but not by hour. That could reflect work allocation, task norms, or reporting structure. The data show the pattern, not the mechanism.
- The farm-household student story is strongest for scheduled-tribe youth and remains high for both sexes. That is more interesting than a generic `boys work more` story.
- `school_exit_reasons_youth.csv` is one of the cleanest lay-reader tables in the whole project. It may be worth turning into a standalone graphic even if it is not the main story.

## Candidate Story Angles

- Marriage appears to overpower education for many women’s labour-market attachment.
- India’s female labour story may be understated when homemakers in agrarian households still do real work that only shows up on a different PLFS lens.
- A large share of `regular salaried` work looks closer to semi-formal or informal work once contract, leave, and social-security fields are combined.
- The graduate premium is not just about education. It is also about whether the job sits in a micro-firm or a larger employer.
- Public works may compress the gender gap without delivering genuinely strong wages.

## Useful Follow-Ups for v3

- Break the marriage cliff by occupation and industry, not just by state and household background.
- Map the hidden-work finding at district level with stricter sample and weighted-size thresholds.
- Decompose nonformal regular jobs by occupation so the proprietorship story is easier to explain to a lay audience.
- Compare these same patterns with older PLFS waves to see which are longstanding and which are getting stronger.
- Push the student-work result into attendance intensity if there is any usable proxy for part-time versus more sustained work.
