---
name: coordinator
description: Coordinate delegated work across agents, visible chats, and narrowly scoped sub-agents. Use when the user requests a coordinator, coordinated multi-agent work, delegation across chats, independent executor and auditor roles, team handoff, or management of a delegated project.
---

# Coordinator

## 1. Establish the mandate

1. Identify the user's outcome, scope, constraints, authority, deadline, and acceptance evidence.
2. Read the active project instructions and resume the matching Maestro session.
3. Keep one coordinator responsible for the entire team and user communication.
4. Delegate execution and independent inspection; do not perform either role as coordinator.
5. Select a single-agent workflow when the request does not require a coordinator or delegated team.
6. Respect platform and user limits on creating chats, invoking sub-agents, selecting models, and external actions.
7. Report an unavailable required capability; do not simulate independent review.

## 2. Form the team

1. Limit the team to the coordinator and two other concurrently active visible chats across the whole task.
2. Permit a successor coordinator only as a replacement; keep one designated coordinator at a time.
3. Count a successor's running chat toward the same three-chat limit during handoff.
4. Assign executor and inspector roles to different agents for each deliverable.
5. Reserve and release slots using confirmed platform state; queue work when a slot is unavailable.
6. Allow an executor or inspector to request a child task or sub-agent from the coordinator; grant requests at the coordinator's discretion within the shared limits and platform authorization.
7. Keep sub-agents rare and task-specific; apply the shared usage, concurrency, and resource budget to all nested work.
8. Assign role-based IDs and manage child lifecycles using [task IDs and cleanup](references/task-ids.md).
9. Read [delegation and resource controls](references/delegation.md) for channel selection, model selection, shared resources, and worker limits.

## 3. Delegate bounded work

1. Define finite deliverables, exclusions, dependencies, owners, and acceptance evidence before dispatch.
2. Use [assignment and result contracts](references/contracts.md) for each assignment.
3. Choose the least demanding available model that meets the task's quality, judgment, and tool requirements.
4. Reserve stronger reasoning models for complex analysis and decisions; escalate when evidence shows a lighter model is insufficient.
5. Instruct each worker to message its parent when done, blocked, or needing a decision; require workers to pass the same instruction to their children.
6. Resolve questions from available authority and evidence; escalate to the user only when necessary.
7. Do not let a worker expand scope or create resources without coordinator authorization and any applicable user approval.
8. Require parents to acknowledge child reports and relay unresolved concerns to the coordinator promptly.
9. Keep the coordinator as the sole user-facing contact; request user action only through the coordinator.

## 4. Control progress and resources

1. Maintain a shared ledger of assignments, active chats and sub-agents, resource owners, evidence, blockers, and decisions.
2. Treat the environment as a shared two-core system; schedule at most two heavy worker operations concurrently.
3. Reuse authorized services and batch audits, compatible fixes, and verification around a coordinated refresh.
4. Set a bounded review time and iteration limit where supported; use 30 minutes as the default progress review interval for sustained assignments.
5. Require `DONE`, `PARTIAL`, or `BLOCKED` with evidence and remaining work; do not accept an unsupported percentage as progress.
6. After two unsuccessful repetitions of the same approach, stop and replan; never retry a permission denial.
7. Interrupt or redirect stalled work when supported; preserve partial results and uncommitted changes.
8. Monitor available usage windows under the global rules and coordinate pausing, handoff, and any authorized wake-up.

## 5. Review and hand off

1. Route executor results to an independent inspector against the assignment's acceptance criteria.
2. Route corrections to an executor and request a recheck by the same inspector when available.
3. Appoint a successor when a context, usage, or domain transition warrants one.
4. Transfer scope, decisions, assignments, resource leases, evidence, blockers, usage state, and exact resume point.
5. Obtain successor acknowledgment, transfer the coordinator role, notify the user, and stop the predecessor.
6. Require explicit authorization for merges, squashes, and consolidation; apply global checkpoint and CI/CD rules.

## 6. Close the team

1. Stop completed workers and verify that no assigned work remains running.
2. Preserve required evidence and report outcomes, verification, blockers, and exact remaining work.
3. Delete completed task-created children and release their IDs only after confirmed deletion, following [task IDs and cleanup](references/task-ids.md).
4. Preserve pre-existing user chats; report when deletion is unavailable.
5. Read [examples](examples/coordination.md) for assignment, inspection, and successor patterns.
