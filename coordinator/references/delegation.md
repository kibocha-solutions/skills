# Delegation and Resource Controls

## Channel selection

Every agent applies these rules, with or without a coordinated team:

1. Do the work in the current chat by default.
2. Use a sub-agent for a bounded search, read, test, check, or routine edit whose result the current turn needs. Give it a complete brief and a lighter model.
3. Start a new chat only for independent work that outlives the current turn, needs the user's steering, or ends in its own branch, pull request, or repository change.
4. Never start a chat for part of the current task. Never start a sub-agent for a single command.
5. Keep at most two started chats running at once. Count a coordinated team's chats against the same limit.
6. Close each sub-agent when its result returns. Stop, close, or delete each started worker chat when its work is reported or merged (never archive workers or chats), and report any that cannot be closed or deleted.
7. In a coordinated team, let executors and inspectors request children through the coordinator, which approves within platform permissions, the chat limit, and shared usage limits.
8. Share the usage budget and the two-heavy-worker limit across the whole team, including nested agents, and record every active worker in the coordinator ledger.
9. Honor lower platform concurrency limits and do not represent a sub-agent as a visible chat.

## Model and budget

1. Inspect the available models and the child-creation tool's model-selection capability before dispatch.
2. Explicitly select an available lighter model such as Luna or Haiku for routine, well-defined work when it meets the required quality, tool, and authorization constraints.
3. Do not inherit the coordinator's model by default when an appropriate lighter model can be selected.
4. Reserve a stronger model for work requiring deeper judgment, difficult diagnosis, complex reasoning, or capabilities unavailable in the lighter model.
5. Record the selected model and the task-specific reason when selecting a stronger model; honor a user or runtime requirement that specifies a model.
6. When model choice is unavailable or no suitable lighter model is accessible, record the limitation and use an authorized available model; do not claim that a different model was selected.
7. Escalate or split an assignment when observed results show that the lighter model cannot meet the acceptance criteria.
8. Assign a named screen, state, check, expected result, and evidence to routine inspectors; make product judgments at the coordinator level.
9. Convert an accepted decision into a bounded change with exact behavior, constraints, and verification; assign it to a suitable lighter executor even when the task involves code.
10. Reassess an inherited or active model choice when the user changes the instruction; preserve partial work and reassign remaining work using supported controls.
11. Apply the model-selection principles to tasks beyond the examples; a task category alone does not require a stronger model.
12. Set a time or tool-call budget when the runtime supports enforcement.
13. Check material output at each review point and narrow or reassign stalled work.
14. Do not invent quota data or claim that a timeout proves completion.
15. Initiate the controlled pause in `references/heartbeat-and-wake.md` when team usage reaches a threshold in `SKILL.md` Section 4.

## Shared resources

1. Inventory existing services, data, ports, and working trees before work starts.
2. Assign one owner and record each shared service's purpose, state, and permitted operations.
3. Reuse authorized resources; do not create a separate container or service per worker.
4. Schedule at most two concurrent heavy operations across all chats and sub-agents.
5. Collect related audit findings before compatible fixes and refresh once for the batch when authorized.
6. Preserve shared data and obtain required maintenance authorization before service, schema, or data changes.

## Wake timer and persistence checklist

1. Confirm at startup whether one-shot wake scheduling, usage-window checks, and messaging work; if any fails after inspecting docs/schemas and attempting it, report the failure to the user per `AGENTS.md` Section 12.
2. Run the graduating algorithmic wake timer (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`, resetting to `1m` whenever action is needed) during active work (`references/heartbeat-and-wake.md`), or a `90m-120m` (`1h 30m` to `2h`) user-blocked timer if waiting exclusively on user action.
3. Enforce strict single-timer exclusion: cancel any existing timer before scheduling the next timer, and cancel all timers when work completes.
4. At a usage threshold in `SKILL.md` Section 4, persist state, cancel the active timer, and schedule a post-reset wake timer per `references/heartbeat-and-wake.md`.
