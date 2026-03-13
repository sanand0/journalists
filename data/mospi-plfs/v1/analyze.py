#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["duckdb>=1.2.1"]
# ///

from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "plfs.parquet"
V1_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = V1_DIR / "outputs"
WEIGHT_TO_MILLIONS = 1_000_000_000.0


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


def setup_views(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        f"""
        CREATE OR REPLACE VIEW plfs AS
        SELECT *,
          CASE
            WHEN "Age" < 5 THEN '0-4'
            WHEN "Age" < 15 THEN '5-14'
            WHEN "Age" < 25 THEN '15-24'
            WHEN "Age" < 35 THEN '25-34'
            WHEN "Age" < 45 THEN '35-44'
            WHEN "Age" < 60 THEN '45-59'
            ELSE '60+'
          END AS age_band,
          CASE
            WHEN "Age" < 15 THEN 'child'
            WHEN "Age" < 30 THEN 'youth'
            WHEN "Age" < 60 THEN 'working_age'
            ELSE 'senior'
          END AS life_stage,
          COALESCE("Person Subsample Multiplier", 1) AS w,
          COALESCE("Day 1 - Total Hours", 0)
            + COALESCE("Day 2 - Total Hours", 0)
            + COALESCE("Day 3 - Total Hours", 0)
            + COALESCE("Day 4 - Total Hours", 0)
            + COALESCE("Day 5 - Total Hours", 0)
            + COALESCE("Day 6 - Total Hours", 0)
            + COALESCE(TRY_CAST("Day 7 - Total Hours" AS BIGINT), 0) AS week_hours
        FROM read_parquet('{sql_string(DATA_PATH)}')
        f"""
    )


def build_candidate_lifts(con: duckdb.DuckDBPyConnection) -> list[dict[str, object]]:
    dims = [
        "Sex",
        "age_band",
        "life_stage",
        "Marital Status",
        "General Education Level",
        "Technical Education Level",
        "Household Religion",
        "Household Social Group",
        "Household Type",
        "Sector",
    ]
    outcomes = {
        "domestic_only": '"CWS Status" = \'attended domestic duties only\'',
        "domestic_plus": '"CWS Status" LIKE \'attended domestic duties and%\'',
        "sought_work": '"CWS Status" = \'sought work\'',
        "regular_wage": '"CWS Status" = \'worked as regular salaried/wage employee\'',
        "self_employed_own": '"CWS Status" = \'worked in h.h. enterprise (self-employed): own account worker\'',
        "casual_other": '"CWS Status" = \'worked as casual wage labour: in other types of work\'',
        "unpaid_helper": '"CWS Status" = \'worked as helper in h.h. enterprise (unpaid family worker)\'',
        "mgnreg": '"CWS Status" = \'worked as casual wage labour in MGNREG works\'',
        "subsidiary_work": '"Subsidiary Work Engagement" = \'yes\'',
    }

    rows: list[dict[str, object]] = []
    base_rates = {
        outcome: con.execute(
            f"SELECT SUM(w) FILTER (WHERE {expr})::DOUBLE / SUM(w) FROM plfs"
        ).fetchone()[0]
        for outcome, expr in outcomes.items()
    }

    for outcome, expr in outcomes.items():
        base_rate = base_rates[outcome]
        if not base_rate:
            continue

        for group_size in (1, 2):
            for combo in combinations(dims, group_size):
                group_cols = [
                    column if column in {"age_band", "life_stage"} else f'"{column}"'
                    for column in combo
                ]
                group_by = ", ".join(group_cols)
                query = f"""
                    SELECT {group_by},
                           COUNT(*) AS sample_n,
                           SUM(w) AS weighted_n,
                           SUM(w) FILTER (WHERE {expr}) AS weighted_yes,
                           SUM(w) FILTER (WHERE {expr})::DOUBLE / SUM(w) AS rate
                    FROM plfs
                    GROUP BY {group_by}
                    HAVING COUNT(*) >= 250 AND SUM(w) >= 5000000 AND rate IS NOT NULL
                """
                for record in con.execute(query).fetchall():
                    values = record[:group_size]
                    sample_n, weighted_n, weighted_yes, rate = record[group_size:]
                    lift = rate / base_rate
                    if lift < 2 or rate < 0.02:
                        continue
                    rows.append(
                        {
                            "outcome": outcome,
                            "baseline_rate": round(base_rate, 6),
                            "lift": round(lift, 2),
                            "rate": round(rate, 6),
                            "weighted_yes": int(weighted_yes),
                            "weighted_yes_m": round(weighted_yes / WEIGHT_TO_MILLIONS, 3),
                            "weighted_n": int(weighted_n),
                            "weighted_n_m": round(weighted_n / WEIGHT_TO_MILLIONS, 3),
                            "sample_n": sample_n,
                            "group_size": group_size,
                            "group_1": combo[0],
                            "value_1": values[0],
                            "group_2": combo[1] if group_size == 2 else "",
                            "value_2": values[1] if group_size == 2 else "",
                        }
                    )

    rows.sort(
        key=lambda row: (
            row["outcome"],
            -float(row["lift"]),
            -float(row["weighted_yes_m"]),
            -int(row["sample_n"]),
        )
    )
    return rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    setup_views(con)

    export_csv(
        con,
        "quality_summary.csv",
        f"""
        SELECT
          COUNT(*) AS rows,
          COUNT(DISTINCT "Person ID") AS distinct_person_ids,
          SUM(w) AS weight_sum,
          MIN("Survey Date") AS min_survey_date,
          MAX("Survey Date") AS max_survey_date,
          MAX("Age") AS max_age,
          COUNT(*) FILTER (WHERE "Age" >= 100) AS age_100_plus,
          MAX(week_hours) AS max_week_hours,
          COUNT(*) FILTER (WHERE week_hours > 112) AS week_hours_gt_112
        FROM plfs
        """,
    )

    export_csv(
        con,
        "weekly_hour_outliers.csv",
        f"""
        SELECT
          "Person ID",
          "Age",
          "Sex",
          "State/UT",
          "District",
          "CWS Status",
          week_hours,
          "Day 1 - Total Hours" AS day_1_hours,
          "Day 2 - Total Hours" AS day_2_hours,
          "Day 3 - Total Hours" AS day_3_hours,
          "Day 4 - Total Hours" AS day_4_hours,
          "Day 5 - Total Hours" AS day_5_hours,
          "Day 6 - Total Hours" AS day_6_hours,
          TRY_CAST("Day 7 - Total Hours" AS BIGINT) AS day_7_hours
        FROM plfs
        WHERE week_hours > 112
        ORDER BY week_hours DESC, "Person ID"
        """,
    )

    export_csv(
        con,
        "graduate_marriage_cliff.csv",
        f"""
        WITH base AS (
          SELECT
            age_band,
            "Sex" AS sex,
            "Marital Status" AS marital_status,
            SUM(w) AS total_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'attended domestic duties only') AS domestic_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'worked as regular salaried/wage employee') AS regular_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'attended educational institution') AS student_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'sought work') AS search_w
          FROM plfs
          WHERE age_band IN ('15-24', '25-34')
            AND "General Education Level" = 'graduate'
          GROUP BY 1, 2, 3
        )
        SELECT
          age_band,
          sex,
          marital_status,
          ROUND(total_w / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * domestic_w / total_w, 1) AS domestic_pct,
          ROUND(100.0 * regular_w / total_w, 1) AS regular_pct,
          ROUND(100.0 * student_w / total_w, 1) AS student_pct,
          ROUND(100.0 * search_w / total_w, 1) AS search_pct
        FROM base
        ORDER BY age_band, sex, marital_status
        """,
    )

    export_csv(
        con,
        "recent_training_outcomes_by_funding_and_sex.csv",
        f"""
        WITH base AS (
          SELECT
            "Sex" AS sex,
            "Training Funding Source" AS funding_source,
            SUM(w) FILTER (WHERE "Training Completed (Last 365 Days)" = 'yes') AS trained_w,
            SUM(w) FILTER (
              WHERE "Training Completed (Last 365 Days)" = 'yes'
                AND "CWS Status" = 'worked as regular salaried/wage employee'
            ) AS regular_w,
            SUM(w) FILTER (
              WHERE "Training Completed (Last 365 Days)" = 'yes'
                AND "CWS Status" = 'attended domestic duties only'
            ) AS domestic_w,
            SUM(w) FILTER (
              WHERE "Training Completed (Last 365 Days)" = 'yes'
                AND "CWS Status" = 'attended educational institution'
            ) AS student_w,
            SUM(w) FILTER (
              WHERE "Training Completed (Last 365 Days)" = 'yes'
                AND "CWS Status" = 'sought work'
            ) AS search_w
          FROM plfs
          GROUP BY 1, 2
        )
        SELECT
          sex,
          funding_source,
          ROUND(trained_w / {WEIGHT_TO_MILLIONS}, 3) AS trained_m,
          ROUND(100.0 * regular_w / trained_w, 1) AS regular_pct,
          ROUND(100.0 * COALESCE(domestic_w, 0) / trained_w, 1) AS domestic_pct,
          ROUND(100.0 * student_w / trained_w, 1) AS student_pct,
          ROUND(100.0 * search_w / trained_w, 1) AS search_pct
        FROM base
        WHERE trained_w IS NOT NULL
        ORDER BY sex, trained_w DESC
        """,
    )

    export_csv(
        con,
        "female_self_funded_training_by_marital_status.csv",
        f"""
        WITH base AS (
          SELECT
            CASE
              WHEN "Age" < 25 THEN '15-24'
              WHEN "Age" < 35 THEN '25-34'
              ELSE '35+'
            END AS age_band,
            "Marital Status" AS marital_status,
            SUM(w) FILTER (
              WHERE "Sex" = 'female'
                AND "Training Completed (Last 365 Days)" = 'yes'
                AND "Training Funding Source" = 'own funding'
            ) AS trained_w,
            SUM(w) FILTER (
              WHERE "Sex" = 'female'
                AND "Training Completed (Last 365 Days)" = 'yes'
                AND "Training Funding Source" = 'own funding'
                AND "CWS Status" = 'attended domestic duties only'
            ) AS domestic_w,
            SUM(w) FILTER (
              WHERE "Sex" = 'female'
                AND "Training Completed (Last 365 Days)" = 'yes'
                AND "Training Funding Source" = 'own funding'
                AND "CWS Status" = 'worked as regular salaried/wage employee'
            ) AS regular_w,
            SUM(w) FILTER (
              WHERE "Sex" = 'female'
                AND "Training Completed (Last 365 Days)" = 'yes'
                AND "Training Funding Source" = 'own funding'
                AND "CWS Status" = 'attended educational institution'
            ) AS student_w,
            SUM(w) FILTER (
              WHERE "Sex" = 'female'
                AND "Training Completed (Last 365 Days)" = 'yes'
                AND "Training Funding Source" = 'own funding'
                AND "CWS Status" = 'sought work'
            ) AS search_w
          FROM plfs
          WHERE "Age" >= 15
          GROUP BY 1, 2
        )
        SELECT
          age_band,
          marital_status,
          ROUND(trained_w / {WEIGHT_TO_MILLIONS}, 3) AS trained_m,
          ROUND(100.0 * COALESCE(domestic_w, 0) / trained_w, 1) AS domestic_pct,
          ROUND(100.0 * COALESCE(regular_w, 0) / trained_w, 1) AS regular_pct,
          ROUND(100.0 * COALESCE(student_w, 0) / trained_w, 1) AS student_pct,
          ROUND(100.0 * COALESCE(search_w, 0) / trained_w, 1) AS search_pct
        FROM base
        WHERE trained_w IS NOT NULL
        ORDER BY age_band, trained_w DESC
        """,
    )

    export_csv(
        con,
        "domestic_duties_hidden_work.csv",
        f"""
        WITH base AS (
          SELECT
            "Sex" AS sex,
            "Principal Activity Status" AS principal_status,
            SUM(w) AS total_w,
            SUM(w) FILTER (WHERE "Subsidiary Work Engagement" = 'yes') AS subsidiary_w
          FROM plfs
          GROUP BY 1, 2
        )
        SELECT
          sex,
          principal_status,
          ROUND(total_w / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * subsidiary_w / total_w, 1) AS subsidiary_pct
        FROM base
        WHERE principal_status IN (
          'attended domestic duties only',
          'attended educational institution',
          'rentiers, pensioners, remittance recipients, etc.',
          'not able to work due to disability'
        )
        ORDER BY subsidiary_pct DESC, total_m DESC
        """,
    )

    export_csv(
        con,
        "female_domestic_duties_cws_work.csv",
        f"""
        WITH base AS (
          SELECT
            "CWS Status" AS cws_status,
            SUM(w) AS weighted_n
          FROM plfs
          WHERE "Sex" = 'female'
            AND "Principal Activity Status" = 'attended domestic duties only'
          GROUP BY 1
        ),
        totals AS (
          SELECT SUM(weighted_n) AS total_w FROM base
        )
        SELECT
          cws_status,
          ROUND(weighted_n / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(100.0 * weighted_n / total_w, 1) AS pct
        FROM base, totals
        WHERE cws_status LIKE 'worked%'
        ORDER BY weighted_n DESC
        """,
    )

    export_csv(
        con,
        "regular_salaried_benefits_by_enterprise.csv",
        f"""
        WITH base AS (
          SELECT
            "Principal Enterprise Type" AS enterprise_type,
            SUM(w) FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
            ) AS regular_w,
            SUM(w) FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
                AND "Principal Job - Paid Leave" = 'no'
            ) AS no_leave_w,
            SUM(w) FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
                AND "Principal Job - Social Security" = 'not eligible for any of above social security benefits'
            ) AS no_ss_w
          FROM plfs
          GROUP BY 1
        )
        SELECT
          enterprise_type,
          ROUND(regular_w / {WEIGHT_TO_MILLIONS}, 3) AS regular_m,
          ROUND(no_leave_w / {WEIGHT_TO_MILLIONS}, 3) AS no_leave_m,
          ROUND(no_ss_w / {WEIGHT_TO_MILLIONS}, 3) AS no_social_security_m,
          ROUND(100.0 * no_leave_w / regular_w, 1) AS no_leave_pct,
          ROUND(100.0 * no_ss_w / regular_w, 1) AS no_social_security_pct
        FROM base
        WHERE regular_w IS NOT NULL
        ORDER BY regular_w DESC
        """,
    )

    export_csv(
        con,
        "regular_salaried_benefits_by_contract.csv",
        f"""
        WITH base AS (
          SELECT
            "Principal Job Contract Type" AS contract_type,
            SUM(w) AS regular_w,
            SUM(w) FILTER (WHERE "Principal Job - Paid Leave" = 'no') AS no_leave_w,
            SUM(w) FILTER (
              WHERE "Principal Job - Social Security" = 'not eligible for any of above social security benefits'
            ) AS no_ss_w
          FROM plfs
          WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
          GROUP BY 1
        )
        SELECT
          contract_type,
          ROUND(regular_w / {WEIGHT_TO_MILLIONS}, 3) AS regular_m,
          ROUND(100.0 * no_leave_w / regular_w, 1) AS no_leave_pct,
          ROUND(100.0 * no_ss_w / regular_w, 1) AS no_social_security_pct
        FROM base
        ORDER BY regular_w DESC
        """,
    )

    export_csv(
        con,
        "youth_technical_education_outcomes.csv",
        f"""
        WITH base AS (
          SELECT
            "Technical Education Level" AS technical_education,
            SUM(w) AS total_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'sought work') AS search_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'worked as regular salaried/wage employee') AS regular_w,
            SUM(w) FILTER (WHERE "CWS Status" = 'attended educational institution') AS student_w
          FROM plfs
          WHERE "Age" BETWEEN 15 AND 24
            AND "Technical Education Level" IS NOT NULL
          GROUP BY 1
        )
        SELECT
          technical_education,
          ROUND(total_w / {WEIGHT_TO_MILLIONS}, 3) AS total_m,
          ROUND(100.0 * search_w / total_w, 1) AS search_pct,
          ROUND(100.0 * regular_w / total_w, 1) AS regular_pct,
          ROUND(100.0 * student_w / total_w, 1) AS student_pct
        FROM base
        ORDER BY search_pct DESC, total_w DESC
        """,
    )

    write_rows(OUTPUT_DIR / "candidate_lifts.csv", build_candidate_lifts(con))
    print(f"Wrote analysis outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
