# Handoff: CI/CD Skill And Instruction Cleanup

## Datetime

2026-06-08 15:45 EAT

## Current objective

Replace competing instruction bundles in the skills repo with one active
`AGENTS.md` policy layer and a new first-class `ci-cd` skill.

## State of the repo

The skills repo now has:

- a revised `.agents/skills/AGENTS.md` with commit-creation rules, skill
  routing, and sandboxed Git guidance;
- a new top-level `.agents/skills/ci-cd/` skill with Git, commit cleanup,
  pipeline, deployment, rollback, and GitHub Actions security guidance;
- a trimmed `sources/project-references/README.md` that treats
  `project-references` as source material, not as a second instruction
  authority.

The old `07-project-wide-instructions/` content is being removed because its
parallel AGENTS, Copilot, and Cursor overlays were stale and conflicting.

## Decisions made

- Keep `documentation` prevalent for docs-facing work, including CI/CD
  documentation.
- Keep durable commit-policy rules in `AGENTS.md`.
- Move heavier workflow guidance into the `ci-cd` skill.
- Treat one meaningful final commit per coherent change as the default history
  goal.
- Allow temporary local fixup commits, but require cleanup before publishing or
  history handoff.
- Default to autonomous cleanup when branch history is local, procedural, and
  clearly compressible into one coherent final change.
- Require branch-state continuity in handoffs whenever branch purpose, cleanup
  state, or rebase risk matters.
- Remove project-reference instruction overlays rather than trying to maintain
  several parallel agent authorities.

## Files changed

- `.agents/skills/AGENTS.md`: clarified active repo rules, skill routing, and
  commit workflow.
- `.agents/skills/ci-cd/SKILL.md`: added a comprehensive CI/CD skill.
- `.agents/skills/ci-cd/references/`: added Git/history, pipeline/deployment,
  and security/operations references.
- `.agents/skills/ci-cd/assets/commit-message-template.md`: added a compact
  commit template.
- `.agents/skills/sources/project-references/README.md`: removed claims that
  project references are the active instruction authority.

## Open questions

- Whether the `ci-cd` skill should later gain scripts, evals, and benchmark
  coverage through the full `skill-creator` loop.
- Whether the `ci-cd` skill should also absorb repository-signing guidance if
  that becomes a recurring workflow in this skills repo.

## Next entry point

1. Verify the deleted instruction overlay files are fully gone from
   `sources/project-references/07-project-wide-instructions/`.
2. Review the new `ci-cd` skill for any repo-specific gaps before running a
   fuller skill-evaluation loop.

## Constraints

- Keep `documentation` as the primary route for documentation artifacts.
- Do not reintroduce secondary AGENTS, Copilot, or Cursor instruction overlays
  under `project-references`.
- Keep commit-history advice focused on useful final history rather than noisy
  procedural trails.
