# Implementation Plan: Skills Deepening, References & Good vs Bad Examples

## Objective
Systematically deepen all skills in the repository according to `/documentation` and `/skill-creator` standards. Replace shallow/presumptive instructions with clear step-by-step procedural directives in `SKILL.md`, move all background and deep specifications to `references/`, and equip every skill with rich `examples/` contrasting good vs bad implementations.

## Acceptance Criteria
1. Every `SKILL.md` is strictly under 500 lines, uses execution-ordered imperative commands, contains no conversational fluff or em dashes, and links directly to relevant references/examples at the affected step.
2. Every skill contains an `examples/` directory featuring concrete, realistic positive and negative ("good vs bad") samples.
3. Complex domain mechanics, tables, and schemas are extracted into focused files under `references/`.
4. Every skill ends with an unambiguous, verifiable pre-completion checklist.

## Proposed Changes
### Group A: Orchestration & Infrastructure Skills
- `[MODIFY]` `maestro/`: Add `examples/` (session initiation, blocker recovery, threshold triggers).
- `[MODIFY]` `bootstrap/`: Add `examples/` (multi-host run, sparse checkout conflict resolution).
- `[MODIFY]` `skill-creator/`: Add `examples/` (eval-viewer generation, trigger optimization).
- `[MODIFY]` `system-design/`: Add `examples/` (clean vs leaky architectural boundaries, ERDs).
- `[MODIFY]` `system-init/`: Add `examples/` (workstation audits, safe dependency resolution).
- `[MODIFY]` `ssh/`: Add `examples/` (SSH signing setup, bastion tunneling).

### Group B: Document & Media Skills
- `[MODIFY]` `docx/`: Create `references/` (table formatting, styles) and `examples/` (clean reports).
- `[MODIFY]` `pdf/`: Create `references/` (AcroForms, OCR) and `examples/` (field extraction).
- `[MODIFY]` `pptx/`: Create `references/` (slide typography, master themes) and `examples/`.
- `[MODIFY]` `xlsx/`: Create `references/` (financial formulas, recalcs) and `examples/`.
- `[MODIFY]` `doc-coauthoring/`: Create `references/` and `examples/` (PRD interview passes).

### Group C: Web, UI & Communication Skills
- `[MODIFY]` `mcp-builder/`: Create `references/` (STDIO/SSE transports) and `examples/` (server templates).
- `[MODIFY]` `frontend-design/`: Create `references/` (typography, CSS tokens) and `examples/` (component diffs).
- `[MODIFY]` `webapp-testing/`: Create `references/` (Playwright locators, assertions) and `examples/`.
- `[MODIFY]` `communications/`: Create `references/` (executive/donor registers) and `examples/`.
- `[MODIFY]` `discernment-nudge/`: Create `references/` and `examples/` (reflection sets).

## Verification Plan
1. Automated inspection of file structure: confirm every skill directory has `SKILL.md`, `references/`, and `examples/`.
2. Static line-count checks (`wc -l < 500` for all `SKILL.md` files).
3. Validate that every reference and example is actively linked from `SKILL.md`.
