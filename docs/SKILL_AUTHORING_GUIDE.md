# Skill Authoring Guide

This guide is the house standard for writing `SKILL.md` files and for deciding
what belongs in repo governance versus skill-specific instructions.

## Repository Roles

- `AGENTS.md`: repo-level contributor rules for the current repository.
- `<skill>/SKILL.md`: the activation and operating guide for one skill.
- `<skill>/references/`: deep detail, domain background, standards, and longer
  explanations loaded only when needed.
- `<skill>/assets/`: templates, output shells, examples meant for reuse, and
  other supporting artifacts.
- `<skill>/scripts/`: deterministic helpers that reduce repetitive or
  error-prone work.
- `docs/`: house standards for authors, reviewers, portability, and privacy.

Use the lightest file that can carry the instruction without bloating the
agent's default context.

## `AGENTS.md` Standard

`AGENTS.md` is not a portable skill body and not a general operations manual.
It governs the current repository. Keep it compact enough that most of the
context budget remains available for the active project.

### Length Budget

- Keep total `AGENTS.md` length under 1500 words.
- Keep reusable baseline guidance around 200-300 tokens.
- Spend the rest of the budget on rules that matter specifically to the repo in
  front of the agent.

### What Belongs In `AGENTS.md`

- repo scope and intent
- contribution boundaries
- edit-permission rules
- skill-routing rules
- conditional helper-tool rules with clear trigger conditions
- privacy and source-material constraints
- continuity and handoff expectations
- short references to the skills or docs that own deeper procedure

### What Does Not Belong In `AGENTS.md`

- detailed workflow steps
- long examples
- templates and boilerplate shells
- decision tables
- deep domain rules that apply only inside one skill
- repeated guidance already maintained in a first-class skill or doc

Simple rule: if the content needs examples, templates, or workflow steps, move
it out of `AGENTS.md`.

When adding external helper tools such as Graphify to repo rules, include:

- when the tool is worth using
- how to probe whether it is available
- what to do if it is unavailable

Do not list helper tools as unconditional defaults unless they are both broadly
useful and reliably available in the target environment.

## Recommended `AGENTS.md` Shape

Use this order unless the repo has a stronger local need:

1. Purpose or baseline
2. Repo-specific working rules
3. Edit-permission rules
4. Skill routing
5. Continuity or handoff rules

The baseline should explain the role of `AGENTS.md` in a few sentences, then
get out of the way.

## `SKILL.md` Standard

Keep `SKILL.md` concise, procedural, and easy to trigger from the description
alone.

- Put activation guidance in the `description`.
- Put task procedure in the body.
- Move long reference material into `references/`.
- Move reusable output shells into `assets/`.
- Add scripts only when deterministic tooling is worth the maintenance cost.
- Prefer one coherent job per skill.

## Offloading Decision Guide

Use `AGENTS.md` when the rule should apply whenever an agent edits the repo.
Use a skill when the rule applies only after a task is routed there. Use docs
when the material is an authoring or review standard for humans and agents.

When in doubt, choose the location that keeps default context smallest while
still making the rule discoverable.
