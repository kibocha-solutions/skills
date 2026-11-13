# Assignment and Result Contracts

## Assignment

Include each field in a delegation:

1. Coordination ID, parent ID, role, coordinator, platform task identifier, channel, and model when selectable.
2. One finite outcome, inputs, owned paths or records, and exclusions.
3. Authorized actions, prohibited actions, dependencies, and resource lease.
4. Deliverables, acceptance criteria, evidence, and independent inspector.
5. Time or tool-call budget, review point, stop condition, and escalation route.
6. Inherited user constraints and applicable skills.
7. The parent recipient, supported message channel, and requirement to notify the parent on completion, blockage, or a required decision; pass the same requirement to any children.
8. At least one relevant example to read before acting, and the corresponding principles to apply to the assignment.

## Result

Require the worker to return:

1. Assignment ID and `DONE`, `PARTIAL`, or `BLOCKED`.
2. Deliverable locations, changed files or records, and concrete evidence.
3. Unmet criteria, blockers, attempted approaches, and exact next action.
4. Resource and uncommitted-work state.

Mark `DONE` only when all assigned criteria pass. A budget limit produces a partial or blocked result when work remains. The inspector returns independent evidence and routes corrections through the coordinator.

## Reporting and escalation

1. Send the result to the parent using the available agent or chat messaging capability as soon as the assignment ends; do not wait for the user to read the worker's chat.
2. Notify the parent promptly when blocked, when a decision or credentials are required, or when a material concern affects the assignment.
3. Describe the required action without sending secrets through messages; use the authorized secure credential flow.
4. Have each parent acknowledge reports, collect its children's results, and forward unresolved issues and the consolidated outcome to its own parent until they reach the coordinator.
5. Have the coordinator resolve what it can and communicate required user action or the final result to the user.
6. If a message cannot be delivered, preserve the report in the shared ledger, record the failed delivery, and use an available permitted alternate channel; notify the coordinator when reachable.
7. Have the coordinator monitor pending assignments and retrieve their state when no report arrives at the agreed review point.

## Parent question routing and self-contained escalations

1. Every delegation contract must instruct the worker to direct all questions, blockers, and status reports exclusively to its parent, and to pass the same rule to any child workers it spawns.
2. The parent must resolve worker questions using available authority, repository files, and verified evidence; the parent escalates to the user only when user action or authorization is required and the agent has no way to resolve it.
3. Any escalation, status update, or request for user intervention must follow `AGENTS.md` Section 12 in full (never a summary), providing: plain problem statement, root cause from actual investigation, what was tried and its result, what was considered and why not tried, exact blocker, clearly defined options with consequences, recommended option and why, and exact action requested.
