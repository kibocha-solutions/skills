# Graphify Usage Examples: Good vs Bad

## Good: Graph-First Navigation and Incremental Maintenance

1. Check graph state and lessons at task start:

```bash
ls -la graphify-out/graph.json
graphify reflect --if-stale
```

2. Query the graph via MCP (`query_graph`, `shortest_path`, `affected`) or CLI before running raw text searches:

```bash
graphify query "hook guard strict claude install"
graphify affected "hook_guard" --depth 2
```

3. Read only the exact file lines identified by the graph (`graphify/cli.py:1561-1620`, `graphify/install.py:567-603`) instead of reading entire modules speculatively.
4. Refresh the graph after making code changes:

```bash
graphify update .
```

Why this works: Token usage stays minimal, cross-module callers and blast radius are surfaced immediately, and `graphify-out/graph.json` remains current for subsequent queries and hooks.

---

## Bad: Graph Bypass, Legacy Tools, and Stale State

1. Jumping straight to raw `rg` or `grep -rn` across the entire repository and reading 12 complete files when `graphify-out/graph.json` already exists.
2. Calling removed legacy tools (`cgc`, `codegraphcontext`, or `code-review-graph`) instead of `graphify` MCP / `graphify` CLI.
3. Dispatching exploration subagents without telling them to query `graphify-out/graph.json` first.
4. Editing functions and signatures without running `graphify update .` afterward, causing subsequent hook checks and `query_graph` calls to cite stale line numbers.
5. Hand-editing `graphify-out/graph.json` instead of re-running `graphify extract`, `graphify update`, or `graphify cluster-only`.
