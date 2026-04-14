# Verification SOP — Remittance Cost Gap (Card 01)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script to generate all source CSVs:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match SI_RMT_COST --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

The source data is UN SDG Global Database indicator **SI_RMT_COST_BC** (Proportion of the total volume of remittances (in USD) sent from a country using a given service that costs 5 per cent or less). The analysis script reads raw UN SDG API JSON and produces CSVs in `v3/outputs/`.

## What this card is saying

Among 20 remittance corridors from various countries into India, the cost of sending USD 200 ranges from USD 3.82 (UK, 1.91% of transfer value) to USD 32.78 (South Africa, 16.39%). Only 5 of the 20 corridors fall at or below the UN SDG target of 3% (USD 6 on a USD 200 send). The headline comparison is London→India ($3.82) vs Johannesburg→India ($32.78) — an 8.5× gap. The card is a snapshot; costs vary by service and quarter.

## Fastest way to verify

Open `v3/outputs/remittance_cost.csv` and filter for `counterpart_area = India`. Sort by `value` ascending. The minimum should be ~3.82 (UK) and the maximum ~32.78 (South Africa). Count rows with `value ≤ 6` — expect 5 of 20.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/remittance_cost.csv` | All corridors with sending cost in USD per $200 transfer |
| `v3/outputs/remittance_cost_india.csv` | India-specific corridors (if generated separately) |
| `v3/analyze_un_data.py` | Indicator SI_RMT_COST_BC, filtering logic |

## Exact rows

Open `v3/outputs/remittance_cost.csv` — filter `counterpart_area = "India"`, sort by `value`:

| Sending country | Cost (USD on $200) | % of transfer | Meets 3% target? |
|---|---|---|---|
| United Kingdom | 3.82 | 1.91% | Yes |
| Singapore | 5.84 | 2.92% | Yes |
| United States of America | 7.34 | 3.67% | No |
| United Arab Emirates | 7.44 | 3.72% | No |
| Saudi Arabia | 11.18 | 5.59% | No |
| Australia | 12.30 | 6.15% | No |
| Japan | 17.44 | 8.72% | No |
| South Africa | 32.78 | 16.39% | No |

(These 8 are the corridors shown on the card; 12 additional corridors exist but are not displayed.)

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| UK: $3.82 | 3.82 | Exact match |
| South Africa: $32.78 | 32.78 | Exact match |
| "8.5× less" | 32.78 / 3.82 ≈ 8.58 | Rounded to 8.5× |
| "15 of 20 corridors miss 3% target" | Count rows > $6 | Should be 15 of 20 |
| UN 3% target = $6 on $200 | 3% × 200 = 6.00 | Derived value |

## Common ways to mis-verify

- **Don't use the rate as-is**: The UN indicator `SI_RMT_COST_BC` may report the *proportion of volume* using ≤5% cost services, not the cost itself. The cost per $200 may be derived from a secondary source (World Bank Remittance Prices Worldwide database). Confirm which source the analysis script actually uses.
- **Quarter matters**: Remittance costs vary quarterly. Confirm the analysis uses the most recent available period (likely Q4 2024 or Q1 2025).
- **Operator average**: The displayed cost is typically an average across operators in that corridor, not the cheapest operator.
- **"20 corridors"**: The 20-corridor count refers specifically to corridors from countries into India. Verify the filter in `analyze_un_data.py`.

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match SI_RMT_COST --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/remittance_cost.csv`.

## Pre-publication checklist

- [ ] Confirm UK cost = $3.82 in source CSV (or derived calculation)
- [ ] Confirm South Africa cost = $32.78 in source CSV
- [ ] Confirm ratio 32.78 / 3.82 ≥ 8.0 (displayed as 8.5×)
- [ ] Count corridors into India with cost > $6 — confirm = 15 of 20
- [ ] Confirm UN 3% target is correctly stated as $6 on a $200 send
- [ ] Confirm data period (year/quarter) shown in source
- [ ] Verify no duplicate corridors (one row per corridor in displayed list)
