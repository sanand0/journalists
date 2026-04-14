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

"""Fetch and parse SDMX metadata for the local UN data slices."""

from __future__ import annotations

from pathlib import Path

import httpx
import pandas as pd
from lxml import etree
from rich.traceback import install

install(show_locals=True)

BASE_DIR = Path(__file__).resolve().parent
METADATA_DIR = BASE_DIR / "metadata"
RAW_DIR = METADATA_DIR / "raw"

NS = {
    "message": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}

STRUCTURES = [
    {
        "name": "sdg",
        "agency": "IAEG-SDGs",
        "structure_id": "SDG",
        "version": "1.24",
    },
    {
        "name": "na_main",
        "agency": "ESTAT",
        "structure_id": "NA_MAIN",
        "version": "1.9",
    },
    {
        "name": "na_sec",
        "agency": "ESTAT",
        "structure_id": "NA_SEC",
        "version": "1.9",
    },
]


def text_or_blank(node: etree._Element | None, xpath: str) -> str:
    """Return the first text match for an xpath, or an empty string."""

    if node is None:
        return ""

    values = node.xpath(xpath, namespaces=NS)
    return str(values[0]).strip() if values else ""


def fetch_xml(client: httpx.Client, config: dict[str, str]) -> bytes:
    """Fetch a datastructure XML document, using a local cache when present."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / f"{config['name']}.xml"
    if target.exists():
        return target.read_bytes()

    url = (
        "https://data.un.org/ws/rest/datastructure/"
        f"{config['agency']}/{config['structure_id']}/{config['version']}?references=all"
    )
    response = client.get(url, timeout=90)
    response.raise_for_status()
    target.write_bytes(response.content)
    return response.content


def parse_dimensions(root: etree._Element, config: dict[str, str]) -> pd.DataFrame:
    """Extract dimension definitions and their attached codelists."""

    rows: list[dict[str, str]] = []
    for dimension in root.xpath(
        ".//structure:DataStructureComponents/structure:DimensionList/structure:Dimension",
        namespaces=NS,
    ):
        enum_ref = dimension.xpath(
            "./structure:LocalRepresentation/structure:Enumeration/Ref/@id",
            namespaces=NS,
        )
        concept_ref = dimension.xpath(
            "./structure:ConceptIdentity/Ref/@id",
            namespaces=NS,
        )
        rows.append(
            {
                "structure_name": config["name"],
                "agency": config["agency"],
                "structure_id": config["structure_id"],
                "structure_version": config["version"],
                "dimension_id": dimension.get("id", ""),
                "concept_id": concept_ref[0] if concept_ref else "",
                "codelist_id": enum_ref[0] if enum_ref else "",
                "position": dimension.get("position", ""),
            }
        )

    return pd.DataFrame(rows)


def parse_codelists(root: etree._Element, config: dict[str, str]) -> pd.DataFrame:
    """Extract code/value labels from every codelist in a datastructure bundle."""

    rows: list[dict[str, str]] = []
    for codelist in root.xpath(".//structure:Codelist", namespaces=NS):
        codelist_id = codelist.get("id", "")
        codelist_name = text_or_blank(codelist, "./common:Name/text()")
        for code in codelist.xpath(".//structure:Code", namespaces=NS):
            parent = code.getparent()
            parent_id = parent.get("id", "") if parent is not None and parent.tag.endswith("Code") else ""
            rows.append(
                {
                    "structure_name": config["name"],
                    "agency": config["agency"],
                    "structure_id": config["structure_id"],
                    "structure_version": config["version"],
                    "codelist_id": codelist_id,
                    "codelist_name": codelist_name,
                    "code": code.get("id", ""),
                    "label": text_or_blank(code, "./common:Name/text()"),
                    "description": text_or_blank(code, "./common:Description/text()"),
                    "parent_code": parent_id,
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    """Write parsed SDMX dimensions and codelists to CSV files."""

    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(follow_redirects=True) as client:
        all_dimensions: list[pd.DataFrame] = []
        all_codes: list[pd.DataFrame] = []

        for config in STRUCTURES:
            root = etree.fromstring(fetch_xml(client, config))
            dimensions = parse_dimensions(root, config)
            codes = parse_codelists(root, config)

            dimensions.to_csv(METADATA_DIR / f"{config['name']}_dimensions.csv", index=False)
            codes.to_csv(METADATA_DIR / f"{config['name']}_codes.csv", index=False)

            all_dimensions.append(dimensions)
            all_codes.append(codes)

        pd.concat(all_dimensions, ignore_index=True).to_csv(
            METADATA_DIR / "all_dimensions.csv",
            index=False,
        )
        pd.concat(all_codes, ignore_index=True).to_csv(
            METADATA_DIR / "all_codes.csv",
            index=False,
        )


if __name__ == "__main__":
    main()
