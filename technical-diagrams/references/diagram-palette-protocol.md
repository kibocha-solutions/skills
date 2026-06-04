# Diagram Palette Protocol

Use this reference before assigning colors to a diagram.

## Lookup Order

Before searching broadly, inspect saved diagram assets in the target project:

1. `docs/diagrams/assets/palette.json`
2. `docs/diagrams/assets/style-tokens.json`
3. `docs/diagrams/assets/geometry.json`
4. `docs/diagrams/<diagram-family>/assets/*.palette.json`

If no diagram palette exists, inspect reliable project design sources:

- CSS variables
- Tailwind or theme configuration
- brand guide
- logo SVG
- existing diagram set
- app shell or product screenshots
- documentation theme

If a reliable project palette exists, create a diagram-safe palette from it. If
palette inference is weak or inconsistent, state that no reliable project
palette was found and use `assets/default-palette.json`.

## Shade Roles

Every color family used in a production diagram must define at least:

- fill
- border
- header when headers are used
- text

Large component backgrounds must use pale tints. Borders, headers, arrows, and
small accents carry stronger color identity.

## Semantic Use

Colors must encode meaning or hierarchy:

- primary: core system or primary flow
- secondary: external systems or supporting services
- neutral: containers, groups, notes, ordinary databases
- green: success, approved, healthy, available
- amber: warning, pending, review, risk
- red: error, blocked, danger, security risk
- blue: information, control path, primary technical flow

Do not use red, amber, or green as ordinary category colors. Limit category
colors to three plus neutral and semantic colors.

## Palette Files

Create or update palette files deliberately. Do not silently diverge from an
existing palette for one diagram.

A reusable palette should include:

- page background
- primary, secondary, and label text
- core system fill and border
- external system fill and border
- data store fill and border
- container fill and border
- risk, warning, and success roles
- arrow stroke and label background

Use diagram-family override palettes only when the family has special semantics
such as activity decisions, deployment zones, threat boundaries, or permission
layers.
