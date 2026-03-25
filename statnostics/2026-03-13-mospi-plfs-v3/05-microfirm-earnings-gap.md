# Verification SOP: microfirm earnings gap

Verifies `05-microfirm-earnings-gap.svg`.

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

- The population is **urban graduates in regular salaried work**.
- The card compares two employer-size extremes: **less than 6 workers** vs **20 and above**.
- The chart shows that the same degree produces very different median monthly earnings depending on employer size.
- The small bottom callout on social security uses the **women's urban rows**, not a combined-sex average.

## Fastest way to verify

1. Open `v3/insights.md` and search for:
   - `Among urban female graduates in regular salaried work, median monthly earnings are 34,000`
   - `Among urban male graduates, the same comparison is 38,500 versus 15,000`
   - `no-social-security rate jumps from 9.7% in 20+ worker firms to 67.4% in firms with fewer than 6`
2. Open `v3/outputs/graduate_microfirm_penalty.csv`.
3. Filter to `sector = urban`, then check the four rows below.

## Source files to open

- `v3/insights.md`
  - Narrative framing and the exact comparisons.
- `v3/outputs/graduate_microfirm_penalty.csv`
  - The exact earnings and no-social-security values used in the chart.
- `v3/outputs/strict_formality_by_workers_count.csv`
  - Optional supporting file if you want to confirm how sharply job quality changes by firm size.
- `v3/analyze.py`
  - Defines the table as regular salaried graduates with non-null salaried earnings.

## Exact rows to check in `graduate_microfirm_penalty.csv`

Filter to `sector = urban`.

### Women graduates

- `workers_count = less than 6`
  - `median_monthly_earnings = 12000.0`
  - `no_social_security_pct = 67.4`
  - `n = 403`
  - `weighted_m = 0.642`
- `workers_count = 20 and above`
  - `median_monthly_earnings = 34000.0`
  - `no_social_security_pct = 9.7`
  - `n = 2003`
  - `weighted_m = 3.597`

### Men graduates

- `workers_count = less than 6`
  - `median_monthly_earnings = 15000.0`
  - `no_social_security_pct = 74.1`
  - `n = 924`
  - `weighted_m = 1.439`
- `workers_count = 20 and above`
  - `median_monthly_earnings = 38500.0`
  - `no_social_security_pct = 6.7`
  - `n = 4967`
  - `weighted_m = 9.689`

## Card text -> source check

| Card element | Source value | Verification note |
|---|---:|---|
| women `< 6 workers` | `12000.0` | Shown as `₹12k`. |
| women `20+ workers` | `34000.0` | Shown as `₹34k`. |
| men `< 6 workers` | `15000.0` | Shown as `₹15k`. |
| men `20+ workers` | `38500.0` | Shown as `₹38.5k`. |
| social-security callout | women `67.4%` vs `9.7%` | Rounded to `67%` vs `10%`. |

Useful derived checks:

- women large-firm / tiny-firm pay ratio = `2.83x`
- men large-firm / tiny-firm pay ratio = `2.57x`

## Why the social-security note needs special attention

The chart shows both women and men, but the bottom line:

- `No social security: 67% in tiny firms vs 10% in large firms`

matches the **urban female** rows:

- less than 6 workers -> `67.4%`
- 20 and above -> `9.7%`

It does **not** match a combined-sex average.

If an editor asks for the male equivalent, it is:

- `74.1%` in tiny firms
- `6.7%` in large firms

## Optional stronger job-quality check

Open `strict_formality_by_workers_count.csv` and verify the strict-formal shares for the same employer-size split:

- women urban `< 6` -> `4.7%`
- women urban `20+` -> `63.0%`
- men urban `< 6` -> `3.4%`
- men urban `20+` -> `64.6%`

This is not printed on the card, but it confirms the same employer-quality story.

## Common ways to mis-verify this card

- Using rural rows instead of urban rows.
- Comparing all workers instead of the `graduate+` and `regular salaried` subset.
- Missing that the CSV labels are `less than 6` and `20 and above`, while the card says `< 6 workers` and `20+ workers`.
- Assuming the social-security callout is pooled across sexes.

## If you want to rerun the tables

```bash
cd /path/to/mospi-plfs
./download_plfs.sh   # only needed if plfs.parquet is missing
./v3/analyze.py
```

## Pre-publication checklist

- [ ] All four chart points come from `sector = urban` rows.
- [ ] The employer-size labels map correctly to `less than 6` and `20 and above`.
- [ ] The women callout still rounds from 67.4% and 9.7%.
- [ ] The copy still says this is about regular salaried graduates, not all graduates.
- [ ] The visual does not imply that men and women are being pooled into one series.
