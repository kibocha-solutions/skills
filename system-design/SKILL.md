---
name: system-design
description: >
  Reason through system architecture, ERD/database models, UML-style class,
  activity, sequence, state, permission, workflow, integration, and deployment
  designs before implementation, documentation, or diagrams. Use when the user
  wants to design a system, database schema, table set, domain model, process
  flow, state machine, permission model, service boundary, or architecture
  concept; when brainstorming should be recorded into .agents/brain; or when
  bad naming, vague responsibilities, shallow ERD notes, or diagram-ready
  design decisions need correction.
---

# System Design

## Goal

Help the agent reason through system designs in chat, preserve settled
brainstorms as durable working notes, and prepare designs that can later become
documentation, diagrams, migrations, or implementation tasks.

## Core Procedure

1. Identify the design type: ERD, architecture, class model, activity flow,
   sequence flow, state machine, permission model, integration, deployment, or
   mixed design.
2. Gather local truth first: existing docs, planning files, schemas, diagrams,
   decisions, source code, tests, and handoffs. Use authoritative external
   sources when the design touches standards, security, authentication,
   databases, protocols, UML notation, or framework behavior.
3. Brainstorm in chat first. Use realistic workflows, traps, lifecycle changes,
   table-like examples, or flow examples when they help the user reason.
4. Keep names boring, standard, and recognizable. Prefer names that a careful
   intern can interpret without team lore.
5. Once the user accepts a design direction, record the refined brainstorm in
   `.agents/brain/<domain>/...` before promoting it to docs, diagrams,
   migrations, or code.
6. Route maintained prose through the `documentation` skill when the output is
   a reader-facing guide, Writerside topic, data dictionary, or reference page.
7. Route production diagrams through the `technical-diagrams` skill when the
   output needs Draw.io source, SVG export, visual QA, or diagram assets.

## Reference Routing

| Need | Read |
| --- | --- |
| Design workflow and where to place artifacts | `references/design-workflow.md` |
| Naming, responsibilities, and bad design language | `references/naming-and-responsibility.md` |
| ERD, database table, and column design | `references/erd-design.md` |
| Common pitfalls to avoid | `references/bad-patterns.md` |

## Design Rules

- Use plain domain language for names. Avoid clever, vague, or in-house names
  unless the user explicitly accepts them.
- Put explanation in the settled design record, not in overlong names.
- Record concrete examples in settled artifacts. Chat examples should become
  durable notes when they settle the design.
- Treat `.agents/brain` notes as source material for later documentation and
  diagrams. They should be understandable without chat history.
- Keep temporary brainstorms separate from maintained docs and production
  diagrams until the user accepts the design.
- Include common pitfalls and rejected approaches when they prevent future
  confusion.

## ERD Quick Standard

When designing database tables, read `references/erd-design.md`. The settled
table files should include dense responsibilities, datatypes, value/default
rules, clear column notes, sample values where useful, example rows with
random non-guessable IDs, and a short normalization check when table placement
is disputed.
