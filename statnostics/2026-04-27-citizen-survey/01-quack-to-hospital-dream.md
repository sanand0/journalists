# Verification SOP — 1 in 7 Indians visits a quack or chemist — but wants a real hospital (Card 01)

## What this card is saying

Among outpatient respondents with valid provider responses on both current and preferred visit (n=41,659), those currently visiting traditional healers/quacks (n=4,095) and chemists (n=1,858) overwhelmingly prefer a government hospital for their **next** visit. If everyone switched to their stated preference, government hospitals would gain a net **+3,402 patients**, traditional healers would lose **−1,761**, and chemists would lose **−1,283**.

## Source fields

| Variable | Description | Location |
|---|---|---|
| `b1_most` | Actual provider for most recent outpatient visit | raw parquet / `citizen_survey_2025.xlsx` → sheet `Data` |
| `b7_1` | Preferred provider for next outpatient visit | same |

Provider code crosswalk (CRITICAL — `b1_most` and `b7_1` use different numbering):

| b1_most code | Provider | b7_1 code |
|---|---|---|
| 1 | ASHA | 1 |
| 2 | Sub Centre | 2 |
| 3 | PHC | 3 |
| 4 | CHC | 4 |
| 5 | Govt Hospital | 5 |
| 6 | Private Clinic | 6 |
| 7 | Private Hospital | 7 |
| 8 | Doctor-MobileVan | (no equivalent in b7_1) |
| 9 | AYUSH | 8 |
| 10 | Trad. Healer / Quack | 9 |
| 11 | Chemist | 10 |

## Verified source table

From `02_verify_cards.py` — all checks pass against the raw parquet.

Valid analysis base: rows where **both** `b1_most` ∈ {1–11} and `b7_1` ∈ {1–10} → **n=41,659**
(Excludes 165 DNA / Other responses on `b7_1` and 1 invalid on `b1_most`.)

| Provider | Current n | Preferred n | Net change |
|---|---:|---:|---:|
| Govt Hospital | 11,146 | 14,548 | **+3,402** |
| Private Clinic | 9,920 | 8,341 | −1,579 |
| PHC | 5,502 | 5,522 | +20 |
| Trad. Healer / Quack | 4,095 | 2,334 | **−1,761** |
| CHC | 3,234 | 3,899 | +665 |
| Private Hospital | 2,731 | 3,816 | +1,085 |
| Sub Centre | 1,498 | 1,258 | −240 |
| ASHA | 1,151 | 1,203 | +52 |
| Chemist | 1,858 | 575 | **−1,283** |
| AYUSH | 275 | 163 | −112 |

## Card text → source check

| Displayed | Source value | Note |
|---|---|---|
| "1 in 7 visits quack or chemist" | (4,095+1,858)/41,659 = **14.3%** | ~1-in-7; avoid rounding to "1 in 4" |
| +3,402 net to Govt Hospital | 3,402 | Exact |
| −1,761 Trad. Healer | 1,761 | Exact |
| −1,283 Chemist | 1,283 | Exact |
| Rural informal use | 15.9% | From `insights.md` |
| Urban informal use | 10.5% | From `insights.md` |

**Important:** The headline "1 in 7" (14.3%) is the correct figure for chemist + quack combined. Do **not** round this to "1 in 4" (25%) — that would overstate informal care use by ~10 percentage points.

## Common ways to mis-verify

- Using all OP rows (n=41,825) as the denominator — net-change computation must use only rows where BOTH `b1_most` and `b7_1` are valid (n=41,659)
- Comparing `b1_most=10` (TradHealer) against `b7_1=10` (which is actually Chemist in b7_1 numbering) — must apply the B1_TO_B7 crosswalk
- `b1_most` captures the single most-used outpatient provider; `b1_all_*` captures all providers used
- "Preferred next" is stated preference only — not observed behaviour

## Pre-publication checklist

- [ ] Confirm valid analysis base n = 41,659 (not 41,825)
- [ ] Confirm Govt Hospital net = +3,402
- [ ] Confirm Trad. Healer / Quack net = −1,761
- [ ] Confirm Chemist net = −1,283
- [ ] Confirm informal-care share (quack+chemist) = 14.3% ≈ 1 in 7 (not "1 in 4")
- [ ] Note to editor: rural informal use 15.9% vs urban 10.5%
- [ ] Confirm b1_most/b7_1 crosswalk was applied (AYUSH: 9→8, TradHealer: 10→9, Chemist: 11→10)
