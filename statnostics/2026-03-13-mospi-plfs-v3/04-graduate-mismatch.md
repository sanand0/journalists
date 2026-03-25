# Verification SOP: graduate occupation mismatch

Verifies `04-graduate-mismatch.svg`.

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

- The card is about **graduate workers with a principal occupation**.
- It compares a custom set of occupation buckets built in `analyze.py`.
- The central contrast is simple: **farm-and-animal work** is larger than the **software-and-engineering** bucket, and farm + sales together are much larger still.
- The callout names the single biggest raw occupation inside the graduate worker pool.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `13.5% are in farm-and-animal work`
   - `Only 6.9% are in the combined software-and-engineering bucket used here`
   - `The single biggest occupation among graduate workers is Market Gardeners & Crop Growers`
2. Open `v3/outputs/graduate_worker_occupation_buckets.csv` and filter to `age_group = all_graduates`.
3. Open `v3/outputs/graduate_worker_top_occupations.csv` to verify the callout occupation.

## Source files to open

- `v3/insights.md`
  - Narrative framing and the exact bucket shares.
- `v3/outputs/graduate_worker_occupation_buckets.csv`
  - Exact percentages behind the horizontal bars.
- `v3/outputs/graduate_worker_top_occupations.csv`
  - Exact top occupation behind the callout.
- `v3/analyze.py`
  - Defines the custom bucket mapping.

## Exact rows behind the bars

In `graduate_worker_occupation_buckets.csv`, filter to `age_group = all_graduates`.

| Card label | `occupation_bucket` | `weighted_m` | `share_pct` |
|---|---|---:|---:|
| Farm & animal work | `farm_and_animal_work` | `7.189` | `13.5%` |
| Teaching | `teaching` | `7.101` | `13.4%` |
| Sales work | `sales_work` | `5.792` | `10.9%` |
| Software & engineering | `software_and_engineering` | `3.68` | `6.9%` |
| Healthcare | `health` | `1.292` | `2.4%` |

## What the headline and deck are checking

- Headline check: `More graduates farm the land than write the code`
  - farm-and-animal work = `13.5%`
  - software-and-engineering = `6.9%`
- Deck check: `farming and sales dwarf software and engineering combined`
  - farm + sales = `24.4%`
  - software-and-engineering = `6.9%`

## Callout occupation to verify

In `graduate_worker_top_occupations.csv`, check:

- `Market Gardeners & Crop Growers` -> `weighted_m = 5.491`, `share_pct = 11.6%`

Useful comparison rows:

- `Shop Salespersons` -> `4.85` million-equivalent
- `Software and Application Developers and Analysts` -> `2.876` million-equivalent

## Important bucket-definition note

The bar chart uses **custom grouped buckets**, not raw PLFS occupation labels.

The mapping in `analyze.py` groups these together:

- `farm_and_animal_work`: Market Gardeners & Crop Growers, Animal Producers, Mixed Crop and Animal Workers, Subsistence Crop Farmers, Subsistence Livestock Farmers, Agricultural/Forestry/Fishery Labourers
- `sales_work`: Shop Salespersons, Street and Market Salespersons, Other Sales Workers
- `software_and_engineering`: Software and Application Developers and Analysts, Engineering Professionals (including the excluding-electrotechnology label)
- `teaching`: occupations whose name contains `Teachers`
- `health`: Medical Doctors, Nursing and Midwifery Associate Professionals, Medical and Pharmaceutical Technicians

If anyone disputes what belongs in a bucket, that is the place to inspect.

## Common ways to mis-verify this card

- Using the `age_21_34` rows instead of `all_graduates`.
- Comparing the card to raw occupations without noticing that the bar chart uses grouped buckets.
- Forgetting the note `with a principal occupation`; unemployed graduates are not in this denominator.
- Treating the headline as if it says all graduates are farmers. It only says the farm bucket is larger than the software-and-engineering bucket used here.

## If you want to rerun the tables

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

## Pre-publication checklist

- [ ] The bucket file is filtered to `all_graduates`.
- [ ] The bar values still read 13.5, 13.4, 10.9, 6.9, and 2.4.
- [ ] The callout still matches `Market Gardeners & Crop Growers`.
- [ ] Any editor reviewing the chart understands that the buckets are custom grouped categories.
- [ ] The copy does not overstate the claim beyond the graduate-worker denominator.
