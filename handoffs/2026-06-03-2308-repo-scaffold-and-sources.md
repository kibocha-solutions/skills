# Handoff: repo scaffold and sources

## Datetime

2026-06-03 23:08 EAT

## Current objective

Build a personal agent skills repository progressively, starting with the documentation skill. The next conversation should begin documentation structuring and research, especially around JetBrains Writerside-compatible documentation and the first `documentation-drafting` skill.

## State of the repo

The repository scaffold exists, but most files are placeholders. The repo-level structure now includes governance files, docs placeholders, tool placeholders, GitHub workflow placeholders, `sources/`, and an empty `documentation-drafting/` directory.

The legacy `00-project-references` submodule has been retired from the root. A fresh clone of `kibocha-solutions/00-project-references.git` was placed under `sources/project-references/` and converted into plain source material by removing its nested `.git` directory.

The skills research report was cleaned of exported citation markers, then moved and renamed to `sources/reports/skills-repository-reference.md`.

## Decisions made

- Use `sources/` for upstream/reference material that guides skill creation but is not itself part of the active skills surface.
- Add `sources/README.md` to clarify that agents must not delete `sources/` or its contents unless the user explicitly requests it.
- Retire the old root-level `00-project-references` submodule so future work focuses on updating skills, not maintaining the old reference repo.
- Store continuity notes in `handoffs/` using timestamped files, because multiple handoffs may happen on the same day.
- Use `documentation-drafting/` as the first skill shell, but keep it empty until further instructions.
- Treat JetBrains Writerside compatibility as the default target for documentation output, not plain generic Markdown.
- Use the Wikipedia “Signs of AI writing” PDF as source context for documentation style guardrails: avoid generic importance claims, unsupported synthesis, promotional tone, placeholders, citation artifacts, malformed markup, and over-formatted AI residue.

## Files changed

- `README.md`: added initial repo overview placeholder.
- `AGENTS.md`: added contributor rules, Writerside default note, source-material rule, and handoff policy/template.
- `LICENSE.txt`: added placeholder noting license is undecided.
- `migration-log.md`: added empty migration log table.
- `docs/`: added placeholder authoring, portability, privacy, review checklist, and examples files.
- `.github/`: added placeholder PR template and placeholder workflows.
- `tools/`: added placeholder scaffold and validation scripts.
- `documentation-drafting/`: created empty directory; no files inside yet, so Git will not track it until content is added.
- `sources/README.md`: added source-material rules.
- `sources/project-references/`: added plain-file copy of the cloned reference repo.
- `sources/reports/skills-repository-reference.md`: added cleaned and renamed skills research report.
- `.gitmodules`: removed with the old submodule.
- `00-project-references/`: removed from the root.

## Open questions

- What exact Writerside conventions should the documentation skill enforce beyond the basics already researched?
- Should the first documentation skill be named `documentation-drafting`, `documentation`, or something else?
- Which source files under `sources/project-references/01-technical-documentation/` should be distilled first?
- Should `documentation-drafting/` begin with only `SKILL.md`, or should it immediately include `references/` and `assets/` folders?

## Next entry point

1. Read `AGENTS.md`.
2. Read this handoff.
3. Inspect `sources/reports/skills-repository-reference.md` for the documented skill layout and authoring principles.
4. Inspect Writerside official docs as needed before encoding Writerside-specific guidance.
5. Inspect `sources/project-references/01-technical-documentation/` and relevant core canons to decide the first documentation skill structure.
6. Create the first real contents for `documentation-drafting/` only after the user gives the next instruction.

## Constraints

- Do not delete `sources/` or handoff documents unless the user explicitly asks.
- Do not recreate `00-project-references/` at the root.
- Do not create the other skill folders yet unless the user asks.
- Keep migrated skill content reusable and sanitized; do not copy old source material wholesale.
- Prefer Writerside-compatible documentation conventions for documentation outputs unless the user requests another format.
