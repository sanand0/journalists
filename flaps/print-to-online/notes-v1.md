# Print-to-Online Flap Conversion — Notes v1

## What Are Flaps?

Flaps are large-format print infographics published in the Times of India. They are produced in Adobe Illustrator (exported as PDF + SVG) in a tall newspaper column format — typically ~930px wide × ~1400–1500px tall at 72dpi. They contain:

- A main headline and byline
- Dense data visualizations (bar charts, line charts, area charts, tables, maps)
- Illustrated characters/icons
- Print-specific typography (Poynter Agate, Griffith Gothic — fonts not available on web)
- Multiple sections packed into a single vertical column

**Why they don't work online as-is:**
- Too tall for screen — readers would scroll through a wall of content
- Print fonts won't render on web browsers
- SVG files are 4–6MB (hundreds of individually positioned characters from Illustrator's kerning)
- Text is split character-by-character in SVG (impossible to extract cleanly)
- Static image embed would be unreadable on mobile

---

## Approach

### Step 1: Extract Content

Text extraction from the SVG files is **not viable** — Adobe Illustrator exports each glyph as a separate `<tspan>` element. Instead, use `pdftotext` with the `-layout` flag on the corresponding PDF:

```bash
pdftotext -layout "originals/Green Power-R3.pdf" -
```

This gives well-structured columnar text, preserving the multi-column layout. The data values, headlines, and captions all come through cleanly.

### Step 2: Visual Reference

Convert PDFs to images to understand the visual design:

```bash
pdftoppm -r 72 "originals/Green Power-R3.pdf" /tmp/greenpower
magick /tmp/greenpower-1.ppm /tmp/greenpower.jpg
```

View the JPG to understand layout, chart types, illustrations, and colour scheme.

### Step 3: Reconstruct as HTML

For each flap, create a standalone HTML file with:
- **All CSS and JS embedded** (no build step, drop-in publishable)
- **Web fonts** loaded from Google Fonts (matching the newspaper aesthetic)
- **Responsive layout** — max-width 700px, single column, mobile-first
- **Animated charts** — CSS bars, SVG line charts, IntersectionObserver triggers
- **TOI brand colour** (`#ed1c24`) used sparingly for badges/labels
- **Each flap gets its own distinct aesthetic** to reflect its editorial tone

---

## Three Conversions Produced

### 1. `output/green-power.html`
**Story:** How India Bridged Energy Gap With Green Power (Atul Thakur)
**Design:** White background, `#ed1c24` red accents, green chart fills — clean TOI editorial style
**Fonts:** Rethink Sans (TOI's actual font, from Google Fonts)
**Approach:** Scroll-driven narrative — IntersectionObserver triggers bar animations and SVG line-draw as you scroll
**Charts:** Country comparison bars (India highlighted red), household electrification SVG line, per capita SVG line, stacked capacity bar, coal-vs-renewables callout cards

### 2. `output/us-university-funding.html`
**Story:** Which US univs will Trump's funding cuts hurt the most? (Richa Gandhi)
**Design:** White background, `#ed1c24` red for highlights, `#f6f6f6` chart backgrounds — data-journalism TOI style
**Fonts:** Rethink Sans
**Approach:** Data-forward with CSS staggered bar animations on load (no IntersectionObserver needed)
**Charts:** Top-10 proposed cuts horizontal bars, 2023 federal funding bars, then-vs-now dependency comparison (gray vs green bars), STEM field breakdown bars

### 3. `output/iran-oil-travel.html`
**Story:** Oil To Travel: Pain Points For India Amid War In Gulf (Saurabh Sinha)
**Design:** White body with narrow `#ed1c24` breaking-news bar at very top — urgent but editorial
**Fonts:** Rethink Sans
**Approach:** Breaking news article with data panels integrated — bullet list (fixed CSS bug), side-by-side passenger flows, styled NRI table, oil import bars, declining Nifty SVG chart
**Charts:** Remittances stacked bar, NRI table, oil imports bars (Gulf in red), Nifty50 SVG line chart

---

## How to Run / Publish

Each HTML file is fully self-contained (single file, no dependencies except Google Fonts CDN). To preview:

```bash
# Option 1: Python server
python3 -m http.server 8000
# then open http://localhost:8000/output/green-power.html

# Option 2: Open directly
open output/green-power.html
```

For TOI publication:
- Embed the `<style>` block and HTML body directly into TOI's CMS
- Or embed as an `<iframe>` pointing to the hosted file
- Google Fonts load from `fonts.googleapis.com` — requires internet access

---

## Questions for Feedback

### On structure/length
1. **How long should the online version be?** Currently each file is roughly 3–4 "screens" of content when scrolled. Should it be shorter (2 screens max) or is longer OK if well-structured?
2. **Should we retain all sections from the print flap**, or aggressively cut to only the 2–3 most important data points?
3. **Is a single-scroll story the right format**, or would a tabbed/paginated layout (like a carousel) work better for TOI's CMS?

### On charts
4. **Should charts be interactive** (hover for tooltips, clickable)? Or is static-animated sufficient for your CMS/audience?
5. **Can the output rely on JavaScript?** If TOI's CMS strips `<script>` tags, pure CSS animations + static SVG is the safer choice.
6. **What chart library (if any) is TOI already using** on data story pages? (Chart.js, Highcharts, D3, Flourish?) We could match that.

### On design
7. **Should all flaps share one visual style** (consistent TOI brand template) or have individual aesthetics as I've done here?
8. **Is the dark theme suitable** for TOI's website (light background, white articles)? The dark look may clash with surrounding page chrome.
9. **Font preference:** Should we use TOI's own web fonts (if licensed), system fonts, or Google Fonts?
10. **What's the target column width?** TOI article bodies appear to be ~660–680px wide based on general analysis — is that right?

### On workflow
11. **How often are flaps published?** This informs whether we should build a reusable script vs. doing each manually.
12. **Is AI-assisted content restructuring acceptable?** (i.e., can we use an LLM to summarise or rewrite the intro text for web?) Or must the text be verbatim from the original?
13. **Who runs the conversion?** A journalist who can tweak HTML, or a developer? This affects how automated/configurable the pipeline should be.
14. **Should the SVG illustration characters** (e.g., the king in the Incumbency flap, the Japanese grandfather in the Japan flap) be extracted and preserved? Or replaced with photos/icons?

### On the originals
15. **Do we always get both PDF and SVG?** Or sometimes only one format?
16. **Are the data values always available in a structured format** (spreadsheet) alongside the flap, or must they always be extracted from the PDF?

---

## What's Next (After Feedback)

Once you review the three samples and answer the questions above, I can:

1. **Create a conversion template** — a base HTML/CSS framework customised for TOI that all flaps slot into
2. **Write a Python extraction script** — reads PDF, extracts text blocks, identifies chart data, outputs structured JSON
3. **Build a prompt-based pipeline** — feeds JSON + image reference to an LLM to generate the HTML section by section
4. **Automate the workflow** — single command `convert.sh <flap.pdf>` outputs a publish-ready HTML file

---

## v2 — Visual Audit & TOI Alignment (2026-04-10)

### Method

Used Python Playwright (`playwright.sync_api`) to:
1. Screenshot each generated HTML file at 1280×900 (desktop) and 390×844 (mobile)
2. Visit a live TOI article and extract computed CSS styles via `page.evaluate()`
3. Compare screenshots side-by-side

```bash
# Install playwright
uv pip install playwright
python3 -m playwright install chromium

# Serve files locally
python3 -m http.server 8765

# Screenshot script
python3 screenshot.py  # see approach above
```

---

### Findings from TOI Inspection

Inspected: `timesofindia.indiatimes.com/technology/tech-news/explained-why-anthropics-claude-mythos-...`

| Property | TOI Actual Value | v1 Used | Fixed |
|---|---|---|---|
| Font family | `"Rethink Sans", -apple-system, BlinkMacSystemFont, "Helvetica Neue", "Segoe UI", sans-serif` | Playfair Display / EB Garamond / Barlow | ✅ |
| Background | `#ffffff` | `#080e1c` / `#fef9f0` / `#0d0d0d` | ✅ |
| Body text | `16px / 28px` | `15px / 22px` | ✅ |
| Text color | `#1a1a1a` (rgb 26,26,26) | `#1a1a1a` | ✅ |
| Muted color | `#595959` (rgb 89,89,89) | `#666666` | ✅ |
| H1 | `28px / 36px / 700` | `28px / 36px / 700` | ✅ (was already correct) |
| H2 (section) | `20px / 28px / 700` | `20px / 28px / 700` | ✅ (was already correct) |
| Article column width | `670px` | `680px` | ✅ (close enough) |
| Chart backgrounds | `#f6f6f6` | dark colors | ✅ |
| Red accent | `#ed1c24` | `#e53935` / `#991b1b` / `#f97316` | ✅ |

---

### Bugs Fixed

#### 1. Iran flap — word-per-line bullet text bug
**Root cause:** `<li>` elements were styled with `display: grid; grid-template-columns: 10px 1fr`. In CSS Grid, each direct child becomes a grid item. The `::before` pseudo-element occupied column 1, `<strong>` occupied column 2 of row 1, and the trailing text node became an implicit grid item placed in row 2 column 1 — which was only 10px wide, forcing every word to wrap onto its own line.

**Fix:** Replaced grid layout with `position: relative; padding-left: 28px` on `<li>` and `position: absolute; left: 10px` on `::before`.

#### 2. All files — Wrong theme (dark vs. light)
**Root cause:** v1 used custom dark/creative themes (navy, black, cream). TOI's CMS pastes content into a white article page — dark backgrounds clash with surrounding chrome.

**Fix:** All three files rebuilt with `background: #ffffff`, no decorative gradients or star-fields.

#### 3. All files — Wrong fonts
**Root cause:** v1 used Playfair Display, EB Garamond, and Barlow Condensed for creative differentiation. TOI actually uses `Rethink Sans` (available on Google Fonts).

**Fix:** All three files now load `Rethink Sans` via `<link>` or `@import` from `fonts.googleapis.com`.

#### 4. All files — Body text size
**Root cause:** Initial assumption was that TOI used 14px body text (measured from navigation items). The actual article body uses `16px / 28px`.

**Fix:** Updated `body`, `.intro`, `.subhead`, `.section-desc`, `.news-list li` from `15px / 22px` to `16px / 28px`.

#### 5. All files — Muted text color
**Root cause:** v1 used `#666666` as the muted/caption color. TOI uses `rgb(89, 89, 89)` = `#595959` for secondary text elements.

**Fix:** Global replace `#666666` → `#595959` across all three files.

---

### Design Decisions (Post-Audit)

- **Red accent `#ed1c24`** used only for: "TIMES SPECIAL" badge, section label supertitles, highlighted bar (top ranked item per chart), `border-top` on stat cards. Everywhere else uses `#1a1a1a` or `#595959`.
- **Chart backgrounds** → `#f6f6f6` (TOI's secondary surface color, seen on ad containers and callout boxes)
- **Section dividers** → `border-bottom: 2px solid #1a1a1a` on `h2` (bold underline style)
- **Bar chart highlight logic** → Top row or India row gets `#ed1c24`; all others use `#374151` (dark gray, not black)
- **Stat strip cards** → `border-top: 3px solid #ed1c24` (echoes TOI's red emphasis style)
- **Breaking news bar** (Iran only) → Full-bleed `#ed1c24` bar at very top, then white body — matches how TOI renders "breaking" labels
- **SVG line charts** → Area fills use tinted versions of the line color (green for households %, amber for per capita, red for Nifty50 decline)

---

### Responsive Notes

Tested at 390×844 (iPhone 14 Pro). All three pages:
- Stat strips collapse from 3-col → 2-col grid at ≤480px
- Bar chart label columns shrink from 160px → 120px
- Two-column panels (passenger flows, dependency comparison) stack to single column
- H1 reduces from 28px → 24px / line-height 30px

---

### Remaining Open Questions (Unchanged from v1)

Questions 1–16 from the previous section still apply. Additionally:

17. **Does TOI's CMS preserve `<link rel="stylesheet">` tags?** If not, the Google Fonts import must use `<style>@import url(...)</style>` instead — or fonts must be self-hosted.
18. **Does the CMS strip `<script>` tags?** The bar animations use `IntersectionObserver` via inline `<script>`. If scripts are stripped, animations won't trigger (bars stay at width 0). A CSS-only fallback using `animation-delay` without IntersectionObserver would be safer.
19. **Is there a maximum file size for CMS paste?** The HTML files are 28–37KB — small, but worth confirming.

*Updated: 2026-04-10*

---

## v3 — Three New Conversions + SKILL.md (2026-04-10)

### New Files Produced

#### 4. `output/nri-money.html`
**Source:** `originals/NRI money.svg` (SVG only — no PDF available)
**Story:** NRI Cash In Indian Banks Is Rising (Richa Gandhi)
**Extraction method:** `rsvg-convert -w 1200` for visual rendering; partial Python ElementTree for numbers
**Design:** Standard TOI white layout, breaking bar ("TIMES SPECIAL · ECONOMY"), vertical bar chart for 7-year inflows, stacked deposit composition bar (NRE/FCNR(B)/NRO), definition cards, dark callout box for 52× growth stat
**Key charts:** Vertical bar (2019–2025 NRI inflows), stacked bar (deposit type breakdown), two stat comparison cards (rupee terms vs dollar terms)

#### 5. `output/japan-growth.html`
**Source:** `originals/Flap-Japan growth.pdf`
**Story:** Is Japan the Future of Every Country? (Chandrima Banerjee)
**Design:** Standard TOI white layout, 3-card problem grid, multiple horizontal bar charts (wages, inflation, interest rates), country ageing data list, country comparison table
**Bug fixed:** Original agent used `opacity: 0` on section containers (`.animate-in` class). Elements below the viewport remained invisible. Fix: removed `opacity: 0` from CSS entirely; bars animate via CSS `@keyframes barGrow` with `animated` class set directly in HTML — no JavaScript needed for horizontal bars.

#### 6. `output/inactive-firms.html`
**Source:** `originals/Inactive_Firm-R2.pdf`
**Story:** India has 383 Govt-Run Firms That Do Nothing (data analysis)
**Design:** Standard TOI white layout, large "18%" percentage callout, state data table (2007 vs 2023), ₹5,700 Cr stat card, numbered closure steps with red circles, Finance Commission timeline

---

### Bug Found and Fixed: `opacity: 0` on Section Containers

**Pattern to avoid:** Using `opacity: 0` in CSS on any element, then revealing it via IntersectionObserver.

**Root cause:** IntersectionObserver fires based on viewport intersection. In full-page screenshots, below-fold elements are never "intersected" — they stay invisible. In browsers, fast scrollers may also miss the trigger.

**Fix applied to japan-growth.html:** Removed `.animate-in { opacity: 0 }` entirely. Bars already had the `animated` class in their HTML, so CSS `@keyframes barGrow` runs on page load without any JavaScript. The page is always fully visible.

**Rule for future conversions:** Never hide section containers with `opacity: 0`. If IntersectionObserver is used, only animate properties that start at 0 (like `height: 0` for vertical bars, `width: 0` for horizontal bars). These don't affect readability if the observer doesn't fire.

---

### SKILL.md Created

`SKILL.md` documents the full conversion process:
- Content extraction (PDF vs SVG-only)
- Visual reference workflow
- TOI design system (exact values for all properties)
- HTML structure patterns (badge, section, stat cards)
- Chart patterns (horizontal bar, vertical bar, SVG line, stacked, table, bullet list)
- Responsive breakpoints
- Quality checklist (25 items)
- Common pitfalls table (10 pitfalls with fixes)
- Full example workflow with bash commands

*Updated: 2026-04-10*
