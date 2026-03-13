# Prompts

## Download the data (Codex - gpt-5.4 xhigh)

Read https://github.com/Vonter/india-plf-survey
Find out how to download the full dataset (preferably as parquet) and how large the total download is.
Do not download it yet. I'm on a low-bandwidth connection and I want to plan the download for when I have better connectivity.

---

That seems small enough. Write and run a small script (bash is fine) that will download the dataset (if not present) and save it to the local directory.
Re-running should not re-download the data if it's already present.

## Analyze the data - v1

Analyze this PLFS data for newsworthy insights.

This is a dataset that people would have already analyzed extensively. So we need to find angles that are obscure, analyses that are niche, and insights that are surprising. The more surprising, the better - but they also need to be true and verifiable from the data.

Using the data-analysis skill, and catalog all insights that you find interesting in v1/insights.md. Write reproducible scripts to create intermediate / final outputs the analyses you perform -- all under v1/ . As you explore the data, if you find anything interesting, any anomalies or outliers, data quality issues, ideas for further analysis, etc., document them in v1/notes.md.

### Deepen analysis - v2

Deepen the analysis. Use the follow-up ideas in v1/notes.md as well.

Keep in mind that the analysis must ALSO be SIMPLE enough for a lay audience to understand quickly and easily. With that in mind, find the big, useful, surprising insights that are unlikely to be well known, and are strongly supported by the data. Use the data analysis skill.

Catalog all insights that you find interesting in v2/insights.md. Write reproducible scripts to create intermediate / final outputs the analyses you perform -- all under v2/ . As you explore the data, if you find anything interesting, any anomalies or outliers, data quality issues, ideas for further analysis, etc., document them in v2/notes.md.

## Document

Create a README.md that clearly explains what the dataset is, how it was analyzed, what the files are, etc. at enough detail for a layman to understand, and enough for them to create a detailed report / data story from the insights you found.
