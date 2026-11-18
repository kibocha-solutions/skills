# Wake Timer Prompt Templates

## 1. Graduating algorithmic wake timer prompt (1m -> 3m -> 5m -> 12m -> 15m -> 30m)

```text
GRADUATING WAKE (Step <1m|3m|5m|12m|15m|30m>):
1. Re-read goal.md, implementation_plan.md, and tasks.md in the active Maestro session to remember exact objectives and acceptance criteria.
2. Re-read AGENTS.md, active SKILL.md files, .agents/MEMORY.md, .agents/brain/approvals.json, and user rulings.
3. Check every worker (chat and subagent) in .agents/brain/workers.json, manage_subagents, and manage_task. Catch any worker sitting idle or waiting for go-ahead even if it failed to forward its blocker; resolve questions from repo authority and assign next work immediately.
4. Persist state to tasks.md, walkthrough.md, .agents/brain/workers.json, and .agents/brain/handoffs/.
5. Check 5-hour and weekly usage limits and next reset time. If >= 95% (5h) or >= 98% (weekly), persist state, cancel this timer, and schedule the post-reset wake timer.
6. Schedule the next single wake timer:
   - If work is complete: cancel all timers and do not schedule another.
   - If blocked exclusively on user action: switch to the 90m-120m (5400s-7200s) user-blocked timer.
   - If coordinator/session action was needed on this tick: reset to 1m (60s).
   - If no action was needed and workers are progressing: graduate to the next interval in [1m, 3m, 5m, 12m, 15m, 30m].
```

## 2. User-blocked long wake timer prompt (90m-120m)

```text
USER-BLOCKED WAKE (90m-120m):
Check whether the user has responded or completed the requested action (such as approving a gated worker command or supplying credentials).
- If still waiting exclusively on user action and no parallel work can proceed, schedule the next 90m-120m (5400s-7200s) wake timer, state "waiting on user action" with the exact worker/action pointer, and end the turn.
- If unblocked, cancel this timer, reset the graduating algorithmic wake timer to 1m (60s), and resume work.
```

## 3. Post-reset wake timer prompt (95% 5-hour / 98% weekly)

```text
POST-RESET WAKE TIMER:
1. Confirm the governing usage window has reset and no other wake timer is active.
2. Read AGENTS.md, coordinator/SKILL.md, the active Maestro session, .agents/brain/workers.json, .agents/brain/approvals.json, and the latest handoff file under .agents/brain/handoffs/ in full.
3. Resume the graduating algorithmic wake timer at 1m (60s).
4. Resume execution from the exact Next Action recorded in the handoff file.
```
