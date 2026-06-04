# Handoff: technical documentation library

## Datetime

2026-06-05 00:10 EAT

## Current objective

Expand the `documentation` skill so agents can create, place, audit, and
validate technical documentation using a predictable Writerside-oriented project
documentation library.

## State of the repo

The documentation skill now has additive technical-documentation guidance on
top of the existing general writing rules and code-comment documentation work.
The new guidance distills `sources/reports/documentation-reference.md` into a
runtime reference instead of copying the source report wholesale.

Separate pre-existing staged work remains present:

- `.gitmodules`
- `sources/anthropic-skills`

Separate pre-existing untracked or modified documentation-comment work remains
present and was not reverted.

## Decisions made

- Keep `docs/` as the default documentation source boundary for application
  repositories. If the whole repository is documentation-only, a project may use
  a root-level equivalent.
- Treat Writerside instances as audience outputs, not source folders.
- Use default Writerside tree files named `public.tree`, `internal.tree`,
  `restricted.tree`, `confidential.tree`, and `shared-library.tree`.
- Keep source folders semantic and reusable across instances:
  `product/`, `planning/`, `architecture/`, `domain/`, `data/`, `security/`,
  `api/`, `engineering/`, `testing/`, `operations/`, `user-guides/`,
  `releases/`, and `diagrams/`.
- Make entity relationships explicit through
  `docs/domain/entity-relationship-model.md` and matching diagram assets.
- Keep production diagram generation in the `technical-diagrams` skill. The
  documentation skill links to final SVGs and expects editable `.drawio`
  sources to be preserved.
- Add a small deterministic checker for required starting technical docs.
- Keep quick-reference tree assets self-contained by including each path's
  confidentiality ladder placement.
- Use Markdown table assets for technical documentation trees because they are
  meant to be scanned by agents and humans.
- Resolved the technical-documentation routing `TBD` entries with compact
  document-family references instead of creating separate skills.
- Added templates only where output shape is fragile or repeatedly needed:
  ADRs, SRE runbooks, threat models, and changelogs.

## Files changed

- `documentation/SKILL.md`: adds a specific technical documentation workflow
  that routes through the new library reference, local source reports, online
  authoritative sources, Writerside instance choice, and diagram handoff.
- `documentation/references/technical-documentation-routing.md`: routes
  technical-library structure and placement tasks to the new reference.
- `documentation/references/writerside-technical-documentation.md`: aligns the
  Writerside project shape with the new docs library model and audience tree
  files.
- `documentation/references/technical-documentation-library.md`: adds the
  default source tree, Writerside instance logic, required starting docs,
  lifecycle triggers, additional documentation catalogue, workflow, and
  placement checklist.
- `documentation/assets/technical-docs-required-tree.md`: adds a reusable
  required starting tree shell with confidentiality ladder placement.
- `documentation/assets/technical-docs-optional-tree.md`: adds optional and
  trigger-based documentation paths with confidentiality ladder placement and
  trigger notes.
- `sources/reports/signs-of-ai-writing.md`: cleaned the source report into a
  Markdown file, removing copied page chrome and improving headings and spacing.
- `documentation/scripts/check_technical_docs_tree.py`: adds a deterministic
  checker for missing required starting docs.
- `documentation/references/technical-architecture-documentation.md`: adds
  architecture overview and C4 documentation guidance.
- `documentation/references/adr-documentation.md`: adds ADR workflow and
  validation guidance.
- `documentation/references/api-documentation.md`: adds REST, GraphQL, gRPC,
  internal API, SDK, and integration guidance.
- `documentation/references/deployment-documentation.md`: adds deployment,
  infrastructure, CI/CD, and environment guidance.
- `documentation/references/documentation-deployment.md`: adds Writerside docs
  build, publish, and redirect guidance.
- `documentation/references/operations-runbook-documentation.md`: adds
  operations, incident response, monitoring, backup, and runbook guidance.
- `documentation/references/database-documentation.md`: adds schema,
  migrations, data dictionary, ERD, backup, and recovery guidance.
- `documentation/references/security-documentation.md`: adds baseline, access,
  threat model, privacy, and data-handling guidance.
- `documentation/references/configuration-documentation.md`: adds environment,
  secret, and feature-flag documentation guidance.
- `documentation/references/testing-documentation.md`: adds strategy, plans,
  cases, and test-data guidance.
- `documentation/references/user-guide-documentation.md`: adds user, admin,
  onboarding, tutorial, FAQ, troubleshooting, and support guidance.
- `documentation/references/changelog-documentation.md`: adds changelog,
  release-note, migration-note, and upgrade-guide guidance.
- `documentation/references/access-level-classification.md`: adds standalone
  confidentiality ladder and placement rules.
- `documentation/assets/madr-adr-template.md`: adds a reusable ADR shell.
- `documentation/assets/sre-runbook-template.md`: adds a reusable runbook shell.
- `documentation/assets/owasp-threat-model-template.md`: adds a reusable threat
  model shell.
- `documentation/assets/keep-a-changelog-template.md`: adds a reusable
  changelog shell.

## Open questions

- Should `confidential.tree` be required by the checker or remain optional until
  a project has genuinely confidential documentation?
- Should the checker later validate Writerside tree inclusion and sensitivity
  metadata, not just file presence?
- Should additional templates be added for API references, database schemas,
  test plans, and user guides, or are references sufficient for now?

## Next entry point

1. Review the new technical documentation library reference for path names and
   required starting docs.
2. Review whether the compact document-family references are sufficiently
   specific in live use.
3. Consider adding templates for API references, database schemas, test plans,
   user guides, and Writerside starting pages under `documentation/assets/`.

## Constraints

- Treat `sources/` as source material, not active skill guidance.
- Do not copy source reports wholesale into skill references.
- Keep `SKILL.md` concise and procedural; keep detailed technical-doc policy in
  `documentation/references/`.
- Do not merge diagram generation back into the documentation skill.
- Do not delete existing handoff documents unless the user explicitly requests
  it.
