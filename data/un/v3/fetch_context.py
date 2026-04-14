#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.28",
#   "lxml>=5.3",
#   "pandas>=2.2",
#   "rich>=14.0",
# ]
# ///

"""Fetch the public context pages used to frame the v3 analysis."""

from __future__ import annotations

import re
from pathlib import Path

import httpx
import pandas as pd
from lxml import html
from rich.traceback import install

install(show_locals=True)

BASE_DIR = Path(__file__).resolve().parent
RESEARCH_DIR = BASE_DIR / "research"
RAW_DIR = RESEARCH_DIR / "raw"

SOURCES = [
    {
        "key": "remittances_un",
        "topic": "remittances",
        "url": "https://www.un.org/en/observances/remittances-day/SDGs",
        "note": "Used to explain why the 3% fee target matters for family budgets.",
    },
    {
        "key": "migration_deaths_un_sdg",
        "topic": "migration deaths",
        "url": "https://sdgs.un.org/partnerships/measuring-safe-migration-collection-global-data-migrant-fatalities-indicator-1073",
        "note": "Used to frame migration-death counts as minimum estimates and to explain why the Missing Migrants dataset matters.",
    },
    {
        "key": "women_parliament_un_news",
        "topic": "parliament representation",
        "url": "https://news.un.org/en/story/2026/03/1167092",
        "note": "Used to contrast the familiar women-in-parliament angle with the less-covered youth angle in the local slice.",
    },
    {
        "key": "productivity_worldbank",
        "topic": "productivity",
        "url": "https://www.worldbank.org/en/research/publication/global-productivity",
        "note": "Used to explain why worker-productivity growth is a broad public-interest metric.",
    },
    {
        "key": "water_participation_unep",
        "topic": "water participation",
        "url": "https://sdgs.unep.org/article/sdg-indicator-6b1",
        "note": "Used to explain that the water indicator compares formal participation procedures with actual community participation in water management.",
    },
    {
        "key": "plant_treaty_datastore",
        "topic": "plant genetic resources",
        "url": "https://www.fao.org/plant-treaty/areas-of-work/the-multilateral-system/datastore/en/",
        "note": "Used to explain that SMTAs track crop-gene transfers within the treaty's multilateral seed-sharing system.",
    },
    {
        "key": "plant_treaty_stats",
        "topic": "plant genetic resources",
        "url": "https://mls.planttreaty.org/itt/index.php?r=stats/pubStats",
        "note": "Used to verify that the treaty datastore publishes aggregate germplasm-flow totals and regional recipient counts.",
    },
    {
        "key": "animal_genetics_fao",
        "topic": "animal genetic resources",
        "url": "https://www.fao.org/animal-genetics/breed-database/indicators/sdg-indicators/en/",
        "note": "Used to explain that the livestock backup indicator counts breeds with enough stored genetic material to reconstitute them.",
    },
    {
        "key": "dad_is_data",
        "topic": "animal genetic resources",
        "url": "https://www.fao.org/dad-is/data/en/",
        "note": "Used to show that FAO's DAD-IS system exposes breed-risk and cryoconservation data behind the animal-genetic indicators.",
    },
]


def squash_whitespace(text: str) -> str:
    """Collapse repeated whitespace."""

    return re.sub(r"\s+", " ", text).strip()


def first_text(document: html.HtmlElement, xpath: str) -> str:
    """Return the first xpath text result, or an empty string."""

    values = document.xpath(xpath)
    if not values:
        return ""

    value = values[0]
    if isinstance(value, str):
        return squash_whitespace(value)

    return squash_whitespace(value.text_content())


def build_excerpt(document: html.HtmlElement) -> str:
    """Create a compact excerpt from the first few paragraphs on the page."""

    snippets: list[str] = []
    for paragraph in document.xpath("//main//p | //article//p | //div[@id='main-content']//p | //p"):
        text = squash_whitespace(paragraph.text_content())
        if len(text) < 60:
            continue

        snippets.append(text)
        if sum(len(item) for item in snippets) >= 700:
            break

    return squash_whitespace(" ".join(snippets))[:900]


def fetch_one(client: httpx.Client, source: dict[str, str]) -> dict[str, str]:
    """Fetch a page, cache the raw HTML, and return extracted metadata."""

    response = client.get(source["url"], timeout=90, follow_redirects=True)
    response.raise_for_status()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / f"{source['key']}.html"
    raw_path.write_text(response.text, encoding="utf-8")

    document = html.fromstring(response.content)
    title = first_text(document, "//title/text()") or first_text(document, "//h1")
    meta_description = first_text(
        document,
        "//meta[@name='description']/@content | //meta[@property='og:description']/@content",
    )

    return {
        "key": source["key"],
        "topic": source["topic"],
        "url": source["url"],
        "title": title,
        "meta_description": meta_description,
        "excerpt": build_excerpt(document),
        "note": source["note"],
        "raw_html_path": raw_path.relative_to(BASE_DIR).as_posix(),
    }


def main() -> None:
    """Fetch all configured context sources."""

    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(headers={"User-Agent": "Mozilla/5.0"}) as client:
        records: list[dict[str, str]] = []
        for source in SOURCES:
            try:
                records.append(fetch_one(client, source))
            except httpx.HTTPError as error:
                records.append(
                    {
                        "key": source["key"],
                        "topic": source["topic"],
                        "url": source["url"],
                        "title": "",
                        "meta_description": "",
                        "excerpt": "",
                        "note": source["note"],
                        "raw_html_path": "",
                        "fetch_error": str(error),
                    }
                )

    frame = pd.DataFrame(records).sort_values(["topic", "key"]).reset_index(drop=True)
    frame.to_csv(RESEARCH_DIR / "context_sources.csv", index=False)
    frame.to_json(RESEARCH_DIR / "context_sources.json", orient="records", indent=2)


if __name__ == "__main__":
    main()
