# UN data: v2 notes

## What worked best in v2

- The strongest broadened angles were the ones that translated a technical indicator into a very plain everyday question:
  - **How much money actually reaches a family in India after fees?**
  - **How much more is each worker producing than last year?**
  - **Which migration routes are killing the most people?**
  - **Do youth-jobs plans exist only on paper, or are they actually live?**
- The best India-specific addition was the **corridor-level remittance table into India**. It is much more vivid than the generic global 3% target story.
- The best universal-but-underused addition was **worker productivity growth**. The outside literature talks about a global slowdown, but the local slice makes India's position unusually easy to show.

## What the outside web research suggested

The direct source pages captured in `research/context_sources.csv` helped decide which angles felt familiar and which ones still had room for novelty.

- **Remittances:** UN framing focuses on why lower fees matter for household budgets and notes that cutting average costs to **3%** would save families billions. The local data added the more concrete and more novel angle: **India's corridor spread is huge**.
- **Women in parliament:** UN/IPU coverage emphasizes how slowly women's representation is improving globally. That made the local youth-representation angle more attractive, because it is a cleaner "same topic, fresher cut" story.
- **Migration deaths:** UN safe-migration pages stress that these are the starkest available data on unsafe migration and that they remain **minimum estimates**. The local slice then makes a simple concentration story possible: a handful of reporting areas dominate the death toll.
- **Productivity:** World Bank material stresses that global productivity growth has been slowing for years. That made India's **5.12%** result stand out more, because it is high against a weak global backdrop.

## Data and interpretation quirks

- The SDG `CL_AREA` codelist still mixes countries, territories, and aggregates. I again used the numeric-plus-alpha label twin heuristic to approximate **country-like areas**.
- That heuristic is useful, but it is not perfect. It excludes some reporting areas and still includes some territories. Safer public phrasing is usually **"reporting areas"** or **"countries and territories"**.
- `SM_DTH_MIGR` should be treated as a **minimum documented count**, not a full death toll. The UN safe-migration material explicitly says the underlying Missing Migrants data are minimum estimates.
- `SI_RMT_COST_BC` required decoding: in this slice, `REF_AREA` behaves like the **sending country**, while `CUST_BREAKDOWN` holds the **receiving country** code prefixed with `C`.
- `SI_RMT_COST_SC` contains **negative values** in the local slice. I treated that as a data-quality/definition warning and did not use it in the lay-facing write-up.
- Parliament youth indicators use mixed age bands. I preferred **`Y0T45`** and fell back to **`Y0T40`** only where needed.

## Interesting findings that stayed in the notes

### 1. India and China look strong on reported forest management plans

In `forest_india_peer_comparison.csv`:

- **China** reports **75.86%** of forest area under long-term management plans
- **India** reports **74.76%**
- **Brazil** reports **12.64%**

This is interesting, but it is harder to explain quickly and likely needs external validation before becoming a headline.

### 2. India's outbound remittance picture is also uneven

The local corridor slice includes only two outbound India corridors:

- **India -> Nepal:** **3.14%**
- **India -> Sri Lanka:** **6.84%**

That is a useful follow-up for a more South Asia-specific remittance story.

### 3. Food price anomalies looked promising, but the local slice is messy

`AG_FPA_COMM` has broad coverage and obvious consumer appeal, but it did not make the final cut because:

- the scale is not instantly intuitive for a lay reader,
- some countries appear multiple times even after simple filtering,
- the local slice appears to mix values in ways that need more metadata work before publication.

### 4. Bribery incidence is easy to understand but too thin here

`IC_FRM_BRIB` is one of the most naturally newsworthy labels in the whole slice, but after filtering down to country-like areas there were only **24** usable rows. That felt too thin for a strong v2 headline.

### 5. Internet/mobile and social protection coverage were not usable

- `IT_USE_II99` collapsed to only **10** country-like areas after filtering.
- `IT_MOB_OWN` collapsed to only **5**.
- `SI_COV_BENFTS` had only **2**.

Those numbers are too thin for a safe lay-facing comparison, even though India appears in some of them.

## Additional India and regional observations

- India's average **receiving-country** remittance cost in the local 2025 slice is **5.3%**, below the global median **5.83%**, but still above the UN's **3%** goal.
- India's **worker-productivity growth** is **5.12%**, while **Pakistan** is at **0.26%** and **Bangladesh** at **2.36%** in the same local slice.
- India is below the local medians on both:
  - **women's share in parliament**: **13.84%** vs median **27.68%**
  - **youth representation ratio**: **0.32** vs median **0.65**
- On youth-employment strategy readiness, **India, Pakistan and Indonesia** all sit at **2** ("developed but not operational"), while **Bangladesh, Nepal and Sri Lanka** are still at **1**.

## Repro assets created in v2

- `build_metadata.py` - fetches and parses the SDMX structures and codelists used in the local slices
- `fetch_context.py` - fetches and caches the public context pages used for framing
- `analyze_un_data.py` - rebuilds the v2 output tables under `v2/outputs/`

## Good follow-ups for v3 or later

- Add an explicit sovereign-state filter from an external country list so refugee and migration tables can cleanly exclude territories.
- Deepen the India remittance story with corridor trends over time if more years are downloaded.
- Validate the food-price anomaly series with FAO methodology before using it publicly.
- Pair parliament ratios with external population-age data for a sharper India political-demography story.
- Check whether the forest-management reporting differences still hold when paired with non-UN deforestation or satellite-based forest-loss data.
