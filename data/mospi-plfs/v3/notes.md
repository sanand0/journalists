# PLFS v3 Notes

## Reproduce

- Run `./v3/analyze.py` to regenerate all exported tables in `v3/outputs/`.
- Run `./v3/run.sh` if you want the wrapper entrypoint instead.

## Outside Idea Sources I Checked

- India Economic Survey 2024-25, Chapter 4 on employment and occupational mismatch:
  [https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/vol2_ch04.pdf](https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/vol2_ch04.pdf)
- Ideas for India on women’s talent misallocation:
  [https://www.ideasforindia.in/topics/macroeconomics/beyond-participation-tackling-the-misallocation-of-womens-talent-in-india](https://www.ideasforindia.in/topics/macroeconomics/beyond-participation-tackling-the-misallocation-of-womens-talent-in-india)
- Ideas for India on female labour-force measurement and data quality:
  [https://www.ideasforindia.in/topics/social-identity/female-labour-force-participation-measurement-and-data-quality](https://www.ideasforindia.in/topics/social-identity/female-labour-force-participation-measurement-and-data-quality)
- Indian Express on recent female labour-force participation patterns:
  [https://indianexpress.com/article/opinion/columns/how-tamil-nadu-has-created-favourable-conditions-for-women-to-join-the-labour-force-9731890/](https://indianexpress.com/article/opinion/columns/how-tamil-nadu-has-created-favourable-conditions-for-women-to-join-the-labour-force-9731890/)

These did not provide `v3` numbers. They were idea prompts for what to test locally: occupation mismatch, women’s hidden work, care burden, and the quality of jobs inside headline employment categories.

## Method Notes

- `Person ID` is unique across all `415,549` rows.
- Survey dates span `2024-01-03` to `2024-12-31`.
- I use `Person Subsample Multiplier` for weighted shares. Its raw sum is `964,260,005,421`, which still does not look like literal people counts. Treat `*_m` columns as approximate scale markers, not hard population counts.
- Percentages are much more trustworthy than weighted headcounts.
- The strongest hidden-work finding still comes from the gap between `Principal Activity Status` and `CWS Status`. That is intentional, not a coding mistake.
- The `strict formal` definition is still deliberately conservative: written contract + paid leave + some social security, restricted to principal-status regular salaried workers.
- `strict_formality_benchmark.csv`, `graduate_microfirm_penalty.csv`, and the occupation-quality tables use unweighted medians for monthly salaried earnings. The weighted shares around those medians still use PLFS weights.
- `casual_person_day_rural.csv` is cleaner than the v2 spell-level wage tables for the MGNREG question because it collapses activity `1` and `2` into a single `person x day x status` observation before comparing hourly rates.

## Household-Key Notes

- For the new child-proxy analysis, I upgraded the household key to use the survey-design fields directly:
  `Sector + Stratum + Sub-Stratum + Sub-Sample + FSU + Sample Segment/Sub-Block + Second Stage Stratum + Household Number`.
- [outputs/household_key_quality.csv](outputs/household_key_quality.csv) shows that this produces `101,957` household keys, and all `101,957` match reported household size exactly.
- That is good enough to treat `child 0-2 in household` and `child 0-5 in household` as defensible co-residence flags.
- It is still not an `own child` field. The current writeup treats it as a household child proxy, not literal motherhood.

## New v3 Caveats

- The child proxy is credible for currently married women and currently married men. It is not clean for never-married women, because the child is often someone else’s.
- The graduate mismatch buckets are deliberately simple. `farm_and_animal_work`, `sales_work`, and `software_and_engineering` are hand-built groups from readable occupation labels, not an official NCO skill ladder.
- `technical_education_low_skill_jobs.csv` uses an intentionally conservative `low_skill_plus_sales` bucket. It is a screening tool, not a definitive measure of occupational mismatch.
- Urban MGNREG and urban other-public-works samples are too small for story-grade comparisons. I stayed with rural person-day comparisons.
- The most dramatic hidden-work state and subgroup numbers are robust enough to describe, but district rankings still need caution even with raw-`n` floors.

## Data Quality Notes

- `Day 7` diary columns arrive as strings and need explicit casting. The script handles that.
- The diary uses many `0` values. I still treat `hours > 0` and `wage > 0` as the usable pay records.
- `casual_diary_pay_quality.csv` still shows clean positive-hour, positive-wage records for rural MGNREG and public-works comparisons after filtering.
- There are `48` records with age `100+`; the maximum age is `112`.
- The transgender sample remains too small for publication-grade claims.
- `Sector` and workplace do not always line up cleanly. Workplace is still useful for job-quality cuts, but it is not a substitute for sector.

## Findings I Checked and Kept in the Notes Rather Than Leading With

- The hidden-homemaker story gets even sharper if you separate `own account` from `unpaid family worker` by state. Bihar leans more unpaid-family; Jammu and Kashmir leans strongly own-account.
- The child-proxy story gets stronger with `child 0-2`, but `child 0-5` is safer for sample size and easier for a lay audience.
- The male comparison is useful as a robustness check, but it is not a story by itself. The interesting fact is that married graduate men barely move when a child is present, while women move a lot.
- The technical-education story is real, but it is less intuitive than the graduate occupation story. That is why it sits in the secondary section.
- `nonformal_regular_top_occupations.csv` has a quietly strong teacher angle too. Primary and secondary teachers show up inside nonformal regular work with surprisingly low medians.

## Candidate Story Angles

- Marriage appears to overpower education for many women’s labour-market attachment, and a young child in the household makes that worse.
- India’s female labour story may be understated when homemakers in agrarian households still do real work that only shows up on a different PLFS lens.
- A large share of `regular salaried` work looks closer to semi-formal or informal work once contract, leave, social-security, and occupation fields are combined.
- Graduate mismatch is less about dramatic manual labour and more about graduates landing in farm and retail roles, plus a lower-tier technical-education pipeline that often fails to deliver good jobs.
- Public works may compress some gaps without actually being the higher-paying casual-work option.

## Useful Follow-Ups for v4

- Break the marriage cliff by occupation and industry using the same stronger household-child proxy.
- Map the hidden-work finding at district level with stricter sample and weighted-size thresholds, especially for Bihar, Madhya Pradesh, and Uttar Pradesh farm households.
- If an official NCO skill-level crosswalk is available, replace the hand-built occupation buckets with a cleaner mismatch ladder.
- Compare these same patterns with older PLFS waves to see which are structural and which look new in `2024`.
- Push the technical-education story one step further into placement quality: contract, social security, and firm size by credential.
