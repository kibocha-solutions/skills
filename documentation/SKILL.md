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

Reduce `not just X, but Y` style contrast formulas. Use a direct positive
sentence unless the contrast is necessary for accuracy.

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
3. Apply these transformations across the draft:
   - tighten wordy but valid text
   - attribute interpretive claims when a source supports them
   - replace vague claims with concrete facts, steps, constraints, or explicit
     unknowns
   - remove sentences that do not narrow, contextualize, instruct, verify, warn,
     or connect
   - remove unsupported significance claims, decorative contrast, and
     unverifiable fluff
   - preserve text that is already clear, factual, and human-written
4. Verify citations and links for claims that depend on external evidence when
   browsing, local source files, or accessible references are available. If a
   source cannot be accessed, do not invent verification. Preserve plausible
   URLs, but flag high-risk claims for user verification.
5. Normalize headings, lists, emphasis, tables, and code fences.
6. Re-read the result for a human documentation voice: direct, grounded, and
   free of ornamental certainty.

## Final Pass

Before handing off documentation, confirm:

- no unsupported significance, legacy, or trend claims remain
- no promotional phrasing remains unless quoted or explicitly attributed
- no sentence remains only because it sounds polished or complete
- no source says less than the prose claims it says
- no unnecessary `not just X, but Y` contrast pattern remains
- no purposeless references to the report, document, guide, or section remain
- no U+2014 dash remains outside the narrow allowed cases
- no placeholders, chatbot artifacts, or stale knowledge disclaimers remain
- formatting serves the reader instead of advertising structure
- known unknowns are stated plainly instead of filled with speculation
