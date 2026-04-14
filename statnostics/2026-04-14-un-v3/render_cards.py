"""Render all 5 UN-v3 SVG cards to PNG using Playwright."""
from playwright.sync_api import sync_playwright
from pathlib import Path

out_dir = Path("/home/vscode/code/journalists/statnostics/2026-04-14-un-v3")

svgs = [
    "01-remittance-cost-gap.svg",
    "02-ukraine-refugee-rate.svg",
    "03-livestock-no-backup.svg",
    "04-india-productivity-growth.svg",
    "05-parliament-below-both-medians.svg",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for svg_name in svgs:
        svg_path = out_dir / svg_name
        png_path = out_dir / svg_name.replace(".svg", ".png")
        svg_content = svg_path.read_text()
        page = browser.new_page(viewport={"width": 480, "height": 480})
        page.set_content(f'<html><body style="margin:0;padding:0;background:#fff">{svg_content}</body></html>')
        page.wait_for_timeout(800)
        page.screenshot(path=str(png_path))
        page.close()
        print(f"Saved {png_path.name}")
    browser.close()

print("All done.")
