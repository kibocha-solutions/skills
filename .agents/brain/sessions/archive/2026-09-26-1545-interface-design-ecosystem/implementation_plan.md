# Implementation Plan: Interface Design & Engineering Ecosystem

## Objective
Establish a legendary, multi-agent Interface Design & Engineering Ecosystem by:
1. Creating the master entry skill `interface-design` (strategy, brief, taste calibration, token contract `DESIGN.md`, Apple HIG vs Material 3 Expressive, anti-slop rules, multi-agent pre-configured MCP onboarding).
2. Refactoring `frontend-design` to `web-design` (production web implementation, semantic HTML, CSS custom properties, container queries, fluid typography, WCAG 2.2 AA, Emil Kowalski spring motion, Rauno Freiberg invisible details).
3. Creating `mobile-app-design` (mobile & tablet applications across phones and tablets in both portrait and landscape orientations, safe areas, thumb zones, gesture ergonomics, touch targets).
4. Ensuring clean alignment across Claude Code, Codex, Gemini, and Copilot.

## Acceptance Criteria
1. `interface-design/SKILL.md` exists, conforms to YAML frontmatter rules, stays under 500 lines, uses imperative voice, and links to all references.
2. `interface-design/references/design-systems-hig-and-material3.md` exists with official links and standards for Apple HIG and Material 3 Expressive.
3. `interface-design/references/taste-and-aesthetic-archetypes.md` exists with Taste dials (density/variance 1-10) and deterministic anti-slop rules.
4. `interface-design/references/multi-agent-mcp-setup.md` exists with automated configuration flows for Claude, Codex, Gemini, and Copilot.
5. `web-design/SKILL.md` exists (refactored from `frontend-design`), stays under 500 lines, and covers modern CSS, fluid type, and web accessibility.
6. `web-design/references/emil-kowalski-interaction-and-motion.md` exists with frequency brackets, spring physics, and origin-aware transforms.
7. `web-design/references/modern-css-and-tokens.md` exists with CSS custom properties and container queries.
8. `web-design/examples/good-vs-bad-web-patterns.md` exists with contrasting accessible patterns.
9. `mobile-app-design/SKILL.md` exists, stays under 500 lines, and covers phone and tablet ergonomics in both portrait and landscape.
10. `mobile-app-design/examples/touch-and-mobile-gestures.md` exists with concrete touch gesture and sheet patterns.
11. `frontend-design/` is cleanly removed/refactored.
12. `README.md` and repository memory are updated to reflect the new skills.
13. Zero U+2014 em dashes across all files.
14. Zero AI attribution across all files and git history.

## Proposed Changes

### 1. `interface-design`
- [NEW] `interface-design/SKILL.md`
- [NEW] `interface-design/references/design-systems-hig-and-material3.md`
- [NEW] `interface-design/references/taste-and-aesthetic-archetypes.md`
- [NEW] `interface-design/references/multi-agent-mcp-setup.md`
- [NEW] `interface-design/LICENSE.txt`

### 2. `web-design`
- [DELETE] `frontend-design/`
- [NEW] `web-design/SKILL.md`
- [NEW] `web-design/references/emil-kowalski-interaction-and-motion.md`
- [NEW] `web-design/references/modern-css-and-tokens.md`
- [NEW] `web-design/examples/good-vs-bad-web-patterns.md`
- [NEW] `web-design/LICENSE.txt`

### 3. `mobile-app-design`
- [NEW] `mobile-app-design/SKILL.md`
- [NEW] `mobile-app-design/references/mobile-and-tablet-ergonomics.md`
- [NEW] `mobile-app-design/examples/touch-and-mobile-gestures.md`
- [NEW] `mobile-app-design/LICENSE.txt`

### 4. Repository Alignment
- [MODIFY] `README.md`
- [MODIFY] `.agents/MEMORY.md`

## Verification Methods
- Automated checks: line counts (<500 lines for all SKILL.md), no em dashes, no AI attribution, link resolution.
- CI/CD checkpoints after logical phases using single-scope 72-word commits.
