# Contributor Rules

## Baseline

`AGENTS.md` governs the current repository. Move procedures, examples, templates, and deep domain guidance into skills, `references/`, `assets/`, or docs. If a rule applies only when a specific skill is active, put it in that skill instead of here.

## Sovereign Drafter

This repository supports the Sovereign Drafter persona for legal drafting tasks. Read `legalese/SKILL.md` before any legal drafting work begins. That file contains the complete instruction set: the nine core architectural doctrines, the Chain of Legal Thought (CoLT) execution protocol, and pointers to the supporting reference, example, and asset files.

Legal drafting tasks include elevating layman or rudimentary text into authoritative legal language, drafting constitutional provisions, commercial instruments, annexes, or any clause where sovereign authority and structural precision are required.

## Maestro — Planning Protocol

All agents follow the Maestro planning protocol for any substantial or multi-step task. This applies regardless of whether the `maestro` skill is explicitly loaded.

**Before starting substantial work:**
1. Check `.agents/brain/active/` in the project root for an existing session matching the current task (match by slug keywords).
2. If a session exists, read its `tasks.md` and `implementation_plan.md` to resume correctly.
3. If no session exists, create one under `.agents/brain/active/YYYY-MM-DD-HHMM-<slug>/` with `implementation_plan.md`, `tasks.md`, and `walkthrough.md`.

**During execution:**
- Mark tasks `[/]` when starting, `[x]` only when verifiably complete.
- Update `walkthrough.md` as phases finish — do not wait until the end.
- Never expand scope silently; document added tasks in a `## Added` section of `tasks.md`.

**When a new instruction arrives and current tasks are all `[x]`:**
- Finalize `walkthrough.md`, then move the session from `active/` to `archive/`.
- Create a fresh session for the new task.

For the full protocol — session states, goal thresholds, archival rules — read `maestro/SKILL.md` and its `references/` files when the maestro skill is available. When it is not available, follow the rules above as the baseline.

## Repo Rules

This repository contains agent skills. Keep changes intentional, reviewable, and grounded in the current repository.

### Rule Fidelity

- Treat skill prescriptions and prohibitions as behavioral requirements, not
  strings to route around. Do not satisfy a rule by changing surface wording,
  renaming a pattern, swapping synonyms, narrowing a definition, or preserving
  the same defect under a new form.
- When a rule forbids a pattern, the cure is a rewrite that removes the
  underlying defect. Quick paraphrase, cosmetic substitution, and
  checkbox-style compliance are insufficient.
- Apply this standard to every prescription and prohibition in a skill,
  including examples and listed trigger phrases.

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
- Check `.agents/brain/active/` in the project root before starting any substantial task. If a brain session exists for the current work, resume from it rather than starting fresh.
- Prefer the latest relevant handoff over older notes. Use only the details that matter to the current task.
- Treat handoffs as continuity aids, not as permanent policy. If a handoff conflicts with this file or the user's latest instruction, follow the higher-priority source and note the conflict when it matters.
- Create or update a handoff when work is about to move to a new chat, a major decision was made, a repo-structure change was completed, a migration phase pauses, or the next agent would otherwise need to reconstruct scattered context.
- Do not create a handoff for every small edit. Do not delete handoff documents unless the user explicitly requests it.

### Tooling and Dependencies

- If a required environment library, CLI tool, or package is missing, the agent may attempt to install it when the installation is necessary to complete the requested task.
- Prefer project-local or temporary installs over global/system installs where practical.
- Ask for approval before network downloads, global installs, system package changes, or changes outside the workspace.
- Record any installed tool or dependency when it affects reproducibility.

### Writerside Validation

- Prefer `wrs` for local Writerside validation. Run `wrs doctor` before
  claiming the Writerside builder is available.
- After changing Writerside topics, snippets, tree files, build profiles, or
  documentation assets, run `wrs build <instance>` for each affected instance
  when Docker is reachable.
- If `wrs`, Docker, or the Writerside builder image is unavailable, use
  `documentation/references/install-writerside.md` before falling back to
  source-only review.
- Do not leave Writerside test artifacts, `.idea/`, or generated build output
  in the project worktree. The `wrs` wrapper writes temporary sources, logs,
  reports, and generated ZIP files outside the repository by default.

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.
