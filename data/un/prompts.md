# Prompts

## Download the data

<!--
cd ~/code/journalists/data/un
dev.sh
codex --yolo --model gpt-5.4 --config model_reasoning_effort=medium
-->

Download all data from https://data.un.org/ efficiently.
It has an API. Learn how to use that.
Write a Python script that downloads all data and saves it in an efficient structured format (e.g. .csv).
Research the data available breadth-first, plan, then execute.
Prioritize downloading the most recent data first, and then work backwards in time.
Name the files that makes it easy to understand the content, and include the date. Use sub-directories if necessary to organize the data.
Ensure that the script is resumable, so that if it is interrupted, it can continue from where it left off without starting over.
Log progress and any errors encountered during the download process for troubleshooting purposes.
Run and test on a sample, then execute on larger batches. Run in parallel if that will help speed up the download.

---

Ensure that the script does not re-download (or even attempt it for) any data that exists unless `--force` is passed.
Run and test.

---

Document how to run the script, examples of usage, and arguments in README.md.

---

Document the data (structure, content) in README.md - even before documenting the data downloader.

<!-- codex resume 019d8a08-5cf0-7d80-97d3-54e7200867b5 -->

## Analysis

<!--
cd ~/code/journalists/data/un
dev.sh
copilot --yolo --model gpt-5.4 --effort xhigh
-->

Analyze this UN data for newsworthy insights.

This is a dataset that people would have already analyzed extensively. So we need to find angles that are obscure, analyses that are niche, and insights that are surprising. The more surprising, the better - but they also need to be true and verifiable from the data.

Keep in mind that the analysis must ALSO be SIMPLE enough for a lay audience to understand quickly and easily. With that in mind, find the big, useful, surprising insights that are unlikely to be well known, and are strongly supported by the data.

Using the data-analysis skill, and catalog all insights that you find interesting in v1/insights.md. Write reproducible scripts to create intermediate / final outputs the analyses you perform -- all under v1/ . As you explore the data, if you find anything interesting, any anomalies or outliers, data quality issues, ideas for further analysis, etc., document them in v1/notes.md.

---

Some of the insights are easy to understand, like:

- Some of the world's most gender-balanced parliaments are still old parliaments
- Ukraine now sits above Afghanistan in refugee-origin pressure

Some are more complex, like:

- Biodiversity Target 14 is moving, but mostly not fast enough (What's a Biodiversity Targe 14? Why do I care?)
- The UN's remittance-cost goal is still basically unmet (What is it and why do I care?)

Broaden the analysis with more insights that have universal appeal. The audience will be typical readers of the Times of India newspaper in India.

Search online for ideas others have thought of / done on such datasets, or even on this dataset but haven't implemented. Use the follow-up ideas in v1/notes.md as potential inputs.

Catalog all insights that you find interesting in v2/insights.md. Write reproducible scripts to create intermediate / final outputs the analyses you perform -- all under v2/ . As you explore the data, if you find anything interesting, any anomalies or outliers, data quality issues, ideas for further analysis, etc., document them in v2/notes.md.

---

Broaden the analysis with more insights. Search online for ideas others have thought of / done on such datasets, or even on this dataset but haven't implemented. Use the follow-up ideas in v2/notes.md as well.

Keep in mind that the analysis must ALSO be SIMPLE enough for a lay audience to understand quickly and easily. With that in mind, find the big, useful, surprising insights that are unlikely to be well known, and are strongly supported by the data. Use the data analysis skill.

Now you'll have even more insights. Catalog ALL insights that you find interesting in v3/insights.md. Write reproducible scripts to create intermediate / final outputs the analyses you perform -- all under v3/ . As you explore the data, if you find anything interesting, any anomalies or outliers, data quality issues, ideas for further analysis, etc., document them in v3/notes.md.

---

`.gitignore` all generated files. Only keep what's essential (e.g. insights.md, notes.md, scripts, anything LLM-generated and cannot be generated)

<!-- copilot --resume=86e60a6e-6405-4374-9f95-94782e973b19 -->
