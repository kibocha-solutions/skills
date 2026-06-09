# Handoff: AGENTS.md compression

## Datetime

2026-06-08 22:13 EAT

## Current objective

Trim the skills repo `AGENTS.md` into a compact governing file, move durable
authoring rules into docs, and add an anti-bloat reminder to the skill-creator
skill.

## State of the repo

The active skills repo guidance now treats `AGENTS.md` as current-repo
governance rather than a long operating manual. The file has been rewritten to
use a short reusable baseline plus repo-specific rules. The placeholder
`docs/SKILL_AUTHORING_GUIDE.md` has been replaced with a real house standard.
The `skill-creator` skill now reminds future agents to keep `AGENTS.md`
compact and to offload heavy procedure into skills and docs.

## Decisions made

- Keep reusable `AGENTS.md` baseline guidance around 200-300 tokens.
- Enforce a hard `AGENTS.md` ceiling of 1500 words.
- Keep `AGENTS.md` limited to repo governance: scope, routing, safety,
  edit-permission, privacy, and continuity rules.
- Push workflow detail, templates, examples, and deep procedure into skills,
  `references/`, `assets/`, or docs.
- Make `docs/SKILL_AUTHORING_GUIDE.md` the canonical standard for deciding
  what belongs in `AGENTS.md` versus `SKILL.md`.

## Files changed

- `AGENTS.md`: replaced long procedural sections with a compact baseline and
  repo-specific governance rules.
- `docs/SKILL_AUTHORING_GUIDE.md`: added the house standard for repo roles,
  `AGENTS.md` length budget, and offloading rules.
- `skill-creator/SKILL.md`: added an operational reminder to prevent future
  `AGENTS.md` bloat.

## Branch state

- Current branch: detached or not reported
- Intended base branch: not established in this session
- Branch purpose: skills-repo governance cleanup
- History cleaned yet: not applicable
- Procedural commits since branch-off: not applicable
- Safe next Git action: review the three changed files in the skills repo and
  keep them separate from unrelated migration work

## Open questions

- Whether the repo should later add a dedicated reusable `AGENTS.md` example in
  `docs/examples/`.

## Next entry point

1. Review the compressed `AGENTS.md` against the desired house tone.
2. If accepted, use `SKILL_AUTHORING_GUIDE.md` as the reference when revising
   other governance docs or creating future skills-repo `AGENTS.md` files.

## Constraints

- Do not re-expand `AGENTS.md` with workflow detail already owned by a skill.
- Keep the reusable baseline short enough that repo-specific rules remain the
  main payload.
- Do not disturb the unrelated in-progress migration changes already present in
  the skills repo worktree.
