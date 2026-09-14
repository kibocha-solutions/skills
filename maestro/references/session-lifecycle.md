# Session Lifecycle

## States

Use these states in `tasks.md`:

| State | Required action |
|---|---|
| `INIT` | Create the session files. |
| `PLANNING` | Write the plan and initial tasks. |
| `EXECUTING` | Complete tasks in order. |
| `VERIFYING` | Test every acceptance criterion. |
| `DONE` | Finalize the walkthrough and wait for the next task. |
| `BLOCKED` | Record the blocker and required input. |

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

## DONE

1. Finalize the walkthrough.
2. Record limitations and deferred work in the walkthrough.
3. Keep the session active until a new task or phase arrives.

## BLOCKED

1. Mark the affected task `[!]`.
2. Record the exact blocker and required input.
3. Notify the user.
4. Continue independent tasks when authorized and safe.
5. Restore the prior state when the blocker clears.

## Archive

1. Trigger archival only after a new task or phase arrives.
2. Confirm the session is `DONE`.
3. Confirm every acceptance criterion has evidence.
4. Move the session from `sessions/active/` to `sessions/archive/`.
5. Do not edit the archived session.
6. Create a new session for the new work.

## Resume

1. Read `tasks.md`.
2. Read `implementation_plan.md`.
3. Read `walkthrough.md`.
4. Read `goal.md` when present.
5. Continue the current `[/]` task or the first `[ ]` task.
