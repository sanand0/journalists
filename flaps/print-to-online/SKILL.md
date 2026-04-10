# SKILL: Convert a Print Flap to TOI Online HTML

A flap is a large-format print infographic (~930 × 1400–1500 px at 72 dpi) produced in Adobe Illustrator and published in the Times of India. This skill converts one into a self-contained, responsive HTML file that looks native in TOI's CMS.

---

## Overview

**Input:** `originals/<Flap Name>.pdf` and/or `originals/<Flap Name>.svg`
**Output:** `output/<flap-name>.html` — single file, no external dependencies except Google Fonts

**Goal:** The HTML, when pasted into TOI's CMS, should be visually indistinguishable from TOI's own article HTML.

---

## Step 1: Extract Content

### If a PDF is available (preferred)

```bash
pdftotext -layout "originals/Flap Name.pdf" -
```

The `-layout` flag preserves columnar alignment. This gives clean, structured text: headlines, section titles, data values, captions, bylines. Copy the full output to use as reference.

### If only SVG is available

Adobe Illustrator exports each character as a separate `<tspan>` — text extraction is not viable. Instead:

1. Render the SVG to an image:
   ```bash
   rsvg-convert -w 1200 "originals/Flap Name.svg" > /tmp/flap.png
   ```
2. View the image with the Read tool to read content visually.
3. Supplement with partial Python extraction for numbers/labels:
   ```bash
   python3 -c "
   import xml.etree.ElementTree as ET
   tree = ET.parse('originals/Flap Name.svg')
   ns = {'svg': 'http://www.w3.org/2000/svg'}
   texts = [t.text for t in tree.iter('{http://www.w3.org/2000/svg}tspan') if t.text and t.text.strip()]
   print('\n'.join(texts[:200]))
   "
   ```

---

## Step 2: Visual Reference

Convert the PDF to an image to understand layout, chart types, colours, and illustration style:

```bash
pdftoppm -r 72 "originals/Flap Name.pdf" /tmp/flap
magick /tmp/flap-1.ppm /tmp/flap.jpg
```

View the image with the Read tool. Note:
- Section count and order
- Chart types (horizontal bar, vertical bar, line, stacked, table, map)
- Which data point is highlighted/emphasised
- Any illustrated characters (currently: describe in text; don't try to extract SVG paths)
- Colour scheme of the original (for editorial tone reference only — final HTML uses TOI palette)

---

## Step 3: Write the HTML

### File structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Headline] — Times of India</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rethink+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>
  /* all CSS here */
</style>
</head>
<body>
  <!-- all HTML here -->
  <script>/* all JS here */</script>
</body>
</html>
```

Everything — CSS, HTML, JS — lives in one file. No external scripts. No build step.

---

## TOI Design System

Copy these values exactly. Do not invent alternatives.

| Property | Value |
|---|---|
| **Font family** | `'Rethink Sans', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'Segoe UI', sans-serif` |
| **Body text** | `font-size: 16px; line-height: 28px; font-weight: 400` |
| **Body color** | `#1a1a1a` |
| **Background** | `#ffffff` |
| **Muted/caption text** | `#595959` |
| **Red accent** | `#ed1c24` |
| **H1** | `font-size: 28px; font-weight: 700; line-height: 36px` |
| **H2 (section)** | `font-size: 20px; font-weight: 700; line-height: 28px` |
| **H2 underline** | `border-bottom: 2px solid #1a1a1a; padding-bottom: 8px` |
| **Content width** | `max-width: 680px; margin: 0 auto; padding: 0 16px 60px` |
| **Chart background** | `#f6f6f6` |
| **Bar (default)** | `#374151` (dark gray) |
| **Bar (highlighted)** | `#ed1c24` |
| **Bar track** | `#e5e7eb` |
| **Section spacing** | `margin-bottom: 40px` |

### Red accent usage — be sparing

Use `#ed1c24` ONLY for:
- "TIMES SPECIAL" badge border and text
- Section label supertitles
- The highest-value / India-highlighted bar in a chart
- `border-top: 3px solid #ed1c24` on stat cards
- Breaking news bar (full-bleed) — only for breaking news stories

Everywhere else: use `#1a1a1a` or `#595959`.

---

## Required CSS Reset

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: #ffffff;
  color: #1a1a1a;
  font-family: 'Rethink Sans', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'Segoe UI', sans-serif;
  font-size: 16px;
  line-height: 28px;
  -webkit-font-smoothing: antialiased;
}
```

---

## HTML Structure Patterns

### Badge + headline block

```html
<div class="badge">TIMES SPECIAL</div>
<h1>[Headline]</h1>
<p class="intro">[One-sentence summary of the story]</p>
<p class="byline">By [Author Name]</p>
```

```css
.badge {
  display: inline-block;
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: #ed1c24; border: 1.5px solid #ed1c24;
  padding: 2px 8px; border-radius: 2px; margin-bottom: 12px;
}
h1 { font-size: 28px; font-weight: 700; line-height: 36px; color: #1a1a1a; margin-bottom: 14px; }
.intro { font-size: 16px; line-height: 28px; margin-bottom: 16px; }
.byline { font-size: 13px; font-weight: 600; color: #595959; padding-bottom: 16px;
          border-bottom: 1px solid #e0e0e0; margin-bottom: 24px; }
```

### Section header

```html
<section>
  <h2>[Section Title]</h2>
  <p class="section-desc">[1–2 sentence context]</p>
  <!-- charts -->
</section>
```

### Stat card strip (2–4 big numbers)

```html
<div class="stat-strip">
  <div class="stat-card">
    <div class="stat-num">[value]</div>
    <div class="stat-label">[label]</div>
  </div>
  <!-- repeat -->
</div>
```

```css
.stat-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin: 20px 0; }
.stat-card { background: #f6f6f6; border-top: 3px solid #ed1c24; padding: 16px; }
.stat-num { font-size: 32px; font-weight: 800; color: #1a1a1a; line-height: 1.1; }
.stat-label { font-size: 12px; color: #595959; line-height: 16px; margin-top: 4px; }
```

---

## Chart Patterns

### Horizontal bar chart (most common)

Highlight the top-ranked item (or India, if country comparison) in red. All others in `#374151`.

```html
<div class="chart">
  <div class="bar-row">
    <div class="bar-label highlight">India</div>
    <div class="bar-track">
      <div class="bar-fill highlight" style="--w: 85%; --i: 0"></div>
    </div>
    <div class="bar-value">85%</div>
  </div>
  <div class="bar-row">
    <div class="bar-label">China</div>
    <div class="bar-track">
      <div class="bar-fill" style="--w: 72%; --i: 1"></div>
    </div>
    <div class="bar-value">72%</div>
  </div>
</div>
<p class="chart-note">Source: [source]</p>
```

```css
.chart { background: #f6f6f6; padding: 14px 16px; border-radius: 2px; margin-bottom: 8px; }
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.bar-row:last-child { margin-bottom: 0; }
.bar-label { font-size: 12px; color: #595959; flex: 0 0 160px; text-align: right; line-height: 16px; }
.bar-label.highlight { color: #ed1c24; font-weight: 700; }
.bar-track { flex: 1; background: #e5e7eb; height: 18px; border-radius: 1px; overflow: hidden; }
.bar-fill { height: 100%; background: #374151; border-radius: 1px;
            animation: barGrow 0.8s ease forwards;
            animation-delay: calc(var(--i, 0) * 0.12s);
            width: 0; }
.bar-fill.highlight { background: #ed1c24; }
.bar-value { font-size: 12px; font-weight: 700; color: #1a1a1a; flex: 0 0 48px; }
.chart-note { font-size: 12px; color: #595959; margin-top: 8px; font-style: italic; line-height: 18px; }

@keyframes barGrow { from { width: 0; } to { width: var(--w); } }
```

**Important:** Set `width: 0` on `.bar-fill` as the CSS default, and use `@keyframes barGrow` with CSS custom property `--w` as the target width. The animation runs on page load automatically — no JavaScript needed.

### Vertical bar chart (for time-series)

```html
<div class="vchart">
  <div class="vchart-col">
    <div class="vchart-bar-wrap">
      <div class="vchart-val">4.3</div>
      <div class="vchart-bar" data-h="26.5" style="background: #374151;"></div>
    </div>
    <div class="vchart-year">2019</div>
  </div>
  <!-- repeat for each year; highlight last/peak with background: #ed1c24 -->
</div>
```

```css
.vchart { display: flex; align-items: flex-end; gap: 6px; height: 160px; padding: 0 4px; }
.vchart-col { display: flex; flex-direction: column; align-items: center; flex: 1; height: 100%; }
.vchart-bar-wrap { display: flex; flex-direction: column; justify-content: flex-end; align-items: center;
                   flex: 1; width: 100%; }
.vchart-val { font-size: 10px; font-weight: 700; color: #1a1a1a; margin-bottom: 2px; }
.vchart-bar { width: 70%; border-radius: 1px 1px 0 0; height: 0; transition: height 0.6s ease; }
.vchart-year { font-size: 10px; color: #595959; margin-top: 4px; }
```

```js
// Animate vertical bars when scrolled into view
var vchart = document.getElementById('vchart');
new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.vchart-bar').forEach(function(bar) {
        bar.style.height = bar.dataset.h + '%';
      });
      this.unobserve(entry.target);
    }
  }.bind(this));
}, { threshold: 0.2 }).observe(vchart);
```

**Note on IntersectionObserver:** Use it only for animations that start at 0 (height: 0, width: 0). Do NOT use `opacity: 0` on section containers — elements that start invisible and are below the viewport may never become visible on non-interactive renders (screenshots, RSS readers, print).

### SVG line chart

```html
<svg class="line-chart" viewBox="0 0 600 200" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ed1c24" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ed1c24" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- Area fill -->
  <path class="area-path" d="M0,180 L100,120 L200,90 L300,60 L400,40 L500,20 L600,10 L600,200 L0,200 Z"
        fill="url(#area-grad)"/>
  <!-- Line -->
  <path class="line-path" d="M0,180 L100,120 L200,90 L300,60 L400,40 L500,20 L600,10"
        fill="none" stroke="#ed1c24" stroke-width="2"/>
  <!-- Axis labels -->
  <text x="0" y="198" class="axis-label">2019</text>
  <text x="600" y="198" class="axis-label" text-anchor="end">2025</text>
</svg>
```

```css
.line-chart { width: 100%; max-width: 600px; }
.axis-label { font-size: 10px; fill: #595959; font-family: 'Rethink Sans', sans-serif; }
.line-path { stroke-dasharray: 1000; stroke-dashoffset: 1000;
             animation: drawLine 1.5s ease forwards; }
@keyframes drawLine { to { stroke-dashoffset: 0; } }
```

Use the actual SVG `getTotalLength()` for accurate dasharray if the path is complex. For simple paths, 1000 is a safe over-estimate.

### Stacked horizontal bar

```html
<div class="stacked-bar">
  <div class="stacked-seg" style="flex: 61; background: #374151;"><span>Category A 61%</span></div>
  <div class="stacked-seg" style="flex: 36; background: #595959;"><span>Category B 36%</span></div>
  <div class="stacked-seg" style="flex: 3;  background: #9ca3af;"><span></span></div>
</div>
```

```css
.stacked-bar { display: flex; height: 32px; border-radius: 2px; overflow: hidden; }
.stacked-seg { display: flex; align-items: center; padding: 0 8px; overflow: hidden; }
.stacked-seg span { font-size: 11px; font-weight: 700; color: #ffffff; white-space: nowrap; overflow: hidden; }
```

### Data table

```html
<table class="data-table">
  <thead>
    <tr><th>State</th><th>2007</th><th>2023</th><th>Change</th></tr>
  </thead>
  <tbody>
    <tr><td>Maharashtra</td><td>45</td><td>38</td><td class="green">▼ 7</td></tr>
    <tr><td>Bihar</td><td>12</td><td>18</td><td class="red">▲ 6</td></tr>
  </tbody>
</table>
```

```css
.data-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.data-table th { background: #1a1a1a; color: #ffffff; font-weight: 700; padding: 8px 12px; text-align: left; font-size: 12px; }
.data-table td { padding: 8px 12px; border-bottom: 1px solid #e5e7eb; color: #1a1a1a; }
.data-table tr:last-child td { border-bottom: none; }
.data-table .red { color: #ed1c24; font-weight: 700; }
.data-table .green { color: #16a34a; font-weight: 700; }
```

### Bullet list

Use `position: relative` + `position: absolute` — NOT CSS Grid — to avoid the word-per-line bug.

```html
<ul class="news-list">
  <li><strong>Key point:</strong> explanation text that flows normally</li>
</ul>
```

```css
.news-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.news-list li {
  position: relative;
  padding: 10px 12px 10px 28px;
  background: #f6f6f6;
  font-size: 16px;
  line-height: 28px;
}
.news-list li::before {
  content: '●';
  position: absolute;
  left: 10px;
  top: 12px;
  color: #ed1c24;
  font-size: 8px;
}
```

**Never use `display: grid` on `<li>` elements with `::before` pseudo-elements** — the pseudo-element becomes a grid child, causing trailing text to wrap word-by-word.

---

## Responsive Design

```css
@media (max-width: 480px) {
  h1 { font-size: 24px; line-height: 30px; }
  .stat-strip { grid-template-columns: repeat(2, 1fr); }
  .bar-label { flex: 0 0 120px; }
  .two-col { grid-template-columns: 1fr; }
}
```

Test at 390×844 (iPhone 14 Pro) and 1280×900 (desktop). Ensure:
- Stat strips collapse from 3-col → 2-col at ≤480px
- Side-by-side panels stack to single column
- Bar label column shrinks from 160px → 120px
- H1 reduces from 28px → 24px

---

## Content Decisions

### What to include

- **All major data sections** from the flap — translate each chart 1:1
- **The headline** — rewrite for web if too print-specific ("bridged energy gap" → "how India closed its energy gap")
- **A one-sentence intro/subhead** — summarise the story angle
- **Source attribution** — small italic note below each chart
- **Byline** — "By [Author Name]"

### What to cut

- Print-specific captions that explain how to read the chart physically
- Page references, print edition notes
- Decorative illustrations (describe them in text if contextually important)
- Redundant headers that repeat the same point in multiple sections

### What to rewrite

- Section headings: make them narrative ("Wages Barely Moved") not categorical ("Wage Trends")
- Data callouts: frame as insight ("India's electrification pace was 3× faster than China's") not raw numbers alone

---

## Quality Checklist

Before finishing, verify each item:

**Design compliance**
- [ ] Font: `Rethink Sans` loaded via Google Fonts `<link>` (not `@import`)
- [ ] Background: `#ffffff` body, no dark backgrounds on main sections
- [ ] Body text: `16px / 28px` line-height
- [ ] H1: `28px / 36px / 700`
- [ ] H2: `20px / 28px / 700` with `border-bottom: 2px solid #1a1a1a`
- [ ] Red accent `#ed1c24` used only for badge, highlights, stat card tops
- [ ] Muted text: `#595959` (not `#666666`)
- [ ] Default bar color: `#374151` (not black, not `#333`)
- [ ] Chart backgrounds: `#f6f6f6`
- [ ] Content max-width: `680px`

**Chart quality**
- [ ] Every chart has a title (h3) and source note (`.chart-note`)
- [ ] Highest value or India row is highlighted in `#ed1c24`
- [ ] Bar animations run on load via `@keyframes barGrow` (no JS required for horizontal bars)
- [ ] Vertical bars animate via IntersectionObserver (height: 0 → target height)
- [ ] SVG line charts draw in via `stroke-dashoffset` animation
- [ ] No `opacity: 0` on section containers

**Responsiveness**
- [ ] Screenshot at 390×844 — no horizontal overflow, text readable
- [ ] Screenshot at 1280×900 — all content visible, proper centering

**CMS safety**
- [ ] No external scripts (only Google Fonts CDN)
- [ ] All JS is inline `<script>` at end of `<body>`
- [ ] File size < 50KB (typical range: 20–40KB)
- [ ] HTML validates (no unclosed tags, no duplicate IDs)

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| SVG text is character-by-character | Use `pdftotext -layout` on the PDF instead |
| `opacity: 0` on section containers | Remove — use it only on bar fills that animate width |
| CSS Grid `<li>` with `::before` bullet | Use `position: relative / absolute` instead |
| Wrong font (Playfair, Barlow, etc.) | Always use `Rethink Sans` |
| Dark themed background | TOI is white — use `#ffffff` |
| Body text at 14px or 15px | Must be `16px / 28px` |
| Muted text at `#666666` | Use `#595959` |
| Red accent overused | Only 3–4 uses per file: badge, chart highlight, stat card border-top |
| Bar color is `#1a1a1a` or black | Use `#374151` for non-highlighted bars |
| IntersectionObserver hides content | Never set `opacity: 0` in CSS; only in JS after observer registers |

---

## Example Conversion Workflow

```bash
# 1. Extract content
pdftotext -layout "originals/My Flap.pdf" > /tmp/flap-text.txt
cat /tmp/flap-text.txt

# 2. Get visual reference
pdftoppm -r 72 "originals/My Flap.pdf" /tmp/flap
magick /tmp/flap-1.ppm /tmp/flap.jpg
# View flap.jpg with Read tool

# 3. Write HTML (see patterns above)
# Save to output/my-flap.html

# 4. Screenshot and review
python3 -m http.server 8765 &
python3 - <<'EOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    for w, h, label in [(1280, 900, "desktop"), (390, 844, "mobile")]:
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto("http://localhost:8765/output/my-flap.html", wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"/tmp/my-flap-{label}.png", full_page=True)
        page.close()
    browser.close()
EOF
# View screenshots with Read tool; fix any issues
```

---

## Produced Examples

| File | Story | Key Charts |
|---|---|---|
| `output/green-power.html` | India's energy transition | Country comparison bars, SVG line chart (electrification), capacity stacked bar |
| `output/us-university-funding.html` | Trump cuts to US universities | Horizontal bars with staggered CSS animation |
| `output/iran-oil-travel.html` | Gulf war impact on India | Bullet list, passenger flow 2-col, oil import bars, SVG Nifty line |
| `output/nri-money.html` | NRI deposits rising | Vertical bar chart, stacked deposit bar, definition cards |
| `output/japan-growth.html` | Japan's economic stagnation | GDP comparison bars, wages/inflation/rates bars, ageing data, country table |
| `output/inactive-firms.html` | 383 inactive govt PSUs | Big % callout, state data table, ₹ stat card, ordered closure steps |
