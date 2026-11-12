# Interface Design Examples

## 1. Token contract and anti-slop discipline

### Bad

1. Use hard-coded hex colors (`#faf6f0`, `#d97757`, `#141413`) and a generic serif headline on every marketing or SaaS brief without consulting the brand.
2. Add all-caps eyebrow labels above every heading, middle-dot metadata chains (`·`), and hover-zoom animations on every card.
3. Give both an outer card (`rounded-2xl`, 16px) and its inner image (`rounded-2xl`, 16px) the same border radius despite `16px` padding.

### Good

1. Calibrate Density and Variance dials to the brief, select one primary archetype, and record semantic tokens (`--surface-primary`, `--content-primary`, `--accent-default`) in `DESIGN.md`.
2. Apply $\text{Radius}_{\text{inner}} = \max(0, \text{Radius}_{\text{outer}} - \text{Padding})$ so a `16px` outer card with `12px` padding uses a `4px` inner radius.
3. Keep copy in sentence case with action-oriented button labels (`Save draft`, `Export report`) and omit decorative arrows (`→`).

## 2. Dual-orientation mobile and tablet layout

### Bad

1. Place primary checkout or filter actions in the top navigation bar on phone portrait.
2. Render stacked full-width form rows in phone landscape (<450px height), pushing the submit button below the fold.
3. Stretch 120-character body paragraphs edge-to-edge on tablet portrait.

### Good

1. Anchor primary actions in the lower 40% thumb zone on phone portrait with `env(safe-area-inset-bottom)` clearance.
2. Collapse top bars into a compact side rail and pair form fields side-by-side in phone landscape.
3. Use a 2-column adaptive layout on tablet portrait (body text capped at 65 to 75 characters) and a master-detail dual-pane layout on tablet landscape.
