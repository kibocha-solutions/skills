# Delegation and Resource Controls

## Channel selection

1. Use a visible chat for sustained execution, independent inspection, a user-visible workstream, or a successor coordinator.
2. Use a sub-agent only for a narrow, self-contained assignment that does not need its own user-facing lifecycle.
3. Do not create a sub-agent for every small operation. An executor or inspector may request a child task or sub-agent through the coordinator.
4. Let the coordinator approve or decline each child request at its discretion within platform permissions, the visible-chat cap, and shared usage and workload limits.
5. Share the overall usage budget and the two-heavy-worker limit across the entire team, including nested agents.
6. Record every active worker, parent, assignment, budget, and state in the coordinator ledger.
7. Honor lower platform concurrency limits and do not represent a sub-agent as a visible chat.

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
15. Initiate controlled pause, durable handoff recording, context compaction when supported, and authorized post-reset wake-up when team usage reaches 95% of the 5-hour window (5% remaining) or 98% of the weekly window (2% remaining).

## Shared resources

1. Inventory existing services, data, ports, and working trees before work starts.
2. Assign one owner and record each shared service's purpose, state, and permitted operations.
3. Reuse authorized resources; do not create a separate container or service per worker.
4. Schedule at most two concurrent heavy operations across all chats and sub-agents.
5. Collect related audit findings before compatible fixes and refresh once for the batch when authorized.
6. Preserve shared data and obtain required maintenance authorization before service, schema, or data changes.

## Heartbeat, wake timer, and persistence checklist

1. Confirm at startup whether timers/cron, one-shot wake, usage-window checks, and messaging work; if any fails after inspecting docs/schemas and attempting it, report the failure to the user per `AGENTS.md` Section 12.
2. Keep one 30-minute active heartbeat running during active work (`references/heartbeat-and-wake.md`), or one 90-minute blocked heartbeat if waiting exclusively on user action.
3. Enforce strict mutual exclusion: cancel any active heartbeat before scheduling a wake timer, and cancel any active wake timer before starting a heartbeat.
4. At 95% 5-hour or 98% weekly usage, persist state to `.agents/brain/sessions/active/` and `.agents/brain/handoffs/`, cancel the heartbeat, and schedule a post-reset wake timer.
