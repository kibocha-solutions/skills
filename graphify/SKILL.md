---
name: graphify
description: Map codebase architecture, dependencies, callers, execution flows, change impact, test coverage, and compliance relationships with CodeGraphContext and code-review-graph. Use for architecture questions, blast-radius analysis, dependency tracing, structural code review, or mapping requirements to implementation.
---

# Graphify

## 1. Establish scope

1. Identify the repository root.
2. Identify the requested symbol, change, subsystem, requirement, or document.
3. Keep generated graph state under `.agents/code-graphs/`.
4. Keep generated graph state out of version control.
5. Do not create or replace root instruction files, editor settings, or MCP configuration unless the user requests persistent setup.

## 2. Check available graph tools

1. Check for callable CodeGraphContext and code-review-graph tools.
2. Use the existing graph before filesystem search when it covers the repository.
3. Check graph freshness before relying on results.
4. Update the graph when the available tool supports an in-scope update.
5. Follow [environment setup](references/environment-setup.md) only when a required tool is unavailable.
6. Follow [recovery](references/recovery-runbook.md) when a configured tool fails.
7. Read `../system-init/SKILL.md` before installing a missing graph tool.

## 3. Route the query

Use [tool routing](references/tool-routing-guide.md).

1. Use code-review-graph for change detection, impact radius, callers, callees, affected flows, and test relationships.
2. Use CodeGraphContext for semantic search, complexity, dead-code analysis, reports, and custom graph queries.
3. Use both tools when the question combines discovery with impact analysis.
4. Use `rg` and direct file reads only for gaps not covered by the graph.

## 4. Inspect changes

1. Detect the changed files and symbols.
2. Retrieve review context for the changed symbols.
3. Map upstream callers and downstream dependencies.
4. Map affected execution flows.
5. Locate tests for the affected symbols and flows.
6. Read the exact source and test passages needed to verify graph results.

## 5. Inspect architecture

1. Generate or retrieve the architecture overview.
2. Identify subsystem, module, and service boundaries.
3. Trace imports, calls, inheritance, data flow, and integration edges.
4. Identify cycles, dead code, and high-complexity nodes when relevant.
5. Verify important relationships against source files.

## 6. Map compliance or documentation

1. Read the controlling requirement or source document in full.
2. Split the source into individually testable requirements.
3. Map each requirement to implementing symbols, configuration, tests, and evidence.
4. Mark each mapping as verified, missing, conflicting, or not applicable.
5. Keep proposals, interpretations, and controlling requirements distinct.
6. Cite the source passage and implementation location for each conclusion.

## 7. Stage implementation work

1. Follow [feature staging](examples/feature-staging-example.md).
2. Locate established patterns before writing code.
3. Identify affected interfaces, schemas, tests, and documentation.
4. Record the intended change and verification path in the active plan.
5. Implement only within the user's authorized scope.
6. Refresh the graph after substantive code changes.
7. Re-run impact and test queries against the final state.

## 8. Manage repository graph state

1. Follow [repository activation](references/repository-activation.md) when persistent local graph state is requested.
2. Store CRG state in `.agents/code-graphs/crg/`.
3. Store CGC state in `.agents/code-graphs/cgc/`.
4. Ignore `.agents/code-graphs/` in version control.
5. Inspect generated files after each initialization or update command.
6. Move generated agent, editor, MCP, report, lock, socket, and database files into the permitted state directory when supported.
7. Remove generated scaffolding outside the permitted state directory only when the user has authorized cleanup.
8. Preserve project-owned files and uncertain material.

## 9. Report results

1. Lead with the verified answer.
2. Name the affected symbols, files, flows, and tests.
3. Separate graph-derived findings from source-verified findings.
4. State graph freshness and tool gaps.
5. State unresolved risks without presenting them as settled facts.
6. Do not commit generated reports or graph state.
