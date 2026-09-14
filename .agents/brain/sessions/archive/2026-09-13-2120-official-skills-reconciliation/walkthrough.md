# Walkthrough — official-skills-reconciliation

## Context

The user hit three recurring agent failure modes (false-completion without
validation, letter-not-substance rule compliance, deliverable/context
bleed) and had already distilled fixes for most of them into a PBO-project
`RULES.md`. Plan was to harden this repo's shared rules first, then
reconcile against official vendor skills. The user reordered this at
plan-approval time: retrieve the official skills first, then analyze/harden.

## Changes so far

- Moved the stale, uncommitted `.agents/prompt.md` (an earlier, PBO-flavored
  draft of doctrine already mostly absorbed by the
  `2026-08-13-1755-generalize-pbo-doctrine` archived session) into this
  session's `meta/prompt-source-spec.md` as historical source material —
  it was loose directly under `.agents/`, not in a session folder.
- Vendored three official skill snapshots into `sources/upstream/`
  (gitignored, never committed — see each subfolder's `PROVENANCE.md` for
  exact commit hashes and licensing notes):
  - `anthropic-skills/` — full clone, 19 skills + spec + template.
  - `google-skills/` — full clone, 142 product-API skills.
  - `openai-plugins/` — partial: only OpenAI's own `plugin-creator` skill,
    since the rest of that repo is a 536-skill third-party marketplace, not
    OpenAI-authored content.

## Phase 3: diff results and actions

Diffed all 8 overlapping skills against `sources/upstream/anthropic-skills/`:

- **License finding (important):** `docx`, `pdf`, `pptx`, `xlsx` carry a
  restrictive proprietary `LICENSE.txt` (no extraction/retention outside
  "the Services," no derivative works, no redistribution) — a different
  posture from the other four, which are plain Apache 2.0. This repo's
  pre-existing copies of those four already carried this same license
  before this session touched anything, and are mirrored to every tool via
  `bootstrap`. Flagged to the user; they are separately reviewing the
  license question. No changes made to any of the four pending that review
  — not to the pre-existing repo copies, not to further adopting upstream
  content into them.
- `pdf`, `webapp-testing`: byte-identical to upstream. No action.
- `internal-comms`: one-line description diff; upstream's is a first-person,
  user-specific phrasing ("my company"), ours is already the better-
  generalized version. Kept ours.
- `skill-creator`: diff is entirely this repo's prior, correct de-vendor-
  locking of Claude/Claude.ai/Cowork-specific language into host-agnostic
  phrasing, plus an added AGENTS.md-authoring section upstream lacks. No
  upstream content is missing from ours. Kept ours.
- `frontend-design`: upstream is a substantially more developed rewrite (AI-
  generated-design-tells calibration section, plan/review/build/critique
  process, a copywriting section). Apache-2.0, no license concern. **Adopted
  upstream's body content**, keeping this repo's more trigger-rich
  `description` field (per this repo's own `skill-creator` guidance on
  "pushy" descriptions) rather than upstream's shorter one.
- `openai-plugins/plugin-creator` vs. this repo's `skill-creator`: not a
  real overlap — plugin-creator is Codex-marketplace/`.codex-plugin.json`
  packaging mechanics, not a skill-authoring methodology guide. No merge.
- `anthropic-skills/mcp-builder` vs. this repo's `graphify`: not a real
  overlap either — mcp-builder is about building a new MCP server from
  scratch; graphify is about using two already-built MCP tools
  (`code-review-graph`, `codegraphcontext`) for codebase graph analysis.
  No merge, but `mcp-builder` is a strong candidate for adoption as its own
  new skill if the user ever needs to build a custom MCP server.
- Surfaced two more net-new candidates worth the user's attention, not yet
  adopted: `discernment-nudge` (Apache-2.0 — appends 2-3 targeted follow-up
  questions after a substantive answer, once per conversation, inviting the
  user's own scrutiny; directly complements this session's own Verification
  Discipline work but from the user-facing side rather than the agent's own
  self-check) and `doc-coauthoring` (Apache-2.0 — a structured interactive
  drafting workflow: Context Gathering → Refinement & Structure → Reader
  Testing; complements rather than duplicates this repo's `documentation`
  skill, which governs the content rules rather than the collaborative
  process).

Nothing has been committed or pushed, per explicit instruction.

## Phase 1 + 2 + pagination consolidation

Executed in one pass at the user's direction ("consolidate... so we do not
have to suffer through this over and over again"):

- **`AGENTS.md`**: added "Verification Discipline" and "Deliverable
  Hygiene" sections under Repo Rules (validate the actual artifact not the
  plan; read fully, don't grep-and-presume; programmatic + visual/
  multimodal + manual validation; independent-method check for consequential
  quantitative results; context stays in chat, never laundered into a
  deliverable; no status/hedge language in delivered text; precedence
  clarified as max-strength within tier 3, still under tier 1 and the live
  user). Noted the rule-19-vs-commit-attribution distinction inline rather
  than as a separate section.
- **`documentation/SKILL.md`**: added the internal-vs-external default gate
  and a register-by-document-type table to the Document Medium section; a
  new "Deliverable Self-Narration and Hedging" section (no compliance
  self-narration, no hedging/approximation in delivered text, verify-
  before-writing, metadata-is-structured-values-not-prose); a new
  "Pagination and Physical Layout" section pointing at the new reference
  file; and four new Final Pass checklist items (12-16: authority-context
  leakage, self-status/progress narration, hedges/approximation, metadata
  restraint, rendered-artifact visual check).
- **`legalese/SKILL.md`**: added "the tier is a floor, not a ceiling" to
  Doctrine 1 with the documented severability-stripping incident as the
  cautionary example; a worked example to Doctrine 3 matching the user's
  own litigant-rights scenario (clean prohibition vs. rationale dressed as
  a second `shall` clause); "wording lock is narrower than structure lock"
  to Doctrine 9; and a "Physical Instrument Layout" pointer section.
- **`internal-comms/SKILL.md`**: added a short gate note — this skill
  applies once the user has confirmed the audience is internal, not merely
  because the communication type (status report, newsletter) sounds
  internal.
- **New `documentation/references/letterhead-and-pagination.md`**:
  consolidates everything worked out across this conversation — header/
  footer spacing (0.5" default), space-efficiency/no-dead-gaps, table
  page-break minimum (heading + 2 data rows, repeat heading on
  continuation pages), image page-break rule + oversized-image scale-down
  fallback, letterhead reduction on continuation pages (full letterhead
  page 1 only; name/motto/one context field, no logo/address/contact,
  page 2+), and front-matter/body numbering (roman for front matter
  becoming visible from the second physical page since the cover silently
  occupies `i`; Arabic restart at the substantive break, and — unlike the
  cover — that restart page's number *is* shown). Verified this last part
  against a real production instrument: screenshotted pages 1, 2, and 5 of
  the ANCEM Constitution (`/home/codelf/data/workspace/kibocha-solutions/PBOs/ANCEM/identity/governance/constitution/GVTM-FGD-8A43-ancem-constitution.pdf`)
  and confirmed the exact model (page 1 unnumbered, page 2 shows `(ii)`,
  page 5 shows `1`). That same screenshot pass also surfaced a live defect
  in that file — a stray unrendered `#` character above "Chapter One" on
  page 5, invisible at the source/text level, visible only on the rendered
  page — noted to the user as evidence for the rendered-artifact-check
  rule, not acted on (different project, not in scope here).

**Deliberately not touched:** `docx`/`pdf`/`pptx`/`xlsx` — the pointer to
the new reference file and the render-then-look verification mandate
belong there too, but those four skills are still held pending the user's
license review (see the earlier Phase 3 entry). Queued in `tasks.md`.

**Self-check flag:** `AGENTS.md` is now ~3,700 words. `skill-creator`'s own
authoring guidance (which this repo also follows) recommends keeping
`AGENTS.md` under ~1,500 words and pushing detail into skills/references.
It was already well past that before this session touched it (Privileged
Command Discipline, full Maestro protocol, full Prompt Injection Defense
tiers, MCP Tools table are all pre-existing, not added here) — flagging
for the user's awareness, not fixed unprompted since trimming/restructuring
it is a separate, larger task than this one.

Nothing has been committed or pushed.

## AGENTS.md precedence strengthened; documentation-skill audit; docx/pdf/pptx/xlsx reconciled

- **`AGENTS.md`**: added an explicit "tier 3 is a compliance requirement,
  not a balancing test" paragraph to Precedence — mandatory compliance
  below tier 1, excused only by material (not hypothetical) harm. Tier 1
  (genuine model-safety/harness constraints) is explicitly kept supreme
  over even this — that boundary isn't something this file can waive
  regardless of phrasing, so the text says so plainly rather than implying
  otherwise.
- **Documentation-skill audit**: scanned all 19 of this repo's own
  `SKILL.md` files (not the vendored snapshots) for the patterns
  `documentation/SKILL.md` itself flags (negative parallelism, weak-
  significance filler, vague attribution, em-dash overuse). Found one
  genuine violation — `legalese/SKILL.md`'s Archaic-tier research step used
  a diminish-to-elevate construction ("not only X but... not just borrow
  Y") — rewritten to state the requirement directly. Other pattern hits
  were false positives on contextual read (functional contrastive phrasing,
  documentation skill's own meta-references to its rules, and
  `pptx-master`'s heavy em-dash count, which is structural label—
  explanation usage in dense procedural tables, not narrative flourish).
  This was a pattern scan, not a full read of all 19 files.
- **`docx`/`pdf`/`pptx`/`xlsx` reconciled** (user's explicit direction:
  "update and merge, just don't commit," specifically so this doesn't have
  to be redone if Anthropic confirms the license only restricts resale/
  redistribution, not this kind of use):
  - Diffing surfaced that our `docx`'s script pipeline (`pack.py`/
    `unpack.py` with integrated run-merging, redline-simplification, and
    auto-repair validation) is more capable than the vendor's current
    public version (manual unzip/edit/zip + a standalone `merge_runs.py`)
    — so this was **not** a wholesale adopt-upstream swap like
    `frontend-design`. Kept our script infrastructure; added what was
    genuinely missing.
  - `docx/SKILL.md`: added a required "Verify the Output" section (render,
    read every page, check the last page of any table and the page after
    any letterhead/front-matter transition) + pointer to the new
    `letterhead-and-pagination.md`.
  - `pptx/SKILL.md`: already had an excellent visual-QA/verification-loop
    section (subagent fresh-eyes review, explicit defect checklist,
    fix-and-reverify loop) — better than what vendor documents, left as
    the reference model rather than "fixed." Added `.potx` support to the
    description (matches vendor's broader trigger coverage) and a
    "Branding Consistency" pointer applying the letterhead-reduction
    principle to title-slide-vs-content-slide branding.
  - `xlsx/SKILL.md`: had strong programmatic verification (`recalc.py`
    formula/error checking) but nothing visual, despite stating Professional
    Font / Color Coding / Number Formatting requirements up top with no way
    to confirm they were actually applied. Added a required "Visual
    Verification" section (render + read the images) explicitly framed as
    additive to, not a replacement for, the formula check.
  - `pdf/SKILL.md`: no content changes needed (byte-identical to vendor,
    and vendor's content was already sound) beyond adding the same
    "Verify the Output" mandate + reference pointer for PDFs created via
    `reportlab`, since pdf had neither before.

All of the above is working-tree only. Nothing committed or pushed.

## Skill-set restructuring at the user's direction

User set an explicit scope filter — adopt Anthropic skills only where they
serve agentic coding (independent of Claude), agentic legal writing, or
agentic document/report creation — and gave direct rename/delete
instructions. Executed:

- **Adopted as new skills**: `discernment-nudge`, `mcp-builder` (Apache-2.0,
  copied with one fix — a stale hardcoded `claude-3-7-sonnet-20250219`
  default in its evaluation script/docs, updated to `claude-sonnet-5`),
  and `doc-coauthoring` (Apache-2.0, but rewritten before insertion per
  explicit instruction: removed a tip suggesting the finished document
  link back to "this conversation" — a Documentation Source Boundary and
  AI-attribution violation — and de-vendor-locked its Claude/claude.ai-
  specific mechanics to host-agnostic language).
- **Not adopted, with reasons**: `claude-api`/`academy-guide` (Claude-
  dependent by the user's own stated filter; also already available
  separately), `web-artifacts-builder` (claude.ai's own artifact runtime,
  not portable), `brand-guidelines` (applies Anthropic's own corporate
  brand specifically — not a generic template), and the purely creative
  skills (`algorithmic-art`, `canvas-design`, `theme-factory`,
  `slack-gif-creator`) — none fit the three focus areas.
- **Google/OpenAI skills**: left to my judgment per the user — decided not
  to adopt any (Google's 142 skills are GCP/Workspace product-API guides;
  OpenAI's only own content, `plugin-creator`, is Codex-marketplace
  packaging mechanics). Kept vendored for reference only.
- **`internal-comms/` → `communications/`**: renamed and restructured with
  two explicit tracks — "External Communications (default)" (new) and
  "Internal Communications (confirmed audience only)" (existing 3P-update/
  newsletter/FAQ/general-comms content, now gated). `documentation/SKILL.md`
  no longer duplicates the internal/external gate logic — it points here.
- **`pptx-master/` deleted** (97 MB) — explicit instruction, no hedging.
  Confirmed no other file referenced it before removing.
- **`ci-cd` reigns supreme** for git/commit conventions — acknowledged as
  standing guidance; nothing currently conflicts with it, so no edit was
  needed, just noted for future conflicts.
- **`technical-diagrams` (Draw.io/mxGraph) diagram-quality question**:
  checked whether a superior skill exists in the vendored Anthropic/Google/
  OpenAI material — none of the three publish a dedicated architecture/
  technical-diagram skill to compare against. The existing skill already
  has render-backed visual QA and a full bundled-resource set; assessed at
  the `SKILL.md` level only, not the 7 `references/*.md` files individually.

Still working-tree only — nothing committed or pushed.

## Not changed yet

- `AGENTS.md`, `documentation/SKILL.md`, `legalese/SKILL.md`,
  `internal-comms/SKILL.md` — Phases 1-2 (hardening) not started.
- No skill has been diffed against its vendored counterpart yet — Phase 3
  not started.
- Nothing has been committed. `sources/upstream/` is untracked by design.

## Session path convention: migrated

Initially created under `.agents/brain/active/` (the convention `AGENTS.md`
and all prior sessions used at the time) and flagged the mismatch against
`maestro/SKILL.md`'s `.agents/brain/sessions/active/` wording rather than
silently picking one. The user confirmed: migrate to `sessions/`, and
discard every other session.

Actions taken:
- Moved this session folder to `.agents/brain/sessions/active/2026-09-13-2120-official-skills-reconciliation/`.
- Deleted `.agents/brain/active/2026-07-29-0333-setup-graphify-mcp/` and
  all five folders under `.agents/brain/archive/` (`graphify-mcp-correction`,
  `antigravity-mcp-activation`, `fix-graphify-local-state`,
  `graphify-cleanup-rollout`, `generalize-pbo-doctrine`). All 16 files were
  git-tracked, so this is a working-tree deletion only — fully recoverable
  from git history (`git log --all -- .agents/brain/archive/...`) even
  though nothing has been committed yet.
- Updated `AGENTS.md`'s two Maestro-section mentions and one
  Continuity-section mention of `.agents/brain/active/` to
  `.agents/brain/sessions/active/`.
- Updated `.agents/memory/gemini-antigravity-mcp-registration.md` to drop
  its now-dead citation of `.agents/brain/archive/` (kept the three
  session names as the evidentiary fact; dropped the path since that
  location no longer exists).
- Left `.agents/brain/handoffs/` and `.agents/brain/git/repo-health.json`
  untouched — the user said "sessions," and neither is a session folder.

## Phase 5 started: governance and full skill remediation

- Removed `sources/upstream/anthropic-skills/`,
  `sources/upstream/google-skills/`, and
  `sources/upstream/openai-plugins/` through the desktop trash after the user
  confirmed the exact scope. Only `sources/upstream/.gitignore` remains.
- Re-read the active session plan, tasks, walkthrough, all repository memory
  and handoff files, the Maestro instructions and references, the skill-creator
  instructions, the documentation instructions and weak-writing reference,
  `docs/SKILL_AUTHORING_GUIDE.md`, `AGENTS.md`, and the PBO root `RULES.md`.
- Confirmed the structural mismatch: `AGENTS.md` is 4,133 words despite the
  repository's 1,500-word ceiling; several skills exceed 500 lines; 17 of 21
  skills contain U+2014 em dashes; the prior audit was a pattern scan rather
  than a full contextual read of every skill.
- Added the sequential remediation checklist. No commit, push, bootstrap
  propagation, or installed-skill synchronization has been performed.

### Governance baseline and skill-creator

- Replaced `AGENTS.md` with a 991-word binding rule set. It contains no U+2014
  em dashes and stays below the 1,500-word authoring ceiling.
- Rewrote `docs/SKILL_AUTHORING_GUIDE.md` as a 618-word standard defining one
  authority chain and a procedural-only `SKILL.md` body.
- Read `skill-creator/SKILL.md` in full and replaced its 540-line,
  5,093-word body with a 215-line, 932-word ordered workflow.
- Preserved intent capture, structural authoring, paired evaluation, grading,
  benchmark aggregation, review UI generation, iteration, description
  optimization, packaging, and single-agent fallback behavior.
- Verified the final skill by full read, line and word counts, frontmatter
  presence, zero U+2014 em dashes, and existence of every linked local
  resource.

### Documentation

- Read the 572-line `documentation/SKILL.md` from start to finish.
- Replaced it with a 178-line ordered workflow covering routing, source
  gathering, document-type structure, technical-document placement, Markdown
  drafting, content verification, conversion, build validation, and final
  visual inspection.
- Preserved every specialized reference route, the external communication
  default, proposal narrative rules, Writerside controls, source-boundary
  checks, exact-artifact verification, and fixed-page inspection requirements.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, and existence of every linked local reference and asset.

### Bootstrap

- Read `bootstrap/SKILL.md` in full.
- Replaced its explanatory deployment narrative with a 124-line sequence for
  scope, source verification, target resolution, rule alignment, sparse skill
  synchronization, host scripts, Antigravity handling, hook registration, and
  final verification.
- Preserved the marker algorithm, non-cone sparse checkout, remote-main source,
  native-skill protection, WSL targets, separate Antigravity target, and
  checksum warning.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, linked-reference presence, and executable script presence.

### CI/CD

- Read the 567-line `ci-cd/SKILL.md` from start to finish.
- Replaced it with a 258-line sequence for task routing, repository-health
  capture, ancestry discovery, delivery inspection, commit creation,
  publication boundaries, failure handling, local cleanup, pull requests,
  pipelines, handoffs, and final verification.
- Preserved the three-attempt ceiling, signing and identity gates, single-scope
  Conventional Commit form, 72-word body cap, one-commit instruction, shared
  history protection, one-level ancestry advancement, and all reference routes.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, and existence of every linked local resource.

### Communications

- Read `communications/SKILL.md` in full.
- Replaced its explanatory register discussion with a 71-line workflow for
  audience classification, content gathering, external drafting, internal
  template routing, and final verification.
- Preserved the external default, per-communication audience confirmation,
  full-title and attachment rules, internal templates, narrative citation
  route, and fixed-page layout route.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, and existence of every linked template and reference.

### Discernment nudge

- Read the 209-line `discernment-nudge/SKILL.md` from start to finish.
- Replaced its philosophical framing and repeated boundary explanations with
  an 87-line eligibility, answer, question, append, and verification sequence.
- Preserved the once-per-conversation limit, all qualifying and excluded
  request classes, two-or-three-question limit, exact lead-in, first-person
  prompts, specificity requirement, and final-position requirement.
- Verified the final file by full read, line and word counts, frontmatter, and
  zero U+2014 em dashes.

### Document co-authoring

- Read the 349-line `doc-coauthoring/SKILL.md` from start to finish.
- Replaced its facilitation narrative with a 154-line sequence for workflow
  selection, context gathering, structure, section drafting, complete-draft
  review, reader-question prediction, independent testing, manual fallback,
  and finalization.
- Preserved the three drafting stages, freeform opt-out, connector handling,
  five-to-ten questions, five-to-twenty options, targeted edits, fresh-reader
  isolation, and documentation-skill verification route.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, and the linked documentation skill.

### DOCX

- Read the 606-line `docx/SKILL.md` from start to finish.
- Replaced it with a 221-line operation sequence for reading, conversion,
  generation, tables, images, XML editing, tracked changes, comments,
  acceptance, validation, rendering, and visual inspection.
- Removed the hardcoded `AI Assistant` tracked-change author. The skill now
  preserves an established author, uses a user-specified author, or uses the
  neutral label `Editor`.
- Preserved the DXA dimensions, table-width constraints, `docx-js` structural
  rules, OOXML change rules, comment marker rules, pack/unpack tools, automatic
  repair boundary, and every-page verification requirement.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, and existence of every invoked script and linked layout reference.

### Frontend design

- Read `frontend-design/SKILL.md` from start to finish.
- Replaced its studio-persona and design-theory prose with a 137-line sequence
  for brief definition, design tokens, layout, default-pattern rejection,
  interface copy, implementation, motion, behavioral testing, and visual QA.
- Preserved the brief-specific visual direction, typography and line-length
  controls, generic-design pattern list, one-memorable-element restraint,
  accessibility floor, responsive checks, state coverage, and screenshot loop.
- Verified the final file by full read, line and word counts, frontmatter, and
  zero U+2014 em dashes.

### Graphify

- Read `graphify/SKILL.md`, every linked reference, the feature-staging example,
  the MCP template, and the repository graph ignore files in full.
- Replaced the explanatory tool survey with an 89-line workflow for scope,
  availability, routing, change analysis, architecture analysis, compliance
  mapping, staging, state management, and reporting.
- Rewrote the supporting references and example as direct procedures. Removed
  remote shell-pipe installation commands, destructive database recovery,
  machine-specific paths, obsolete session paths, and U+2014 em dashes.
- Moved the graph-state convention to `.agents/code-graphs/`, corrected the
  root ignore files so they no longer exclude the tracked `graphify` skill or
  all skill content, and moved the generated CGC and CRG database artifacts to
  the desktop Trash.
- Replaced the explanatory MCP asset with a valid two-server JSON template.
- Verified the final package by full read, JSON parsing, link review, ignore
  checks, `git diff --check`, and prohibited-pattern scans.

### Legalese

- Read `legalese/SKILL.md`, every linked legal reference, the calibration
  examples, the termination-phrase asset, and the fixed-page layout reference.
- Replaced the persona declaration, repeated doctrine commentary, placeholder
  flag, and hidden-thought disclosure instruction with a 167-line drafting and
  evidence-verification sequence.
- Preserved the four registers, Sovereign default, register-floor rule, nine
  doctrines, user wording lock, structural fidelity, source hierarchy,
  hostile-reading audit, sovereign economy, severability, and fixed-page QA.
- Made user-supplied legal wording controlling and prohibited silent changes to
  locked wording or hierarchy.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, link resolution, prohibited-pattern scans, and `git diff --check`.

### Maestro

- Read `maestro/SKILL.md` and all four references in full.
- Replaced the narrative planning manual with a 112-line orientation, session,
  plan, task, execution, threshold, verification, memory, and archival flow.
- Rewrote all references as compact procedures and corrected the singular
  `session/` tree defect to the repository's `sessions/active/` and
  `sessions/archive/` convention.
- Restricted `goal.md` creation to an explicit user request or governing
  runtime requirement and kept repository memory descriptive rather than a
  duplicate policy authority.
- Verified the package by full read, line and word counts, zero U+2014 em
  dashes, link resolution, prohibited-pattern scans, and `git diff --check`.

### MCP builder

- Read `mcp-builder/SKILL.md` and all four supporting references in full.
- Verified the current MCP protocol and official TypeScript and Python SDK
  documentation before editing.
- Replaced the vendor-oriented guide with a 126-line provider-neutral sequence
  for protocol verification, transport, surface design, schemas, security,
  implementation, errors, tests, evaluation, and documentation.
- Rewrote the references for current SDK v2 routing, including Python
  `MCPServer`, current TypeScript packages, Standard Schema inputs, Streamable
  HTTP, and provider-neutral evaluations.
- Moved the obsolete Anthropic-specific evaluation scripts and requirements to
  the desktop Trash while retaining the source license.
- Verified the package by full read, line and word counts, zero U+2014 em
  dashes, link resolution, provider-residue scans, and `git diff --check`.

### PDF

- Read `pdf/SKILL.md`, `forms.md`, and `reference.md` in full and inventoried
  every bundled PDF utility.
- Replaced library tutorials and code dumps with a 136-line operation sequence
  for inspection, reading, scans, extraction, manipulation, creation, forms,
  encryption, repair, and exact-final-artifact verification.
- Preserved source and derived boundaries, fillable and annotation form paths,
  OCR verification, page-range accountability, ReportLab glyph controls, and
  mandatory every-page rendering and inspection.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, linked-resource and script resolution, prohibited-pattern scans, and
  `git diff --check`.

### PPTX

- Read `pptx/SKILL.md`, `editing.md`, and `pptxgenjs.md` in full and inventoried
  the Office package utilities.
- Replaced the palette catalogue, motivational design prose, mandatory
  delegation, and forced defect-cycle rule with a 136-line source, inspection,
  build-path, storyboard, design, layout, content, data, package, validation,
  and render workflow.
- Preserved template fidelity, XML relationship controls, PptxGenJS corruption
  guards, formal-branding reduction, placeholder detection, and exact-final
  slide inspection.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, link and script resolution, prohibited-pattern scans, and
  `git diff --check`.

### SSH

- Read `ssh/SKILL.md` and all four references in full.
- Replaced the compact router and unsafe deep references with a 82-line
  inspect, safety, routing, configuration, verification, and documentation
  workflow plus four concise task procedures.
- Removed routine instructions to uninstall Git, change Windows services,
  install packages, reload SSH, edit firewalls, delete keys, use destructive
  synchronization, terminate sessions, or bypass failed access controls.
- Preserved host aliases, WSL client separation, password-manager routes, Git
  authentication, SSH signing, allowed signers, deploy-key inventories,
  rotation, offboarding, and critical-infrastructure verification.
- Verified the package by full read, line and word counts, zero U+2014 em
  dashes, link resolution, dangerous-command scans, and `git diff --check`.

### System design

- Read `system-design/SKILL.md` and all four references in full.
- Replaced the goal prose and abbreviated procedure with a 125-line sequence
  for scope, project truth, workflows, responsibilities, naming, ERDs,
  behavior, alternatives, durable design records, promotion, and verification.
- Added declared-dependency normalization through 5NF, lossless decomposition,
  dependency preservation, anomaly tests, lifecycle behavior, source-of-truth
  separation, and implementation authorization gates.
- Verified the final file by full read, line and word counts, zero U+2014 em
  dashes, link resolution, prohibited-pattern scans, and `git diff --check`.

### System init

- Read `system-init/SKILL.md` and all four references in full.
- Replaced the workstation narrative and machine-specific procedures with an
  82-line scope, read-only audit, permission, installation, storage,
  toolchain, and verification sequence plus four concise references.
- Removed policy tests that attempted forbidden `systemctl` and package-manager
  commands, hardcoded devices and UUIDs, automatic symlink replacement,
  self-applied sudoers changes, and workstation-specific upgrade recipes.
- Preserved exact-device confirmation, unknown-device exclusion, existing-data
  preservation, dedicated install authorization, `sudoedit` boundaries,
  official version checks, and exact final-state reporting.
- Verified the package by full read, line and word counts, zero U+2014 em
  dashes, link resolution, dangerous-command and machine-residue scans, and
  `git diff --check`.

### Technical diagrams

- Read `technical-diagrams/SKILL.md`, all eight references, and all three
  scripts in full.
- Replaced the explanatory structure with a 70-line source, modeling,
  generation, validation, rendering, inspection, and delivery procedure plus
  eight concise references.
- Removed the automatic Draw.io download and system-package installer and
  changed renderer failure handling to preserve the separate-user-authorization
  boundary.
- Preserved editable Draw.io source, stable mxGraph identifiers, project style
  tokens, standards traceability, exact-final rendering, every-canvas visual
  inspection, and Writerside export checks.
- Verified the package with XML and JSON bundle checks, Bash syntax checking,
  Python compilation, full final read, zero U+2014 em dashes, residue scans,
  and `git diff --check`.

### Web application testing

- Read `webapp-testing/SKILL.md`, its server helper, and all three examples in
  full.
- Replaced the black-box and explanation-heavy guide with a 94-line inspect,
  start, exercise, assert, capture, inspect, clean-up, and report procedure.
- Replaced the helper's `shell=True` execution and unconsumed output pipes with
  direct argument execution, readiness checks, process-group cleanup, and
  explicit working directories.
- Replaced hardcoded example identities and output paths with argument-driven
  examples that close browsers in `finally` blocks.
- Verified syntax, help output, live server startup, HTTP readiness, command
  execution, process cleanup, full final read, zero U+2014 em dashes, residue
  scans, and `git diff --check`.

### XLSX

- Read `xlsx/SKILL.md`, the recalculation helper, and its LibreOffice wrapper
  in full.
- Replaced the 310-line tutorial and fixed financial-format mandate with a
  154-line inspection, tool-routing, preservation, creation, formula,
  formatting, recalculation, rendering, and exact-final validation procedure.
- Removed the user-profile macro mutation, compiled `LD_PRELOAD` shim, and
  unrelated Office package utilities and schemas.
- Rebuilt recalculation around an isolated temporary LibreOffice profile,
  atomic replacement after formula-error validation, and an XLSM exclusion.
- Verified help output, Python compilation, an end-to-end XLSX formula
  recalculation with preserved formula and cached value, full final read, zero
  U+2014 em dashes, residue scans, and `git diff --check`.

### PBO rules migration

- Re-read the 24-rule PBO `RULES.md` and compared every rule with the final
  shared `AGENTS.md`, `documentation`, `legalese`, `maestro`, and artifact
  skills.
- Added the deliberate dual-memory requirement and the exact release hash
  sequence to the shared `AGENTS.md`.
- Rewrote the proposal-narrative and fixed-page pagination references as
  direct procedures while preserving the user's exact proposal defaults and
  page-flow rule.
- Added `documentation/references/pbo-document-rules.md` for the PBO-only
  ANCEM/SOP punctuation rule and proposal formatting defaults, and made the
  documentation skill require it for PBO repository work.
- Created and verified a 24-entry disposition register in `meta/`.
- Moved the superseded PBO root `RULES.md` to the desktop Trash after every
  rule had an authoritative destination.

## Final verification

- Read each of the 21 final top-level `SKILL.md` files in full during its
  individual remediation pass and recorded the result above.
- Re-read the final shared rules, documentation routes, PBO-specific
  reference, authoring standard, rule-disposition register, README, scaffold,
  and validator after the last edits.
- Replaced the repository scaffold placeholder with a deterministic tool that
  validates kebab-case names, requires a trigger description, quotes YAML
  safely, creates only requested resource directories, and refuses to
  overwrite an existing destination.
- Tested scaffold creation, optional resource directories, colon-containing
  descriptions, invalid-name refusal, overwrite refusal, and Python syntax.
- Ran `tools/validate-all.sh` against the exact final worktree. Result: 21
  skills passed frontmatter, structure, line-count, prose-residue, local-link,
  routed-resource, JSON, Draw.io XML, and Python checks. Shell syntax and
  `git diff --check` also passed.
- Confirmed `sources/upstream/` contains only `.gitignore`.
- Confirmed `/mnt/data/workspace/kibocha-solutions/PBOs/RULES.md` is absent.
- Applied the Maestro memory admission test. No memory entry was added because
  every durable rule is explicit in `AGENTS.md`, a skill, or a routed
  reference.
- Did not run bootstrap propagation and did not commit or push.

## Completion

Every Phase 5 acceptance criterion passed. The session state is `DONE` and
remains under `sessions/active/` until a new task or phase triggers archival.
