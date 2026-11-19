# Implementation Plan: Clarify Maestro and Coordinator Terminology

## Objective
Clarify `maestro` and `coordinator` definitions so `session` and `archive` refer exclusively to Maestro sessions under `.agents/brain/sessions/` and conversations controlled by `coordinator` are referred to as `workers` or `chats` (stopped, closed, or deleted, never archived).

## Acceptance Criteria
1. `maestro/SKILL.md`, `maestro/references/session-lifecycle.md`, `maestro/examples/session-lifecycle-and-recovery.md`, and `maestro/evals/evals.json` define `session` and `archive` exclusively for Maestro sessions under `.agents/brain/sessions/`.
2. `coordinator/SKILL.md`, `coordinator/references/delegation.md`, `coordinator/references/heartbeat-and-wake.md`, `coordinator/references/task-ids.md`, `coordinator/assets/heartbeat-prompts.md`, `coordinator/examples/coordination.md`, and `coordinator/evals/evals.json` refer to coordinated and standalone conversations as `workers` or `chats` (stopped, closed, or deleted, never archived) and remove conflicting `lone session` / `means a chat` / `archive` phrasing.
3. All edited non-code files are read in full, pass zero-residue and style checks (no U+2014 em dashes, no `means` definitions, no diminish-to-elevate phrasing, no AI attribution), and pass `quick_validate.py` and `tools/validate-all.sh` with zero errors in `maestro/`, `coordinator/`, and `AGENTS.md`.
4. `steward.py check` reports clean and `git diff --check` exits 0.

## Proposed Changes
- `[MODIFY] maestro/SKILL.md`
- `[MODIFY] maestro/references/session-lifecycle.md`
- `[MODIFY] maestro/examples/session-lifecycle-and-recovery.md`
- `[MODIFY] maestro/evals/evals.json`
- `[MODIFY] coordinator/SKILL.md`
- `[MODIFY] coordinator/references/delegation.md`
- `[MODIFY] coordinator/references/heartbeat-and-wake.md`
- `[MODIFY] coordinator/references/task-ids.md`
- `[MODIFY] coordinator/assets/heartbeat-prompts.md`
- `[MODIFY] coordinator/examples/coordination.md`
- `[MODIFY] coordinator/evals/evals.json`

## Verification Plan
- Read all 11 edited files in full and run a terminology grep check across `maestro/` and `coordinator/`.
- Run `/usr/bin/python3 skill-creator/scripts/quick_validate.py` on `maestro` and `coordinator`.
- Run `bash tools/validate-all.sh`, `python3 -m json.tool` on modified eval JSON files, `git diff --check`, and `python3 steward/scripts/steward.py check`.

## Temporary Artifacts
- None.
