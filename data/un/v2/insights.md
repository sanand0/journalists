# UN data: v2 insights

Reproduce from the raw local slices:

```bash
uv run v2/build_metadata.py
uv run v2/fetch_context.py
uv run v2/analyze_un_data.py
```

Supporting tables are in `v2/outputs/`. The public context pages used to shape the plain-language framing are listed in `v2/research/context_sources.csv`.

## 1. Sending `$200` to India can cost **$3.82** or **$32.78**, depending on where it comes from

This is the clearest remittance story in the local slice.

The UN's benchmark is simple: sending **`$200`** home should cost no more than **3%**, or about **`$6`** in fees. But India's own average receiving-country cost in the 2025 slice is **5.3%**, which means about **`$10.60`** disappears before the money reaches a household. The global median in this local file is even worse at **5.83%** or **`$11.65`**.

The corridor view is even more striking. In the **20** observed corridors sending money **into India**, the median fee is still **4.12%**, or about **`$8.25`** on a **`$200`** transfer, and only **5** corridors are already at or below the 3% target. The cheapest corridor in the file is the **UK to India** at **1.91%** (**`$3.82`**), while the most expensive is **South Africa to India** at **16.39%** (**`$32.78`**). Even some major Indian diaspora corridors are still above target: **U.S. to India** is **3.67%**, **UAE to India** is **3.72%**, and **Saudi Arabia to India** is **5.59%**.

Why this matters: the UN notes that cheaper remittances directly raise disposable income for families. In plain terms, every extra fee dollar is a dollar that never reaches a home budget.

Files: `outputs/remittance_global_summary.csv`, `outputs/remittance_global_country_rank.csv`, `outputs/india_inbound_remittance_corridors.csv`, `outputs/india_inbound_remittance_summary.csv`

## 2. India is near the top of the worker-productivity table

The most India-relevant new finding in the local slice is not about phones, internet, or social protection. It is about **output per worker**.

In `SL_EMP_PCAP`, India reports **5.12%** growth in real GDP per employed person in 2025. That puts it **11th out of 181** reporting countries and territories in this filtered table, almost **3 times** the median reporting value of **1.71%**.

Among nearby or comparable countries in the same slice:

1. **Viet Nam**: **5.74%**  
2. **Bhutan**: **5.44%**  
3. **India**: **5.12%**  
4. **China**: **4.90%**  
5. **Nepal**: **4.03%**  
6. **Sri Lanka**: **3.99%**  
7. **Indonesia**: **3.43%**  
8. **Bangladesh**: **2.36%**  
9. **Pakistan**: **0.26%**

Why this matters: the World Bank treats productivity growth as a core driver of sustainable income growth and poverty reduction. Put simply, it is a measure of how much more output each worker produces than before.

Files: `outputs/worker_productivity_summary.csv`, `outputs/worker_productivity_growth_rank.csv`, `outputs/worker_productivity_india_peers.csv`

## 3. A few migration routes dominate the recorded death toll

The migration-deaths indicator is grim, but it is very easy to understand.

In the local 2025 slice for `SM_DTH_MIGR`, the top **5** reporting areas account for **56.83%** of all recorded migration deaths, and the top **10** account for **77.29%**.

The top five in this file are:

1. **Iran** - **1,387**
2. **Libya** - **1,125**
3. **Yemen** - **809**
4. **Myanmar** - **570**
5. **Tunisia** - **469**

India reports **17** recorded deaths in this local slice, ranking **31st** among the **82** country-like reporting areas that survived the country filter.

Why this matters: the safe-migration pages behind SDG 10.7.3 describe this dataset as the starkest indicator of unsafe migration. The concentration pattern suggests that a relatively small number of reporting areas tied to major migration corridors drive most of the recorded loss of life.

Caveat: these are minimum documented counts, not the true total.

Files: `outputs/migration_deaths_summary.csv`, `outputs/migration_deaths_concentration.csv`, `outputs/migration_deaths_rank.csv`

## 4. Ukraine now sends out refugees at a higher per-capita rate than Afghanistan

This is still one of the clearest and most surprising numbers in the data.

In `SM_POP_REFG_OR`, **Ukraine** records **11,969.7 refugees per 100,000 people**, ranking **6th** in the local table. **Afghanistan** is **8th** at **9,819.5 per 100,000**.

That means the refugee-origin pressure in this slice is roughly:

- **Ukraine**: about **12%** of the population
- **Afghanistan**: about **10%** of the population

The top eight are:

1. Western Sahara
2. Venezuela
3. Syrian Arab Republic
4. South Sudan
5. Eritrea
6. **Ukraine**
7. Central African Republic
8. **Afghanistan**

Why this matters: many readers know the Ukraine war created a huge refugee crisis in absolute numbers. This data shows that even after adjusting for population size, Ukraine is now in the very top tier.

Files: `outputs/refugee_origin_summary.csv`, `outputs/refugee_origin_country_rank.csv`

## 5. Some of the world's most gender-balanced parliaments are still old parliaments, and India is below both medians

This remains the best politics-meets-demography story in the slice.

Across the **156** reporting areas with complete lower-house female and youth data:

- the median share of seats held by women is **27.68%**
- the median youth representation ratio is **0.65**

That youth ratio matters. A value of **1.0** would mean younger MPs are represented in parliament in line with their share in the eligible population. The median country is well below that.

Some parliaments that already look strong on women still look old on youth:

1. **Nicaragua** - **54.95%** women, youth ratio **0.22**
2. **United Arab Emirates** - **50.0%** women, youth ratio **0.30**
3. **Iceland** - **46.03%** women, youth ratio **0.49**

India is below both medians in this reporting set:

- **13.84%** women in parliament
- youth ratio **0.32**

Why this matters: representation is not one story. A country can improve gender balance and still leave younger adults badly underrepresented.

Files: `outputs/parliament_summary.csv`, `outputs/parliament_high_female_low_youth.csv`, `outputs/india_parliament_peers.csv`, `outputs/parliament_representation_rank.csv`

## 6. Youth jobs plans are common on paper, but not yet fully live across much of South and Southeast Asia

This one is dry in indicator language and simple in real language.

In `SL_CPA_YEMP`, a score of:

- **3** means a youth employment strategy is **operationalized**
- **2** means it is **developed but not operational**
- **1** means it is still **under development**
- **0** means **no strategy**

In the local slice, only **72 of 185** reporting areas are at **3**. Another **67** are stuck at **2**, **40** are still at **1**, and **6** report **0**.

The India-relevant regional pattern is straightforward:

- **China**: **3**
- **India**: **2**
- **Indonesia**: **2**
- **Pakistan**: **2**
- **Bangladesh**: **1**
- **Nepal**: **1**
- **Sri Lanka**: **1**

Why this matters: many governments can say they have a youth-jobs plan. Far fewer can say it is actually up and running.

Files: `outputs/youth_employment_strategy_summary.csv`, `outputs/youth_employment_strategy_india_peers.csv`, `outputs/youth_employment_strategy_scores.csv`

## 7. Governments say they have biodiversity plans, but far fewer say the job is done

This is the version of the biodiversity finding that is easiest to explain quickly.

The 2026 world roll-up for `ER_BDY_KMGBFT14` covers **195** reporting areas. **158** say they have a national target aligned with this biodiversity-planning goal, but only **50** say it is **achieved**. Another **63** say progress exists but is **insufficient**, **41** say progress is **unknown**, and **37** still say they have **no target** at all.

In plain English: lots of governments can say they have written nature into their official plans, but only about **1 in 4** reporting areas says it has actually finished the job.

Why this matters: this is about whether biodiversity gets built into official national planning rather than treated as an afterthought.

Files: `outputs/biodiversity_planning_summary.csv`, `outputs/biodiversity_planning_country_status.csv`
