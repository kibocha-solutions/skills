## graphify

This project uses `graphifyy` (`graphify-out/graph.json`, `GRAPH_REPORT.md`) as its codebase knowledge graph.

Rules:
- Whenever `graphify-out/graph.json` exists, read and follow `graphify/SKILL.md` and run `graphify` MCP (`query_graph`, `shortest_path`, `get_node`, `get_neighbors`, `god_nodes`, `graph_stats`) or `graphify query "<question>"` BEFORE running raw grep, glob, or broad source-file reads, and include this requirement in every code-exploring subagent prompt.
- Read raw files only for lines already located by the graph or when preparing code edits.
- Use `graphify path "<A>" "<B>"` for shortest connections, `graphify explain "<concept>"` for single-node explanations, and `graphify affected "<symbol>"` for blast radius.
- After modifying source files, run `graphify update .` to keep the code graph current (AST-only, no LLM cost).
