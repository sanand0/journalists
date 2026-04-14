#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "numpy>=2.0",
#   "pandas>=2.2",
#   "rich>=14.0",
# ]
# ///

"""Generate reproducible v2 insight tables from the local UN data slices."""

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

CANDIDATE_SERIES = [
    "SI_RMT_COST",
    "SI_RMT_COST_BC",
    "SI_RMT_COST_SND",
    "SL_EMP_PCAP",
    "SM_DTH_MIGR",
    "SM_POP_REFG_OR",
    "SG_GEN_PARL",
    "SG_DMK_PARLMP_LC",
    "SG_DMK_PARLYTHP_LC",
    "SG_DMK_PARLYTHR_LC",
    "SL_CPA_YEMP",
    "ER_BDY_KMGBFT14",
    "AG_LND_FRSTCHG",
    "AG_LND_FRSTMGT",
    "IC_FRM_BRIB",
    "AG_FPA_COMM",
    "IT_USE_II99",
    "IT_MOB_OWN",
    "SI_COV_BENFTS",
]

INDIA_PEERS = [
    "India",
    "Pakistan",
    "Bangladesh",
    "Nepal",
    "Sri Lanka",
    "Bhutan",
    "China",
    "Indonesia",
    "Viet Nam",
]


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
            f"Missing metadata files: {missing_list}. Run `uv run v2/build_metadata.py` first."
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
    """Attach numeric observation and sortable time columns."""

    frame = df.copy()
    frame["obs_value_num"] = pd.to_numeric(frame["OBS_VALUE"], errors="coerce")
    frame["time_period_sort"] = pd.to_numeric(
        frame["TIME_PERIOD"].astype(str).str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )
    return frame


def label_map(codes: pd.DataFrame, codelist_id: str) -> pd.Series:
    """Build a code-to-label lookup for one codelist."""

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
    return (
        areas.loc[areas["label"].isin(labels) & areas["is_numeric"], ["code", "label"]]
        .rename(columns={"code": "area_code", "label": "area_name"})
        .sort_values("area_name")
        .reset_index(drop=True)
    )


def latest_per_area(frame: pd.DataFrame, *, sort_columns: list[str], ascending: list[bool]) -> pd.DataFrame:
    """Keep the preferred row per area after sorting."""

    ordered = frame.sort_values(["REF_AREA", *sort_columns], ascending=[True, *ascending])
    return ordered.drop_duplicates(subset=["REF_AREA"], keep="first")


def latest_series(
    frame: pd.DataFrame,
    *,
    series: str,
    filters: dict[str, str | list[str]],
    value_name: str,
    extra_columns: list[str] | None = None,
    sort_columns: list[str] | None = None,
    ascending: list[bool] | None = None,
) -> pd.DataFrame:
    """Filter a series and keep the preferred latest row per area."""

    subset = frame.loc[frame["SERIES"] == series].copy()
    for column, allowed in filters.items():
        allowed_values = [allowed] if isinstance(allowed, str) else allowed
        subset = subset.loc[subset[column].astype(str).isin([str(value) for value in allowed_values])]

    subset = subset.loc[np.isfinite(subset["obs_value_num"])]
    keep_columns = ["REF_AREA", "TIME_PERIOD", "time_period_sort", "obs_value_num"]
    if extra_columns:
        keep_columns.extend(extra_columns)

    latest = latest_per_area(
        subset[keep_columns].copy(),
        sort_columns=sort_columns or ["time_period_sort"],
        ascending=ascending or [False],
    )
    return latest.rename(columns={"obs_value_num": value_name})


def with_country_names(frame: pd.DataFrame, country_map: pd.DataFrame) -> pd.DataFrame:
    """Attach country labels to a REF_AREA-based table."""

    return (
        country_map.merge(frame, left_on="area_code", right_on="REF_AREA", how="inner")
        .drop(columns=["REF_AREA"])
        .sort_values("area_name")
        .reset_index(drop=True)
    )


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
            }
        )

    write_csv(pd.DataFrame(records), "local_file_inventory.csv")


def build_candidate_indicator_profile(sdg: pd.DataFrame, country_sdg: pd.DataFrame, codes: pd.DataFrame) -> None:
    """Summarize the main series screened for v2."""

    series_labels = label_map(codes, "CL_SERIES")
    profile = (
        country_sdg.loc[country_sdg["SERIES"].isin(CANDIDATE_SERIES)]
        .groupby("SERIES", dropna=False)
        .agg(
            country_like_areas=("REF_AREA", "nunique"),
            periods=("TIME_PERIOD", "nunique"),
            finite_values=("obs_value_num", lambda s: np.isfinite(s).sum()),
            min_value=("obs_value_num", "min"),
            median_value=("obs_value_num", "median"),
            max_value=("obs_value_num", "max"),
            unit_measure=("UNIT_MEASURE", lambda s: "|".join(sorted(set(s.dropna().astype(str))))),
        )
        .reset_index()
        .assign(series_label=lambda df: df["SERIES"].map(series_labels).fillna(""))
        .sort_values(["country_like_areas", "SERIES"], ascending=[False, True])
    )
    write_csv(profile, "candidate_indicator_profile.csv")

    india_snapshot = (
        sdg.loc[(sdg["REF_AREA"].astype(str) == "356") & sdg["SERIES"].isin(CANDIDATE_SERIES) & np.isfinite(sdg["obs_value_num"])]
        .assign(series_label=lambda df: df["SERIES"].map(series_labels).fillna(""))
        .loc[
            :,
            [
                "SERIES",
                "series_label",
                "TIME_PERIOD",
                "SEX",
                "AGE",
                "CUST_BREAKDOWN",
                "COMPOSITE_BREAKDOWN",
                "UNIT_MEASURE",
                "obs_value_num",
            ],
        ]
        .rename(columns={"obs_value_num": "value"})
        .sort_values(["SERIES", "TIME_PERIOD", "AGE", "SEX"])
        .reset_index(drop=True)
    )
    write_csv(india_snapshot, "india_indicator_snapshot.csv")


def build_global_remittance_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Summarize the standard remittance-cost indicator."""

    remittance = latest_series(
        country_sdg,
        series="SI_RMT_COST",
        filters={},
        value_name="cost_pct",
    )

    ranking = with_country_names(remittance, country_map).assign(
        cost_pct=lambda df: df["cost_pct"].round(2),
        fee_usd_on_200=lambda df: (df["cost_pct"] * 2).round(2),
    )
    ranking = ranking.sort_values(["cost_pct", "area_name"]).reset_index(drop=True)
    ranking["rank_low_to_high"] = ranking.index + 1
    ranking["meets_3pct_target"] = ranking["cost_pct"] <= 3
    write_csv(ranking, "remittance_global_country_rank.csv")

    india_row = ranking.loc[ranking["area_name"] == "India"]
    summary = pd.DataFrame(
        [
            {
                "reporting_areas": len(ranking),
                "median_cost_pct": round(float(ranking["cost_pct"].median()), 2),
                "median_fee_usd_on_200": round(float(ranking["fee_usd_on_200"].median()), 2),
                "areas_meeting_3pct_target": int((ranking["meets_3pct_target"]).sum()),
                "areas_above_5pct": int((ranking["cost_pct"] > 5).sum()),
                "india_cost_pct": float(india_row["cost_pct"].iloc[0]) if not india_row.empty else np.nan,
                "india_fee_usd_on_200": float(india_row["fee_usd_on_200"].iloc[0]) if not india_row.empty else np.nan,
                "india_rank_low_to_high": int(india_row["rank_low_to_high"].iloc[0]) if not india_row.empty else pd.NA,
            }
        ]
    )
    write_csv(summary, "remittance_global_summary.csv")


def build_india_corridor_outputs(sdg: pd.DataFrame, codes: pd.DataFrame) -> None:
    """Summarize corridor-level remittance costs into India."""

    area_labels = (
        codes.loc[codes["codelist_id"] == "CL_AREA", ["code", "label"]]
        .drop_duplicates("code")
        .rename(columns={"code": "area_code", "label": "area_name"})
    )

    corridor = (
        sdg.loc[(sdg["SERIES"] == "SI_RMT_COST_BC") & np.isfinite(sdg["obs_value_num"])]
        .assign(
            sender_code=lambda df: df["REF_AREA"].astype(str),
            receiver_code=lambda df: df["CUST_BREAKDOWN"].astype(str).str.replace(r"^C", "", regex=True),
        )
        .loc[:, ["sender_code", "receiver_code", "obs_value_num"]]
        .rename(columns={"obs_value_num": "cost_pct"})
    )

    inbound = (
        corridor.loc[corridor["receiver_code"] == "356"]
        .merge(area_labels.rename(columns={"area_code": "sender_code", "area_name": "sender_area"}), on="sender_code", how="left")
        .merge(area_labels.rename(columns={"area_code": "receiver_code", "area_name": "receiver_area"}), on="receiver_code", how="left")
        .assign(
            cost_pct=lambda df: df["cost_pct"].round(2),
            fee_usd_on_200=lambda df: (df["cost_pct"] * 2).round(2),
            band=lambda df: np.select(
                [df["cost_pct"] <= 3, df["cost_pct"] <= 5],
                ["at_or_below_target", "above_target_but_under_5"],
                default="above_5",
            ),
            meets_3pct_target=lambda df: df["cost_pct"] <= 3,
        )
        .sort_values(["cost_pct", "sender_area"])
        .reset_index(drop=True)
    )
    write_csv(inbound, "india_inbound_remittance_corridors.csv")

    outbound = (
        corridor.loc[corridor["sender_code"] == "356"]
        .merge(area_labels.rename(columns={"area_code": "receiver_code", "area_name": "receiver_area"}), on="receiver_code", how="left")
        .assign(
            cost_pct=lambda df: df["cost_pct"].round(2),
            fee_usd_on_200=lambda df: (df["cost_pct"] * 2).round(2),
        )
        .sort_values(["cost_pct", "receiver_area"])
        .reset_index(drop=True)
    )
    write_csv(outbound, "india_outbound_remittance_corridors.csv")

    summary = pd.DataFrame(
        [
            {
                "india_corridors": len(inbound),
                "median_cost_pct": round(float(inbound["cost_pct"].median()), 2),
                "median_fee_usd_on_200": round(float(inbound["fee_usd_on_200"].median()), 2),
                "corridors_at_or_below_3pct": int((inbound["meets_3pct_target"]).sum()),
                "corridors_above_5pct": int((inbound["cost_pct"] > 5).sum()),
                "cheapest_sender": inbound.iloc[0]["sender_area"],
                "cheapest_cost_pct": float(inbound.iloc[0]["cost_pct"]),
                "cheapest_fee_usd_on_200": float(inbound.iloc[0]["fee_usd_on_200"]),
                "costliest_sender": inbound.iloc[-1]["sender_area"],
                "costliest_cost_pct": float(inbound.iloc[-1]["cost_pct"]),
                "costliest_fee_usd_on_200": float(inbound.iloc[-1]["fee_usd_on_200"]),
            }
        ]
    )
    write_csv(summary, "india_inbound_remittance_summary.csv")


def build_worker_productivity_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Rank worker-productivity growth."""

    productivity = latest_series(
        country_sdg,
        series="SL_EMP_PCAP",
        filters={
            "AGE": "Y_GE15",
            "SEX": "_T",
            "URBANISATION": "_T",
            "INCOME_WEALTH_QUANTILE": "_T",
            "EDUCATION_LEV": "_T",
            "OCCUPATION": "_T",
            "CUST_BREAKDOWN": "_T",
            "COMPOSITE_BREAKDOWN": "_T",
            "DISABILITY_STATUS": "_T",
            "ACTIVITY": "_T",
            "PRODUCT": "_T",
        },
        value_name="productivity_growth_pct",
    )

    ranking = with_country_names(productivity, country_map)
    ranking["productivity_growth_pct"] = ranking["productivity_growth_pct"].round(2)
    ranking = ranking.sort_values(["productivity_growth_pct", "area_name"], ascending=[False, True]).reset_index(drop=True)
    ranking["rank_high_to_low"] = ranking.index + 1
    write_csv(ranking, "worker_productivity_growth_rank.csv")

    peers = ranking.loc[ranking["area_name"].isin(INDIA_PEERS)].copy()
    write_csv(peers, "worker_productivity_india_peers.csv")

    india_row = ranking.loc[ranking["area_name"] == "India"].iloc[0]
    median_value = float(ranking["productivity_growth_pct"].median())
    summary = pd.DataFrame(
        [
            {
                "reporting_areas": len(ranking),
                "median_productivity_growth_pct": round(median_value, 2),
                "india_productivity_growth_pct": float(india_row["productivity_growth_pct"]),
                "india_rank_high_to_low": int(india_row["rank_high_to_low"]),
                "india_vs_median_ratio": round(float(india_row["productivity_growth_pct"]) / median_value, 2),
                "top_area": ranking.iloc[0]["area_name"],
                "top_productivity_growth_pct": float(ranking.iloc[0]["productivity_growth_pct"]),
            }
        ]
    )
    write_csv(summary, "worker_productivity_summary.csv")


def build_migration_deaths_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Rank migration deaths and measure concentration."""

    deaths = latest_series(
        country_sdg,
        series="SM_DTH_MIGR",
        filters={
            "AGE": "_T",
            "SEX": "_T",
            "CUST_BREAKDOWN": "_T",
            "COMPOSITE_BREAKDOWN": "_T",
            "ACTIVITY": "_T",
            "PRODUCT": "_T",
        },
        value_name="recorded_deaths",
    )

    ranking = with_country_names(deaths, country_map)
    ranking["recorded_deaths"] = ranking["recorded_deaths"].round(0)
    ranking = ranking.sort_values(["recorded_deaths", "area_name"], ascending=[False, True]).reset_index(drop=True)
    ranking["rank_high_to_low"] = ranking.index + 1
    write_csv(ranking, "migration_deaths_rank.csv")

    total_deaths = float(ranking["recorded_deaths"].sum())
    concentration = pd.DataFrame(
        [
            {
                "top_n": 5,
                "deaths_in_top_n": float(ranking.head(5)["recorded_deaths"].sum()),
                "share_of_total_pct": round(float(ranking.head(5)["recorded_deaths"].sum()) / total_deaths * 100, 2),
            },
            {
                "top_n": 10,
                "deaths_in_top_n": float(ranking.head(10)["recorded_deaths"].sum()),
                "share_of_total_pct": round(float(ranking.head(10)["recorded_deaths"].sum()) / total_deaths * 100, 2),
            },
        ]
    )
    write_csv(concentration, "migration_deaths_concentration.csv")

    india_row = ranking.loc[ranking["area_name"] == "India"]
    summary = pd.DataFrame(
        [
            {
                "reporting_areas": len(ranking),
                "median_recorded_deaths": round(float(ranking["recorded_deaths"].median()), 2),
                "total_recorded_deaths": round(total_deaths, 0),
                "top_area": ranking.iloc[0]["area_name"],
                "top_recorded_deaths": float(ranking.iloc[0]["recorded_deaths"]),
                "india_recorded_deaths": float(india_row["recorded_deaths"].iloc[0]) if not india_row.empty else np.nan,
                "india_rank_high_to_low": int(india_row["rank_high_to_low"].iloc[0]) if not india_row.empty else pd.NA,
                "top_5_share_pct": float(concentration.loc[concentration["top_n"] == 5, "share_of_total_pct"].iloc[0]),
                "top_10_share_pct": float(concentration.loc[concentration["top_n"] == 10, "share_of_total_pct"].iloc[0]),
            }
        ]
    )
    write_csv(summary, "migration_deaths_summary.csv")


def build_refugee_origin_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Rank refugee-origin pressure per 100,000 people."""

    refugees = latest_series(
        country_sdg,
        series="SM_POP_REFG_OR",
        filters={},
        value_name="refugees_per_100k",
    )

    ranking = with_country_names(refugees, country_map)
    ranking["refugees_per_100k"] = ranking["refugees_per_100k"].round(2)
    ranking = ranking.sort_values(["refugees_per_100k", "area_name"], ascending=[False, True]).reset_index(drop=True)
    ranking["rank_high_to_low"] = ranking.index + 1
    write_csv(ranking, "refugee_origin_country_rank.csv")

    ukraine = ranking.loc[ranking["area_name"] == "Ukraine"].iloc[0]
    afghanistan = ranking.loc[ranking["area_name"] == "Afghanistan"].iloc[0]
    summary = pd.DataFrame(
        [
            {
                "reporting_areas": len(ranking),
                "median_refugees_per_100k": round(float(ranking["refugees_per_100k"].median()), 2),
                "areas_above_5000_per_100k": int((ranking["refugees_per_100k"] >= 5000).sum()),
                "areas_above_10000_per_100k": int((ranking["refugees_per_100k"] >= 10000).sum()),
                "ukraine_rank_high_to_low": int(ukraine["rank_high_to_low"]),
                "ukraine_refugees_per_100k": float(ukraine["refugees_per_100k"]),
                "afghanistan_rank_high_to_low": int(afghanistan["rank_high_to_low"]),
                "afghanistan_refugees_per_100k": float(afghanistan["refugees_per_100k"]),
            }
        ]
    )
    write_csv(summary, "refugee_origin_summary.csv")


def build_parliament_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Compare female representation with youth representation in parliament."""

    female_share = latest_series(
        country_sdg,
        series="SG_GEN_PARL",
        filters={"SEX": "F"},
        value_name="female_share",
    )

    female_ratio = latest_series(
        country_sdg,
        series="SG_DMK_PARLMP_LC",
        filters={},
        value_name="female_ratio",
    )

    youth_share_candidates = country_sdg.loc[
        (country_sdg["SERIES"] == "SG_DMK_PARLYTHP_LC")
        & country_sdg["AGE"].astype(str).isin(["Y0T45", "Y0T40"])
        & np.isfinite(country_sdg["obs_value_num"])
    ].copy()
    youth_share_candidates["age_priority"] = youth_share_candidates["AGE"].map({"Y0T45": 0, "Y0T40": 1}).fillna(9)
    youth_share = latest_per_area(
        youth_share_candidates.loc[:, ["REF_AREA", "TIME_PERIOD", "time_period_sort", "AGE", "age_priority", "obs_value_num"]],
        sort_columns=["age_priority", "time_period_sort"],
        ascending=[True, False],
    ).rename(columns={"obs_value_num": "youth_share", "AGE": "youth_share_age_band"})

    youth_ratio_candidates = country_sdg.loc[
        (country_sdg["SERIES"] == "SG_DMK_PARLYTHR_LC")
        & country_sdg["AGE"].astype(str).isin(["Y0T45", "Y0T40"])
        & np.isfinite(country_sdg["obs_value_num"])
    ].copy()
    youth_ratio_candidates["age_priority"] = youth_ratio_candidates["AGE"].map({"Y0T45": 0, "Y0T40": 1}).fillna(9)
    youth_ratio = latest_per_area(
        youth_ratio_candidates.loc[:, ["REF_AREA", "TIME_PERIOD", "time_period_sort", "AGE", "age_priority", "obs_value_num"]],
        sort_columns=["age_priority", "time_period_sort"],
        ascending=[True, False],
    ).rename(columns={"obs_value_num": "youth_ratio", "AGE": "youth_ratio_age_band"})

    parliament = (
        country_map.merge(female_share[["REF_AREA", "female_share"]], left_on="area_code", right_on="REF_AREA", how="left")
        .merge(female_ratio[["REF_AREA", "female_ratio"]], on="REF_AREA", how="left")
        .merge(youth_share[["REF_AREA", "youth_share", "youth_share_age_band"]], on="REF_AREA", how="left")
        .merge(youth_ratio[["REF_AREA", "youth_ratio", "youth_ratio_age_band"]], on="REF_AREA", how="left")
        .drop(columns=["REF_AREA"])
        .sort_values("area_name")
        .reset_index(drop=True)
    )
    parliament = parliament.loc[
        parliament[["female_share", "female_ratio", "youth_share", "youth_ratio"]].notna().any(axis=1)
    ].copy()

    female_rank = (
        parliament.loc[parliament["female_share"].notna(), ["area_name", "female_share"]]
        .sort_values(["female_share", "area_name"], ascending=[False, True])
        .reset_index(drop=True)
    )
    female_rank["female_share_rank_high_to_low"] = female_rank.index + 1

    youth_rank = (
        parliament.loc[parliament["youth_ratio"].notna(), ["area_name", "youth_ratio"]]
        .sort_values(["youth_ratio", "area_name"], ascending=[False, True])
        .reset_index(drop=True)
    )
    youth_rank["youth_ratio_rank_high_to_low"] = youth_rank.index + 1

    parliament = parliament.merge(female_rank[["area_name", "female_share_rank_high_to_low"]], on="area_name", how="left")
    parliament = parliament.merge(youth_rank[["area_name", "youth_ratio_rank_high_to_low"]], on="area_name", how="left")

    for column in ["female_share", "female_ratio", "youth_share", "youth_ratio"]:
        parliament[column] = parliament[column].round(2)

    write_csv(parliament, "parliament_representation_rank.csv")

    high_female_low_youth = parliament.loc[
        (parliament["female_share"] >= 45) & (parliament["youth_ratio"] < 0.5),
        [
            "area_name",
            "female_share",
            "female_ratio",
            "youth_share",
            "youth_share_age_band",
            "youth_ratio",
            "youth_ratio_age_band",
        ],
    ].sort_values(["youth_ratio", "female_share"], ascending=[True, False])
    write_csv(high_female_low_youth, "parliament_high_female_low_youth.csv")

    india_peers = parliament.loc[parliament["area_name"].isin([peer for peer in INDIA_PEERS if peer != "Bhutan"])].copy()
    write_csv(india_peers.sort_values("area_name"), "india_parliament_peers.csv")

    complete = parliament.dropna(subset=["female_share", "youth_ratio"]).copy()
    india_row = parliament.loc[parliament["area_name"] == "India"].iloc[0]
    summary = pd.DataFrame(
        [
            {
                "areas_with_complete_female_and_youth_data": len(complete),
                "median_female_share": round(float(complete["female_share"].median()), 2),
                "median_youth_ratio": round(float(complete["youth_ratio"].median()), 2),
                "india_female_share": float(india_row["female_share"]),
                "india_female_share_rank_high_to_low": int(india_row["female_share_rank_high_to_low"]),
                "india_youth_ratio": float(india_row["youth_ratio"]),
                "india_youth_ratio_rank_high_to_low": int(india_row["youth_ratio_rank_high_to_low"]),
                "high_female_parliaments": int((complete["female_share"] >= 45).sum()),
                "high_female_low_youth_parliaments": int(len(high_female_low_youth)),
            }
        ]
    )
    write_csv(summary, "parliament_summary.csv")


def build_youth_employment_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Summarize youth-employment strategy scorecards."""

    strategy = latest_series(
        country_sdg,
        series="SL_CPA_YEMP",
        filters={},
        value_name="score",
    )

    description_map = {
        0.0: "No strategy",
        1.0: "Under development",
        2.0: "Developed but not operational",
        3.0: "Operationalized",
    }

    ranking = with_country_names(strategy, country_map)
    ranking = ranking.assign(
        score=lambda df: df["score"].round(0),
        description=lambda df: df["score"].map(description_map).fillna("Unknown"),
    )
    ranking = ranking.sort_values(["score", "area_name"], ascending=[False, True]).reset_index(drop=True)
    ranking["rank_high_to_low"] = ranking.index + 1
    write_csv(ranking, "youth_employment_strategy_scores.csv")

    counts = (
        ranking.groupby(["score", "description"], as_index=False)
        .agg(areas=("area_name", "size"))
        .sort_values("score")
        .reset_index(drop=True)
    )
    counts["share_of_reporting_pct"] = (counts["areas"] / len(ranking) * 100).round(2)
    write_csv(counts, "youth_employment_strategy_summary.csv")

    peers = ranking.loc[ranking["area_name"].isin([peer for peer in INDIA_PEERS if peer != "Bhutan"])].copy()
    write_csv(peers, "youth_employment_strategy_india_peers.csv")


def build_biodiversity_planning_outputs(sdg: pd.DataFrame, country_sdg: pd.DataFrame, codes: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Summarize the Target 14 biodiversity-planning indicator."""

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
    write_csv(country_status, "biodiversity_planning_country_status.csv")

    world = sdg.loc[
        (sdg["SERIES"] == "ER_BDY_KMGBFT14")
        & (sdg["REF_AREA"].astype(str) == "1")
        & np.isfinite(sdg["obs_value_num"]),
        ["COMPOSITE_BREAKDOWN", "obs_value_num"],
    ].copy()
    with_target = int(world.loc[world["COMPOSITE_BREAKDOWN"] == "_T", "obs_value_num"].iloc[0])
    no_target = int(world.loc[world["COMPOSITE_BREAKDOWN"] == "KMGBFT14_NONTLT", "obs_value_num"].iloc[0])
    reporting = with_target + no_target

    breakdown = (
        world.loc[world["COMPOSITE_BREAKDOWN"] != "_T"]
        .assign(
            countries=lambda df: df["obs_value_num"].astype(int),
            status_label=lambda df: df["COMPOSITE_BREAKDOWN"].map(comp_labels).fillna(df["COMPOSITE_BREAKDOWN"]),
            share_of_reporting_pct=lambda df: (df["obs_value_num"] / reporting * 100).round(2),
        )[["COMPOSITE_BREAKDOWN", "status_label", "countries", "share_of_reporting_pct"]]
        .rename(columns={"COMPOSITE_BREAKDOWN": "metric"})
        .sort_values("countries", ascending=False)
        .reset_index(drop=True)
    )

    summary = pd.concat(
        [
            pd.DataFrame(
                [
                    {"metric": "reporting_areas", "countries": reporting, "share_of_reporting_pct": 100.0, "status_label": ""},
                    {"metric": "areas_with_target", "countries": with_target, "share_of_reporting_pct": round(with_target / reporting * 100, 2), "status_label": ""},
                    {"metric": "areas_without_target", "countries": no_target, "share_of_reporting_pct": round(no_target / reporting * 100, 2), "status_label": ""},
                ]
            ),
            breakdown,
        ],
        ignore_index=True,
    )
    write_csv(summary, "biodiversity_planning_summary.csv")


def build_forest_peer_outputs(country_sdg: pd.DataFrame, country_map: pd.DataFrame) -> None:
    """Build a small India-and-peers forest comparison table for notes."""

    forest_change = latest_series(
        country_sdg,
        series="AG_LND_FRSTCHG",
        filters={},
        value_name="forest_change_pct",
    )
    managed_forest = latest_series(
        country_sdg,
        series="AG_LND_FRSTMGT",
        filters={},
        value_name="managed_forest_pct",
    )

    forest = (
        country_map.merge(forest_change[["REF_AREA", "forest_change_pct"]], left_on="area_code", right_on="REF_AREA", how="left")
        .merge(managed_forest[["REF_AREA", "managed_forest_pct"]], on="REF_AREA", how="left")
        .drop(columns=["REF_AREA"])
    )
    forest = forest.loc[forest["area_name"].isin(["India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka", "China", "Indonesia", "Brazil"])].copy()
    forest["forest_change_pct"] = forest["forest_change_pct"].round(2)
    forest["managed_forest_pct"] = forest["managed_forest_pct"].round(2)
    write_csv(forest.sort_values("area_name"), "forest_india_peer_comparison.csv")


def main() -> None:
    """Run the full v2 analysis pipeline."""

    require_metadata()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    codes = read_csv(METADATA_DIR / "sdg_codes.csv")
    country_map = country_like_areas(codes)
    write_csv(country_map, "sdg_country_like_areas.csv")

    build_file_inventory()

    sdg = add_numeric_value(read_many(sorted(SDG_DIR.glob("*.csv.gz")), compression="gzip"))
    country_sdg = sdg.loc[sdg["REF_AREA"].astype(str).isin(country_map["area_code"])].copy()

    build_candidate_indicator_profile(sdg, country_sdg, codes)
    build_global_remittance_outputs(country_sdg, country_map)
    build_india_corridor_outputs(sdg, codes)
    build_worker_productivity_outputs(country_sdg, country_map)
    build_migration_deaths_outputs(country_sdg, country_map)
    build_refugee_origin_outputs(country_sdg, country_map)
    build_parliament_outputs(country_sdg, country_map)
    build_youth_employment_outputs(country_sdg, country_map)
    build_biodiversity_planning_outputs(sdg, country_sdg, codes, country_map)
    build_forest_peer_outputs(country_sdg, country_map)


if __name__ == "__main__":
    main()
