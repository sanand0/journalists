# India PLFS 2024 Analysis Workspace

This folder is a reporting and analysis workspace built around a single parquet file, [`plfs.parquet`](plfs.parquet), which contains person-level data from India’s 2024 Periodic Labour Force Survey (PLFS).

The goal of this project is not to reproduce the obvious PLFS headlines. It is to find story angles that are:

- simple enough for a general reader to understand quickly
- surprising enough to be worth reporting
- defensible enough to survive scrutiny

The latest and best analysis lives in [`v3/`](v3/).

## What The Dataset Is

The dataset in this folder is a processed parquet file downloaded from the public GitHub repository `Vonter/india-plf-survey`. In plain English:

- one row is one person
- the file covers survey interviews conducted during `2024`
- it contains both household-level information and person-level information
- it includes demographic details, education, household background, employment status, earnings, and a 7-day work diary

The latest profile exported by this project is in [`v3/outputs/dataset_profile.csv`](v3/outputs/dataset_profile.csv). At the time of analysis it showed:

- `415,549` person records
- survey dates from `2024-01-03` to `2024-12-31`
- a unique `Person ID` for every row

## What PLFS Measures, In Plain English

Some of the strongest findings in this project come from the fact that PLFS describes work in more than one way.

The most important lenses are:

- `Principal Activity Status`
  This is the person’s main activity over a longer reference period. A person can be coded here as `attended domestic duties only`, `worked as regular salaried/wage employee`, `self-employed`, and so on.
- `Subsidiary Work Engagement` and `Subsidiary Activity Status`
  This captures whether the person also did a second kind of work.
- `CWS Status`
  `CWS` means `Current Weekly Status`. This is what the person was doing in the reference week.
- Daily diary fields
  The file also records day-by-day work activity, hours, and wages for up to two activities per day over seven days.

Why that matters:

- someone can look like a `homemaker` on the principal-status lens
- but still show up as a worker on the weekly-status lens
- that tension is the basis of one of the strongest stories in this project

## What This Repository Contains

The workspace is organized by analysis version:

- [`download_plfs.sh`](download_plfs.sh)
  Downloads `plfs.parquet` if it is missing, and skips re-downloading if the file is already complete.
- [`v1/`](v1/)
  First exploratory pass. Broad search for unusual patterns.
- [`v2/`](v2/)
  Tighter, more lay-reader-friendly analysis with stronger filtering and better benchmark tables.
- [`v3/`](v3/)
  Current best version. This is the one to use first if you are writing a story now.

Inside each versioned folder you will usually find:

- `analyze.py`
  The main reproducible analysis script.
- `run.sh`
  A small wrapper that runs the same analysis.
- `insights.md`
  A plain-English summary of the strongest findings.
- `notes.md`
  Caveats, false starts, anomalies, follow-up ideas, and methodology notes.
- `outputs/`
  The CSV files that back the written claims.

## Quick Start

If the parquet file is not present yet:

```bash
./download_plfs.sh
```

To regenerate the latest analysis:

```bash
./v3/analyze.py
```

Or:

```bash
./v3/run.sh
```

These scripts use `uv` and install Python dependencies automatically through inline script metadata.

## The Best Place To Start

If you are new to this project, read these files in this order:

1. [`v3/insights.md`](v3/insights.md)
2. [`v3/notes.md`](v3/notes.md)
3. the specific CSVs cited inside `v3/insights.md`

That gives you:

- the headline findings
- the exact tables behind them
- the caveats you need before publication

## Strongest Story-Ready Findings

These are the clearest, most defensible reporting angles from `v3`.

### 1. Marriage looks like a labour-market cliff for educated women

Best files:

- [`v3/outputs/marriage_weighted_model.csv`](v3/outputs/marriage_weighted_model.csv)
- [`v3/outputs/marriage_gradplus_state_compare.csv`](v3/outputs/marriage_gradplus_state_compare.csv)
- [`v3/outputs/marriage_control_cells_household_type.csv`](v3/outputs/marriage_control_cells_household_type.csv)

Short version:

- among women aged `25-34`, marriage is associated with a big rise in `domestic duties only`
- the same group becomes much less likely to be in regular salaried work
- the pattern is especially sharp for graduates

### 2. Many women counted as homemakers are still workers on another PLFS lens

Best files:

- [`v3/outputs/hidden_work_national_benchmark.csv`](v3/outputs/hidden_work_national_benchmark.csv)
- [`v3/outputs/hidden_work_weekly_work_composition.csv`](v3/outputs/hidden_work_weekly_work_composition.csv)
- [`v3/outputs/hidden_work_state_mass.csv`](v3/outputs/hidden_work_state_mass.csv)

Short version:

- `8.4%` of women whose principal status is `attended domestic duties only` still show up as working in the current week
- most of that hidden work is not formal employment
- it is mainly family-enterprise work: own-account work and unpaid family work

### 3. A child in the household makes the marriage cliff steeper

Best files:

- [`v3/outputs/household_key_quality.csv`](v3/outputs/household_key_quality.csv)
- [`v3/outputs/child_proxy_women_25_34_under5.csv`](v3/outputs/child_proxy_women_25_34_under5.csv)
- [`v3/outputs/child_proxy_married_graduate_model.csv`](v3/outputs/child_proxy_married_graduate_model.csv)

Short version:

- among currently married graduate women aged `25-34`, living with a child under `5` is linked to more domestic-only status and less regular salaried work
- the pattern is even stronger for a child under `2`
- the same pattern barely appears for married graduate men

Important caution:

- this is a `child in the household` proxy, not a literal `own child` field

### 4. Only about one in three regular salaried jobs looks formal by a strict test

Best files:

- [`v3/outputs/strict_formality_benchmark.csv`](v3/outputs/strict_formality_benchmark.csv)
- [`v3/outputs/nonformal_regular_top_occupations.csv`](v3/outputs/nonformal_regular_top_occupations.csv)
- [`v3/outputs/strict_formality_nonformal_concentration.csv`](v3/outputs/strict_formality_nonformal_concentration.csv)

Short version:

- many `regular salaried` jobs do not have a written contract, paid leave, and social security at the same time
- the gap is not abstract
- the biggest nonformal regular jobs are familiar occupations like shop salespersons, cleaners, drivers, and cooks

### 5. Graduate mismatch looks more like farm-and-retail work than white-collar work

Best files:

- [`v3/outputs/graduate_worker_occupation_buckets.csv`](v3/outputs/graduate_worker_occupation_buckets.csv)
- [`v3/outputs/graduate_worker_top_occupations.csv`](v3/outputs/graduate_worker_top_occupations.csv)
- [`v3/outputs/graduate_regular_selected_occupations.csv`](v3/outputs/graduate_regular_selected_occupations.csv)

Short version:

- among all graduate workers with a principal occupation, `farm_and_animal_work` and `sales_work` are both larger than the `software_and_engineering` bucket used in this project
- the single biggest occupation among graduate workers is `Market Gardeners & Crop Growers`
- even inside regular salaried work, shop salespersons are a large graduate occupation and a low-quality one

### 6. Tiny firms erase much of the graduate premium

Best files:

- [`v3/outputs/graduate_microfirm_penalty.csv`](v3/outputs/graduate_microfirm_penalty.csv)
- [`v3/outputs/strict_formality_by_workers_count.csv`](v3/outputs/strict_formality_by_workers_count.csv)

Short version:

- graduate earnings and job quality are dramatically worse in firms with fewer than `6` workers than in firms with `20+`

### 7. MGNREG is not the higher-paying casual-work option in this file

Best files:

- [`v3/outputs/casual_person_day_rural.csv`](v3/outputs/casual_person_day_rural.csv)
- [`v3/outputs/casual_person_day_rural_6_8h.csv`](v3/outputs/casual_person_day_rural_6_8h.csv)
- [`v3/outputs/casual_mgnreg_state_compare.csv`](v3/outputs/casual_mgnreg_state_compare.csv)

Short version:

- for rural men, MGNREG clearly pays less per hour than other casual work
- for rural women, the gap is smaller in the aggregate but still generally does not favor MGNREG
- state comparisons show that the national average hides sharp regional splits

## How The Analysis Was Done

The latest script is [`v3/analyze.py`](v3/analyze.py). It uses DuckDB to read the parquet directly and export story-ready CSVs.

The analysis strategy was:

1. profile the dataset and check basic quality
2. identify variables that can support unusual but understandable stories
3. build simple benchmark tables first
4. test whether surprising patterns survive alternative cuts
5. write only the findings that remained large, simple, and defensible

The strongest methods used in `v3` were:

- weighted shares using `Person Subsample Multiplier`
- comparison tables across sex, age, education, marital status, state, and household type
- conservative regression-style controls for the marriage and child-proxy stories
- person-day wage reconstruction from the 7-day diary
- occupation grouping for graduate mismatch

## Important Caveats

If you are writing from this project, do not skip this section.

- The weights are useful for shares and comparisons, but the raw weight scale does not look like direct headcounts. Treat percentage findings as stronger than absolute weighted totals.
- These are descriptive findings, not causal claims.
- The household-child analysis uses a co-residence proxy, not a direct motherhood field.
- The `strict formal` definition is a project choice, not an official PLFS category.
- The occupation mismatch buckets in `v3` are hand-built from readable occupation labels. They are simple and useful, but they are not a full occupational-skill taxonomy.
- Urban MGNREG and urban public-works samples are too small for a strong story.

For fuller caveats, read [`v3/notes.md`](v3/notes.md).

## How To Build A Report Or Data Story From This

If you are turning this into a story, the safest workflow is:

1. Pick one lead, not five.
2. Use `v3/insights.md` to understand the claim in plain English.
3. Pull the benchmark CSV and one or two supporting detail CSVs from `v3/outputs/`.
4. Add one concrete place, group, or occupation that makes the pattern tangible.
5. Include the main caveat in the body of the story, not in a footnote.

Example story packages:

- `Marriage + child burden + graduate women`
  Start with [`v3/outputs/marriage_weighted_model.csv`](v3/outputs/marriage_weighted_model.csv), then use [`v3/outputs/child_proxy_married_graduate_model.csv`](v3/outputs/child_proxy_married_graduate_model.csv) and [`v3/outputs/child_proxy_married_graduate_sex_compare_under2.csv`](v3/outputs/child_proxy_married_graduate_sex_compare_under2.csv).
- `Hidden work among homemakers`
  Start with [`v3/outputs/hidden_work_national_benchmark.csv`](v3/outputs/hidden_work_national_benchmark.csv), then use [`v3/outputs/hidden_work_weekly_work_composition.csv`](v3/outputs/hidden_work_weekly_work_composition.csv) and [`v3/outputs/hidden_work_state_mass.csv`](v3/outputs/hidden_work_state_mass.csv).
- `India’s “regular salaried” jobs are less formal than they sound`
  Start with [`v3/outputs/strict_formality_benchmark.csv`](v3/outputs/strict_formality_benchmark.csv), then use [`v3/outputs/nonformal_regular_top_occupations.csv`](v3/outputs/nonformal_regular_top_occupations.csv).
- `Graduate mismatch`
  Start with [`v3/outputs/graduate_worker_occupation_buckets.csv`](v3/outputs/graduate_worker_occupation_buckets.csv), then use [`v3/outputs/graduate_regular_selected_occupations.csv`](v3/outputs/graduate_regular_selected_occupations.csv) and [`v3/outputs/graduate_microfirm_penalty.csv`](v3/outputs/graduate_microfirm_penalty.csv).

## Version Guide

- [`v1/`](v1/) is the broad exploratory pass.
- [`v2/`](v2/) is the tighter, more publication-ready version.
- [`v3/`](v3/) is the current best synthesis and the recommended starting point.

If you only read one thing in the whole repository, read [`v3/insights.md`](v3/insights.md).
