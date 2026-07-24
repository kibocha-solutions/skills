# Memory Conventions

This file defines the authoritative format and rules for `.agents/MEMORY.md`
and `.agents/memory/` — durable, cross-agent project knowledge, distinct
from `.agents/brain/` (session-scoped planning, see `brain-conventions.md`)
and `.agents/brain/handoffs/` (in-progress-work continuity).

---

## Root Location

```
<project-root>/
└── .agents/
    ├── MEMORY.md      # concise index, one line per entry
    ├── memory/         # one file per topic
    │   └── <slug>.md
    └── brain/
        ├── sessions/
        │   ├── active/
        │   └── archive/
        └── handoffs/
```

`.agents/MEMORY.md` and `.agents/memory/` are committed to version control,
same as `.agents/brain/`. Any agent — Claude Code, Codex, Gemini CLI,
Copilot, or a human — can read them regardless of which tool wrote them.

---

## Why This Exists, Separately From `brain/` and `brain/handoffs/`

| Mechanism | Scope | Lifespan |
|---|---|---|
| `.agents/brain/sessions/active/<session>/` | One task or session | Archived when the task completes; not re-read by default afterward |
| `.agents/brain/handoffs/` | Continuity of *in-progress* work across a session boundary | Superseded by the next handoff; not a knowledge base |
| `.agents/MEMORY.md` + `.agents/memory/` | Durable facts, decisions, and preferences that outlive any one session | Persists until stale or wrong, then corrected |

A fact belongs in memory when losing it would mean the *next* agent —
possibly weeks later, possibly a different tool — has to re-derive it,
re-ask for it, or re-make the same mistake before getting corrected again.

---

## What NOT to Save Here

- Anything already prescribed in `AGENTS.md` or a skill's `SKILL.md`. Memory
  is descriptive knowledge (what's true, what was decided, what's
  preferred), not a second copy of behavioral rules — duplicating them
  creates two sources of truth that can drift apart.
- Anything derivable by reading the current code, repo structure, or git
  history.
- Session-scoped detail that belongs in a `brain/sessions/active/<session>/`
  folder instead — implementation notes, in-progress task state, research
  specific to one piece of work.
- Secrets, credentials, internal URLs, or client-confidential content — the
  same rule `AGENTS.md`'s Working Rules already states for commits applies
  here, and matters more since this gets written *during* work rather than
  checked only at review time.

---

## Entry Format

Each `.agents/memory/<slug>.md` file:

```markdown
---
name: {{kebab-case-slug, matches the filename}}
description: {{one line, specific enough to judge relevance without opening the file}}
type: {{user, feedback, project, reference}}
---

{{Lead with the fact or rule itself. For feedback/project entries, follow
with a **Why:** line (the reasoning or incident behind it) and a
**How to apply:** line (when this should change agent behavior). Link
related entries with [[slug]].}}
```

**Types**, adapted for a shared repo rather than one person's global
preferences:

- `user` — who's driving this project and how they work: role, priorities,
  how they want to collaborate.
- `feedback` — validated working preferences and corrections: what an agent
  got wrong and was corrected on, or what approach was confirmed as right.
  Record both — corrections alone drift the agent toward excessive caution
  over time.
- `project` — facts about this repo or its deployment that aren't derivable
  from the code: topology, workflows, decisions and their rationale.
- `reference` — pointers to external systems (issue trackers, dashboards,
  docs) relevant to this repo.

## `.agents/MEMORY.md` Itself

Keep it to one line per entry, linking to the topic file — a short list, not
a summary of each entry's content. If it grows long enough that sweeping it
stops being cheap, that's a signal to trim stale entries or split further,
not to let it keep growing.

## Updating an Entry

Read the existing entry before writing a new one on the same topic. Update
in place rather than creating a near-duplicate. Remove or correct an entry
outright when it turns out to be wrong or the situation it described no
longer holds — a stale memory is worse than no memory, because it gets
trusted by default.

## Committing Memory Changes

Memory updates are swept into whatever commit is already in progress and
are not called out in the commit message — see
`.agents/memory/skills-repo-deployment-workflow.md` for the full publish
workflow.
