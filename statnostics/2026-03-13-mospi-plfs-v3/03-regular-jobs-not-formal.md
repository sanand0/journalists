# Verification SOP: regular salaried is not the same as formal

Verifies `03-regular-jobs-not-formal.svg`.

## If you do not have the `data/` folder

These steps are meant to work even if you only received this cards folder.

Before verifying any card, download the original `mospi-plfs` analysis workspace used to make these graphics. The upstream repository is:

- `https://github.com/sanand0/journalists`
- analysis folder: `data/mospi-plfs/`
- latest story-ready analysis: `data/mospi-plfs/v3/`

The most direct way to get it is:

```bash
git clone --depth 1 https://github.com/sanand0/journalists.git
cd journalists/data/mospi-plfs
```

If you downloaded only the `mospi-plfs/` folder as a zip or archive, start from that folder instead.

If `plfs.parquet` is not already present, fetch it and regenerate the v3 tables before checking the card:

```bash
./download_plfs.sh
./v3/analyze.py
```

Inside `mospi-plfs/`, you should have `README.md`, `download_plfs.sh`, `v3/analyze.py`, `v3/insights.md`, and `v3/outputs/`.

`README.md` in that workspace says `plfs.parquet` is a processed person-level PLFS 2024 file downloaded from the public `Vonter/india-plf-survey` repository. In the rest of this SOP, all source paths are relative to the downloaded `mospi-plfs/` workspace root, not to this `statnostics/` folder.

## What this card is saying

- A project-defined `strict formal` job is a **regular salaried** job that has **all three** of the following at once:
  - a written contract
  - paid leave
  - at least one social-security benefit
- On that strict test, only about one in three regular salaried jobs qualify.
- The pay gap between the strict-formal bucket and the rest of regular salaried work is very large.
- The occupations driving the nonformal bucket are familiar jobs, not obscure categories.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `Only 34.9% have all three at once`
   - `Median monthly earnings are 32,000 in the strict-formal bucket and 12,000 in the rest`
   - `Shop Salespersons alone account for 11.5%`
2. Open `v3/outputs/strict_formality_benchmark.csv` and use the `sex = all` row.
3. Open `v3/outputs/nonformal_regular_top_occupations.csv` for the occupation note.

## Source files to open

- `v3/insights.md`
  - Narrative summary and the conservative definition warning.
- `v3/outputs/strict_formality_benchmark.csv`
  - Exact percentages and medians used by the card.
- `v3/outputs/nonformal_regular_top_occupations.csv`
  - Exact occupation ranks and weighted masses behind the bottom annotation.
- `v3/analyze.py`
  - `is_strict_formal` is defined in the top setup view.

## Exact benchmark row to check

In `strict_formality_benchmark.csv`, filter to `sex = all`.

- `regular_m = 92.259`
- `written_contract_pct = 44.2`
- `paid_leave_pct = 52.4`
- `any_social_security_pct = 45.4`
- `strict_formal_pct = 34.9`
- `median_monthly_earnings_strict_formal = 32000.0`
- `median_monthly_earnings_other_regular = 12000.0`

## Card text -> source check

| Card element | Source value | Verification note |
|---|---:|---|
| `Only 1 in 3 regular salaried jobs is truly formal` | `34.9%` | The card rounds 34.9% to `about one in three`. |
| 3 dark squares out of 10 | `34.9%` | Visual shorthand, not a literal 30.0% value. |
| `₹32,000` median monthly pay | `32000.0` | Exact value already rounds cleanly. |
| `₹12,000` median monthly pay | `12000.0` | Exact value already rounds cleanly. |
| `written contract + paid leave + any social security` | defined in `analyze.py` | This is a project definition, not an official PLFS category name. |

## Exact strict-formal logic

The analysis treats a worker as `is_strict_formal = 1` only if all of these are true:

- principal activity is `worked as regular salaried/wage employee`
- `Principal Job Contract Type` is present and is **not** `no written job contract`
- `Principal Job - Paid Leave = yes`
- `Principal Job - Social Security` is neither `not eligible for any of above social security benefits` nor `not known`

That is intentionally conservative.

## Occupation annotation: what to check carefully

The card line `Biggest nonformal regular jobs: shop salespersons, cleaners, drivers, cooks, teachers` is an **editorial grouping line**, not a literal machine-generated top-5 list.

Check these rows in `nonformal_regular_top_occupations.csv`:

- `Shop Salespersons` -> `6.496` million-equivalent, `11.5%`
- `Domestic, Hotel and Office Cleaners and Helpers` -> `4.898`
- `Car, Van and Motorcycle Drivers` -> `3.007`
- `Heavy Truck and Bus Drivers` -> `2.699`
- `Cooks` -> `2.637`
- `Primary School and Early Childhood Teachers` -> `1.75`
- `Secondary Education Teachers` -> `1.06`

Useful grouped checks:

- combined `drivers` = `5.706` million-equivalent
- combined `teachers` = `2.810` million-equivalent

Important omission to note in review:

- `Manufacturing Labourers` are actually `3.838` million-equivalent and rank above some categories named on the card.
- So the bottom annotation should be treated as a **reader-friendly set of familiar examples**, not a literal ranked top-5 sentence.

## Common ways to mis-verify this card

- Using the `male` or `female` row instead of the `all` row.
- Forgetting that `strict formal` is stricter than many other common definitions of formality.
- Treating the 3/10 square row as a mathematically exact 30% claim.
- Reading the occupation caption as a literal exhaustive ranking instead of grouped examples.

## If you want to rerun the tables

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

## Pre-publication checklist

- [ ] The `all` row in `strict_formality_benchmark.csv` is the one used.
- [ ] The formality definition is described accurately and conservatively.
- [ ] The 3/10 visual is treated as `about one in three`, not exactly 30.0%.
- [ ] The occupation annotation is not oversold as a strict rank order.
- [ ] The pay figures are still `₹32,000` vs `₹12,000`.
