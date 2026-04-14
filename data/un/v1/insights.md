# UN data: v1 insights

Reproduce from the raw local slices:

```bash
uv run v1/build_metadata.py
uv run v1/analyze_un_data.py
```

All supporting tables below live in `v1/outputs/`.

## 1. The UN's remittance-cost goal is still basically unmet

In the 2025 `SI_RMT_COST` slice, the median reported cost of sending `$200` was **5.83%** across **96** reporting countries and territories. Only **3** were already at or below the SDG target of **3%**: **Pakistan (2.74%)**, **Croatia (2.96%)**, and **Tajikistan (2.99%)**. At the other end, **Malawi** was at **31.48%**.

Why this is strong: it has a built-in pass/fail line that a lay reader understands immediately, and almost everyone is still on the wrong side of it.

Caveat: this is only the set of reporting countries and territories present in the local slice, not all UN members.

Files: `outputs/remittance_cost_summary.csv`, `outputs/remittance_cost_country_rank.csv`

## 2. Biodiversity Target 14 is moving, but mostly not fast enough

The 2026 world roll-up for `ER_BDY_KMGBFT14` covers **195** reporting countries. **158** say they have a national target aligned with Kunming-Montreal Global Biodiversity Framework Target 14, but only **50** say it is already achieved. **63** say progress exists but is **insufficient**, **41** say progress is **unknown**, and **37** still report **no aligned target at all**.

The simple headline is not "nothing is happening." It is "a lot of countries can say they have a target, but only about **1 in 4** reporting countries say they have actually achieved it."

Caveat: the headline counts come from the dataset's own `World` aggregate row. The per-area table in this repo filters out aggregates and ends up with **194** reporting country-like areas.

Files: `outputs/target14_status_summary.csv`, `outputs/target14_country_status.csv`

## 3. Some of the world's most gender-balanced parliaments are still old parliaments

Across **156** countries and territories with complete parliament data, the median youth representation ratio was **0.65**. In plain English: under-45 lawmakers hold only about **two-thirds** of the seats their population share would imply. Only **21** countries reached youth parity or better.

The niche, surprising twist is what happens inside already gender-balanced legislatures. Among the **14** parliaments where women hold at least **45%** of seats, **3** still give younger politicians less than half the representation their population share would imply:

- **Nicaragua**: **54.95%** women, youth ratio **0.22**
- **United Arab Emirates**: **50.0%** women, youth ratio **0.30**
- **Iceland**: **46.03%** women, youth ratio **0.49**

Why this is strong: it is a clean "progress on one representation axis does not guarantee progress on another" story.

Caveat: the youth indicator uses an under-45 band where available, with under-40 as fallback in some countries.

Files: `outputs/parliament_summary.csv`, `outputs/parliament_high_female_low_youth.csv`, `outputs/parliament_representation_country_rank.csv`

## 4. Ukraine now sits above Afghanistan in refugee-origin pressure

In `SM_POP_REFG_OR`, **7** reporting countries and territories were above **10,000 refugees per 100,000 people**. **Ukraine** ranked **6th** at **11,969.7**, which puts it above **Afghanistan** at **9,819.5**.

The top tier in this local slice was:

1. Western Sahara - **22,512.5**
2. Venezuela - **18,468.6**
3. Syrian Arab Republic - **17,632.5**
4. South Sudan - **16,351.8**
5. Eritrea - **13,441.9**
6. Ukraine - **11,969.7**
7. Central African Republic - **11,025.1**
8. Afghanistan - **9,819.5**

Why this is strong: Ukraine is now in the dataset's highest-displacement tier on a per-capita basis, not just as a large absolute crisis.

Caveat: this is a per-capita measure, so territories and smaller-population places can move sharply up the ranking.

Files: `outputs/refugee_origin_summary.csv`, `outputs/refugee_origin_country_rank.csv`

## 5. Youth employment policy is often written down, but not operational

In `SL_CPA_YEMP`, only **72** of **185** reporting countries had a fully operationalized national youth employment strategy. Another **67** had a strategy that existed but was **not operational**, **40** were still **developing** one, and **6** reported **no strategy**.

Why this is interesting: the bottleneck here looks less like awareness and more like execution.

Caveat: this is a policy-readiness score, not a direct measure of youth labor-market outcomes.

Files: `outputs/youth_employment_strategy_summary.csv`, `outputs/youth_employment_strategy_scores.csv`
