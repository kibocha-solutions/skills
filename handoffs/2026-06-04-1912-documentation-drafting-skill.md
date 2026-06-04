# Handoff: documentation drafting skill

## Datetime

2026-06-04 19:12 EAT

## Current objective

Build the first real skill in the repository: `documentation-drafting`. The skill should guide agents in drafting, rewriting, and reviewing documentation, with strong rules for weak AI-patterned writing, Writerside technical documentation, and professional code comment documentation.

## State of the repo

The `documentation-drafting/` skill now exists and has been committed and pushed on branch `feat/docs`.

Latest pushed commit:

```text
9cc3a26 feat(documentation-drafting): add Writerside documentation skill
```

The branch now tracks `origin/feat/docs`.

Current working tree note: `sources/reports/signs-of-ai-writing.txt` remains untracked. It was intentionally not staged or committed because it pre-existed this final commit scope and is source material.

## Decisions made

- Keep `documentation-drafting` as the single skill for general documentation, technical documentation, Writerside output, and code comment documentation for now.
- Keep `SKILL.md` concise and procedural. Detailed guidance lives in `documentation-drafting/references/`.
- Use Writerside-compatible Markdown for all new software or systems technical documentation.
- Do not route active skill behavior back to `sources/project-references/`. Those files are legacy source material to migrate from, not runtime guidance.
- Use `TBD: references/...` entries in `technical-documentation-routing.md` for technical doc types that still need migration.
- Treat weak AI-patterned writing as a quality issue due for improvement, not as proof of authorship.
- Do not create scripts yet. Current guidance is procedural and judgment-based; deterministic validation can come later.
- Use official Writerside documentation as source material through distilled references and links, not by copying the full docs into the repo.

## Files changed

- `AGENTS.md`: added rules for Writerside technical documentation and code comment documentation.
- `documentation-drafting/SKILL.md`: added the main skill with routing to Writerside, technical documentation, comment documentation, and weak-pattern cleanup references.
- `documentation-drafting/references/weak-ai-writing-patterns.md`: distilled weak AI-patterned writing checks from the source report.
- `documentation-drafting/references/technical-documentation-routing.md`: routes technical doc types to migrated references, using `TBD` placeholders for content not yet migrated.
- `documentation-drafting/references/writerside-technical-documentation.md`: distilled Writerside guidance from official JetBrains docs.
- `documentation-drafting/references/code-comment-documentation.md`: added package/module/file/class/function/line-level comment documentation guidance.

## Open questions

- Which `TBD` technical documentation reference should be migrated first?
- Should access-level classification become its own migrated reference next?
- Should a later validation script check Writerside topic references, tree inclusion, U+2014 dash usage, placeholder residue, and comment freshness?
- Should `sources/reports/signs-of-ai-writing.txt` be committed as source material, ignored, or left untracked?

## Next entry point

1. Review `documentation-drafting/references/technical-documentation-routing.md` and choose the first `TBD` reference to migrate.
2. Migrate one technical documentation type at a time from `sources/project-references/01-technical-documentation/`, distilling reusable rules into `documentation-drafting/references/`.
3. Keep `SKILL.md` lean; update it only when a new reference needs to be routed from the always-loaded skill.
4. Decide what to do with untracked `sources/reports/signs-of-ai-writing.txt`.

## Constraints

- Do not delete `sources/` or handoff documents unless the user explicitly asks.
- Treat `sources/` as source material, not as active skill guidance.
- Do not copy source material wholesale; distill reusable procedures, templates, and constraints.
- New technical documentation guidance should target Writerside-compatible Markdown only.
- Do not recreate root `00-project-references/`.
- Keep future technical documentation migrations in `references/`, not in `SKILL.md`, unless the rule must always be loaded.
