# Hack of the Day

A Mustache-based card system for the "Hack of the Day" series — practical tips for everyday digital life.

## Files

```
index.html             Gallery page — browse, preview, and download all cards
template.html          Mustache template for rendering a single card
cards.json             All card data
```

## Gallery (`index.html`)

Open `index.html` in a browser (via a local server — required for `fetch`).

```bash
npx serve .
# or
python3 -m http.server
```

The gallery:
- Renders every card in `cards.json` as a scaled-down thumbnail using Mustache + `<iframe srcdoc>`
- Each thumbnail auto-sizes to the card's actual rendered height
- **Click a thumbnail** to open the full 800 px card in a popup
- **← / → arrow keys** (or on-screen buttons) navigate between cards in the popup
- **Download** button on each thumbnail saves that card as `hack-of-the-day-001.html`
- **Download All** button in the header saves all cards as `hack-of-the-day.zip`

## JSON schema

```jsonc
{
  "title": "CARD TITLE IN UPPERCASE",       // shown in header
  "what_it_solves": "One-sentence description",
  "what_to_do": "Intro sentence or null",   // null → "WHAT TO DO (QUICK STEPS):"
                                            // non-null → "WHAT TO DO: …" + red "STEPS:"
  "steps": [
    {
      "bold_title": "Optional bold prefix", // null to omit
      "text": "Step body (HTML allowed)"
    }
  ],
  "note_label": "NOTE",   // use "NOTE", "CAREFUL", or null to hide the section
  "note": "Note text",    // null hides the note section entirely
  "tip_name": "firstname.lastname",
  "tip_domain": "@domain.com",
  "qr_url": "https://…"  // URL encoded in the QR code
}
```

Supports 3–5 steps without layout issues.

## Design details

| Element            | Value                                                                  |
| ------------------ | ---------------------------------------------------------------------- |
| Card width         | 800 px                                                                 |
| Card background    | `#d2ddf2`                                                              |
| Badge / accent red | `#ec1b22`                                                              |
| Dark text          | `#0e1628`                                                              |
| Badge shape        | Pentagon arrow-right via `clip-path`                                   |
| Title font         | [Barlow Condensed](https://fonts.google.com/specimen/Barlow+Condensed) |
| Body font          | [Archivo Narrow](https://fonts.google.com/specimen/Archivo+Narrow)     |
| Step numbering     | CSS `counter-reset` / `::before` — no JS needed                        |
| Step stacking      | `margin-top: -10px` + decreasing `z-index` + `box-shadow`             |
| QR code            | [qrcodejs](https://github.com/davidshimjs/qrcodejs) (CDN, 80 × 80 px) |
