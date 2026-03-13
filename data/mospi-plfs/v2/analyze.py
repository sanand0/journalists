#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["duckdb>=1.2.1", "pandas>=2.2", "statsmodels>=0.14"]
# ///

from __future__ import annotations

import csv
from pathlib import Path

import duckdb
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "plfs.parquet"
V2_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = V2_DIR / "outputs"

WEIGHT_TO_MILLIONS = 1_000_000_000.0
MODEL_WEIGHT_SCALE = 1_000_000.0


def sql_string(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def export_csv(con: duckdb.DuckDBPyConnection, filename: str, query: str) -> None:
    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    con.execute(
        f"COPY ({query}) TO '{sql_string(output_path)}' (HEADER, DELIMITER ',')"
    )


def diary_union(activity_numbers: tuple[int, ...]) -> str:
    selects: list[str] = []
    for day_no in range(1, 8):
        for act_no in activity_numbers:
            selects.append(
                f"""
                SELECT
                  "Person ID" AS person_id,
                  "Sex" AS sex,
                  "Age" AS age,
                  "Sector" AS sector,
                  "State/UT" AS state,
                  "District" AS district,
                  "Person Subsample Multiplier" AS w,
                  {day_no} AS day_no,
                  {act_no} AS act_no,
                  "Day {day_no} - Activity {act_no} - Status" AS status,
                  TRY_CAST("Day {day_no} - Activity {act_no} - Hours" AS DOUBLE) AS hours,
                  TRY_CAST("Day {day_no} - Activity {act_no} - Wage" AS DOUBLE) AS wage
                FROM plfs
                """
            )
    return "\nUNION ALL\n".join(selects)


def setup_views(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        f"""
        CREATE OR REPLACE VIEW plfs AS
        SELECT *,
          CASE
            WHEN "General Education Level" IN ('graduate', 'postgraduate and above')
              THEN 'graduate+'
            WHEN "General Education Level" IN ('higher secondary', 'secondary')
              THEN 'secondary_to_hs'
            ELSE 'below_secondary'
          END AS edu_band,
          CASE
            WHEN "Age" BETWEEN 15 AND 24 THEN '15-24'
            WHEN "Age" BETWEEN 25 AND 34 THEN '25-34'
            WHEN "Age" BETWEEN 35 AND 44 THEN '35-44'
            WHEN "Age" BETWEEN 45 AND 59 THEN '45-59'
            WHEN "Age" >= 60 THEN '60+'
          END AS age_band,
          CASE
            WHEN "Principal Activity Status" = 'worked as regular salaried/wage employee'
              THEN 1
            ELSE 0
          END AS is_regular_salaried,
          CASE
            WHEN "Principal Activity Status" = 'worked as regular salaried/wage employee'
              AND "Principal Job Contract Type" IS NOT NULL
              AND "Principal Job Contract Type" != 'no written job contract'
              AND "Principal Job - Paid Leave" = 'yes'
              AND "Principal Job - Social Security" NOT IN (
                'not eligible for any of above social security benefits',
                'not known'
              )
              THEN 1
            ELSE 0
          END AS is_strict_formal,
          CASE
            WHEN "CWS Status" = 'attended domestic duties only' THEN 1
            ELSE 0
          END AS is_domestic_only,
          CASE
            WHEN "CWS Status" = 'worked as regular salaried/wage employee' THEN 1
            ELSE 0
          END AS is_cws_regular_salaried,
          CASE
            WHEN "CWS Status" LIKE 'worked%' THEN 1
            ELSE 0
          END AS is_cws_working
        FROM read_parquet('{sql_string(DATA_PATH)}')
        """
    )

    con.execute(
        f"""
        CREATE OR REPLACE VIEW diary_all AS
        {diary_union((1, 2))}
        """
    )
    con.execute(
        f"""
        CREATE OR REPLACE VIEW diary_primary AS
        {diary_union((1,))}
        """
    )


def export_weighted_models(con: duckdb.DuckDBPyConnection) -> None:
    frame = con.execute(
        """
        SELECT
          CASE WHEN "Marital Status" = 'currently married' THEN 1 ELSE 0 END AS married,
          CASE WHEN "CWS Status" = 'attended domestic duties only' THEN 1 ELSE 0 END AS domestic_only,
          CASE WHEN "CWS Status" = 'worked as regular salaried/wage employee' THEN 1 ELSE 0 END AS regular_salaried,
          "Sector" AS sector,
          edu_band,
          "Household Social Group" AS social_group,
          "Household Type" AS household_type,
          "Household Religion" AS religion,
          "State/UT" AS state,
          "Person Subsample Multiplier" / ? AS model_weight
        FROM plfs
        WHERE "Sex" = 'female'
          AND "Age" BETWEEN 25 AND 34
          AND "Marital Status" IN ('currently married', 'never married')
        """,
        [MODEL_WEIGHT_SCALE],
    ).fetch_df()

    rows: list[dict[str, object]] = []
    for outcome in ("domestic_only", "regular_salaried"):
        model = smf.wls(
            (
                f"{outcome} ~ married + C(sector) + C(edu_band)"
                " + C(social_group) + C(household_type)"
                " + C(religion) + C(state)"
            ),
            data=frame,
            weights=frame["model_weight"],
        ).fit()
        rows.append(
            {
                "outcome": outcome,
                "married_effect": round(model.params["married"], 4),
                "married_effect_points": round(100 * model.params["married"], 2),
                "std_error": round(model.bse["married"], 4),
                "std_error_points": round(100 * model.bse["married"], 2),
                "sample_n": len(frame),
                "weighted_total_m": round(frame["model_weight"].sum() / 1000, 3),
                "controls": (
                    "state + sector + education band + social group"
                    " + household type + religion"
                ),
            }
        )

    write_rows(OUTPUT_DIR / "marriage_weighted_model.csv", rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    setup_views(con)

    export_csv(
        con,
        "dataset_profile.csv",
        f"""
        SELECT
          COUNT(*) AS rows,
          COUNT(DISTINCT "Person ID") AS distinct_person_ids,
          MIN("Survey Date") AS min_survey_date,
          MAX("Survey Date") AS max_survey_date,
          MAX("Age") AS max_age,
          SUM("Person Subsample Multiplier") AS weight_sum,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weight_sum_m
        FROM plfs
        """,
    )

    export_csv(
        con,
        "marriage_gradplus_state_compare.csv",
        f"""
        WITH cells AS (
          SELECT
            "State/UT" AS state,
            "Marital Status" AS marital_status,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            AVG(is_domestic_only) AS domestic_rate,
            AVG(is_cws_regular_salaried) AS salaried_rate
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Age" BETWEEN 25 AND 34
            AND edu_band = 'graduate+'
            AND "Marital Status" IN ('currently married', 'never married')
          GROUP BY 1, 2
        ),
        paired AS (
          SELECT
            married.state,
            married.n AS married_n,
            never.n AS never_married_n,
            ROUND(married.weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS married_m,
            ROUND(never.weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS never_married_m,
            ROUND(100.0 * married.domestic_rate, 1) AS domestic_married_pct,
            ROUND(100.0 * never.domestic_rate, 1) AS domestic_never_married_pct,
            ROUND(100.0 * married.salaried_rate, 1) AS salaried_married_pct,
            ROUND(100.0 * never.salaried_rate, 1) AS salaried_never_married_pct,
            ROUND(100.0 * (married.domestic_rate - never.domestic_rate), 1) AS domestic_gap_pts,
            ROUND(100.0 * (married.salaried_rate - never.salaried_rate), 1) AS salaried_gap_pts
          FROM cells married
          JOIN cells never USING (state)
          WHERE married.marital_status = 'currently married'
            AND never.marital_status = 'never married'
            AND married.n >= 50
            AND never.n >= 50
        )
        SELECT *
        FROM paired
        ORDER BY domestic_gap_pts DESC, married_n DESC
        """,
    )

    export_csv(
        con,
        "marriage_control_cells_household_type.csv",
        """
        WITH cells AS (
          SELECT
            "Sector" AS sector,
            edu_band,
            "Household Type" AS household_type,
            "Marital Status" AS marital_status,
            COUNT(*) AS n,
            AVG(is_domestic_only) AS domestic_rate,
            AVG(is_cws_regular_salaried) AS salaried_rate
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Age" BETWEEN 25 AND 34
            AND "Marital Status" IN ('currently married', 'never married')
          GROUP BY 1, 2, 3, 4
        ),
        paired AS (
          SELECT
            married.sector,
            married.edu_band,
            married.household_type,
            married.n AS married_n,
            never.n AS never_married_n,
            ROUND(100.0 * married.domestic_rate, 1) AS domestic_married_pct,
            ROUND(100.0 * never.domestic_rate, 1) AS domestic_never_married_pct,
            ROUND(100.0 * married.salaried_rate, 1) AS salaried_married_pct,
            ROUND(100.0 * never.salaried_rate, 1) AS salaried_never_married_pct,
            ROUND(100.0 * (married.domestic_rate - never.domestic_rate), 1) AS domestic_gap_pts,
            ROUND(100.0 * (married.salaried_rate - never.salaried_rate), 1) AS salaried_gap_pts
          FROM cells married
          JOIN cells never
            ON married.sector = never.sector
           AND married.edu_band = never.edu_band
           AND married.household_type = never.household_type
          WHERE married.marital_status = 'currently married'
            AND never.marital_status = 'never married'
            AND married.n >= 100
            AND never.n >= 100
        )
        SELECT *
        FROM paired
        ORDER BY domestic_gap_pts DESC, married_n DESC
        """,
    )

    export_csv(
        con,
        "marriage_control_cells_social_group.csv",
        """
        WITH cells AS (
          SELECT
            "Sector" AS sector,
            edu_band,
            "Household Social Group" AS social_group,
            "Marital Status" AS marital_status,
            COUNT(*) AS n,
            AVG(is_domestic_only) AS domestic_rate,
            AVG(is_cws_regular_salaried) AS salaried_rate
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Age" BETWEEN 25 AND 34
            AND "Marital Status" IN ('currently married', 'never married')
          GROUP BY 1, 2, 3, 4
        ),
        paired AS (
          SELECT
            married.sector,
            married.edu_band,
            married.social_group,
            married.n AS married_n,
            never.n AS never_married_n,
            ROUND(100.0 * married.domestic_rate, 1) AS domestic_married_pct,
            ROUND(100.0 * never.domestic_rate, 1) AS domestic_never_married_pct,
            ROUND(100.0 * married.salaried_rate, 1) AS salaried_married_pct,
            ROUND(100.0 * never.salaried_rate, 1) AS salaried_never_married_pct,
            ROUND(100.0 * (married.domestic_rate - never.domestic_rate), 1) AS domestic_gap_pts,
            ROUND(100.0 * (married.salaried_rate - never.salaried_rate), 1) AS salaried_gap_pts
          FROM cells married
          JOIN cells never
            ON married.sector = never.sector
           AND married.edu_band = never.edu_band
           AND married.social_group = never.social_group
          WHERE married.marital_status = 'currently married'
            AND never.marital_status = 'never married'
            AND married.n >= 100
            AND never.n >= 100
        )
        SELECT *
        FROM paired
        ORDER BY domestic_gap_pts DESC, married_n DESC
        """,
    )
    export_weighted_models(con)

    export_csv(
        con,
        "hidden_work_rural_urban.csv",
        f"""
        WITH base AS (
          SELECT
            "Sector" AS sector,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE is_cws_working = 1) AS working_n,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_cws_working = 1) AS working_weight
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1
        )
        SELECT
          sector,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          working_n,
          ROUND(working_weight / {WEIGHT_TO_MILLIONS}, 3) AS working_m,
          ROUND(100.0 * working_n / n, 1) AS raw_working_pct,
          ROUND(100.0 * working_weight / weighted_n, 1) AS weighted_working_pct
        FROM base
        ORDER BY weighted_working_pct DESC
        """,
    )

    export_csv(
        con,
        "hidden_work_rural_female_age_education.csv",
        f"""
        WITH base AS (
          SELECT
            CASE
              WHEN "Age" BETWEEN 15 AND 24 THEN '15-24'
              WHEN "Age" BETWEEN 25 AND 44 THEN '25-44'
              WHEN "Age" BETWEEN 45 AND 59 THEN '45-59'
              WHEN "Age" >= 60 THEN '60+'
            END AS age_band,
            "General Education Level" AS education,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE is_cws_working = 1) AS working_n,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_cws_working = 1) AS working_weight
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Sector" = 'rural'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1, 2
        )
        SELECT
          age_band,
          education,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          working_n,
          ROUND(working_weight / {WEIGHT_TO_MILLIONS}, 3) AS working_m,
          ROUND(100.0 * working_n / n, 1) AS raw_working_pct,
          ROUND(100.0 * working_weight / weighted_n, 1) AS weighted_working_pct
        FROM base
        WHERE n >= 100
        ORDER BY weighted_working_pct DESC, n DESC
        """,
    )

    export_csv(
        con,
        "hidden_work_rural_female_state.csv",
        f"""
        WITH base AS (
          SELECT
            "State/UT" AS state,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE is_cws_working = 1) AS working_n,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_cws_working = 1) AS working_weight
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Sector" = 'rural'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1
        )
        SELECT
          state,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * working_n / n, 1) AS raw_working_pct,
          ROUND(100.0 * working_weight / weighted_n, 1) AS weighted_working_pct
        FROM base
        WHERE n >= 300
        ORDER BY weighted_working_pct DESC, n DESC
        """,
    )

    export_csv(
        con,
        "hidden_work_rural_female_social_group.csv",
        f"""
        WITH base AS (
          SELECT
            "Household Social Group" AS social_group,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE is_cws_working = 1) AS working_n,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_cws_working = 1) AS working_weight
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Sector" = 'rural'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1
        )
        SELECT
          social_group,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * working_n / n, 1) AS raw_working_pct,
          ROUND(100.0 * working_weight / weighted_n, 1) AS weighted_working_pct
        FROM base
        WHERE n >= 200
        ORDER BY weighted_working_pct DESC, n DESC
        """,
    )

    export_csv(
        con,
        "hidden_work_rural_female_household_type.csv",
        f"""
        WITH base AS (
          SELECT
            "Household Type" AS household_type,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE is_cws_working = 1) AS working_n,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_cws_working = 1) AS working_weight
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Sector" = 'rural'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1
        )
        SELECT
          household_type,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * working_n / n, 1) AS raw_working_pct,
          ROUND(100.0 * working_weight / weighted_n, 1) AS weighted_working_pct
        FROM base
        WHERE n >= 200
        ORDER BY weighted_working_pct DESC, n DESC
        """,
    )

    export_csv(
        con,
        "hidden_work_rural_female_district.csv",
        f"""
        WITH base AS (
          SELECT
            "State/UT" AS state,
            "District" AS district,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE is_cws_working = 1) AS working_n,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_cws_working = 1) AS working_weight
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Sector" = 'rural'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1, 2
        )
        SELECT
          state,
          district,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * working_n / n, 1) AS raw_working_pct,
          ROUND(100.0 * working_weight / weighted_n, 1) AS weighted_working_pct
        FROM base
        WHERE n >= 100
        ORDER BY weighted_working_pct DESC, n DESC
        LIMIT 100
        """,
    )

    export_csv(
        con,
        "strict_formality_overall.csv",
        f"""
        WITH base AS (
          SELECT
            "Sex" AS sex,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1) AS regular_weight,
            SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1) AS strict_formal_weight
          FROM plfs
          GROUP BY 1
        )
        SELECT
          sex,
          ROUND(regular_weight / {WEIGHT_TO_MILLIONS}, 3) AS regular_m,
          ROUND(strict_formal_weight / {WEIGHT_TO_MILLIONS}, 3) AS strict_formal_m,
          ROUND(100.0 * strict_formal_weight / regular_weight, 1) AS strict_formal_share_pct
        FROM base
        UNION ALL
        SELECT
          'all' AS sex,
          ROUND(
            SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1)
            / {WEIGHT_TO_MILLIONS},
            3
          ) AS regular_m,
          ROUND(
            SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / {WEIGHT_TO_MILLIONS},
            3
          ) AS strict_formal_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1),
            1
          ) AS strict_formal_share_pct
        FROM plfs
        """,
    )

    export_csv(
        con,
        "strict_formality_benchmark.csv",
        f"""
        WITH base AS (
          SELECT
            COALESCE("Sex", 'all') AS sex,
            "Person Subsample Multiplier" AS w,
            is_regular_salaried,
            is_strict_formal,
            "Principal Job Contract Type" AS contract_type,
            "Principal Job - Paid Leave" AS paid_leave,
            "Principal Job - Social Security" AS social_security,
            "CWS Earnings (Salaried)" AS cws_earnings
          FROM plfs
        ),
        rows_by_sex AS (
          SELECT
            sex,
            ROUND(SUM(w) FILTER (WHERE is_regular_salaried = 1) / {WEIGHT_TO_MILLIONS}, 3) AS regular_m,
            ROUND(
              100.0
              * SUM(w) FILTER (
                  WHERE is_regular_salaried = 1
                    AND contract_type IS NOT NULL
                    AND contract_type != 'no written job contract'
                )
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS written_contract_pct,
            ROUND(
              100.0
              * SUM(w) FILTER (
                  WHERE is_regular_salaried = 1
                    AND paid_leave = 'yes'
                )
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS paid_leave_pct,
            ROUND(
              100.0
              * SUM(w) FILTER (
                  WHERE is_regular_salaried = 1
                    AND social_security NOT IN (
                      'not eligible for any of above social security benefits',
                      'not known'
                    )
                )
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS any_social_security_pct,
            ROUND(
              100.0
              * SUM(w) FILTER (WHERE is_strict_formal = 1)
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS strict_formal_pct,
            ROUND(quantile_cont(cws_earnings, 0.5) FILTER (WHERE is_strict_formal = 1), 1) AS median_monthly_earnings_strict_formal,
            ROUND(
              quantile_cont(cws_earnings, 0.5)
                FILTER (WHERE is_regular_salaried = 1 AND is_strict_formal = 0),
              1
            ) AS median_monthly_earnings_other_regular
          FROM base
          GROUP BY 1
        ),
        total_row AS (
          SELECT
            'all' AS sex,
            ROUND(SUM(w) FILTER (WHERE is_regular_salaried = 1) / {WEIGHT_TO_MILLIONS}, 3) AS regular_m,
            ROUND(
              100.0
              * SUM(w) FILTER (
                  WHERE is_regular_salaried = 1
                    AND contract_type IS NOT NULL
                    AND contract_type != 'no written job contract'
                )
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS written_contract_pct,
            ROUND(
              100.0
              * SUM(w) FILTER (
                  WHERE is_regular_salaried = 1
                    AND paid_leave = 'yes'
                )
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS paid_leave_pct,
            ROUND(
              100.0
              * SUM(w) FILTER (
                  WHERE is_regular_salaried = 1
                    AND social_security NOT IN (
                      'not eligible for any of above social security benefits',
                      'not known'
                    )
                )
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS any_social_security_pct,
            ROUND(
              100.0
              * SUM(w) FILTER (WHERE is_strict_formal = 1)
              / SUM(w) FILTER (WHERE is_regular_salaried = 1),
              1
            ) AS strict_formal_pct,
            ROUND(quantile_cont(cws_earnings, 0.5) FILTER (WHERE is_strict_formal = 1), 1) AS median_monthly_earnings_strict_formal,
            ROUND(
              quantile_cont(cws_earnings, 0.5)
                FILTER (WHERE is_regular_salaried = 1 AND is_strict_formal = 0),
              1
            ) AS median_monthly_earnings_other_regular
          FROM base
        )
        SELECT *
        FROM (
          SELECT * FROM rows_by_sex
          UNION ALL
          SELECT * FROM total_row
        ) combined
        ORDER BY CASE sex WHEN 'male' THEN 1 WHEN 'female' THEN 2 WHEN 'transgender' THEN 3 ELSE 4 END
        """,
    )

    export_csv(
        con,
        "strict_formality_by_workers_count.csv",
        f"""
        SELECT
          "Sex" AS sex,
          "Sector" AS sector,
          "Principal Workers Count" AS workers_count,
          ROUND(
            SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1)
            / {WEIGHT_TO_MILLIONS},
            3
          ) AS regular_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1),
            1
          ) AS strict_formal_share_pct
        FROM plfs
        GROUP BY 1, 2, 3
        HAVING regular_m IS NOT NULL
        ORDER BY sex, sector, regular_m DESC
        """,
    )

    export_csv(
        con,
        "strict_formality_by_enterprise.csv",
        f"""
        SELECT
          "Principal Enterprise Type" AS enterprise_type,
          ROUND(
            SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1)
            / {WEIGHT_TO_MILLIONS},
            3
          ) AS regular_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1),
            1
          ) AS strict_formal_share_pct
        FROM plfs
        GROUP BY 1
        HAVING regular_m IS NOT NULL
        ORDER BY regular_m DESC
        """,
    )

    export_csv(
        con,
        "strict_formality_by_workplace.csv",
        f"""
        SELECT
          "Principal Workplace Location" AS workplace,
          ROUND(
            SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1)
            / {WEIGHT_TO_MILLIONS},
            3
          ) AS regular_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1),
            1
          ) AS strict_formal_share_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier")
              FILTER (
                WHERE is_regular_salaried = 1
                  AND "Principal Job Contract Type" = 'no written job contract'
              )
            / SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1),
            1
          ) AS no_contract_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier")
              FILTER (
                WHERE is_regular_salaried = 1
                  AND "Principal Job - Social Security"
                    = 'not eligible for any of above social security benefits'
              )
            / SUM("Person Subsample Multiplier") FILTER (WHERE is_regular_salaried = 1),
            1
          ) AS no_social_security_pct
        FROM plfs
        GROUP BY 1
        HAVING regular_m >= 1
        ORDER BY strict_formal_share_pct ASC, regular_m DESC
        """,
    )

    export_csv(
        con,
        "strict_formality_nonformal_concentration.csv",
        f"""
        WITH base AS (
          SELECT
            "Principal Enterprise Type" AS enterprise_type,
            SUM("Person Subsample Multiplier")
              FILTER (WHERE is_regular_salaried = 1 AND is_strict_formal = 0) AS nonformal_regular_weight
          FROM plfs
          GROUP BY 1
        ),
        totals AS (
          SELECT SUM(nonformal_regular_weight) AS total_nonformal_regular_weight
          FROM base
        )
        SELECT
          enterprise_type,
          ROUND(nonformal_regular_weight / {WEIGHT_TO_MILLIONS}, 3) AS nonformal_regular_m,
          ROUND(
            100.0 * nonformal_regular_weight / total_nonformal_regular_weight,
            1
          ) AS share_of_nonformal_regular_pct
        FROM base
        CROSS JOIN totals
        WHERE nonformal_regular_weight IS NOT NULL
        ORDER BY share_of_nonformal_regular_pct DESC, nonformal_regular_m DESC
        """,
    )

    export_csv(
        con,
        "graduate_microfirm_penalty.csv",
        """
        SELECT
          "Sex" AS sex,
          "Sector" AS sector,
          "Principal Workers Count" AS workers_count,
          COUNT(*) AS n,
          ROUND(SUM("Person Subsample Multiplier") / 1000000000.0, 3) AS weighted_m,
          ROUND(
            quantile_cont("CWS Earnings (Salaried)", 0.5)
              FILTER (WHERE "CWS Earnings (Salaried)" IS NOT NULL),
            1
          ) AS median_monthly_earnings,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier")
              FILTER (
                WHERE "Principal Job - Social Security"
                  = 'not eligible for any of above social security benefits'
              )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS no_social_security_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier")
              FILTER (WHERE "Principal Job Contract Type" = 'no written job contract')
            / SUM("Person Subsample Multiplier"),
            1
          ) AS no_contract_pct
        FROM plfs
        WHERE is_regular_salaried = 1
          AND edu_band = 'graduate+'
          AND "CWS Earnings (Salaried)" IS NOT NULL
        GROUP BY 1, 2, 3
        HAVING n >= 100
        ORDER BY sex, sector, weighted_m DESC
        """,
    )

    export_csv(
        con,
        "student_subwork_benchmark.csv",
        f"""
        WITH base AS (
          SELECT *
          FROM plfs
          WHERE "Age" BETWEEN 18 AND 24
            AND "CWS Status" = 'attended educational institution'
        ),
        groups AS (
          SELECT
            'all_students_18_24' AS group_name,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subwork_n,
            SUM("Person Subsample Multiplier")
              FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subwork_weight
          FROM base
          UNION ALL
          SELECT
            'rural_farm_household_students_18_24' AS group_name,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subwork_n,
            SUM("Person Subsample Multiplier")
              FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subwork_weight
          FROM base
          WHERE "Sector" = 'rural'
            AND "Household Type" = 'self-employed in agriculture'
          UNION ALL
          SELECT
            'other_students_18_24' AS group_name,
            COUNT(*) AS n,
            SUM("Person Subsample Multiplier") AS weighted_n,
            COUNT(*) FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subwork_n,
            SUM("Person Subsample Multiplier")
              FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subwork_weight
          FROM base
          WHERE NOT (
            "Sector" = 'rural'
            AND "Household Type" = 'self-employed in agriculture'
          )
        )
        SELECT
          group_name,
          n,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * subwork_n / n, 1) AS raw_subwork_pct,
          ROUND(100.0 * subwork_weight / weighted_n, 1) AS weighted_subwork_pct
        FROM groups
        ORDER BY
          CASE group_name
            WHEN 'all_students_18_24' THEN 1
            WHEN 'other_students_18_24' THEN 2
            WHEN 'rural_farm_household_students_18_24' THEN 3
            ELSE 4
          END
        """,
    )

    export_csv(
        con,
        "student_subwork_farmhousehold_breakdown.csv",
        f"""
        SELECT
          "Sex" AS sex,
          "Household Social Group" AS social_group,
          COUNT(*) AS n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(
            100.0
            * COUNT(*) FILTER (WHERE "Subsidiary Work Engagement" = 'yes')
            / COUNT(*),
            1
          ) AS raw_subwork_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier")
              FILTER (WHERE "Subsidiary Work Engagement" = 'yes')
            / SUM("Person Subsample Multiplier"),
            1
          ) AS weighted_subwork_pct
        FROM plfs
        WHERE "Age" BETWEEN 18 AND 24
          AND "CWS Status" = 'attended educational institution'
          AND "Sector" = 'rural'
          AND "Household Type" = 'self-employed in agriculture'
        GROUP BY 1, 2
        HAVING n >= 150
        ORDER BY weighted_subwork_pct DESC, n DESC
        """,
    )

    export_csv(
        con,
        "school_exit_reasons_youth.csv",
        f"""
        WITH dropouts AS (
          SELECT
            "Sex" AS sex,
            CASE
              WHEN "Age" BETWEEN 15 AND 17 THEN '15-17'
              WHEN "Age" BETWEEN 18 AND 24 THEN '18-24'
            END AS age_band,
            "Marital Status" AS marital_status,
            "Current Attendance Status" AS attendance_status,
            "Person Subsample Multiplier" AS w
          FROM plfs
          WHERE "Age" BETWEEN 15 AND 24
            AND "Current Attendance Status" LIKE 'attended but currently not attending%'
        )
        SELECT
          sex,
          age_band,
          marital_status,
          COUNT(*) AS n,
          ROUND(SUM(w) / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(
            100.0
            * COUNT(*) FILTER (
              WHERE attendance_status
                = 'attended but currently not attending - to attend domestic chores'
            )
            / COUNT(*),
            1
          ) AS raw_domestic_chore_pct,
          ROUND(
            100.0
            * SUM(w) FILTER (
              WHERE attendance_status
                = 'attended but currently not attending - to attend domestic chores'
            )
            / SUM(w),
            1
          ) AS weighted_domestic_chore_pct,
          ROUND(
            100.0
            * SUM(w) FILTER (
              WHERE attendance_status
                = 'attended but currently not attending - to supplement household income'
            )
            / SUM(w),
            1
          ) AS weighted_income_pct
        FROM dropouts
        GROUP BY 1, 2, 3
        HAVING n >= 200
        ORDER BY weighted_domestic_chore_pct DESC, n DESC
        """,
    )

    export_csv(
        con,
        "casual_pay_rural_gender_benchmarks.csv",
        f"""
        WITH spells AS (
          SELECT
            sex,
            status,
            w,
            wage,
            wage / hours AS hourly
          FROM diary_primary
          WHERE sector = 'rural'
            AND status IN (
              'worked as casual wage labour: in other types of work',
              'worked as casual wage labour in MGNREG works',
              'worked as casual wage labour in public works other than MGNREG works'
            )
            AND hours > 0
            AND wage > 0
        ),
        weighted AS (
          SELECT
            *,
            SUM(w) OVER (
              PARTITION BY sex, status
              ORDER BY hourly, wage, w
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS hourly_cum_w,
            SUM(w) OVER (
              PARTITION BY sex, status
              ORDER BY wage, hourly, w
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS wage_cum_w,
            SUM(w) OVER (PARTITION BY sex, status) AS total_w
          FROM spells
        ),
        medians AS (
          SELECT
            sex,
            status,
            MIN(hourly) FILTER (WHERE hourly_cum_w >= total_w / 2) AS weighted_median_hourly,
            MIN(wage) FILTER (WHERE wage_cum_w >= total_w / 2) AS weighted_median_daily_wage
          FROM weighted
          GROUP BY 1, 2
        )
        SELECT
          female.status,
          ROUND(female.weighted_median_daily_wage, 2) AS female_weighted_median_daily_wage,
          ROUND(male.weighted_median_daily_wage, 2) AS male_weighted_median_daily_wage,
          ROUND(100.0 * female.weighted_median_daily_wage / male.weighted_median_daily_wage, 1) AS female_daily_as_pct_of_male,
          ROUND(female.weighted_median_hourly, 2) AS female_weighted_median_hourly,
          ROUND(male.weighted_median_hourly, 2) AS male_weighted_median_hourly,
          ROUND(100.0 * female.weighted_median_hourly / male.weighted_median_hourly, 1) AS female_hourly_as_pct_of_male
        FROM medians female
        JOIN medians male USING (status)
        WHERE female.sex = 'female'
          AND male.sex = 'male'
        ORDER BY female_daily_as_pct_of_male DESC, female.status
        """,
    )

    export_csv(
        con,
        "casual_diary_pay_quality.csv",
        """
        SELECT
          status,
          COUNT(*) AS activity_rows,
          COUNT(*) FILTER (WHERE hours > 0 AND wage > 0) AS positive_pay_rows,
          MIN(hours) FILTER (WHERE hours IS NOT NULL) AS min_hours,
          MAX(hours) FILTER (WHERE hours IS NOT NULL) AS max_hours,
          MIN(wage) FILTER (WHERE wage IS NOT NULL) AS min_wage,
          MAX(wage) FILTER (WHERE wage IS NOT NULL) AS max_wage
        FROM diary_all
        WHERE status IN (
          'worked as casual wage labour: in other types of work',
          'worked as casual wage labour in MGNREG works',
          'worked as casual wage labour in public works other than MGNREG works'
        )
        GROUP BY 1
        ORDER BY activity_rows DESC
        """,
    )

    export_csv(
        con,
        "casual_diary_pay_primary_activity.csv",
        f"""
        WITH spells AS (
          SELECT
            sex,
            sector,
            status,
            w,
            hours,
            wage,
            wage / hours AS hourly
          FROM diary_primary
          WHERE status IN (
            'worked as casual wage labour: in other types of work',
            'worked as casual wage labour in MGNREG works',
            'worked as casual wage labour in public works other than MGNREG works'
          )
            AND hours > 0
            AND wage > 0
        ),
        weighted AS (
          SELECT
            *,
            SUM(w) OVER (
              PARTITION BY sex, sector, status
              ORDER BY hourly, wage, hours, w
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cum_w,
            SUM(w) OVER (PARTITION BY sex, sector, status) AS total_w
          FROM spells
        )
        SELECT
          sex,
          sector,
          status,
          COUNT(*) AS positive_rows,
          ROUND(MAX(total_w) / {WEIGHT_TO_MILLIONS}, 3) AS weighted_rows_m,
          ROUND(AVG(hours), 2) AS avg_hours,
          ROUND(AVG(wage), 2) AS avg_daily_wage,
          ROUND(AVG(hourly), 2) AS avg_hourly_wage,
          ROUND(quantile_cont(hourly, 0.5), 2) AS median_hourly_unweighted,
          ROUND(MIN(hourly) FILTER (WHERE cum_w >= total_w / 2), 2) AS weighted_median_hourly
        FROM weighted
        GROUP BY 1, 2, 3
        ORDER BY weighted_rows_m DESC
        """,
    )

    export_csv(
        con,
        "casual_diary_pay_all_activities.csv",
        f"""
        WITH spells AS (
          SELECT
            sex,
            sector,
            status,
            w,
            hours,
            wage,
            wage / hours AS hourly
          FROM diary_all
          WHERE status IN (
            'worked as casual wage labour: in other types of work',
            'worked as casual wage labour in MGNREG works',
            'worked as casual wage labour in public works other than MGNREG works'
          )
            AND hours > 0
            AND wage > 0
        ),
        weighted AS (
          SELECT
            *,
            SUM(w) OVER (
              PARTITION BY sex, sector, status
              ORDER BY hourly, wage, hours, w
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cum_w,
            SUM(w) OVER (PARTITION BY sex, sector, status) AS total_w
          FROM spells
        )
        SELECT
          sex,
          sector,
          status,
          COUNT(*) AS positive_rows,
          ROUND(MAX(total_w) / {WEIGHT_TO_MILLIONS}, 3) AS weighted_rows_m,
          ROUND(AVG(hours), 2) AS avg_hours,
          ROUND(AVG(wage), 2) AS avg_daily_wage,
          ROUND(AVG(hourly), 2) AS avg_hourly_wage,
          ROUND(quantile_cont(hourly, 0.5), 2) AS median_hourly_unweighted,
          ROUND(MIN(hourly) FILTER (WHERE cum_w >= total_w / 2), 2) AS weighted_median_hourly
        FROM weighted
        GROUP BY 1, 2, 3
        ORDER BY weighted_rows_m DESC
        """,
    )

    print(f"Wrote analysis outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
