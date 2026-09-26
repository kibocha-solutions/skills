# Taste, Aesthetic Archetypes, and Anti-Slop Discipline

This reference defines the calibration parameters, design archetypes, and deterministic anti-pattern rules that elevate user interfaces from generic AI boilerplate to legendary craft.

## 1. Taste Calibration Dials

Every interface must establish explicit positions on two primary design axes:

### Information Density Dial (1 to 10)
- **1 to 3 (Expansive / Narrative)**: Large hero typography, generous padding (64px to 128px), single-column reading paths, maximum visual breathing room. Best for brand marketing, editorial landing pages, luxury showcases.
- **4 to 6 (Balanced / Productivity)**: Standard 16px to 24px container padding, 48px input heights, multi-column modular grids. Best for standard SaaS dashboards, consumer applications, settings portals.
- **7 to 10 (Compact / Dense Utility)**: 8px to 12px cell padding, 28px to 32px table row heights, monospace numerical alignment, minimal ornamentation, high data throughput. Best for developer consoles, financial trading screens, logistics management.

### Structural Variance Dial (1 to 10)
- **1 to 3 (Strict Symmetry)**: Rigid 12-column grid, uniform card dimensions, predictable vertical cadence. Best for corporate documentation, compliance portals, enterprise forms.
- **4 to 6 (Curated Contrast)**: Balanced layout with one deliberate asymmetrical hero or feature block. Secondary cards vary in column span (e.g. 8-column primary card paired with 4-column telemetry card).
- **7 to 10 (Expressive / Dynamic)**: Overlapping containers, editorial typography scales, diagonal section dividers, interactive spatial transitions. Best for creative tools, gaming interfaces, cultural platforms.

---

## 2. Curated Style Archetypes

Select exactly one archetype to anchor the visual language:

### Archetype A: Clean Functional (Modern SaaS)
- **Palette**: Neutral monochromatic base (slate or zinc), pure white/dark surface, one saturated brand accent.
- **Typography**: Crisp modern sans-serif (Inter, SF Pro, Geist). Small tracking tweaks on headings (`tracking-tight`).
- **Containers**: 1px subtle border (`border-zinc-200` / `border-zinc-800`), 6px to 8px border radius, no heavy drop shadows.
- **Micro-interactions**: Instant border highlight on hover, snappy button states (`100ms`).

### Archetype B: Refined Editorial
- **Palette**: Warm paper tones (eggshell, warm stone, charcoal text).
- **Typography**: High-legibility serif display face (Newsreader, Fraunces, Playfair) paired with a clean neutral sans-serif body.
- **Containers**: Structural hairline dividers, generous top and bottom padding, asymmetric text blocks.
- **Micro-interactions**: Underline fill transitions, subtle opacity fades (`200ms`).

### Archetype C: Dense Utility
- **Palette**: Dark or neutral gray background, high-contrast white content, semantic status colors (emerald, amber, rose).
- **Typography**: Monospace or tabular figures for data (`font-mono` / `tabular-nums`), compact uppercase headers (11px, `tracking-wider`).
- **Containers**: Sharp or minimal radius (2px to 4px), visible table gridlines, compact action bars.
- **Micro-interactions**: Direct keyboard shortcut badges, instant row selection highlights.

### Archetype D: Soft Tactile
- **Palette**: Muted pastels, soft tonal surfaces, deep dark charcoal text.
- **Typography**: Rounded or humanist sans-serif.
- **Containers**: Large rounded corners (16px to 24px), subtle inset highlights (`box-shadow: inset 0 1px 0 rgba(255,255,255,0.1)`).
- **Micro-interactions**: Spring-based bounce on touch-down, fluid drag-to-dismiss sheets.

### Archetype E: Bold Contemporary
- **Palette**: High-contrast dark mode or stark brutalist black/white with electric neon accent.
- **Typography**: Heavy grotesque or geometric display type, oversized numeric metrics.
- **Containers**: Solid high-contrast borders (2px solid), sharp corners (0px) or full pills (9999px).
- **Micro-interactions**: Snappy scale jumps, high-velocity spring transitions.

---

## 3. Deterministic Anti-Slop Rules

Never implement any of the following patterns:

1. **The AI Broadsheet Default**: Do not combine cream backgrounds, high-contrast serif headlines, and terracotta accents unless the user explicitly requested that exact palette.
2. **The Acid Dark Default**: Do not pair a pitch-black surface with a single neon lime or cyan accent as a substitute for thought.
3. **Card Uniformity**: Do not build interfaces out of identical rounded rectangles with uniform drop shadows (`shadow-lg`). Differentiate primary objects with scale, borders, or layout position.
4. **Gratuitous Gradients**: Do not use multi-color gradient background blobs or animated mesh gradients behind standard content text.
5. **Eyebrow Abuse**: Do not put an all-caps, tracked-out label (e.g. `FEATURES`, `TESTIMONIALS`) above every single heading.
6. **Headline Highlighting**: Do not highlight a single word in a headline with a different accent color or gradient text.
7. **Punctuation Metadata**: Do not link metadata items with spaced middle dots (`Post · 5 min read · Design`). Use whitespace, font weights, or subtle badges instead.
8. **Automatic Arrow Suffixes**: Never append `→` or `&rarr;` automatically to buttons or links unless the action specifically represents forward pagination or next step.
9. **Universal Hover Zoom**: Never apply `hover:scale-105` to every card in a grid. Motion must encode actionable interactivity.
