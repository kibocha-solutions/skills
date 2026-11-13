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

## Parent question routing

**Good:**
The coordinator instructs a worker: "Direct all questions and blockers to me (your parent), never to the user. Pass this same rule to any sub-agent you spawn." When the worker asks whether to use `pytest` or `unittest`, the parent checks `pyproject.toml`, sees `pytest` configured, and answers the worker directly without bothering the user. Only when a production deploy requires a credential the agent does not have does the parent send a complete `AGENTS.md` Section 12 escalation to the user.

**Bad:**
A worker hits a minor naming question and tells the coordinator to ask the user, or asks the user directly in a child chat without investigating the repository first.

## Heartbeat and wake timer mutual exclusion

**Good:**
During active multi-agent work, the coordinator runs a single 30-minute active heartbeat. At 95% 5-hour usage, the coordinator updates `tasks.md`, `walkthrough.md`, and `.agents/brain/handoffs/`, cancels the 30-minute heartbeat, and schedules a one-shot wake timer for `reset_time + 5m`. When the wake timer fires, it verifies no wake timer remains active, reads state files, and starts a fresh 30-minute heartbeat.

**Bad:**
The coordinator schedules a post-reset wake timer while leaving the 30-minute heartbeat running, or switches to a 90-minute blocked heartbeat while parallel verification work is still possible.

## 90-minute blocked heartbeat

**Good:**
All parallel work and verification are complete, and the only remaining step requires the user to authorize an external account change. The coordinator persists state, cancels the 30-minute heartbeat, and starts a 90-minute blocked heartbeat. When it fires and the user has not yet replied, the coordinator replies `"waiting on user action"`.

**Bad:**
The coordinator stops scheduling any check-in while waiting on the user, or replies with a long summary instead of `"waiting on user action"`.

## Unavailable timer or usage-check capability

**Good:**
The coordinator inspects the `schedule` tool schema and platform usage command docs, attempts to query the 5-hour reset timestamp, and observes a `command not found` error. It immediately notifies the user following `AGENTS.md` Section 12, stating what docs were checked, what command failed with the exact error, the consequence for automated 95%/98% pausing, and the recommended manual fallback.

**Bad:**
The coordinator notices the usage command is missing and silently skips usage monitoring and wake timers without telling the user.
