---
name: documentation
description: >
  Draft, review, rewrite, and improve documentation, README files, guides,
  procedures, reference pages, Writerside-compatible technical documentation,
  API prose, docstrings, comments, and API comment blocks. Use to remove weak
  AI-patterned writing such as generic importance claims, promotional tone,
  unsupported synthesis, vague attribution, unnecessary verbosity, negative
  parallelisms, purposeless fourth-wall references, placeholder residue,
  citation artifacts, malformed markup, and over-formatted prose. For
  technical diagrams, architecture visuals, Draw.io sources, diagram palettes,
  and SVG exports, route to the technical-diagrams skill.
---

# Documentation

## Goal

Produce documentation that is specific, verifiable, neutral, and easy to use.
When revising existing text, treat suspicious patterns as quality risks due for
improvement. Preserve the author's useful meaning.

## Default Approach

1. Identify the audience, document type, and reader task.
   For software or systems technical documentation, read
   `references/technical-documentation-routing.md` and
   `references/technical-documentation-library.md`, then
   `references/writerside-technical-documentation.md` and any migrated
   reference for the matching documentation type if it exists.
   For documentation comments, docstrings, API comment blocks, or
   implementation comments, read
   `references/code-comment-documentation.md`; consult
   `examples/code-comments/` when the right comment level, language convention,
   or amount of detail is unclear.
2. Audit whether existing documentation is current and whether expected
   documentation levels are missing. For source-level documentation, check
   package, module, file, class/type, constructor, property/field,
   function/method, and implementation comments where the language and repo
   convention expect them.
3. If a missing or stale documentation update is safe and non-destructive,
   make it from local evidence and tell the user what was added or refreshed.
   If the update would replace existing docs, delete disputed comments, or
   require unverifiable contract details, ask before changing it, state what
   is missing and wait for explicit confirmation.
4. Preserve verified facts, concrete examples, source-backed claims, and useful
   structure.
5. Flag suspicious text as a quality risk due for improvement.
6. Replace broad claims with precise facts, steps, constraints, or stated
   unknowns.
7. Use Writerside-compatible Markdown for software and systems technical
   documentation, and follow the code comment guide for source-level
   documentation. This does not apply to ordinary reports, word-processing
   documents, or non-technical prose unless the user asks for Writerside.
8. Remove text that does no work for the reader.
9. If the text already meets the target quality, preserve it. Do not force
   edits just to show activity.
10. Do a final residue pass before delivery.

## Technical Documentation Workflow

For software or systems documentation, use the technical library workflow before
drafting:

1. Identify the requested document type, audience, lifecycle stage, and access
   level.
2. Decide the target path from
   `references/technical-documentation-library.md`. Use the existing project
   structure if present; otherwise use the default `docs/` library structure.
   For quick path lookup, consult `assets/technical-docs-required-tree.md`
   and `assets/technical-docs-optional-tree.md`.
3. Choose the Writerside instance tree: `public.tree`, `internal.tree`,
   `restricted.tree`, or `confidential.tree`. Use a TOC library tree only
   when the project needs reusable navigation sections; use snippet library
   topics for reusable content fragments.
4. Gather local sources of truth first: source code, schemas, configs, tests,
   tickets, existing docs, diagrams, and generated artifacts.
5. If the repository contains `sources/reports/documentation-reference.md` or
   an equivalent documentation architecture report, read the relevant sections
   before creating or restructuring technical docs.
6. Review authoritative online sources when the document type depends on an
   external standard, framework, API, security rule, or Writerside behavior.
   For Writerside-specific structure, markup, navigation, or rendering claims,
   consult the official Writerside documentation at
   `https://www.jetbrains.com/help/writerside/`.
7. If the document needs production diagrams or SVG exports, route that work to
   the `technical-diagrams` skill and embed only the final documentation asset.
8. Draft with the general writing rules in this skill: concrete facts,
   neutral language, no filler, and explicit unknowns.
9. Validate path, classification, sources, required sections, links, commands,
   diagrams, and Writerside tree inclusion before handing off.

## Core Checks

Apply these checks on every documentation task. For detailed watchlists and
examples, read `references/weak-ai-writing-patterns.md` when the user asks for
a close rewrite, quality cleanup, or editorial review.

### Specificity

Replace broad claims with the concrete fact, source-backed consequence, or
explicit unknown.

### Economy

Every sentence in an artifact must do useful work. Keep text that narrows the
subject, adds context, gives an instruction, states a constraint, verifies a
claim, warns about a real risk, or connects two necessary ideas.

Remove text that merely announces, decorates, repeats, praises, previews,
summarizes without adding a decision, or explains why the document exists.
Technical documentation needs this rule most because filler hides the command,
parameter, failure mode, or operational constraint the reader came to find.

Before keeping a sentence, ask what would break if it disappeared. If the answer
is "nothing," delete it or merge the one useful detail into a nearby sentence.

### Neutrality

Use plain descriptions. Attribute evaluative claims or remove them.

### Analysis

Remove interpretation that the source does not support. Keep facts,
recommendations, and constraints distinct.

### Negative Parallelism

Eradicate the diminish-to-elevate rhetorical move in all its forms. The
forbidden pattern is not a specific phrase — it is any construction that
elevates Y by first diminishing X. Paraphrasing the surface words while
preserving the rhetorical move is not compliance.

Forbidden forms include but are not limited to:

- `not just X, but Y`
- `not only X, but also Y`
- `more than X` / `more than just X`
- `went beyond X`
- `exceeded mere X`
- `was not limited to X`
- `Y, rather than X`
- `Y, not just X`
- `not X. Y.` / `not just X. This is Y.`

**Paraphrase loophole example:**

Original: `This was not just an alignment concern.`

Malicious compliance: `This was more than alignment concerns.` — the surface
words changed but the diminish-to-elevate move survived. This is a failure.

Compliant: remove the contrast entirely. State the important point directly.
If emphasis on the secondary point is needed, place it elsewhere in the
paragraph without the contrast frame:

```text
All aspects of the structure appeared null if not nullable. [...paragraph...]
Alignment concerns could not cure this document.
```

Use a direct positive sentence. The only exception is when the contrast itself
is the factual point the reader needs — when the distinction between X and Y
is the information, not a rhetorical device for emphasis.

### Attribution

Replace vague authority with named, checkable sources. Watch for `experts
argue`, `observers note`, `industry reports`, `critics say`, `several sources`,
`media outlets`, `independent coverage`, `active social media presence`, and
notability claims that summarize coverage instead of explaining substance.

Do not imply broad agreement from one or two sources.

### Structure

Keep headings, lists, emphasis, tables, and conclusions proportional to the
reader task. Remove scaffolding that only makes the artifact look complete.

### Fourth Wall

Keep every section focused on its subject, not on the document as a medium. The
writer is the researcher, programmer, analyst, operator, or actor who did the
work. Write from that position.

Do not write purposeless medium references:

- `This report analyzes...`
- `This document outlines...`
- `This section discusses...`
- `The purpose of this guide is...`

Name the subject directly:

- `The problem exposes...`
- `The deployment failed because...`
- `The experiment measured...`
- `The migration requires...`

For each section, identify the section subject before drafting. A problem
statement talks about the problem, who it affects, how it was found, and what it
changes. A method section talks about the method. A results section talks about
the results. Do not drift into the document's intent unless the user explicitly
asked for a meta-description.

Allowed fourth-wall references are narrow:

- Cross-references that help navigation, such as `As noted in Prerequisites`.
- Required structural labels, such as `Scope`, `Assumptions`, or `Method`.
- Explicit user requests to explain document structure.

### Em Dash Character

Avoid the U+2014 dash in normal prose. It is allowed only for preserved
quotations, legal or policy-style enumerated exceptions, authorized headings,
and formal names that already include the character.

### Markup and Residue

Remove chatbot artifacts, placeholders, malformed markup, tracking parameters,
broken references, and citation residue. Repair the underlying source or claim.

## Rewrite Procedure

1. Read the text once for purpose and structure.
2. Use internal notes to identify weak passages. Do not include those notes in
   the final documentation unless the user asks for an editorial report.
3. Draft or rewrite in Markdown first, regardless of the final target format.
   Markdown is the quality-control medium — it is readable, diffable, and easy
   to verify against every check in this skill. Do not convert to the target
   format (docx, pdf, pptx, or any non-Markdown format) until the Final Pass
   is complete and clean.
4. Apply these transformations across the draft:
   - tighten wordy but valid text
   - attribute interpretive claims when a source supports them
   - replace vague claims with concrete facts, steps, constraints, or explicit
     unknowns
   - remove sentences that do not narrow, contextualize, instruct, verify, warn,
     or connect
   - remove unsupported significance claims, decorative contrast, and
     unverifiable fluff
   - eradicate every forbidden pattern in all its rhetorical forms, not just
     the exact surface phrasing listed in the Core Checks — paraphrases of
     forbidden patterns are still failures
   - preserve text that is already clear, factual, and human-written
5. Verify citations and links for claims that depend on external evidence when
   browsing, local source files, or accessible references are available. If a
   source cannot be accessed, do not invent verification. Preserve plausible
   URLs, but flag high-risk claims for user verification.
6. Normalize headings, lists, emphasis, tables, and code fences.
7. Re-read the result for a human documentation voice: direct, grounded, and
   free of ornamental certainty.
8. Run the Final Pass. Only after the Final Pass is clean, convert to the
   target format if the target is not Markdown.

## Final Pass

Run this checklist after drafting is complete but before delivery or format
conversion. Every item must pass. If any item fails, fix it in the Markdown
draft and re-run the pass. Do not convert to the target format until the pass
is clean.

1. **Significance** — no unsupported significance, legacy, or trend claims
   remain
2. **Promotional** — no promotional phrasing remains unless quoted or
   explicitly attributed
3. **Dead weight** — no sentence remains only because it sounds polished or
   complete
4. **Source fidelity** — no source says less than the prose claims it says
5. **Diminish-to-elevate** — no contrast formula remains in any form: not the
   listed patterns, not paraphrases of them, not any construction that elevates
   Y by first diminishing X. Scan for `not just`, `more than`, `beyond`,
   `went further`, `exceeded`, `was not limited to`, `not only`, and similar
   rhetorical moves. If the underlying move survives under different words, the
   check fails.
6. **Fourth wall** — no purposeless references to the report, document, guide,
   or section remain
7. **Em dash** — no U+2014 dash remains outside the narrow allowed cases
8. **Residue** — no placeholders, chatbot artifacts, or stale knowledge
   disclaimers remain
9. **Structure** — formatting serves the reader instead of advertising structure
10. **Unknowns** — known unknowns are stated plainly instead of filled with
    speculation
11. **Format gate** — if the target format is not Markdown, confirm the
    Markdown draft is clean before converting. Do not fix quality issues inside
    the target format; fix them in Markdown and reconvert.
