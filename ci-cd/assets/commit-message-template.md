# Commit Template

Use this shape for final commits:

```text
type(scope): short imperative summary

Why this change matters, what risk it addresses, or what operator behavior it
changes. Keep the body concise.
```

`type` is one of the canonical Conventional Commits types: `feat`, `fix`,
`docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
Summary is a single imperative sentence; body is 72 words or fewer, total.

Keep the title and body focused on the durable repo change. Do not mention
unrelated workspace state, submodule noise, sandbox mechanics, local tooling,
or incidental formatting and punctuation edits unless the user explicitly asks
for those details in the commit message.

Never name or point to an agentic/planning/scaffolding file (`AGENTS.md`,
`design.md`, `implementation-plan.md`, and the like) or a skill by name — see
`SKILL.md`'s Reference Boundary. This holds regardless of where the file
lives and regardless of how obliquely it's described.

Examples:

```text
fix(ci): restore workflow cache key stability

The previous cache key changed on every run, which removed the intended speed
benefit and made failures harder to compare across runs.
```

```text
docs(ci-cd): document autosquash cleanup workflow

The skills repo now expects procedural local commits to be squashed into one
publishable commit before review or handoff.
```
