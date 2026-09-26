---
name: interface-design
description: Design legendary, production-grade user interfaces, design systems, visual languages, and interactive blueprints for websites, responsive web applications, and mobile apps across phones and tablets in both portrait and landscape orientations. Use for interface design, UI/UX, product design, website design, mobile app design, design systems, design tokens, layout wireframes, Apple HIG, Material 3 Expressive, taste calibration, anti-slop rules, and Figma MCP extraction.
license: Complete terms in LICENSE.txt
---

# Interface Design

## 1. Establish the brief and platform target

1. Identify the subject, product, target audience, primary user tasks, brand constraints, and delivery targets.
2. Determine the target platform and form factor:
   - Website or responsive web application (desktop, tablet, mobile web).
   - Native or hybrid mobile application (iOS, Android, PWA, React Native, Flutter).
3. Determine supported orientations:
   - Portrait (standard vertical ergonomics).
   - Landscape (compact vertical constraint for phones; split-view multi-column for tablets).
4. Propose one concrete subject and target audience when the brief omits them.
5. Confirm any assumption that would materially alter the design.
6. Gather real content or write realistic domain-specific copy.

## 2. Check and initialize multi-agent MCP tooling

Read [multi-agent MCP setup](references/multi-agent-mcp-setup.md) to inspect, configure, and authenticate tooling across Claude Code, Codex CLI, Gemini Antigravity, and GitHub Copilot.

1. Check if the task requires extracting Figma designs or running visual/accessibility browser verification.
2. Inspect the active agent host configuration file for registered MCP servers:
   - Claude Code: `~/.claude/settings.json`
   - Codex CLI: `~/.codex/config.toml`
   - Gemini Antigravity: `~/.gemini/antigravity/mcp_config.json`
   - Gemini CLI: `~/.gemini/settings.json`
   - GitHub Copilot: VS Code User settings or `~/.copilot/` config
3. Check for the `figma` MCP server when Figma links or assets are supplied:
   - If missing, autonomously write the server configuration into the active host's configuration file.
   - Pause execution and guide the user through the authentication step by requesting their Figma Personal Access Token.
   - Store the provided token in the environment configuration and verify connectivity before continuing.
4. Check for the `playwright` MCP server when browser verification is required:
   - If missing, autonomously register the `@playwright/mcp@latest` server in the active host's configuration.
   - Verify that Playwright browser runtimes are available.
5. Extract frame nodes, component variants, text styles, and color variables via Figma MCP when connected.

## 3. Calibrate taste dials and style archetypes

Read [taste and aesthetic archetypes](references/taste-and-aesthetic-archetypes.md) for calibration scales and archetype specifications.

1. Set the **Density Dial** from 1 to 10 based on information throughput:
   - Low density (1 to 3): Consumer marketing, portfolios, onboarding flows.
   - Balanced density (4 to 6): Standard SaaS applications, settings, documentation.
   - High density (7 to 10): Financial workstations, analytics dashboards, developer tools.
2. Set the **Variance Dial** from 1 to 10 based on structural distinctiveness:
   - Low variance (1 to 3): Standard modular grid, predictable form hierarchy.
   - Medium variance (4 to 6): Distinctive grid rhythms, asymmetric hero regions.
   - High variance (7 to 10): Editorial typography, dynamic split viewpoints.
3. Select one primary style archetype:
   - Clean Functional (modern SaaS, crisp borders, neutral surfaces, deliberate focus).
   - Refined Editorial (serif display type, generous leading, structured rules).
   - Dense Utility (monospace data tables, minimal padding, visible dividers).
   - Soft Tactile (gentle inner shadows, pill geometry, tactile spring response).
   - Bold Contemporary (vibrant accents, high-contrast type, expressive geometry).
4. Restrain all secondary elements around the primary focal anchor.

## 4. Select the platform design system

Read [design systems HIG and Material 3](references/design-systems-hig-and-material3.md) for component anatomy, official URLs, and platform selection matrices.

1. Choose the authoritative design foundation:
   - **Apple Human Interface Guidelines (HIG)**: For iOS and iPadOS applications. Enforce 44x44pt minimum touch targets, San Francisco typography, vibrancy materials, and standard navigation controllers.
   - **Google Material 3 Expressive**: For Android applications. Enforce 48x48dp minimum touch targets, dynamic color tonal palettes, 35+ expressive shape corners, and container transforms.
   - **Modern Web Synthesis**: For responsive cross-platform web applications. Combine Apple's typographic restraint and touch ergonomics with Material 3's semantic container token hierarchy.
2. Inspect the official design guideline documentation for each requested component type:
   - Apple HIG: `https://developer.apple.com/design/human-interface-guidelines/`
   - Material 3 Components: `https://m3.material.io/components/`

## 5. Formulate the token contract

1. Create a project-local `DESIGN.md` file defining all design tokens before implementation.
2. Define semantic color roles:
   - `surface-primary`, `surface-secondary`, `surface-elevated`
   - `content-primary`, `content-secondary`, `content-muted`
   - `accent-default`, `accent-hover`, `accent-subtle`
   - `feedback-error`, `feedback-warning`, `feedback-success`, `feedback-info`
3. Define the typographic scale:
   - Restrict the design to at most two font families.
   - Set modular line heights (minimum 1.5 for body text).
   - Limit body line length to 65 to 75 characters.
4. Define spacing tokens on a strict 4px or 8px baseline grid (4, 8, 12, 16, 24, 32, 48, 64px).
5. Define container elevation, borders, and motion tokens.

## 6. Plan layout and ergonomic geometry

1. Apply the nested border radius formula to all nested elements:
   $$\text{Radius}_{\text{inner}} = \max(0, \text{Radius}_{\text{outer}} - \text{Padding})$$
   Never use identical radius on an outer container and an inner child.
2. Plan mobile and tablet ergonomics based on orientation:
   - **Phone Portrait**: Keep primary actions in the thumb reach zone (lower 40% of viewport). Use sticky bottom action bars and expandable bottom sheets. Respect `env(safe-area-inset-bottom)`.
   - **Phone Landscape**: Handle severe vertical height constraints (<450px). Replace stacked rows with side-by-side fields. Collapse top app bars into compact side navigation rails.
   - **Tablet Portrait**: Use a 2-column adaptive layout. Restrict line lengths to avoid unreadable edge-to-edge text. Position touch controls along lateral margins.
   - **Tablet Landscape**: Use a master-detail dual-pane architecture with a persistent left sidebar. Support dual touch targets (44pt) and mouse hover states.
3. Draw an ASCII wireframe when comparing layout alternatives.

## 7. Reject unearned defaults

Do not select any of these generic tropes without explicit support from the brief:

- Terracotta, cream, and high-contrast serif palette.
- Near-black surface paired automatically with one acid accent.
- Broadsheet layout with hairline rules used as default decoration.
- Identical rounded cards with uniform floating drop shadows.
- Gradient washes applied purely as decorative background filler.
- All-caps eyebrow labels placed above every single section heading.
- Single-word colored accenting inside headlines.
- Middle-dot (`·`) metadata chains used without semantic hierarchy.
- Automatic right arrows (`→`) appended to every button and link.
- Hover zoom animations applied to every card container.

1. Compare proposed wireframes and tokens against this exclusion list.
2. Replace any choice that cannot be justified by the brief or brand constraints.
3. Record confirmed choices in `DESIGN.md`.

## 8. Write interface content and copy

1. Use plain, direct language in active voice.
2. Use sentence case for headings, labels, and buttons.
3. Write button labels as the concrete action executed upon click or tap.
4. State error conditions precisely and provide the exact recovery step.
5. Equip empty states with one clear forward-moving action.
6. Remove filler words, marketing puffery, and placeholder text.

## 9. Route to implementation

Route the confirmed `DESIGN.md` contract to the matching implementation skill:
1. **Websites and Responsive Web Apps**: Route to `web-design` for semantic HTML, CSS custom properties, container queries, fluid typography, and web accessibility.
2. **Mobile and Tablet Applications**: Route to `mobile-app-design` for native/hybrid shells, touch gestures, safe area handling, and dual-orientation adaptations.
3. For design-only tasks, deliver `DESIGN.md`, component specifications, and wireframe blueprints directly.

## 10. Pre-completion checklist

Before delivering any interface design specification or routing to implementation, confirm evidence exists for each item:

- [ ] Brief and form factor identified, including phone/tablet portrait and landscape requirements.
- [ ] Active agent host detected and required MCPs inspected/pre-configured.
- [ ] Taste dials (density and variance) calibrated and archetype selected.
- [ ] Platform foundation chosen (Apple HIG, Material 3, or Web Synthesis) with component URLs referenced.
- [ ] Project token contract written to `DESIGN.md`.
- [ ] Nested border radius formula applied to all nested containers.
- [ ] All items on the anti-slop exclusion list checked and rejected.
- [ ] Zero AI attribution across all specifications, documentation, and metadata.
- [ ] No U+2014 em dashes in any file or deliverable.
