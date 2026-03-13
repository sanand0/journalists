PRAGMA threads=4;

CREATE OR REPLACE TEMP VIEW plfs AS
SELECT * FROM 'plfs.parquet';

CREATE OR REPLACE TEMP VIEW base AS
SELECT
  "Person ID" AS person_id,
  "Person Subsample Multiplier" AS wt,
  "Sex" AS sex,
  "Age" AS age,
  CASE
    WHEN "Age" BETWEEN 15 AND 17 THEN '15-17'
    WHEN "Age" BETWEEN 18 AND 24 THEN '18-24'
    WHEN "Age" BETWEEN 25 AND 34 THEN '25-34'
    WHEN "Age" BETWEEN 35 AND 44 THEN '35-44'
    WHEN "Age" BETWEEN 45 AND 59 THEN '45-59'
    WHEN "Age" >= 60 THEN '60+'
  END AS age_band,
  "Marital Status" AS marital_status,
  CASE
    WHEN "General Education Level" IN ('graduate', 'postgraduate and above') THEN 'graduate+'
    WHEN "General Education Level" IN ('higher secondary', 'secondary') THEN 'secondary_to_hs'
    ELSE 'below_secondary'
  END AS education_band,
  "General Education Level" AS education_level,
  "Sector" AS sector,
  "Household Social Group" AS social_group,
  "Household Religion" AS religion,
  "Household Type" AS household_type,
  "Current Attendance Status" AS attendance_status,
  "Principal Activity Status" AS principal_status,
  "Subsidiary Work Engagement" AS subsidiary_work_engagement,
  "Principal Job - Paid Leave" AS principal_paid_leave,
  "Principal Job - Social Security" AS principal_social_security,
  "Training Completed (Last 365 Days)" AS training_completed_last_365_days,
  "Household Monthly Consumer Expenditure (MPCE)" AS mpce
FROM plfs;

COPY (
  SELECT
    COUNT(*) AS rows,
    COUNT(DISTINCT person_id) AS distinct_persons,
    MIN(age) AS min_age,
    MAX(age) AS max_age,
    MIN(wt) AS min_weight,
    MAX(wt) AS max_weight,
    AVG(wt) AS avg_weight
  FROM base
) TO 'v1/out/overview.csv' (HEADER, DELIMITER ',');

COPY (
  WITH dropouts AS (
    SELECT *
    FROM base
    WHERE age BETWEEN 15 AND 24
      AND attendance_status LIKE 'attended but currently not attending%'
  )
  SELECT
    sex,
    age_band,
    marital_status,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to attend domestic chores' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_domestic_chore_share_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to attend domestic chores' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_domestic_chore_share_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to supplement household income' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_income_share_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to supplement household income' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_income_share_pct
  FROM dropouts
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 200
  ORDER BY weighted_domestic_chore_share_pct DESC
) TO 'v1/out/dropout_reasons_young_people.csv' (HEADER, DELIMITER ',');

COPY (
  WITH dropouts AS (
    SELECT *
    FROM base
    WHERE age BETWEEN 15 AND 24
      AND sex = 'female'
      AND marital_status = 'currently married'
      AND attendance_status LIKE 'attended but currently not attending%'
  )
  SELECT
    sector,
    social_group,
    religion,
    household_type,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to attend domestic chores' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_domestic_chore_share_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to attend domestic chores' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_domestic_chore_share_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to supplement household income' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_income_share_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN attendance_status = 'attended but currently not attending - to supplement household income' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_income_share_pct
  FROM dropouts
  GROUP BY 1, 2, 3, 4
  HAVING COUNT(*) >= 120
  ORDER BY weighted_domestic_chore_share_pct DESC
) TO 'v1/out/dropout_reasons_married_young_women_detail.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    sex,
    marital_status,
    age_band,
    education_band,
    sector,
    household_type,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'attended domestic duties only' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_domestic_only_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'attended domestic duties only' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_domestic_only_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'worked as regular salaried/wage employee' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_salaried_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'worked as regular salaried/wage employee' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_salaried_pct
  FROM base
  WHERE age BETWEEN 25 AND 44
    AND household_type = 'regular wage/salary earning'
  GROUP BY 1, 2, 3, 4, 5, 6
  HAVING COUNT(*) >= 200
  ORDER BY weighted_domestic_only_pct DESC
) TO 'v1/out/regular_wage_household_gender_gap.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    age_band,
    education_band,
    sector,
    marital_status,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'worked as regular salaried/wage employee' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_salaried_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'worked as regular salaried/wage employee' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_salaried_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'attended domestic duties only' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_domestic_only_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'attended domestic duties only' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_domestic_only_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status LIKE 'worked%' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_any_work_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status LIKE 'worked%' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_any_work_pct
  FROM base
  WHERE sex = 'female'
    AND age BETWEEN 25 AND 44
  GROUP BY 1, 2, 3, 4
  HAVING COUNT(*) >= 180
  ORDER BY age_band, education_band, sector, weighted_salaried_pct DESC
) TO 'v1/out/female_work_by_marital_status.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    sex,
    age_band,
    social_group,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN subsidiary_work_engagement = 'yes' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_subwork_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN subsidiary_work_engagement = 'yes' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_subwork_pct
  FROM base
  WHERE age BETWEEN 18 AND 24
    AND principal_status = 'attended educational institution'
    AND sector = 'rural'
    AND household_type = 'self-employed in agriculture'
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 250
  ORDER BY weighted_subwork_pct DESC
) TO 'v1/out/student_subwork_farm_households.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    'all_students_18_24' AS group_name,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN subsidiary_work_engagement = 'yes' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_subwork_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN subsidiary_work_engagement = 'yes' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_subwork_pct
  FROM base
  WHERE age BETWEEN 18 AND 24
    AND principal_status = 'attended educational institution'

  UNION ALL

  SELECT
    'rural_farm_household_students_18_24' AS group_name,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN subsidiary_work_engagement = 'yes' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_subwork_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN subsidiary_work_engagement = 'yes' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_subwork_pct
  FROM base
  WHERE age BETWEEN 18 AND 24
    AND principal_status = 'attended educational institution'
    AND sector = 'rural'
    AND household_type = 'self-employed in agriculture'
) TO 'v1/out/student_subwork_benchmarks.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    sex,
    age_band,
    social_group,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'worked as helper in h.h. enterprise (unpaid family worker)' THEN 1.0
          ELSE 0.0
        END
      ) FILTER (WHERE principal_status LIKE 'worked%'),
      1
    ) AS raw_unpaid_family_share_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'worked as helper in h.h. enterprise (unpaid family worker)' THEN wt
          ELSE 0
        END
      ) / SUM(
        CASE
          WHEN principal_status LIKE 'worked%' THEN wt
          ELSE 0
        END
      ),
      1
    ) AS weighted_unpaid_family_share_pct
  FROM base
  WHERE age >= 15
    AND sector = 'rural'
    AND household_type = 'self-employed in agriculture'
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 300
  ORDER BY age_band, social_group, sex
) TO 'v1/out/unpaid_family_farm_workers.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    sex,
    age_band,
    marital_status,
    education_band,
    sector,
    social_group,
    religion,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_paid_leave = 'no' THEN 1.0
          ELSE 0.0
        END
      ) FILTER (WHERE principal_paid_leave IS NOT NULL),
      1
    ) AS raw_no_paid_leave_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_paid_leave = 'no' THEN wt
          ELSE 0
        END
      ) / SUM(
        CASE
          WHEN principal_paid_leave IS NOT NULL THEN wt
          ELSE 0
        END
      ),
      1
    ) AS weighted_no_paid_leave_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_social_security = 'not eligible for any of above social security benefits' THEN 1.0
          ELSE 0.0
        END
      ) FILTER (WHERE principal_social_security IS NOT NULL),
      1
    ) AS raw_no_social_security_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_social_security = 'not eligible for any of above social security benefits' THEN wt
          ELSE 0
        END
      ) / SUM(
        CASE
          WHEN principal_social_security IS NOT NULL THEN wt
          ELSE 0
        END
      ),
      1
    ) AS weighted_no_social_security_pct
  FROM base
  WHERE principal_status = 'worked as regular salaried/wage employee'
    AND household_type = 'regular wage/salary earning'
  GROUP BY 1, 2, 3, 4, 5, 6, 7
  HAVING COUNT(*) >= 120
  ORDER BY weighted_no_social_security_pct DESC
) TO 'v1/out/salaried_worker_security_gaps.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    'all_regular_wage_household_salaried_workers' AS group_name,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_paid_leave = 'no' THEN 1.0
          ELSE 0.0
        END
      ) FILTER (WHERE principal_paid_leave IS NOT NULL),
      1
    ) AS raw_no_paid_leave_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_paid_leave = 'no' THEN wt
          ELSE 0
        END
      ) / SUM(
        CASE
          WHEN principal_paid_leave IS NOT NULL THEN wt
          ELSE 0
        END
      ),
      1
    ) AS weighted_no_paid_leave_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_social_security = 'not eligible for any of above social security benefits' THEN 1.0
          ELSE 0.0
        END
      ) FILTER (WHERE principal_social_security IS NOT NULL),
      1
    ) AS raw_no_social_security_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_social_security = 'not eligible for any of above social security benefits' THEN wt
          ELSE 0
        END
      ) / SUM(
        CASE
          WHEN principal_social_security IS NOT NULL THEN wt
          ELSE 0
        END
      ),
      1
    ) AS weighted_no_social_security_pct
  FROM base
  WHERE principal_status = 'worked as regular salaried/wage employee'
    AND household_type = 'regular wage/salary earning'
) TO 'v1/out/salaried_worker_security_benchmarks.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    sex,
    marital_status,
    education_band,
    sector,
    household_type,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'did not work but was seeking and/or available for work' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_unemployed_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'did not work but was seeking and/or available for work' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_unemployed_pct,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN principal_status = 'worked as regular salaried/wage employee' THEN 1.0
          ELSE 0.0
        END
      ),
      1
    ) AS raw_salaried_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN principal_status = 'worked as regular salaried/wage employee' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      1
    ) AS weighted_salaried_pct
  FROM base
  WHERE age BETWEEN 25 AND 34
    AND marital_status = 'never married'
  GROUP BY 1, 2, 3, 4, 5
  HAVING COUNT(*) >= 250
  ORDER BY weighted_unemployed_pct DESC
) TO 'v1/out/never_married_25_34_unemployment.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    sex,
    age_band,
    education_band,
    sector,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN training_completed_last_365_days = 'yes' THEN 1.0
          ELSE 0.0
        END
      ),
      2
    ) AS raw_training_completed_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN training_completed_last_365_days = 'yes' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      2
    ) AS weighted_training_completed_pct
  FROM base
  WHERE age BETWEEN 15 AND 34
  GROUP BY 1, 2, 3, 4
  HAVING COUNT(*) >= 250
  ORDER BY weighted_training_completed_pct DESC
) TO 'v1/out/training_completion_youth.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    'all_15_34' AS group_name,
    COUNT(*) AS sample_n,
    ROUND(SUM(wt)) AS weighted_pop,
    ROUND(
      100.0 * AVG(
        CASE
          WHEN training_completed_last_365_days = 'yes' THEN 1.0
          ELSE 0.0
        END
      ),
      2
    ) AS raw_training_completed_pct,
    ROUND(
      100.0 * SUM(
        CASE
          WHEN training_completed_last_365_days = 'yes' THEN wt
          ELSE 0
        END
      ) / SUM(wt),
      2
    ) AS weighted_training_completed_pct
  FROM base
  WHERE age BETWEEN 15 AND 34
) TO 'v1/out/training_completion_benchmark.csv' (HEADER, DELIMITER ',');
