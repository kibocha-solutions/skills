# Tasks: Interface Design & Engineering Ecosystem

STATE: IN_PROGRESS

## Phase 1: Master Entry Skill (`interface-design`)
- [x] Create `interface-design/SKILL.md` with entry workflow, brief definition, Taste dials, HIG/M3 selection, anti-slop rules, and routing
- [x] Create `interface-design/references/design-systems-hig-and-material3.md` with Apple HIG and Google Material 3 Expressive guidelines and official URLs
- [x] Create `interface-design/references/taste-and-aesthetic-archetypes.md` with density/variance dials and anti-slop catalog
- [x] Create `interface-design/references/multi-agent-mcp-setup.md` with autonomous setup instructions for Claude, Codex, Gemini, and Copilot
- [x] Create `interface-design/LICENSE.txt`
- [x] Run compliance checks for `interface-design` (lines <500, no em dashes, no AI attribution)

## Phase 2: Refactor `frontend-design` to `web-design`
- [x] Refactor and create `web-design/SKILL.md` (web and responsive web apps, container queries, fluid type, WCAG 2.2 AA)
- [x] Create `web-design/references/emil-kowalski-interaction-and-motion.md` with frequency brackets, spring physics, and origin-aware transforms
- [x] Create `web-design/references/modern-css-and-tokens.md` with CSS custom properties and container queries
- [x] Create `web-design/examples/good-vs-bad-web-patterns.md` with contrasting accessible components
- [x] Create `web-design/LICENSE.txt`
- [x] Remove deprecated `frontend-design/` directory
- [x] Run compliance checks for `web-design` (lines <500, no em dashes, no AI attribution)

## Phase 3: Mobile & Tablet App Skill (`mobile-app-design`)
- [x] Create `mobile-app-design/SKILL.md` with mobile and tablet ergonomics across portrait and landscape orientations
- [x] Create `mobile-app-design/references/mobile-and-tablet-ergonomics.md` with touch targets, thumb zones, split views, and orientation rules
- [x] Create `mobile-app-design/examples/touch-and-mobile-gestures.md` with pull-to-refresh, bottom sheets, swipe gestures, and master-detail layouts
- [x] Create `mobile-app-design/LICENSE.txt`
- [x] Run compliance checks for `mobile-app-design` (lines <500, no em dashes, no AI attribution)

## Phase 4: Repository Alignment & Documentation
- [x] Update `README.md` with the new skill architecture
- [x] Update `.agents/MEMORY.md` with the interface design ecosystem documentation
- [x] Run cross-repository checks across `.agents/brain/git/` and verify git params

## Phase 5: Verification & Checkpoint Commit
- [x] Verify zero U+2014 em dashes across all files in repository
- [x] Verify zero AI attribution across all files in repository
- [x] Verify all markdown links resolve correctly
- [x] Record walkthrough in `walkthrough.md`
- [x] Save checkpoint commit using `ci-cd` standards (single-scope, imperative title, <= 72 words body)
- [/] Request user permission to execute `bootstrap`
