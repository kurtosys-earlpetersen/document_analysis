# InDesign Style Guide — Allianz Income and Growth Factsheet

Companion reference for `allianz_factsheet_indesign.xmp`. This document defines every Paragraph Style, Character Style, Table Style, colour swatch, and template setup needed in InDesign so the XML import auto-maps correctly.

---

## 1. Document Setup

| Property | Value |
|----------|-------|
| Page size | US Letter (8.5 × 11 in / 215.9 × 279.4 mm) |
| Pages | 6 |
| Columns | Single column (use anchored frames for multi-col layouts) |
| Margins | Top: 0.5 in, Bottom: 0.55 in, Inside/Outside: 0.6 in |
| Bleed | 0.125 in (for header band on page 1) |
| Primary font | Inter (install from Google Fonts) |
| Fallback font | Helvetica Neue / Arial |
| Baseline grid | 12pt, starting at 0.5 in from top |

---

## 2. Colour Swatches

Create these as named swatches (CMYK values given for print; hex for reference):

| Swatch Name | Hex | CMYK (approx.) | Usage |
|-------------|-----|-----------------|-------|
| Navy 900 | `#071935` | C:95 M:75 Y:35 K:55 | Headings, header band, primary text |
| Navy 700 | `#0E305E` | C:90 M:65 Y:20 K:30 | Header gradient end |
| Blue 600 | `#0342E4` | C:85 M:70 Y:0 K:0 | Accent, links, positive callout border |
| Blue 100 | `#E8EEFB` | C:8 M:5 Y:0 K:0 | Callout blue background |
| Blue 50 | `#F0F4FD` | C:4 M:2 Y:0 K:0 | Investor profile background |
| Slate 600 | `#3A4051` | C:55 M:45 Y:30 K:55 | Body text |
| Slate 400 | `#6B7280` | C:40 M:30 Y:20 K:30 | Captions, labels, footers |
| Gray 200 | `#E5E7EB` | C:8 M:5 Y:4 K:4 | Rules, borders, table lines |
| Gray 50 | `#F9FAFB` | C:2 M:1 Y:1 K:1 | Table header backgrounds |
| White | `#FFFFFF` | C:0 M:0 Y:0 K:0 | Card backgrounds |
| Green 700 | `#15803D` | C:75 M:0 Y:85 K:30 | ESG text, green callout |
| Green 600 | `#16A34A` | C:70 M:0 Y:80 K:15 | Positive values, opportunity bullets |
| Green 100 | `#DCFCE7` | C:12 M:0 Y:10 K:0 | Green callout background |
| Red 600 | `#DC2626` | C:0 M:90 Y:85 K:5 | Negative values, risk bullets |
| Red 100 | `#FEE2E2` | C:0 M:10 Y:8 K:0 | (reserved for alerts) |
| Amber 600 | `#D97706` | C:0 M:55 Y:95 K:10 | Amber values, caution callout border |
| Amber 50 | `#FFFBEB` | C:0 M:1 Y:6 K:0 | Amber callout background |
| Indigo | `#6366F1` | C:60 M:60 Y:0 K:0 | Convertible allocation bar |

---

## 3. Paragraph Styles

Create these styles in InDesign. The XML `aid:pstyle` values match these names exactly (case-sensitive) for "Map By Name" import.

### Headers & Titles

| Style Name | Font | Size | Weight | Colour | Leading | Space After | Notes |
|------------|------|------|--------|--------|---------|-------------|-------|
| **Fund Title** | Inter | 16pt | ExtraBold (800) | White | 18pt | 2pt | Used on dark header band |
| **Fund Subtitle** | Inter | 8pt | Regular (400) | White 65% opacity | 10pt | 0 | Below fund title |
| **Report Date** | Inter | 8pt | SemiBold (600) | White 80% opacity | 10pt | 0 | Right-aligned |
| **Badge** | Inter | 7pt | SemiBold (600) | White | 9pt | 0 | Pill-shaped with rounded rectangle frame |

### Section Headings

| Style Name | Font | Size | Weight | Colour | Leading | Space Before / After | Notes |
|------------|------|------|--------|--------|---------|----------------------|-------|
| **Section Heading** | Inter | 10pt | Bold (700) | Navy 900 | 13pt | 8pt / 5pt | Rule below: 1.5pt Gray 200 |
| **Section Description** | Inter | 7pt | Regular (400) | Slate 400 | 9pt | 0 / 0 | Below section heading |
| **Subsection Heading** | Inter | 8pt | Bold (700) | Navy 900 | 10pt | 6pt / 4pt | Within cards |

### Body & Commentary

| Style Name | Font | Size | Weight | Colour | Leading | Space After |
|------------|------|------|--------|--------|---------|-------------|
| **Commentary Body** | Inter | 8pt | Regular (400) | Slate 600 | 12.4pt (155%) | 7pt |
| **Disclaimer** | Inter | 6.5pt | Regular (400) | Amber 600 | 8pt | 0 |

### Metric Cards

| Style Name | Font | Size | Weight | Colour | Alignment |
|------------|------|------|--------|--------|-----------|
| **Metric Label** | Inter | 5.5pt | Bold (700) | Slate 400 | Centre, uppercase, tracking +80 |
| **Metric Value Positive** | Inter | 14pt | ExtraBold (800) | Green 600 | Centre |
| **Metric Value Negative** | Inter | 14pt | ExtraBold (800) | Red 600 | Centre |
| **Metric Value Neutral** | Inter | 14pt | ExtraBold (800) | Navy 900 | Centre |
| **Metric Value Amber** | Inter | 14pt | ExtraBold (800) | Amber 600 | Centre |
| **Metric Context** | Inter | 6pt | Regular (400) | Slate 400 | Centre |

### Investor Profile

| Style Name | Font | Size | Weight | Colour | Notes |
|------------|------|------|--------|--------|-------|
| **Profile Label** | Inter | 5.5pt | Bold (700) | Blue 600 | Uppercase, tracking +60 |
| **Profile Value** | Inter | 8pt | SemiBold (600) | Navy 900 | — |

### Tables

| Style Name | Font | Size | Weight | Colour | Alignment | Notes |
|------------|------|------|--------|--------|-----------|-------|
| **Table Caption** | Inter | 8pt | Bold (700) | Navy 900 | Left | Space below: 5pt |
| **Table Header** | Inter | 6pt | SemiBold (600) | Slate 500 | Left | Uppercase, tracking +40, bg: Gray 50 |
| **Table Header Right** | Inter | 6pt | SemiBold (600) | Slate 500 | Right | Same as above, right-aligned |
| **Table Header Dark** | Inter | 6pt | SemiBold (600) | White | Left | bg: Navy 900 (scenario table) |
| **Table Header Dark Right** | Inter | 6pt | SemiBold (600) | White | Right | bg: Navy 900 |
| **Table Cell** | Inter | 7.5pt | Regular (400) | Slate 600 | Left | — |
| **Table Cell Right** | Inter | 7.5pt | Regular (400) | Slate 600 | Right | — |
| **Table Cell Label** | Inter | 7.5pt | SemiBold (600) | Navy 900 | Left | First column |
| **Table Cell Label Bold** | Inter | 7.5pt | Bold (700) | Navy 900 | Left | Highlight row fund name |
| **Table Cell Positive** | Inter | 7.5pt | SemiBold (600) | Green 600 | Right | Positive returns |
| **Table Cell Negative** | Inter | 7.5pt | SemiBold (600) | Red 600 | Right | Negative returns |
| **Table Cell Amber** | Inter | 7.5pt | SemiBold (600) | Amber 600 | Left | Scenario labels |
| **Table Footnote** | Inter | 5.5pt | Regular (400) | Slate 400 | Left | Space before: 5pt |

### Callouts

| Style Name | Font | Size | Weight | Colour | Notes |
|------------|------|------|--------|--------|-------|
| **Callout Blue** | Inter | 7.5pt | Regular (400) | Navy 900 | Frame: bg Blue 50, left border 3pt Blue 600, rounded 6pt |
| **Callout Green** | Inter | 7.5pt | Regular (400) | Green 700 | Frame: bg Green 100, left border 3pt Green 600 |
| **Callout Amber** | Inter | 7.5pt | Regular (400) | Slate 600 | Frame: bg Amber 50, left border 3pt Amber 600 |

### Outlook

| Style Name | Font | Size | Weight | Colour | Alignment |
|------------|------|------|--------|--------|-----------|
| **Outlook Indicator** | Inter | 10pt | Regular | Navy 900 | Centre |
| **Outlook Label** | Inter | 5.5pt | SemiBold (600) | Slate 400 | Centre, uppercase, tracking +40 |
| **Outlook Value Positive** | Inter | 7pt | Bold (700) | Green 600 | Centre |
| **Outlook Value Neutral** | Inter | 7pt | Bold (700) | Navy 900 | Centre |
| **Outlook Value Amber** | Inter | 7pt | Bold (700) | Amber 600 | Centre |

### Lists (Opportunities & Risks)

| Style Name | Font | Size | Weight | Colour | Bullet |
|------------|------|------|--------|--------|--------|
| **List Heading Green** | Inter | 8pt | Bold (700) | Green 700 | — |
| **List Heading Red** | Inter | 8pt | Bold (700) | Red 600 | — |
| **Opportunity Item** | Inter | 7pt | Regular (400) | Slate 600 | 4pt circle Green 600, left indent 10pt |
| **Risk Item** | Inter | 7pt | Regular (400) | Slate 600 | 4pt circle Red 600, left indent 10pt |

### ESG

| Style Name | Font | Size | Weight | Colour | Notes |
|------------|------|------|--------|--------|-------|
| **ESG Badge** | Inter | 6pt | Bold (700) | Green 700 | Uppercase, tracking +40, bg Green 100, pill frame |
| **ESG Body** | Inter | 7.5pt | Regular (400) | Slate 600 | Line height 1.6 |
| **ESG Link** | Inter | 7pt | Regular (400) | Slate 500 | — |

### Team

| Style Name | Font | Size | Weight | Colour |
|------------|------|------|--------|--------|
| **Team Initials** | Inter | 6pt | Bold (700) | White (on Navy 900 circle) |
| **Team Name** | Inter | 7.5pt | SemiBold (600) | Navy 900 |
| **Team Role** | Inter | 6pt | Regular (400) | Slate 400 |

### Fund Info

| Style Name | Font | Size | Weight | Colour | Alignment |
|------------|------|------|--------|--------|-----------|
| **Info Group Heading** | Inter | 8pt | Bold (700) | Navy 900 | Left |
| **Info Label** | Inter | 7pt | Regular (400) | Slate 400 | Left |
| **Info Value** | Inter | 7pt | SemiBold (600) | Navy 900 | Right |

### CTA

| Style Name | Font | Size | Weight | Colour |
|------------|------|------|--------|--------|
| **CTA Heading** | Inter | 9pt | Bold (700) | White |
| **CTA Body** | Inter | 7pt | Regular (400) | White 70% opacity |
| **CTA Link** | Inter | 7pt | SemiBold (600) | Navy 900 (on white pill) |
| **CTA Link Secondary** | Inter | 7pt | SemiBold (600) | White (on transparent pill) |

### Author

| Style Name | Font | Size | Weight | Colour |
|------------|------|------|--------|--------|
| **Author Initials** | Inter | 6pt | Bold (700) | White (on Navy 900 circle 24pt) |
| **Author Name** | Inter | 7pt | SemiBold (600) | Navy 900 |
| **Author Role** | Inter | 6pt | Regular (400) | Slate 400 |

### Footnotes & Legal

| Style Name | Font | Size | Weight | Colour | Notes |
|------------|------|------|--------|--------|-------|
| **Footnote** | Inter | 6pt | Regular (400) | Slate 400 | Numbered list, left indent 12pt |
| **Attribution** | Inter | 6pt | Regular (400) | Slate 400 | Space before: 4pt |
| **Legal Heading** | Inter | 6.5pt | Bold (700) | Slate 600 | — |
| **Legal Body** | Inter | 6.5pt | Regular (400) | Slate 400 | Line height 1.6, space after 5pt |
| **Legal Signoff** | Inter | 7pt | SemiBold (600) | Slate 600 | Space before: 10pt |
| **Risk Note** | Inter | 6pt | Regular (400) | Slate 400 | — |

### Page Footer

| Style Name | Font | Size | Weight | Colour | Alignment |
|------------|------|------|--------|--------|-----------|
| **Page Footer Brand** | Inter | 6.5pt | SemiBold (600) | Slate 300 | Left, tracking +40 |
| **Page Footer Number** | Inter | 7pt | Medium (500) | Slate 400 | Right |

---

## 4. Character Styles

| Style Name | Weight | Colour | Notes |
|------------|--------|--------|-------|
| **Commentary Label** | Bold (700) | Navy 900 | Inline bold labels within commentary paragraphs |
| **Callout Heading** | Bold (700) | (inherits parent) | Inline bold heading within callout text |

---

## 5. Table Styles

Create the following table styles and cell styles:

### Table Style: "Data Table"
- Row stroke: 0.5pt Gray 200
- Column stroke: None
- Header row fill: Gray 50
- Alternating row fill: None (or very subtle Gray 50 every other row)
- Cell insets: Top/Bottom 3.5pt, Left/Right 6pt

### Table Style: "Dark Header Table" (for scenario table)
- Same as Data Table but header row fill: Navy 900, header text: White

### Table Style: "Peer Table"
- Same as Data Table
- Apply "highlight row" cell style to the fund's own row: fill Blue 50

---

## 6. Object Styles

| Object Style | Description |
|--------------|-------------|
| **Card Frame** | Fill: White, Stroke: 0.5pt Gray 200, Corner radius: 8pt, Shadow: 1pt Y offset, 2pt blur, 4% opacity |
| **Header Band** | Fill: Navy 900 to Navy 700 gradient (135°), bleeds to trim on top/left/right |
| **Callout Blue** | Fill: Blue 50, Left stroke: 3pt Blue 600, Corner radius: 6pt |
| **Callout Green** | Fill: Green 100, Left stroke: 3pt Green 600, Corner radius: 6pt |
| **Callout Amber** | Fill: Amber 50, Left stroke: 3pt Amber 600, Corner radius: 6pt |
| **ESG Card** | Fill: Green 50, Stroke: 0.5pt Green 100, Corner radius: 8pt |
| **CTA Strip** | Fill: Navy 900 to Navy 700 gradient, Corner radius: 8pt |
| **Team Card** | Fill: Gray 50, Stroke: 0.5pt Gray 200, Corner radius: 6pt |
| **Badge Pill** | Fill: varies, Corner radius: 100pt (fully rounded), Inset: 2pt top/bottom, 8pt left/right |
| **Page Footer Rule** | Stroke: 1pt Gray 200, positioned at 0.45in from bottom |

---

## 7. XML Import Workflow

### Step 1: Prepare Template
1. Create a 6-page US Letter document with the setup above
2. Create all Paragraph Styles, Character Styles, and Colour Swatches
3. Place text frames on each page (primary story frame + footer frames)

### Step 2: Import XML
1. **File > Import XML** → select `allianz_factsheet_indesign.xmp`
2. The Structure panel will populate with the document tree
3. Open the **Tags panel** → flyout menu → **Map Tags to Styles**
4. Click **Map By Name** — this links all `aid:pstyle` tags to matching Paragraph Styles

### Step 3: Place Content
1. Drag the `<factsheet>` root element from the Structure panel into your primary text frame
2. Tables with `aid:table="table"` attributes auto-create InDesign tables
3. Chart placeholders (`<chart-placeholder>`) → right-click in structure → place your chart image/graphic
4. Allocation, sector, and rating data elements → build as anchored graphics using the weight/color attributes

### Step 4: Tagged PDF Export
1. **File > Export > Adobe PDF (Print)**
2. Enable **Create Tagged PDF** checkbox
3. The XML structure maps directly to PDF tags for accessibility:
   - `<section-heading>` → `<H2>`
   - `<subsection-heading>` → `<H3>`
   - `<commentary-paragraph>` → `<P>`
   - `<data-table>` → `<Table>`
   - `<list-item>` → `<LI>`
   - `<chart-placeholder alt="...">` → `<Figure>` with alt text
4. Verify in Acrobat: **Accessibility > Full Check**

---

## 8. Accessibility Checklist for InDesign

- [ ] All images and charts have alt text (provided in `alt` attributes)
- [ ] Reading order matches visual order (check Articles panel)
- [ ] Tables have header rows marked in Table > Table Options
- [ ] Document language set to English (File > File Info > Advanced)
- [ ] All text is live (no images of text)
- [ ] Colour contrast meets WCAG AA (4.5:1 for body text, 3:1 for large text)
- [ ] Tagged PDF export enabled
- [ ] PDF/UA compliance verified in Acrobat Pro

---

## 9. Data Attributes Reference

The XML includes structured data attributes for programmatic chart/graphic generation:

| Element | Attributes | Purpose |
|---------|-----------|---------|
| `<allocation-item>` | `asset`, `weight`, `color` | Build allocation bar graphic |
| `<sector-item>` | `name`, `weight`, `color` | Build sector bar chart |
| `<rating-item>` | `grade`, `category`, `weight`, `color` | Build credit rating bars |
| `<key-metric>` | `label`, `value` | Populate metric card frames |
| `<risk-indicator>` | `level`, `max` | Build risk scale graphic |
| `<chart-annotation>` | `position`, `year`, `color` | Position annotations on chart |
| `<table-row highlight="true">` | `highlight` | Apply highlight row cell style |
