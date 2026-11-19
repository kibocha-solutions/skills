# Maestro Examples: Session Lifecycle and Threshold Recovery

## 1. Clean Task State Progression

### Bad (Uncoordinated State Jumps and Premature Completion)

```markdown
# Tasks: Feature Rollout
State: DONE

## Phase 1
- [x] Write implementation plan
- [x] Refactor database queries
- [x] Run load tests (encountered errors, skipped for now)
- [x] Ship release
```

Defects:
- Marks session `DONE` while verification checks failed.
- Hides failed criteria instead of reopening under `## Added`.
- No link between task checkmarks and concrete evidence in `walkthrough.md`.

### Good (Disciplined Execution and Threshold Recovery)

```markdown
# Tasks: Feature Rollout
State: IN_PROGRESS

## Phase 1: Database Refactoring
- [x] Implement parameterized batch query in `src/db.ts`
- [x] Execute unit tests (`npm test -- src/db.test.ts`)

## Phase 2: Load Verification
- [/] Run concurrency benchmarks (`k6 run load-test.js`)
- [ ] Verify 99th percentile response time is under 200ms

## Added (Threshold Recovery: Latency Spike at 500 Concurrency)
- [ ] Add connection pool tuning to `src/config.ts`
- [ ] Re-run benchmark to verify latency drops below 200ms
```

Advantages:
- Single active task `[/]` matches ongoing execution.
- Discovered verification failure immediately converted into explicit tasks under `## Added`.
- Session state remains `IN_PROGRESS` until all criteria pass.

## 2. Archiving Sessions vs Worker Chats

### Bad (Treating "Session" or "Archive" as Worker Chats)

The user says: "Archive the finished sessions." The agent closes or UI-archives active worker chats managed by `coordinator` and leaves completed folders in `.agents/brain/sessions/active/`.

Defects:
- Confuses chats and workers with Maestro sessions.
- Applies "archive" to worker chats while leaving completed Maestro sessions unarchived.

### Good (Exclusively Archiving Maestro Sessions)

The user says: "Archive the finished sessions." The agent runs `python3 maestro/scripts/sessions.py status` and `python3 maestro/scripts/sessions.py stale --apply` (or `close <session> DONE "<note>"`) to move finished Maestro sessions into `.agents/brain/sessions/archive/` and update `INDEX.md`, leaving active worker chats untouched for `coordinator`.

Advantages:
- Keeps "session" and "archive" scoped exclusively to Maestro sessions.
- Leaves worker and chat lifecycle operations (stop, close, delete) under `coordinator`.
