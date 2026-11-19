# Tasks: Clarify Maestro and Coordinator Terminology
## State: DONE (Clarified exclusive Maestro session/archive and Coordinator worker/chat definitions)
## Phase 1: Update Maestro Files
- [x] Update `maestro/SKILL.md`, `maestro/references/session-lifecycle.md`, `maestro/examples/session-lifecycle-and-recovery.md`, and `maestro/evals/evals.json`

## Phase 2: Update Coordinator Files
- [x] Update `coordinator/SKILL.md`, `coordinator/references/delegation.md`, `coordinator/references/heartbeat-and-wake.md`, `coordinator/references/task-ids.md`, `coordinator/assets/heartbeat-prompts.md`, `coordinator/examples/coordination.md`, and `coordinator/evals/evals.json`

## Phase 3: Verify and Close
- [x] Read all 11 modified files in full, run terminology sweep, `quick_validate.py`, `tools/validate-all.sh`, JSON syntax check, `git diff --check`, and `steward.py check`
- [x] Update `walkthrough.md` and close/archive Maestro session as `DONE`
