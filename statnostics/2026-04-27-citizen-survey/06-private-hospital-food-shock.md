# Verification SOP — One private hospital stay can swallow months of food (Card 06)

## What this card is saying

Among inpatient cases with both hospitalisation spending and monthly food spending reported, the **median private-hospital out-of-pocket bill equals 2.32 months of food**. The median at a government hospital is just **0.16 months**. Even among **insured** private-hospital patients, the median still comes to **1.43 months** of food. Overall, **43.2%** of private-hospital cases exceed three monthly food budgets, and only **27%** of respondents have any health insurance.

## Source fields

| Variable | Description |
|---|---|
| `c1_most` | Most-used inpatient provider (**3**=Govt Hospital, **5**=Private Hospital) |
| `oope_total_ip` | Total inpatient out-of-pocket expenditure (₹) |
| `a2g_food` | Monthly household food expenditure (₹) |
| `c10a` | Govt insurance scheme (1=Yes) |
| `c10b` | Employer insurance (1=Yes) |
| `c10d` | State-specific scheme (1=Yes) |
| `c10e` | Other private insurance (1=Yes) |

**CRITICAL:** `c1_most` inpatient codes differ from outpatient `b1_most`. Govt Hospital = **3**, Private Hospital = **5**. Using the outpatient codes (5 and 7) will swap the rows entirely.

**Months-of-food ratio:** `oope_total_ip / a2g_food` — computed per row. Rows where `a2g_food` is zero or missing are excluded from ratio computation.

**Insurance:** any respondent with `c10a=1` OR `c10b=1` OR `c10d=1` OR `c10e=1`.

## Verified source table

From `02_verify_cards.py` — all checks pass against the raw parquet.

**Inpatient cost as months of household food:**

| Provider | Insurance | n | Median OOPE (₹) | Median food/mo (₹) | Median months food | % > 1 month | % > 3 months |
|---|---|---:|---:|---:|---:|---:|---:|
| Govt Hospital | All | 9,751 | 850 | 5,000 | **0.16** | 11.2% | 2.6% |
| Private Hospital | All | 1,844 | 15,000 | 6,000 | **2.32** | 70.9% | 43.2% |
| Private Hospital | Insured | 579 | 7,500 | 6,000 | **1.43** | 58.0% | 35.2% |
| Private Hospital | Uninsured | 1,265 | 17,000 | 6,000 | **2.67** | 76.8% | 46.9% |

**Insurance coverage (all 50,217 respondents):**

| Scheme | Coverage % |
|---|---:|
| Any insurance (c10a/b/d/e) | **27.0%** |
| Govt scheme (c10a) | 18.6% |
| Employer-provided (c10b) | 9.2% |
| State-specific (c10d) | 6.4% |
| Other private (c10e) | 6.4% |

## Card text → source check

| Displayed | Source value | Note |
|---|---|---|
| "2.3 months" (private, all) | 2.323810 | Rounded to 1 d.p. |
| "0.16 months" (govt, all) | 0.161538 | Exact to 2 d.p. |
| "1.4 months even if insured" | 1.433333 | Rounded to 1 d.p. |
| "2.67 months if uninsured" | 2.666667 | Exact |
| "43% exceed 3 months" | 43.2% | Private hospital All |
| "3 in 5 insured face catastrophic" | 58.0% | 58% ≈ 3 in 5 |
| "27% have insurance" | 27.0% | Any scheme |

## Common ways to mis-verify

- Using wrong `c1_most` codes — the most common error. Govt Hospital = **3**, Private Hospital = **5**. If you see a govt-hospital median OOPE of ₹15,000 and private of ₹850, the codes are swapped.
- This card uses a **food-ratio catastrophic threshold** (OOPE > 1× monthly food), not the WHO 10%-of-household-consumption threshold used in other analyses.
- `oope_total_ip` includes all inpatient out-of-pocket costs (medicines, procedures, transport); cases where food spend is zero or missing are excluded.
- Insurance is **any** scheme — not limited to government schemes or validated benefit coverage.

## Pre-publication checklist

- [ ] Confirm `c1_most` coding: Govt=3, Private=5 (check by verifying Govt median OOPE ≈ ₹850, not ₹15,000)
- [ ] Confirm private-hospital All median months food = 2.32
- [ ] Confirm govt-hospital All median months food = 0.16
- [ ] Confirm insured private-hospital median months = 1.43
- [ ] Confirm uninsured private-hospital median months = 2.67
- [ ] Confirm private-hospital pct > 3 months = 43.2%
- [ ] Confirm insured pct > 1 month food = 58.0%
- [ ] Confirm overall insurance coverage = 27.0%
- [ ] Note: "catastrophic" here = OOPE > 1× monthly food spend (not WHO threshold)
- [ ] Note: insurance is "any scheme" — not disaggregated by generosity or benefit cap
