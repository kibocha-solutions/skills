# Coordination Examples

## Bounded assignment

Bad: “Audit the application and fix everything.”

Good: “Inspect the candidate table in the existing browser session. Record sort steps, observed row order, expected order, and screenshots. Do not change code or restart services. Return DONE or BLOCKED with evidence after the seven listed columns are checked.”

## Independent verification

Bad: The executor changes the comparator and declares its own fix accepted.

Good: The executor reports the changed file and focused checks. The coordinator asks the inspector who found the issue to repeat the original browser steps against the refreshed service.

## Coordinator succession

Bad: A second coordinator begins assigning work while the first continues to lead.

Good: The current coordinator reserves a chat slot, transfers the ledger, receives acknowledgment, names the successor as the sole coordinator, informs the user, and stops its own coordinator work.

## Task IDs and cleanup

Bad: Assign `1000` to an executor, reuse `1003` while its inspector still exists, or count only inspectors in the child bucket.

Good: Assign `0000` to the coordinator, `1000` to an inspector, and `2000` to an executor. The inspector requests a child from the coordinator. After approval and completion, the inspector preserves evidence, confirms deletion through an authorized platform capability, and releases the child's ID. When retained child tasks exceed ten, the coordinator removes up to seven eligible completed children across both worker roles, subject to the cleanup rules.

## Coordinator rollover

Bad: Create a new `0000` while the old `0000` still exists, or delete the active `0009` before the handoff.

Good: Coordinator `0009` preserves the handoff and deletes eligible retired predecessors. After the old `0000` is confirmed deleted and a slot is free, `0009` creates a new `0000` with instructions to delete `0009`. The successor acknowledges the handoff, assumes coordination, waits for `0009` to stop, and confirms its deletion.

## Reporting completion and blockers

Bad: A child finishes its inspection and leaves its findings only in its own chat. Another worker waits for credentials without notifying anyone.

Good: The child messages its parent with its result and evidence. The parent acknowledges and forwards the outcome to the coordinator. A worker needing credentials sends its parent a blocker describing the required access without including a secret; the coordinator requests user action through the authorized channel.

## Child model selection

Bad: Launch a routine screenshot inspection with the coordinator's powerful model merely because it is the inherited default.

Good: Select Luna or Haiku explicitly when available and capable of performing the bounded inspection. If only a stronger model has the required browser access, record that limitation and select an authorized model with the necessary tools.

## Parent question routing and Worker Rules

**Good:**
The coordinator records the sub-agent in `.agents/brain/workers.json` and tells it: "You are a worker under coordinator 0000. Presume the user is exclusively with me and will not see your chat or catch unforwarded issues. Send ALL questions, blockers, and status reports to me without exception; pass these same Worker Rules to any child." When the worker asks whether to use `pytest` or `unittest`, the coordinator searches `.agents/MEMORY.md`, instructions, Maestro rulings, and `pyproject.toml`, sees `pytest` configured, and answers directly without bothering the user or asking for go-ahead. Only when a gated command physically requires the user's approval does the coordinator point the user to the exact worker ID (`2001`, `platform_id`, `subagent`, executor) and action required.

**Bad:**
A worker hits a minor naming question and tells the coordinator to ask the user, waits silently for go-ahead without messaging the coordinator, or the coordinator asks the user for routine go-ahead before resolving from repo files.

## Graduating algorithmic wake timer

**Good:**
During active work (or a lone session), the agent schedules a 1-minute (`60s`) wake timer. On tick 1, workers are still running and no coordinator action is needed, so after re-reading `goal.md`/`tasks.md`/`AGENTS.md`, checking `.agents/brain/workers.json`, and persisting state, the coordinator graduates the next wake timer to 3 minutes (`180s`), then 5m, 12m, 15m, and 30m while waiting. On tick 4, a worker in `.agents/brain/workers.json` is waiting for go-ahead; the coordinator assigns its next task and resets the next wake timer back to 1 minute (`60s`). At 95% 5-hour usage, it cancels the active timer and schedules a post-reset wake timer for `reset_time + 5m`. When all work finishes, it cancels every wake timer.

**Bad:**
Keeping a fixed 30-minute timer while a worker silently stalls after 2 minutes, running two wake timers simultaneously, or leaving an active wake timer running after the task is complete.

## User-blocked long wake timer (90m-120m)

**Good:**
All parallel work and verification are complete, and the only remaining step requires the user to approve an external account change or a gated command on worker `2001`. The coordinator persists state, cancels the active graduating timer, points the user to the exact worker and action, and schedules a 90m-120m (`5400s-7200s`) wake timer. Once the user acts, it cancels the long timer and resumes the graduating timer at 1 minute (`60s`).

**Bad:**
Interrupting the user every 1 minute while waiting exclusively on user action, or stopping all timers when user-blocked work still needs resumption.

## Unavailable timer or usage-check capability

**Good:**
The coordinator inspects the `schedule` tool schema and platform usage command docs, attempts to query the 5-hour reset timestamp, and observes a `command not found` error. It immediately notifies the user following `AGENTS.md` Section 12, stating what docs were checked, what command failed with the exact error, the consequence for automated 95%/98% pausing, and the recommended manual fallback.

**Bad:**
The coordinator notices the usage command is missing and silently skips usage monitoring and wake timers without telling the user.
