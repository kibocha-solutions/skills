---
name: coordinator
description: Coordinate delegated work across workers, visible chats, and narrowly scoped sub-agents. Use when the user requests a coordinator, coordinated multi-agent work, delegation across workers or chats, independent executor and auditor roles, team handoff, or management of a delegated project; before any agent starts a new worker, chat, or sub-agent; when applying the graduating wake timer for a coordinator or standalone chat; and when stopping, closing, or deleting workers, chats, or sub-agents an agent started.
---

# Coordinator

A **chat** (or **worker**) is a separate conversation with its own lifecycle controlled by this skill; never call a chat or worker a "session". A **sub-agent** is a worker that runs inside the current chat and returns its result in the same turn. A **session** (or **Maestro session**) is exclusively a work-record folder under `.agents/brain/sessions/`, governed by `maestro/SKILL.md`. Treat every user reference to a "session" as a Maestro session, and treat every user request to "archive" as moving Maestro sessions to `.agents/brain/sessions/archive/`, never as archiving workers or chats. Stop, close, or delete completed workers and chats under Section 6.

Every agent applies [channel selection](references/delegation.md#channel-selection) before starting a worker, chat, or sub-agent, and applies [graduating wake timer controls](references/heartbeat-and-wake.md) for sustained work in either a coordinated team or a standalone chat.

## 1. Assume the mantle of the user

1. Assume the mantle of the user for the entire delegated team: act as the primary decision-maker, resolve operational questions yourself, and drive work to completion without asking the user for go-ahead between phases or tasks.
2. Identify the user's outcome, scope, constraints, repository `approval_mode` (`ask`, `true`, `false`), deadline, and acceptance evidence.
3. Read the active project instructions, global rules, applicable skills, and resume the matching Maestro session (`maestro/SKILL.md` Section 1).
4. Before escalating any question or decision to the user, search and resolve from these sources in order:
   1. Repository memories (`.agents/MEMORY.md`, `.agents/memory/*.md`) and `.agents/brain/approvals.json`.
   2. Global and repository instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/rules/`) and activated `SKILL.md` files.
   3. User rulings recorded in the active Maestro session (`implementation_plan.md`, `tasks.md`, `walkthrough.md`, `goal.md`) and `.agents/brain/handoffs/`.
   4. Repository documentation (`README.md`, `docs/`) and codebase (querying `graphify` first when `graphify-out/graph.json` exists).
5. Escalate to the user ONLY when the answer cannot be found in those four sources and requires a user ruling (under `ask` or `false` mode), or when a physical user action is required (such as approving a gated command or supplying credentials) and the coordinator cannot approve it on the user's behalf.
6. When a worker requires user action or command approval that the coordinator cannot grant, point the user directly to the exact worker (`coordination_id`, `platform_id`, `kind`, `role`) and the exact action needed.
7. Keep one coordinator responsible for the entire team and user communication; delegate execution and independent inspection rather than performing either role as coordinator.
8. Select a single-agent workflow when the request does not require a coordinator or delegated team, while still running the graduating wake timer in [heartbeat and wake](references/heartbeat-and-wake.md) if the task spans long-running or background work.
9. Respect platform and user limits on creating chats, invoking sub-agents, selecting models, and external actions; report an unavailable required capability without simulating independent review.

## 2. Form the team and track workers

1. Limit the team to the coordinator and two other concurrently active visible chats across the whole task.
2. Permit a successor coordinator only as a replacement; keep one designated coordinator at a time, counting an overlapping successor chat toward the three-chat limit during handoff.
3. Assign executor and inspector roles to different agents for each deliverable.
4. Maintain a durable worker registry at `.agents/brain/workers.json` listing every chat and sub-agent under your mandate (`coordination_id`, `platform_id` from `invoke_subagent`/`swarm`/MCP/chat creation, `kind`: `chat` or `subagent`, `role`, `parent_id`, `model`, `state`, `assignment`, `last_checked_at`, and `deletion_confirmed`).
5. Reserve and release slots using confirmed platform state; queue work when a slot is unavailable.
6. Allow an executor or inspector to request a child task or sub-agent from the coordinator; grant requests within shared limits and platform authorization.
7. Keep sub-agents narrow and task-specific; apply the shared usage, concurrency, and resource budget to all nested work.
8. Assign role-based IDs and manage child lifecycles using [task IDs and cleanup](references/task-ids.md).
9. Read [delegation and resource controls](references/delegation.md) for channel selection, model selection, shared resources, and worker limits.

## 3. Delegate bounded work and enforce worker rules

1. Define finite deliverables, exclusions, dependencies, owners, and acceptance evidence before dispatch.
2. Read at least one scenario relevant to the work in [model selection examples](examples/model-selection.md) before choosing a model or dispatching work; apply its principles to other scenarios.
3. Use [assignment and result contracts](references/contracts.md) and [coordination examples](examples/coordination.md) for each assignment and instruct each worker to read at least one relevant example before acting.
4. Explicitly select a lighter available model for every routine, well-defined child task when model selection is supported and permitted; do not inherit the coordinator's model by default, and record the reason when a stronger model is required.
5. Reassess active assignments when the user corrects the model choice; preserve work and use supported controls to redirect or reassign remaining bounded work.
6. Include mandatory **Worker Rules** in every worker brief:
   - Inform the worker explicitly that it is a worker under a coordinator (`parent_id`) and that the user is with the coordinator and will NOT monitor the worker's chat or catch issues unless forwarded.
   - Command the worker to send ALL blockers, questions, concerns, decisions, and completion reports exclusively to its parent/coordinator WITHOUT EXCEPTION.
   - Forbid the worker from waiting silently for user go-ahead or contacting the user directly, and require it to pass the exact same Worker Rules to any child worker it spawns.
7. Do not let a worker expand scope or create resources without coordinator authorization (and user approval when required by `approval_mode`).
8. Keep the coordinator as the sole user-facing contact; format every user escalation or status report as a complete, self-contained brief per `AGENTS.md` Section 12 (never as a summary).
9. Dispatch authorized work directly when the platform permits it; report specific capability or authorization blockers instead of making the user operate a workaround.

## 4. Control progress with the graduating wake timer

1. Maintain `.agents/brain/workers.json`, resource leases, evidence, blockers, and decisions across all active chats and sub-agents.
2. Treat the environment as a shared two-core system; schedule at most two heavy worker operations concurrently.
3. Reuse authorized services and batch audits, compatible fixes, and verification around a coordinated refresh.
4. Run the **graduating algorithmic wake timer** (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`) per `references/heartbeat-and-wake.md` using prompts in `assets/heartbeat-prompts.md`, keeping at most ONE timer active at any moment:
   - Start at `1` minute (`60s`). When no coordinator or standalone-chat action is needed and workers are progressing, graduate through `1m`, `3m`, `5m`, `12m`, `15m`, and `30m` (capped at `30m`).
   - Reset immediately back to `1` minute (`60s`) whenever action is needed (dispatching, answering a worker, unblocking, reviewing, or handling completion), then graduate upward again.
   - On every wake tick: (a) re-read `goal.md`, `implementation_plan.md`, and `tasks.md`; (b) re-read `AGENTS.md`, active skills, memories, `approval_mode`, and user rulings; (c) inspect every worker (`chat` and `subagent`) in `.agents/brain/workers.json`, unblock or assign work to any worker sitting idle or waiting for go-ahead even if it failed to forward its blocker; and (d) persist state and check usage limits.
   - Switch to a `90m-120m` (`1h 30m` to `2h`) user-blocked wake timer ONLY when waiting exclusively on the user to act; once the user acts, cancel it and resume at `1` minute.
   - Stop and cancel ALL wake timers immediately when all assigned work completes.
5. Require `DONE`, `PARTIAL`, or `BLOCKED` with evidence and remaining work; do not accept unsupported percentages as progress.
6. After two unsuccessful repetitions of the same approach, stop and replan; never retry a permission denial.
7. Interrupt or redirect stalled work when supported; preserve partial results and uncommitted changes.
8. Monitor 5-hour and weekly usage windows across the team; when usage reaches `95%` of the 5-hour window (`5%` remaining) or `98%` of the weekly window (`2%` remaining), persist state, cancel the active timer, and schedule the post-reset wake timer per `references/heartbeat-and-wake.md`.
9. Never silently skip a timer, wake, or usage check: inspect platform docs and tool schemas first, attempt the call, and notify the user per `AGENTS.md` Section 12 if it still fails.

## 5. Review and hand off

1. Route executor results to an independent inspector against the assignment's acceptance criteria.
2. Route corrections to an executor and request a recheck by the same inspector when available.
3. Appoint a successor when a context, usage, or domain transition warrants one; transfer scope, decisions, `.agents/brain/workers.json`, resource leases, evidence, blockers, usage state, timer state, and exact resume point.
4. Obtain successor acknowledgment, transfer the coordinator role, notify the user, and stop the predecessor.
5. Follow `approval_mode` and `ci-cd/SKILL.md` for merges, squashes, and consolidation.

## 6. Close the team

1. Stop completed workers, verify no assigned work remains running, and cancel every active wake timer.
2. Close every worker chat and sub-agent started for the task once its result is reported or merged, updating `.agents/brain/workers.json`. Never archive workers or chats when the user asks to archive; archiving moves Maestro sessions under `maestro/SKILL.md`.
3. Preserve required evidence and report outcomes, verification, blockers, and exact remaining work.
4. Delete completed task-created children and release their IDs only after confirmed deletion, following [task IDs and cleanup](references/task-ids.md).
5. Preserve pre-existing user chats; report when deletion is unavailable.

## 7. Pre-completion checklist

Before closing a coordinated project, confirm evidence exists for each item:

- [ ] Active project instructions, global rules, `approval_mode`, and Maestro session read and maintained.
- [ ] Coordinator resolved questions from memories, instructions, user rulings, and docs/code before escalating, and avoided asking the user for routine go-ahead.
- [ ] Every worker (`chat` and `subagent`) recorded with its platform ID and state in `.agents/brain/workers.json` and instructed with the mandatory Worker Rules.
- [ ] Team stayed within the coordinator-plus-two visible-chat limit and two-heavy-worker limit.
- [ ] Executor and inspector roles assigned to separate agents for each deliverable.
- [ ] Lighter model explicitly selected for bounded routine tasks when supported; stronger-model exceptions recorded.
- [ ] Graduating wake timer (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`) followed during active work and all wake timers cancelled upon completion.
- [ ] Usage windows monitored against `95%` 5-hour (`5%` remaining) and `98%` weekly (`2%` remaining) thresholds.
- [ ] Completed task-created children deleted and IDs released only after confirmed deletion.
- [ ] Acceptance criteria verified with concrete evidence; zero unsupported percentage claims.
- [ ] Terminology kept distinct: "session" and "archive" applied exclusively to Maestro sessions, and coordinated conversations referred to as workers or chats (stopped, closed, or deleted, never archived).
- [ ] Zero AI attribution and no U+2014 em dashes in deliverables or reports.
