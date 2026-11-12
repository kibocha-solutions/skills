# Graphify Tool Routing Guide

## 1. Graph-First Decision Rule

When `graphify-out/graph.json` exists in a repository:

1. Start architectural, structural, dependency, impact, and symbol-location questions with `graphify` MCP tools or `graphify` CLI commands.
2. Expand natural-language query terms against node labels (`query_graph` and `graphify query` match literal tokens/IDF with no stemming or synonym expansion).
3. Restrict `grep`, `rg`, `glob`, and raw `read_file` calls to exact file paths and line ranges surfaced by the graph, or to editing targets already located.
4. Inspect `graphify-out/wiki/index.md` or `graphify-out/GRAPH_REPORT.md` only for whole-repository overview or when targeted queries return insufficient context.

## 2. MCP vs CLI Tool Selection

| Question / Intent | MCP Tool (`graphify-mcp`) | CLI Equivalent (`graphify`) | Key Parameters / Notes |
|---|---|---|---|
| Broad symbol/concept context | `query_graph` (`mode="bfs"`) | `graphify query "<terms>"` | Pass `depth`, `token_budget`, `context_filter`, `demote_docs`, `project_path` |
| Trace execution / dependency chain | `query_graph` (`mode="dfs"`) | `graphify query "<terms>" --dfs --budget 3000` | Deeper linear path tracing |
| Exact path between two concepts | `shortest_path` | `graphify path "<A>" "<B>"` | Pass `max_hops`, `undirected=true` when edge direction should be ignored |
| Single node details or immediate neighbors | `get_node`, `get_neighbors` | `graphify explain "<node>"` | Accepts `relation_filter` and `token_budget` on `get_neighbors` |
| Blast radius of modifying a symbol | Combine `get_neighbors` / `query_graph` | `graphify affected "<node>" --depth 2` | Returns exit code `3` if ambiguous, `4` if not found |
| Core hubs and repo graph size | `god_nodes`, `graph_stats` | `graphify god-nodes --top 10` | `graph_stats` prints `built_at_commit` and HEAD staleness |
| Module / community membership | `get_community` | Check `GRAPH_REPORT.md` | 0-indexed `community_id` |
| Open GitHub PR impact and triage | `list_prs`, `get_pr_impact`, `triage_prs` | `graphify prs` | Requires `gh` CLI authenticated in target repo |
| Work memory feedback loop | Write after answer via CLI | `graphify reflect --if-stale`; `graphify save-result ...` | Check `graphify-out/reflections/LESSONS.md` first |
| Bypass detection on god nodes | Grep distinctive literal only in unlinked files | Same after reading `query_graph` neighbor list | Report files with no edge to hub separately as Bypasses |

## 3. Graph Build, Update, and Export Commands

| Operation | Command | Behavior |
|---|---|---|
| Structural AST extract (code only) | `graphify extract <path>` | Deterministic tree-sitter extraction, no LLM needed |
| Incremental code update | `graphify update <path>` | Re-extracts changed code files and updates `graph.json` + `GRAPH_REPORT.md` |
| Re-cluster existing graph | `graphify cluster-only <path>` | Re-clusters and regenerates outputs without re-extracting |
| Background folder watcher | `graphify watch <path> --debounce 3` | Auto-updates code changes; flags doc changes via `graphify-out/needs_update` |
| Ingest URL into corpus | `graphify add <url>` | Downloads PDF, webpage, X/Twitter, arXiv, or media into `./raw` |
| Export formats | `graphify export <html|wiki|obsidian|svg|graphml|neo4j|falkordb>` | Generates static or external graph views |
| Interactive D3 tree HTML | `graphify tree` | Writes `graphify-out/GRAPH_TREE.html` |
| Diagnostic check | `graphify diagnose` | Checks dangling endpoints, collapsed edges, self-loops |
| Benchmark compression | `graphify benchmark` | Measures token reduction on graphs with >5,000 words |
