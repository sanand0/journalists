#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright"]
# ///
from playwright.sync_api import sync_playwright
import pathlib

files = [
    "06-seed-crop-diversity",
    "07-migration-deaths-concentration",
    "08-youth-strategy-gap",
    "09-water-rules-vs-practice",
    "10-biodiversity-plans-vs-done",
]

base = pathlib.Path("/home/vscode/code/journalists/statnostics/2026-04-14-un-v3")

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name in files:
        svg_path = base / f"{name}.svg"
        svg = svg_path.read_text()
        page = browser.new_page(viewport={"width": 480, "height": 480})
        page.set_content(f'<html><body style="margin:0;padding:0;background:#fff">{svg}</body></html>')
        page.wait_for_timeout(800)
        page.screenshot(path=str(base / f"{name}.png"), clip={"x":0,"y":0,"width":480,"height":480})
        page.close()
        print(f"✓ {name}.png")
    browser.close()
print("All done")
