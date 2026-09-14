# Tasks — official-skills-reconciliation

**State:** DONE
**Last updated:** 2026-09-14

## Phase 0: Retrieve official skill snapshots
- [x] Clone `anthropics/skills` @ `34040c9` (2026-09-10), vendor full `skills/`, `spec/`, `template/`, README, notices into `sources/upstream/anthropic-skills/` + PROVENANCE.md
- [x] Clone `google/skills` @ `150f8525` (2026-09-11), vendor full `skills/`, `plugins/`, index/README/LICENSE into `sources/upstream/google-skills/` + PROVENANCE.md
- [x] Investigate `openai/skills` (deprecated) → `openai/plugins`; vendor only OpenAI's own `plugin-creator` skill + README into `sources/upstream/openai-plugins/` + PROVENANCE.md (536-skill third-party marketplace intentionally not bulk-vendored)
- [x] Add `sources/upstream/.gitignore` so none of this is ever committed
- [x] Clean up scratch clones from `/tmp`

## Phase 1: Harden AGENTS.md
- [x] Add "Verification Discipline" section
- [x] Add "Deliverable Hygiene" section
- [x] Append precedence clarification (max-strength within tier 3, still subordinate to tier 1 + live user)
- [x] Note rule-19-vs-commit-attribution scope distinction (folded into Deliverable Hygiene's closing bullet)

## Phase 2: Fill documentation/legalese gaps from RULES.md
- [x] `documentation/SKILL.md`: No Compliance Self-Narration
- [x] `documentation/SKILL.md`: Verify Before Writing
- [x] `documentation/SKILL.md`: No Hedging or Approximation in Delivered Text
- [x] `documentation/SKILL.md`: register-by-document-type table
- [x] `documentation/SKILL.md`: internal-vs-external communication default/gate (extended "Memo / correspondence" bullet)
- [x] `documentation/SKILL.md` + `internal-comms/SKILL.md`: cross-reference gate added to both
- [x] `documentation/SKILL.md`: extend Final Pass checklist (items 12-16: authority-context leakage, self-status/progress narration, hedges/approximation, metadata restraint, rendered-artifact check)
- [x] `legalese/SKILL.md`: "User-supplied wording is locked" (Doctrine 9)
- [x] `legalese/SKILL.md`: "Tier is a floor, not a ceiling" + severability incident example (Doctrine 1)
- [x] `legalese/SKILL.md`: Doctrine 3 worked example (litigant-rights scenario)

## Added (this session, mid-conversation): pagination/layout convention
- [x] New `documentation/references/letterhead-and-pagination.md` — header/footer spacing (0.5" default), table page-break minimum (heading + 2 rows, repeat heading on continuation), image page-break + oversized-image scale-down fallback, letterhead reduction on continuation pages, front-matter/body roman→Arabic numbering (cover silently unshown, substantive-break page shown), space-efficiency/no-dead-gaps, never-hand-patch-generated-output
- [x] Verified the numbering model against a real instrument: ANCEM Constitution (`GVTM-FGD-8A43`) — screenshotted pages 1/2/5 to confirm, also surfaced a live defect (stray unrendered `#` on the Article 1 page) as evidence for why rendered-page visual inspection matters
- [x] `documentation/SKILL.md`: added "Pagination and Physical Layout" pointer section
- [x] `legalese/SKILL.md`: added "Physical Instrument Layout" pointer section
- [x] Add artifact-specific verification procedures to `docx`, `pdf`, `pptx`, and `xlsx`
- [x] Place proposal/CFP narrative conventions in the documentation references and PBO-only formatting in the PBO-specific reference

## Phase 3: Reconcile against vendored official skills
- [x] Diff `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`, `internal-comms`, `webapp-testing`, `frontend-design` against Anthropic vendor copies
- [x] Note candidate patterns from `openai-plugins/plugin-creator` vs. this repo's `skill-creator` — finding: not comparable (plugin-creator is Codex-marketplace/`.codex-plugin` packaging, not skill-authoring methodology); no merge
- [x] Note candidate patterns from `anthropic-skills/mcp-builder` vs. this repo's `graphify` — finding: not comparable (mcp-builder = building a new MCP server; graphify = using two already-built MCP tools for codebase graphs); no merge, but mcp-builder flagged as a good net-new adoption if the user ever needs to build a custom MCP server
- [x] Present merge/adopt/skip recommendations per skill for sign-off before any rename/merge/delete
- [x] Execute user-approved low-risk items: adopted upstream `frontend-design/SKILL.md` body (kept this repo's more trigger-rich description)
- [x] `docx`/`pdf`/`pptx`/`xlsx` reconciliation — executed at user's explicit direction while license review is pending with Anthropic ("update and merge, just don't commit"); working-tree only, see walkthrough for exactly what changed and why nothing was blindly copied wholesale from the vendor snapshot
- [x] Adopted `discernment-nudge` (unmodified, Apache-2.0) and `mcp-builder` (Apache-2.0, fixed one stale hardcoded model reference in `evaluation.py`/`evaluation.md`) as new skill folders
- [x] Adopted `doc-coauthoring` — rewritten before insertion: removed the "link this conversation in an appendix" tip (violated Documentation Source Boundary + AI-attribution policy) and de-vendor-locked Claude/claude.ai-specific mechanics to host-agnostic language, matching the treatment already given to `skill-creator`
- [x] Evaluated remaining Anthropic skills against the three focus areas (agentic coding independent of Claude, agentic legal writing, agentic document/report creation) — not adopted: `claude-api`/`academy-guide` (Claude-dependent, already separately available), `web-artifacts-builder` (claude.ai-specific artifact system), `algorithmic-art`/`canvas-design`/`theme-factory`/`slack-gif-creator` (creative/consumer, off-focus), `brand-guidelines` (applies Anthropic's own corporate brand specifically, not a generic client-brand template)
- [x] Google/OpenAI vendor snapshots — user's call, my judgment: don't adopt any skill folders from either (Google's 142 skills are GCP/Workspace product-API guides; OpenAI's `plugin-creator` is Codex-marketplace packaging) — kept vendored for reference only
- [x] `pptx` vs `pptx-master`: resolved by removal, not boundary-clarification — see below

## Added: rule 19 (no AI attribution), rule 15 (NGO narrative), rule 24 sharpening
- [x] `AGENTS.md` Deliverable Hygiene: explicit no-AI-attribution rule + limit (can't suppress a coding tool's own fixed platform convention)
- [x] `ci-cd/SKILL.md` Commit Hygiene Expectations: same rule, commit/PR-specific form
- [x] `documentation/SKILL.md`: strengthened general prose-over-bullets Structure rule for narrative documents + cross-reference
- [x] New `documentation/references/ngo-and-donor-narrative.md`: full narrative/citation/tone guide (rule 15, de-PBO'd; rule 16's specific pt-size/color table deliberately left out — donor template wins, no universal default asserted)
- [x] `AGENTS.md` Verification Discipline: added exact-artifact-over-report validation rule (rule 24 sharpened)

## Added: skill-set restructuring (user directive)
- [x] `internal-comms/` renamed to `communications/`: broadened description, added an "External Communications (default)" section (full-title references, attach/cite not bare-link, formal tone, pointer to letterhead-and-pagination.md) alongside the existing "Internal Communications (confirmed audience only)" section; `documentation/SKILL.md`'s Memo/correspondence bullet now points here instead of duplicating the gate logic
- [x] `pptx-master/` deleted entirely (97 MB) per explicit instruction ("ppt master dies")
- [x] `README.md` active-skills list updated: `communications` (renamed), `doc-coauthoring`/`mcp-builder`/`discernment-nudge` (new), `pptx-master` removed, `legalese`/`graphify`/`maestro`/`bootstrap`/`system-init`/`system-design`/`ssh` added (were missing from the list even though they existed)
- [x] `ci-cd` supremacy for git/commit conventions — acknowledged; no current conflict existed to resolve, applying going forward
- [x] `technical-diagrams` (Draw.io/mxGraph) assessed against vendor snapshots for a superior alternative — none found; Anthropic/Google/OpenAI have no dedicated architecture-diagram skill to compare against. Current skill already has render-backed visual QA, non-circumvention rules, and a full bundled-resource set (palettes, style tokens, geometry, templates, render/install scripts). Assessed at the `SKILL.md` level only — the 7 `references/*.md` files were not individually audited; offered as a follow-up, not done

## Phase 4: Ship
- [x] Apply the memory admission test; do not duplicate rules already explicit in `AGENTS.md`, skills, or references
- [x] Leave bootstrap propagation, commits, and pushes untouched because the user did not authorize them
- [x] Finalize the walkthrough and keep the `DONE` session active until a new task triggers archival

## Added: governance and full skill remediation
- [x] Remove Anthropic, Google, and OpenAI snapshots from `sources/upstream/`
- [x] Read the original implementation plan, task register, and walkthrough
- [x] Read the PBO root `RULES.md` in full
- [x] Update the skill-authoring standard and compact `AGENTS.md`
- [x] Audit and remediate `skill-creator`
- [x] Audit and remediate `documentation`
- [x] Audit and remediate `bootstrap`
- [x] Audit and remediate `ci-cd`
- [x] Audit and remediate `communications`
- [x] Audit and remediate `discernment-nudge`
- [x] Audit and remediate `doc-coauthoring`
- [x] Audit and remediate `docx`
- [x] Audit and remediate `frontend-design`
- [x] Audit and remediate `graphify`
- [x] Audit and remediate `legalese`
- [x] Audit and remediate `maestro`
- [x] Audit and remediate `mcp-builder`
- [x] Audit and remediate `pdf`
- [x] Audit and remediate `pptx`
- [x] Audit and remediate `ssh`
- [x] Audit and remediate `system-design`
- [x] Audit and remediate `system-init`
- [x] Audit and remediate `technical-diagrams`
- [x] Audit and remediate `webapp-testing`
- [x] Audit and remediate `xlsx`
- [x] Build and verify the 24-rule disposition register
- [x] Remove the migrated PBO root `RULES.md`
- [x] Run repository-wide structural, prose, and link validation
- [x] Re-read every changed instruction file and finalize the walkthrough
