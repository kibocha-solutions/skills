# Implementation Plan: Coordinator Heartbeat, Wake Timer, Escalation Rules, and AGENTS.md Restoration

## Objective

Deliver to the user a coordinator skill and an AGENTS.md that together (1) state the 95% (5-hour) and 98% (weekly) usage thresholds, (2) route every worker question to its parent, (3) require self-contained reports and questions, (4) require user notification when timers, wakes, or usage checks are unavailable, (5) define the heartbeat and wake-timer procedure with mutual exclusion and persistent state, and (6) restore every rule that the previous compression removed from AGENTS.md, within a 2,500-word limit.

## Acceptance criteria

1. `AGENTS.md` contains every rule of the committed version `cdc8647` in its original section and item numbering for sections 3 to 11, with the usage-percentage thresholds absent, and the elevated sections 1 and 2 retained.
2. `AGENTS.md` is below 2,500 words and `tools/validate-all.sh` reports no AGENTS.md error.
3. `AGENTS.md` contains a user-communication section requiring self-contained, non-summary reports, questions, status updates, and intervention requests with the seven required elements.
4. `AGENTS.md` requires graph-based repository orientation, periodic persistence of state, and user notification when a needed capability is unavailable.
5. `skill-creator/references/skill-authoring-standard.md` and `tools/validate-all.sh` state the 2,500-word limit.
6. `coordinator/SKILL.md` states the thresholds, the parent-routing rule for worker questions, the unavailable-capability notification, and routes to the heartbeat reference.
7. `coordinator/references/heartbeat-and-wake.md` defines capability inventory, heartbeat, blocked heartbeat, wake timer, mutual exclusion, and persistence with exact steps.
8. `coordinator/assets/heartbeat-prompts.md` holds the exact prompts for the heartbeat, blocked heartbeat, and wake resume.
9. `coordinator/examples/coordination.md` shows contrasting good and bad practice for each new rule.
10. `coordinator/evals/evals.json` contains falsifiable cases for each new rule and the paired evaluation results are recorded.
11. `tools/validate-all.sh` reports no new error from the changed files, all JSON parses, and no AGENTS.md section cross-reference elsewhere in the repository is broken.
12. The change is committed as one signed commit, pushed, and every host mirror and instruction file is realigned.

## Proposed changes

- [MODIFY] `AGENTS.md`
- [MODIFY] `skill-creator/references/skill-authoring-standard.md`
- [MODIFY] `tools/validate-all.sh`
- [MODIFY] `coordinator/SKILL.md`
- [MODIFY] `coordinator/references/contracts.md`
- [MODIFY] `coordinator/references/delegation.md`
- [MODIFY] `coordinator/examples/coordination.md`
- [MODIFY] `coordinator/evals/evals.json`
- [NEW] `coordinator/references/heartbeat-and-wake.md`
- [NEW] `coordinator/assets/heartbeat-prompts.md`
- [NEW] `.agents/memory/agents-md-limits-and-cross-references.md`
- [MODIFY] `.agents/MEMORY.md`

## Blocking questions

None. The user decided on 2026-11-13 to restore all rules and raise the AGENTS.md limit to 2,500 words.

## Verification

1. Diff the rules of `cdc8647` against the new AGENTS.md section by section.
2. Run `bash tools/validate-all.sh` and compare with the baseline of 15 existing errors.
3. Run `skill-creator/scripts/quick_validate.py` on `coordinator`.
4. Run paired evaluations for the new cases with the new skill and the snapshot of the old skill; grade and aggregate.
5. Re-read every changed file in full.
6. Verify the commit signature, the push, and the host alignment.
