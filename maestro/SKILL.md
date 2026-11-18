---
name: maestro
description: Plan, track, resume, verify, park, wake, and archive substantial or multi-session work with repository-local sessions under `.agents/brain/`. Use for multi-step tasks, phased work, long-running tasks, project orchestration, explicit planning requests, work that must survive context changes, deferred or future work that must be kept as a dormant session with wake conditions, and checking dormant sessions once active work is cleared.
---

# Maestro

A Maestro session is the work-record folder under `.agents/brain/sessions/`. A chat is a separate conversation. When the user says "session", the user means a chat; always write "Maestro session" for the folder.

Run scripts with the skill directory as the base path, for example `python3 <skill-dir>/scripts/sessions.py status`.

## 1. Orient

Before forming or resuming any Maestro session, acquaint yourself thoroughly with the repository, rules, and skills:

1. Identify the project root and discover all agent instruction and state directories (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/`, `.claude/`, `.cursor/`, `.github/`, and any memory index, handoff folder, or sessions folder).
2. Read the host's global rules and every repository instruction and `.agents/rules/*.md` file in full.
3. Map the project: if `graphify-out/graph.json` or `graphify-out/GRAPH_REPORT.md` exists (or when `graphify` applies to the repository), activate `graphify/SKILL.md` and query `graph_stats`, `god_nodes`, and `GRAPH_REPORT.md`; where `graphify` does not apply, read the repository's documentation and configuration files in full.
4. Inspect the skill catalogue against the project map and task, identify every skill applicable to the project, and read each applicable `SKILL.md` (with its routed `references/` and `examples/`) in full from disk.
5. Read `.agents/MEMORY.md` in full when it exists, every topic file linked from relevant memory entries, and relevant files in `.agents/brain/handoffs/`.
6. Read the repository's persistent approval mode with `python3 scripts/sessions.py approval` (`ask`, `true`, `false`); record any new user approval directive immediately with `python3 scripts/sessions.py approval set <ask|true|false> "<note>"`.
7. Run `python3 scripts/sessions.py status` to list every active and dormant Maestro session and the active `approval_mode`.
8. Close finished and stale Maestro sessions with `python3 scripts/sessions.py stale --apply`, and report the closures to the user in one line.
9. Match the current task to the remaining active Maestro sessions by objective and slug. Match it to a dormant Maestro session only when the user names that work or `approval_mode` is `true` and its conditions are met.
10. Do not create a duplicate Maestro session.
11. Activate `steward/SKILL.md` and size the plan to the capacity in `~/.agents/system-profile.md`.

Read [dormant sessions](references/session-lifecycle.md#dormant) before parking, checking, or waking a Maestro session.

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
5. Put text sources and research notes in `meta/`. Put screenshots, renders, logs, and other evidence in the steward agent store.

## 3. Write the plan

Write `implementation_plan.md` before substantive edits.

1. State the objective and final user-visible outcome.
2. List numbered, falsifiable acceptance criteria.
3. List proposed changes by component and file.
4. Mark each file `[NEW]`, `[MODIFY]`, `[MOVE]`, or `[DELETE]`.
5. List blocking questions.
6. List the verification method for every acceptance criterion.
7. Decide missing questions from repository memories, instructions, user rulings, and docs/code first; stop for user input only when `approval_mode` is `false`, or when `approval_mode` is `ask` and a missing major or out-of-scope decision cannot be resolved from repository authority.
8. List each temporary artifact the work will create and the step that removes it.

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
4. Handle scope additions by `approval_mode`: in `true` mode, record and execute bounded in-repository additions in `walkthrough.md`; in `ask` mode, stop for the user when added scope crosses the approved threshold; in `false` mode, obtain approval before any added work.
5. Record every threshold event in `walkthrough.md`.

## 7. Verify

Read [session lifecycle](references/session-lifecycle.md).

1. Confirm that every required task is `[x]`.
2. Verify each acceptance criterion against the exact final artifact.
3. Reopen failed criteria as tasks under `## Added`.
4. Run every required automated, manual, and visual check.
5. Read each changed instruction or narrative file in full.
6. Record evidence and limitations in `walkthrough.md`.
7. Run `steward/scripts/steward.py check` and resolve every finding.
8. Set the session state to `DONE` only after all criteria pass.

## 8. Preserve durable knowledge

Read [memory conventions](references/memory-conventions.md).

1. Identify facts, decisions, or user preferences that future work cannot recover cheaply from current artifacts.
2. Update an existing topic before creating a new one.
3. Keep behavioral rules in `AGENTS.md` or the relevant skill.
4. Keep session state in the session folder.
5. Keep secrets, private strategy, and client-confidential content out of memory.

## 9. Close and archive

Read [session lifecycle](references/session-lifecycle.md#close).

1. Close a Maestro session as soon as one closed state applies, even when work remains:
   - `DONE`: every acceptance criterion passed.
   - `PARTIAL`: the user accepted the result or moved to other work; record the deferred items in `walkthrough.md`.
   - `SUPERSEDED`: another Maestro session took over; name it in `walkthrough.md`.
   - `ABANDONED`: no change for 14 days, no open user request, and no deferral by the user; park deferred work under Section 10 instead.
2. Fold the Maestro session's handoffs into `walkthrough.md`, then delete them.
3. Run `python3 scripts/sessions.py close <session> <STATE> "<note>"` to set the state, move evidence to the agent store, archive the folder, and update `sessions/archive/INDEX.md`.
4. Do not edit an archived Maestro session; reopen one by moving it back to `sessions/active/`.
5. Run `python3 scripts/sessions.py prune --apply` after the archive is committed and holds more than 10 folders.
6. Report each closure to the user in one line.

## 10. Park and wake dormant sessions

1. Park a Maestro session as `DORMANT` instead of closing it when the user defers its work to the future or ties it to a condition: `python3 scripts/sessions.py dormant <session> "<reason>" --wake "<condition>"`. Repeat `--wake` for each condition. To park an archived Maestro session the user names, move it back to `sessions/active/` first.
2. Write each wake condition in a checkable form when possible: `date: YYYY-MM-DD`, `after: <session> closes`, or `exists: <project path>`. Write any other condition in plain words.
3. Never close, abandon, prune, or edit the plan of a dormant Maestro session.
4. Work every open active Maestro session first.
5. When no active Maestro session remains open, run `python3 scripts/sessions.py wake-check`.
6. For each session reported `ready` or `judge conditions`, decide each plain-word condition from current evidence, and apply `approval_mode`:
   - In `true` mode, automatically run `python3 scripts/sessions.py wake <session> "auto-wake under approval_mode=true"` for sessions whose conditions are met or that have none, and resume under Section 2.
   - In `ask` or `false` mode, ask the user for permission before running `python3 scripts/sessions.py wake <session> "<user approval>"`, naming the session, its reason, and each condition with its result.
7. Leave a session dormant when its conditions are not met or the user declines, and report it in one line.

Inspect [session examples](examples/session-lifecycle-and-recovery.md) for task state transitions and recovery patterns.

## 11. Pre-completion checklist

Before marking a Maestro session complete, confirm evidence exists for each item:

- [ ] Global rules, repository instructions, project map (`graphify` or docs/configs), applicable skills, memories, and `approval_mode` read before forming or resuming the session.
- [ ] Every listed task in `tasks.md` is marked `[x]`.
- [ ] Every acceptance criterion in `implementation_plan.md` verified against the exact final artifact.
- [ ] Any failed check or unexpected defect reopened under `## Added` and resolved.
- [ ] `walkthrough.md` records verifiable evidence, test commands, and limitations.
- [ ] All changed narrative or instruction files read manually in full from start to finish.
- [ ] Durable knowledge and decisions recorded in `.agents/MEMORY.md` or topic files.
- [ ] Steward check clean and every temporary artifact removed.
- [ ] Maestro session closed with `DONE`, `PARTIAL`, `SUPERSEDED`, or `ABANDONED` and archived, parked as `DORMANT` with its reason and wake conditions, or left active in an open state.
- [ ] Dormant Maestro sessions checked with `wake-check` once no active Maestro session remained open, and woken only under `approval_mode=true` (when conditions pass) or explicit user approval.
- [ ] Zero AI attribution across all session artifacts and commits.
- [ ] No U+2014 em dashes in normal prose.

