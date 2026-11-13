# Heartbeat and Wake Timer Prompt Templates

## 1. 30-minute active heartbeat prompt

```text
HEARTBEAT (30m):
1. Check all active sub-agents, tasks, and child chats for status, blockers, and unanswered questions. Resolve worker questions from authority and evidence; escalate to the user only when user action is required.
2. Verify progress against active deliverables and acceptance criteria.
3. Re-read AGENTS.md and active SKILL.md files to refresh rules and gates.
4. Update active Maestro session files (tasks.md, walkthrough.md) and .agents/brain/handoffs/ with current state and next action.
5. Check 5-hour and weekly usage limits and next reset time. If >= 95% (5h) or >= 98% (weekly), persist state, cancel this heartbeat, and schedule the post-reset wake timer. If blocked solely on user action with no parallel work, cancel this heartbeat and start the 90-minute blocked heartbeat.
```

## 2. 90-minute blocked heartbeat prompt

```text
BLOCKED HEARTBEAT (90m):
Check whether the user has responded or unblocked the pending action.
- If still waiting exclusively on user action and no other work can proceed, respond exactly with: "waiting on user action" and end the turn.
- If unblocked, cancel this 90-minute blocked heartbeat, start the 30-minute active heartbeat, and resume work.
```

## 3. Post-reset wake timer prompt

```text
WAKE TIMER (POST-RESET RESUME):
1. Confirm the governing usage window has reset and no other wake timer or heartbeat is active.
2. Read AGENTS.md, coordinator/SKILL.md, the active Maestro session under .agents/brain/sessions/active/, and the latest handoff file under .agents/brain/handoffs/ in full.
3. Start the 30-minute active heartbeat.
4. Resume execution from the exact Next Action recorded in the handoff file.
```
