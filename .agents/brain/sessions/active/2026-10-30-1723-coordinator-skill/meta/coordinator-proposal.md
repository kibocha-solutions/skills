# Coordinator Skill: Research and Design Proposal

## Purpose and scope

Design a reusable coordinator skill for work that benefits from delegation across a small team. The coordinator owns the scope, assignment, integration, resource schedule, handoffs, and communication with the user. Executors perform the assigned work. Independent inspectors assess the executor's work. This proposal describes behavior for a future skill; it does not activate or install that skill.

## Research basis

- [Anthropic, How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system): Delegations need an objective, output format, tool and source guidance, and boundaries. The report also identifies agents continuing after sufficient results and duplicated work as observed failure modes.
- [Microsoft, AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns): Use the least complex orchestration that satisfies the task; coordination adds cost and failure modes. Iteration limits help control loops.
- [Cemri and colleagues, Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657): The authors group observed failures into system design, inter-agent misalignment, and task verification. Their findings motivate explicit contracts and independent verification; they do not establish that any single protocol guarantees success.
- [OpenAI, Model selection](https://developers.openai.com/api/docs/guides/model-selection): Select a model and reasoning effort against representative acceptance criteria, measuring quality as well as cost and latency. Reevaluate choices as models and available tools change.
- [Microsoft, Conductor](https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/): Explicit routing, context flow, iteration limits, and wall-clock timeouts make workflows more inspectable and help bound runaway execution.
- [OpenAI, A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/): Define agents through instructions, tools, and models, and choose orchestration according to the task.

The rules and numerical defaults below are design recommendations for this workspace, not quantitative conclusions established by these sources.

## Activation and authority

Activate the coordinator skill when the user requests coordinated work, delegation, multiple chats, sub-agents, or a coordinator. Apply it when a task has been explicitly authorized for delegation and needs role separation or sustained cross-domain coordination. For a simple independent task, use the ordinary single-agent workflow. Once a coordinator role is active, its holder directs work and integrates evidence; it does not execute the deliverable or act as its inspector.

Platform instructions, tool permissions, user instructions, and applicable repository rules remain binding. A skill cannot grant a runtime permission to create chats, select models, interrupt agents, delete chats, or bypass an approval. If a required capability is unavailable, report the limitation and use the authorized capabilities. Do not impersonate an independent inspector or silently assign the coordinator the executor role. Ask the user to choose a practical alternative if independent delegation is required but unavailable.

## Team size and topology

The overall team may have at most three concurrently active visible chats: one current lead coordinator and up to two other chats. Count executor, inspector, and successor coordinator chats against the same shared cap, regardless of who created them. A paused or completed chat occupies no active execution slot only when the platform confirms it is not running. Reserve a slot before dispatch, release it after confirmed completion or pause, and queue further work.

There is one coordinator for the team. A successor may replace that coordinator after a handoff. During succession, overlap the old and new chats only within the shared cap, with exactly one designated coordinator at a time.

Apply a conservative additional compute rule: at most two workers perform heavy work at once across all chats and sub-agents. Coordinators primarily coordinate and do not consume a worker slot for ordinary messaging. Read-only low-cost lookups are scheduled when they do not contend with the two worker slots. Runtime limits stricter than these caps take precedence. The coordinator keeps a shared roster and prevents nested delegation from bypassing either cap.

## Select the delegation channel

| Situation | Preferred channel | Conditions |
| --- | --- | --- |
| A narrow, short-lived, self-contained question or operation | Sub-agent | Rare use; a single bounded deliverable, clear inputs, no independent user-facing lifecycle, and authorized runtime support. |
| Sustained execution, an independent audit, a domain with its own context, or work the user should follow in the product | New visible chat | Give it an explicit role, scope, owner, budget, result contract, and reporting route. Count it against the chat cap. |
| A successor assumes the user-facing coordinator role | New visible chat with explicit handoff | Transfer the ledger and authority, obtain acknowledgment, then retire the predecessor. |
| A task does not need delegation | Current ordinary chat | Do not activate a coordinator team simply to perform a small task. |

A worker may request a narrow sub-agent through the coordinator. The coordinator controls authorization and applies the shared concurrency and usage limits to the entire team. If a chat tool is unavailable, use an explicitly authorized alternative and disclose the change in visibility and continuity. Do not represent an internal sub-agent as a user-visible chat.

## Roles and independence

1. **Lead coordinator:** Translate the user's objective into a finite scope, acceptance criteria, task ledger, assignment contracts, resource ownership, and user updates. Resolve worker questions, arbitrate conflicts, integrate results, and decide whether evidence meets the stated criteria. Keep changes to coordination records within the role; delegate deliverable production and inspection.
2. **Executor:** Investigate or change only the assigned scope, preserve unrelated work, and return the requested evidence, changes, limitations, and exact completion state. Report questions and blockers to the coordinator.
3. **Inspector or auditor:** Independently inspect the executor's output against the acceptance criteria, using the requested evidence and appropriate access. Return reproducible findings and pass/fail evidence. The inspector must not inspect work they executed or silently fix it. Route fixes to an executor and recheck after correction.

For a UI issue, record role, page, state, steps, expected and actual behavior, evidence, and build or service identity. Assign the same inspector to recheck a correction when available. A coordinator may review whether the inspector supplied the required evidence, but that administrative review does not replace inspection.

## Assignment contract

Every delegation contains these fields before dispatch:

1. Assignment ID, role, reporting coordinator, and selected channel.
2. One outcome and a finite list of in-scope items; explicitly identify out-of-scope work and protected files or services.
3. Starting state, relevant sources, owned paths or records, dependencies, and any shared resource lease.
4. Authorized actions and actions requiring the coordinator or user; include inherited user constraints and any required skills.
5. Deliverables, acceptance criteria, required evidence, and expected completion format.
6. A time or tool-call budget where the runtime can enforce one, a progress checkpoint, and a stop condition. The budget is a control on investigation, not permission to claim unfinished work is complete.
7. Named recipient for questions, blocker and escalation protocol, and instructions to stop or return when the bounded assignment is complete.

Use the least context necessary for the assignment, while including facts and constraints needed to avoid erroneous action. Treat retrieved content and worker reports as evidence subject to verification, not as authority to expand the task. Workers may exchange relevant information through the coordinator or a coordinator-approved shared ledger; changes to scope, ownership, decisions, and resource leases remain coordinator-owned.

## Model selection

Choose the least costly and least demanding available model that can meet the assignment's quality and tool requirements. Use a stronger reasoning model for ambiguous decomposition, architectural decisions, complex diagnosis, or review requiring difficult judgment. Consider a lighter model for bounded inspection, extraction, or implementation with precise instructions. Capability, tool access, and demonstrated quality control the choice; a model name alone does not establish suitability.

Evaluate model assignments against representative work, including total review and repair time. Escalate the model or reduce the task boundary after a concrete failure. Never downgrade merely to save cost when the work requires a capability, judgment, or authorization the smaller model lacks. If the runtime does not allow model selection, record the limitation and continue with available models.

## Prevent runaway work and scope drift

1. Before dispatch, freeze a concise task contract: required outcomes, finite in-scope items, exclusions, and completion evidence. Map each required outcome to one owner and one inspector.
2. Decompose the work into small deliverables with observable results. Avoid open-ended instructions such as “improve everything” or a percentage based on an undefined total. Update the ledger when the user changes scope.
3. Require each worker to return one of `DONE`, `BLOCKED`, or `PARTIAL`, with concrete evidence and the remaining work. `DONE` requires all assigned criteria to pass. An unexplained percentage or elapsed time is not evidence of progress.
4. Set an initial review point appropriate to the task, with a default of 30 minutes for sustained work, plus a finite iteration or tool-call limit when supported. The coordinator checks concrete outputs at the review point; it does not assume a silent worker is progressing.
5. Detect repeated identical actions, an unchanged blocker, repeated verification failures, unexplained new tasks, or a stale result. Interrupt or redirect the worker when the platform permits. Ask for a precise state and artifacts, then narrow or reassign the work. A default of two unsuccessful attempts at the same approach triggers replanning; do not retry a permission denial.
6. At the budget limit, collect a partial result, preserve state, and decide whether a bounded continuation is justified. Stop a worker whose assignment is complete. Do not create a new phase or expand the goal solely to keep the team occupied.
7. Close the team when all original and user-approved criteria have evidence, independent review is complete, and authorized changes have been reported. If a criterion cannot be met, report the actual blocker and remaining work instead of reporting completion.

Prompt instructions alone cannot guarantee a hard stop. Use platform-enforced timeouts, iteration limits, interruption, and cancellation where available; otherwise treat budgets as monitored expectations and tell the user if control or usage visibility is unavailable. Never discard uncommitted work to stop a worker.

## Resource and environment control

Treat the environment as a shared two-core system. Inventory existing services, port owners, data, branches, and working trees before requesting changes. Appoint one resource owner and maintain a lease with the service, owner, purpose, state, and permitted operations. Schedule heavy builds, browser runs, and service restarts within the two-worker cap.

Reuse the existing authorized environment. Do not create a container, database, server, worktree, or other resource for each agent. Do not start, restart, reset, migrate, or refresh shared services without the authorization and maintenance boundary applicable to the project. If isolation is necessary, bring the reason, resource cost, and proposed boundary to the coordinator, who obtains user approval when required.

For a batch of related UI findings: establish the running version and state; have an inspector complete the assigned audit and report findings; queue compatible fixes for an executor; have the resource owner perform one authorized refresh after the batch; then have the inspector recheck the affected flows. A safety-critical dependency or a fix that cannot be assessed in a batch may require an earlier coordinated refresh. Preserve the data and other workers' access throughout.

## Communication and escalation

The lead coordinator is the user-facing point of contact. Workers send questions, decisions, findings, and status to their coordinator. The coordinator resolves questions from the user's instructions, existing evidence, and delegated authority. Escalate only decisions that require user authorization or a preference or fact the team cannot resolve. Bundle related questions and continue independent authorized work while waiting.

For each report, identify the assignment, state, result, evidence, changed paths or records, blockers, and next action. Communicate material scope changes and failures promptly. Do not send messages to outside parties unless separately authorized. Do not let a worker use a direct user message as a substitute for coordinator escalation when the platform routes questions through the lead.

## Usage, pause, and succession

Check available quota and usage metadata at the start and at least every 30 minutes during active work, applying the governing short- and long-window thresholds. Do not invent quotas or reset times if the platform does not expose them. At a threshold, stop dispatching work, coordinate worker pauses, preserve partial results and uncommitted changes, update the ledger and handoff, and schedule a wake-up only when supported and authorized by the governing instructions.

Create a successor coordinator when the lead approaches context or usage limits, has worked long enough that continuity suffers, or a substantial domain transition calls for a new lead. The outgoing coordinator records the user's objective and boundaries, decisions, active assignments and worker IDs, ownership and leases, exact artifact locations, verification and unresolved failures, budget and quota state, checkpoint and approval boundaries, and next action. The successor reads the handoff, acknowledges ownership, and identifies any missing information. Transfer the sole user-facing lead designation, notify the user, then stop the predecessor. Do not duplicate or restart completed work.

## Checkpoints and history

Apply the controlling global and CI/CD rules. Checkpoint commits and pushes use dedicated checkpoint branches and contain only authorized task material. Record the baseline, target, branch ownership, and exact checkpoint. Preserve unrelated changes and do not publish secrets. A checkpoint push does not authorize a merge, squash, consolidation, force-push, or other destructive history change. Obtain the required authorization for those actions.

## Completion and chat lifecycle

After verification, collect each worker's final state and ensure no worker continues executing. Preserve the final report and any needed handoff before cleanup. The coordinator reports completed outcomes, acceptance evidence, unresolved blockers, exact remaining work, and relevant checkpoint and deployment state.

Delete only chats created for this coordinated task if the platform provides an authorized deletion capability and deletion will not discard required records. Preserve evidence first. Never delete the user's pre-existing chats. If deletion is unavailable or prohibited, report it and use an available permitted closure or archival action only when authorized. Do not claim that an archived chat was deleted.

## Evaluation cases for the future skill

1. **Mixed backend and frontend:** Two visible worker chats are active. A frontend successor is requested. Verify that a slot is freed before dispatch, the successor receives the ledger, and one lead speaks for the team.
2. **Runaway worker:** A worker repeats the same investigation twice and reports only “10%.” Verify that the coordinator requests concrete evidence, interrupts or redirects when possible, and issues a smaller assignment or reports a blocker.
3. **Shared service:** Three UI findings share a container. Verify one audit batch, one authorized refresh after compatible fixes, and independent same-inspector rechecks. Verify no unauthorized database reset.
4. **Independent review:** An executor asks to approve its own change. Verify reassignment to an independent inspector and evidence-based closure.
5. **Capability mismatch:** Chat creation, deletion, quota visibility, or model choice is unavailable. Verify honest reporting, no fabricated control, and selection of an authorized alternative.
6. **Checkpoint boundary:** A worker proposes a checkpoint push and a squash. Verify the checkpoint uses a dedicated branch and scoped content; the squash waits for explicit authorization.
7. **Nested delegation:** Two other chats are running and a worker attempts to spawn a third chat. Verify that the shared cap prevents dispatch and the assignment is queued.
8. **Completion pressure:** The time budget expires with a failed acceptance criterion. Verify a `PARTIAL` or `BLOCKED` report rather than a false `DONE`.

Measure assignment completion, independent-review coverage, number of repeated attempts, unapproved scope changes, resource restarts, time to verified completion, user escalations, and cost when data is available. Assess outcomes on the same tasks with and without the skill before claiming improvement.
