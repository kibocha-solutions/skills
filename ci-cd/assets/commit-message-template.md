# Commit Template

Use this shape for final commits:

```text
type(scope): short imperative summary

Why this change matters, what risk it addresses, or what operator behavior it
changes. Keep the body concise.
```

Keep the title and body focused on the durable repo change. Do not mention
unrelated workspace state, submodule noise, sandbox mechanics, local tooling,
or incidental formatting and punctuation edits unless the user explicitly asks
for those details in the commit message.

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
