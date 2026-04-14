# Prompts

## Hack of the day, feedback, 23 Mar 2026 (Github Copilot - gpt-5.4 medium)

Update hackoftheday/cards.json marking the following as rejected, with reason that they have been published earlier: 61, 57, 45, 36, 26, 17, 15, 12, 11, 7, 6, 5, 3, 2, 1.
Mark the rest as status: Accepted.
The review date for all changes is 10:13 pm SGT on 23 Mar 2026.

---

No no - only items that did NOT have a status should have been marked as accepted! Think about the best way to correct things (revert and redo? edit from here?) and make the change and verify.

<!-- copilot --resume=8f64fc0b-8e3b-462b-8bde-68805890fdfb -->

## MOSPI Statoistics, 13 Mar 2026 (GitHub Copilot - claude-sonnet-4.6 high)

Read data/mospi-plfs/README.md and the insights in data/mospi-plfs/v3/insights.md (and any related files).

Render them as consistent SVGs in the format described by statoistics-svg/statoistics-format.md.
Make sure the text, chart, etc. are easy to understand for a lay audience reading an Indian national newspaper.
Use the data and insights as the source of truth.
But use your judgement on content, style, design elements, annotations, etc. to make the story clearer and more compelling.

You will be saving them as 2026-03-13-mospi-plfs-v3/\*.svg (named descriptively, e.g. 01-marriage-labor-market-cliff.svg, etc.)

To start with, generate one SVG, view the output, fix any errors you find, and pause to check with me for feedback.

---

1. Headline is OK. Shorten and simplify the rest of the content
2. Slope-chart is clear enough
3. Cut the controlled-model callout - too complex & verbose
4. Use a print-friendly color palette

Update statoistics-svg/statoistics-format.md to incorporate the above feedback, as well as the following MANDATORY guidelines for print:

- Match the title bar font, colors, size, and other formatting exactly. This is a brand guideline. Especially the word "Statoistics"
- Use a white background, since this is for print. Ensure contrast is good against the background.
- Use larger fonts overall to ensure readability on print.

Regenerate the SVG, test it visually by converting it into an image and viewing it, and pause to check with me for feedback.

---

1. STATOISTICS" with dark "TOI" looks fine but "A slice of life in numbers" is a bit small. Check with the original.
2. Data colours are good
3. Headline and deck text are good

Update statoistics-svg/statoistics-format.md to incorporate the above correction (#1), as well as the following MANDATORY guidelines for print:

- Use the SAME font used in the statnostics/statoistics-svg/\*.svg images
- Use a slightly larger font for the subtitle and footnote. See statnostics/statoistics-svg/\*.svg images

Regenerate the SVG, test it visually by converting it into an image and viewing it, and pause to check with me for feedback.

---

OK, generate the rest. But generate them under statnostics/2026-03-13-mospi-plfs-v3/ -- including moving the current image under that directory.

---

<!-- 25 Mar 2026: Add citations -->

Add citations as corresponding .md files alongside the SVGs, and named the same as the basename of the SVG.
Each should contain enough detail for a journalist to EASILY verify the facts. Think about what HOW they would verify and what to check.
For example, providing text to search for (via copy-paste) is helpful. Citing actual numbers to verify against is helpful.
In fact, make this a comprehensive verification checklist & SOP.
Do this for all the SVGs.

---

Modify the SOP .md files to point to the original source for someone who does not have the data/ folder but will be able to verify it by downloading the source. Guide them on how to verify with respect to the original MOSPI PLFS v3 data.

---

Create an elegant gallery page statnostics/2026-03-13-mospi-plfs-v3/index.html that shows all the SVGs in cards.
Clicking on the image opens a popup with the full size SVG.
The card also has a "Verify" button that opens the corresponding SOP .md file in a new window popup (rendered as HTML) for easy verification.

--- <!-- 10 Apr 2026 -->

Now, there is a data/mospi-plfs/v4/insights.md. Go through it, find the insights that are interesting, and create SVGs for them as well, following the same format and style as the v3 SVGs. Save them under statnostics/2026-03-13-mospi-plfs-v4/. Create corresponding SOP .md files for each new SVG as well, and link them from the gallery page.

<!-- copilot --resume=5cf8e597-fd8c-4b14-ac5b-ff6139f507d4 -->

### UN Statoistics, 14 Apr 2026 (GitHub Copilot - claude-sonnet-4.6 high)

Read data/us/README.md and the insights in data/un/v3/insights.md (and any related files).
Go through it, find the insights that are interesting, and create SVGs for them as well, following the same format and style.
Save them under statnostics/2026-04-14-un-v3/.
Create corresponding SOP .md files for each new SVG as well.
Link them from the gallery page.
Move the gallery page from statnostics/2026-03-13-mospi-plfs-v3/index.html to statnostics/index.html and update links accordingly.
The UN v3 insights will form a new section at the top.

---

Generate SVGs and SOPs for the remaining data/un/v3/insights.md insights and link from the gallery.

Use slightly more innovative visualizations - but make sure they're especially appropriate, not just fancy. Think about best practices in data visualization and apply them.

---

Create a narrative data story explaining how these Statoistics were created - specifically how AI automates the process of creating these.

Generate this as statnostics/process.html and link it from the gallery.

Make sure that the first page or so gives them a quick summary of the process - and the clear takeaway that AI can automate analysis and insight generation and visualization against a format - to the point of being able to automate a newsroom function. Then continue with the rest of the story explaining the details of the process.

To understand the download process, read data/un/prompts.md and data/un/download_un_data.py.

To understand the analytics process, read data/un/prompts.md and any other files under data/un/ (and if you want more details on how Copilot created these, you can find the session logs for session 86e60a6e-6405-4374-9f95-94782e973b19 in ~/.copilot/ - if you really want to go deep.)

To understand the visualization process, the history of this conversation and related files that were generated will be helpful. So is ./prompts.md - especially the first 150 lines or so, which explain the Statoistics prompts (and if you want more details on how Copilot created these, you can find the session logs for session 5cf8e597-fd8c-4b14-ac5b-ff6139f507d4 in ~/.copilot/ - if you really want to go deep.)

Use the data-story skill. Use tooltips, popups, interactions, and animations as informative and engaging aids.

---

Use SVG images instead of PNG images. The PNGs will not be committed.

Add `.output-box-inner { white-space: pre-wrap; }` to the CSS.

Improve contrast: --crimson is too dark against the black background, so use something lighter.

Increase the default font size for better readability. Increase the `.section { max-width }` correspondingly. Update `.section.wide` width accordingly.

<!-- copilot --resume=5cf8e597-fd8c-4b14-ac5b-ff6139f507d4 -->

## Hack of the day, SVG alignment (Github Copilot - claude-sonnet-4.6 high)

Modify the hackoftheday/ HTML and SVG to use the Poytner Agate One font from assets/\*.otf. Use the bold condensed / condensed versions.

Modify the SVG rendering to native SVG elements: text and tspan (not foreignObject, div), rect, clipPath, defs > style, named fonts, styles scoped via CSS classes on SVG elements, static pre-positioned elements. No JavaScript, div, @import, QR code library, etc. Use robust libraries for conversion if required.

---

The SVGs have a number of issues.

- There's a line across the "NOTE" at the bottom that looks like a strikeout
  - For template=broadsheet, there's also a line through the title
- STEPS: is too small and too close to the "What to do" section
- The QR code is missing

There may be potentually other issues. Also, it doesn't quite look like the HTML.

Take screenshots of the SVG. Fix issues.
Compare with screenshots of the HTML. Align.

---

There are still a few issues with the SVG templates. For example:

- broadsheet: to the left of the QR code, it says "Times Internet, not "Scan for more hacks" above the QR code. Also the contrast against the background is not good - maybe a white background would help? Same for the original template. Maybe others?
- Shadows would help where we're using them in the HTML.

Similarly, think about other ways to align the SVG with the HTML. Where possible, standardize the code across templates.

### Improve SVG (Github Copilot - claude-sonnet-4.6 high)

Increase the font sizes of all text in the hackoftheday HTML and SVG by about 2 points (and make the headline larger as well, though that’s negotiable).

In the SVG:

- A blue band appears behind the headline. See temp/2026-03-13-hack-of-the-day-svg-output.png
- The 'Hack of the Day' formatting is lost, and the series number shows up
- The SVG also loses the shadow effect after each point.

Fix these and verify by converting the SVG to PNG and visually comparing it with temp/2026-03-13-hack-of-the-day-svg-output.png.

<!-- #TODO Resume and fix via copilot --resume=1365910e-bcba-4ea0-a132-b63e7c4399a6 -->

## Hack of the day, UI fixes, 12 Mar 2026 (Github Copilot - claude-sonnet-4.6 medium)

For the newly added cards in cards.json, set the created date to 12 Mar 2026 at 9:30 am SGT.

index.html should show the created date like "Thu, 12 Mar 2026" in each card. Change default sort order to descending order of index. Allow sorting by ascending / descending order of created, reviewed, or index. Make it easy to filter by status (accepted, rejected, pending). Ensure that sorting and filtering are bookmarkable via URL hash parameters.

---

The color contrast (blue on blue) makes a lot of content barely visible. Review the foreground-background color contrast across elements and ensure contrast while preserving aesthetics.

---

In index.html, when shrinking the cards at the end, make sure all cards have the same height.

---

"Rejected" and "Accepted" pills are too large. Just mark it with 🔴 or 🟢 or 🟡 (pending). Rename "Download" to "Save" in the buttons to save space. Move the sort and filters to the .page-header. The tooltip on "Rejected" is getting cropped by the card - make sure it doesn't.

---

Make the .page-header more compact - one line.

Make the app more responsive. On mobile, clicking on a card should expand it in a way that does not exceed the viewport width. The close button should still be visible on the screen. The sort and filter options should be easily accessible on mobile as well, but collapsed.

Think about any other responsive features that would be important and implement them. It should look good and work well on mobile, tablet, and desktop.

## Hack of the day, SVG fixes, 12 Mar 2026 (Github Copilot - claude-sonnet-4.6 high)

I could not load the generated SVGs on Gnome nor on VS Code's image viewer. But they render on Chrome. Get them to work on these as well. Keep in mind that they'll finally be opened by Adobe Illustrator and similar tools - so tool compatibility is important. Update SVG templates accordingly and test if you can.

## Hack of the day, feedback, 12 Mar 2026 (Github Copilot - claude-sonnet-4.6 high)

Update config.json with optional "status" and "reason" fields.

1. Hacks #4, 8, 10, 13, 14, 16, 18, 19, 20, 21, 22, 23, 24, 25, 38, 43, 44, 46, 47. Mark them as "Accepted"
2. Hacks #27, 28, 30, 31, 33 - iphone specific and 29, 34, 35,37, 39, 40, 41, 42, 48, 49 - Android specific. Mark them as "Rejected" with reason: "Hacks must be platform agnostic".
3. Hack #9: Mark as "Rejected". Reason: "Duplicate of similar one via Sanchar Sathi portal instead of CEIR"
4. Hack #32: Mark as "Rejected". Reason: "Not a tech hack"

Include an ISO "created" date for all existing hacks, setting it to 10 Mar 2026 at around 12 noon SGT.
Include an ISO "reviewed" date for all existing hacks, setting it to 11 Mar 2026 10:45 pm SGT.

Modify index.html to include the new created field and status field (if present). Hovering over the status should show the reviewed date and reason if present.

Sort the hacks (by default) by created date (latest first), then by index number (lowest first). Allow sorting by reviewed date as well as by index.

## Hack of the day, convert to SVG, 12 Mar 2026 (Github Copilot - claude-sonnet-4.6 high)

Create a template.svg that achieves the same outcome as the hack-of-the-day/template.html, but using SVG instead of HTML/CSS. The same JSON should be able to be used with both the HTML and SVG templates to produce the same visual output. (Handle text wrapping thoughtfully!)

Modify index.html to allow switching between the HTML and SVG templates for rendering the cards. The gallery should show the same thumbnails, but clicking on a card should open the popup with the version rendered using the currently selected template (HTML or SVG).

Later on, I will ask you to extend this to the other template-\* but for now, just get this far so I can test it.

IMPORTANT: Because Claude will almost certainly stall when generating large file at one shot, generate changes in chunks rather than creating single massive files.

---

When the format is SVG, the "Download" button should download the SVG.
Download All should include the SVG files.
Update the other templates similarly.
Commit (including prompts.md) which I'm modifying.

---

I've added new cards to cards.json. Now, add an "index" field to "cards.json" starting with "001", in order. Use this index in the filename when downloading, e.g. `hack-of-the-day-001.html` or `hack-of-the-day-001.svg`, as well as everywhere we are using the index. This will be a unique reference for the hacks. This will make it easier to keep track of the cards and ensure they are ordered correctly.

Commit all files (including prompts.md which I'm modifying) and push.

### New templates (Github Copilot - claude-sonnet-4.6 high)

Add 2 new HTML + SVG templates. This time, get more creative. Draw inspiration from similar properties other, innovative, publications have created (e.g. the New York Times' "The Daily" newsletter, or the "Wait But Why" blog). The templates should be visually distinct from each other and from the existing template. They should be designed to make the content more engaging and easier to consume, while still maintaining a consistent overall aesthetic for the Hack of the Day series.

## Hack of the day redesign, 10 Mar 2026 (Github Copilot - claude-sonnet-4.6 high)

Create a hackoftheday/redesign.md that suggest 10 different ways the SAME cards in hackof

## Hack of the day gallery, 10 Mar 2026 (GitHub Copilot - claude-sonnet-4.6 high)

<!-- cards.json created by https://chatgpt.com/c/69aef234-93f8-839b-932d-cb41c0ed8f2f -->

Create a beautiful hackoftheday/index.html gallery that loads hackoftheday/cards.json and renders a card for each entry by applying mustache templating to hackoftheday/template.html.

The home page should show a beautiful thumbnail gallery of all the cards, showing miniature versions of the cards in a grid. Clicking on a card should open the card in a popup with 800px width, showing the fully rendered card. The miniature version is exactly the same as the full version, just scaled down.

---

The hacks are typically taller. Increase the size of thCe cards so that the entire hack card is visible on the gallery.
On the popup, add arrow buttons to navigate to the previous and next cards without closing the popup. Allow left and right arrow keys to also navigate between cards when the popup is open.

---

Add an inline SVG favicon (check skills on how).
Ensure that .thumb-footer is always at the bottom - right now there's a bit of spacing even below .thumb-footer.

---

Modify so that clicking on the .thumb-footer does not open the popup. Add a tiny "Download" button that downloads the HTML as `hack-of-the-day-${number}.html` when clicked, e.g. `hack-of-the-day-001.html`.

---

Replace fonts with the closest Google Fonts.

---

Include a "Download All" button that downloads a ZIP of all the cards as individual HTML files named `hack-of-the-day-${number}.html`.

---

Vertically center the step elements.

---

Update README.md.

---

Briefly (in one line) document "Hack of the Day" in the root ./README.md and link to hackoftheday/README.md. It'll be deployed as a static page at https://sanand0.github.io/journalists/hackoftheday/. Give people a sense of what it is and how it was built.

## Hack of the day, 10 Mar 2026 (Claude Code - Sonnet 4.6) - Manually edited

Create a template.html that can be combined (e.g. via mustache) with a JSON that, when run, produces the EXACT visual output as the cards in \*.avif.

Inspect these cards. Create an appropriate JSON schema to capture these cards.

Then generate HTML (use SVG if required) to create a fluid layout that will render the same cards/folders as the .avif. Keep in mind that the images may look slightly different - but the template must render the same size, font, colors every time, and avoid overlapping or cut-off text. The template should be flexible enough to handle slightly different lengths of text and different numbers of points (e.g. 3-5) without breaking the layout.

Test even small details, e.g.

- The steps are supposed to look like folders, overlapping / stacked.
- The name in the email ID should be in bold, and the domain in regular font.
- The number in the steps must be larger, and in a different font - look carefully.
- The text in the steps must be close to the number - look carefully.

These are examples. Using this as a reference, carefully identify more such, test and fix them all.

Test by generating a few variations beyond the existing cards, e.g. with different text lengths and number of points, and ensure the layout still works.

DO NOT COMMIT.

---

Document this project in README.md.

## Hack of the day, 10 Mar 2026 (Codex - gpt-5.4 xhigh) - Dropped

Create a hack-of-the-day/template.html that can be combined (e.g. via mustache) with a JSON that, when run, produces the EXACT visual output as the cards in hack-of-the-day/\*.avif.

Inspect these cards. Create an appropriate JSON schema to capture these cards.

Then generate HTML (use SVG if required) to create a fluid layout that will render the same cards as the .avif. Keep in mind that the images may look slightly different - but the template must render the same size, font, colors every time, and avoid overlapping or cut-off text. The template should be flexible enough to handle slightly different lengths of text and different numbers of points (e.g. 3-5) without breaking the layout.

Test by generating a few variations beyond the existing cards, e.g. with different text lengths and number of points, and ensure the layout still works.

Commit as you go.

---

Not sure why some files vanished. It might be a conflict between sub-agents committing, so feel free to resolve it yourself.

But I took a quick look at the output, and it needs some work. For example:

- The fonts are much smaller
- The steps are supposed to look like folders, overlapping / stacked. Right now, they look like rounded cards with a gap between them.
- Hack of the day is not horizontally / vertically centered.
- The QR code formatting is off.
- The name in the email ID should be in bold, and the domain in regular font.
- The number in the steps must be larger, and in a different font - look carefully.
- The text in the steps must be closer to the number - look carefully.

These are examples. Using this as a reference, carefully identify more such issues, fix them all, and continue.

## Statnostics, 2 Mar 2026

### Find stories via ChatGPT

Used https://chatgpt.com/c/69a5244f-0a24-8398-a70e-dfa54ac68d69 to find a bunch of data stories copy-pasted into:

- [Crash severity paradox](2026-03-02-crash-severity-paradox/insight.md)
- [Anaemia outlier](2026-03-02-anaemia-outlier/insight.md)
- [Banking fraud whiplash](2026-03-02-banking-fraud-whiplash/insight.md)
- [Suicide geography](2026-03-02-suicide-geography/insight.md)
- [India's hidden gold superpower](2026-03-02-india-s-hidden-gold-superpower/insight.md)

### Find stories via Codex

````markdown
You are a research assistant finding publicly available data for Indian data journalism.

Extensively search the following authoritative sources and extract 5 SURPRISING comparative insights - e.g. an extreme outlier, an unexpected ranking, or a dramatic change over time - that has not yet been widely reported in the media. These insights should be of interest to a general audience and have the potential to be developed into a compelling data-driven story.

**Primary Indian sources to search:**

- NCRB (ncrb.gov.in) - crime, violations, accidents
- MOSPI / data.gov.in - economic, demographic indicators
- RBI (rbi.org.in) - financial, banking, reserves data
- EAC-PM reports - household surveys, consumption
- NFHS (rchiips.org) - health, nutrition, gender
- World Gold Council, IMF, World Bank - for India vs. world comparisons
- SEBI, NSE/BSE - financial markets
- MoRTH - road transport, vehicle ownership

**For each insight found, create a folder:**

Save the insight under `statnostics/${date:yyyy-mm-dd}-insight-slug/insight.json` e.g. `statnostics/2026-03-02-road-safety-paradox/insight.json` with:

```jsonc
{
  "headline": "...", // One-sentence insight
  "story": "...", // A few sentences explaining the insight in more detail
  "surprise": "...", // Why this is surprising or counter-intuitive
  "data": [
    // Top data points needed to visualize the insight
  ],
  "sources": [
    // Include citations links
  ],
}
```

**Filter criteria - only return data where:**

- There is a clear #1 that stands far above others (outlier story), OR
- There is a dramatic before/after change (transformation story), OR
- India's position vs. the world is unexpected (global comparison story)
````

This generated:

- [Crash severity paradox](2026-03-02-crash-severity-paradox/insight.json)
- [Rural consumption catchup](2026-03-02-rural-consumption-catchup/insight.json)
- [Rural durables overtake](2026-03-02-rural-durables-overtake/insight.json)
- [Cash rebound paradox](2026-03-02-cash-rebound-paradox/insight.json)
- [Remittance rank paradox](2026-03-02-remittance-rank-paradox/insight.json)

### Visualize using Gemini Pro

**Sketchnotes** worked well:

```markdown
Summarize this as a visually rich, intricately detailed, colorful, and funny, sketchnote.
Think about the most important points, structure it logically so that the sketchnote is easy to follow, then draw it.
```

- [Sketchnote - India's hidden gold superpower](https://gemini.google.com/u/2/app/c07bc6a82f6c6dcf) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/sketchnote.avif)
- [Sketchnote - Suicide geography](https://gemini.google.com/u/2/app/aaa45a7cb3608bc7) - [Image](statnostics/2026-03-02-suicide-geography/sketchnote.avif)
- [Sketchnote - Suicide geography 2](https://gemini.google.com/u/2/app/6425216f8a12fe2c) - [sketchnote2](statnostics/2026-03-02-suicide-geography/sketchnote2.avif)
- [Sketchnote - Anaemia outlier](https://gemini.google.com/u/2/app/55b1d04dd6a038ac) - [Image](statnostics/2026-03-02-anaemia-outlier/sketchnote.avif)
- [Sketchnote - Crash severity paradox](https://gemini.google.com/u/2/app/b1da3c954ea10e8e) - [Image](statnostics/2026-03-02-crash-severity-paradox/sketchnote.avif)
- [Sketchnote - Banking fraud whiplash](https://gemini.google.com/u/2/app/6c5ad23238ff2db2) - [Image](statnostics/2026-03-02-banking-fraud-whiplash/sketchnote.avif)

**Comics** did not, because Gemini couldn't always create a funny picture to go with the point. Gold worked well, the rest didn't.

```markdown
Draw this as a single-panel simple black and white line drawing comic strip with minimal shading, in RK Laxman's style, featuring the iconic "common man".
Think about the most important point, how best to convey it in the simplest, humorous yet impactful way in a single panel, then draw it.
```

**Funny Infographics** worked OK:

```markdown
Draw this as a visually rich, intricately detailed, colorful, and funny, infographic poster.
Think about the most important points, structure it logically so that the infographic is easy to understand, then draw it.
```

- [Funny Infographic - India's hidden gold superpower](https://gemini.google.com/u/2/app/8696754025e73a86) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/funny-infographic.avif)
- [Funny Infographic - Suicide geography](https://gemini.google.com/u/2/app/679d778c6214315d) - [Image](statnostics/2026-03-02-suicide-geography/funny-infographic.avif)
- [Funny Infographic - Anaemia outlier](https://gemini.google.com/u/2/app/f34906f0d24aaf39) - [Image](statnostics/2026-03-02-anaemia-outlier/funny-infographic.avif)
- [Funny Infographic - Crash severity paradox](https://gemini.google.com/u/2/app/a8997ac01fb80387) - [Image](statnostics/2026-03-02-crash-severity-paradox/funny-infographic.avif)
- [Funny Infographic - Banking fraud whiplash](https://gemini.google.com/u/2/app/88c097add1c70d40) - [Image](statnostics/2026-03-02-banking-fraud-whiplash/funny-infographic.avif)

**Infographics** worked OK:

```markdown
Draw this as a professional, visually appealing, informative, colorful, infographic poster.
Think about the most important points, structure it logically so that the infographic is easy to understand, then draw it.
```

- [Infographic - India's hidden gold superpower](https://gemini.google.com/u/2/app/5cd69b1b818fd6d0) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/infographic.avif)
- [Infographic - Suicide geography](https://gemini.google.com/u/2/app/bd84d0cdce0e0c42) - [Image](statnostics/2026-03-02-suicide-geography/infographic.avif)
- [Infographic - Anaemia outlier](https://gemini.google.com/u/2/app/27b7c25e30151293) - [Image](statnostics/2026-03-02-anaemia-outlier/infographic.avif)
- [Infographic - Crash severity paradox](https://gemini.google.com/u/2/app/6a5647fb472fd303) - [Image](statnostics/2026-03-02-crash-severity-paradox/infographic.avif)
- [Infographic - Banking fraud whiplash](https://gemini.google.com/u/2/app/aded2d46c6776b99) - [Image](statnostics/2026-03-02-banking-fraud-whiplash/infographic.avif)

**Feedback**

> These are nice in their own way but won’t work for us. A, ours have a square aspect ratio. B, the new ones have too much info packed into it. It needs to be sparse, with a sharp takeaway and maybe a smaller secondary message. These ones are too elaborate — if you see what I mean. Basically, from the data, one will need to distill the most important point and play that up. Something short and sharp.

**Revisions**: [Chat](https://gemini.google.com/u/2/app/b1da3c954ea10e8e)

- [Version 2a](https://gemini.google.com/u/2/app/968651555b6976a4) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/v2a.avif): Create a square (1:1), minimalist visual summary. Ruthlessly distill the data into ONE main headline insight (the 'Paradox') and one smaller secondary footnote. Keep the design sparse and uncluttered: use bold typography, simple iconography, and ample negative space. Aim for a 'poster-style' look that is instantly readable rather than a detailed infographic.
  - **Feedback**: This works well.
- [Version 2b](https://gemini.google.com/u/2/app/33670759b2be4535) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/v2b.avif): Create a square (1:1), high-impact minimalist graphic in the style of Swiss international design or a vintage propaganda poster. The composition must have extreme negative space and a rigid grid layout. The primary goal is a single, clear, and 'funny' visual comparison between the 'top crash state' and the 'top fatality state,' which are the only key data points. Use bold, sans-serif typography, large simple geometric icons, and a limited, high-contrast color palette to deliver the one main takeaway instantly. Include only one small, distinct secondary message.
- [Version 2c](https://gemini.google.com/u/2/app/6ffedf993807bbd9) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/v2c.avif): Generate a square (1:1) minimalist poster in a clean, Neo-Vector style, similar to a modern mobile app's start screen or a tech blog header. Focus the entire image on a single, creative, and slightly humorous metaphor that illustrates the 'Paradox,' making the high-fatality point the massive focal point. Keep all lines crisp and the flat colors bright but muted. Use substantial white space around a central illustrative element. Avoid complex charts; use clear scale and position to show the hierarchy of the two core numbers. The design must feature a clear main headline and one subtle, smaller footnote.
  - **Feedback**: This could work, too, but with a headline.
- [Version 2d](https://gemini.google.com/u/2/app/666f195803867b9c) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/v2d.avif): Create a square (1:1), tactile typographic poster in a distressed letterpress or screen-print style, using simple, bold, and slightly playful fonts. The image's dominant feature must be the main paradox headline, with a creative typographic 'clash' and 'skull' icon incorporated into the main title. The primary two pieces of data should be huge, and the secondary message is small. Emphasize a textured paper background and a single accent color for emphasis. This is not an infographic; it is a conceptual graphic where typography and negative space are the primary tools to convey the sharp, simple message.
  - **Feedback**: Too radical.

**Version 2a iterations**

- [Statnostics V2a - India's hidden gold superpower](https://gemini.google.com/u/2/app/968651555b6976a4) - [Image](statnostics/2026-03-02-india-s-hidden-gold-superpower/v2a.avif)
- [Statnostics V2a - Suicide geography](https://gemini.google.com/u/2/app/e7d9d0ba96ce4fa9) - [Image](statnostics/2026-03-02-suicide-geography/v2a.avif)
- [Statnostics V2a - Anaemia outlier](https://gemini.google.com/u/2/app/0b2c30b826552837) - [Image](statnostics/2026-03-02-anaemia-outlier/v2a.avif)
- [Statnostics V2a - Crash severity paradox](https://gemini.google.com/u/2/app/bbdd93d7b71beaa7) - [Image](statnostics/2026-03-02-crash-severity-paradox/v2a.avif)
- [Statnostics V2a - Banking fraud whiplash](https://gemini.google.com/u/2/app/0d2d4740f71d82ab) - [Image](statnostics/2026-03-02-banking-fraud-whiplash/v2a.avif)

## West Bengal's Voter Roll Revision, 1 Mar 2026

posts/2026-03-02-west-bengal-s-voter-roll-revision.md

### Research

```markdown
Here is the "Times News Network Newslist" - which are sent to journalists to write stories on - as of 27 Feb 2026.

If we wanted to write analytical pieces, i.e. that would be of interest even a week or two later rather than just as breaking news, what stories would you pick and why?

Think like an expert editor of the Times of India. In this context:

- What patterns would an expert in this field check / recognize that beginners would miss?
- What questions would an expert ask that a beginner would not know to?
- What problems / failures would an expert anticipate that beginners may not be aware of?

Based on this, identify criteria to select news articles, select the top 10 that meet these criteria, rank order them, and explain why you chose these stories and how they would be of interest to readers even a week or two later. Also, suggest potential angles for analysis for each story.

<NEWS>...</NEWS>
```

- [GPT 5.2 Extended Thinking](https://chatgpt.com/c/69a3d872-da74-839a-aa82-49fa7436a9fa)
- [Sonnet 4.5 Extended Thinking](https://claude.ai/chat/6a18438f-4926-4323-8b1d-55b3aaaeccac)
- [Gemini 3.1 Pro](https://gemini.google.com/app/3b5ac48dc592bdaf)

### Cross-reference research

```markdown
Here are opinions by Gemini and ChatGPT. Factor in what's better in their analysis, drop what's less good, and rewrite your version. Also share whose opinion (yours, Gemini's, or ChatGPT's) was the best and why - rank-ordered.
```

### Suggest prompts

```markdown
For the top 5 stories, suggest prompts I could use to run on AI deep research agents to get deeper insights and analysis on the story.

My aim is to, as a journalist, submit a story that is not just a rehash of the news, but has deeper insights and analysis that would be of interest to readers even a week or two later, and uncovers insights that are not yet publicly known or widely discussed.

Ways an AI agent can achieve this include data analysis from primary data sources, niche websites (non-media / mainstream) / social media, etc. Factor these into the prompt.
```

### Research West Bengal SIR

```markdown
You are a research analyst supporting an investigative journalist at the Times of India. Your task is to map the legal and administrative precedent for West Bengal's 2025-26 Special Intensive Revision (SIR) exercise and its outcomes.

Research the following specific questions:

1. Has any Indian state previously conducted a voter roll revision that resulted in: (a) out-of-state judges being requisitioned to adjudicate disputes, (b) state cabinet compensating deaths linked to the process, or (c) a category of voters marked "under adjudication" on a published electoral roll? Search Election Commission of India orders, Supreme Court filings, and academic work on Indian electoral administration (search SSRN, EPW archives, and Lok Dhaba datasets).

2. What is the legal status of a voter whose name is "under adjudication" on polling day? Search for Election Commission of India guidelines, Representation of the People Act provisions, and any HC or SC orders specifically addressing this category. If no precedent exists, document that gap explicitly.

3. Find and analyse the geographic distribution of the 60+ lakh "under adjudication" names — are they disproportionately concentrated in specific districts or assembly constituencies? Cross-reference with 2021 Census demographic data and 2021 West Bengal election results to identify whether the burden falls unevenly on specific communities or opposition strongholds.

4. Search social media (X/Twitter, Facebook public groups, Bengali-language platforms) for testimonials from BLOs (Booth Level Officers) or ground-level workers describing the verification process — specifically any accounts of threats, coercion, or impossible documentation demands placed on voters.

Primary sources to prioritise: Election Commission of India press releases and order archives, Supreme Court cause list and filings (search for SIR-related petitions), West Bengal government gazette notifications, and Lok Dhaba (Trivedi Centre) electoral data.

Output a structured memo with: key findings, gaps in publicly available data, and 3 questions that still require on-ground reporting to answer.
```

### Compare outputs

- 🟢 Sonnet 4.6 Research: Strong analytical rigor, deep constitutional analysis, nuanced data, actionable. https://claude.ai/chat/4fa8b807-3c1a-467d-888a-4b49851f256d
- 🟢 GPT 5.2: Strong sources, well structured, good legal analysis, intellectually honest, less granular on district data. https://chatgpt.com/g/g-p-69a3db6550888191b431eb352f946803-journalists/c/69a3dbca-b1c0-8399-91e2-63d4fce8f35c
- 🟡 ChatGPT Deep Research: Weak district analysis. https://chatgpt.com/g/g-p-69a3db6550888191b431eb352f946803-journalists/c/69a3dbc0-33e4-83a0-bebe-676f3b5b6e77
- 🔴 Gemini Deep Research: Poor logic, overconfident. https://gemini.google.com/app/3c5398043e4b4a29

Ranking by Claude Opus 4.6 Extended - Incognito:

```markdown
Here are responses from four agents to the same question below. Rank order the responses by quality, with reason.
<QUESTION>...</QUESTION>
<CHATGPT>...</CHATGPT>
<CHATGPT-DEEP-RESEARCH>...</CHATGPT-DEEP-RESEARCH>
<CLAUDE-RESEARCH>...</CLAUDE-RESEARCH>
<GEMINI-DEEP-RESEARCH>...</GEMINI-DEEP-RESEARCH>
```

**1. Claude Research**

This is the strongest response across nearly every dimension that matters for an investigative journalist.

**Analytical rigor.** It's the only response that includes a formal, tiered source-quality assessment (Tier 1–4), which is exactly what a journalist needs to know which claims can go in print and which need further verification. It flags the Hamimul Islam case — a BLO death TMC attributed to SIR stress but police later linked to a personal loan dispute — which is a genuine investigative insight none of the others catch. It also notes TMC's escalating death toll claims (39→120) as unverified at the higher figure, showing appropriate skepticism toward all sides.

**Legal depth.** The constitutional analysis is the most thorough. It walks through Sections 22, 23, 24 of RPA 1950, the Registration of Electors Rules 1960, and the Electoral Roll Management Rules 2003, documenting not just that "under adjudication" has no statutory basis, but listing exactly which provisions were searched and found lacking. It traces the evolving Supreme Court jurisprudence on the right to vote from _Jyoti Basu_ (1982) through _PUCL_ (2003) to _Anoop Baranwal_ (2023), giving the legal story a doctrinal arc.

**Data and nuance.** The district-level table is the most analytically useful of any response, combining under-adjudication figures, Muslim population percentages, 2021 political control, and border status in one place. Crucially, it identifies the Matua (Hindu refugee) community's burden and the Sabrang India finding that initial deletion rates were actually _lower_ in Muslim-majority areas — a counterpoint that prevents simplistic communal framing and shows genuine analytical honesty. The Purba Bardhaman anomaly (high under-adjudication numbers despite moderate Muslim population and no border) is identified as a puzzle requiring on-ground investigation — the kind of question that makes a reporter's next trip productive.

**Actionability.** The recommended next steps — specific RTI requests, interview targets (Odisha/Jharkhand judicial officers as neutral witnesses), data journalism cross-references (literacy, poverty, urbanization, not just religion), and a legal angle (whether Article 142 can create voter categories Parliament hasn't legislated) — go beyond the brief and are immediately usable.

**Weakness:** Occasionally verges on advocacy framing, and some district figures are hedged with tildes (~), reflecting wire-report sourcing rather than official data.

---

**2. ChatGPT (Regular)**

A very strong second that in some ways is more polished as a deliverable than Claude's response.

**Sourcing.** The inline hyperlinked citations (Indian Kanoon, CaseMine, TOI, Reuters, SSRN, EPW) are the most verifiable of any response. A journalist can click through and confirm claims immediately, which is operationally valuable.

**Structure.** Clean, well-organized, and appropriately scoped. It doesn't try to do more than the brief asks, and it handles each sub-question with the right level of depth.

**Legal analysis.** The framing of "under adjudication" as a "court-enabled interim label" managed through the Article 142 deeming fiction is precise and well-articulated. The practical question — "what does the presiding officer do on polling day?" — is the right one for a newsroom.

**Intellectual honesty.** Clearly flags the 2021 Census gap (noting India's census won't conclude until ~2027 per Reuters), distinguishes between what was and wasn't found, and avoids overclaiming. The "Why this matters beyond WB" closing paragraph — that administrative deadlines can now trump adjudication completion, with courts "patching legitimacy after the fact" — is analytically sharp and gives the journalist a framing for the national significance.

**Weakness:** Less granular than Claude on district-level data (doesn't construct a comparative table), thinner on BLO testimonials and ground-level accounts, and the social media section acknowledges its limitations without compensating with alternative sourcing. Doesn't flag the Hamimul Islam police-investigation contradiction, which matters for editorial credibility.

---

**3. ChatGPT Deep Research**

Thorough and competent but more diffuse than the top two.

**Strengths.** The comparative precedent analysis is well-structured, and the Assam D-voter parallel is developed more fully here than in any other response. The identification of Bihar as the earlier SIR escalation point — and the documentation-controversy timeline (Aadhaar added September 2025 after SC intervention) — provides useful chronological context. The distinction between enumeration-phase and hearing-phase documentation requirements is correctly identified.

**Weaknesses.** The district-level analysis is the thinnest of the four — it mentions the TOI report citing 40% concentration in three districts but doesn't construct a data table or test the pattern further. The social media section is essentially an admission that nothing attributable was found, without the compensating ground-level detail that Claude and Gemini provide. The three on-ground questions are reasonable but more generic ("what is the actual decision logic," "how are judicial officers conducting adjudication") than Claude's specifically targeted questions (the Purba Bardhaman anomaly, the clearance-rate arithmetic). It doesn't include a source-quality assessment, which means the journalist has to do their own triage. Overall, it reads as a careful literature review rather than an investigative research brief.

---

**4. Gemini Deep Research**

The most ambitious in scope and the weakest in reliability.

**Strengths.** The two data tables (district impact table and Kolkata constituency table with specific draft-roll and deletion figures for Kolkata Port, Bhowanipore, Maniktala, Entally) are genuinely useful additions that no other response provides at that level of specificity. The BLO testimonial section includes named cases (Shantimoni Ekka, Rinku Tarafdar, Sanjay Garai's attack in Salanpur) and the NHRC complaint, giving the journalist concrete leads. The identification of the 4.98 lakh "no-shows" as an unresolved data gap is a good catch.

**Critical weaknesses.** First, the editorial register is wrong for a research memo supporting an investigative journalist. Phrases like "catastrophic breakdown," "weaponized the livelihoods of state employees," "lethal physiological costs," and "extract rigid statistical purity" are advocacy language that would undermine credibility if carried into reporting. A research analyst's job is to present findings neutrally so the journalist can make editorial choices.

Second, there's an analytical confusion around "opposition strongholds." TMC is the ruling party in West Bengal. When the data shows TMC constituencies bearing the heaviest burden, that's the _ruling party's_ base being affected — which complicates rather than supports the "targeting opposition" frame. Gemini doesn't clearly navigate this ambiguity.

Third, the source list includes clearly tangential references (a US Congressional hearing on judicial appointments, US State Department country reports, an ETH Zurich research paper) that pad the bibliography without supporting the specific claims. This raises questions about source-verification discipline.

Fourth, it's the least honest about uncertainty. Claims are presented with high confidence where others appropriately hedge. The CEO's alleged quote that this is "the first time any final electoral roll will be having an adjudication-marked list" is attributed without the same verification caveats other responses apply. The response doesn't flag the Hamimul Islam police-investigation contradiction or the TMC death-toll escalation issue.

Finally, it's significantly longer than the others without proportionally more insight, which is itself a problem for a working journalist on deadline.

### Meta-prompt

I asked Claude Opus 4.6 Extended (incognito):

```markdown
Improve this prompt. How would an expert editor brief their investigative journalist?

<PROMPT>
You are a journalist at the Times of India. Your analysts have researched the legal and administrative precedent for West Bengal's 2025-26 Special Intensive Revision (SIR) exercise and its outcomes below.
Write a story for review by the editor for publication in the Times of India. Ensure that the story is written in the style of a Times of India piece suitable for this story.
Add a note to the editor mentioning what you're confident about, what's still uncertain, and what data / reporting gaps remain, and what further reporting could clarify the story.
</PROMPT>
```

... which led to:

```markdown
**ROLE:** You are a senior investigative journalist on the politics & governance beat at the Times of India.

**ASSIGNMENT:** Your editor has handed you analysts' research (provided below) on the legal and administrative precedent for West Bengal's 2025-26 Special Intensive Revision (SIR) exercise and its outcomes. Write the story for editorial review.

**STORY REQUIREMENTS:**

1. **Lead with the news.** Open with the single most consequential finding — what happened, who is affected, and why it matters now. No throat-clearing.

2. **Structure:** Follow TOI's standard investigative format: hard news lede → context and stakes → evidence and precedent → official/expert response → implications. Use short paragraphs and subheadings where they aid scanning.

3. **Tone & register:** Authoritative but accessible. Write for a politically literate general reader, not a legal specialist. Define jargon on first use. Avoid editorialising — let the facts carry the weight.

4. **Source discipline:** Attribute every factual claim. Distinguish clearly between confirmed facts, official statements, analyst inferences, and unverified allegations. Flag any single-source claims explicitly.

5. **Contextualise the precedent.** Show how prior SIR exercises (or comparable revision drives in other states) played out — what worked, what was challenged in court, and what the outcomes were. Draw the comparison explicitly so the reader understands what's new here.

6. **Quantify wherever possible.** Voter numbers, demographic breakdowns, timelines, court case citations — concrete data over vague characterisations.

**EDITORIAL NOTE (append after the story):**

Separately, write a candid note to the editor covering:

- **High-confidence claims:** What in this story is well-sourced and publication-ready?
- **Uncertain or thinly sourced elements:** Where are you relying on a single source, inference, or incomplete data?
- **Known gaps:** What questions does the available research _not_ answer?
- **Recommended next steps:** What specific reporting (RTI requests, interviews, court filings, field verification) would strengthen or reshape the story before publication?
- **Legal/sensitivity flags:** Anything that should go past the legal desk before print.

<CHATGPT>...</CHATGPT>
<CLAUDE-RESEARCH>...</CLAUDE-RESEARCH>
```

Claude Opus 4.6 Extended: https://claude.ai/chat/e81ad777-6227-402e-90a1-383a94b3df58
