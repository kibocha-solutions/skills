---
name: web-design
description: Implement distinctive, production-grade websites and responsive web applications from design contracts or specifications. Replaces and extends frontend-design. Covers modern CSS architecture, semantic HTML, CSS custom properties, container queries, fluid typography, WCAG 2.2 AA accessibility, Baseline browser support, Google Modern Web Guidance, Core Web Vitals, Emil Kowalski spring motion, Rauno Freiberg craft details, anti-slop detection, and Playwright verification. Use for web design, frontend design, frontend development, responsive web apps, HTML/CSS layouts, client-side JavaScript UI, Tailwind styling, React views, UI components, web accessibility, web performance, and modernizing legacy web code.
license: Complete terms in LICENSE.txt
---

# Web Design and Implementation

## 1. Ingest the design contract

1. Read the project `DESIGN.md` contract.
2. If `DESIGN.md` is absent, invoke `interface-design` to establish tokens, taste dials, and wireframes before writing code.
3. Identify required breakpoints, responsive layout behavior, and supported input modalities (mouse, trackpad, touch).
4. Preserve the established visual direction and typography choices.
5. Read the `Standards` section of `DESIGN.md` and the [web standards catalogue](../interface-design/references/web-standards-catalogue.md). Apply every selected standard, and implement only the design foundation `DESIGN.md` names.

## 2. Apply modern platform guidance

1. Run `python3 <steward-skill-dir>/scripts/steward.py tool ensure modern-web-guidance`.
2. Read the project's Baseline target from `AGENTS.md` or `CLAUDE.md`. Use Baseline Widely available when none is set, and suggest recording a target in chat.
3. List each platform capability or UI pattern the task touches, such as a dialog, popover, form validation, container query, view transition, image loading, or date handling.
4. Run `modern-web-guidance search "<query>"` for each capability before writing its code:
   - Write two to five words naming the user-visible capability and its UI primitive, such as `light dismiss dialog` or `responsive data table`.
   - Omit framework, library, product, route, and file names.
   - Split a compound capability into separate searches.
5. Rephrase a search once with the concrete HTML or CSS component noun when no result describes the capability. Continue without a guide when the topic is not covered.
6. Run `modern-web-guidance retrieve "<id>[,<id>]"` for each matching guide and the broader discipline guide that applies, such as `forms`, `accessibility`, or `performance`. Read the output in full; when it is saved to a file, read that file in full, then delete it.
7. Apply the guide's pattern and every fallback required by the Baseline target. Adapt the pattern to the project framework without dropping the platform feature.
8. Take appearance from `DESIGN.md` and the selected foundation, and take platform features, markup, and fallbacks from the guide. Report any conflict between them to the user instead of choosing one.
9. Run `modern-web-guidance legacy-scan <path> --json` only for a request to modernize or audit a codebase without a named feature. Drop findings that fail their `keepWhen` or `dropWhen` rule, report the rest, and change code only when the user asked to modernize.

## 3. Implement the token system

1. Read [modern CSS and tokens](references/modern-css-and-tokens.md) for custom property structure and fluid scales.
2. Implement the tokens named in `DESIGN.md` as CSS custom properties under `:root` and `[data-theme]`. Keep the selected foundation's role names; for a product's own system, use:
   - Surface colors: `--surface-primary`, `--surface-secondary`, `--surface-elevated`
   - Content colors: `--content-primary`, `--content-secondary`, `--content-muted`
   - Accent colors: `--accent-default`, `--accent-hover`, `--accent-subtle`
   - Feedback colors: `--feedback-error`, `--feedback-warning`, `--feedback-success`, `--feedback-info`
   - Radius tokens: `--radius-sm`, `--radius-md`, `--radius-lg`
3. Implement fluid typography and spacing scales using `clamp()` formulas.
4. Keep body line length below 75 characters (`max-width: 68ch`).
5. Ensure theme switching works cleanly via custom properties without duplicating component layout classes.

## 4. Implement semantic markup and hierarchy

1. Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`, `<button>`).
2. Never use `<div>` or `<span>` for clickable controls. Always use `<button type="button">`, `<button type="submit">`, or `<a href="...">`.
3. Provide descriptive `aria-label` or `aria-labelledby` attributes when interactive controls lack visible text.
4. Associate form inputs with labels using `for` and `id` attributes.
5. Link form error messages to inputs using `aria-invalid="true"` and `aria-describedby`.
6. Add alt text to meaningful imagery. Hide decorative images with `aria-hidden="true"`.

## 5. Implement responsive layout architecture

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

## 6. Implement motion and interaction physics

1. Take motion curves and durations from the selected foundation when it defines them, such as Material 3 motion or Apple HIG animation. Apply steps 3 to 6 only to a product's own system.
2. Read [Emil Kowalski interaction and motion](references/emil-kowalski-interaction-and-motion.md) for timing brackets and spring curve parameters.
3. Enforce frequency-based duration brackets:
   - High-frequency actions (buttons, toggles, checkboxes): 100ms to 150ms.
   - Medium-frequency actions (menus, dropdowns, tooltips): 150ms to 200ms.
   - Low-frequency actions (modals, drawers, sheets): 200ms to 280ms.
4. Apply damped spring physics curves instead of linear or generic transitions.
5. Anchor spatial transforms to the trigger element's bounding box (`transform-origin`).
6. Implement tactile touch-down feedback on interactive elements:
   ```css
   button:active {
     transform: scale(0.98);
     transition: transform 75ms ease-out;
   }
   ```
7. Wrap all animations in `@media (prefers-reduced-motion: reduce)` to disable non-essential motion.

## 7. Verify accessibility (WCAG 2.2 AA)

1. Verify text contrast ratios:
   - Normal text: minimum 4.5:1 ratio against surface.
   - Large text (>=18pt or >=14pt bold): minimum 3:1 ratio.
   - Interactive boundaries and icons: minimum 3:1 ratio against background.
2. Preserve high-contrast `:focus-visible` indicators on all keyboard-navigable elements. Never suppress outlines without an explicit focus ring replacement.
3. Verify logical DOM focus order matching visual reading flow.
4. Ensure minimum interactive touch target dimensions:
   - Desktop pointer controls: minimum 24x24px (WCAG 2.2 SC 2.5.8).
   - Mobile web touch controls: minimum 44x44px.

## 8. Inspect and verify in browser

1. Inspect [good vs bad web patterns](examples/good-vs-bad-web-patterns.md) for focus rings and validation states.
2. Run the project formatter, linter, type checker, and test suite.
3. Capture full-page screenshots at desktop (1280px), tablet (768px), and mobile (375px) viewports using Playwright MCP or local CLI.
4. Verify layout behavior across all supported viewports:
   - Check for unwanted text clipping, line wrapping, or dead space.
   - Inspect focus indicators in keyboard navigation.
   - Verify empty, loading, error, and success states for dynamic components.
5. Check the code against every guide retrieved in Section 2, including its fallbacks.
6. Run `python3 <steward-skill-dir>/scripts/steward.py tool ensure impeccable`, then `impeccable detect --json <changed markup files or directories>`. Treat exit status 2 as findings. Resolve each finding, or record in `DESIGN.md` the brief requirement that justifies it.
7. When the change affects loading, rendering, or interaction, record a lab performance trace on a throttled mobile profile, using Lighthouse or Chrome DevTools, and confirm the Core Web Vitals thresholds in the [web standards catalogue](../interface-design/references/web-standards-catalogue.md#2-universal-floor).
8. Correct any identified visual or behavioral defects.
9. Report the Modern Web Guidance guide IDs applied, or the capabilities searched without a matching guide.

## 9. Pre-completion checklist

Before delivering completed web design code, confirm evidence exists for each item:

- [ ] Standards and the single design foundation in `DESIGN.md` applied; no component or token from another foundation.
- [ ] Baseline target identified; Modern Web Guidance searched for every platform capability, and each retrieved guide and its fallbacks applied.
- [ ] Design tokens derived from `DESIGN.md` and implemented via CSS custom properties.
- [ ] Semantic HTML elements used for all document landmarks and interactive controls.
- [ ] Container queries (`@container`) and fluid typography (`clamp()`) applied.
- [ ] Nested border radius math applied to all nested containers.
- [ ] Motion taken from the selected foundation, or frequency-based durations (100 to 150ms for buttons) and spring curves for a product's own system.
- [ ] `impeccable detect` clean or each finding justified in `DESIGN.md`.
- [ ] Core Web Vitals thresholds met in a lab trace when loading, rendering, or interaction changed.
- [ ] Active touch-down scale feedback (`active:scale-[0.98]`) implemented.
- [ ] WCAG 2.2 AA contrast and `:focus-visible` rings verified.
- [ ] Safe area insets handled for mobile viewports.
- [ ] Playwright screenshots captured and inspected at 375px, 768px, and 1280px widths.
- [ ] Zero AI attribution in code, markup, comments, or documentation.
- [ ] No U+2014 em dashes in normal prose.
