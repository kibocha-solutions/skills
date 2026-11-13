# Heartbeat, Wake Timer, and Persistence Procedure

## Contents

1. Startup capability inventory and reset-time lookup
2. Strict mutual exclusion invariant
3. 30-minute active heartbeat
4. 90-minute blocked heartbeat
5. Post-reset wake timer (95% 5-hour / 98% weekly)
6. Exact persistence mechanism
7. Unavailable capability reporting

## 1. Startup capability inventory and reset-time lookup

At session start, before dispatching sustained work:

1. Inspect platform tool schemas, documentation, and local commands for:
   - Recurring timer or cron scheduling (`schedule` with `CronExpression` or platform equivalent).
   - One-shot wake timer scheduling (`schedule` with `DurationSeconds` or platform equivalent).
   - Usage-window status and next reset time (e.g., platform usage command, status endpoint, or metadata).
   - Inter-agent messaging (`send_message`, `manage_task`, `manage_subagents`, or platform equivalent).
   - Persistent state storage (`.agents/brain/sessions/active/` and `.agents/brain/handoffs/`).
2. Attempt to read the current 5-hour and weekly usage percentages and their exact next reset timestamps.
3. If any required capability (timer, wake, usage check, or messaging) fails or is missing after inspecting documentation and attempting it, report the failure to the user per Section 7 instead of silently skipping it.

## 2. Strict mutual exclusion invariant

Heartbeat and Wake Timer MUST NEVER be active at the same time:

1. Before creating or starting a **Wake Timer**, list active tasks (`manage_task` `list`) and cancel every active **Heartbeat** (`manage_task` `kill`).
2. Before creating or starting a **Heartbeat** (30-minute or 90-minute), list active tasks (`manage_task` `list`) and cancel every active **Wake Timer** (`manage_task` `kill`).
3. Verify that at most one scheduling loop (either one Heartbeat OR one Wake Timer) is active at any moment.

## 3. 30-minute active heartbeat

While work is active (or parallel work remains), keep one 30-minute recurring Heartbeat active (`CronExpression: "*/30 * * * *"`, `IsDaemon: false`), using the prompt template in `assets/heartbeat-prompts.md`.

On every 30-minute Heartbeat trigger:

1. Check active sub-agents and child chats (`manage_subagents` `list`, `manage_task` `list`, or messaging). Follow up with stalled workers, resolve worker questions from authority and evidence, and reassign or redirect work if needed.
2. Verify whether active deliverables and acceptance criteria are being met.
3. Re-read `AGENTS.md` and the active `SKILL.md` files to refresh rules, gates, and step ordering in context.
4. Persist current state using the exact persistence mechanism in Section 6.
5. Check current 5-hour and weekly usage percentages and the next reset timestamp.
   - If usage is below 95% (5-hour) and below 98% (weekly), continue work.
   - If usage has reached or exceeded 95% (5-hour) or 98% (weekly), immediately execute the Wake Timer handoff in Section 5.
   - If all non-blocked work is finished and the team is blocked exclusively on user action, switch to the 90-minute Blocked Heartbeat in Section 4.

## 4. 90-minute blocked heartbeat

Use the 90-minute Blocked Heartbeat ONLY when the coordinator is waiting exclusively on user action and no parallel, verification, or preparation work can proceed.

1. Cancel the 30-minute Heartbeat (and verify no Wake Timer is active).
2. Persist current state per Section 6, clearly recording the exact user blocker and requested action.
3. Schedule a recurring 90-minute Heartbeat (`CronExpression: "0 */3 * * *"` or platform-supported 90-minute interval, or chain a 5400-second one-shot timer if cron does not support 90 minutes) using the blocked heartbeat prompt in `assets/heartbeat-prompts.md`.
4. On each blocked heartbeat trigger, if still waiting exclusively on the user with no new user message or unblocked work, reply with `"waiting on user action"` and end the turn.
5. As soon as the user responds or unblocks the task, cancel the 90-minute Blocked Heartbeat and restore the 30-minute active Heartbeat.

## 5. Post-reset wake timer (95% 5-hour / 98% weekly)

When team or coordinator usage reaches **95% of the 5-hour window** (5% remaining) or **98% of the weekly window** (2% remaining):

1. Stop dispatching new work and pause active workers cleanly, preserving partial results.
2. Persist all state immediately using the exact persistence mechanism in Section 6.
3. Cancel the active Heartbeat (`manage_task` `kill`) so Heartbeat and Wake Timer are never both active.
4. Compute `DurationSeconds` until `next_reset_time + 5 minutes` (300 seconds buffer after the governing window resets; or exact reset time if the platform supports exact wake scheduling).
5. Schedule the one-shot Wake Timer (`schedule` with `DurationSeconds` and the wake prompt from `assets/heartbeat-prompts.md`).
6. Compact context if the platform supports compaction.
7. Report the controlled pause to the user in chat, including: completed work, remaining work, exact state file paths, and the scheduled wake-up timestamp.
8. When the Wake Timer fires:
   - Cancel any lingering timer if applicable.
   - Read `AGENTS.md`, `coordinator/SKILL.md`, the active Maestro session files, and the latest handoff file in full.
   - Start a fresh 30-minute Heartbeat (confirming no Wake Timer remains active).
   - Resume execution from the recorded next action.

## 6. Exact persistence mechanism

Persist durable state at every phase boundary, on every 30-minute Heartbeat, before switching to a Blocked Heartbeat or Wake Timer, and immediately whenever context compaction is near or unpredictable:

1. Update the active Maestro session under `.agents/brain/sessions/active/<session-slug>/`:
   - `tasks.md`: mark completed items `[x]`, in-progress items `[/]`, and pending items `[ ]`.
   - `walkthrough.md`: record verified evidence, command outputs, changed files, and open blockers.
2. Write or update a handoff note at `.agents/brain/handoffs/YYYY-MM-DD-HHMM-<slug>.md` containing:
   - **Objective**: overall goal and scope.
   - **Current task**: active step and owner.
   - **Completed work**: concrete outputs and verified file paths.
   - **Changed files**: exact paths modified since last commit or checkpoint.
   - **Verification**: commands run and exact observed pass/fail counts.
   - **Blockers**: unresolved dependencies or user decisions needed.
   - **Next action**: the exact next command, edit, or tool call to execute on resume.
   - **Usage and timer state**: last observed 5-hour/weekly percentages, next reset time, and which timer (30-min Heartbeat, 90-min Blocked Heartbeat, or Wake Timer) is active.

## 7. Unavailable capability reporting

Never silently skip a required capability check, heartbeat, wake timer, or usage-limit check:

1. Inspect the relevant platform documentation, CLI commands, and tool schemas first, and attempt the call.
2. If the capability is unavailable, unsupported, or errors out, notify the user in chat following `AGENTS.md` Section 12:
   - State which capability failed (usage check, cron/heartbeat, or one-shot wake timer).
   - State the exact documentation/schemas inspected and the exact command or tool call attempted, along with the verbatim error or absence observed.
   - Explain the consequence (for example, inability to detect the 95%/98% threshold automatically or inability to auto-resume after reset).
   - Recommend the fallback (such as manual user check-ins or manual resumption at reset time) and wait or proceed as directed.
