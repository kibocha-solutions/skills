---
name: web-design
description: Implement distinctive, production-grade websites and responsive web applications from design contracts or specifications. Replaces and extends frontend-design. Covers modern CSS architecture, semantic HTML, CSS custom properties, container queries, fluid typography, WCAG 2.2 AA accessibility, Emil Kowalski spring motion, Rauno Freiberg craft details, and Playwright verification. Use for web design, frontend design, frontend development, responsive web apps, HTML/CSS layouts, Tailwind styling, React views, UI components, and web accessibility.
license: Complete terms in LICENSE.txt
---

# Web Design and Implementation

## 1. Ingest the design contract

1. Read the project `DESIGN.md` contract.
2. If `DESIGN.md` is absent, invoke `interface-design` to establish tokens, taste dials, and wireframes before writing code.
3. Identify required breakpoints, responsive layout behavior, and supported input modalities (mouse, trackpad, touch).
4. Preserve the established visual direction and typography choices.

## 2. Implement the token system

Read [modern CSS and tokens](references/modern-css-and-tokens.md) for custom property structure and fluid scales.

1. Implement confirmed tokens as CSS custom properties under `:root` and `[data-theme]`:
   - Surface colors: `--surface-primary`, `--surface-secondary`, `--surface-elevated`
   - Content colors: `--content-primary`, `--content-secondary`, `--content-muted`
   - Accent colors: `--accent-default`, `--accent-hover`, `--accent-subtle`
   - Feedback colors: `--feedback-error`, `--feedback-warning`, `--feedback-success`, `--feedback-info`
   - Radius tokens: `--radius-sm`, `--radius-md`, `--radius-lg`
2. Implement fluid typography and spacing scales using `clamp()` formulas.
3. Keep body line length below 75 characters (`max-width: 68ch`).
4. Ensure theme switching works cleanly via custom properties without duplicating component layout classes.

## 3. Implement semantic markup and hierarchy

1. Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`, `<button>`).
2. Never use `<div>` or `<span>` for clickable controls. Always use `<button type="button">`, `<button type="submit">`, or `<a href="...">`.
3. Provide descriptive `aria-label` or `aria-labelledby` attributes when interactive controls lack visible text.
4. Associate form inputs with labels using `for` and `id` attributes.
5. Link form error messages to inputs using `aria-invalid="true"` and `aria-describedby`.
6. Add alt text to meaningful imagery. Hide decorative images with `aria-hidden="true"`.

## 4. Implement responsive layout architecture

1. Build layouts container-first using CSS container queries (`@container`) rather than relying solely on global viewport queries.
2. Use CSS grid and subgrid for multi-column alignments and card groups.
3. Implement responsive behavior down to a minimum width of 320px.
4. Support mobile web viewports with safe area padding:
   ```css
   padding-bottom: env(safe-area-inset-bottom, 16px);
   ```
5. Apply the nested border radius formula:
   $$\text{Radius}_{\text{inner}} = \max(0, \text{Radius}_{\text{outer}} - \text{Padding})$$
6. Prevent horizontal viewport overflow.

## 5. Implement motion and interaction physics

Read [Emil Kowalski interaction and motion](references/emil-kowalski-interaction-and-motion.md) for timing brackets and spring curve parameters.

1. Enforce frequency-based duration brackets:
   - High-frequency actions (buttons, toggles, checkboxes): 100ms to 150ms.
   - Medium-frequency actions (menus, dropdowns, tooltips): 150ms to 200ms.
   - Low-frequency actions (modals, drawers, sheets): 200ms to 280ms.
2. Apply damped spring physics curves instead of linear or generic transitions.
3. Anchor spatial transforms to the trigger element's bounding box (`transform-origin`).
4. Implement tactile touch-down feedback on interactive elements:
   ```css
   button:active {
     transform: scale(0.98);
     transition: transform 75ms ease-out;
   }
   ```
5. Wrap all animations in `@media (prefers-reduced-motion: reduce)` to disable non-essential motion.

## 6. Verify accessibility (WCAG 2.2 AA)

1. Verify text contrast ratios:
   - Normal text: minimum 4.5:1 ratio against surface.
   - Large text (>=18pt or >=14pt bold): minimum 3:1 ratio.
   - Interactive boundaries and icons: minimum 3:1 ratio against background.
2. Preserve high-contrast `:focus-visible` indicators on all keyboard-navigable elements. Never suppress outlines without an explicit focus ring replacement.
3. Verify logical DOM focus order matching visual reading flow.
4. Ensure minimum interactive touch target dimensions:
   - Desktop pointer controls: minimum 24x24px (WCAG 2.2 SC 2.5.8).
   - Mobile web touch controls: minimum 44x44px.

## 7. Inspect and verify in browser

Inspect [good vs bad web patterns](examples/good-vs-bad-web-patterns.md) for focus rings and validation states.

1. Run the project formatter, linter, type checker, and test suite.
2. Capture full-page screenshots at desktop (1280px), tablet (768px), and mobile (375px) viewports using Playwright MCP or local CLI.
3. Verify layout behavior across all supported viewports:
   - Check for unwanted text clipping, line wrapping, or dead space.
   - Inspect focus indicators in keyboard navigation.
   - Verify empty, loading, error, and success states for dynamic components.
4. Correct any identified visual or behavioral defects.

## 8. Pre-completion checklist

Before delivering completed web design code, confirm evidence exists for each item:

- [ ] Design tokens derived from `DESIGN.md` and implemented via CSS custom properties.
- [ ] Semantic HTML elements used for all document landmarks and interactive controls.
- [ ] Container queries (`@container`) and fluid typography (`clamp()`) applied.
- [ ] Nested border radius math applied to all nested containers.
- [ ] Frequency-based motion durations (100 to 150ms for buttons) and spring curves implemented.
- [ ] Active touch-down scale feedback (`active:scale-[0.98]`) implemented.
- [ ] WCAG 2.2 AA contrast and `:focus-visible` rings verified.
- [ ] Safe area insets handled for mobile viewports.
- [ ] Playwright screenshots captured and inspected at 375px, 768px, and 1280px widths.
- [ ] Zero AI attribution in code, markup, comments, or documentation.
- [ ] No U+2014 em dashes in normal prose.
