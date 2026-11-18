# Assignment and Result Contracts

## Assignment

Include each field in a delegation:

1. Coordination ID, parent ID, role, coordinator, platform task identifier, channel, and model when selectable.
2. One finite outcome, inputs, owned paths or records, and exclusions.
3. Authorized actions, prohibited actions, dependencies, and resource lease.
4. Deliverables, acceptance criteria, evidence, and independent inspector.
5. Time or tool-call budget, review point, stop condition, and escalation route.
6. Inherited user constraints and applicable skills.
7. The parent recipient, supported message channel, and explicit **Worker Rules**: inform the worker that it is a worker under a coordinator, that the user is with the coordinator and will not see unforwarded worker issues, and that ALL blockers, questions, concerns, and completion reports must go to the coordinator/parent WITHOUT EXCEPTION; require passing the exact same rules to any child worker.
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

1. Every delegation contract must instruct the worker that it is a worker under a coordinator, to presume the user is exclusively with the coordinator and will not catch any unforwarded issue, question, or blocker, to send ALL questions, blockers, concerns, and decisions exclusively to its parent/coordinator WITHOUT EXCEPTION, never to wait silently for user go-ahead, and to pass the same rules to any child workers it spawns.
2. The parent/coordinator assumes the mantle of the user and must resolve worker questions only after searching, in order: (a) `.agents/MEMORY.md`, `.agents/memory/*.md`, and `.agents/brain/approvals.json`; (b) global and repo instruction files and active `SKILL.md` files; (c) user rulings in the active Maestro session and `.agents/brain/handoffs/`; and (d) repo docs and codebase (`graphify` first when present). Escalate to the user only when those four sources cannot resolve a required decision or when physical user action (such as approving a gated command) is required, naming the exact worker (`coordination_id`, `platform_id`, `kind`, `role`).
3. Any escalation, status update, or request for user intervention must follow `AGENTS.md` Section 12 in full (never a summary), providing: plain problem statement, root cause from actual investigation, what was tried and its result, what was considered and why not tried, exact blocker, clearly defined options with consequences, recommended option and why, and exact action requested.
