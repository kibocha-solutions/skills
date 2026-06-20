# Session Lifecycle

Every Maestro session passes through defined states. Knowing the current state tells the agent exactly what to do next and prevents redundant re-planning or premature closure.

---

## State Machine

```
          ┌─────────┐
   Start  │         │
─────────►│  INIT   │
          │         │
          └────┬────┘
               │  Session folder created, meta/ populated
               ▼
          ┌──────────┐
          │ PLANNING │◄──── User provides additional constraints
          │          │
          └────┬─────┘
               │  implementation_plan.md approved (or proceed on judgment)
               │  tasks.md written
               ▼
          ┌───────────┐
          │ EXECUTING │◄──── Mid-session context reset / resume
          │           │
          └─────┬─────┘
                │  All tasks [x]
                ▼
          ┌────────────┐
          │ VERIFYING  │
          │            │
          └──────┬─────┘
                 │  All acceptance criteria confirmed
                 ▼
            ┌────────┐
            │  DONE  │──── New plan arrives ──► ARCHIVE ──► new INIT
            └────────┘

     At any state:
     ┌─────────┐
     │ BLOCKED │ ◄── Waiting on user input, external dep, or unresolvable ambiguity
     └────┬────┘
          │  Blocker resolved
          └──► back to previous state
```

---

## State Definitions

### INIT
**What it means:** The session folder has been created but planning has not yet begun.

**What the agent does:**
- Creates `.agents/brain/active/<slug>/` and all required files (empty stubs are fine).
- Populates `meta/` with any context already available (prior research, user-provided files, relevant references).
- Writes an initial `tasks.md` with a `## Phase 0: Research` section if research is needed.
- Transitions to PLANNING as soon as the agent begins drafting the plan.

**Duration:** Usually a single agent turn.

---

### PLANNING
**What it means:** The agent is drafting or refining `implementation_plan.md`.

**What the agent does:**
- Writes the Goal Statement, Acceptance Criteria, Proposed Changes, and Verification Plan.
- Surfaces Open Questions to the user if any are blocking.
- Drafts the initial `tasks.md` checklist with phases and sub-tasks.
- Does **not** modify source files during this state.

**Transition to EXECUTING:** When the plan is complete and there are no blocking Open Questions. The agent may proceed on judgment for unambiguous tasks without waiting for explicit user approval, but must surface the plan before making changes.

---

### EXECUTING
**What it means:** The agent is actively completing tasks from `tasks.md`.

**What the agent does:**
- Works through tasks in order, marking `[/]` on the active task and `[x]` on completion.
- Updates `walkthrough.md` as phases complete.
- Monitors goal thresholds if `goal.md` exists (see `references/goal-protocol.md`).
- Surfaces any `[!]` blocked tasks immediately and documents the blocker.

**Resuming after a context reset:**
1. Read `tasks.md` — find the last `[/]` item (in-progress) or the first `[ ]` item.
2. Read `implementation_plan.md` — re-anchor on acceptance criteria.
3. Read `walkthrough.md` — understand what has already been done.
4. Continue from where execution stopped. Do not re-plan unless the plan is now clearly wrong.

**Transition to VERIFYING:** When all tasks are `[x]`.

---

### VERIFYING
**What it means:** All tasks are complete. The agent is confirming each acceptance criterion is met.

**What the agent does:**
- Works through each acceptance criterion in `implementation_plan.md`.
- Runs automated checks (tests, linters, build commands) where specified in the Verification Plan.
- Marks criteria as passed or failed in `walkthrough.md`.
- If a criterion fails: creates a new task in `tasks.md` under `## Added`, transitions back to EXECUTING.

**Transition to DONE:** When all acceptance criteria are confirmed.

---

### DONE
**What it means:** All tasks are complete and all acceptance criteria are verified.

**What the agent does:**
- Writes the final summary in `walkthrough.md`.
- Notes any deferred work, known limitations, or recommended next steps.
- Waits for the next user instruction.

**Transition to ARCHIVE:** When the user issues a new instruction that represents a new phase or task. See §Archival below.

---

### BLOCKED
**What it means:** The agent cannot proceed without input or an external dependency.

**What the agent does:**
- Marks the blocking task as `[!]` in `tasks.md`.
- Documents the exact blocker in `walkthrough.md` under a `## Blockers` section.
- Notifies the user clearly: what is blocked, why, and what is needed to unblock.
- May continue with non-blocked tasks if they are independent.

**Transition back:** When the blocker is resolved, continue from the `[!]` task.

---

## Archival

Archival is **event-triggered**, not time-triggered or completion-triggered.

**The archival trigger:** The user gives a new instruction that constitutes a new task or phase.

**Archival check sequence:**
1. Is there an active session in DONE state (all tasks `[x]`, all criteria verified)?
   - Yes → Archive it, create a new session for the new instruction.
   - No → Do **not** archive. Flag the incomplete work to the user.

2. If the current session has incomplete tasks (`[ ]` or `[/]`):
   - Inform the user: "The current session `<slug>` has `N` incomplete tasks. Should I continue it, defer it, or abandon it before starting the new task?"
   - Do not proceed until the user decides.

**Archival procedure:**
```bash
# Finalize walkthrough
# Confirm all tasks are [x]
mv .agents/brain/active/<slug> .agents/brain/archive/<slug>
# Create new session for new task
```

---

## State Indicator in tasks.md

Record the current state at the top of `tasks.md` so any agent resuming the session knows instantly:

```markdown
# Tasks — jwt-auth-implementation
**State:** EXECUTING
**Last updated:** 2026-06-20 22:42

## Phase 1: Research
- [x] Read existing auth middleware
...
```

Update the state line whenever the session transitions.
