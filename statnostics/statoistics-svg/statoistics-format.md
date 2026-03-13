# Statoistics SVG Format

This note is based on the current set of five SVGs:

- `Statoistics-American firms.svg`: line chart
- `Statoistics_Crude oil.svg`: ranked horizontal bars
- `Statoistics-gold production.svg`: annotated trend line plus illustration
- `Statoistics-pothole accidents.svg`: photo-led ranking graphic
- `Statoistics_Teaching_Staff.svg`: diagram / treemap-style explainer

## What these files are

Each piece is a square social card built around one memorable statistical takeaway. The structure is consistent:

- a thin branded masthead at the top
- a strong 1-2 line headline
- a short deck explaining the stat
- one main chart / diagram / photo-led graphic
- a tiny source line at the bottom
- an optional note when a definition needs explaining

The tone is editorial, compact, and high-contrast rather than presentation-like.

## Layout conventions

- Use a square artboard. The current files are roughly `227 x 227` user units, with one slightly wider variant, but the exact number is less important than the `1:1` format.
- Reserve a shallow top strip for branding. In the current files it is a full-width red bar, about the top 5-7% of the canvas.
- Put the headline in the upper third, usually centered and split over 2 lines.
- Place the deck directly below the headline in 2-5 short lines.
- Let the main visual occupy the middle and lower two-thirds.
- Keep the source on the bottom edge, usually right-aligned or centered. Keep it small but still editable and readable.

## Background and print requirements

These cards are produced for **print** (newspaper / magazine). This has hard consequences:

- Use a **white background** (`#ffffff`). Never use dark backgrounds.
- All text, lines, and chart marks must have strong contrast against white. Avoid pastels or light greys for data marks.
- Use a **print-friendly colour palette**: deep, saturated hues that hold up on newsprint. Good choices: dark crimson `#c1121f`, dark navy `#1d3461`, dark teal `#1a5e6e`, dark amber `#92400e`. Avoid neon, bright cyan, or pastel variants.
- Use **larger fonts** than feel necessary on screen. In a 480 × 480 canvas: minimum body text 11 px, deck 13–15 px, headline 24–30 px.
- Keep data line weights 2.5–4 px so marks survive print reproduction.

## Visual language

- All cards use a **white base** with one strong accent palette chosen for the story.
- Accent colours should be dark and saturated (crimson, navy, teal, amber). Avoid light or neon colours.
- Labels are usually direct, inside or beside the marks, instead of relying on separate legends.
- Numbers are prominent and often paired closely with category labels.
- The graphic can be pure chart, chart plus illustration, or chart plus photo cutout, as long as there is one clear focal idea.

## Masthead brand specification (MANDATORY)

The masthead must be reproduced exactly on every card. Deviating from these rules breaks the brand.

### Title bar
- Full-width red rectangle, colour `#ed1c24`, height = ~6% of canvas (≈29 px in a 480 px canvas).
- Thin dark border (`#231f20`, 0.8 px in a 480 px canvas) runs around all four edges of the full card.

### "Statoistics" wordmark
The wordmark is the string **STATOISTICS** split into three colour groups rendered as a single continuous text element using `<tspan>`:

| Letters | Colour     | Notes                          |
|---------|------------|--------------------------------|
| `STA`   | `#ffffff`  | White, bold condensed          |
| `TOI`   | `#231f20`  | Dark/black, bold condensed     |
| `STICS` | `#ffffff`  | White, bold condensed          |

- Font: `PoynterAgateOne-BoldCondensed, 'Poynter Agate One'` (fallback: `'Arial Narrow', Arial, sans-serif`)
- Font size in a 480 px canvas: **19 px**, font-weight bold
- Positioned at x ≈ 6 px, y ≈ 21 px (≈72% down the 29 px bar)
- Apply `transform="scale(1 1.11)"` to vertically stretch the text slightly, as in the reference files

### Tagline
- Text: **"A slice of life in numbers"**
- Colour: `#ffffff` (white)
- Font: `PoynterAgateOne-Condensed, 'Poynter Agate One'` — the **Condensed** (not Bold) variant — fallback: `'Arial Narrow', Arial, sans-serif`
- Font size: 7.2 px in the reference 226.77 px canvas → **≈ 15 px in a 480 px canvas**
- Positioned immediately to the right of the wordmark, baseline y ≈ 22 px
- Estimated x start: ≈ 128 px in a 480 px canvas (adjust so it does not crowd the wordmark)

### Content guidelines for simplicity
- Headline: maximum 2 lines, short and direct. Strip sub-clauses and qualifications.
- Deck: maximum 2 short lines. One is better. Cut anything that can be inferred from the chart.
- Do not include callout boxes or verbose controlled-model annotations inside the chart area. If a methodological note is needed, put it in the note line at the bottom in small type.

## Typography

The house font stack — use these **exact** font names first so InDesign / Illustrator picks them up when the fonts are installed. Fallbacks are for browser / screen preview only.

| Role                      | Exact font name(s)                                          | Fallback                              | Size (480 px canvas) |
|---------------------------|-------------------------------------------------------------|---------------------------------------|----------------------|
| Headline                  | `PoynterOSDisplay-Bold, 'Poynter OS Display'`               | `Georgia, 'Times New Roman', serif`   | 28–30 px             |
| Wordmark STA / STICS      | `PoynterAgateOne-BoldCondensed, 'Poynter Agate One'`        | `'Arial Narrow', Arial, sans-serif`   | 19 px                |
| Wordmark TOI (dark)       | same as above                                               | same                                  | 19 px                |
| Tagline in masthead       | `PoynterAgateOne-Condensed, 'Poynter Agate One'`            | `'Arial Narrow', Arial, sans-serif`   | **15 px**            |
| Deck / chart labels       | `PoynterAgateOne-Condensed, 'Poynter Agate One'`            | `'Arial Narrow', Arial, sans-serif`   | 14–15 px             |
| Numeric callouts (values) | `GriffithGothic-Bold, 'Griffith Gothic'`                    | `'Arial Narrow', Arial, sans-serif`   | 22–28 px             |
| Note / footnote           | `PoynterAgateOne-Condensed, 'Poynter Agate One'`            | `'Arial Narrow', Arial, sans-serif`   | **10–11 px**         |
| Source line               | `PoynterAgateOne-Condensed, 'Poynter Agate One'`            | `'Arial Narrow', Arial, sans-serif`   | **10 px**            |

**Reference scale:** the originals use a 226.77 × 226.77 canvas. To find correct sizes for a 480 px canvas, multiply by **2.117** (= 480 ÷ 226.77).

- Tagline: 7.2 px × 2.117 = **15 px**
- Source: 4.5 px × 2.117 = **9.5 → round to 10 px**
- Deck: 7.2 px × 2.117 = **15 px**
- Headline: 16.2 px × 2.117 = 34 px — use 28–30 px in practice so long lines don't overflow

Preserve the hierarchy: headline large, deck mid-size, note and source small but readable.


## Content patterns that fit the style

- A single surprising comparison, ranking, rise/fall, or disproportion.
- One main chart type, not a dashboard.
- Short contextual copy that sharpens the takeaway instead of retelling the whole article.
- Source-first credibility: always include a source, and add a note if a term or category needs clarification.

## What can vary

These cards do not need to share one rigid template. It is fine to vary:

- chart type
- accent palette
- use of illustration or photography
- exact composition of the lower half
- whether the main visual is chart-first or illustration-first

What should stay stable is the editorial hierarchy, density, and branded top bar.

## Recommended SVG authoring format

Keep the output simple enough to open cleanly in Illustrator, InDesign, and similar tools:

- use plain SVG with a `viewBox`
- keep text live as `<text>` wherever practical
- organize top-level groups semantically, for example:
  - `masthead`
  - `headline`
  - `deck`
  - `graphic`
  - `labels`
  - `footer`
- use meaningful class names such as `.masthead`, `.headline`, `.deck`, `.value`, `.source` instead of anonymous export classes like `.cls-17`
- prefer simple `rect`, `line`, `polyline`, and `path` shapes for charts
- use clip paths, masks, and blend modes only when they are actually needed
- keep the palette small and intentional for each card

## Simplifications worth making

The current SVGs are editable, but their exports are more complex than necessary. Future files can be cleaner by:

- reducing auto-generated classes and repeated transforms
- avoiding excessive clip paths and masks
- using vector-first graphics unless a photo or raster object genuinely helps the story
- embedding raster images only when portability matters; otherwise keep the working file easier to manage
- preserving editability instead of outlining all text too early

Do not copy the current export clutter literally. Recreate the visual hierarchy and mood, not the accidental complexity of the existing files.
