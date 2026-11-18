# Graduating Wake Timer and Persistence Procedure

## Contents

1. Startup capability inventory and reset-time lookup
2. Strict single-timer exclusion invariant
3. Graduating algorithmic wake timer (1m -> 3m -> 5m -> 12m -> 15m -> 30m)
4. User-blocked long wake timer (90m-120m)
5. Post-reset wake timer (95% 5-hour / 98% weekly)
6. Exact persistence mechanism
7. Unavailable capability reporting

## 1. Startup capability inventory and reset-time lookup

At the start of a chat, before dispatching sustained work:

1. Inspect platform tool schemas, documentation, and local commands for:
   - One-shot wake timer scheduling (`schedule` with `DurationSeconds` or platform equivalent).
   - Task management (`manage_task` `list` and `kill`) to cancel superseded or completed timers.
   - Usage-window status and next reset time (e.g., platform usage command, status endpoint, or metadata).
   - Inter-agent messaging (`send_message`, `manage_subagents`, `swarm`, or platform equivalent).
   - Persistent state storage (`.agents/brain/sessions/active/`, `.agents/brain/workers.json`, `.agents/brain/approvals.json`, and `.agents/brain/handoffs/`).
2. Attempt to read the current 5-hour and weekly usage percentages and their exact next reset timestamps.
3. If any required capability (timer, wake, usage check, or messaging) fails or is missing after inspecting documentation and attempting it, report the failure to the user per Section 7 instead of silently skipping it.

## 2. Strict single-timer exclusion invariant

At most ONE wake or monitoring timer may be active for a coordinator or lone session at any moment:

1. Before scheduling any new timer (`Graduating Wake`, `User-Blocked Wake`, or `Post-Reset Wake`), list active tasks (`manage_task` `list`) and cancel every existing wake or heartbeat timer (`manage_task` `kill`).
2. When all task work finishes, cancel every active timer immediately so no scheduled wake fires after completion.

## 3. Graduating algorithmic wake timer (1m -> 3m -> 5m -> 12m -> 15m -> 30m)

Both coordinators and lone sessions (working independently without a coordinator) use the graduating sequence `[1, 3, 5, 12, 15, 30]` minutes (`60`, `180`, `300`, `720`, `900`, `1800` seconds) via one-shot `schedule(DurationSeconds=...)` using the prompt template in `assets/heartbeat-prompts.md`:

1. **Initial timer**: Schedule the first wake at **1 minute (`60` seconds)** (`step = 0`).
2. **On every wake tick, execute these mandatory steps in order**:
   1. Re-read `goal.md`, `implementation_plan.md`, and `tasks.md` to refresh exact objectives, acceptance criteria, and pending tasks.
   2. Re-read `AGENTS.md`, active `SKILL.md` files, `.agents/MEMORY.md`, `.agents/brain/approvals.json`, and user rulings to keep all rules and constraints active in context.
   3. Inspect every worker (`chat` and `subagent`) recorded in `.agents/brain/workers.json` (plus `manage_subagents` `list` / `swarm` `status` / `manage_task` `list`):
      - Detect any worker that is sitting idle, stalled, or waiting for go-ahead/response even if it opted not to forward a blocker.
      - Resolve questions from memories, instructions, user rulings, and repo docs/code, or assign the next bounded task immediately so work never stalls until completion.
   4. Persist updated state per Section 6 (`.agents/brain/workers.json`, Maestro session, and `.agents/brain/handoffs/`).
   5. Check 5-hour and weekly usage limits: if usage reaches `>= 95%` (5-hour) or `>= 98%` (weekly), execute the Post-Reset Wake Timer handoff in Section 5.
3. **Choose the next timer interval**:
   - **Action was needed** (dispatched work, answered/unblocked a worker, reviewed deliverables, reassigned a stalled worker, or took a lone-session step): reset the sequence back to **1 minute (`60` seconds)** (`step = 0`).
   - **No action was needed** and workers (or background tasks) are still actively running: advance one step along `[1, 3, 5, 12, 15, 30]` minutes (staying at `30` minutes once reached).
   - **Blocked exclusively on user action**: switch to Section 4 (`90m-120m`).
   - **All work complete**: cancel all timers and do not schedule another.

## 4. User-blocked long wake timer (90m-120m)

Use the long wake timer ONLY when waiting exclusively on the user to act (such as approving a gated command or supplying credentials) and no parallel, verification, or preparation work can proceed:

1. Cancel any active graduating timer.
2. Persist state per Section 6, naming the exact worker (`coordination_id`, `platform_id`, `kind`, `role`) if applicable and the exact user action requested.
3. Schedule a one-shot wake timer between **90 and 120 minutes** (`DurationSeconds`: `5400` to `7200`, i.e., `1h 30m` to `2h`) using the user-blocked template in `assets/heartbeat-prompts.md`.
4. On trigger, if still waiting exclusively on the user with no new user action, re-schedule another `5400-7200` second timer and end the turn cleanly without nagging.
5. As soon as the user acts or responds, cancel the long wake timer and resume the graduating algorithmic wake timer at **1 minute (`60` seconds)**.

## 5. Post-reset wake timer (95% 5-hour / 98% weekly)

When team or coordinator usage reaches **95% of the 5-hour window** (`5%` remaining) or **98% of the weekly window** (`2%` remaining):

1. Stop dispatching new work and pause active workers cleanly, preserving partial results.
2. Persist all state immediately using Section 6.
3. Cancel any active graduating or user-blocked timer (`manage_task` `kill`).
4. Compute `DurationSeconds` until `next_reset_time + 5 minutes` (`300` seconds buffer after the governing window resets).
5. Schedule the one-shot Post-Reset Wake Timer (`schedule` with `DurationSeconds` and the wake prompt from `assets/heartbeat-prompts.md`).
6. Compact context if the platform supports compaction, and report the controlled pause and wake timestamp to the user.
7. When the Post-Reset Wake Timer fires:
   - Read `AGENTS.md`, `coordinator/SKILL.md`, the active Maestro session files, `.agents/brain/workers.json`, `.agents/brain/approvals.json`, and the latest handoff file in full.
   - Resume the graduating algorithmic wake timer at **1 minute (`60` seconds)** and continue from the recorded Next Action.

## 6. Exact persistence mechanism

Persist durable state at every phase boundary, on every wake timer tick, before switching to a user-blocked or post-reset wake timer, and whenever compaction is near:

1. Update `.agents/brain/workers.json` with current `coordination_id`, `platform_id`, `kind`, `role`, `parent_id`, `model`, `state`, `assignment`, `last_checked_at`, and `deletion_confirmed` for every worker.
2. Update the active Maestro session under `.agents/brain/sessions/active/<session-slug>/`:
   - `tasks.md`: mark completed items `[x]`, in-progress items `[/]`, and pending items `[ ]`.
   - `walkthrough.md`: record verified evidence, command outputs, changed files, decisions made, and open blockers.
3. Write or update a handoff note at `.agents/brain/handoffs/YYYY-MM-DD-HHMM-<slug>.md` containing:
   - **Objective**, **Current task**, **Completed work**, **Changed files**, **Verification**, **Blockers**, **Next action**, and **Usage and timer state** (last observed 5h/weekly percentages, next reset time, active timer type, and current graduation step `1m`/`3m`/`5m`/`12m`/`15m`/`30m` or `90m-120m`).

## 7. Unavailable capability reporting

Never silently skip a required capability check, wake timer, or usage-limit check:

1. Inspect the relevant platform documentation, CLI commands, and tool schemas first, and attempt the call.
2. If the capability is unavailable, unsupported, or errors out, notify the user in chat following `AGENTS.md` Section 12:
   - State which capability failed (usage check, wake timer, or worker inspection).
   - State the exact documentation/schemas inspected and the exact command or tool call attempted, along with the verbatim error or absence observed.
   - Explain the consequence (for example, inability to detect the 95%/98% threshold automatically or inability to auto-resume).
   - Recommend the fallback and wait or proceed as directed.
