# Verification SOP — Biodiversity Plans vs. Done (Card 10)

## If you do not have the `data/` folder

Clone the journalists repo and run the v3 analysis script:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/un
uv run download_un_data.py download --match ER_BDY_KMGBFT14 --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Source: UN SDG Global Database indicator **ER_BDY_KMGBFT14** (Progress toward national biodiversity strategy and action plan targets, Aichi Target 14 — ecosystem services and human well-being). Each reporting area is classified by whether it has achieved, is progressing toward, or has fallen short of its self-set biodiversity targets.

## What this card is saying

Of 195 reporting areas:
- Only **50 (25.6%)** have *achieved* their biodiversity targets — one in four.
- **63 (32.3%)** are making progress but remain insufficient.
- **41 (21.0%)** have unknown or untracked progress.
- **4 (2.0%)** show no significant progress at all.
- **37 (19.0%)** never set a target.

The waffle chart maps all 195 areas as unit squares, with color encoding status. The headline message: 74% of areas that set a target have not achieved it.

## Fastest way to verify

Open `v3/outputs/biodiversity_planning_summary.csv`. Check the five rows for status categories and counts. Sum all counts — should equal 195. Confirmed: achieved=50, insufficient=63, unknown=41, no_progress=4, no_target=37.

Open `v3/outputs/biodiversity_planning_country_status.csv` to find individual countries.

## Source files to open

| File | What it contains |
|------|-----------------|
| `v3/outputs/biodiversity_planning_summary.csv` | Count and share per status category across 195 areas |
| `v3/outputs/biodiversity_planning_country_status.csv` | All 195 areas with their individual status values |

## Exact rows

`biodiversity_planning_summary.csv`:

| status | label | count | share |
|--------|-------|-------|-------|
| 1 | Achieved | 50 | 25.64% |
| 2 | Progress insufficient | 63 | 32.31% |
| 3 | Unknown | 41 | 21.03% |
| 4 | No significant progress | 4 | 2.05% |
| 5 | No target set | 37 | 18.97% |
| **Total** | | **195** | 100% |

## Card text → source check

| Displayed | Source value | Note |
|-----------|-------------|------|
| "25.6% achieved" (50 cells teal) | 50/195 = 25.64% | Rounds to 25.6% ✓ |
| "32.3% insufficient" (63 cells pink) | 63/195 = 32.31% | Rounds to 32.3% ✓ |
| "21.0% unknown" (41 cells yellow) | 41/195 = 21.03% | Rounds to 21.0% ✓ |
| "2.1% no progress" (4 cells crimson) | 4/195 = 2.05% | Rounds to 2.1% ✓ |
| "19.0% no target" (37 cells grey) | 37/195 = 18.97% | Rounds to 19.0% ✓ |
| Total cells = 195 | Sum of all counts | Waffle chart is exactly 15×13 = 195 cells |

## Waffle chart layout verification

The waffle chart encodes areas in reading order (left to right, top to bottom), filling categories in sequence:

| Category | Cells | Fill colour | Start cell | End cell |
|----------|-------|------------|-----------|---------|
| Achieved | 50 | Teal `#1a5e6e` | 1 | 50 |
| Insufficient | 63 | Pink `#fca5a5` | 51 | 113 |
| Unknown | 41 | Yellow `#fde68a` | 114 | 154 |
| No progress | 4 | Crimson `#c1121f` | 155 | 158 |
| No target | 37 | Grey `#e5e7eb` | 159 | 195 |

Grid: 15 columns × 13 rows = 195 cells. Cell size 15px, gap 2px, step 17px. Origin: x=113, y=155.

## Common ways to mis-verify

- **195 total**: The denominator is 195 reporting areas, not 193 UN member states. UN data can include territories, economic unions, and regional aggregates. Do not assume "1 area = 1 country."
- **"Achieved" vs. "on track"**: Status 1 (Achieved) means the area has met its *self-defined* Aichi target 14 objective. This is self-reported. The UN does not independently audit each national report. An area claiming achievement may have set a weak initial target.
- **No target = no data?**: Status 5 (No target set, 37 areas) means the area reported having no biodiversity strategy target for this indicator. It does not mean data is missing — it is a deliberate reporting category.
- **Rounding**: 4/195 = 2.051% which rounds to 2.1%, not 2.0%. Check whether the card displays "2.1%" or "2.0%" — the source rounds to one decimal, so 2.1% is the correct display.
- **Order in waffle**: The visual order (teal first → grey last) is by decreasing "success level," not by count. Verify that no cells are in the wrong color (e.g., that crimson 4-cell block falls in the correct position in row 11–12 of the grid).

## If you want to rerun

```bash
cd journalists/data/un
uv run download_un_data.py download --match ER_BDY_KMGBFT14 --latest-only --max-jobs 1
uv run v3/analyze_un_data.py
```

Then open `v3/outputs/biodiversity_planning_summary.csv`.

## Pre-publication checklist

- [ ] Confirm total reporting areas = 195
- [ ] Achieved (teal) = 50; 50/195 = 25.64% → rounds to 25.6% ✓
- [ ] Insufficient (pink) = 63; 63/195 = 32.31% → rounds to 32.3% ✓
- [ ] Unknown (yellow) = 41; 41/195 = 21.03% → rounds to 21.0% ✓
- [ ] No progress (crimson) = 4; 4/195 = 2.05% → check display value (2.0% or 2.1%)
- [ ] No target (grey) = 37; 37/195 = 18.97% → rounds to 19.0% ✓
- [ ] Sum all counts: 50+63+41+4+37 = 195 ✓
- [ ] Confirm waffle grid is 15 cols × 13 rows = 195 cells ✓
- [ ] Verify color sequence in SVG matches status order (teal → pink → yellow → crimson → grey)
- [ ] Verify data period is most recent available (confirm year label on card)
- [ ] Remind editorial: "achieved" is self-reported; consider caveat note if publishing as hard news
