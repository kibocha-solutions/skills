# Implementation Plan — official-skills-reconciliation

## Goal Statement

Two linked problems, worked in this order per the user's explicit direction:

1. **Retrieve and store current, stable official skill material** from
   Anthropic, Google, and OpenAI as local reference snapshots inside this
   repo (done — see Phase 0), so later comparison work has something
   concrete and current to diff against instead of relying on training-data
   memory of what these vendors ship.
2. **Harden this repo's own governing rules and drafting skills** against
   three recurring agent failure modes the user has hit repeatedly: (a)
   claiming a deliverable is done without validating the actual artifact —
   programmatically, visually/multimodally, and manually — and never
   cross-checking quantitative results by an independent method; (b)
   satisfying a rule's letter (grepping a description, cosmetic rewording)
   while missing its substance; (c) leaking chat-only context (rationale,
   status, approval-pending state) into delivered documents instead of
   raising it with the user. Then, using the vendored snapshots from Phase
   0, reconcile this repo's skills against them: merge where genuinely
   redundant (preferring official naming), keep real specializations
   separate, adopt or reference net-new official skills where valuable.

"Done" looks like: `AGENTS.md` carries two new maximally-strong,
repo-wide sections (Verification Discipline, Deliverable Hygiene);
`documentation/SKILL.md` and `legalese/SKILL.md` absorb the still-missing
material from `/home/codelf/data/workspace/kibocha-solutions/PBOs/RULES.md`;
the internal/external communication default is gated between `documentation`
and `internal-comms`; and a scoped, evidence-based comparison exists between
this repo's skills and the vendored Anthropic/Google/OpenAI snapshots,
with concrete merge/adopt/skip recommendations the user signs off on before
any skill is renamed, merged, or deleted.

## Background

- `/home/codelf/data/workspace/kibocha-solutions/PBOs/RULES.md` (24 rules,
  dated 2026-09-04) is the user's own hard-won, PBO-flavored doctrine. Diffed
  against current `documentation/SKILL.md` and `legalese/SKILL.md`: most of
  it is already merged (economy of disclosure, context/content source
  boundary, general-first, no-rationale-in-operative-clauses, cosmetic-
  compliance ban, self-status narration) via the prior archived session
  `2026-08-13-1755-generalize-pbo-doctrine`. Real gaps remain — see Phase 2.
- `.agents/brain/archive/2026-08-13-1755-generalize-pbo-doctrine/` already
  generalized an earlier draft of this doctrine
  (`meta/prompt-source-spec.md` in this session — formerly the loose,
  uncommitted `.agents/prompt.md`) into the same two skills. That draft is
  now superseded; kept here only as historical source material.
- `AGENTS.md`'s existing "Rule Fidelity" section already targets letter-vs-
  substance compliance, but scoped to skills only, not to deliverables or to
  itself — the user's live complaints show it isn't strong or broad enough
  in practice.
- `skill-creator/SKILL.md` in this repo is already a verbatim vendor of
  Anthropic's own `skill-creator`, confirming this repo already does
  official-skill vendoring in at least one place — Phase 0 generalizes that
  practice into a proper `sources/upstream/` snapshot area.

## Phase 0 — Retrieve official skill snapshots (COMPLETE)

Stored under `sources/upstream/` (gitignored — reference only, never
committed, per user instruction and existing `sources/` convention):

- **`sources/upstream/anthropic-skills/`** — full clone of
  `github.com/anthropics/skills` @ `34040c9` (2026-09-10). 19 skills incl.
  direct overlaps with this repo (`docx`, `pdf`, `pptx`, `xlsx`,
  `skill-creator`, `internal-comms`, `webapp-testing`, `frontend-design`) and
  net-new candidates (`claude-api`, `mcp-builder`, `doc-coauthoring`,
  `academy-guide`, `discernment-nudge`, `algorithmic-art`,
  `web-artifacts-builder`, `brand-guidelines`, `canvas-design`,
  `slack-gif-creator`, `theme-factory`). Also carries the canonical
  `spec/` (Agent Skills spec) and Anthropic's `template/`.
  **License flag**: `docx`/`pdf`/`pptx`/`xlsx` here are source-available,
  not open source — reference/diff only, do not copy their implementation
  into this repo's skills of the same name. See its `PROVENANCE.md`.
- **`sources/upstream/google-skills/`** — full clone of
  `github.com/google/skills` @ `150f8525` (2026-09-11), Apache 2.0. 142
  skills, all Google Cloud/Workspace product-API skills (`ads/`,
  `analytics/`, `cloud/`, `developers/`, `identity/`) — low direct overlap
  with this repo's generalist skill set; vendored for completeness per the
  user's request. See its `PROVENANCE.md`.
- **`sources/upstream/openai-plugins/`** — partial: only
  `.agents/skills/plugin-creator/` (OpenAI's own authoring skill) and
  `README.md` from `github.com/openai/plugins` @ `1dc19589`. OpenAI's prior
  dedicated skills catalog (`openai/skills`) is deprecated in favor of this
  repo, but the full repo (98 MB, 536 `SKILL.md` files) is a third-party
  plugin marketplace (CircleCI, Notion, Temporal, NVIDIA, etc.), not an
  OpenAI-authored collection — bulk-vendoring it would mostly capture other
  vendors' product plugins. See its `PROVENANCE.md` for the scoping
  rationale; re-fetch a specific third-party plugin later if one becomes
  relevant.

## Phase 1 — Harden `AGENTS.md`

Add two new sections under "Repo Rules", alongside the existing "Rule
Fidelity":

**Verification Discipline** (new):
- Never report a deliverable complete without confirming the artifact
  itself — not the plan for it — exists, is reachable, and matches the ask.
- A full contextual read is mandatory before judging compliance or quality,
  for both skills and deliverables; grep/keyword search locates, it never
  substitutes for reading start to finish.
- Validate with every method the artifact type warrants: programmatic
  (tests, linters, schema checks, builds), visual/multimodal (actually
  render and look at the output), and manual read-through.
- Quantitative/mathematical/computational results with material
  consequences get checked by an independent method (different tool,
  formula path, or model) before being presented as settled.
- Speed and the appearance of having satisfied the user are not success
  criteria.
- Cosmetic/letter-only compliance that preserves a rule's underlying
  defect counts as non-compliance.

**Deliverable Hygiene** (new):
- Context the user supplies to explain a decision is for the agent's
  judgment only — never transcribed or dressed up as a clause/comment
  inside the deliverable.
- No status, progress, or approval-pending language inside a deliverable;
  no hedge/approximation words around figures.
- Missing authorization or an unverified/estimated fact goes to the user in
  chat, every time — never encoded as an in-document caveat.

Append a precedence clarification: both sections are maximum-strength within
tier 3 (no skill or shortcut loosens them), still subordinate to tier 1
(actual harm/safety) and to the live user's own current-turn instruction —
clarifying, not weakening, the existing tier order.

Note the rule-19-vs-commit-attribution distinction (content deliverables vs.
this session's own harness-level Claude Code commit/PR attribution
convention) inline as a one-line scope clarifier, not a contradiction.

## Phase 2 — Fill remaining `documentation`/`legalese` gaps from RULES.md

`documentation/SKILL.md`:
- Add "No Compliance Self-Narration" (rule 7 gap).
- Add "Verify Before Writing" (rule 17 gap).
- Add "No Hedging or Approximation in Delivered Text" (rule 20 — the core
  gap behind the user's main complaint).
- Add a register-by-document-type table (rule 9, de-PBO'd).
- Add a trimmed artifact-freshness principle (rule 23: never hand-patch a
  generated Word/PDF; regenerate from source).
- Extend the Final Pass checklist with: authority-context leakage,
  self-status/progress narration, hedge/approximation words, metadata
  restraint.
- Add the internal-vs-external communication default (flagged mid-planning
  by the user): default every communication/deliverable to external
  register until the user explicitly confirms, live, an internal audience;
  external default means full-title references (never filenames),
  attachment/citation instead of bare links, and formal tone. Gate this as
  the trigger boundary with `internal-comms/SKILL.md` (add a one-line
  cross-reference there too).
- Optional, flag for the user's call: condensed proposal/CFP narrative
  conventions (rule 15). Rule 16's specific formatting table (point sizes,
  colors) stays PBO-local house style, not a generalized rule.

`legalese/SKILL.md`:
- Add "User-supplied wording is locked" (rule 18).
- Add "Tier is a floor, not a ceiling" (rule 11), with the documented
  severability-clause-removal incident as the cautionary example.
- Reinforce Doctrine 3 with a worked example matching the user's own
  litigant-rights scenario (clean prohibition vs. rationale dressed as a
  command).

## Phase 3 — Reconcile against vendored official skills

For each of this repo's skills that has a direct Anthropic counterpart
(`docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`, `internal-comms`,
`webapp-testing`, `frontend-design`): diff current vs. vendored, identify
drift, and propose which specific pieces to adopt from upstream vs. which
of this repo's specializations to keep layered on top. Present the mapping
for sign-off before merging, renaming, or deleting anything — this step is
structurally hard to reverse cleanly once executed.

For skills without a direct official equivalent, note candidate patterns
worth borrowing from the vendored material (e.g. OpenAI's `plugin-creator`
vs. this repo's `skill-creator`; Anthropic's `mcp-builder` vs. this repo's
`graphify`/MCP-registration content) rather than wholesale adoption.

## Open Questions

- Whether to add the condensed proposal/CFP narrative conventions (rule 15)
  to `documentation/SKILL.md` inline or as a `references/` file — the user's
  call at review time.
- Exact scope of Phase 3 merges — held for explicit sign-off per skill
  before any rename/merge/delete, per this session's own Verification
  Discipline addition (don't let "reconciliation" become silent scope
  change).

## Verification Plan

- Re-read each edited `SKILL.md` and `AGENTS.md` in full after editing (not
  grepped) to confirm no duplicate or contradictory guidance was introduced.
- Confirm `sources/upstream/` stays untracked (`git status --porcelain`
  shows nothing under it) after each Phase 0-related step.
- Spot-check the two worked examples added (litigant-rights clause,
  severability-stripping incident) against the user's own described
  scenarios for fidelity.
- Do not run `bootstrap`'s propagation scripts or commit/push without
  asking first — this fans out to every tool's global instructions on this
  machine.

## Phase 5 — Governance and full skill remediation

### Goal Statement

Replace the current mixed instruction architecture with one compact authority
chain. `AGENTS.md` will contain only universal, absolute instructions and
prohibitions. Each `SKILL.md` will contain a clear task procedure in execution
order, without explanatory or justificatory prose. Human-facing authoring
standards will remain in `docs/`. The rules currently held in the PBO
repository's root `RULES.md` will be mapped into the controlling file for each
subject, verified, and removed from the PBO repository.

### Acceptance Criteria

1. `sources/upstream/` contains none of the Anthropic, Google, or OpenAI
   snapshot directories named by the user.
2. `AGENTS.md` contains fewer than 1,500 words and states universal rules as
   direct, absolute instructions or prohibitions.
3. Every top-level `SKILL.md` is read from start to finish and remediated one
   skill at a time.
4. Every remediated `SKILL.md` has valid frontmatter, ordered operational
   steps, necessary constraints, and no explanatory or justificatory prose.
5. No remediated `SKILL.md` contains U+2014 em dashes, decorative contrast,
   purposeless fourth-wall prose, promotional language, or placeholder
   residue.
6. Each of the 24 rules in the PBO `RULES.md` has an explicit disposition:
   universal rule in `AGENTS.md`, task rule in a skill or reference, local-only
   PBO rule retained elsewhere in that repository, or deliberate retirement.
7. The PBO root `RULES.md` is removed only after the disposition check passes.
8. Repository validation and a final manual read of every changed instruction
   file pass against the exact final files.

### Proposed Changes

- [MODIFY] `docs/SKILL_AUTHORING_GUIDE.md`: define the compact authority chain
  and the required procedural form for skills.
- [MODIFY] `AGENTS.md`: retain universal absolutes and route task procedure to
  skills.
- [MODIFY] `*/SKILL.md`: remediate each skill independently in the sequence
  recorded in `tasks.md`.
- [MODIFY] Relevant `references/`: retain necessary task detail that would
  overload a skill body.
- [DELETE] `/mnt/data/workspace/kibocha-solutions/PBOs/RULES.md`: remove the
  former root authority after all 24 rules are accounted for.
- [MODIFY] Session plan, tasks, and walkthrough: record each completed skill
  and its verification evidence.

### Open Questions

None. The physical move of `RULES.md` is implemented as a verified migration
of its rules into their controlling destinations, followed by removal of the
old root file. This avoids creating another competing runtime authority.

### Verification Plan

- Re-read each skill in full before editing and again after editing.
- Validate frontmatter and bundled-resource links after each skill.
- Run the documentation residue checks after each skill.
- Run `tools/validate-all.sh` after the complete pass.
- Count `AGENTS.md` words and inspect every retained rule manually.
- Check all 24 PBO rules against a disposition register before removing the
  old file.
- Inspect the final Git diff without reverting or overwriting unrelated user
  changes.
