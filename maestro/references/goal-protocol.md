# Goal Protocol

The goal protocol gives long-running sessions an always-on monitor that evaluates progress against defined success criteria and automatically activates responses when thresholds are crossed.

---

## When to Create goal.md

Create `goal.md` when a session:
- Is expected to span more than one chat session
- Has a broad objective that could silently drift
- Involves multiple agents or phases
- Requires autonomous overnight or background execution (e.g., `/goal` mode)

For quick sessions (< 1 hour, single phase), `goal.md` is optional. Offer it; let the user decide.

---

## goal.md Format

```yaml
# goal.md

objective: |
  One clear paragraph describing the ultimate outcome. Written from the user's
  perspective. Describes what success looks like when the work is complete.

success_criteria:
  - id: SC-1
    description: "All API endpoints return correct status codes under test"
    verification: "Run `npm test` — 0 failures"
  - id: SC-2
    description: "Database migration runs without errors on a clean schema"
    verification: "Run `npm run migrate:fresh` — exits 0"
  - id: SC-3
    description: "Walkthrough documents every endpoint added"
    verification: "Manual check: walkthrough lists all routes in routes/"

thresholds:
  progress:
    stall_turns: 4          # Activate if no [x] in N consecutive turns
    action: deepen_plan     # What the agent does: deepen_plan | escalate | pause
  quality:
    warning_signals:
      - "test failure rate > 20%"
      - "agent has retried same task > 2 times"
    action: replan_phase
  scope:
    max_added_tasks_pct: 30 # Activate if Added tasks exceed X% of original count
    action: pause_and_review

escalation:
  notify_user: true         # Always notify user on threshold activation
  recommend_goal_command: true  # Recommend /goal when appropriate
```

---

## The Three Threshold Types

### 1. Progress Threshold

**Detects:** Stalled execution — the agent is working but no tasks are completing.

**Trigger condition:** No task transitions from `[ ]`/`[/]` to `[x]` within `stall_turns` consecutive agent turns.

**Default:** 4 turns without a completion.

**Agent response (`deepen_plan`):**
1. Stop current execution.
2. Re-read `implementation_plan.md` and the stalled task.
3. Decompose the stalled task into smaller sub-tasks and insert them into `tasks.md`.
4. Add a note to `walkthrough.md`: what was stalling and what decomposition was applied.
5. Resume with the first sub-task.

**User notification:** "I've been on `<task>` for `N` turns without progress. I've broken it into smaller steps and am continuing. No action needed from you unless you want to redirect."

**When to recommend `/goal`:** When the task involves a large body of work that would benefit from uninterrupted autonomous execution. Say: "For best results on this task, consider using `/goal` to let me run without context resets."

---

### 2. Quality Threshold

**Detects:** Execution that is completing tasks but producing defective output.

**Trigger conditions (any one):**
- Test failure rate exceeds 20% across the session
- The agent has retried the same logical task more than 2 times
- A verification step fails after the agent declared a task `[x]`

**Agent response (`replan_phase`):**
1. Stop current phase execution.
2. Add a `## Quality Review` section to `walkthrough.md` documenting:
   - Which tasks produced failures
   - What the failure pattern is
   - What root cause is suspected
3. Revise the affected section of `implementation_plan.md` with a corrected approach.
4. Re-create the affected `tasks.md` items as `[ ]` with a note: `[replanned: <reason>]`.
5. Resume with the revised plan.

**User notification:** "I've hit repeated failures on `<area>`. I've revised the approach and am re-executing. See `walkthrough.md` § Quality Review for details."

**When to recommend `/goal`:** When quality issues suggest the task needs sustained focus without interruption.

---

### 3. Scope Threshold

**Detects:** Silent scope creep — the task is growing beyond what was planned.

**Trigger condition:** Tasks added to the `## Added` section of `tasks.md` exceed `max_added_tasks_pct` percent of the original task count.

**Default:** 30%. If the original plan had 10 tasks and 3+ have been added, the threshold is crossed.

**Agent response (`pause_and_review`):**
1. Stop execution immediately.
2. Do not add further tasks.
3. Write a `## Scope Alert` section in `walkthrough.md` listing:
   - Original task count
   - Added task count and percentage
   - Summary of what the added tasks represent
4. Present the scope alert to the user with a clear question: "The task has grown by `N`%. Do you want me to continue with the full expanded scope, trim it back to the original plan, or create a separate session for the added work?"

**Do not proceed until the user responds to a scope alert.**

**When to recommend `/goal`:** Only after the user confirms the expanded scope. If they accept the full scope, recommend `/goal` if the total task count is now large.

---

## Dual Activation: Autonomous + User Notification

When any threshold is triggered, both of the following happen:

**Autonomous (agent acts immediately):**
- Applies the defined `action` for that threshold
- Updates `walkthrough.md` with a clear record of what triggered and what changed
- Updates `tasks.md` to reflect the new plan
- Updates the `State` line in `tasks.md` if transitioning states

**User-facing (agent notifies):**
- Surfaces the condition to the user in plain language
- Explains what autonomous action was taken
- Recommends `/goal` if appropriate (see conditions above)
- Does NOT ask for permission to continue unless the action is `pause_and_review`

Only `pause_and_review` requires user input before continuing. `deepen_plan` and `replan_phase` proceed autonomously after notifying.

---

## Reading goal.md During Execution

The agent checks thresholds at the start of every turn during EXECUTING state:

1. Count turns since last `[x]` → compare to `stall_turns`
2. Count failures and retries → compare to quality signals
3. Count `## Added` tasks → compute percentage of original

If any threshold is crossed, activate before doing anything else in that turn.

---

## Updating goal.md

`goal.md` may be updated if:
- The user explicitly changes the objective
- A scope review results in a formally approved expanded scope
- Success criteria are revised after new information emerges

Always note the change at the bottom of `goal.md`:

```markdown
## Change Log
- 2026-06-21 09:15 — Added SC-4 after discovering auth flow requires refresh tokens (user confirmed)
```

Never silently change success criteria. The change log is mandatory.
