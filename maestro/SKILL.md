---
name: maestro
description: Plan, track, resume, verify, and archive substantial or multi-session work with repository-local sessions under `.agents/brain/`. Use for multi-step tasks, phased work, long-running tasks, project orchestration, explicit planning requests, or work that must survive context changes.
---

# Maestro

## 1. Orient

1. Identify the project root.
2. Read `.agents/MEMORY.md` in full when it exists.
3. Read every topic file linked from relevant memory entries.
4. Read relevant files in `.agents/brain/handoffs/`.
5. List every session in `.agents/brain/sessions/active/`.
6. Match the current task to active sessions by objective and slug.
7. Do not create a duplicate session.

Read [brain conventions](references/brain-conventions.md) before creating or moving session files.

## 2. Resume or create a session

### Resume

1. Read `tasks.md`.
2. Read `implementation_plan.md` when present.
3. Read `walkthrough.md`.
4. Read `goal.md` when present.
5. Continue the current `[/]` task or the first `[ ]` task.
6. Do not re-plan completed work.

### Create

1. Create `.agents/brain/sessions/active/YYYY-MM-DD-HHMM-<slug>/`.
2. Use local time and a two-to-five-word lowercase slug.
3. Create `meta/`, `implementation_plan.md`, `tasks.md`, and `walkthrough.md`.
4. Create `goal.md` only when the user requests a tracked goal or the governing runtime explicitly requires it.
5. Put source material and task-specific research in `meta/`.

## 3. Write the plan

Write `implementation_plan.md` before substantive edits.

1. State the objective and final user-visible outcome.
2. List numbered, falsifiable acceptance criteria.
3. List proposed changes by component and file.
4. Mark each file `[NEW]`, `[MODIFY]`, `[MOVE]`, or `[DELETE]`.
5. List blocking questions.
6. List the verification method for every acceptance criterion.
7. Stop for user input only when a missing decision would materially change the result or authority.

## 4. Write and maintain tasks

1. Set the state at the top of `tasks.md`.
2. Divide work into ordered phases.
3. Use `[ ]` for not started.
4. Use `[/]` for the single active task.
5. Use `[x]` only after artifact verification.
6. Use `[!]` for a genuine blocker.
7. Add unplanned work under `## Added`.
8. Do not expand scope silently.
9. Update the task list immediately after each state change.

## 5. Execute

1. Work through tasks in order.
2. Preserve unrelated worktree changes.
3. Apply the skills triggered by each task.
4. Record material deviations in `walkthrough.md`.
5. Record commands and verification results needed for resumption.
6. Update `walkthrough.md` after each completed phase.
7. Create a handoff before changing tasks or chats when reconstruction would otherwise be required.

## 6. Monitor thresholds

Read [goal protocol](references/goal-protocol.md) when `goal.md` exists.

1. Check progress, quality, and scope thresholds at the start of each continuation.
2. Decompose stalled work.
3. Re-plan work with repeated verification failures.
4. Stop for the user when added scope crosses the approved threshold.
5. Record every threshold event in `walkthrough.md`.

## 7. Verify

Read [session lifecycle](references/session-lifecycle.md).

1. Confirm that every required task is `[x]`.
2. Verify each acceptance criterion against the exact final artifact.
3. Reopen failed criteria as tasks under `## Added`.
4. Run every required automated, manual, and visual check.
5. Read each changed instruction or narrative file in full.
6. Record evidence and limitations in `walkthrough.md`.
7. Set the session state to `DONE` only after all criteria pass.

## 8. Preserve durable knowledge

Read [memory conventions](references/memory-conventions.md).

1. Identify facts, decisions, or user preferences that future work cannot recover cheaply from current artifacts.
2. Update an existing topic before creating a new one.
3. Keep behavioral rules in `AGENTS.md` or the relevant skill.
4. Keep session state in the session folder.
5. Keep secrets, private strategy, and client-confidential content out of memory.

## 9. Archive

1. Wait for a new task or phase before archiving a `DONE` session.
2. Confirm the final walkthrough and acceptance evidence.
3. Move the session from `sessions/active/` to `sessions/archive/`.
4. Do not edit an archived session.
5. Create a new session for the new task.
6. Keep an incomplete session active unless the user authorizes abandonment.
