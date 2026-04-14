# UN data: v3 notes

## What worked best in v3

- The strongest new angles were the ones that turned technical indicators into plain questions:
  - **How expensive is it to send money home to India?**
  - **How much crop diversity is flowing into India through the global seed-sharing system?**
  - **If a local livestock breed disappeared tomorrow, could it actually be rebuilt?**
  - **Do water-participation rules exist only on paper, or do communities really participate?**
- The best fresh India-specific addition was **seed-sharing**. The rank is strong, the numbers are large, and the explanation is short once `SMTA` is translated into ordinary language.
- The best new universal story was **livestock genetic backup**. "25 local breeds, 0 fully backed up" is both surprising and easy to understand.
- The water-governance indicators also held up well because they naturally support a **paper versus practice** framing.

## What the outside web research suggested

- **Plant genetic resources:** the FAO Plant Treaty datastore and public stats pages make it clear that SMTAs are not obscure internal paperwork. They are the treaty's standard mechanism for moving crop genetic material across borders, and the public site explicitly tracks top recipient countries and regional totals.
- **Animal genetic resources:** FAO's animal-genetics and DAD-IS pages make the backup indicator much easier to explain. "Stored for reconstitution" literally means enough genetic material is in long-term conservation to recreate the breed if needed.
- **Water participation:** UNEP's SDG 6.b.1 page confirms that the two water indicators are meant to be read together: one captures whether participation procedures exist, the other captures the level of actual participation.
- The earlier v2 context still mattered:
  - UN remittance material kept the **3% target** easy to translate into household money.
  - World Bank productivity framing kept the India productivity number anchored to a broader slowdown story.
  - UN migration pages reinforced that migration-death counts are **minimum documented counts**.
  - UN/IPU framing on women in parliament made the **youth representation** cut feel fresher.

## Data and interpretation quirks

- The SDG `CL_AREA` codelist still mixes countries, territories, and aggregates. I again used the numeric-plus-alpha label twin heuristic to approximate **country-like areas**.
- That heuristic is useful, but it is not perfect. Safer public phrasing is usually **"reporting areas"** or **"countries and territories"**.
- `SM_DTH_MIGR` should still be treated as a **minimum documented count**, not a full death toll.
- `SI_RMT_COST_BC` still needs decoding: in this slice, `REF_AREA` behaves like the **sending country**, while `CUST_BREAKDOWN` holds the **receiving country** code prefixed with `C`.
- `SI_RMT_COST_SC` still contains **negative values** in the local slice. I kept it out of the lay-facing write-up.
- Parliament youth indicators still use mixed age bands. I again preferred **`Y0T45`** and fell back to **`Y0T40`** only where needed.
- The crop-treaty status indicators need light normalization:
  - **Lesotho** appears with a raw treaty value of **2**
  - **Nicaragua** appears with a raw `NaN`
  - v3 treats any positive treaty/framework value as **yes**, preserves the raw values in `seed_treaty_status.csv`, and drops fully missing rows from the normalized summary table.
- The livestock indicators have uneven coverage:
  - `ER_GRF_ANIMKPT` is much broader than `ER_GRF_ANIMRCNTN` and `ER_RSK_LBREDS`
  - blank cells for Bangladesh, Nepal, or Pakistan in the v3 livestock peer table usually mean **missing local-slice data**, not zero breeds.
- India is absent from the local `ER_WAT_PRDU` / `ER_WAT_PART` rows, so the water-participation story has to be framed regionally rather than directly around India.

## Interesting findings that stayed in the notes

### 1. India and China still look strong on reported forest management plans

In `forest_india_peer_comparison.csv`:

- **China** reports **75.86%** of forest area under long-term management plans
- **India** reports **74.76%**
- **Brazil** reports **12.64%**

This is still interesting, but it needs outside validation before becoming a headline.

### 2. The treaty-framework gap is useful context, but too abstract to lead with by itself

The gap is real: **56** reporting areas in the normalized table show treaty participation without a framework on file. But on its own, that is harder for a lay reader to care about than India's rank in the seed-transfer table.

### 3. The breed-risk table is striking, but the denominator is technical

Many places score extremely high on `ER_RSK_LBREDS`; for example, **Algeria, Belgium, Botswana, Cyprus, Estonia, Gabon, Ireland, Malta, Mauritius, Paraguay, and Peru** all show **100%**. But this indicator is a share of local breeds with **known** extinction-risk status, which makes it harder to explain cleanly than the backup-count table.

### 4. India's outbound remittance picture is still uneven

The local corridor slice still includes only two outbound India corridors:

- **India -> Nepal:** **3.14%**
- **India -> Sri Lanka:** **6.84%**

That remains useful for a more South Asia-specific remittance follow-up.

### 5. Food price anomalies still look promising, but the local slice is messy

`AG_FPA_COMM` still has broad consumer appeal, but it stayed out because:

- the scale is not instantly intuitive,
- products are split across multiple commodity codes,
- the local slice still mixes values in ways that need more metadata work before publication.

### 6. Bribery incidence is still easy to understand but too thin here

`IC_FRM_BRIB` still collapses to only **24** country-like rows after filtering. That is too thin for a confident headline.

## Additional India and regional observations

- **India** accounts for **66.69%** of the local **Southern Asia** total in seed-transfer agreements and reports **5.18 times** as many agreements as **China**.
- On livestock backup, **India** ranks **3rd** with **44** backed-up local breeds, behind **China** (**96**) and **Spain** (**52**), but that still covers only **14.81%** of India's **297** local breeds.
- In the regional livestock peer table:
  - **Sri Lanka** reports **0** backed-up local breeds and **56%** of breeds with known risk status at risk
  - **Indonesia** reports **9** backed up and **50%** at risk
  - **Bhutan** reports **1** backed up and **52%** at risk
- In the regional water table:
  - **Bangladesh** and **Pakistan** both score **10** on formal procedures and **1** on participation
  - **Indonesia** and **Viet Nam** both score **10** and **3**
  - **Nepal** is the interesting exception: **5** on procedures but **3** on participation
- The big v2 India points still hold in v3:
  - India is still above the UN remittance target at **5.3%**
  - India still ranks **11th** on worker-productivity growth
  - India is still below both parliament medians on women and youth representation

## Repro assets created in v3

- `build_metadata.py` - fetches and parses the SDMX structures and codelists used in the local slices
- `fetch_context.py` - fetches and caches the public context pages used to frame the v3 analysis
- `analyze_un_data.py` - rebuilds the v3 output tables under `v3/outputs/`
- `insights.md` - the full v3 catalog of usable story leads
- `notes.md` - the data quirks, weaker leads, and follow-up ideas

## Good follow-ups for v4 or later

- Add an explicit sovereign-state filter from an external country list so the refugee and migration tables can cleanly exclude territories.
- Pair parliament ratios with external age-structure data for a sharper India political-demography story.
- Deepen the India remittance story with corridor trends over time if more years are downloaded.
- Use FAO DAD-IS export or breed-level tables to move from country counts to named livestock breeds at risk.
- Validate the forest-management reporting differences against non-UN deforestation or satellite-based forest-loss data.
- Figure out whether the seed-treaty status anomalies are upstream data issues or expected coding quirks, and see whether Nicaragua can be recovered cleanly.
