# Assignment and Result Contracts

## Assignment

Include each field in a delegation:

1. ID, role, coordinator, channel, and model when selectable.
2. One finite outcome, inputs, owned paths or records, and exclusions.
3. Authorized actions, prohibited actions, dependencies, and resource lease.
4. Deliverables, acceptance criteria, evidence, and independent inspector.
5. Time or tool-call budget, review point, stop condition, and escalation route.
6. Inherited user constraints and applicable skills.

## Result

Require the worker to return:

1. Assignment ID and `DONE`, `PARTIAL`, or `BLOCKED`.
2. Deliverable locations, changed files or records, and concrete evidence.
3. Unmet criteria, blockers, attempted approaches, and exact next action.
4. Resource and uncommitted-work state.

Mark `DONE` only when all assigned criteria pass. A budget limit produces a partial or blocked result when work remains. The inspector returns independent evidence and routes corrections through the coordinator.
