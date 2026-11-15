# Skill Depth & Example Gap Analysis

## 1. The Quality Gap
User Feedback:
> *"even those that have them are shallow, ie. the content is brief, presumptive and lacks the clear directive or samples or instructions needed for an agent to act confidently. I am not asking for fluff; I am asking for clear directives the agent can follow step by step to reach the goal. all background or detail goes to the overview/background/whatever name you give (in the reference/examples), then the rest of the document is step by step commands or good vs bad samples."*

## 2. Standardized Architecture per Skill
Per `/skill-creator` and `/documentation`:
1. **`SKILL.md` (Execution Core)**:
   - YAML frontmatter with exact triggers and capabilities.
   - Body contains strictly step-by-step, ordered imperative commands.
   - Explicit links to `references/` for specifications and `examples/` for sample patterns.
   - Mandatory verification checklist before declaring completion.
   - Strictly below 500 lines, zero conversational filler or rationale, no em dashes.
2. **`references/` (Operating Specs & Background)**:
   - Background theory, design philosophies, schema specifications, parameter tables, and edge-case protocols.
   - Table of contents if over 300 lines.
3. **`examples/` (Actionable Good vs Bad Patterns)**:
   - Contrasting, concrete code/prose/data snippets.
   - Shows *Wrong* (the failure mode/anti-pattern) vs *Right* (the compliant, production-grade output).

---

## 3. Skill Remediation Targets by Domain

### Group A: Process & Orchestration
* `maestro`: Session recovery, goal decomposition, threshold checks (missing `examples/`).
* `bootstrap`: Multi-agent alignment commands, collision handling, hook validation (missing `examples/`).
* `skill-creator`: Benchmark authoring, eval loop running, packaging (missing `examples/`).
* `system-design`: Boundary contracts, ERD normalization, state sequences (missing `examples/`).
* `system-init`: Dependency triage, sudoers boundary, partition storage (missing `examples/`).
* `ssh`: Bastion configuration, agent forwarding, SSH Git signing (missing `examples/`).

### Group B: Document & Media Production
* `docx`: Layout margins, tables, styles, pagination (missing `examples/` and `references/`).
* `pdf`: Form filling, OCR, annotations, cryptographic verification (missing `examples/` and `references/`).
* `pptx`: Slide typography, layout grids, graphic components (missing `examples/` and `references/`).
* `xlsx`: Financial modeling, cell formatting, recalc scripts (missing `examples/` and `references/`).
* `doc-coauthoring`: Interview protocols, structured drafts (missing `examples/` and `references/`).

### Group C: Web, UI & Communications
* `mcp-builder`: Server implementations, transport debugging (missing `examples/` and `references/`).
* `frontend-design`: Responsive tokens, UI components, interaction design (missing `examples/` and `references/`).
* `webapp-testing`: Playwright test scripts, selector strategies (missing `references/`).
* `communications`: Corporate/donor/regulator correspondence (missing `references/`).
* `discernment-nudge`: Reflection query sets (missing `examples/` and `references/`).
