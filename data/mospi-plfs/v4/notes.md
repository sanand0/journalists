# PLFS v4 Notes

## Reproduce

- Run `./v4/analyze.py` to regenerate `v4/outputs/`.
- Run `./v4/run.sh` if you want the wrapper entrypoint instead.
- `v4` first reruns `./v3/analyze.py`, copies the full `v3/outputs/` tree into `v4/outputs/`, and then adds the new `v4` tables.

## Outside Idea Sources I Checked

- India Economic Survey 2024-25, Chapter 4 on employment and occupational mismatch:
  [https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/vol2_ch04.pdf](https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/vol2_ch04.pdf)
- ILO, *India Employment Report 2024: Youth employment, education and skills*:
  [https://www.ilo.org/publications/india-employment-report-2024-youth-employment-education-and-skills](https://www.ilo.org/publications/india-employment-report-2024-youth-employment-education-and-skills)
- Ideas for India on women’s talent misallocation:
  [https://www.ideasforindia.in/topics/macroeconomics/beyond-participation-tackling-the-misallocation-of-womens-talent-in-india](https://www.ideasforindia.in/topics/macroeconomics/beyond-participation-tackling-the-misallocation-of-womens-talent-in-india)
- Ideas for India on female labour-force measurement and data quality:
  [https://www.ideasforindia.in/topics/social-identity/female-labour-force-participation-measurement-and-data-quality](https://www.ideasforindia.in/topics/social-identity/female-labour-force-participation-measurement-and-data-quality)
- World Bank / IFC women’s-employment legal and childcare context for India:
  [https://documents1.worldbank.org/curated/en/377711511422588789/pdf/Main-Report.pdf](https://documents1.worldbank.org/curated/en/377711511422588789/pdf/Main-Report.pdf)
- World Bank note on women’s labour-force participation in India:
  [https://documents1.worldbank.org/curated/en/099950506282325566/pdf/IDU0c4c7e5b705c31049590a7de00a50244345ba.pdf](https://documents1.worldbank.org/curated/en/099950506282325566/pdf/IDU0c4c7e5b705c31049590a7de00a50244345ba.pdf)
- WHO, *Employment and working conditions of nurses in private hospitals in Delhi*:
  [https://www.who.int/publications/i/item/9789290209720](https://www.who.int/publications/i/item/9789290209720)

These did not provide `v4` numbers. They were prompts for what to test locally: household role after marriage, long job-search duration, education and health job quality, and technical-credential ladders.

## What I Added In v4

- Household-role tables for currently married graduate women aged `25-34`, using `Relationship to Head` plus the stronger child-in-household proxy.
- A weighted household-role model that tests whether the role gap survives after controlling for `child under 5`, state, sector, social group, household type, and religion.
- Young-profession job-quality tables for teaching, nursing, software, and medicine.
- A technical-credential quality table that keeps both job entry and job quality in the same view.
- A long-duration job-search table for graduate job seekers aged `25-34`.
- A stricter district screen for the hidden-homemaker result.

## Method Notes

- `Person ID` is unique across all `415,549` rows.
- Survey dates span `2024-01-03` to `2024-12-31`.
- I still use `Person Subsample Multiplier` for weighted shares. Its raw sum does not look like literal headcounts, so percentages remain safer than weighted totals.
- `v4` keeps the same conservative `strict formal` definition from `v3`: written contract + paid leave + some social security, restricted to principal-status regular salaried work.
- The stronger household key from `v3` is reused here:
  `Sector + Stratum + Sub-Stratum + Sub-Sample + FSU + Sample Segment/Sub-Block + Second Stage Stratum + Household Number`.
- The `wife_role_in_extended_household` label in `married_graduate_household_role_*.csv` is a readable shorthand, not an official PLFS field. It combines `spouse of head` and `spouse of married child`.
- The comparison group `self_or_child_role` combines `self` and `married child`.
- The household-role model is deliberately narrow. It only compares those four relationship categories, because the small leftover categories are too noisy for a clean story.
- `selected_professions_quality_21_34.csv` and `selected_professions_gender_gaps_21_34.csv` only cover principal-status regular salaried workers aged `21-34`.
- `technical_credential_quality_21_34.csv` uses age `21-34` because it is the cleanest window for recent school-to-work transitions with workable sample sizes.
- In the technical-credential table, `regular_pct`, `seeking_pct`, `strict_formal_pct`, and `social_security_pct` are shares of all people with that credential in the `21-34` age band. `median_regular_salary` and `micro_small_regular_pct` are conditional on being in regular salaried work.

## District-Screen Notes

- `hidden_work_district_strict.csv` is intentionally conservative. It keeps only rural districts with `sample_n >= 100` and approximate homemaker weight `>= 0.4` on the project’s million-equivalent scale.
- Even that stricter filter still leaves some low-rate districts in the table. This is a reminder that district rankings are screening tools, not clean league tables.
- The big message is not that one district is exactly `64.0` and another is exactly `51.3`. The message is that the hidden-work pattern survives a much stricter district cut and remains concentrated in a relatively small set of places.

## Data Quality and Interpretation Notes

- `Relationship to Head` is a household-position field, not a literal `lives with in-laws` field. It is still highly informative about family structure.
- The job-seeker duration tables are subgroup analyses with small weighted totals. They are useful for rates, not population counts.
- `Other Teaching Professionals` appears to be a broad and messy occupation bucket, but it remains low-paid and weak on formality even after splitting by sex.
- Industry labels are much less readable than occupation labels for the teacher and nurse story. The occupation route is clearer for lay readers.
- The official NCO code or skill-level ladder is not available cleanly enough in this parquet for a robust crosswalk. I kept the occupation analysis human-readable instead of forcing a shaky skill ladder.

## Findings I Checked And Kept In Notes Rather Than Leading With

- The household-role gap is very large even before adding the child proxy, but the child proxy still matters independently in the model.
- The most striking long-duration job-search result is for urban currently married graduate women `25-34`. Rural currently married graduate women also look bad, but the urban number is cleaner and stronger.
- The teacher story is stronger than the industry-level education story because it lets the reader compare teachers directly with software developers and doctors.
- The technical-credential ladder is strongest for engineering and medicine. The `other subjects` credentials show high search rates too, but their occupation mix is too diffuse for a clean headline.
- The district hidden-work screen throws up strong outliers in Madhya Pradesh, Bihar, Uttar Pradesh, and Odisha, but the state-level story remains safer than district rank-ordering.

## Candidate Story Frames

- Marriage and childcare are not the whole story. Household position itself appears to matter for whether educated women stay in paid work.
- Some educated women who are still trying to work are not in a short job-search spell. They look stuck.
- The `good jobs` many families imagine for daughters, like teaching or nursing, often look much less formal and much less well-paid than software or medicine.
- Technical education in India behaves less like one ladder and more like several different ladders with very different job-quality payoffs.
- The hidden-homemaker story remains real even after raising the bar on district sample thresholds.

## Useful Follow-Ups For v5

- Compare the same household-role and long-duration job-search patterns with older PLFS waves.
- Add a map for `hidden_work_district_strict.csv`, but keep the thresholding visible in the graphic itself.
- Bring in an external NCO skill-level crosswalk if a clean occupation-code field can be recovered.
- Push the teacher and nurse story into public versus private sector splits if a reliable proxy can be built from enterprise type and workplace fields.
- Test whether the household-role gap varies sharply by state, especially in the south versus north comparison already visible in the marriage tables.
