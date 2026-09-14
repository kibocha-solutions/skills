# Memory Conventions

## Placement

```text
<project-root>/.agents/
├── MEMORY.md
└── memory/
    └── <topic>.md
```

## Admission test

Save a fact only when all conditions pass:

1. The fact will matter beyond the current session.
2. The fact is not already explicit in current code, documentation, `AGENTS.md`, or a skill.
3. The fact would require meaningful work or user correction to recover.
4. The fact is stable enough to remain useful.
5. The fact contains no secret, internal URL, private strategy, or client-confidential content.

## Topic file

```markdown
---
name: <kebab-case-topic>
description: <one-line routing description>
type: user | feedback | project | reference
---

<durable fact, decision, preference, or reference>
```

1. Match `name` to the filename.
2. Keep one topic per file.
3. Lead with the durable fact.
4. Record its source or verification date when freshness matters.
5. Link related topics by relative Markdown link.

## Memory index

1. Keep `.agents/MEMORY.md` as a concise list of topic links.
2. Give each link a routing phrase.
3. Remove stale or superseded entries.
4. Do not duplicate the topic body in the index.

## Update procedure

1. Read the index and matching topic before writing.
2. Update an existing topic when it covers the same fact.
3. Correct or remove stale facts.
4. Create a new topic only when no existing topic fits.
5. Verify the final index link and topic file.

## Exclusions

1. Keep universal rules in `AGENTS.md`.
2. Keep task procedures in skills.
3. Keep current execution state in active sessions.
4. Keep short transfer context in handoffs.
5. Do not use memory as a second policy authority.
