# UN data: v1 notes

## What actually worked

- The strongest story leads came from the **SDG Harmonized Global Dataflow**.
- The local Eurostat slices were still useful, but mostly for scoping limits rather than for final layperson-friendly insights.
- The local download set is narrow: **7** observation files total, concentrated in SDG 2025/2026 plus a few Eurostat 2024/2025 slices.

## Method choices

- The SDG `CL_AREA` codelist mixes countries, territories, and regional aggregates. For country-level tables, I treated numeric area codes whose labels also exist with alphabetic twins as **country-like areas**. That removes most roll-ups without hand-curating a sovereign-state list.
- Because of that heuristic, the safest public phrasing is usually **"countries and territories"** or **"reporting areas"** unless using the dataset's own `World` aggregate row.
- For `ER_BDY_KMGBFT14`, I used the dataset's **World aggregate** for the headline counts because it gives the cleanest denominator (**195** reporting countries). The filtered per-area table lands at **194** reporting country-like areas after aggregate removal.
- For youth-parliament analysis, I preferred `Y0T45` and fell back to `Y0T40` where needed. The **ratio** indicator is safer than raw youth seat share because it already adjusts for each country's age structure.

## Data-quality and interpretation quirks

- In the local SDG slice, `REPORTING_TYPE` is always `G`, so it was **not** useful for separating countries from aggregates.
- `SI_RMT_COST_SC` contains **negative values** in the local data. I did not use it for any lay-facing claim without extra validation.
- Several parliament indicators contain `NaN` values for some countries. All published parliament counts use **finite values only**.
- `ER_BDY_KMGBFT14` has both no-breakdown and status-breakdown rows. The no-breakdown `World` value (**158**) matches the sum of **achieved + insufficient + unknown + no significant progress**, which is a useful internal check on the indicator logic.

## Eurostat-specific limits

- `TITLE` and `TITLE_COMPL` were blank in the local Eurostat observation files, so interpretation depended on SDMX codelists rather than ready-made labels.
- Cross-country comparable GDP coverage is thin in the local `NA_MAIN` slice. GDP is mostly in **domestic currency**; GDP in **USD** appears for only **2** geos in chain-linked volume and **1** geo at current prices in the local files.
- The quarterly financial-accounts slice only uses **domestic currency** locally, which makes quick layperson-friendly cross-country comparisons much harder.
- Repro files for this limitation: `outputs/eurostat_na_main_gdp_availability.csv`, `outputs/eurostat_na_main_unit_measures.csv`, `outputs/eurostat_na_sec_unit_measures.csv`

## Interesting but weaker follow-ups

- **Nigeria** is a sharp one-country biodiversity chart: **70.3%** terrestrial KBA coverage versus **0.0%** marine KBA coverage. It is visually striking, but not a broad global pattern in this slice.
- A secondary biodiversity-governance story exists in `ER_IAS_LEGIS` versus `ER_IAS_NBSAP`: all **195** reporting countries say they have invasive-species legislation, but only **139** report aligned biodiversity-plan targets. I did not elevate it because the Target 14 story is stronger and more current.
- The refugee-origin ranking is strong, but small-population territories can dominate the very top. If we want a sovereign-states-only version, add an explicit statehood filter before publishing.
- The youth-employment strategy score is solid, but it is less surprising than the remittance and Target 14 findings.

## Repro assets created in v1

- `build_metadata.py` - fetches and parses the SDMX datastructures and codelists used in the local slices
- `analyze_un_data.py` - rebuilds the output tables under `v1/outputs/`
- `outputs/local_file_inventory.csv` - basic inventory of the downloaded observation files
- `outputs/sdg_series_profile.csv` - broad screening table for the local SDG series
