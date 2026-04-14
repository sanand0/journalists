# UN Global Data v3 · Statoistics Cards

This folder contains ten print-ready SVG cards derived from the UN's SDG Harmonized Global Dataflow (2025 slice), plus a journalist verification SOP for each card.

## What is in this folder

- [`../index.html`](../index.html) — **gallery page**: view all cards with image popup and one-click Verify panel
- `*.svg` — finished print-ready Statoistics cards (480×480px)
- `*.md` — fact-checking and verification SOP for the matching card

> **Tip:** Open the gallery via a local HTTP server to enable the in-page Verify panel:
> ```bash
> cd statnostics
> python3 -m http.server 8000
> # then open http://localhost:8000
> ```

## Card index

| # | Card | SVG | SOP |
|---|------|-----|-----|
| 01 | Sending $200 to India: $3.82 or $32.78 | [01-remittance-cost-gap.svg](01-remittance-cost-gap.svg) | [01-remittance-cost-gap.md](01-remittance-cost-gap.md) |
| 02 | Ukraine sends out more refugees per capita than Afghanistan | [02-ukraine-refugee-rate.svg](02-ukraine-refugee-rate.svg) | [02-ukraine-refugee-rate.md](02-ukraine-refugee-rate.md) |
| 03 | Most countries have zero livestock breeds ready for recovery | [03-livestock-no-backup.svg](03-livestock-no-backup.svg) | [03-livestock-no-backup.md](03-livestock-no-backup.md) |
| 04 | India's workers grew 3× more productive than the world median | [04-india-productivity-growth.svg](04-india-productivity-growth.svg) | [04-india-productivity-growth.md](04-india-productivity-growth.md) |
| 05 | India's parliament scores below the global median on women and youth | [05-parliament-below-both-medians.svg](05-parliament-below-both-medians.svg) | [05-parliament-below-both-medians.md](05-parliament-below-both-medians.md) |
| 06 | India is the world's #2 destination for crop genetic material | [06-seed-crop-diversity.svg](06-seed-crop-diversity.svg) | [06-seed-crop-diversity.md](06-seed-crop-diversity.md) |
| 07 | Five migration routes account for over half of all documented deaths | [07-migration-deaths-concentration.svg](07-migration-deaths-concentration.svg) | [07-migration-deaths-concentration.md](07-migration-deaths-concentration.md) |
| 08 | Only 39% of governments have a youth-jobs plan that's actually running | [08-youth-strategy-gap.svg](08-youth-strategy-gap.svg) | [08-youth-strategy-gap.md](08-youth-strategy-gap.md) |
| 09 | Written water rules are common. Real community participation is not. | [09-water-rules-vs-practice.svg](09-water-rules-vs-practice.svg) | [09-water-rules-vs-practice.md](09-water-rules-vs-practice.md) |
| 10 | Nature is in the plan. But only 1 in 4 countries says it's achieved. | [10-biodiversity-plans-vs-done.svg](10-biodiversity-plans-vs-done.svg) | [10-biodiversity-plans-vs-done.md](10-biodiversity-plans-vs-done.md) |

## Source material

All cards draw from UN SDG data, 2025 slice:

- **UN Data portal**: [data.un.org](https://data.un.org)
- **SDG Harmonized Global Dataflow**: `IAEG-SDGs:DF_SDG_GLH(1.24)`
- **Local analysis scripts**: [`data/un/v3/analyze_un_data.py`](../../data/un/v3/analyze_un_data.py)
- **Local output CSVs**: [`data/un/v3/outputs/`](../../data/un/v3/outputs/)
- **Insights document**: [`data/un/v3/insights.md`](../../data/un/v3/insights.md)

### SDG indicators used

| Card | Indicator | Description |
|------|-----------|-------------|
| 01 | `SI_RMT_COST_BC` | Remittance cost — bilateral corridors |
| 02 | `SM_POP_REFG_OR` | Refugees by origin country per 100,000 |
| 03 | `ER_GRF_ANIMRCNTN` | Livestock breeds backed up for reconstitution |
| 04 | `SL_EMP_PCAP` | Real GDP per employed person (annual growth) |
| 05 | `SG_GEN_PARL` + `SG_PLT_RPTY` | Women in parliament + youth representation |
| 06 | `ER_CBD_SMTA` | Standard Material Transfer Agreements (crop genetic material) |
| 07 | `SM_DTH_MIGR` | Documented deaths of migrants in transit |
| 08 | `SL_CPA_YEMP` | Youth employment policy implementation score |
| 09 | `ER_WAT_PRDU` + `ER_WAT_PART` | Water user participation — procedures and practice |
| 10 | `ER_BDY_KMGBFT14` | Biodiversity in national planning (Kunming-Montreal GBF) |

## Recommended workflow

1. Open the card SVG.
2. Open the matching SOP markdown file.
3. Use the SOP's search strings, CSV row filters, and checklist to verify the claim.

## Reproducing the data

If you do not have the `data/` folder:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match DF_SDG_GLH --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

The output CSVs will appear in `data/un/v3/outputs/` and match the values on the cards exactly.
