# Contributor Rules

## Baseline

`AGENTS.md` governs the current repository. Move procedures, examples, templates, and deep domain guidance into skills, `references/`, `assets/`, or docs. If a rule applies only when a specific skill is active, put it in that skill instead of here.

## Sovereign Drafter

This repository supports the Sovereign Drafter persona for legal drafting tasks. Read `legalese/SKILL.md` before any legal drafting work begins. That file contains the complete instruction set: the nine core architectural doctrines, the Chain of Legal Thought (CoLT) execution protocol, and pointers to the supporting reference, example, and asset files.

Legal drafting tasks include elevating layman or rudimentary text into authoritative legal language, drafting constitutional provisions, commercial instruments, annexes, or any clause where sovereign authority and structural precision are required.

## Repo Rules

This repository contains agent skills. Keep changes intentional, reviewable, and grounded in the current repository.

### Working Rules

- Treat `sources/` as source material, not as content to copy wholesale. Extract reusable methods, constraints, and patterns into local skills, references, assets, and scripts.
- Keep `SKILL.md` files concise, procedural, and easy to route from the description alone. Move long domain detail into `references/`. Move reusable output shells into `assets/`. Add scripts only when deterministic tooling earns their maintenance cost.
- Do not commit secrets, client-confidential content, internal URLs, or private strategy.
- Prefer Writerside-compatible documentation conventions for docs-facing artifacts unless a task explicitly asks for another format.

### Edit Permission

- Unless the user explicitly asks for a file update, assume counsel is expected before modification.
- Treat a request as explicit permission to modify files when the user directly asks to `update`, `edit`, `change`, `fix`, `rewrite`, `refactor`, `implement`, `add`, `remove`, `replace`, `correct`, or `apply` a change to a file, document, topic, skill, rule, or repo artifact; asks for a plan and then explicitly says to implement it; asks a `can you fix/add/update this?` style question whose natural completion is a file change; or asks to address a review comment, fix a bug, or revise a document where the outcome plainly requires modification.
- Do not treat requests to explain, assess, confirm, review, critique, summarize, inspect, compare, advise, or plan as explicit permission to edit unless the user also asks for implementation.
- When explicit permission is absent, modify files only if the file contains a factual error verifiable from local evidence, a broken link or malformed structure, materially stale guidance relative to nearby source-of-truth files, or missing required documentation that can be added safely from local evidence.
- Ask before replacing disputed wording, changing scope or policy, adding unverifiable claims, or performing broad editorial cleanup whose main issue is taste rather than correctness.

### Continuity

- Read this `AGENTS.md` before substantial work and check `handoffs/` when it exists.
- Prefer the latest relevant handoff over older notes. Use only the details that matter to the current task.
- Treat handoffs as continuity aids, not as permanent policy. If a handoff conflicts with this file or the user's latest instruction, follow the higher-priority source and note the conflict when it matters.
- Create or update a handoff when work is about to move to a new chat, a major decision was made, a repo-structure change was completed, a migration phase pauses, or the next agent would otherwise need to reconstruct scattered context.
- Do not create a handoff for every small edit. Do not delete handoff documents unless the user explicitly requests it.

### Tooling and Dependencies

- If a required environment library, CLI tool, or package is missing, the agent may attempt to install it when the installation is necessary to complete the requested task.
- Prefer project-local or temporary installs over global/system installs where practical.
- Ask for approval before network downloads, global installs, system package changes, or changes outside the workspace.
- Record any installed tool or dependency when it affects reproducibility.