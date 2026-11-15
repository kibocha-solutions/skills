---
name: coordinator
description: Coordinate delegated work across agents, visible chats, and narrowly scoped sub-agents. Use when the user requests a coordinator, coordinated multi-agent work, delegation across chats, independent executor and auditor roles, team handoff, or management of a delegated project; before any agent starts a new chat or a sub-agent; and when cleaning up chats or sub-agents an agent started.
---

# Coordinator

A chat is a separate conversation with its own lifecycle; when the user says "session", the user means a chat. A sub-agent runs inside the current chat and returns its result in the same turn. A Maestro session is the work-record folder under `.agents/brain/sessions/`.

Every agent applies [channel selection](references/delegation.md#channel-selection) before starting a chat or sub-agent, with or without a coordinated team.

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
2. Read at least one scenario relevant to the work in [model selection examples](examples/model-selection.md) before choosing a model or dispatching work; apply its principles to other scenarios.
3. Use [assignment and result contracts](references/contracts.md) and [coordination examples](examples/coordination.md) for each assignment and instruct each worker to read at least one relevant example before acting.
4. Explicitly select a lighter available model for every routine, well-defined child task when model selection is supported and permitted; do not rely on the parent's inherited model.
5. Separate decisions requiring deeper judgment from bounded implementation and inspection; route each part according to its actual requirements.
6. Use a stronger model only when the task requires its judgment or capabilities, the lighter model is unavailable, or the user or governing runtime requires it; record the reason.
7. Reassess active assignments when the user corrects the model choice; preserve work and use supported controls to redirect or reassign the remaining bounded work.
8. Instruct each worker to direct all questions, blockers, and completion reports to its parent (never directly to the user), and require workers to pass the same instruction to their children.
9. Require the parent to make the best decision from available authority and evidence; escalate to the user only when user action is required and the agent has no way to resolve it.
10. Do not let a worker expand scope or create resources without coordinator authorization and any applicable user approval.
11. Require parents to acknowledge child reports and relay unresolved concerns to the coordinator promptly.
12. Keep the coordinator as the sole user-facing contact; format every escalation, status update, or question as a complete, self-contained brief per `AGENTS.md` Section 12 (never as a summary).
13. Dispatch authorized work directly when the platform permits it; if a required action cannot be performed, report the specific capability or authorization blocker.

## 4. Control progress and resources

1. Maintain a shared ledger of assignments, active chats and sub-agents, resource owners, evidence, blockers, and decisions.
2. Treat the environment as a shared two-core system; schedule at most two heavy worker operations concurrently.
3. Reuse authorized services and batch audits, compatible fixes, and verification around a coordinated refresh.
4. Run the 30-minute active heartbeat, 90-minute blocked heartbeat, post-reset wake timer, and state persistence per `references/heartbeat-and-wake.md` using prompts in `assets/heartbeat-prompts.md`; enforce strict mutual exclusion so Heartbeat and Wake Timer are never active at the same time.
5. Require `DONE`, `PARTIAL`, or `BLOCKED` with evidence and remaining work; do not accept an unsupported percentage as progress.
6. After two unsuccessful repetitions of the same approach, stop and replan; never retry a permission denial.
7. Interrupt or redirect stalled work when supported; preserve partial results and uncommitted changes.
8. Monitor 5-hour and weekly usage windows across the team; when usage reaches 95% of the 5-hour window (5% remaining) or 98% of the weekly window (2% remaining), persist state, cancel the active heartbeat, and schedule a post-reset wake timer per `references/heartbeat-and-wake.md`.
9. Never silently skip a timer, wake, or usage check: inspect platform documentation, commands, and tool schemas first, attempt the call, and if it still fails, notify the user per `AGENTS.md` Section 12 and `references/heartbeat-and-wake.md`.

## 5. Review and hand off

1. Route executor results to an independent inspector against the assignment's acceptance criteria.
2. Route corrections to an executor and request a recheck by the same inspector when available.
3. Appoint a successor when a context, usage, or domain transition warrants one.
4. Transfer scope, decisions, assignments, resource leases, evidence, blockers, usage state, and exact resume point.
5. Obtain successor acknowledgment, transfer the coordinator role, notify the user, and stop the predecessor.
6. Require explicit authorization for merges, squashes, and consolidation; apply global checkpoint and CI/CD rules.

## 6. Close the team

1. Stop completed workers and verify that no assigned work remains running.
2. Close or archive every chat and sub-agent started for the task once its result is reported or merged.
3. Preserve required evidence and report outcomes, verification, blockers, and exact remaining work.
4. Delete completed task-created children and release their IDs only after confirmed deletion, following [task IDs and cleanup](references/task-ids.md).
5. Preserve pre-existing user chats; report when deletion is unavailable.

## 7. Pre-completion checklist

Before closing a coordinated project, confirm evidence exists for each item:

- [ ] Active project instructions, constraints, and Maestro session read and maintained.
- [ ] Team stayed within the coordinator-plus-two visible-chat limit and two-heavy-worker limit.
- [ ] Executor and inspector roles assigned to separate agents for each deliverable.
- [ ] Lighter model explicitly selected for bounded routine tasks when supported; stronger-model exceptions recorded.
- [ ] Usage windows monitored against 95% 5-hour (5% remaining) and 98% weekly (2% remaining) thresholds.
- [ ] Completed task-created children deleted and IDs released only after confirmed deletion.
- [ ] Acceptance criteria verified with concrete evidence; zero unsupported percentage claims.
- [ ] Zero AI attribution and no U+2014 em dashes in deliverables or reports.
