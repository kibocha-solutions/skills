# Web Standards Catalogue

Read this reference before designing or implementing a website, web application, progressive web application, or mobile web surface. It sets the minimum standard. A stricter or more specific standard required by the brief, jurisdiction, sector, or platform governs over it.

## Contents

1. Find the standards
2. Universal floor
3. Standards by product category
4. Keep one design foundation
5. Reject slop practices

## 1. Find the standards

1. Classify the product into every matching category in Section 3.
2. Apply every universal floor standard in Section 2.
3. Apply the standards listed for each matching category.
4. Select one design foundation under Section 4.
5. Open each source before relying on it and confirm its current edition. A newer edition at the source governs over the edition named here.
6. Search the publisher's site for a newer edition, standard, or research report when the source page is dated more than 12 months earlier.
7. Add any sector, jurisdiction, or platform standard the brief implies, and ask the user when the jurisdiction is unknown and a legal accessibility, privacy, or payment standard may apply.
8. Record the selected standards, the Baseline target, and the design foundation in the `Standards` section of `DESIGN.md`.

## 2. Universal floor

| Area | Standard | Source | Apply |
| :--- | :--- | :--- | :--- |
| Markup and platform APIs | HTML Living Standard; MDN Web Docs | https://html.spec.whatwg.org/ ; https://developer.mozilla.org/en-US/docs/Web | Use native elements and documented API behavior. Check compatibility tables before using an API. |
| Browser support | Baseline | https://web.dev/baseline ; https://web.dev/articles/how-to-choose-your-baseline-target | Read the project's Baseline target from `AGENTS.md` or `CLAUDE.md`. Use Baseline Widely available when none is set. Apply the fallback for every feature outside the target. |
| Modern implementation | Modern Web Guidance | https://developer.chrome.com/docs/modern-web-guidance | Query `modern-web-guidance` for each platform capability before writing it, as `web-design` directs. |
| Accessibility | WCAG 2.2 Level AA | https://www.w3.org/TR/WCAG22/ | Meet every Level A and AA success criterion. WCAG 3.0 is a Working Draft; never cite it as a requirement. |
| Widget behavior | WAI-ARIA Authoring Practices Guide | https://www.w3.org/WAI/ARIA/apg/ | Follow the APG pattern for each custom widget. Prefer a native element over ARIA. |
| Public procurement accessibility | EN 301 549 | https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf | Apply when the product serves European Union users, public bodies, or the European Accessibility Act. |
| Performance | Core Web Vitals | https://web.dev/articles/vitals | Reach LCP of 2.5 seconds or less, INP of 200 milliseconds or less, and CLS of 0.1 or less at the 75th percentile on mobile and desktop. |
| Security | OWASP Top 10:2025; OWASP ASVS 5.0.0 | https://owasp.org/Top10/ ; https://owasp.org/www-project-application-security-verification-standard/ | Address every Top 10 category. Verify against ASVS Level 1 at minimum and Level 2 for any product that handles personal, financial, or health data. |
| Usability | Nielsen Norman Group ten usability heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ | Review each screen against the ten heuristics before completion. |
| Internationalization | W3C Internationalization | https://www.w3.org/International/ | Declare the language, support right-to-left text when the audience requires it, and keep text out of images. |

## 3. Standards by product category

| Category | Examples | Add these standards | Foundation candidates |
| :--- | :--- | :--- | :--- |
| Marketing, brand, and landing sites | Product sites, campaigns, portfolios | Core Web Vitals on the slowest target device; every check in Section 5 | The brand's own system, documented in `DESIGN.md` |
| Editorial, content, and documentation sites | Publications, blogs, knowledge bases | Readable line length and type scale under `interface-design` Section 5; route documentation to `documentation/SKILL.md` | The brand's own system |
| E-commerce and checkout | Stores, booking, checkout flows | Baymard Institute research, https://baymard.com/research | The brand's own system; Polaris for Shopify admin apps |
| Productivity and collaboration apps | Project tools, editors, workspaces | Atlassian Design System, https://atlassian.design/ ; Fluent 2, https://fluent2.microsoft.design/ | One of Atlassian, Fluent 2, Material 3, or the product's own system |
| Data-dense enterprise apps and dashboards | Analytics, operations consoles, admin back offices | Carbon Design System, including its data visualization guidance, https://carbondesignsystem.com/ | Carbon or the product's own system |
| Developer tools | Code hosting, CI dashboards, consoles | Primer, https://primer.style/ | Primer or the product's own system |
| Creative tools | Media editors, design tools | Adobe Spectrum, https://spectrum.adobe.com/ | Spectrum or the product's own system |
| Public sector and civic services | Government services, licensing, benefits | GOV.UK Service Manual, https://www.gov.uk/service-manual ; GOV.UK Design System, https://design-system.service.gov.uk/ ; U.S. Web Design System, https://designsystem.digital.gov/ | The national design system of the serving government; GOV.UK patterns where none exists |
| Apps inside Shopify admin | Shopify embedded apps | Polaris web components, https://shopify.dev/docs/api/app-home/polaris-web-components | Polaris |
| Android-aligned products | Companion web apps and progressive web applications for Android products | Material 3, https://m3.material.io/ | Material 3 or Material 3 Expressive |
| Apple-aligned products | Companion web apps for Apple-platform products | Apple Human Interface Guidelines, https://developer.apple.com/design/human-interface-guidelines/ | Apple Human Interface Guidelines |
| Microsoft-aligned products | Microsoft 365 add-ins and companion apps | Fluent 2 | Fluent 2 |

## 4. Keep one design foundation

1. Select exactly one design foundation for each product surface: an established system from Section 3 or the product's own system documented in `DESIGN.md`.
2. Continue the foundation a project already uses. Propose a change in chat before replacing it.
3. Take tokens, color roles, type scale, shape, elevation, motion, iconography, components, and interaction patterns from the selected foundation only.
4. Never combine components, tokens, or interaction patterns from two foundations on one surface.
5. Map brand colors and typefaces onto the selected foundation's roles instead of adding parallel tokens.
6. Apply the density and variance dials and the style archetype within the selected foundation.
7. When the selected foundation is Material 3, use Material 3 color roles, type scale, shape scale, motion, and components on every screen.
8. When the selected foundation is Material 3 Expressive, apply its expressive shape, motion, and type to every component, not to selected screens.
9. On the web, `@material/web` has been in maintenance mode since 10 June 2024 and does not implement Material 3 Expressive. Implement Material 3 Expressive from the specifications and tokens at https://m3.material.io/, or use a maintained library that states the Material 3 version it implements. Record the choice in `DESIGN.md`.
10. When the selected foundation is the Apple Human Interface Guidelines, take navigation, controls, typography, and materials from them on every screen.
11. A product with separate native apps may use the Apple Human Interface Guidelines on Apple platforms and Material 3 on Android. Keep each surface to its own foundation, and map shared brand tokens onto each foundation's roles.
12. Define every token and component of a product's own system in `DESIGN.md` before implementation. Take research findings from Sections 2 and 3, never visual components from another system.

## 5. Reject slop practices

A **slop practice** is a design or code habit that recurs across generated interfaces, templates, or popular posts without a source in Sections 2 to 4 or the brief.

1. Trace every design and implementation rule to the brief, the selected foundation, or a source in Sections 2 and 3. Drop any rule that traces to none of them.
2. Prefer research-backed sources over articles, social media posts, template galleries, and generated examples.
3. Confirm each platform feature with Modern Web Guidance, Baseline, or MDN before applying it. Never rely on recalled browser support.
4. Check the generic traits listed in `interface-design` Section 7 against the design plan before building.
5. Run `impeccable detect --json <markup files or directories>` on the built markup. Resolve every finding, or record in `DESIGN.md` the brief requirement that justifies it.
6. Replace each practice in the table below with the governing practice.

| Slop practice | Governing practice | Source |
| :--- | :--- | :--- |
| Placeholder text as the only field label | A visible label tied to the field | WCAG 2.2 SC 3.3.2; GOV.UK Design System |
| A `div` or `span` with a click handler | A `button` or `a` element | HTML Living Standard; APG |
| ARIA roles added to native elements by default | Native semantics first; ARIA only for patterns HTML lacks | APG |
| Zoom disabled through the viewport meta tag | Zoom allowed | WCAG 2.2 SC 1.4.4 |
| A toast as the only error message | An inline error linked to the field, plus an error summary for forms | WCAG 2.2 SC 3.3.1; GOV.UK Design System |
| Icon-only controls without an accessible name | A visible label or an accessible name | WCAG 2.2 SC 4.1.2 |
| Muted text on a colored or tinted surface below contrast | Text that meets the contrast minimum | WCAG 2.2 SC 1.4.3 |
| Lazy loading the largest above-the-fold image | Eager loading with high fetch priority for the LCP image | Core Web Vitals; Modern Web Guidance |
| A custom select, dialog, or tooltip built from scratch | The native element or the Modern Web Guidance pattern with its fallback | Modern Web Guidance; APG |
| Motion on every section and card | Motion that answers a user action, honoring reduced motion | WCAG 2.2 SC 2.3.3; selected foundation |
| One default typeface, gradient accents, cards inside cards, and an eyebrow label above every heading | Choices taken from the brief and the selected foundation | Impeccable detector rules; `interface-design` Section 7 |

| Resource | Use | Source |
| :--- | :--- | :--- |
| Impeccable | Deterministic detector for generic generated-interface patterns; heuristic critique and audit commands | https://github.com/pbakaus/impeccable |
| Anthropic frontend-design skill | Calibration list of traits that generated designs cluster around | https://github.com/anthropics/skills/tree/main/skills/frontend-design |
| Nielsen Norman Group | Usability research and heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| Baymard Institute | E-commerce and form usability research | https://baymard.com/research |
| GOV.UK Design System | Research-backed patterns for forms, errors, and questions | https://design-system.service.gov.uk/ |
| Inclusive Components | Accessible component construction | https://inclusive-components.design/ |
| Every Layout | Intrinsic CSS layout primitives | https://every-layout.dev/ |
