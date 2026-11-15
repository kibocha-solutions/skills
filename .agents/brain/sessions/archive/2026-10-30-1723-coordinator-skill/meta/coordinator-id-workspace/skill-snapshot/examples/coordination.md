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
