CREATE OR REPLACE TEMP VIEW plfs AS
SELECT
  *,
  COALESCE("Day 1 - Total Hours", 0)
    + COALESCE("Day 2 - Total Hours", 0)
    + COALESCE("Day 3 - Total Hours", 0)
    + COALESCE("Day 4 - Total Hours", 0)
    + COALESCE("Day 5 - Total Hours", 0)
    + COALESCE("Day 6 - Total Hours", 0)
    + COALESCE(TRY_CAST("Day 7 - Total Hours" AS BIGINT), 0) AS week_hours
FROM read_parquet('../plfs.parquet');

CREATE OR REPLACE TEMP VIEW households AS
SELECT DISTINCT
  Panel,
  Quarter,
  Visit,
  Sector,
  "State/UT",
  "District",
  Stratum,
  "Sub-Stratum",
  "Sub-Sample",
  "First Stage Unit (FSU)",
  "Sample Segment/Sub-Block Number",
  "Second Stage Stratum Number",
  "Household Number",
  "Survey Status",
  "Response Status",
  "Household Substitution Reason",
  "Household Subsample Multiplier"
FROM plfs;

COPY (
  SELECT
    COUNT(*) AS rows,
    COUNT(DISTINCT "Person ID") AS distinct_person_ids,
    (SELECT COUNT(*) FROM households) AS distinct_households,
    MIN("Survey Date") AS min_survey_date,
    MAX("Survey Date") AS max_survey_date,
    MIN(Age) AS min_age,
    MAX(Age) AS max_age,
    COUNT(*) FILTER (WHERE Age >= 100) AS age_100_plus,
    COUNT(*) FILTER (WHERE "Person Subsample Multiplier" <> "Household Subsample Multiplier") AS unequal_weights,
    quantile_cont("Person Subsample Multiplier", 0.5) AS weight_p50,
    quantile_cont("Person Subsample Multiplier", 0.9) AS weight_p90,
    quantile_cont("Person Subsample Multiplier", 0.99) AS weight_p99,
    SUM("Person Subsample Multiplier") AS weight_sum_raw
  FROM plfs
) TO 'codex_outputs/dataset_profile.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    column_name,
    column_type
  FROM (DESCRIBE SELECT * FROM plfs)
  WHERE column_name LIKE 'Day %'
  ORDER BY column_name
) TO 'codex_outputs/quality_day_column_types.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    COUNT(*) AS wage_cells,
    COUNT(*) FILTER (WHERE wage IS NOT NULL) AS numeric_wage_cells,
    quantile_cont(wage, 0.5) FILTER (WHERE wage IS NOT NULL) AS median_wage,
    quantile_cont(wage, 0.99) FILTER (WHERE wage IS NOT NULL) AS p99_wage,
    MAX(wage) AS max_wage
  FROM (
    SELECT TRY_CAST("Day 1 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 1 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 2 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 2 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 3 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 3 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 4 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 4 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 5 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 5 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 6 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 6 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 7 - Activity 1 - Wage" AS BIGINT) AS wage FROM plfs
    UNION ALL
    SELECT TRY_CAST("Day 7 - Activity 2 - Wage" AS BIGINT) AS wage FROM plfs
  )
) TO 'codex_outputs/quality_daily_wage_profile.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    day_name,
    min_hours,
    max_hours,
    gt_24
  FROM (
    SELECT
      'Day 1' AS day_name,
      MIN("Day 1 - Total Hours") AS min_hours,
      MAX("Day 1 - Total Hours") AS max_hours,
      COUNT(*) FILTER (WHERE "Day 1 - Total Hours" > 24) AS gt_24
    FROM plfs
    UNION ALL
    SELECT
      'Day 2',
      MIN("Day 2 - Total Hours"),
      MAX("Day 2 - Total Hours"),
      COUNT(*) FILTER (WHERE "Day 2 - Total Hours" > 24)
    FROM plfs
    UNION ALL
    SELECT
      'Day 3',
      MIN("Day 3 - Total Hours"),
      MAX("Day 3 - Total Hours"),
      COUNT(*) FILTER (WHERE "Day 3 - Total Hours" > 24)
    FROM plfs
    UNION ALL
    SELECT
      'Day 4',
      MIN("Day 4 - Total Hours"),
      MAX("Day 4 - Total Hours"),
      COUNT(*) FILTER (WHERE "Day 4 - Total Hours" > 24)
    FROM plfs
    UNION ALL
    SELECT
      'Day 5',
      MIN("Day 5 - Total Hours"),
      MAX("Day 5 - Total Hours"),
      COUNT(*) FILTER (WHERE "Day 5 - Total Hours" > 24)
    FROM plfs
    UNION ALL
    SELECT
      'Day 6',
      MIN("Day 6 - Total Hours"),
      MAX("Day 6 - Total Hours"),
      COUNT(*) FILTER (WHERE "Day 6 - Total Hours" > 24)
    FROM plfs
    UNION ALL
    SELECT
      'Day 7',
      MIN(TRY_CAST("Day 7 - Total Hours" AS BIGINT)),
      MAX(TRY_CAST("Day 7 - Total Hours" AS BIGINT)),
      COUNT(*) FILTER (WHERE TRY_CAST("Day 7 - Total Hours" AS BIGINT) > 24)
    FROM plfs
  )
) TO 'codex_outputs/quality_daily_hours_profile.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      Sex,
      Sector,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" = 'attended domestic duties only'
  )
  SELECT
    Sex,
    Sector,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status LIKE 'worked%') AS worked_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status LIKE 'worked%') AS worked_w,
    100.0 * SUM(w) FILTER (WHERE cws_status LIKE 'worked%') / SUM(w) AS pct_worked_weekly
  FROM base
  GROUP BY 1, 2
  ORDER BY pct_worked_weekly DESC
) TO 'codex_outputs/domestic_hidden_work_overall.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      Sex,
      Sector,
      "CWS Status" AS cws_status,
      week_hours,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" = 'attended domestic duties only'
      AND "CWS Status" LIKE 'worked%'
  ),
  agg AS (
    SELECT
      Sex,
      Sector,
      cws_status,
      COUNT(*) AS n,
      SUM(w) AS w,
      quantile_cont(week_hours, 0.5) AS median_week_hours,
      quantile_cont(week_hours, 0.9) AS p90_week_hours,
      AVG(week_hours) AS avg_week_hours
    FROM base
    GROUP BY 1, 2, 3
  ),
  totals AS (
    SELECT
      Sex,
      Sector,
      SUM(n) AS total_n,
      SUM(w) AS total_w
    FROM agg
    GROUP BY 1, 2
  )
  SELECT
    agg.*,
    totals.total_n,
    totals.total_w,
    100.0 * agg.w / totals.total_w AS pct_of_hidden_workers
  FROM agg
  JOIN totals USING (Sex, Sector)
  ORDER BY totals.total_w DESC, agg.w DESC
) TO 'codex_outputs/domestic_hidden_work_breakdown.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      Sector,
      "General Education Level" AS education,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age BETWEEN 15 AND 59
      AND Sex = 'female'
      AND "Principal Activity Status" = 'attended domestic duties only'
  )
  SELECT
    Sector,
    education,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status LIKE 'worked%') AS worked_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status LIKE 'worked%') AS worked_w,
    100.0 * SUM(w) FILTER (WHERE cws_status LIKE 'worked%') / SUM(w) AS pct_worked_weekly
  FROM base
  GROUP BY 1, 2
  HAVING SUM(w) > 1000000000
  ORDER BY pct_worked_weekly DESC
) TO 'codex_outputs/domestic_hidden_work_female_education.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      Sector,
      "Household Social Group" AS social_group,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND Sex = 'female'
      AND "Principal Activity Status" = 'attended domestic duties only'
  )
  SELECT
    Sector,
    social_group,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status LIKE 'worked%') AS worked_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status LIKE 'worked%') AS worked_w,
    100.0 * SUM(w) FILTER (WHERE cws_status LIKE 'worked%') / SUM(w) AS pct_worked_weekly
  FROM base
  GROUP BY 1, 2
  HAVING SUM(w) > 1000000000
  ORDER BY pct_worked_weekly DESC
) TO 'codex_outputs/domestic_hidden_work_female_social_group.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      "State/UT",
      Sector,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND Sex = 'female'
      AND "Principal Activity Status" = 'attended domestic duties only'
  )
  SELECT
    "State/UT",
    Sector,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status LIKE 'worked%') AS worked_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status LIKE 'worked%') AS worked_w,
    100.0 * SUM(w) FILTER (WHERE cws_status LIKE 'worked%') / SUM(w) AS pct_worked_weekly
  FROM base
  GROUP BY 1, 2
  HAVING COUNT(*) >= 200
  ORDER BY pct_worked_weekly DESC
) TO 'codex_outputs/domestic_hidden_work_female_state.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      "State/UT",
      "District",
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND Sex = 'female'
      AND Sector = 'rural'
      AND "Principal Activity Status" = 'attended domestic duties only'
  )
  SELECT
    "State/UT",
    "District",
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status LIKE 'worked%') AS worked_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status LIKE 'worked%') AS worked_w,
    100.0 * SUM(w) FILTER (WHERE cws_status LIKE 'worked%') / SUM(w) AS pct_worked_weekly
  FROM base
  GROUP BY 1, 2
  HAVING COUNT(*) >= 50
  ORDER BY pct_worked_weekly DESC
) TO 'codex_outputs/domestic_hidden_work_female_rural_district.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      "Principal Enterprise Type" AS enterprise_type,
      "Principal Job Contract Type" AS contract,
      "Principal Job - Paid Leave" AS paid_leave,
      "Principal Job - Social Security" AS social_security,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" = 'worked as regular salaried/wage employee'
      AND "Principal Workers Count" = '20 and above'
  )
  SELECT
    enterprise_type,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE contract = 'no written job contract') AS no_contract_n,
    COUNT(*) FILTER (WHERE contract = 'no written job contract' AND paid_leave = 'yes') AS no_contract_leave_n,
    COUNT(*) FILTER (
      WHERE contract = 'no written job contract'
        AND social_security <> 'not eligible for any of above social security benefits'
    ) AS no_contract_some_social_security_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE contract = 'no written job contract') AS no_contract_w,
    SUM(w) FILTER (WHERE contract = 'no written job contract' AND paid_leave = 'yes') AS no_contract_leave_w,
    SUM(w) FILTER (
      WHERE contract = 'no written job contract'
        AND social_security <> 'not eligible for any of above social security benefits'
    ) AS no_contract_some_social_security_w,
    100.0 * SUM(w) FILTER (WHERE contract = 'no written job contract') / SUM(w) AS pct_no_contract,
    100.0 * SUM(w) FILTER (WHERE contract = 'no written job contract' AND paid_leave = 'yes')
      / SUM(w) FILTER (WHERE contract = 'no written job contract') AS pct_leave_among_no_contract,
    100.0 * SUM(w) FILTER (
      WHERE contract = 'no written job contract'
        AND social_security <> 'not eligible for any of above social security benefits'
    ) / SUM(w) FILTER (WHERE contract = 'no written job contract') AS pct_some_social_security_among_no_contract
  FROM base
  GROUP BY 1
  HAVING SUM(w) > 100000000
  ORDER BY pct_no_contract DESC, total_w DESC
) TO 'codex_outputs/formal_contract_mismatch_large_employers.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      "State/UT",
      "Principal Job Contract Type" AS contract,
      "Principal Job - Paid Leave" AS paid_leave,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" = 'worked as regular salaried/wage employee'
      AND "Principal Enterprise Type" = 'Public/Private limited company'
      AND "Principal Workers Count" = '20 and above'
  )
  SELECT
    "State/UT",
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE contract = 'no written job contract') AS no_contract_n,
    COUNT(*) FILTER (WHERE contract = 'no written job contract' AND paid_leave = 'yes') AS no_contract_leave_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE contract = 'no written job contract') AS no_contract_w,
    SUM(w) FILTER (WHERE contract = 'no written job contract' AND paid_leave = 'yes') AS no_contract_leave_w,
    100.0 * SUM(w) FILTER (WHERE contract = 'no written job contract') / SUM(w) AS pct_no_contract,
    100.0 * SUM(w) FILTER (WHERE contract = 'no written job contract' AND paid_leave = 'yes')
      / SUM(w) FILTER (WHERE contract = 'no written job contract') AS pct_leave_among_no_contract
  FROM base
  GROUP BY 1
  HAVING COUNT(*) >= 100
  ORDER BY pct_no_contract DESC
) TO 'codex_outputs/formal_contract_mismatch_private_ltd_state.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      "Principal Activity Status" AS principal_status,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" LIKE 'worked%'
  )
  SELECT
    principal_status,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) AS weekly_unemployed_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) AS weekly_unemployed_w,
    100.0 * SUM(w) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) / SUM(w) AS pct_weekly_unemployed
  FROM base
  GROUP BY 1
  ORDER BY pct_weekly_unemployed DESC
) TO 'codex_outputs/weekly_unemployment_among_usual_workers.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      Sex,
      Sector,
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" = 'worked as casual wage labour: in other types of work'
  )
  SELECT
    Sex,
    Sector,
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) AS weekly_unemployed_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) AS weekly_unemployed_w,
    100.0 * SUM(w) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) / SUM(w) AS pct_weekly_unemployed
  FROM base
  GROUP BY 1, 2
  ORDER BY pct_weekly_unemployed DESC
) TO 'codex_outputs/weekly_unemployment_casual_other_sex_sector.csv' (HEADER, DELIMITER ',');

COPY (
  WITH base AS (
    SELECT
      "State/UT",
      "CWS Status" AS cws_status,
      "Person Subsample Multiplier" AS w
    FROM plfs
    WHERE Age >= 15
      AND "Principal Activity Status" = 'worked as casual wage labour: in other types of work'
  )
  SELECT
    "State/UT",
    COUNT(*) AS total_n,
    COUNT(*) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) AS weekly_unemployed_n,
    SUM(w) AS total_w,
    SUM(w) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) AS weekly_unemployed_w,
    100.0 * SUM(w) FILTER (WHERE cws_status IN ('sought work', 'did not seek but was available for work')) / SUM(w) AS pct_weekly_unemployed
  FROM base
  GROUP BY 1
  HAVING COUNT(*) >= 100
  ORDER BY pct_weekly_unemployed DESC
) TO 'codex_outputs/weekly_unemployment_casual_other_state.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    COUNT(*) AS households,
    COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') AS substitute_households,
    100.0 * COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') / COUNT(*) AS pct_substitute_households
  FROM households
) TO 'codex_outputs/survey_substitution_overall.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    Sector,
    COUNT(*) AS households,
    COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') AS substitute_households,
    100.0 * COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') / COUNT(*) AS pct_substitute_households
  FROM households
  GROUP BY 1
  ORDER BY pct_substitute_households DESC
) TO 'codex_outputs/survey_substitution_sector.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    "State/UT",
    COUNT(*) AS households,
    COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') AS substitute_households,
    100.0 * COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') / COUNT(*) AS pct_substitute_households
  FROM households
  GROUP BY 1
  ORDER BY pct_substitute_households DESC
) TO 'codex_outputs/survey_substitution_state.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    "State/UT",
    "District",
    COUNT(*) AS households,
    COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') AS substitute_households,
    100.0 * COUNT(*) FILTER (WHERE "Survey Status" = 'substitute household surveyed') / COUNT(*) AS pct_substitute_households
  FROM households
  GROUP BY 1, 2
  HAVING COUNT(*) >= 100
  ORDER BY pct_substitute_households DESC
) TO 'codex_outputs/survey_substitution_district.csv' (HEADER, DELIMITER ',');

COPY (
  SELECT
    "Household Substitution Reason" AS substitution_reason,
    COUNT(*) AS households,
    100.0 * COUNT(*) / SUM(COUNT(*)) OVER () AS pct_of_substitutions
  FROM households
  WHERE "Household Substitution Reason" IS NOT NULL
  GROUP BY 1
  ORDER BY households DESC
) TO 'codex_outputs/survey_substitution_reason.csv' (HEADER, DELIMITER ',');
