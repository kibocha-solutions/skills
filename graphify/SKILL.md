---
name: graphify
description: Build, update, query, export, and enforce codebase and document knowledge graphs with `graphifyy` (`graphify` CLI and `graphify-mcp`). Use for architecture mapping, blast-radius and PR impact analysis, dependency and path tracing, structural code review, community and god-node inspection, setting up `graphify` MCP or guard hooks, and handling `/graphify`, `--update`, `--cluster-only`, `--watch`, or `--mode deep`.
compatibility: "Requires Python >=3.10,<3.15, uv or pip, and graphifyy (optional extras: mcp, watch, leiden, pdf, office, svg)."
---

# Graphify

## 1. Establish scope and check graph state

1. Classify the request as environment setup, graph build, graph query, incremental update, export, or hook/MCP enforcement.
2. Check whether `graphify` and `graphify-mcp` are installed in the active environment; if missing or broken, read [environment setup](references/environment-setup.md).
3. Check whether `<repo>/graphify-out/graph.json` exists in the target repository or directory.
4. Check `graphify-out/GRAPH_REPORT.md` and `graphify-out/reflections/LESSONS.md` when present (`graphify reflect --if-stale` refreshes lessons cheaply).
5. Enforce the graph-first rule whenever `graphify-out/graph.json` exists:
   - Query `graphify` MCP (`query_graph`, `get_neighbors`, `shortest_path`, `god_nodes`, `graph_stats`) or run `graphify query` / `graphify path` / `graphify explain` / `graphify affected` before running raw `grep`, `rg`, `glob`, or broad file discovery reads.
   - Include the graph-first rule in every code-exploring subagent prompt.
   - Read raw source files only for lines located by the graph or when preparing edits.

## 2. Query and navigate an existing graph

Read [the tool routing guide](references/tool-routing-guide.md) before querying or picking between MCP and CLI tools.

1. Match user terms against actual graph node labels before querying (`query_graph` and `graphify query` match literal tokens/IDF without stemming or cross-language synonyms).
2. Run `query_graph` (MCP) or `graphify query "<terms>"` (`--dfs` to trace a dependency chain, `--budget N` to cap tokens, `--context-filter` for specific edge types).
3. Use targeted traversal tools when the question asks for:
   - shortest connection between two concepts: `shortest_path` (MCP) or `graphify path "<A>" "<B>"`
   - single symbol neighborhood: `get_node` / `get_neighbors` (MCP) or `graphify explain "<node>"`
   - change blast radius: `graphify affected "<node>"`
   - structural core or summary stats: `god_nodes` / `graph_stats` (MCP)
   - GitHub PR impact: `list_prs`, `get_pr_impact`, or `triage_prs` (MCP) or `graphify prs`
4. Read `graphify-out/wiki/index.md` or `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when targeted queries return insufficient context.
5. Cite `source_file` and `source_location` from graph output; never invent unverified edges or files.
6. Record high-value query outcomes when maintaining project work memory: run `graphify save-result --question "..." --answer "..." --type query --nodes ... --outcome useful|dead_end|corrected`.

## 3. Build a new knowledge graph

Read [repository activation](references/repository-activation.md) before building a graph, configuring `.graphifyignore`/`.graphifyrc`, or running semantic extraction.

1. Respect `.graphifyignore` and `.gitignore`, and warn the user if the corpus exceeds 2,000 files or ~5,000,000 words before proceeding.
2. Determine corpus types:
   - Code-only repositories require AST extraction only (`graphify extract <path> --code-only`), with zero LLM API key required.
   - Mixed corpora (docs, papers, PDFs, Office files, images, videos) use AST extraction for code plus semantic extraction (`GEMINI_API_KEY`/`GOOGLE_API_KEY` if already set, otherwise host subagents following [the extraction specification](references/extraction-spec.md)).
   - Never prompt for or block on `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.
3. Build, cluster, run `graphify diagnose` if needed, label communities, and export outputs (`graph.json`, `GRAPH_REPORT.md`, and `graph.html` unless `--no-viz` or >5,000 nodes without warning).
4. Confirm `.gitignore` handling for `graphify-out/` according to project preference (`graphify-out/` ignored for local-only use, or tracked explicitly for team workflows).

Inspect [good vs bad usage examples](examples/feature-staging-example.md) to verify graph-first querying and update discipline.

## 4. Update, watch, or re-cluster after changes

1. After code edits, run `graphify update <path>` (incremental AST rebuild, no LLM cost).
2. Run semantic `--update` per [repository activation](references/repository-activation.md) when documentation, papers, images, or deleted files changed (check `graphify-out/needs_update` or `.graphify_partial.txt`).
3. Run `graphify cluster-only <path>` to re-cluster communities and regenerate reports without re-extracting nodes.
4. Use `graphify watch <path> --debounce 3` for continuous background code graph updates during active multi-wave editing, or `graphify add <url>` to ingest external URLs.

## 5. Export, serve over MCP, and enforce hooks

Read [environment setup](references/environment-setup.md) and [the tool routing guide](references/tool-routing-guide.md) when registering MCP or hooks across hosts.

1. Serve the graph over stdio (`graphify-mcp`, optional `[graph_path]`, supports `project_path` per tool call for multi-project setups) or HTTP (`graphify-mcp --transport http`).
2. Generate optional exports only when requested: `--obsidian`, `--wiki`, `--svg`, `--graphml`, `--neo4j`, `--falkordb`, or interactive `graphify tree`.
3. Install repository git hooks with `graphify hook install` (`status`, `uninstall`) to refresh the code graph automatically after commits.
4. Register agent guard and enforcement hooks per host (`--strict` on Claude Code `PreToolUse` denies the first unqueried raw `Read`/`Grep` per session; `BeforeTool` for Gemini CLI; `PreInvocation` / `.agents/rules/graphify.md` for Antigravity; `AGENTS.md` + `SessionStart` for Codex).
5. If a graph fails to load, refuses to shrink (`--force`), goes stale, or bypasses hooks, follow [the recovery runbook](references/recovery-runbook.md).

## 6. Pre-completion checklist

- [ ] `graphify` and `graphify-mcp` binaries resolve and respond to smoke tests (`graphify --version`).
- [ ] Codebase queries used `graphify` MCP or CLI before raw grep or broad file reads when `graphify-out/graph.json` existed.
- [ ] `graphify-out/graph.json` and `graphify-out/GRAPH_REPORT.md` are current after code edits (`graphify update`).
- [ ] Required MCP config uses valid `graphify-mcp` or `python -m graphify.serve` paths (reference [MCP config template](assets/mcp-config-template.json)).
- [ ] Configured hooks pass syntax and standalone execution checks without affecting unrelated host tools.
- [ ] Zero U+2014 em dashes, unverified edges, or AI attribution appear in deliverables.
