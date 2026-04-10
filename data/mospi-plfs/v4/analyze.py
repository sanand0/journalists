#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["duckdb>=1.2.1", "pandas>=2.2", "statsmodels>=0.14"]
# ///

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path

import duckdb
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "plfs.parquet"
V3_DIR = ROOT / "v3"
V4_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = V4_DIR / "outputs"
V3_OUTPUT_DIR = V3_DIR / "outputs"

WEIGHT_TO_MILLIONS = 1_000_000_000.0
MODEL_WEIGHT_SCALE = 1_000_000.0
HOUSEHOLD_KEY_SQL = """
CONCAT_WS(
  '|',
  CAST("Sector" AS VARCHAR),
  CAST("Stratum" AS VARCHAR),
  CAST("Sub-Stratum" AS VARCHAR),
  CAST("Sub-Sample" AS VARCHAR),
  CAST("First Stage Unit (FSU)" AS VARCHAR),
  CAST("Sample Segment/Sub-Block Number" AS VARCHAR),
  CAST("Second Stage Stratum Number" AS VARCHAR),
  CAST("Household Number" AS VARCHAR)
)
""".strip()
SELECTED_PROFESSIONS = (
    "Primary School and Early Childhood Teachers",
    "Secondary Education Teachers",
    "Other Teaching Professionals",
    "Nursing and Midwifery Associate Professionals",
    "Medical Doctors",
    "Software and Application Developers and Analysts",
)
FOCUS_CREDENTIALS = (
    "technical degree in engineering/technology",
    "diploma or certificate (below graduate level) in engineering/technology",
    "technical degree in medicine",
    "diploma or certificate (below graduate level) in medicine",
)


def sql_string(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def quote_values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value.replace("'", "''")}'" for value in values)


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


def seed_v3_outputs() -> None:
    subprocess.run([str(V3_DIR / "analyze.py")], cwd=ROOT, check=True)
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    shutil.copytree(V3_OUTPUT_DIR, OUTPUT_DIR)


def setup_views(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        f"""
        CREATE OR REPLACE VIEW plfs AS
        SELECT *,
          {HOUSEHOLD_KEY_SQL} AS hhid,
          CASE
            WHEN "General Education Level" IN ('graduate', 'postgraduate and above')
              THEN 'graduate+'
            WHEN "General Education Level" IN ('higher secondary', 'secondary')
              THEN 'secondary_to_hs'
            ELSE 'below_secondary'
          END AS edu_band,
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
          END AS is_cws_regular_salaried
        FROM read_parquet('{sql_string(DATA_PATH)}')
        """
    )

    con.execute(
        """
        CREATE OR REPLACE VIEW households AS
        SELECT
          hhid,
          MAX(CASE WHEN "Age" BETWEEN 0 AND 5 THEN 1 ELSE 0 END) AS has_child_0_5
        FROM plfs
        GROUP BY 1
        """
    )

    con.execute(
        """
        CREATE OR REPLACE VIEW hidden_domestic AS
        SELECT
          "State/UT" AS state,
          "District" AS district,
          "Sector" AS sector,
          "Household Type" AS household_type,
          "Household Social Group" AS social_group,
          "Person Subsample Multiplier" AS w,
          CASE WHEN "CWS Status" LIKE 'worked%' THEN 1 ELSE 0 END AS worked_week
        FROM plfs
        WHERE "Sex" = 'female'
          AND "Principal Activity Status" = 'attended domestic duties only'
        """
    )


def export_household_role_tables(con: duckdb.DuckDBPyConnection) -> None:
    export_csv(
        con,
        "married_graduate_household_role_detail.csv",
        f"""
        SELECT
          CASE
            WHEN p."Relationship to Head" IN ('spouse of head', 'spouse of married child')
              THEN 'wife_role_in_extended_household'
            WHEN p."Relationship to Head" IN ('self', 'married child')
              THEN 'self_or_child_role'
            ELSE 'other_role'
          END AS role_group,
          p."Relationship to Head" AS relationship_to_head,
          COUNT(*) AS sample_n,
          ROUND(SUM(p."Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE hh.has_child_0_5 = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS child_u5_pct,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE p.is_domestic_only = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS domestic_only_pct,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE p.is_cws_regular_salaried = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS regular_salaried_pct
        FROM plfs p
        JOIN households hh USING (hhid)
        WHERE p."Sex" = 'female'
          AND p."Age" BETWEEN 25 AND 34
          AND p.edu_band = 'graduate+'
          AND p."Marital Status" = 'currently married'
        GROUP BY 1, 2
        HAVING COUNT(*) >= 100
        ORDER BY domestic_only_pct DESC, weighted_m DESC
        """,
    )

    export_csv(
        con,
        "married_graduate_household_role_grouped.csv",
        f"""
        SELECT
          CASE
            WHEN p."Relationship to Head" IN ('spouse of head', 'spouse of married child')
              THEN 'wife_role_in_extended_household'
            WHEN p."Relationship to Head" IN ('self', 'married child')
              THEN 'self_or_child_role'
            ELSE 'other_role'
          END AS role_group,
          COUNT(*) AS sample_n,
          ROUND(SUM(p."Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE hh.has_child_0_5 = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS child_u5_pct,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE p.is_domestic_only = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS domestic_only_pct,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE p.is_cws_regular_salaried = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS regular_salaried_pct
        FROM plfs p
        JOIN households hh USING (hhid)
        WHERE p."Sex" = 'female'
          AND p."Age" BETWEEN 25 AND 34
          AND p.edu_band = 'graduate+'
          AND p."Marital Status" = 'currently married'
          AND p."Relationship to Head" IN (
            'spouse of head',
            'spouse of married child',
            'self',
            'married child'
          )
        GROUP BY 1
        ORDER BY domestic_only_pct DESC
        """,
    )

    export_csv(
        con,
        "married_graduate_household_role_gender_compare.csv",
        f"""
        SELECT
          p."Sex" AS sex,
          p."Relationship to Head" AS relationship_to_head,
          COUNT(*) AS sample_n,
          ROUND(SUM(p."Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE p.is_domestic_only = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS domestic_only_pct,
          ROUND(
            100.0
            * SUM(p."Person Subsample Multiplier") FILTER (WHERE p.is_cws_regular_salaried = 1)
            / SUM(p."Person Subsample Multiplier"),
            1
          ) AS regular_salaried_pct
        FROM plfs p
        WHERE p."Sex" IN ('female', 'male')
          AND p."Age" BETWEEN 25 AND 34
          AND p.edu_band = 'graduate+'
          AND p."Marital Status" = 'currently married'
          AND p."Relationship to Head" IN (
            'spouse of head',
            'spouse of married child',
            'self',
            'married child'
          )
        GROUP BY 1, 2
        HAVING COUNT(*) >= 100
        ORDER BY sex, domestic_only_pct DESC
        """,
    )


def export_household_role_models(con: duckdb.DuckDBPyConnection) -> None:
    frame = con.execute(
        """
        SELECT
          CASE
            WHEN p."Relationship to Head" IN ('spouse of head', 'spouse of married child')
              THEN 1
            ELSE 0
          END AS spouse_role,
          hh.has_child_0_5,
          CASE WHEN p.is_domestic_only = 1 THEN 1 ELSE 0 END AS domestic_only,
          CASE WHEN p.is_cws_regular_salaried = 1 THEN 1 ELSE 0 END AS regular_salaried,
          p."Sector" AS sector,
          p."Household Social Group" AS social_group,
          p."Household Type" AS household_type,
          p."Household Religion" AS religion,
          p."State/UT" AS state,
          p."Person Subsample Multiplier" / ? AS model_weight
        FROM plfs p
        JOIN households hh USING (hhid)
        WHERE p."Sex" = 'female'
          AND p."Age" BETWEEN 25 AND 34
          AND p.edu_band = 'graduate+'
          AND p."Marital Status" = 'currently married'
          AND p."Relationship to Head" IN (
            'spouse of head',
            'spouse of married child',
            'self',
            'married child'
          )
        """,
        [MODEL_WEIGHT_SCALE],
    ).fetch_df()

    rows: list[dict[str, object]] = []
    for outcome in ("domestic_only", "regular_salaried"):
        model = smf.wls(
            (
                f"{outcome} ~ spouse_role + has_child_0_5 + C(sector)"
                " + C(social_group) + C(household_type)"
                " + C(religion) + C(state)"
            ),
            data=frame,
            weights=frame["model_weight"],
        ).fit()
        rows.append(
            {
                "outcome": outcome,
                "spouse_role_effect": round(model.params["spouse_role"], 4),
                "spouse_role_effect_points": round(100 * model.params["spouse_role"], 2),
                "spouse_role_std_error_points": round(
                    100 * model.bse["spouse_role"], 2
                ),
                "child_u5_effect": round(model.params["has_child_0_5"], 4),
                "child_u5_effect_points": round(
                    100 * model.params["has_child_0_5"], 2
                ),
                "child_u5_std_error_points": round(
                    100 * model.bse["has_child_0_5"], 2
                ),
                "sample_n": len(frame),
                "weighted_total_m": round(frame["model_weight"].sum() / 1000, 3),
                "controls": (
                    "child under 5 + state + sector + social group"
                    " + household type + religion"
                ),
            }
        )

    write_rows(OUTPUT_DIR / "married_graduate_household_role_model.csv", rows)


def export_selected_professions(con: duckdb.DuckDBPyConnection) -> None:
    export_csv(
        con,
        "selected_professions_quality_21_34.csv",
        f"""
        SELECT
          "Principal Occupation" AS occupation,
          COUNT(*) AS sample_n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE "Sex" = 'female')
            / SUM("Person Subsample Multiplier"),
            1
          ) AS female_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Job Contract Type" IS NOT NULL
                AND "Principal Job Contract Type" != 'no written job contract'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS written_contract_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Job - Paid Leave" = 'yes'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS paid_leave_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Job - Social Security" NOT IN (
                'not eligible for any of above social security benefits',
                'not known'
              )
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS social_security_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier"),
            1
          ) AS strict_formal_pct,
          ROUND(
            quantile_cont("CWS Earnings (Salaried)", 0.5) FILTER (
              WHERE "CWS Earnings (Salaried)" IS NOT NULL
            ),
            1
          ) AS median_salary
        FROM plfs
        WHERE "Age" BETWEEN 21 AND 34
          AND "Principal Activity Status" = 'worked as regular salaried/wage employee'
          AND "Principal Occupation" IN ({quote_values(SELECTED_PROFESSIONS)})
        GROUP BY 1
        ORDER BY strict_formal_pct DESC, weighted_m DESC
        """,
    )

    export_csv(
        con,
        "selected_professions_gender_gaps_21_34.csv",
        f"""
        SELECT
          "Sex" AS sex,
          "Principal Occupation" AS occupation,
          COUNT(*) AS sample_n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier"),
            1
          ) AS strict_formal_pct,
          ROUND(
            quantile_cont("CWS Earnings (Salaried)", 0.5) FILTER (
              WHERE "CWS Earnings (Salaried)" IS NOT NULL
            ),
            1
          ) AS median_salary
        FROM plfs
        WHERE "Age" BETWEEN 21 AND 34
          AND "Principal Activity Status" = 'worked as regular salaried/wage employee'
          AND "Principal Occupation" IN ({quote_values(SELECTED_PROFESSIONS)})
        GROUP BY 1, 2
        ORDER BY occupation, sex
        """,
    )


def export_technical_credential_quality(con: duckdb.DuckDBPyConnection) -> None:
    export_csv(
        con,
        "technical_credential_quality_21_34.csv",
        f"""
        SELECT
          "Technical Education Level" AS credential,
          COUNT(*) AS sample_n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Activity Status" = 'did not work but was seeking and/or available for work'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS seeking_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS regular_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (WHERE is_strict_formal = 1)
            / SUM("Person Subsample Multiplier"),
            1
          ) AS strict_formal_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Job - Social Security" NOT IN (
                'not eligible for any of above social security benefits',
                'not known'
              )
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS social_security_pct,
          ROUND(
            quantile_cont("CWS Earnings (Salaried)", 0.5) FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
                AND "CWS Earnings (Salaried)" IS NOT NULL
            ),
            1
          ) AS median_regular_salary,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
                AND "Principal Workers Count" IN ('less than 6', '6-9')
            )
            / SUM("Person Subsample Multiplier") FILTER (
              WHERE "Principal Activity Status" = 'worked as regular salaried/wage employee'
            ),
            1
          ) AS micro_small_regular_pct
        FROM plfs
        WHERE "Age" BETWEEN 21 AND 34
          AND "Technical Education Level" != 'no technical education'
        GROUP BY 1
        HAVING COUNT(*) >= 80
        ORDER BY regular_pct DESC, strict_formal_pct DESC
        """,
    )

    export_csv(
        con,
        "technical_credential_top_jobs_21_34.csv",
        f"""
        SELECT
          "Technical Education Level" AS credential,
          "Principal Occupation" AS occupation,
          COUNT(*) AS sample_n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            quantile_cont("CWS Earnings (Salaried)", 0.5) FILTER (
              WHERE "CWS Earnings (Salaried)" IS NOT NULL
            ),
            1
          ) AS median_salary
        FROM plfs
        WHERE "Age" BETWEEN 21 AND 34
          AND "Principal Activity Status" = 'worked as regular salaried/wage employee'
          AND "Technical Education Level" IN ({quote_values(FOCUS_CREDENTIALS)})
        GROUP BY 1, 2
        HAVING COUNT(*) >= 30
        ORDER BY credential, weighted_m DESC, occupation
        """,
    )


def export_jobseeker_duration(con: duckdb.DuckDBPyConnection) -> None:
    export_csv(
        con,
        "graduate_jobseeker_duration_25_34.csv",
        f"""
        SELECT
          "Sex" AS sex,
          "Sector" AS sector,
          COUNT(*) AS sample_n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'less than or equal to 6 months'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS le_6m_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 6 months but less than or equal to 1 year'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS m6_to_1y_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 1 year but less than or equal to 2 years'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS y1_to_2_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 2 years but less than or equal to 3 years'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS y2_to_3_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 3 years'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS y3plus_pct
        FROM plfs
        WHERE "Age" BETWEEN 25 AND 34
          AND edu_band = 'graduate+'
          AND "Principal Activity Status" = 'did not work but was seeking and/or available for work'
        GROUP BY 1, 2
        ORDER BY sex, sector
        """,
    )

    export_csv(
        con,
        "graduate_women_jobseeker_duration_marital_25_34.csv",
        f"""
        SELECT
          "Sector" AS sector,
          "Marital Status" AS marital_status,
          COUNT(*) AS sample_n,
          ROUND(SUM("Person Subsample Multiplier") / {WEIGHT_TO_MILLIONS}, 3) AS weighted_m,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 1 year but less than or equal to 2 years'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS y1_to_2_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 2 years but less than or equal to 3 years'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS y2_to_3_pct,
          ROUND(
            100.0
            * SUM("Person Subsample Multiplier") FILTER (
              WHERE "Unemployment Duration" = 'more than 3 years'
            )
            / SUM("Person Subsample Multiplier"),
            1
          ) AS y3plus_pct
        FROM plfs
        WHERE "Sex" = 'female'
          AND "Age" BETWEEN 25 AND 34
          AND edu_band = 'graduate+'
          AND "Principal Activity Status" = 'did not work but was seeking and/or available for work'
          AND "Marital Status" IN ('currently married', 'never married')
        GROUP BY 1, 2
        ORDER BY sector, marital_status
        """,
    )


def export_hidden_work_districts(con: duckdb.DuckDBPyConnection) -> None:
    export_csv(
        con,
        "hidden_work_district_strict.csv",
        f"""
        WITH ranked AS (
          SELECT
            state,
            district,
            COUNT(*) AS sample_n,
            SUM(w) AS weighted_total,
            100.0 * SUM(w * worked_week) / SUM(w) AS hidden_work_pct
          FROM hidden_domestic
          WHERE sector = 'rural'
          GROUP BY 1, 2
          HAVING COUNT(*) >= 100
            AND SUM(w) >= 400000000
        )
        SELECT
          state,
          district,
          sample_n,
          ROUND(weighted_total / {WEIGHT_TO_MILLIONS}, 3) AS homemaker_m,
          ROUND(hidden_work_pct, 1) AS hidden_work_pct
        FROM ranked
        ORDER BY hidden_work_pct DESC, homemaker_m DESC
        """,
    )

    export_csv(
        con,
        "hidden_work_district_strict_overview.csv",
        """
        WITH ranked AS (
          SELECT
            state,
            district,
            COUNT(*) AS sample_n,
            SUM(w) AS weighted_total,
            100.0 * SUM(w * worked_week) / SUM(w) AS hidden_work_pct
          FROM hidden_domestic
          WHERE sector = 'rural'
          GROUP BY 1, 2
          HAVING COUNT(*) >= 100
            AND SUM(w) >= 400000000
        )
        SELECT
          COUNT(*) AS districts_passing,
          ROUND(AVG(hidden_work_pct), 1) AS avg_hidden_work_pct,
          ROUND(100.0 * AVG(CASE WHEN hidden_work_pct >= 20 THEN 1 ELSE 0 END), 1)
            AS districts_20plus_pct,
          ROUND(100.0 * AVG(CASE WHEN hidden_work_pct >= 30 THEN 1 ELSE 0 END), 1)
            AS districts_30plus_pct
        FROM ranked
        """,
    )

    export_csv(
        con,
        "hidden_work_district_strict_state_summary.csv",
        """
        WITH ranked AS (
          SELECT
            state,
            district,
            COUNT(*) AS sample_n,
            SUM(w) AS weighted_total,
            100.0 * SUM(w * worked_week) / SUM(w) AS hidden_work_pct
          FROM hidden_domestic
          WHERE sector = 'rural'
          GROUP BY 1, 2
          HAVING COUNT(*) >= 100
            AND SUM(w) >= 400000000
        )
        SELECT
          state,
          COUNT(*) AS districts_passing,
          ROUND(AVG(hidden_work_pct), 1) AS avg_hidden_work_pct,
          ROUND(MAX(hidden_work_pct), 1) AS max_hidden_work_pct,
          ROUND(100.0 * AVG(CASE WHEN hidden_work_pct >= 30 THEN 1 ELSE 0 END), 1)
            AS districts_30plus_pct
        FROM ranked
        GROUP BY 1
        ORDER BY districts_passing DESC, avg_hidden_work_pct DESC
        """,
    )


def main() -> None:
    seed_v3_outputs()

    con = duckdb.connect()
    setup_views(con)
    export_household_role_tables(con)
    export_household_role_models(con)
    export_selected_professions(con)
    export_technical_credential_quality(con)
    export_jobseeker_duration(con)
    export_hidden_work_districts(con)
    con.close()


if __name__ == "__main__":
    main()
