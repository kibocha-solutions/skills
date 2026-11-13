# Walkthrough

## 2026-11-13 17:30

- Finding: the AGENTS.md pushed in commit 805d514 was a 1,482-word compression of a 2,787-word committed file. It dropped detailed rules and broke the cross-references `AGENTS.md §9.11`, `§9.12`, and `§9.2-9.12` used by other skills.
- Decision from the user: restore every rule, raise the AGENTS.md limit to 2,500 words, and update skill-creator accordingly.
- Baseline: `tools/validate-all.sh` fails with 15 errors before this task (em dash in the required attachment phrase, research documents under ci-cd, and communications files).
- Archived the previous session to `sessions/archive/`.

## 2026-11-13 17:46

- Rebuilt `AGENTS.md` (2,479 words, under the 2,500-word limit), restoring `cdc8647` §§3–11 rules/cross-references (`§9.2`–`§9.14`), keeping `§10` percentage-free, and adding `§12. Communicating with the user`, `§13. Situational awareness and continuity`, and `§14. Pre-completion checklist`.
- Updated `skill-creator/references/skill-authoring-standard.md` and `tools/validate-all.sh` to enforce the 2,500-word limit.
- Updated `coordinator` (`SKILL.md`, `references/heartbeat-and-wake.md`, `assets/heartbeat-prompts.md`, `references/contracts.md`, `references/delegation.md`, `examples/coordination.md`, `evals/evals.json`) with parent question routing, self-contained Section 12 escalations, 95% 5h / 98% weekly thresholds, 30-min active / 90-min blocked heartbeat, post-reset wake timer with strict mutual exclusion, exact Maestro + `.agents/brain/handoffs/` persistence, and unavailable-capability reporting.
- Validation: `/usr/bin/python3 skill-creator/scripts/quick_validate.py coordinator` -> `Skill is valid!`; `bash tools/validate-all.sh` -> 15 pre-existing baseline errors, zero new errors.
- Paired evals (evals 18–21): `with_skill` passed 12/12 expectations (100%) vs `without_skill` snapshot 2/12 (16.7%); benchmark generated at `/tmp/coordinator-workspace/iteration-1/benchmark.json`.
