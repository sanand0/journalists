#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "numpy>=2.0",
#   "pandas>=2.2",
#   "rich>=14.0",
# ]
# ///

"""Generate reproducible insight tables from the local UN data slices."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from rich.traceback import install

install(show_locals=True)

BASE_DIR = Path(__file__).resolve().parent
REPO_DIR = BASE_DIR.parent
DATA_DIR = REPO_DIR / "data" / "downloads"
METADATA_DIR = BASE_DIR / "metadata"
OUTPUT_DIR = BASE_DIR / "outputs"

SDG_DIR = DATA_DIR / "iaeg-sdgs" / "sdg-harmonized-global-dataflow" / "by-year"
NA_MAIN_DIR = DATA_DIR / "estat" / "na-main-aggregates" / "by-year"
NA_SEC_DIR = DATA_DIR / "estat" / "quarterly-financial-accounts" / "by-year"


def require_metadata() -> None:
    """Fail fast if the parsed metadata has not been built yet."""

    required = [
        METADATA_DIR / "sdg_codes.csv",
        METADATA_DIR / "na_main_codes.csv",
        METADATA_DIR / "na_sec_codes.csv",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        missing_list = ", ".join(path.name for path in missing)
        raise FileNotFoundError(
            f"Missing metadata files: {missing_list}. Run `uv run v1/build_metadata.py` first."
        )


def read_csv(path: Path, **kwargs: object) -> pd.DataFrame:
    """Read a CSV while keeping coded values as strings."""

    return pd.read_csv(
        path,
        dtype=str,
        keep_default_na=True,
        na_values=["", "nan", "NaN"],
        **kwargs,
    )


def read_many(paths: list[Path], **kwargs: object) -> pd.DataFrame:
    """Concatenate several CSV files with a source filename column."""

    frames = [read_csv(path, **kwargs).assign(source_file=path.name) for path in paths]
    return pd.concat(frames, ignore_index=True)


def add_numeric_value(df: pd.DataFrame) -> pd.DataFrame:
    """Attach a numeric observation column and a year-like sort key."""

    frame = df.copy()
    frame["obs_value_num"] = pd.to_numeric(frame["OBS_VALUE"], errors="coerce")
    frame["time_period_sort"] = pd.to_numeric(
        frame["TIME_PERIOD"].astype(str).str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )
    return frame


def label_map(codes: pd.DataFrame, codelist_id: str) -> pd.Series:
    """Build a simple code-to-label lookup."""

    subset = codes.loc[codes["codelist_id"] == codelist_id, ["code", "label"]].drop_duplicates("code")
    return subset.set_index("code")["label"]


def country_like_areas(codes: pd.DataFrame) -> pd.DataFrame:
    """Approximate countries and territories using numeric+alpha area label twins."""

    areas = (
        codes.loc[codes["codelist_id"] == "CL_AREA", ["code", "label"]]
        .drop_duplicates()
        .assign(
            is_numeric=lambda df: df["code"].astype(str).str.fullmatch(r"\d+"),
            is_alpha=lambda df: df["code"].astype(str).str.fullmatch(r"[A-Z]{2,3}"),
        )
    )
    flags = areas.groupby("label", as_index=False).agg(
        has_numeric=("is_numeric", "any"),
        has_alpha=("is_alpha", "any"),
    )
    labels = flags.loc[flags["has_numeric"] & flags["has_alpha"], "label"]
    country_map = (
        areas.loc[areas["label"].isin(labels) & areas["is_numeric"], ["code", "label"]]
        .rename(columns={"code": "area_code", "label": "area_name"})
        .sort_values("area_name")
        .reset_index(drop=True)
    )
    return country_map


def latest_per_area(frame: pd.DataFrame, *, sort_columns: list[str], ascending: list[bool]) -> pd.DataFrame:
    """Keep the preferred row per area after sorting."""

    ordered = frame.sort_values(["REF_AREA", *sort_columns], ascending=[True, *ascending])
    return ordered.drop_duplicates(subset=["REF_AREA"], keep="first")


def write_csv(df: pd.DataFrame, filename: str) -> None:
    """Write a dataframe into the outputs directory."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / filename, index=False)


def build_file_inventory() -> None:
    """Profile the downloaded files on disk."""

    records: list[dict[str, object]] = []
    for path in sorted(DATA_DIR.rglob("*.csv.gz")):
        frame = read_csv(path, compression="gzip")
        records.append(
            {
                "path": path.relative_to(REPO_DIR).as_posix(),
                "rows": len(frame),
                "columns": len(frame.columns),
                "column_names": "|".join(frame.columns.tolist()),
            }
        )

    write_csv(pd.DataFrame(records), "local_file_inventory.csv")


def build_sdg_series_profile(sdg: pd.DataFrame, codes: pd.DataFrame) -> None:
    """Create a broad screening table for the SDG slice."""

    series_labels = label_map(codes, "CL_SERIES")
    profile = (
        sdg.groupby("SERIES", dropna=False)
        .agg(
            rows=("SERIES", "size"),
            unique_areas=("REF_AREA", "nunique"),
            unique_periods=("TIME_PERIOD", "nunique"),
            finite_values=("obs_value_num", lambda s: np.isfinite(s).sum()),
            min_value=("obs_value_num", "min"),
            median_value=("obs_value_num", "median"),
            max_value=("obs_value_num", "max"),
            unit_measure=("UNIT_MEASURE", lambda s: "|".join(sorted(set(s.dropna().astype(str))))),
            sex_values=("SEX", "nunique"),
            age_values=("AGE", "nunique"),
            composite_values=("COMPOSITE_BREAKDOWN", "nunique"),
        )
        .reset_index()
        .assign(series_label=lambda df: df["SERIES"].map(series_labels).fillna(""))
        .sort_values(["unique_areas", "rows"], ascending=[False, False])
    )
    write_csv(profile, "sdg_series_profile.csv")


def build_target14_outputs(
    sdg: pd.DataFrame,
    country_sdg: pd.DataFrame,
    codes: pd.DataFrame,
    country_map: pd.DataFrame,
) -> None:
    """Summarize the Kunming-Montreal Target 14 rollout indicator."""

    comp_labels = label_map(codes, "CL_COMP_BREAKDOWN")
    target14 = country_sdg.loc[country_sdg["SERIES"] == "ER_BDY_KMGBFT14"].copy()

    has_target = latest_per_area(
        target14.loc[target14["COMPOSITE_BREAKDOWN"] == "_T", ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"]],
        sort_columns=["time_period_sort"],
        ascending=[False],
    ).rename(columns={"obs_value_num": "has_target"})

    status = target14.loc[
        target14["COMPOSITE_BREAKDOWN"] != "_T",
        ["REF_AREA", "TIME_PERIOD", "time_period_sort", "COMPOSITE_BREAKDOWN", "obs_value_num"],
    ].copy()
    status = status.loc[status["obs_value_num"] == 1].assign(
        status_label=lambda df: df["COMPOSITE_BREAKDOWN"].map(comp_labels).fillna(df["COMPOSITE_BREAKDOWN"])
    )
    status = latest_per_area(
        status,
        sort_columns=["time_period_sort"],
        ascending=[False],
    )[["REF_AREA", "COMPOSITE_BREAKDOWN", "status_label"]]

    country_status = (
        country_map.merge(has_target[["REF_AREA", "has_target"]], left_on="area_code", right_on="REF_AREA", how="left")
        .merge(status, on="REF_AREA", how="left")
        .drop(columns=["REF_AREA"])
        .sort_values("area_name")
    )
    country_status = country_status.loc[
        country_status["has_target"].notna() | country_status["status_label"].notna()
    ].copy()
    country_status["has_target"] = country_status["has_target"].astype("Int64")
    write_csv(country_status, "target14_country_status.csv")

    world = sdg.loc[
        (sdg["SERIES"] == "ER_BDY_KMGBFT14")
        & (sdg["REF_AREA"].astype(str) == "1")
        & np.isfinite(sdg["obs_value_num"]),
        ["COMPOSITE_BREAKDOWN", "obs_value_num"],
    ].copy()
    with_target = int(world.loc[world["COMPOSITE_BREAKDOWN"] == "_T", "obs_value_num"].iloc[0])
    no_target = int(world.loc[world["COMPOSITE_BREAKDOWN"] == "KMGBFT14_NONTLT", "obs_value_num"].iloc[0])
    reporting = with_target + no_target

    status_counts = (
        world.loc[world["COMPOSITE_BREAKDOWN"] != "_T"]
        .assign(
            countries=lambda df: df["obs_value_num"].astype(int),
            status_label=lambda df: df["COMPOSITE_BREAKDOWN"].map(comp_labels).fillna(df["COMPOSITE_BREAKDOWN"]),
            share_of_reporting_pct=lambda df: (df["obs_value_num"] / reporting * 100).round(2),
        )[["COMPOSITE_BREAKDOWN", "status_label", "countries", "share_of_reporting_pct"]]
        .rename(columns={"COMPOSITE_BREAKDOWN": "metric"})
        .sort_values("countries", ascending=False)
    )

    top_rows = pd.DataFrame(
        [
            {"metric": "reporting_countries", "countries": reporting, "share_of_reporting_pct": 100.0},
            {"metric": "countries_with_target", "countries": with_target, "share_of_reporting_pct": round(with_target / reporting * 100, 2)},
            {"metric": "countries_without_target", "countries": no_target, "share_of_reporting_pct": round(no_target / reporting * 100, 2)},
        ]
    )
    status_counts = status_counts.rename(columns={"COMPOSITE_BREAKDOWN": "metric"})
    summary = pd.concat([top_rows, status_counts], ignore_index=True)
    write_csv(summary, "target14_status_summary.csv")


def build_remittance_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Summarize the remittance cost indicator against the SDG 3% target."""

    remittance = (
        country_sdg.loc[
            (country_sdg["SERIES"] == "SI_RMT_COST") & np.isfinite(country_sdg["obs_value_num"]),
            ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"],
        ]
        .pipe(latest_per_area, sort_columns=["time_period_sort"], ascending=[False])
        .rename(columns={"obs_value_num": "cost_pct"})
    )

    ranking = (
        country_map.merge(remittance[["REF_AREA", "cost_pct"]], left_on="area_code", right_on="REF_AREA", how="inner")
        .drop(columns=["REF_AREA"])
        .assign(cost_pct=lambda df: df["cost_pct"].round(2))
        .sort_values(["cost_pct", "area_name"])
        .reset_index(drop=True)
    )
    ranking["rank_low_to_high"] = ranking.index + 1
    write_csv(ranking, "remittance_cost_country_rank.csv")

    summary = pd.DataFrame(
        [
            {
                "reporting_countries": len(ranking),
                "median_cost_pct": round(float(ranking["cost_pct"].median()), 2),
                "countries_meeting_3pct_target": int((ranking["cost_pct"] <= 3).sum()),
                "countries_above_5pct": int((ranking["cost_pct"] > 5).sum()),
                "share_meeting_3pct_target_pct": round(float((ranking["cost_pct"] <= 3).mean() * 100), 2),
                "lowest_cost_area": ranking.iloc[0]["area_name"],
                "lowest_cost_pct": float(ranking.iloc[0]["cost_pct"]),
                "highest_cost_area": ranking.iloc[-1]["area_name"],
                "highest_cost_pct": float(ranking.iloc[-1]["cost_pct"]),
            }
        ]
    )
    write_csv(summary, "remittance_cost_summary.csv")


def build_refugee_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Rank refugee-origin pressure per 100,000 people."""

    refugees = (
        country_sdg.loc[
            (country_sdg["SERIES"] == "SM_POP_REFG_OR") & np.isfinite(country_sdg["obs_value_num"]),
            ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"],
        ]
        .pipe(latest_per_area, sort_columns=["time_period_sort"], ascending=[False])
        .rename(columns={"obs_value_num": "refugees_per_100k"})
    )

    ranking = (
        country_map.merge(refugees[["REF_AREA", "refugees_per_100k"]], left_on="area_code", right_on="REF_AREA", how="inner")
        .drop(columns=["REF_AREA"])
        .sort_values(["refugees_per_100k", "area_name"], ascending=[False, True])
        .reset_index(drop=True)
    )
    ranking["rank_high_to_low"] = ranking.index + 1
    ranking["refugees_per_100k"] = ranking["refugees_per_100k"].round(2)
    write_csv(ranking, "refugee_origin_country_rank.csv")

    ukraine = ranking.loc[ranking["area_name"] == "Ukraine"].iloc[0]
    afghanistan = ranking.loc[ranking["area_name"] == "Afghanistan"].iloc[0]
    summary = pd.DataFrame(
        [
            {
                "reporting_countries": len(ranking),
                "median_refugees_per_100k": round(float(ranking["refugees_per_100k"].median()), 2),
                "countries_above_5000_per_100k": int((ranking["refugees_per_100k"] >= 5000).sum()),
                "countries_above_10000_per_100k": int((ranking["refugees_per_100k"] >= 10000).sum()),
                "top_area": ranking.iloc[0]["area_name"],
                "top_rate": float(ranking.iloc[0]["refugees_per_100k"]),
                "ukraine_rank": int(ukraine["rank_high_to_low"]),
                "ukraine_rate": float(ukraine["refugees_per_100k"]),
                "afghanistan_rank": int(afghanistan["rank_high_to_low"]),
                "afghanistan_rate": float(afghanistan["refugees_per_100k"]),
            }
        ]
    )
    write_csv(summary, "refugee_origin_summary.csv")


def build_parliament_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Compare parliamentary gender balance with youth representation."""

    female_share = latest_per_area(
        country_sdg.loc[
            (country_sdg["SERIES"] == "SG_GEN_PARL")
            & (country_sdg["SEX"] == "F")
            & np.isfinite(country_sdg["obs_value_num"]),
            ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"],
        ],
        sort_columns=["time_period_sort"],
        ascending=[False],
    ).rename(columns={"obs_value_num": "female_share"})

    female_ratio = latest_per_area(
        country_sdg.loc[
            (country_sdg["SERIES"] == "SG_DMK_PARLMP_LC") & np.isfinite(country_sdg["obs_value_num"]),
            ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"],
        ],
        sort_columns=["time_period_sort"],
        ascending=[False],
    ).rename(columns={"obs_value_num": "female_ratio"})

    youth_share_candidates = country_sdg.loc[
        (country_sdg["SERIES"] == "SG_DMK_PARLYTHP_LC")
        & country_sdg["AGE"].isin(["Y0T45", "Y0T40"])
        & np.isfinite(country_sdg["obs_value_num"]),
        ["REF_AREA", "TIME_PERIOD", "time_period_sort", "AGE", "obs_value_num"],
    ].copy()
    youth_share_candidates["age_priority"] = youth_share_candidates["AGE"].map({"Y0T45": 0, "Y0T40": 1}).fillna(9)
    youth_share = latest_per_area(
        youth_share_candidates,
        sort_columns=["age_priority", "time_period_sort"],
        ascending=[True, False],
    ).rename(columns={"obs_value_num": "youth_share", "AGE": "youth_age_band"})

    youth_ratio_candidates = country_sdg.loc[
        (country_sdg["SERIES"] == "SG_DMK_PARLYTHR_LC")
        & country_sdg["AGE"].isin(["Y0T45", "Y0T40"])
        & np.isfinite(country_sdg["obs_value_num"]),
        ["REF_AREA", "TIME_PERIOD", "time_period_sort", "AGE", "obs_value_num"],
    ].copy()
    youth_ratio_candidates["age_priority"] = youth_ratio_candidates["AGE"].map({"Y0T45": 0, "Y0T40": 1}).fillna(9)
    youth_ratio = latest_per_area(
        youth_ratio_candidates,
        sort_columns=["age_priority", "time_period_sort"],
        ascending=[True, False],
    ).rename(columns={"obs_value_num": "youth_ratio", "AGE": "youth_ratio_age_band"})

    parliament = (
        country_map.merge(female_share[["REF_AREA", "female_share"]], left_on="area_code", right_on="REF_AREA", how="left")
        .merge(female_ratio[["REF_AREA", "female_ratio"]], on="REF_AREA", how="left")
        .merge(youth_share[["REF_AREA", "youth_share", "youth_age_band"]], on="REF_AREA", how="left")
        .merge(youth_ratio[["REF_AREA", "youth_ratio", "youth_ratio_age_band"]], on="REF_AREA", how="left")
        .drop(columns=["REF_AREA"])
        .sort_values("area_name")
        .reset_index(drop=True)
    )

    for column in ["female_share", "female_ratio", "youth_share", "youth_ratio"]:
        parliament[column] = parliament[column].round(2)

    write_csv(parliament, "parliament_representation_country_rank.csv")

    complete = parliament.dropna(subset=["female_share", "female_ratio", "youth_share", "youth_ratio"]).copy()
    high_female_low_youth = complete.loc[
        (complete["female_share"] >= 45) & (complete["youth_ratio"] < 0.5),
        ["area_name", "female_share", "female_ratio", "youth_share", "youth_ratio", "youth_age_band"],
    ].sort_values(["youth_ratio", "female_share"], ascending=[True, False])
    write_csv(high_female_low_youth, "parliament_high_female_low_youth.csv")

    summary = pd.DataFrame(
        [
            {
                "countries_with_complete_data": len(complete),
                "median_female_share": round(float(complete["female_share"].median()), 2),
                "median_female_ratio": round(float(complete["female_ratio"].median()), 2),
                "median_youth_share": round(float(complete["youth_share"].median()), 2),
                "median_youth_ratio": round(float(complete["youth_ratio"].median()), 2),
                "youth_parity_or_better": int((complete["youth_ratio"] >= 1).sum()),
                "youth_less_than_half_represented": int((complete["youth_ratio"] < 0.5).sum()),
                "high_female_parliaments": int((complete["female_share"] >= 45).sum()),
                "high_female_low_youth": int(len(high_female_low_youth)),
            }
        ]
    )
    write_csv(summary, "parliament_summary.csv")


def build_youth_employment_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Summarize youth-employment strategy scorecards."""

    strategy = (
        country_sdg.loc[
            (country_sdg["SERIES"] == "SL_CPA_YEMP") & np.isfinite(country_sdg["obs_value_num"]),
            ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"],
        ]
        .pipe(latest_per_area, sort_columns=["time_period_sort"], ascending=[False])
        .rename(columns={"obs_value_num": "score"})
    )

    ranking = (
        country_map.merge(strategy[["REF_AREA", "score"]], left_on="area_code", right_on="REF_AREA", how="inner")
        .drop(columns=["REF_AREA"])
        .sort_values(["score", "area_name"], ascending=[False, True])
        .reset_index(drop=True)
    )
    write_csv(ranking, "youth_employment_strategy_scores.csv")

    counts = (
        ranking.groupby("score", as_index=False)
        .agg(countries=("area_name", "size"))
        .assign(
            description=lambda df: df["score"].map(
                {
                    0.0: "No strategy",
                    1.0: "Under development",
                    2.0: "Developed but not operational",
                    3.0: "Operationalized",
                }
            )
        )
        .sort_values("score")
    )
    write_csv(counts, "youth_employment_strategy_summary.csv")


def build_eurostat_inventory(na_main_codes: pd.DataFrame, na_sec_codes: pd.DataFrame) -> None:
    """Document why the local Eurostat slices were less usable for simple cross-country insights."""

    na_main = read_many(sorted(NA_MAIN_DIR.glob("*.csv.gz")), compression="gzip", usecols=["STO", "UNIT_MEASURE", "PRICES", "ACCOUNTING_ENTRY", "REF_AREA"])
    na_sec = read_many(sorted(NA_SEC_DIR.glob("*.csv.gz")), compression="gzip", usecols=["UNIT_MEASURE"])

    unit_labels_main = label_map(na_main_codes, "CL_UNIT")
    price_labels_main = label_map(na_main_codes, "CL_NA_PRICES")
    sto_labels_main = label_map(na_main_codes, "CL_NA_STO")

    na_main_units = (
        na_main[["UNIT_MEASURE"]]
        .drop_duplicates()
        .assign(unit_label=lambda df: df["UNIT_MEASURE"].map(unit_labels_main).fillna(""))
        .sort_values("UNIT_MEASURE")
    )
    write_csv(na_main_units, "eurostat_na_main_unit_measures.csv")

    gdp_availability = (
        na_main.loc[na_main["STO"] == "B1GQ"]
        .groupby(["UNIT_MEASURE", "PRICES", "ACCOUNTING_ENTRY"], as_index=False)
        .agg(rows=("REF_AREA", "size"), geos=("REF_AREA", "nunique"))
        .assign(
            sto_label=sto_labels_main.get("B1GQ", ""),
            unit_label=lambda df: df["UNIT_MEASURE"].map(unit_labels_main).fillna(""),
            price_label=lambda df: df["PRICES"].map(price_labels_main).fillna(""),
        )
        .sort_values(["geos", "rows"], ascending=[False, False])
    )
    write_csv(gdp_availability, "eurostat_na_main_gdp_availability.csv")

    unit_labels_sec = label_map(na_sec_codes, "CL_UNIT")
    na_sec_units = (
        na_sec[["UNIT_MEASURE"]]
        .drop_duplicates()
        .assign(unit_label=lambda df: df["UNIT_MEASURE"].map(unit_labels_sec).fillna(""))
        .sort_values("UNIT_MEASURE")
    )
    write_csv(na_sec_units, "eurostat_na_sec_unit_measures.csv")


def main() -> None:
    """Run the full local analysis pipeline."""

    require_metadata()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    codes = read_csv(METADATA_DIR / "sdg_codes.csv")
    na_main_codes = read_csv(METADATA_DIR / "na_main_codes.csv")
    na_sec_codes = read_csv(METADATA_DIR / "na_sec_codes.csv")

    build_file_inventory()
    country_map = country_like_areas(codes)
    write_csv(country_map, "sdg_country_like_areas.csv")

    sdg = add_numeric_value(read_many(sorted(SDG_DIR.glob("*.csv.gz")), compression="gzip"))
    build_sdg_series_profile(sdg, codes)

    country_sdg = sdg.loc[sdg["REF_AREA"].astype(str).isin(country_map["area_code"])].copy()
    build_target14_outputs(sdg, country_sdg, codes, country_map)
    build_remittance_outputs(country_sdg, country_map)
    build_refugee_outputs(country_sdg, country_map)
    build_parliament_outputs(country_sdg, country_map)
    build_youth_employment_outputs(country_sdg, country_map)
    build_eurostat_inventory(na_main_codes, na_sec_codes)


if __name__ == "__main__":
    main()
