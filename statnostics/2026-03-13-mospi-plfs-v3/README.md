# MOSPI PLFS v3 Statoistics cards

This folder contains the final SVG cards for the PLFS v3 package, plus a matching verification SOP for each card.

## What is in this folder

- `*.svg` — the finished print-ready Statoistics cards
- `*.md` — the fact-checking and verification SOP for the matching card

Each SOP is named to match its SVG basename, so reviewers can open the card and its verification note side by side.

## Recommended workflow

1. Open the card SVG.
2. Open the matching SOP markdown file.
3. Use the SOP's search strings, CSV row filters, and checklist to verify the claim before publication or revision.

## Source material

- [PLFS workspace README](../../data/mospi-plfs/README.md)
- [PLFS v3 insights](../../data/mospi-plfs/v3/insights.md)
- [PLFS v3 outputs](../../data/mospi-plfs/v3/outputs/)
- [PLFS v3 analysis script](../../data/mospi-plfs/v3/analyze.py)

## Card index

| # | Topic | Card | Verification SOP | Main editorial claim |
|---|---|---|---|---|
| 01 | Marriage and women's work | [01-marriage-labor-market-cliff.svg](./01-marriage-labor-market-cliff.svg) | [01-marriage-labor-market-cliff.md](./01-marriage-labor-market-cliff.md) | Among urban graduate women in salaried households, marriage is linked to a sharp move from salaried work to domestic duties. |
| 02 | Hidden homemaker work | [02-hidden-homemaker-work.svg](./02-hidden-homemaker-work.svg) | [02-hidden-homemaker-work.md](./02-hidden-homemaker-work.md) | Many women coded as homemakers still show up as workers in PLFS current-week data, mostly in family-enterprise work. |
| 03 | Formality gap | [03-regular-jobs-not-formal.svg](./03-regular-jobs-not-formal.svg) | [03-regular-jobs-not-formal.md](./03-regular-jobs-not-formal.md) | Only about one in three regular salaried jobs passes a strict formality test. |
| 04 | Graduate mismatch | [04-graduate-mismatch.svg](./04-graduate-mismatch.svg) | [04-graduate-mismatch.md](./04-graduate-mismatch.md) | More graduate workers are in farm-and-animal work than in the project's software-and-engineering bucket. |
| 05 | Employer-size penalty | [05-microfirm-earnings-gap.svg](./05-microfirm-earnings-gap.svg) | [05-microfirm-earnings-gap.md](./05-microfirm-earnings-gap.md) | Urban graduates in tiny firms earn much less, and face much worse job quality, than graduates in large firms. |
| 06 | MGNREG wage comparison | [06-mgnreg-pays-less.svg](./06-mgnreg-pays-less.svg) | [06-mgnreg-pays-less.md](./06-mgnreg-pays-less.md) | In rural men's diary data, MGNREG pays less per hour than other casual work. |
| 07 | School-exit gender split | [07-school-dropout-gender-split.svg](./07-school-dropout-gender-split.svg) | [07-school-dropout-gender-split.md](./07-school-dropout-gender-split.md) | Among currently married youth aged 18-24 who are no longer attending school, women and men report sharply different reasons. |

## Notes for editors

- These cards are based on `PLFS 2024` analysis in `data/mospi-plfs/v3/`.
- The verification files are designed for newsroom use: they point to exact CSVs, subgroup filters, rounding rules, and common misreads.
- Some cards use project-defined groupings or conservative proxies. When that happens, the matching SOP explains the definition and where it comes from in `analyze.py`.
