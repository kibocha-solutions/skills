# Implementation Plan: Universal Rules Deduplication, PBO Integration & Compliance Checklists

## Objective
Clean and deduplicate `AGENTS.md` (removing doubled headers and repeated section 1 declarations), integrate universal rules extracted from `kibocha-solutions/PBOs/RULES.md` (specifically enshrining the Universal Non-Code Full-Read Mandate), route domain rules to governing skills, and equip all applicable skills and `AGENTS.md` with explicit pre-completion verification checklists.

## Acceptance Criteria
1. `AGENTS.md` is deduplicated: duplicate `# Universal Agent Rules` and doubled Section 1 declarations are eliminated; total word count is strictly under 1,500 words.
2. The **Universal Non-Code Full-Read Mandate** is explicitly integrated into `AGENTS.md`: if an artifact/document being touched is non-code (with markdown `.md` files explicitly declared as non-code), the agent MUST read it in full; grep/search cannot substitute.
3. Core universal PBO rules (external reader orientation, no uncertainty markers or approximation words, no cosmetic compliance, memory continuity, exact artifact hash validation) are codified in `AGENTS.md`.
4. Domain-specific rules from PBOs are routed into `documentation`, `legalese`, `communications`, and format skills (`pdf`, `docx`).
5. An explicit, unambiguous pre-completion checklist is appended to `AGENTS.md` and to each governing skill.

## Proposed Changes
### Components & Files
* `[MODIFY]` `AGENTS.md`: Deduplicate header blocks, integrate universal PBO rules and non-code reading mandate, append pre-completion compliance checklist.
* `[MODIFY]` `documentation/SKILL.md` & references: Integrate rules on operative vs rationale separation, proposal register/citations, and formatting standards; add pre-completion checklist.
* `[MODIFY]` `legalese/SKILL.md`: Integrate register floor rule (Sovereign tier is a floor) and command-only clause discipline; add checklist.
* `[MODIFY]` `communications/SKILL.md`: Integrate correspondence register and external reader boundary; add checklist.
* `[MODIFY]` `pdf/SKILL.md`, `docx/SKILL.md`, `pptx/SKILL.md`, `xlsx/SKILL.md`: Integrate page-flow, layout integrity, and SHA-256 validation rules.

## Verification Method
1. Word count verification on `AGENTS.md` (`wc -w < 1500`).
2. Verify removal of duplicate headers and sections.
3. Verify presence of explicit non-code full read mandate covering `.md` files.
4. Verify pre-completion checklists in `AGENTS.md` and skills.
