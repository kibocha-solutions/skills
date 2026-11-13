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

1. Match model and reasoning effort to task complexity, required tools, accuracy, and cost.
2. Prefer a lighter model for precise bounded work when it meets the acceptance criteria.
3. Use stronger reasoning for ambiguous decomposition, difficult diagnosis, or judgment-heavy review.
4. Set a time or tool-call budget when the runtime supports enforcement.
5. Check material output at each review point and narrow or reassign stalled work.
6. Do not invent quota data or claim that a timeout proves completion.

## Shared resources

1. Inventory existing services, data, ports, and working trees before work starts.
2. Assign one owner and record each shared service's purpose, state, and permitted operations.
3. Reuse authorized resources; do not create a separate container or service per worker.
4. Schedule at most two concurrent heavy operations across all chats and sub-agents.
5. Collect related audit findings before compatible fixes and refresh once for the batch when authorized.
6. Preserve shared data and obtain required maintenance authorization before service, schema, or data changes.
