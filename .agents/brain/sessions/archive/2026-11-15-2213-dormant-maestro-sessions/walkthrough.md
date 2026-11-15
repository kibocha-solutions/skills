# Walkthrough

Dormant Maestro sessions now live under `sessions/dormant/` with a `wake.md` record, are exempt from closing, staleness, and pruning, and wake only with the user's approval after active work is cleared.

## Evidence

1. A throwaway project parked three sessions: a future date with a plain-word condition reported `waiting`; an `after:` and `exists:` pair reported `waiting`, then `ready: ask the user` once both were met; a session without conditions reported `ready: ask the user`.
2. `stale --apply` parked a hand-marked `DORMANT` session and wrote its `wake.md`; `prune --keep 0` listed only archived sessions.
3. `wake` restored `EXECUTING` and appended the approval to the history. The throwaway project was deleted.

## Candidates reported to the user

Archived sessions that may hold deferred work: skills `2026-10-30-1701-human-writer-skill` and `2026-10-30-1723-coordinator-skill`; PBOs framework sessions from 2026-08-19. None was moved; parking them is the user's decision.
