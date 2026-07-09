---
name: graphify
description: >
  Activate this skill whenever the user asks about codebase architecture,
  code-impact analysis, blast-radius mapping, inheritance or dependency chains,
  or compliance / regulatory documentation mapping (e.g., "what changes if I
  touch X?", "show me who calls this module", "does the new code satisfy the
  UN compliance PDF?", "map the architecture of the auth layer"). This skill
  integrates CodeGraphContext (CGC) and code-review-graph (CRG) to support
  codebase-impact and architectural analysis. Trigger proactively whenever the
  query requires structural code understanding.
---

# Code Intelligence Integration

Graphify integrates CodeGraphContext (CGC) and code-review-graph (CRG) to
support codebase-impact and architectural analysis.

## Complementary Roles

| Tool | Focus Area | Key Specialty & Strengths |
|---|---|---|
| **code-review-graph (CRG)** | **Change Staging & Impact Analysis** | AST parsing, change detection, blast-radius mapping, callers/callees, affected execution flows, and code reviews. |
| **CodeGraphContext (CGC)** | **Codebase Intelligence & Query Engine** | Semantic code search, dead code detection, cyclomatic complexity profiling, and custom Cypher graph querying. |

---

## Graph Storage Layout

All graph state for this repo lives under a single repo-local directory:

```
graphify/
graphify/cgc/
graphify/crg/
```

`graphify/` is generated output, excluded from Git (see `.gitignore`). Never
commit graph databases, caches, generated reports, sockets, or lock files from
either tool.

When operating inside this repo, prefer repo-local graph state over any
home-directory graph state (`~/.codegraphcontext`, `~/.code-review-graph`,
or any path outside the repo root).

---

## Operating Lifecycle

### 1. Mandatory Generated Tooling Inspection And Cleanup

Before building, updating, or using graph indexes, and again after any graphify,
CRG, or CGC command creates files, inspect generated agent, editor, MCP, and
graph-tooling files across the repository. Do a full pass from the repo root
instead of checking only a short list of known paths. Existing files are not
exempt from review; a file that was already present can still be generated
tooling that does no project work.

The skill terms are not satisfied until the cleanup pass is complete. Generated
graph tooling may remain only in `graphify/` or in the allowed `.agents/`
layout. The allowed `.agents/` layout contains `.agents/brain/` and/or
`.agents/skills/`; when `.agents/skills/` exists, it must contain
`.agents/skills/documentation/SKILL.md`.

Look for stale or generated material such as:

- root instruction duplicates: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `QODER.md`, `.cursorrules`, `.windsurfrules`;
- MCP and agent-client configs: `.mcp.json`, `.opencode.json`, `mcp.json`,
  `opencode.json`;
- assistant-platform folders: `.claude/`, `.gemini/`, `.kiro/`, `.qoder/`;
- assistant-generated instruction folders such as `.github/` when they contain
  graph-tooling or agent instruction scaffolding and do not contain
  project-owned GitHub workflows;
- generated reports such as `CGC_REPORT.md`;
- graph-tool ignore/config files such as `.code-review-graphignore` and
  `.cgcignore` when they were created only for the graph run;
- local editor metadata such as `.idea/` when it is not part of the project;
- stale graph state outside the canonical `graphify/` directory, such as
  `.code-review-graph/` or `.codegraphcontext/`;
- any affiliated generated file elsewhere in the repo that points agents to
  obsolete graph paths, overrides current repo instructions, or duplicates
  platform-specific instructions.

When the user has authorized cleanup:

1. List candidate files and folders from the repo root.
2. Inspect their contents or filenames enough to classify their role.
3. Remove generated/non-project material that matches the cleanup authority.
4. Preserve user-authored project material, durable documentation, source files,
   project-owned GitHub workflows, `graphify/`, and the allowed `.agents/`
   layout.
5. Treat uncertain provenance as user-owned and report it instead of deleting
   it.
6. Run a final repo-root scan and explicitly confirm that no generated
   graphify/CRG/CGC scaffolding remains outside `graphify/` and the allowed
   `.agents/` layout before reporting the skill complete.

Do not restrict cleanup to `.claude/`, `.gemini/`, `.kiro/`, and `.qoder/`.
Those folders are examples, not the full cleanup scope.

### 2. Verification

Before querying the codebase or running analysis, verify that both MCP servers
are reachable. Probe availability using the procedures in
[environment-setup.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/environment-setup.md).
If either tool fails the availability check, follow the recovery instructions.

### 3. Synchronization

Sync the repository indexes before answering the user's prompt:

- Update CRG:
  ```bash
  code-review-graph update --repo . --data-dir graphify/crg
  ```
- Update CGC:
  ```bash
  cgc update --quiet
  ```
  CGC stores its database at the path configured in `FALKORDB_PATH` (or the
  equivalent `KUZUDB_PATH` / `LADYBUGDB_PATH`) inside
  `~/.codegraphcontext/.env`. To redirect a single command to the project-local
  path, pass the global `--path` flag:
  ```bash
  cgc --path graphify/cgc index .
  cgc --path graphify/cgc update --quiet
  ```

### 4. Staging and Implementation Workflow

When designing or implementing a new feature, follow the self-inquiry and
documentation-first staging workflow documented in
[feature-staging-example.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/examples/feature-staging-example.md).

### 5. Tool Routing

Select the appropriate tool for each query using the routing logic in
[tool-routing-guide.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/tool-routing-guide.md).

---

## Index Exclusion Rules

Both tools must exclude the following paths from indexing. For this skills
repository, these patterns live in the committed root ignore files. For other
target repositories, prefer tool-local configuration under `graphify/` unless
the user explicitly asks to install durable root-level ignore files.

**Excluded (generated, transient, or non-project):**

```
graphify/
.code-review-graph/
AGENTS.md
CLAUDE.md
GEMINI.md
QODER.md
.cursorrules
.windsurfrules
.mcp.json
.opencode.json
.github/
.idea/
**/skills/
.agents/skills/
.agents/brain/active/
.agents/brain/archive/
.claude/
.gemini/
.kiro/
.qoder/
```

**Preserved (durable project-owned design material):**

```
.agents/brain/db_design/
```

Do not add `.agents/brain/db_design/` to any ignore file. Its content
represents user-authored design decisions that benefit from graph indexing.

---

## Repo File Requirements

For this skills repository, the following files must exist in the repo root
with the contents described in the subsections below. In another target
repository, create or update these root files only when the user explicitly
asks for durable graph-tool activation. Otherwise treat newly created copies as
generated setup scaffolding and remove them during the mandatory cleanup pass.

### `.gitignore`

Must include `graphify/` so generated graph state is never committed.

### `.code-review-graphignore`

Controls CRG indexing. Uses glob patterns; `<dir>/**` matches at any depth.
See [repository-activation.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/repository-activation.md)
for the required contents.

### `.cgcignore`

Controls CGC indexing. Uses gitignore-style syntax. CGC discovers this file
by walking up from the indexed path to the git root, so placing it at the repo
root ensures it applies to all invocations.
See [repository-activation.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/repository-activation.md)
for the required contents.

---

## Reference Documents

*   [environment-setup.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/environment-setup.md): Installing and setting up the environment from zero.
*   [repository-activation.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/repository-activation.md): Activating both graph tools in a local repository.
*   [tool-routing-guide.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/tool-routing-guide.md): Choosing the right tool for specific query types.
*   [recovery-runbook.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/recovery-runbook.md): Detailed troubleshooting steps for common installation and runtime errors.
*   [feature-staging-example.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/examples/feature-staging-example.md): Walkthrough of a feature staging workflow.
