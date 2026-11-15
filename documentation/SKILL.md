---
name: documentation
description: Draft, review, rewrite, and validate documentation, README files, guides, procedures, policies, proposals, reports, correspondence, reference pages, Writerside technical documentation, API prose, docstrings, and code comments. Use for documentation structure, source fidelity, citation cleanup, and documentation quality control. Route sentence-level prose quality to human-writer, legal instruments to legalese, and production diagrams to technical-diagrams.
---

# Documentation

## 1. Route the task

1. Identify the audience, document type, reader task, access level, source
   format, and delivery format.
2. Apply the user's template and document-specific instructions.
3. Route constitutions, charters, contracts, and legal clauses through
   `legalese/SKILL.md`.
4. Route production diagrams and SVG exports through
   `technical-diagrams/SKILL.md`.
5. Route correspondence through `communications/SKILL.md`.
6. Read `references/ngo-and-donor-narrative.md` for proposals and calls for
   proposals.
7. Read `references/code-comment-documentation.md` for docstrings, API
   comments, and implementation comments.
8. Read `references/screenshot-standards.md` before capturing or placing a
   screenshot.
9. Read `references/letterhead-and-pagination.md` before producing or
   reviewing fixed-page documents.
10. Read `references/cso-document-rules.md` for documentation work in CSOs.

## 2. Gather sources

1. Read the existing artifact from start to finish.
2. Read every supplied source required by the requested scope.
3. Gather the current code, schema, configuration, tests, durable
   documentation, and external authorities that control the content.
4. Verify external facts against primary or authoritative sources.
5. Mark unresolved facts in working notes and tell the user in chat.
6. Keep plans, sessions, memory, handoffs, chat history, temporary files, and
   skill instructions out of published source citations.
7. Preserve user-supplied and expressly locked wording. Propose a change to
   that wording in chat before applying it. Treat other source wording as
   editable.
8. Record the source controlling each claim, command, field, state, and figure.

## 3. Select the structure

### Policy or procedure

1. Put motivation and rationale in `Purpose` and `Scope`.
2. Write numbered operational sections as direct rules or role-attributed
   steps.
3. Select the modal register by instrument class as defined in AGENTS.md §9.2. Use the imperative mood for procedure steps. Route legal instruments to `legalese/SKILL.md`.
4. Put violations and enforcement in a dedicated section.
5. State each rule, definition, and constraint once.

### Proposal or call response

1. Put explanatory context in `Background` or `Needs`.
2. Put outcomes in `Approach`, `Objectives`, or `Solution`.
3. Use first-person plural and forward-looking language.
4. Use paragraphs and tables for narrative content.
5. Name sources in prose.
6. Add a bibliography only when the controlling instructions require one.
7. Follow `references/ngo-and-donor-narrative.md`.

### Memo or correspondence

1. Confirm the audience classification.
2. Apply the external register until the user confirms an internal audience.
3. Move from context to the requested action.
4. Use polite direct address.
5. Apply the declaratory register (AGENTS.md §9.2): simple present for a stated position or present fact, past tense for a completed event, and `will` for a future event.
6. Do not use command modals such as `shall` or `must`.
7. Follow `communications/SKILL.md`.

### Technical documentation

1. Write for a careful new contributor unless the repository specifies another
   audience.
2. Read the following routing references:
   1. `references/technical-documentation-routing.md`
   2. `references/technical-documentation-library.md`
   3. `references/writerside-technical-documentation.md`
3. Read the matching document-family reference:
   1. architecture: `references/technical-architecture-documentation.md`
   2. ADR: `references/adr-documentation.md`
   3. API: `references/api-documentation.md`
   4. deployment: `references/deployment-documentation.md`
   5. documentation delivery: `references/documentation-deployment.md`
   6. operations: `references/operations-runbook-documentation.md`
   7. database: `references/database-documentation.md`
   8. security: `references/security-documentation.md`
   9. configuration: `references/configuration-documentation.md`
   10. testing: `references/testing-documentation.md`
   11. user guide: `references/user-guide-documentation.md`
   12. changelog: `references/changelog-documentation.md`
4. Use `references/access-level-classification.md` for audience classification.
5. Give each independently meaningful contract, schema, state model, interface,
   lifecycle, or responsibility its own focused page.
6. Put orientation and relationship summaries on overview pages.
7. Include the subject, direct dependencies, and direct dependents in a
   page-level diagram.
8. Keep field, parameter, and state detail on the focused subject page.

## 4. Place technical documentation

1. Use the repository's existing documentation structure.
2. Use `docs/` when no durable structure exists.
3. Select the target path through
   `references/technical-documentation-library.md`.
4. Use these assets for a new library:
   1. `assets/technical-docs-required-tree.md`
   2. `assets/technical-docs-optional-tree.md`
5. Select the Writerside tree for the intended audience.
6. Include each topic in the correct tree.
7. Keep reusable snippets in the snippet library.
8. Keep editable diagram sources with their exported documentation assets.

## 5. Enforce deliverable boundaries

1. Apply `AGENTS.md` Sections 9.5 to 9.7 to every deliverable: no progress markers, workflow notes, sample labels, hedging, uncertainty markers, unprompted details, or sensitive identifiers.
2. Inspect existing repository documents for prerequisite instruments before drafting; if one is missing, stop and ask the user in chat.
3. Withhold financial amounts beyond those requested and compliance-status detail unless an authoritative form field requires them or the user explicitly directs disclosure.
4. Treat a funder's eligibility statement as a condition to satisfy, not as a request for an identifier or certificate.

## 6. Draft in Markdown

1. Draft or rewrite in Markdown before converting to another format.
2. Apply `human-writer/SKILL.md` for sentence-level prose quality, including its weak writing pattern checks.
3. Keep facts, recommendations, constraints, and unknowns distinct.
4. Remove malformed markup, tracking parameters, citation residue, and broken references.
5. Use headings, lists, tables, emphasis, and code fences only when they
   improve retrieval or execution.
6. Apply the list rules of `AGENTS.md` §9.11 and the definition rule of §9.3 to instruments.
7. Use prose and tables for narrative or persuasive documents.
8. Use Writerside components where the repository convention requires them.

## 7. Verify content

1. Re-read the complete Markdown draft as the intended reader.
2. Check every claim against its controlling source.
3. Check every citation and link.
4. Check names, dates, identifiers, figures, units, commands, fields, states,
   and cross-references.
5. Check register, tense, mood, and voice.
6. Check that each section owns its rules and definitions.
7. Check that metadata contains structured values only.
8. Check that the deliverable contains no progress notes, self-disclaimers,
   sample labels, compliance narration, uncertainty markers, hedging,
   unprompted sensitive identifiers, or AI attribution.
9. Check that an external deliverable, such as a proposal, correspondence, or
   filed record, references other documents by title only and contains no
   internal paths. Check that a documentation-library topic links other topics
   by relative path and never references a higher-sensitivity topic.
10. Correct every defect in the Markdown source.
11. Repeat the full read after each correction pass.

## 8. Convert and validate

1. Convert only after the Markdown source passes.
2. Regenerate the output after every source change.
3. Never patch a generated Word or PDF file directly.
4. Run the artifact-specific validator, tests, linter, schema check, or build.
5. Run `wrs doctor` before a Writerside build.
6. Read `references/install-writerside.md` when the Writerside toolchain is
   unavailable, and before building or serving Writerside output.
7. Build every affected Writerside instance with `wrs build` when Podman or
   Docker and the builder image are reachable. Inspect
   `examples/writerside-validation.md` for build and serve reporting.
8. Treat every nonzero validation or build status as failure.
9. Report exact errors and log paths in chat.

## 9. Inspect the final artifact

1. Open the exact final artifact.
2. Read it from start to finish.
3. Render every fixed-layout page, slide, sheet, screen, or image. Serve
   Writerside output with `wrs serve` and open each changed topic. Serve gated
   instances with `wrs serve --dev`; leave the password manager sign-in to the
   user.
4. Inspect every rendered output visually.
5. Check page flow, tables, images, headers, footers, numbering, continuation
   pages, links, and final-page layout.
6. Check the last page of each table and the page after each front-matter,
   section, or letterhead transition.
7. Rebuild and repeat all checks after any correction.
8. Deliver only the final verified artifact.

## 10. Pre-completion checklist

Before delivering any documentation artifact, confirm evidence exists for each item:

- [ ] Source documents and existing artifacts read manually in full from start to finish.
- [ ] Motivation and rationale kept in Purpose and Scope; operative sections state direct rules or role-attributed steps only.
- [ ] Deliverables free of progress markers, workflow notes, sample labels, and self-disclaimers.
- [ ] Deliverables free of uncertainty markers and quantity hedging.
- [ ] No unprompted sensitive identifiers, background methodology explanations, or donor context explanations included.
- [ ] Doubts, concerns, and missing prerequisites raised directly to the user in chat before writing.
- [ ] External deliverables reference documents by title only, with no internal repository paths, session filenames, memory files, or handoffs; documentation-library topics link by relative path and never reference a higher-sensitivity topic.
- [ ] Zero AI attribution across all documents, deliverables, and metadata.
- [ ] No U+2014 em dashes in normal prose, except when introducing a list.
- [ ] Derived deliverables regenerated from clean sources after the final edit and visually verified.
- [ ] All links, code symbols, commands, and cross-references verified against controlling code or authoritative sources.


