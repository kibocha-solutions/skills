# Brain Conventions

## Directory layout

```text
<project-root>/.agents/
├── MEMORY.md
├── memory/
└── brain/
    ├── handoffs/
    └── sessions/
        ├── active/
        ├── dormant/
        └── archive/
```

## Session name

Use `YYYY-MM-DD-HHMM-<slug>`.

1. Use local time.
2. Use two to five lowercase words.
3. Separate words with hyphens.
4. Describe the task.
5. Do not use generic slugs such as `task` or `work`.

## Session layout

```text
<session>/
├── meta/
├── implementation_plan.md
├── tasks.md
├── walkthrough.md
├── goal.md
└── wake.md
```

1. Require `implementation_plan.md`, `tasks.md`, and `walkthrough.md` for a full session.
2. Use `meta/` for text sources and research notes. Keep screenshots, renders, logs, traces, and other evidence in `~/.agents/evidence/` through `steward.py store path evidence`.
3. Create `goal.md` only when authorized or required.
4. Let `sessions.py dormant` create `wake.md`; it exists only for a session that has been parked.
5. Keep generated binaries and downloaded datasets out of version control.

## Handoffs

1. Store handoffs in `.agents/brain/handoffs/`.
2. Name each handoff `YYYY-MM-DD-HHMM-<slug>.md`.
3. Record the objective, current task, completed work, changed files, verification, blockers, and next action.
4. Create a handoff before moving substantial unfinished work to another task or chat.
5. Do not use a handoff as permanent policy.
6. Fold a handoff into its Maestro session's walkthrough and delete it when that Maestro session closes.

## Multiple sessions

1. List every active session before creating a new one.
2. Match by objective before slug.
3. Keep independent tasks in separate sessions.
4. Do not merge sessions.
5. Close sessions under the rules in [session lifecycle](session-lifecycle.md#close).

## Version control

1. Keep `.agents/brain/` and `.agents/memory/` in version control unless the project policy says otherwise.
2. Ignore only reproducible generated artifacts within session `meta/` folders.
3. Use `.gitattributes` `export-ignore` for distributions that must omit agent files.
4. Do not remove project continuity files merely to prepare a client export.
