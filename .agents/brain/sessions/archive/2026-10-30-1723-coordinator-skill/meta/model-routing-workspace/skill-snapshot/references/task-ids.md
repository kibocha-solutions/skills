# Task IDs and Cleanup

## Assign IDs

1. Maintain a shared registry for the coordinated task with coordination ID, role, parent ID, platform identifier, state, creation order, and deletion confirmation.
2. Assign the initial coordinator `0000` and each successor the next unused ID in sequence through `0009`.
3. Keep exactly one designated coordinator; count an overlapping successor chat against the existing visible-chat cap.
4. Assign inspectors IDs from `1000` through `1999` and executors IDs from `2000` through `2999`.
5. Treat IDs as four-character strings so leading zeroes are retained.
6. Assign each child an ID in the range for its own role and record its parent independently of its numeric ID.
7. Reserve an ID before creating a task; bind it to the platform identifier when creation succeeds.
8. Keep IDs unique across the shared registry; never reuse an ID while its task exists or deletion is unconfirmed.
9. Release an unbound reservation when creation fails and the platform confirms no task was created.
10. Stop allocating and report exhaustion when a role's ID range has no available ID; do not silently widen or collide with another range.
11. Keep coordinator IDs unique among existing tasks; distinguish reused coordinator IDs by cycle and platform identifier.
12. Use coordination IDs as ledger labels when the platform does not support changing its own IDs.

## Approve children

1. Require an executor or inspector to ask the coordinator before creating a child task or sub-agent.
2. Let the coordinator approve or deny the request at its discretion after checking scope, authority, available IDs, usage, and the shared concurrency and resource limits.
3. Count all running visible chats, including children and successor chats, against the coordinator-plus-two limit.
4. Count nested work against the two-heavy-worker limit and any stricter platform limit.
5. Queue the request when capacity is unavailable; do not create it until approved and capacity exists.

## Delete and release

1. Require the parent executor or inspector to preserve the child's required results, evidence, and handoff, then delete the completed child using an authorized supported deletion capability.
2. Allow the coordinator to perform the same cleanup for completed task-created children when the parent cannot do so.
3. Check that the child has stopped, its descendants are closed, and no work or required records will be lost before deletion.
4. Apply applicable authorization and irreversible-action rules; do not delete a pre-existing user task or an active child.
5. Confirm deletion with the platform before marking the ID available for reuse; retain the registry history and distinguish each reuse by creation order and platform identifier.
6. Do not equate archiving, hiding, interruption, or a request to delete with confirmed deletion.
7. When deletion is unavailable, denied, or unconfirmed, preserve the child and reserve its ID; report the limitation and use another available ID.

## Coordinator rollover

1. When coordinator `0009` takes responsibility, preserve the handoff and required evidence for predecessors `0000` through `0008`.
2. Delete each eligible task-created predecessor that has stopped when an authorized deletion capability is available; confirm each deletion and release its ID.
3. Keep any pre-existing, active, protected, or unconfirmed predecessor and its ID reserved; report the limitation.
4. When `0009` completes its assigned work, create a successor with ID `0000` only after the previous `0000` has been confirmed deleted and a visible-chat slot is available.
5. In the handoff, instruct the new `0000` to preserve the required records and delete the retired `0009` after it has stopped, subject to the same deletion and confirmation rules.
6. Obtain the successor's acknowledgment, transfer the sole coordinator role, notify the user, and stop `0009` before the successor deletes it.
7. If the previous `0000` cannot be deleted or deletion cannot be confirmed, keep its ID reserved, report the blocker, and do not create another `0000` or claim rollover succeeded.
8. Record the cycle, platform identifiers, handoff, deletion results, and ID reuse in the registry.

## Retained-child threshold

1. Count retained task-created children across executor and inspector roles in one shared bucket, including active and completed children that still exist.
2. When the count exceeds ten, have the coordinator select the oldest eligible completed children across both roles and delete up to seven, subject to the deletion checks above.
3. If fewer than seven are eligible, delete only those eligible; never delete running tasks or required records to reach the target.
4. Record actual deletions, reserved IDs, and remaining children. The threshold does not authorize exceeding the active-chat or worker limits.
