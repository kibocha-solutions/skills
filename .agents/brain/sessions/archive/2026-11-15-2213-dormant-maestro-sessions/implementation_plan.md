# Dormant Maestro Sessions

## Objective

Keep future or condition-bound work as dormant Maestro sessions that no retention rule closes, and check them only after active work is cleared, asking the user before waking any.

## Acceptance criteria

1. `sessions.py dormant` writes `wake.md`, sets `DORMANT`, and moves the session to `sessions/dormant/`.
2. `sessions.py stale`, `close`, and `prune` never act on `sessions/dormant/`; `stale` parks an active session marked `DORMANT`.
3. `sessions.py wake-check` reports `waiting`, `judge conditions`, or `ready: ask the user` from date, session, path, and plain-word conditions.
4. `sessions.py wake` restores the parked state and records the approval.
5. Maestro orders active work first, then dormant checks, and requires user approval before waking.

## Changes

1. `[MODIFY]` `maestro/scripts/sessions.py`.
2. `[MODIFY]` `maestro/SKILL.md`, `maestro/references/session-lifecycle.md`, `maestro/references/brain-conventions.md`, `maestro/evals/evals.json`.

## Verification

1. Exercise every command on a throwaway project in the steward scratch store, then delete it.
2. Read every changed file in full; run em dash and JSON checks; run the steward check.
