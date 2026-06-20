---
name: maestro
description: Plan, track, and execute complex multi-session tasks. Use this skill when a task requires structured planning before implementation, spans multiple chat sessions, involves distinct phases (research, build, verify), needs goal-based progress tracking with automatic threshold monitoring, or when the user asks to plan, map out, or orchestrate a project. Activate this skill proactively for any task that cannot be completed in a single straightforward step.
---

# Maestro

Maestro is the agent planning and execution protocol. It gives every complex task a persistent home — a session folder in `.agents/brain/active/` — and keeps the agent oriented across restarts, scope changes, and long execution runs.

Read `references/brain-conventions.md` for the full directory specification.
Read `references/session-lifecycle.md` for the session state machine.
Read `references/goal-protocol.md` for goal activation, threshold monitoring, and archival logic.

---

## 1. Orient First

At the start of any substantial task, before writing a single line of code or making any file change:

1. Check whether `.agents/brain/active/` contains a session for this task.
   - Match by slug (keywords from the task description).
   - If a match exists, read its `implementation_plan.md` and `tasks.md` to resume.
2. If no matching session exists, create one now. See §2.

This step is mandatory. An agent that skips it risks duplicating work or overwriting a prior plan.

---

## 2. Create a Session

Name the session folder using the format: `YYYY-MM-DD-HHMM-<slug>`

- Date/time from the current local time at session creation.
- Slug: 2–5 lowercase words from the task, hyphen-separated. Be descriptive.
  - Good: `2026-06-20-2242-product-doc-refactor`
  - Good: `2026-06-21-0900-api-auth-implementation`
  - Bad: `2026-06-20-2242-task` (too vague)

Create this structure inside `.agents/brain/active/<session-slug>/`:

```
<session-slug>/
├── meta/                    # Supporting content: research notes, references, context
├── implementation_plan.md   # The plan (see §3)
├── tasks.md                 # Live TODO checklist (see §4)
├── walkthrough.md           # Completion record (see §5)
└── goal.md                  # Goal spec + thresholds (see goal-protocol.md — optional but recommended)
```

---

## 3. Write the Implementation Plan

The `implementation_plan.md` is the contract for the task. Write it before touching any code or files.

It must contain:

### Goal Statement
One clear paragraph: what is being built, why, and what "done" looks like from the user's perspective.

### Acceptance Criteria
A numbered list of verifiable conditions. These are not tasks — they are the finish line.

```markdown
## Acceptance Criteria
1. All API endpoints return correct status codes under test.
2. The database migration runs without errors on a clean schema.
3. The walkthrough documents every endpoint added.
```

Acceptance criteria must be falsifiable. "Works correctly" is not a criterion. "Returns 200 for valid inputs and 422 for invalid inputs" is.

### Proposed Changes
Group by component. List files as `[NEW]`, `[MODIFY]`, or `[DELETE]` with a one-line rationale each.

### Open Questions
Any ambiguity that blocks the plan. List these explicitly and stop for user input if they are blocking.

### Verification Plan
How the agent will confirm each acceptance criterion is met before closing the session.

---

## 4. Maintain tasks.md

`tasks.md` is the live execution checklist. Update it continuously as work progresses.

Status markers:
- `[ ]` — not started
- `[/]` — in progress (agent is actively working on this)
- `[x]` — complete
- `[!]` — blocked (waiting for user input or an external dependency)

Rules:
- Mark a task `[/]` when you begin it. Mark it `[x]` only when it is verifiably done.
- Never mark `[x]` based on intent ("I will write the test"). Mark it only after the work exists.
- If you add new tasks mid-execution (scope expansion), add them to a clearly labeled `## Added` section at the bottom. Do not silently expand the original task list.

```markdown
# Tasks — api-auth-implementation

## Phase 1: Research
- [x] Read existing auth middleware
- [x] Document current token flow

## Phase 2: Implementation
- [x] Add JWT validation function
- [/] Wire validation into route handlers
- [ ] Write integration tests

## Phase 3: Verification
- [ ] Run test suite
- [ ] Update walkthrough

## Added
- [ ] Fix token expiry edge case discovered during implementation
```

---

## 5. Maintain walkthrough.md

`walkthrough.md` is the running record of what was done and why. It is written for the *next agent* reading this session, not for the current user.

Update it as phases complete — do not wait until the end.

Include:
- What was changed and the rationale behind non-obvious decisions.
- Commands run and their outcomes.
- Any deviations from the implementation plan, and why.
- Verification results (test output, screenshots if relevant).

---

## 6. Goal Activation

If `goal.md` exists in the session, the agent monitors three thresholds continuously. When any threshold is met, two things happen simultaneously:

1. **Autonomous response** — the agent adjusts its execution strategy (see `references/goal-protocol.md` §3).
2. **User notification** — the agent surfaces the condition clearly and, where appropriate, recommends `/goal` for a deeper autonomous run.

Thresholds are defined in `goal.md`. Read `references/goal-protocol.md` before writing or evaluating `goal.md`.

If `goal.md` does not exist, offer to create one when the task is complex or long-running.

---

## 7. Session Archival

Sessions are archived when a **new plan is issued** and the **prior session's tasks are all complete**.

The lifecycle is:
1. User gives a new instruction or the next phase of work begins.
2. Agent checks the current active session's `tasks.md`.
3. If all tasks are `[x]` (no `[ ]` or `[/]` remaining), finalize the walkthrough, then move the session folder from `active/` to `archive/`.
4. Create a new session for the next phase.

If tasks remain incomplete when a new instruction arrives, do **not** archive. Instead, flag the incomplete work to the user and ask whether to continue, defer, or abandon it.

Do not archive proactively based on task completion alone — wait for the new-plan trigger.

---

## 8. Resuming a Session

When resuming after a context reset or new chat session:

1. Read `tasks.md` to find the current `[/]` and `[ ]` items.
2. Read `implementation_plan.md` to re-anchor on acceptance criteria.
3. Read `walkthrough.md` to understand what was already done.
4. Continue from where the last `[/]` task left off.

Do not re-plan from scratch. The session folder is the source of truth.

---

## 9. Minimal Session (Quick Tasks)

For tasks that are complex enough to warrant a session but too small for a full plan, use a minimal session:

- Create the session folder and `tasks.md`.
- Skip `implementation_plan.md` and `goal.md`.
- Write a brief `walkthrough.md` summary when done.

Use judgment. A 3-step task needs a minimal session. A 30-step task needs the full protocol.
