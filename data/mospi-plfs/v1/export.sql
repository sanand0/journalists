PRAGMA threads=4;

CREATE OR REPLACE TEMP VIEW plfs AS
SELECT *
FROM 'plfs.parquet';

COPY (
  SELECT
    COUNT(*) AS rows,
    COUNT(DISTINCT "Person ID") AS distinct_persons,
    MIN("Survey Date") AS min_survey_date,
    MAX("Survey Date") AS max_survey_date,
    SUM("Person Subsample Multiplier") AS total_person_weight,
    quantile_cont("Person Subsample Multiplier", 0.5) AS median_person_weight,
    quantile_cont("Person Subsample Multiplier", 0.99) AS p99_person_weight
  FROM plfs
) TO 'v1/out/dataset_overview.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH hours AS (
    SELECT unnest([
      "Day 1 - Activity 1 - Hours", "Day 1 - Activity 2 - Hours",
      "Day 2 - Activity 1 - Hours", "Day 2 - Activity 2 - Hours",
      "Day 3 - Activity 1 - Hours", "Day 3 - Activity 2 - Hours",
      "Day 4 - Activity 1 - Hours", "Day 4 - Activity 2 - Hours",
      "Day 5 - Activity 1 - Hours", "Day 5 - Activity 2 - Hours",
      "Day 6 - Activity 1 - Hours", "Day 6 - Activity 2 - Hours",
      "Day 7 - Activity 1 - Hours", "Day 7 - Activity 2 - Hours"
    ]) AS raw_value
    FROM plfs
  ),
  wages AS (
    SELECT unnest([
      "Day 1 - Activity 1 - Wage", "Day 1 - Activity 2 - Wage",
      "Day 2 - Activity 1 - Wage", "Day 2 - Activity 2 - Wage",
      "Day 3 - Activity 1 - Wage", "Day 3 - Activity 2 - Wage",
      "Day 4 - Activity 1 - Wage", "Day 4 - Activity 2 - Wage",
      "Day 5 - Activity 1 - Wage", "Day 5 - Activity 2 - Wage",
      "Day 6 - Activity 1 - Wage", "Day 6 - Activity 2 - Wage",
      "Day 7 - Activity 1 - Wage", "Day 7 - Activity 2 - Wage"
    ]) AS raw_value
    FROM plfs
  )
  SELECT
    'hours' AS field,
    COUNT(*) AS cells,
    SUM(CASE WHEN raw_value IS NULL THEN 1 ELSE 0 END) AS null_cells,
    SUM(CASE WHEN raw_value IS NOT NULL AND TRY_CAST(raw_value AS BIGINT) IS NULL THEN 1 ELSE 0 END) AS non_numeric_cells,
    MIN(TRY_CAST(raw_value AS BIGINT)) AS min_value,
    MAX(TRY_CAST(raw_value AS BIGINT)) AS max_value,
    SUM(CASE WHEN TRY_CAST(raw_value AS BIGINT) > 24 THEN 1 ELSE 0 END) AS gt_24_cells
  FROM hours
  UNION ALL
  SELECT
    'wages' AS field,
    COUNT(*) AS cells,
    SUM(CASE WHEN raw_value IS NULL THEN 1 ELSE 0 END) AS null_cells,
    SUM(CASE WHEN raw_value IS NOT NULL AND TRY_CAST(raw_value AS BIGINT) IS NULL THEN 1 ELSE 0 END) AS non_numeric_cells,
    MIN(TRY_CAST(raw_value AS BIGINT)) AS min_value,
    MAX(TRY_CAST(raw_value AS BIGINT)) AS max_value,
    SUM(CASE WHEN TRY_CAST(raw_value AS BIGINT) > 100000 THEN 1 ELSE 0 END) AS gt_24_cells
  FROM wages
) TO 'v1/out/daily_field_quality.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH base AS (
    SELECT
      "Sector" AS sector,
      "Person Subsample Multiplier" AS w,
      CASE
        WHEN list_count(list_filter([
          "Day 1 - Activity 1 - Status", "Day 1 - Activity 2 - Status",
          "Day 2 - Activity 1 - Status", "Day 2 - Activity 2 - Status",
          "Day 3 - Activity 1 - Status", "Day 3 - Activity 2 - Status",
          "Day 4 - Activity 1 - Status", "Day 4 - Activity 2 - Status",
          "Day 5 - Activity 1 - Status", "Day 5 - Activity 2 - Status",
          "Day 6 - Activity 1 - Status", "Day 6 - Activity 2 - Status",
          "Day 7 - Activity 1 - Status", "Day 7 - Activity 2 - Status"
        ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) > 0
          THEN 1
        ELSE 0
      END AS had_week_work,
      list_count(list_filter([
        "Day 1 - Activity 1 - Status", "Day 1 - Activity 2 - Status",
        "Day 2 - Activity 1 - Status", "Day 2 - Activity 2 - Status",
        "Day 3 - Activity 1 - Status", "Day 3 - Activity 2 - Status",
        "Day 4 - Activity 1 - Status", "Day 4 - Activity 2 - Status",
        "Day 5 - Activity 1 - Status", "Day 5 - Activity 2 - Status",
        "Day 6 - Activity 1 - Status", "Day 6 - Activity 2 - Status",
        "Day 7 - Activity 1 - Status", "Day 7 - Activity 2 - Status"
      ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) AS work_status_cells,
      coalesce(TRY_CAST("Day 1 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 2 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 3 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 4 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 5 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 6 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 7 - Total Hours" AS BIGINT), 0) AS week_hours
    FROM plfs
    WHERE "Principal Activity Status" = 'attended domestic duties only'
      AND "Sex" = 'female'
  )
  SELECT
    sector,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    SUM(had_week_work) AS n_had_week_work,
    ROUND(SUM(CASE WHEN had_week_work = 1 THEN w ELSE 0 END), 0) AS wt_had_week_work,
    ROUND(100.0 * SUM(CASE WHEN had_week_work = 1 THEN w ELSE 0 END) / SUM(w), 1) AS pct_had_week_work,
    ROUND(AVG(CASE WHEN had_week_work = 1 THEN week_hours END), 1) AS avg_week_hours_if_worked,
    ROUND(quantile_cont(CASE WHEN had_week_work = 1 THEN week_hours END, 0.5), 1) AS median_week_hours_if_worked,
    ROUND(AVG(CASE WHEN had_week_work = 1 THEN work_status_cells END), 2) AS avg_work_status_cells_if_worked,
    ROUND(quantile_cont(CASE WHEN had_week_work = 1 THEN work_status_cells END, 0.5), 1) AS median_work_status_cells_if_worked,
    ROUND(quantile_cont(CASE WHEN had_week_work = 1 THEN work_status_cells END, 0.9), 1) AS p90_work_status_cells_if_worked
  FROM base
  GROUP BY 1
  ORDER BY 1
) TO 'v1/out/domestic_duties_hidden_work_summary.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH base AS (
    SELECT
      "Sector" AS sector,
      CASE
        WHEN "Age" BETWEEN 15 AND 24 THEN '15-24'
        WHEN "Age" BETWEEN 25 AND 44 THEN '25-44'
        WHEN "Age" BETWEEN 45 AND 59 THEN '45-59'
        WHEN "Age" >= 60 THEN '60+'
        ELSE '<15'
      END AS age_band,
      "General Education Level" AS education,
      "Person Subsample Multiplier" AS w,
      CASE
        WHEN list_count(list_filter([
          "Day 1 - Activity 1 - Status", "Day 1 - Activity 2 - Status",
          "Day 2 - Activity 1 - Status", "Day 2 - Activity 2 - Status",
          "Day 3 - Activity 1 - Status", "Day 3 - Activity 2 - Status",
          "Day 4 - Activity 1 - Status", "Day 4 - Activity 2 - Status",
          "Day 5 - Activity 1 - Status", "Day 5 - Activity 2 - Status",
          "Day 6 - Activity 1 - Status", "Day 6 - Activity 2 - Status",
          "Day 7 - Activity 1 - Status", "Day 7 - Activity 2 - Status"
        ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) > 0
          THEN 1
        ELSE 0
      END AS had_week_work
    FROM plfs
    WHERE "Principal Activity Status" = 'attended domestic duties only'
      AND "Sex" = 'female'
  )
  SELECT
    sector,
    age_band,
    education,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    SUM(had_week_work) AS n_had_week_work,
    ROUND(100.0 * SUM(CASE WHEN had_week_work = 1 THEN w ELSE 0 END) / SUM(w), 1) AS pct_had_week_work
  FROM base
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 25
  ORDER BY pct_had_week_work DESC, wt DESC
) TO 'v1/out/domestic_duties_hidden_work_by_age_education.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH base AS (
    SELECT
      "Sector" AS sector,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE "Principal Activity Status" = 'attended domestic duties only'
      AND "Sex" = 'female'
      AND list_count(list_filter([
        "Day 1 - Activity 1 - Status", "Day 1 - Activity 2 - Status",
        "Day 2 - Activity 1 - Status", "Day 2 - Activity 2 - Status",
        "Day 3 - Activity 1 - Status", "Day 3 - Activity 2 - Status",
        "Day 4 - Activity 1 - Status", "Day 4 - Activity 2 - Status",
        "Day 5 - Activity 1 - Status", "Day 5 - Activity 2 - Status",
        "Day 6 - Activity 1 - Status", "Day 6 - Activity 2 - Status",
        "Day 7 - Activity 1 - Status", "Day 7 - Activity 2 - Status"
      ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) > 0
  )
  SELECT
    sector,
    cws_status,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(w) / SUM(SUM(w)) OVER (PARTITION BY sector), 1) AS pct_within_workers
  FROM base
  GROUP BY 1, 2
  ORDER BY sector, wt DESC
) TO 'v1/out/domestic_duties_hidden_work_cws.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH base AS (
    SELECT
      "Sector" AS sector,
      "Person Subsample Multiplier" AS w,
      unnest(list_filter([
        "Day 1 - Activity 1 - Status", "Day 1 - Activity 2 - Status",
        "Day 2 - Activity 1 - Status", "Day 2 - Activity 2 - Status",
        "Day 3 - Activity 1 - Status", "Day 3 - Activity 2 - Status",
        "Day 4 - Activity 1 - Status", "Day 4 - Activity 2 - Status",
        "Day 5 - Activity 1 - Status", "Day 5 - Activity 2 - Status",
        "Day 6 - Activity 1 - Status", "Day 6 - Activity 2 - Status",
        "Day 7 - Activity 1 - Status", "Day 7 - Activity 2 - Status"
      ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) AS work_status
    FROM plfs
    WHERE "Principal Activity Status" = 'attended domestic duties only'
      AND "Sex" = 'female'
  )
  SELECT
    sector,
    work_status,
    COUNT(*) AS cells,
    ROUND(SUM(w), 0) AS wt
  FROM base
  GROUP BY 1, 2
  ORDER BY sector, wt DESC
) TO 'v1/out/domestic_duties_hidden_work_status_cells.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH salaried AS (
    SELECT
      "Sector" AS sector,
      "Sex" AS sex,
      "Principal Workplace Location" AS workplace,
      "Principal Job Contract Type" AS contract_type,
      "Principal Job - Paid Leave" AS paid_leave,
      "Principal Job - Social Security" AS social_security,
      "CWS Earnings (Salaried)" AS earnings,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
  )
  SELECT
    sector,
    sex,
    workplace,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(CASE WHEN contract_type = 'no written job contract' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_contract,
    ROUND(100.0 * SUM(CASE WHEN paid_leave = 'no' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_paid_leave,
    ROUND(100.0 * SUM(CASE WHEN social_security = 'not eligible for any of above social security benefits' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_social_security,
    ROUND(quantile_cont(earnings, 0.5), 0) AS median_earnings
  FROM salaried
  GROUP BY 1, 2, 3
  ORDER BY sector, workplace, sex
) TO 'v1/out/salaried_workplace_insecurity.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH salaried AS (
    SELECT
      "Principal Workers Count" AS workers_count,
      "Principal Job Contract Type" AS contract_type,
      "Principal Job - Paid Leave" AS paid_leave,
      "Principal Job - Social Security" AS social_security,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
  )
  SELECT
    workers_count,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(CASE WHEN contract_type = 'no written job contract' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_contract,
    ROUND(100.0 * SUM(CASE WHEN paid_leave = 'no' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_paid_leave,
    ROUND(100.0 * SUM(CASE WHEN social_security = 'not eligible for any of above social security benefits' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_social_security
  FROM salaried
  GROUP BY 1
  ORDER BY wt DESC
) TO 'v1/out/salaried_microfirm_overall.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH salaried AS (
    SELECT
      "Sex" AS sex,
      "Sector" AS sector,
      "General Education Level" AS education,
      "Principal Workers Count" AS workers_count,
      "Principal Job Contract Type" AS contract_type,
      "Principal Job - Social Security" AS social_security,
      "CWS Earnings (Salaried)" AS earnings,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
      AND "General Education Level" IN ('graduate', 'postgraduate and above')
  )
  SELECT
    sex,
    sector,
    education,
    workers_count,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(CASE WHEN contract_type = 'no written job contract' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_contract,
    ROUND(100.0 * SUM(CASE WHEN social_security = 'not eligible for any of above social security benefits' THEN w ELSE 0 END) / SUM(w), 1) AS pct_no_social_security,
    ROUND(quantile_cont(earnings, 0.5), 0) AS median_earnings
  FROM salaried
  GROUP BY 1, 2, 3, 4
  ORDER BY education, sex, sector, workers_count
) TO 'v1/out/salaried_microfirm_graduates.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH salaried AS (
    SELECT
      "Sex" AS sex,
      "Sector" AS sector,
      "Principal Job Contract Type" AS contract_type,
      "Person Subsample Multiplier" AS w,
      CASE
        WHEN list_count(list_filter([
          "Day 1 - Activity 2 - Status", "Day 2 - Activity 2 - Status",
          "Day 3 - Activity 2 - Status", "Day 4 - Activity 2 - Status",
          "Day 5 - Activity 2 - Status", "Day 6 - Activity 2 - Status",
          "Day 7 - Activity 2 - Status"
        ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) > 0
          THEN 1
        ELSE 0
      END AS has_second_work
    FROM plfs
    WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
  )
  SELECT
    sex,
    sector,
    contract_type,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    SUM(has_second_work) AS n_with_second_work,
    ROUND(100.0 * SUM(CASE WHEN has_second_work = 1 THEN w ELSE 0 END) / SUM(w), 1) AS pct_with_second_work
  FROM salaried
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 100
  ORDER BY pct_with_second_work DESC, wt DESC
) TO 'v1/out/salaried_second_job_contracts.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH base AS (
    SELECT
      "Sex" AS sex,
      "Sector" AS sector,
      "Principal Job Contract Type" AS contract_type,
      "Person Subsample Multiplier" AS w,
      unnest(list_filter([
        "Day 1 - Activity 2 - Status", "Day 2 - Activity 2 - Status",
        "Day 3 - Activity 2 - Status", "Day 4 - Activity 2 - Status",
        "Day 5 - Activity 2 - Status", "Day 6 - Activity 2 - Status",
        "Day 7 - Activity 2 - Status"
      ], x -> x IS NOT NULL)) AS second_status
    FROM plfs
    WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
  )
  SELECT
    sex,
    sector,
    contract_type,
    second_status,
    COUNT(*) AS cells,
    ROUND(SUM(w), 0) AS wt
  FROM base
  GROUP BY 1, 2, 3, 4
  HAVING SUM(w) > 200000000
  ORDER BY sex, sector, contract_type, wt DESC
) TO 'v1/out/salaried_second_job_types.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH salaried AS (
    SELECT
      "Sex" AS sex,
      "Sector" AS sector,
      "Principal Job Contract Type" AS contract_type,
      "Person Subsample Multiplier" AS w,
      coalesce(TRY_CAST("Day 1 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 2 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 3 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 4 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 5 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 6 - Total Hours" AS BIGINT), 0) +
      coalesce(TRY_CAST("Day 7 - Total Hours" AS BIGINT), 0) AS week_hours,
      CASE
        WHEN list_count(list_filter([
          "Day 1 - Activity 2 - Status", "Day 2 - Activity 2 - Status",
          "Day 3 - Activity 2 - Status", "Day 4 - Activity 2 - Status",
          "Day 5 - Activity 2 - Status", "Day 6 - Activity 2 - Status",
          "Day 7 - Activity 2 - Status"
        ], x -> x IS NOT NULL AND (x LIKE 'worked%' OR x LIKE 'had work%'))) > 0
          THEN 1
        ELSE 0
      END AS has_second_work
    FROM plfs
    WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
  )
  SELECT
    sex,
    sector,
    contract_type,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(CASE WHEN has_second_work = 1 THEN w ELSE 0 END) / SUM(w), 1) AS pct_with_second_work,
    ROUND(AVG(CASE WHEN has_second_work = 1 THEN week_hours END), 1) AS avg_week_hours_if_second_work,
    ROUND(quantile_cont(CASE WHEN has_second_work = 1 THEN week_hours END, 0.5), 1) AS median_week_hours_if_second_work
  FROM salaried
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 100
  ORDER BY pct_with_second_work DESC, wt DESC
) TO 'v1/out/salaried_second_job_hours.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  SELECT
    "Unemployment Duration" AS duration,
    COUNT(*) AS n,
    ROUND(SUM("Person Subsample Multiplier"), 0) AS wt
  FROM plfs
  WHERE "Principal Activity Status" = 'did not work but was seeking and/or available for work'
    AND "Unemployment Duration" IS NOT NULL
  GROUP BY 1
  ORDER BY wt DESC
) TO 'v1/out/unemployment_duration_distribution.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH seekers AS (
    SELECT
      "Sex" AS sex,
      "Sector" AS sector,
      CASE
        WHEN "Age" BETWEEN 15 AND 24 THEN '15-24'
        WHEN "Age" BETWEEN 25 AND 34 THEN '25-34'
        WHEN "Age" BETWEEN 35 AND 44 THEN '35-44'
        WHEN "Age" BETWEEN 45 AND 59 THEN '45-59'
        ELSE '60+'
      END AS age_band,
      "Unemployment Duration" AS duration,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE "Principal Activity Status" = 'did not work but was seeking and/or available for work'
  )
  SELECT
    sex,
    sector,
    age_band,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(CASE WHEN duration = 'more than 3 years' THEN w ELSE 0 END) / SUM(w), 1) AS pct_jobless_3y_plus,
    ROUND(100.0 * SUM(CASE WHEN duration IN (
      'more than 1 year but less than or equal to 2 years',
      'more than 2 years but less than or equal to 3 years',
      'more than 3 years'
    ) THEN w ELSE 0 END) / SUM(w), 1) AS pct_jobless_1y_plus
  FROM seekers
  GROUP BY 1, 2, 3
  ORDER BY pct_jobless_3y_plus DESC, wt DESC
) TO 'v1/out/unemployment_duration_by_age_band.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);

COPY (
  WITH seekers AS (
    SELECT
      "Sex" AS sex,
      "Sector" AS sector,
      "General Education Level" AS education,
      "Unemployment Duration" AS duration,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE "Principal Activity Status" = 'did not work but was seeking and/or available for work'
  )
  SELECT
    sex,
    sector,
    education,
    COUNT(*) AS n,
    ROUND(SUM(w), 0) AS wt,
    ROUND(100.0 * SUM(CASE WHEN duration = 'more than 3 years' THEN w ELSE 0 END) / SUM(w), 1) AS pct_jobless_3y_plus,
    ROUND(100.0 * SUM(CASE WHEN duration IN (
      'more than 1 year but less than or equal to 2 years',
      'more than 2 years but less than or equal to 3 years',
      'more than 3 years'
    ) THEN w ELSE 0 END) / SUM(w), 1) AS pct_jobless_1y_plus
  FROM seekers
  GROUP BY 1, 2, 3
  HAVING COUNT(*) >= 100
  ORDER BY pct_jobless_3y_plus DESC, wt DESC
) TO 'v1/out/unemployment_duration_by_education.csv'
WITH (HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE 1);
