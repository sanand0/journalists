# Verification SOP — 9 in 10 Indians want a family doctor. Barely 1 in 35 has one. (Card 03)

## What this card is saying

**87.1%** of survey respondents (43,197 of 49,623 valid responses) agree they want a dedicated family doctor as their primary first contact for health care. In practice, only **2.8%** of outpatient visits were to an ASHA/community worker — the closest proxy for a designated first-contact provider. The gap is 84 percentage points.

## Source fields

| Variable | Description |
|---|---|
| `d1a` | Want dedicated family doctor as first contact (1=Yes, 2=No, 3=Can't say, 88=DNA) |
| `d1b` | Want ASHA/community worker for regular home visits (same coding) |
| `d1c` | Want same facility for all health needs (same coding) |
| `d1d` | Satisfied with current primary care access (same coding) |
| `b1_most` | Actual most-used outpatient provider (1=ASHA) |

Valid base for d1a: excludes `d1a=88` (DNA). Denominator = rows with d1a ∈ {1,2,3}.

## Verified numbers

From `02_verify_cards.py` — all checks pass against the raw parquet.

**Primary care preference cascade (raw d1a–d1d counts):**

| Statement | % Agree | n valid |
|---|---:|---:|
| Want dedicated family doctor (d1a=1) | **87.1%** | 49,623 |
| Want ASHA home visits (d1b=1) | **82.2%** | 49,334 |
| Want same facility for all needs (d1c=1) | **80.3%** | 49,545 |
| Satisfied with current access (d1d=1) | **58.7%** | 49,202 |

**d1a raw breakdown:**

| d1a value | Meaning | Count |
|---|---|---:|
| 1 | Yes / Agree | 43,197 |
| 2 | No | 5,150 |
| 3 | Can't say | 1,276 |
| 88 | DNA (excluded) | 377 |

Denominator: 43,197 + 5,150 + 1,276 = **49,623**
Want % = 43,197 / 49,623 = **87.1%**

**Actual ASHA use:** rows where `b1_most=1` / total OP rows (41,659) = **2.76% ≈ 2.8%**

## Card text → source check

| Displayed | Source value | Note |
|---|---|---|
| "87%" want family doctor | 87.1% | From d1a raw count |
| "9 in 10" | 87.1% | Rounded up to 9/10 |
| "1 in 35" has one | 1/2.8% = 1/35.7 | Exact match |
| 82% want ASHA home visits | 82.2% | d1b |
| 80% want same facility | 80.3% | d1c |
| 58.7% satisfied | 58.7% | d1d |

## Caveat

"Want family doctor" (d1a) measures stated preference across all 50,217 respondents. "Actual ASHA use" (b1_most=1) measures revealed behaviour for a specific outpatient episode among 41,659 outpatient respondents. These are different denominators and different question types; the 84pp gap is directionally real but not a like-for-like comparison.

The satisfaction paradox (58.7% satisfied yet 87.1% want more) reflects low baseline expectations: India's patients benchmark against what they know, not what is possible.

## Common ways to mis-verify

- Using a report-level weighted figure (e.g. 89.3%) instead of the raw `d1a` count — the card uses the raw count (87.1%)
- Including `d1a=88` (DNA) in the denominator — these must be excluded
- Confusing `d1d` (satisfaction) with `d1a` (family doctor want) — they have different base n

## Pre-publication checklist

- [ ] Confirm d1a: 43,197 agree out of 49,623 valid = 87.1%
- [ ] Confirm d1b = 82.2%, d1c = 80.3%, d1d = 58.7%
- [ ] Confirm actual ASHA provider use = 2.76% ≈ 2.8% (b1_most=1 / n=41,659)
- [ ] Confirm "1 in 35" = 1/35.7 (from 2.8%)
- [ ] Note that want/have comparison is stated vs revealed preference, not identical metrics
- [ ] Note denominator difference: d1a uses all 49,623; ASHA use uses 41,659 OP respondents
