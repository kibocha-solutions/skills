# Session Lifecycle

## States

Use these states in `tasks.md`:

| State | Required action |
|---|---|
| `INIT` | Create the session files. |
| `PLANNING` | Write the plan and initial tasks. |
| `EXECUTING` | Complete tasks in order. |
| `VERIFYING` | Test every acceptance criterion. |
| `BLOCKED` | Record the blocker and required input. |
| `DONE` | Closed: every acceptance criterion passed. |
| `PARTIAL` | Closed: the user accepted the result or moved on; deferred items recorded. |
| `SUPERSEDED` | Closed: another Maestro session took over. |
| `ABANDONED` | Closed: no change for 14 days and no open user request. |
| `DORMANT` | Parked: future or condition-bound work kept under `sessions/dormant/`, exempt from closing, staleness, and pruning. |

Write the state as the first state line of `tasks.md`, exactly `## State: <STATE>` with an optional parenthesized note. Never use another word or format.

## INIT

1. Create the session directory.
2. Create required files.
3. Add available task context to `meta/`.
4. Set the state to `PLANNING`.

## PLANNING

1. Write the objective.
2. Write falsifiable acceptance criteria.
3. List proposed file changes.
4. Write the verification plan.
5. Write ordered tasks.
6. Resolve blocking questions.
7. Set the state to `EXECUTING`.

## EXECUTING

1. Mark one task `[/]`.
2. Complete and verify that task.
3. Mark it `[x]`.
4. Update the walkthrough.
5. Repeat until no required task remains.
6. Set the state to `VERIFYING`.

## VERIFYING

1. Test each acceptance criterion against the final artifact.
2. Add failed criteria to `tasks.md` under `## Added`.
3. Return to `EXECUTING` when any criterion fails.
4. Record passing evidence.
5. Set the state to `DONE` when all criteria pass.

## Close

1. Finalize the walkthrough with the outcome in its first sentence, which becomes the archive index entry.
2. Record limitations and deferred work in the walkthrough.
3. Fold the Maestro session's handoffs into the walkthrough and delete them.
4. Run `python3 scripts/sessions.py close <session> <STATE> "<note>"` immediately; do not wait for a new task.

## BLOCKED

1. Mark the affected task `[!]`.
2. Record the exact blocker and required input.
3. Notify the user.
4. Continue independent tasks when authorized and safe.
5. Restore the prior state when the blocker clears.

## Archive and retention

1. `sessions.py close` and `sessions.py stale --apply` move evidence to `~/.agents/evidence/<project>/<session>/`, move the folder to `sessions/archive/`, and rewrite `sessions/archive/INDEX.md`.
2. Keep the 10 newest archived folders on disk.
3. In a Git repository, `sessions.py prune --apply` removes older committed archive folders and records a restore command for each in `INDEX.md`; Git history keeps the content.
4. Outside Git, `sessions.py prune --apply` bundles older folders into one `YYYY-Qn.tar.gz` per quarter.
5. Delete a quarterly bundle older than 12 months only with the user's approval.
6. Do not edit an archived Maestro session.

## Dormant

1. Park a session only when the user defers its work or ties it to a future condition.
2. Run `python3 scripts/sessions.py dormant <session> "<reason>" --wake "<condition>"`. The command writes `wake.md` with the reason, the conditions, and a history line, sets `## State: DORMANT`, and moves the folder to `sessions/dormant/`.
3. Use these condition forms:

| Form | Met when |
|---|---|
| `date: YYYY-MM-DD` | The current date is on or after the date. |
| `after: <session> closes` | The named session is in the archive or its index. |
| `exists: <project path>` | The path exists in the project. |
| Plain words | The agent judges it from current evidence and reports the evidence. |

4. A session with no condition is ready whenever no active session remains open.
5. `sessions.py stale --apply` moves an active session whose state is `DORMANT` to `sessions/dormant/` instead of closing it.
6. `sessions.py close`, `stale`, and `prune` never act on `sessions/dormant/`.
7. Run `python3 scripts/sessions.py wake-check` after the last open active session closes. It reports `waiting`, `judge conditions`, or `ready: ask the user` for each dormant session.
8. Ask the user before waking any session. Run `python3 scripts/sessions.py wake <session> "<approval>"` after approval; it restores the state the session was parked from, or `PLANNING`, appends to the history, and moves the folder back to `sessions/active/`.

## Resume

1. Read `tasks.md`.
2. Read `implementation_plan.md`.
3. Read `walkthrough.md`.
4. Read `goal.md` when present.
5. Continue the current `[/]` task or the first `[ ]` task.
