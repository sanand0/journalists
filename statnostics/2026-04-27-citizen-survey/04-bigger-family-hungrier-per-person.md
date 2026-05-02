# Verification SOP — Bigger family, smaller plate (Card 04)

## What this card is saying

As household size grows, total food spending rises — but per-person food spending **falls**. A household of 9+ members spends a median of ₹10,000/month on food (4× more than a 1–2 member household's ₹2,500), yet each individual gets only ₹889/month — **29% less** per person than someone in a small household (₹1,250). Aggregate household spending obscures per-capita deprivation.

## Source fields

| Variable | Description |
|---|---|
| `a2g_food` | Monthly household food expenditure (₹) |
| `a2f` | Household size (number of members) |
| Per-capita = `a2g_food / a2f` | Derived field |

Household size groups from `a2f`:
- 1–2: `a2f` ∈ {1, 2}
- 3–4: `a2f` ∈ {3, 4}
- 5–6: `a2f` ∈ {5, 6}
- 7–8: `a2f` ∈ {7, 8}
- 9+: `a2f` ≥ 9

## Verified source table

From `02_verify_cards.py` — all checks pass against the raw parquet.

| Household size | n | Median total food (₹) | Median per-capita (₹) | Mean per-capita (₹) |
|---|---:|---:|---:|---:|
| 1–2 | 3,368 | 2,500 | **1,250** | 1,648 |
| 3–4 | 17,609 | 5,000 | 1,250 | 1,348 |
| 5–6 | 19,563 | 6,000 | 1,000 | 1,156 |
| 7–8 | 6,215 | 7,000 | 1,000 | 1,013 |
| 9+ | 3,245 | 10,000 | **889** | 917 |

## Derived numbers on card

- Per-capita drop from 1–2 to 9+: (1,250 − 889) / 1,250 = **28.9% → rounded to 29%**
- Total spend ratio: 10,000 / 2,500 = **4×**
- Inflection point: per-capita drops from ₹1,250 to ₹1,000 (−20%) at the 4→5 member transition

## State-level extremes (median per-capita food)

| Lowest | ₹/mo | Highest | ₹/mo |
|---|---:|---|---:|
| Chhattisgarh | 800 | Delhi | 1,700 |
| Odisha | 800 | Jammu & Kashmir | 1,667 |
| Assam | 1,000 | Nagaland | 1,600 |

## Card text → source check

| Displayed | Source value | Note |
|---|---|---|
| 1–2 member median per-capita = ₹1,250 | 1,250.0 | Exact |
| 9+ member median per-capita = ₹889 | 889.0 | Exact |
| 9+ total food = ₹10,000 | 10,000.0 | Exact |
| 1–2 total food = ₹2,500 | 2,500.0 | Exact |
| 29% drop | 28.9% | Rounded to whole number |
| 4× total spend ratio | 4.0 | Exact |

## Common ways to mis-verify

- Using **mean** per-capita instead of **median** — the mean for 1–2 member households is ₹1,648, not ₹1,250 (right-skewed by wealthy small households)
- Grouping `a2f ≥ 9` incorrectly — the 9+ group requires `a2f >= 9`, not `a2f > 9`
- Using total household food spend (not per-capita) to compare groups — this always rises with household size and obscures the per-person compression

## Caveats

- Household food spend is **recall-based** and rounded (99.8% of responses are multiples of ₹100)
- The 1–2 member group is disproportionately elderly households with no children; their per-capita food spend may reflect different dietary needs, not greater abundance
- This is cross-sectional; we cannot infer that adding a family member causes per-capita food to drop

## Pre-publication checklist

- [ ] Confirm 1–2 member median per-capita food = ₹1,250 (from `a2g_food / a2f`, median)
- [ ] Confirm 9+ member median per-capita food = ₹889
- [ ] Confirm 9+ total food = ₹10,000
- [ ] Confirm 1–2 total food = ₹2,500
- [ ] Confirm drop = (1250−889)/1250 = 28.9% ≈ 29%
- [ ] Confirm mean vs median difference is understood (use median for headline)
- [ ] Note caveat on household composition (elderly vs large joint families)
