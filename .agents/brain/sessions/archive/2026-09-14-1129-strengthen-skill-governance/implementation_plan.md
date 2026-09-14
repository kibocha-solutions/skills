# Implementation Plan: strengthen skill governance

## Objective

Rebuild the repository instruction architecture so `AGENTS.md` is an
unmistakably binding universal authority, skill use follows a repeatable
read-act-check-reread procedure, tool installation supports quality work, the
CI/CD attribution prohibition is absolute, and skill-authoring procedure lives
inside the `skill-creator` package.

## Acceptance criteria

1. The exact former PBO `RULES.md` is read in full and each rule is reassessed
   for a universal form before any governance rewrite.
2. Universal rules are stated directly in `AGENTS.md`; mechanics and examples
   are routed to the applicable skill or reference.
3. `AGENTS.md` contains an early, numbered skill-use protocol requiring full
   reads before action, checklist tracking during work, rereads when the task
   reaches a skill-governed phase, and final verification against the skill.
4. `AGENTS.md` states its project-level authority without claiming power over
   non-waivable runtime safety or law.
5. Safe, task-relevant tool installation may proceed without a separate
   permission request when omission would reduce quality or compliance; a
   privilege failure routes immediately to the user with the exact command.
6. The CI/CD skill prohibits AI attribution in commits, pull requests, release
   notes, and other repository work product.
7. The standalone skill-authoring guide is moved into the `skill-creator`
   package and every route to it resolves.
8. Full contextual reads and automated repository validation pass against the
   final artifacts.

## Files

- [MODIFY] `AGENTS.md`
- [MODIFY] `skill-creator/SKILL.md`
- [MOVE] `docs/SKILL_AUTHORING_GUIDE.md`
- [MODIFY] `ci-cd/SKILL.md` or its routed reference
- [MODIFY] relevant skill references selected after the 24-rule reassessment
- [MODIFY] `tools/validate-all.sh` if the move requires validator coverage

## Verification

1. Read each affected instruction file in full before and after editing.
2. Maintain a 24-rule universalization register with exact destinations.
3. Check instruction precedence, installation boundaries, and attribution
   wording manually.
4. Run `tools/validate-all.sh`.
5. Run `git diff --check` and inspect the scoped diff.
