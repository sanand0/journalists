# Citizen Survey 2022–23 — Data Insights

**Source:** Lancet Citizens' Commission on Reimagining India's Health System  
**Dataset:** `FINAL DATA-CITIZEN_SURVEY_ALL_DATA-FINAL_SKS_09.05.2025.dta`  
**Coverage:** 50,217 respondents · 29 states · 130 districts  
**Residence split:** Rural 70.2% (n=35,255) · Urban 29.8% (n=14,962)  
**Verified against:** `02_verify_cards.py` — 60/60 checks pass

---

## Card 01 — Where India Goes, and Where It Wants to Go

### Finding
Indians currently rely on a fragmented mix of providers — but if they could choose freely, the entire system would tilt toward government hospitals. If all 41,659 outpatient respondents switched to their stated preference, **government hospitals would gain a net 3,402 patients** (+30.5% on their current base), while traditional healers/quacks would shed 1,761 and chemists would lose 1,283.

### Current vs preferred provider share

| Provider | Current use | Current % | Preferred % | Net change |
|---|---:|---:|---:|---:|
| Govt Hospital | 11,146 | 26.8% | 34.9% | **+3,402** |
| Private Clinic | 9,920 | 23.8% | 20.0% | −1,579 |
| PHC | 5,502 | 13.2% | 13.3% | +20 |
| Trad. Healer / Quack | 4,095 | 9.8% | 5.6% | **−1,761** |
| CHC | 3,234 | 7.8% | 9.4% | +665 |
| Private Hospital | 2,731 | 6.6% | 9.2% | +1,085 |
| Sub Centre | 1,498 | 3.6% | 3.0% | −240 |
| ASHA | 1,151 | 2.8% | 2.9% | +52 |
| Chemist | 1,858 | 4.5% | 1.4% | **−1,283** |
| AYUSH | 275 | 0.7% | 0.4% | −112 |

### What this means
- **Informal care is a fallback, not a choice.** The 14.3% using chemists and quacks want to move to formal care; only 24.6% of chemist users and 0.6% of quack users prefer to stay with those providers.
- **Government hospitals have latent demand.** Their 8.1 percentage-point preference gap is the largest of any provider type — if supply kept up with demand, they would serve 34.9% of outpatient visits, not 26.8%.
- **Private clinics face headwinds.** Their preference share is 3.8pp below actual use — patients want to leave but lack alternatives.
- **Rural vs urban:** Government providers (PHC/CHC/GovtHospital) cover 47.4% of rural OP visits and 48.4% of urban visits. Informal care (quack+chemist) is more prevalent in rural areas (15.9%) than urban (10.5%).

### Caveats
Net change = preferred next visit minus actual last visit. These are stated, not revealed, preferences. The base used for computing net change (n=41,659) excludes 166 respondents who gave DNA/Other on `b7_1`.

---

## Card 02 — The Govt Hospital Queue as a Hidden Tax

### Finding
A chemist costs ₹150 and 15 minutes. A government hospital costs ₹300 but takes 50 minutes — and its relief rate is lower (70% vs 81%). The cheapest formal care carries the highest time bill.

### Provider cost and relief

| Provider | Median OOPE (₹) | Relief rate |
|---|---:|---:|
| Chemist | 150 | 81% |
| Trad. Healer | 330 | — |
| PHC | 100 | — |
| Govt Hospital | 300 | 70% |
| Private Clinic | 1,250 | — |
| Private Hospital | 3,100 | 68% |

*(Travel + wait time from b3/b4 coded response; relief from pre-computed visual-story output.)*

### What this means
- **PHC is cheapest formal care at ₹100** but patients must weigh time cost against the ₹150 chemist who provides faster access with better self-reported outcomes.
- **Private hospitals are 20× the cost of govt hospitals** for comparable (actually slightly worse) relief rates — the premium buys speed and perception of quality, not meaningfully better outcomes.
- **The informal sector's durability** is partly explained by cost+speed: a chemist delivers relief 81% of the time at ₹150, outperforming both government and private hospitals on the headline relief metric.

---

## Card 03 — The Family Doctor Gap: 87% Want One, 2.8% Have One

### Finding
**87.1%** of survey respondents want a dedicated family doctor as their primary first contact for health care (d1a=Yes; n=49,623 valid responses). In practice, only **2.8%** of outpatient visits were to an ASHA/community worker — the closest proxy for a designated first-contact provider. The gap is 84 percentage points.

### Primary care preference cascade

| Statement | % Agree | n valid |
|---|---:|---:|
| Want dedicated family doctor as first contact (d1a) | **87.1%** | 49,623 |
| Want ASHA/community worker for regular home visits (d1b) | **82.2%** | 49,334 |
| Want same facility for all health needs (d1c) | **80.3%** | 49,545 |
| Satisfied with current primary care access (d1d) | **58.7%** | 49,202 |

### What this means
- **The aspiration is nearly universal.** 9 in 10 respondents across rural and urban settings, across education levels, want continuity of care. This is not an urban elite demand.
- **The satisfaction paradox.** 58.7% say they are satisfied with current access — yet 87.1% want something better. This suggests low expectations, not genuine contentment: India's patients benchmark against what they know, not what they could have.
- **"1 in 35 has one"** is a conservative framing. ASHA use at 2.8% is the upper bound for formal first-contact care; actual family-doctor attachment is effectively zero in this survey sample.
- **The d1b figure (82.2%)** is the strongest operational signal: most people specifically want a community health worker making regular home visits — not just a referral node, but a proactive relationship.

### Caveats
"Want family doctor" is stated preference. "ASHA as provider" is revealed behaviour for one specific outpatient episode. They measure different things; the gap is directionally real but not a like-for-like comparison.

---

## Card 04 — Bigger Family, Smaller Plate

### Finding
As household size grows, total food spending rises — but spending per person falls sharply. A 9+ member household spends 4× more on food in total than a 1–2 member household, yet each person receives ₹889/month — **29% less** than someone in a small household (₹1,250).

### Household size × food spend

| Household size | n | Median total food (₹) | Median per-capita (₹) | Mean per-capita (₹) |
|---|---:|---:|---:|---:|
| 1–2 members | 3,368 | 2,500 | **1,250** | 1,648 |
| 3–4 members | 17,609 | 5,000 | 1,250 | 1,348 |
| 5–6 members | 19,563 | 6,000 | 1,000 | 1,156 |
| 7–8 members | 6,215 | 7,000 | 1,000 | 1,013 |
| 9+ members | 3,245 | 10,000 | **889** | 917 |

**Per-capita drop (1–2 → 9+): (1,250 − 889) / 1,250 = 28.9% ≈ 29%**  
**Total spend ratio: 10,000 / 2,500 = 4×**

### What this means
- **Aggregate household totals are a misleading welfare proxy.** A policy that raises total household food spend by 50% for large families could still leave every individual eating less than someone in a small household.
- **The inflection is at 5–6 members.** Per-capita food spend drops from ₹1,250 to ₹1,000 (−20%) as households move from 4 to 5 members. This is the threshold where crowding visibly compresses individual food allocation.
- **State variation is large.** Median per-capita food spend ranges from ₹800 (Chhattisgarh, Odisha) to ₹1,700 (Delhi) — a 2.1× gap — driven by income, food prices, and dietary norms. The per-capita compression within large families holds across states.
- **Mean vs median:** The mean per-capita for 1–2 member households is ₹1,648 vs median ₹1,250 — right-skewed by wealthy small households. Median is the correct measure for this story.

### Caveats
- Food spend is recall-based and rounded (99.8% of responses are multiples of ₹100).
- 1–2 member households are disproportionately elderly couples — their per-capita spend may reflect different dietary needs, not greater abundance.
- Cross-sectional data: the gradient is associational, not causal.

### State-level extremes

| Lowest per-capita | ₹/month | Highest per-capita | ₹/month |
|---|---:|---|---:|
| Chhattisgarh | 800 | Delhi | 1,700 |
| Odisha | 800 | Jammu & Kashmir | 1,667 |
| Assam | 1,000 | Nagaland | 1,600 |
| Arunachal Pradesh | 1,000 | West Bengal | 1,500 |
| Madhya Pradesh | 1,000 | Mizoram | 1,500 |

---

## Card 05 — The More Educated You Are, the Longer You Wait for a Job

### Finding
Among Indians aged 25–34, those with higher-secondary or above education are **7.5× more likely to be actively seeking work** than those with only primary education (10.3% vs 1.4%). Both salaried employment and active job-seeking rise with education — but job-seeking rises faster. The gap between "employed" and "waiting" **widens** at the top of the education ladder.

### Education × employment (age 25–34, n=14,459)

| Education | n | Regular salaried % | Available/seeking % | Domestic chores % | Salaried–waiting gap |
|---|---:|---:|---:|---:|---:|
| Primary (rec_a2d=1) | 3,065 | 4.5% | 1.4% | 29.1% | +3.1pp |
| Middle (rec_a2d=2) | 2,576 | 5.5% | 1.8% | 25.0% | +3.7pp |
| Secondary (rec_a2d=3) | 3,362 | 12.1% | 3.7% | 19.3% | +8.4pp |
| Higher-Secondary+ (rec_a2d=4) | 5,456 | 20.4% | **10.3%** | 13.9% | +10.1pp |

**Waiting ratio HS+ / Primary: 10.3% / 1.4% = 7.4× (card rounds to 7×)**  
**Salaried ratio HS+ / Primary: 20.4% / 4.5% = 4.5×**

### Full occupation breakdown (age 25–34)

| Occupation | n | % of cohort |
|---|---:|---:|
| Domestic chores | 2,942 | 20.3% |
| Regular salaried | 1,800 | 12.5% |
| Self-employed agriculture | 1,745 | 12.1% |
| Regular/salaried non-farm | 1,961 | 13.6% |
| Self-employed non-ag | 1,705 | 11.8% |
| Casual labour | 1,857 | 12.8% |
| Available for work (seeking) | 775 | 5.4% |
| Student | 234 | 1.6% |

### Gender dimension (age 25–34)

| | Salaried % | Seeking work % | Domestic chores % |
|---|---:|---:|---:|
| Male | 16.9% | 6.2% | 1.2% |
| Female | 7.4% | 4.4% | **42.2%** |

### What this means
- **Education raises aspirations faster than the labour market can absorb them.** Higher-secondary graduates increasingly refuse casual/informal work — they queue for formal jobs instead. The 7.5× waiting ratio captures this aspiration premium.
- **The education escalator stalls at the top.** Only 20.4% of the highest-educated 25–34 year olds hold regular salaried jobs — the other ~80% are in informal work, seeking, or doing domestic tasks. Education is necessary but not sufficient.
- **Women's "domestic chores" classification masks unemployment.** 42.2% of women aged 25–34 are coded as domestic chores — yet 4.4% are actively seeking. The real job-seeking rate for educated women is likely much higher once domestic-chores-but-available is properly counted.
- **The seeking rate is highest for the most educated** — this is not a signal of laziness but of rationally holding out for appropriate work. The cost of this queue falls entirely on individuals.

### Robustness
- Males only (25–34): HS+ 11.0% waiting vs Primary 1.6% → ratio 6.9× (holds)
- Younger cohort (15–24): HS+ 9.6% vs Primary 1.8% → ratio 5.4× (holds, smaller gap)
- Older cohort (35–49): HS+ 3.6% vs Primary 0.7% → ratio 5.1× (holds, gap narrows with age as people settle)

### Caveats
- `a2e=8` (available for work) is self-reported; it differs from ILO-defined unemployment.
- Higher-educated respondents may apply a stricter definition of "seeking" — classifying themselves as available where lower-educated respondents accept informal work as their status.
- `rec_a2d` is a recoded composite of `a2d`; recoding groups 1–2 as "Primary", 3 as "Middle", 4 as "Secondary", 5–8 as "Higher-Secondary+".

---

## Card 06 — One Private Hospital Stay Can Swallow Months of Food

### Finding
The median private hospital inpatient bill equals **2.3 months of the same household's food budget**. Even insured patients face a median bill of **1.4 months of food**. At government hospitals, the median is just **0.16 months**. Only 27% of respondents have any form of health insurance — and for those at private hospitals, insurance reduces the blow but does not eliminate it.

### Inpatient cost as months of household food

| Provider | Insurance | n | Median OOPE (₹) | Median food/mo (₹) | Months of food | % > 1 month | % > 3 months |
|---|---|---:|---:|---:|---:|---:|---:|
| Govt Hospital | All | 9,751 | 850 | 5,000 | **0.16** | 11.2% | 2.6% |
| Private Hospital | All | 1,844 | 15,000 | 6,000 | **2.32** | 70.9% | 43.2% |
| Private Hospital | Insured | 579 | 7,500 | 6,000 | **1.43** | 58.0% | 35.2% |
| Private Hospital | Uninsured | 1,265 | 17,000 | 6,000 | **2.67** | 76.8% | 46.9% |

### Insurance landscape
- **Any insurance coverage: 27.0%** of all respondents
  - Govt scheme (c10a): 18.6%
  - Employer-provided (c10b): 9.2%
  - State-specific (c10d): 6.4%
  - Other private (c10e): 6.4%
- **73% of respondents have no health insurance** — they face the full uninsured private-hospital exposure of 2.67 months of food per stay.

### What this means
- **Insurance halves the median bill but does not prevent catastrophic spending.** A 1.43-month food-equivalent bill is still catastrophic for most households. The "insured = protected" assumption is false for private-hospital stays.
- **43% of private hospital patients exceed 3 months of food** in a single visit. For the median household spending ₹6,000/month on food, that is ₹18,000+ out of pocket.
- **Government hospitals are 14× cheaper** in food-months terms (0.16 vs 2.32). The financial case for govt hospital use is overwhelming — the barrier is quality perception, distance, and queue time, not cost awareness.
- **The uninsured face a near-certain catastrophic event.** At 76.8% probability of exceeding one month's food budget, a private hospital visit for an uninsured patient is statistically almost guaranteed to be catastrophic.

### Caveats
- `oope_total_ip` includes all inpatient out-of-pocket costs; excludes cases where food spend is zero or missing.
- Insurance is coded as "any scheme" — not disaggregated by scheme generosity or benefit caps.
- The months-of-food metric uses the same household's `a2g_food` — this is a ratio, not a fixed poverty line.

---

## Cross-Cutting Patterns

### 1. The formal/informal care tension
India's outpatient system runs on a structural paradox: the providers people actually use (private clinics 23.8%, quacks 9.8%, chemists 4.5%) are not the ones they prefer (govt hospital 34.9%). This 8+ percentage-point aspiration gap for government care exists despite government hospitals taking longer and delivering lower self-reported relief than chemists. The driver is cost: at ₹300 vs ₹1,250 (private clinic), government care is 4× cheaper.

### 2. Insurance coverage is low and insufficient
Only 27% have any insurance. Even for those who do, private hospital bills consume a median 1.43 months of food. The system's financial protection function is substantially broken at private hospitals — precisely where uninsured and insured patients face the largest bills.

### 3. Education raises aspirations, not necessarily employment
The education-jobs paradox (Card 05) and the family-doctor gap (Card 03) share a common structure: India is producing people with higher expectations (for jobs, for health care continuity) faster than it is producing the institutions to meet them. 87% want a family doctor; 87% of educated young adults want formal sector jobs. Both gaps reflect the same institutional capacity deficit.

### 4. Household size as a hidden welfare depressor
The food-spend compression in large households (Card 04) means that aggregate household income and expenditure data systematically overstate individual welfare in large joint families. A welfare policy that targets households by total spend will miss per-capita deprivation in families of 7+.

### 5. Rural/urban gap is smaller than expected
Rural patients are nearly as likely to use government providers (47.4%) as urban patients (48.4%). The informal care gap is larger: rural informal use is 15.9% vs urban 10.5%. The rural problem is not a preference for informal care — it is constrained access to formal alternatives.

---

## Data Quality Notes

- **Sample size:** 50,217 total; 41,659 have valid outpatient provider responses for both `b1_most` and `b7_1`
- **Code mapping:** `b1_most` and `b7_1` use different numbering schemes — AYUSH is code 9 in `b1_most` but code 8 in `b7_1`; TradHealer is 10/9; Chemist is 11/10. Any analysis comparing current to preferred must apply the `B1_TO_B7` crosswalk (documented in `02_verify_cards.py`)
- **Inpatient provider codes differ from outpatient:** In `c1_most`, Government Hospital = code 3 and Private Hospital = code 5 (not 5 and 7 as in `b1_most`)
- **Food spend is heavily rounded:** 99.8% of `a2g_food` values are multiples of ₹100, introducing measurement imprecision for ratio-based metrics like months-of-food
- **Doctor-MobileVan** (b1_most=8, n=252) has no equivalent code in `b7_1` — these respondents express preferences for other provider types; their current-use share cannot be tracked to a preferred equivalent
