# Design Workflow

## Artifact Path

Use this path unless the project has a stronger local convention:

| Stage | Location | Content |
| --- | --- | --- |
| Brainstorming | Chat | Tradeoffs, sketches, naming debates, workflow examples, traps, and user decisions. |
| Refined working notes | `.agents/brain/<domain>/...` | Settled or near-settled design records, table candidates, diagram candidates, examples, responsibilities, open questions, and rejected approaches. |
| Maintained documentation | `docs/topics/...` or project docs path | Stable reader-facing prose, reference tables, guides, and data dictionaries. |
| Diagram source and export | `docs/diagrams/...` or project diagram path | Editable Draw.io source and generated documentation exports. |
| Implementation | Source, migration, or config paths | Code, migrations, tests, and runtime assets after design acceptance. |

## Working Rhythm

1. Reason in chat while the design is still unstable.
2. Use concrete scenarios to expose traps before naming tables, classes,
   states, or activities.
3. Ask the user to choose between meaningful tradeoffs when local sources
   cannot answer the decision.
4. Record accepted design pieces in `.agents/brain` with enough detail for a
   future contributor to understand them without the chat.
5. Promote only stable design into maintained documentation, diagrams, or
   implementation.

## Brain Notes Are Not Throwaway

Settled brainstorm files are source material. Write them clearly enough that
later documentation can reuse tables, examples, and responsibilities with
minor editing instead of reconstructing the design from memory.

## Routing To Other Skills

Use `documentation` when the task becomes reader-facing prose, Writerside
structure, data dictionaries, setup guides, reference pages, or cleanup of weak
writing.

Use `technical-diagrams` when the task becomes a production diagram, Draw.io
source, SVG export, visual QA, or diagram bundle.

Use `maestro` when a design effort spans multiple sessions, needs a durable
task tracker, or should preserve a long-running sequence of decisions.

