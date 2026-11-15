# PBO Standing Rules Extraction & Categorization Matrix

Source: `kibocha-solutions/PBOs/RULES.md` (Commit `13851685a58c96b8b7d6b9c245ce5e863d3b6967`)

---

## 1. Global Rules (Target: `AGENTS.md`)

These rules are cross-cutting, domain-independent constraints governing all tasks and repositories:

1. **Universal Non-Code Full-Read Mandate (Rules 21 & Explicit User Directive)**:
   - If the artifact, instrument, or document being touched is **NOT CODE** (markdown `.md` files are explicitly excluded from code, meaning `.md` files ARE non-code), the agent **MUST READ that document in full from start to finish**.
   - The agent cannot rely on `grep`, `search_web`, or ripgrep passages as a substitute for full reading. Search locates passages; only a complete read catches structural contradictions, hedges, and context errors.
2. **Process, Memory & Continuity (Rules 1 & 2)**:
   - Sweep memory stores (`.agents/MEMORY.md` and `.agents/memory/`) before acting.
   - Deliberate memory duplication across stores is an intentional hedge; agents must never prune or deduplicate mandated memory files.
3. **Disclosure, Confidentiality & Economy of Disclosure (Rules 3 & 5)**:
   - Withhold sensitive identifiers (registration numbers, certificate PINs, banking info, internal governance deliberations) by default unless explicitly commanded by the user or an authoritative form field.
   - Economy of disclosure: Do not leak background conversational facts into reader-facing deliverables.
4. **Context vs. Content & Reader Boundary (Rule 4)**:
   - Never cite internal workspace paths, temporary files, sessions, handoffs, plans, chat history, or filenames in external deliverables. Refer to documents by title only.
5. **No Compliance or Status Self-Narration (Rules 7 & 8)**:
   - Never narrate compliance ("done to comply with X") inside deliverable prose.
   - Never report drafting status ("draft", "WIP", "pending board ratification", "next steps") inside deliverable bodies.
6. **Sentence-Level Economy & Anti-Filler (Rule 10)**:
   - Every sentence must do work: narrow, instruct, constrain, verify, warn, or connect. Eliminate intern-defense filler.
7. **No Cosmetic Compliance (Rule 12)**:
   - Removing flagged patterns means restructuring sentences, not swapping tokens (e.g. changing em dashes to semicolons while keeping the construction).
8. **Verify Facts & Mark Unresolved (Rule 17)**:
   - Verify external facts against primary sources. Mark unresolved facts in working notes/chat instead of guessing.
9. **User-Supplied Wording is Locked (Rule 18)**:
   - Never silently substitute user-supplied or locked wording. Propose changes first.
10. **Absolute AI-Attribution Prohibition (Rule 19)**:
    - Never attribute work to AI, models, or automated agents anywhere in work products, commits, or metadata.
11. **External Reader Focus & No Uncertainty Markers (Rule 20)**:
    - Deliverables are for external readers: never include uncertainty markers (`[estimate]`, "provisional", "draft") or approximation words around figures ("about", "roughly"). Voice doubt directly to the user in chat.
12. **Metadata Restraint (Rule 22)**:
    - Frontmatter and metadata carry short structured values only; no notes to self or process narration.
13. **Freshness, Provenance & Exact-Artifact Validation (Rules 23 & 24)**:
    - Regenerate compiled outputs after final source changes. Never direct-patch compiled outputs.
    - Tie validation strictly to the exact final artifact SHA-256 hash. Compiled artifact governs over reports.

---

## 2. Skill-Specific Rules & Routing

These rules belong inside the operational workflows, references, and checklists of specific skills:

### To `documentation/` & `doc-coauthoring/`:
* **Rule 6**: Separate operative text from rationale (Purpose/Scope holds the why; numbered steps hold the rule).
* **Rule 9**: Match mood, tense, and voice to document type (Procedure: simple present, role-attributed; Proposal: first-person plural forward-looking; Order: shall/absolute; Correspondence: polite direct address).
* **Rule 14**: Page flow and vertical whitespace management (fill gaps before footers).
* **Rule 15**: Proposal narrative structure and tone (paragraphs and tables only, in-prose citations, donor call calibration).
* **Rule 16**: Default proposal typography and formatting (heading sizes, table styling, informative headings over marketing claims).

### To `legalese/`:
* **Rule 6**: Legal instrument clauses state commands only, without background rationale.
* **Rule 9**: Directive register: third-person, absolute "shall".
* **Rule 11**: Assigned register/tier is a floor, not a ceiling (Sovereign tier clauses in a policy represent elevation, not mismatch).

### To `communications/`:
* **Rule 9**: Correspondence register (polite direct address, past tense for completed action).
* **Rule 20**: External reader focus; internal concerns voice to the user.

### To `docx/`, `pdf/`, `pptx/`, `xlsx/`:
* **Rule 14**: Layout integrity, dead-space prevention, page breaks.
* **Rule 23 & 24**: Output regeneration from source; compiled artifact verification against cryptographic hash.

---

## 3. Mandatory Checklists Integration
Every governing skill and `AGENTS.md` must conclude with a mandatory checklist that the agent must explicitly evaluate before reporting task completion.
