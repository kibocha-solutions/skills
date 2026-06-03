# Contributor Rules

This repository contains agent skills. Keep changes small, intentional, and easy to review.

## Working rules

- Treat `sources/` as source material, not as content to copy wholesale.
- Extract reusable methods, templates, and constraints.
- Keep skill `SKILL.md` files concise and procedural.
- Move detailed domain guidance into `references/`.
- Move reusable output shells into `assets/`.
- Add scripts only when deterministic tooling is worth the maintenance cost.
- Do not commit secrets, client-confidential content, internal URLs, or private strategy.
- Prefer Writerside-compatible documentation conventions for docs-facing artifacts unless a task explicitly asks for another format.
- For software or systems technical documentation, use the `documentation-drafting` skill and its Writerside references. New technical documentation must be Writerside-compatible Markdown.
- For comments, docstrings, or API comment blocks, use `documentation-drafting/references/code-comment-documentation.md`. Comments must explain contract, intent, constraints, side effects, risks, or non-obvious decisions, not restate obvious code.
- Keep comment documentation professional and maintained at the right level:
  - Package/module/file: document responsibility, boundaries, public entry points, generated status, ownership, source of truth, and system-level assumptions.
  - Class: document abstraction, lifecycle, resource ownership, thread safety, mutability, collaborators, and failure modes.
  - Function/method: document caller contract, parameters, returns, side effects, errors, idempotency, ordering, security, and performance when relevant.
  - Line/block: document local intent, invariants, workarounds, security checks, concurrency assumptions, and trade-offs.
- Delete stale or decorative comments. Update comments in the same change that updates behavior.

## Handoff rules

Use handoff documents to preserve continuity across chats while this repository is still being built.

Before starting substantial work:

- Read this `AGENTS.md` file.
- Check `handoffs/` if it exists.
- Prefer the latest relevant handoff document over older notes.
- Use only the handoff details that are relevant to the current request.
- Treat handoffs as continuity aids, not as permanent policy. If a handoff conflicts with `AGENTS.md` or the user's latest instruction, follow the higher-priority source and record the conflict if it matters.

Create or update a handoff when:

- work is about to move to a new chat,
- a major decision was made,
- a repo structure change was completed,
- a skill migration phase pauses before completion, or
- the next agent would otherwise need to reconstruct context from scattered conversation history.

Do not create a handoff for every small edit.

Store handoffs in `handoffs/` as one file per meaningful session or milestone. Use this filename pattern:

```text
handoffs/YYYY-MM-DD-HHMM-short-topic.md
```

Use this structure:

```md
# Handoff: [short topic]

## Datetime

YYYY-MM-DD HH:MM timezone

## Current objective

[What the work is trying to accomplish.]

## State of the repo

[What exists now.]

## Decisions made

- [Decision and reason.]

## Files changed

- [Path]: [what changed]

## Open questions

- [Question]

## Next entry point

1. [First thing the next chat should do]
2. [Second thing]

## Constraints

- [Anything the next agent must not forget.]
```

Agents must not delete handoff documents unless the user explicitly requests it.
