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
