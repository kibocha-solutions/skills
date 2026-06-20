# Brain Conventions

This file defines the authoritative directory layout and naming rules for the `.agents/brain/` system.

---

## Root Location

The brain always lives at the **project workspace root**:

```
<project-root>/
└── .agents/
    ├── brain/
    │   ├── active/
    │   └── archive/
    └── skills/        ← skills live here in repos that bundle them
```

The `.agents/brain/` directory is committed to version control. It is part of the project, not a hidden cache. This means any agent — or human — can inspect past sessions, review decisions, and understand the full history of how the project evolved.

---

## Session Naming

Session folders use a fixed format:

```
YYYY-MM-DD-HHMM-<slug>
```

- **YYYY-MM-DD** — ISO date of session creation (local time)
- **HHMM** — 24-hour time of session creation, no colon
- **slug** — 2–5 lowercase words describing the task, hyphen-separated

### Good slug examples
| Task | Slug |
|---|---|
| Refactor product documentation | `product-doc-refactor` |
| Implement JWT authentication | `jwt-auth-implementation` |
| Migrate Postgres to v15 | `postgres-v15-migration` |
| Build admin dashboard UI | `admin-dashboard-ui` |

### Rules
- Slugs describe the **task**, not the outcome ("add-login-page" not "login-done")
- No version numbers in slugs — use the date for versioning
- No abbreviations that aren't universally obvious (use `auth` not `athntctn`)
- Maximum 5 words. If you need more, you have two tasks, not one.

---

## Session Structure

```
.agents/brain/active/<session-slug>/
├── meta/                    # Supporting content
│   ├── research-notes.md    # Research gathered before planning
│   ├── context.md           # Domain context, constraints, decisions
│   └── <anything else>/     # Diagrams, copied reference files, etc.
├── implementation_plan.md   # The contract (required for full sessions)
├── tasks.md                 # Live checklist (required)
├── walkthrough.md           # Completion record (required)
└── goal.md                  # Goal spec + thresholds (optional)
```

### meta/
Anything you want the next agent to have ready without re-researching:
- Notes from web research
- API docs snippets
- Decisions made and why
- Files copied for reference

Keep meta files concise. They are not the walkthrough — they are *inputs* to the plan, not outputs of the work.

### implementation_plan.md
The plan, written before execution starts. See `SKILL.md §3` for the required structure.

### tasks.md
The live checklist, updated continuously during execution. See `SKILL.md §4`.

### walkthrough.md
The completion record. Written for the next agent or human reviewer. See `SKILL.md §5`.

### goal.md
Optional goal specification. See `references/goal-protocol.md` for the format and when to create it.

---

## Active vs. Archive

| State | Location | Meaning |
|---|---|---|
| `active/` | `.agents/brain/active/<slug>/` | Work is in progress or paused |
| `archive/` | `.agents/brain/archive/<slug>/` | Session is complete and frozen |

An archived session is **never modified**. It is a historical record.

When archiving:
1. Ensure `walkthrough.md` is complete and accurate.
2. Ensure all `tasks.md` items are `[x]` or explicitly noted as deferred/abandoned.
3. Move (do not copy) the session folder from `active/` to `archive/`.

```bash
mv .agents/brain/active/<slug> .agents/brain/archive/<slug>
```

---

## Gitignore Considerations

Do **not** gitignore `.agents/brain/`. The entire brain is project history.

You may gitignore large generated artifacts inside `meta/` if they are reproducible (e.g., downloaded datasets, compiled binaries). Mark these clearly in a `meta/README.md`.

Example `.gitignore` entry if needed:
```gitignore
# Reproducible artifacts in brain meta — regenerate with scripts/fetch-data.sh
.agents/brain/**/meta/raw-data/
```

---

## Multiple Active Sessions

A project may have more than one active session simultaneously. This is normal when:
- Multiple independent features are in development
- A blocked session is waiting on user input while another proceeds

When starting work, scan **all** active sessions and identify the most relevant one by slug. If two sessions are equally relevant, read both `implementation_plan.md` files and pick the one that matches the current instruction.

Never merge two active sessions. If work in one session overtakes or obsoletes another, archive the obsolete one with a note in its `walkthrough.md` explaining why.

---

## Searching the Brain

To find a prior session:

```bash
# List all active sessions
ls .agents/brain/active/

# List all archived sessions
ls .agents/brain/archive/

# Search for a topic across all session plans
grep -r "jwt" .agents/brain/ --include="implementation_plan.md" -l

# Find the most recent session
ls -t .agents/brain/active/ | head -1
```
