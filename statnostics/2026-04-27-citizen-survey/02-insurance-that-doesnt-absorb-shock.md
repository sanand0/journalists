# Verification SOP — Your insurance card won't save you at a private hospital (Card 02)

## What this card is saying

Among inpatient cases at private hospitals, **59.2% of insured patients** still faced catastrophic health spending (bill > 1 month of household food spend). Among uninsured patients at private hospitals, that rises to **77.6%**. The median bill for uninsured private-hospital patients equals **2.67 months of food**; for insured it is **1.43 months**. The government hospital median is just **0.16 months**. Overall, **only 27%** of respondents have any health insurance.

## Source fields

| Variable | Description |
|---|---|
| `c1_most` | Most-used inpatient provider (3=Govt Hospital, 5=Private Hospital) |
| `oope_total_ip` | Total inpatient out-of-pocket expenditure |
| `a2g_food` | Monthly household food expenditure |
| `c10a` | Govt insurance scheme (1=Yes) |
| `c10b` | Employer insurance (1=Yes) |
| `c10d` | State-specific scheme (1=Yes) |
| `c10e` | Other private insurance (1=Yes) |

**CRITICAL:** `c1_most` inpatient codes differ from outpatient `b1_most` codes. Govt Hospital = **3** (not 5), Private Hospital = **5** (not 7).

**Insurance coding:** Any respondent with `c10a=1` OR `c10b=1` OR `c10d=1` OR `c10e=1` is classified as insured.

**Months-of-food ratio:** `oope_total_ip / a2g_food` — computed per row; cases where `a2g_food` is zero or missing are excluded.

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
| Govt Hospital 0.16 months | 0.161538 | Rounded to 2 d.p. |
| Pvt Hospital All 2.32 months | 2.323810 | Exact |
| Pvt Hospital Insured 1.43 months | 1.433333 | Exact |
| Pvt Hospital Uninsured 2.67 months | 2.666667 | Exact |
| "3 in 5 insured face catastrophic spend" | 58.0% | 58 ≈ 3 in 5 |
| "43% exceed 3 months" | 43.2% | Private hospital All |
| "27% insured" | 27.0% | Any scheme |

## Common ways to mis-verify

- Using wrong `c1_most` codes: Govt Hospital is **3**, Private Hospital is **5**. If you use 5 for Govt and 7 for Private (the `b1_most` outpatient codes), you will swap the rows and get inverted medians.
- This card is based on **ratios of inpatient OOPE to the same household's monthly food spend**, not on the WHO 10%-of-household-consumption catastrophic threshold.
- Insurance is coded as **any** scheme — not limited to one scheme type or government schemes only.
- `oope_total_ip` is total inpatient out-of-pocket costs; cases where food spend is zero or missing are excluded from ratio computation.

## Pre-publication checklist

- [ ] Confirm `c1_most` codes: Govt=3, Private=5 (not the outpatient codes)
- [ ] Confirm private-hospital All median months food = 2.32
- [ ] Confirm govt-hospital All median months food = 0.16
- [ ] Confirm insured private-hospital median months = 1.43
- [ ] Confirm uninsured private-hospital median months = 2.67
- [ ] Confirm insured catastrophic (>1 month food) = 58.0%
- [ ] Confirm private-hospital pct > 3 months = 43.2%
- [ ] Confirm overall insurance coverage = 27.0%
- [ ] Note: insurance definition is "any scheme" — not disaggregated by benefit cap or scheme type
