---
name: gemini-antigravity-mcp-registration
description: Verified working MCP server registration path and command shape for Google Antigravity on this workstation
type: project
---

Google Antigravity (`~/.gemini/antigravity/`) reads its MCP server config
from `~/.gemini/antigravity/mcp_config.json` (a top-level file sibling to
`builtin/`, not inside it, and not at `~/.gemini/antigravity-cli/mcp_config.json`).
`~/.gemini/antigravity/builtin/` holds built-in skills; `~/.gemini/config/mcp_config.json`
is a superseded location alongside `.migrated` (kept mirrored only as legacy fallback).

The active codebase knowledge graph MCP server on this workstation is `graphify`
from `graphifyy[mcp]` installed with `uv tool install --python 3.14 "graphifyy[mcp,watch,leiden,pdf,office,svg]"`:

```json
{
  "mcpServers": {
    "graphify": {
      "command": "/home/vaelric/.local/bin/graphify-mcp",
      "args": []
    }
  }
}
```

`graphify-mcp` starts cleanly without an in-cwd `graphify-out/graph.json` and accepts
an optional `project_path` parameter on every tool call (`query_graph`, `get_node`,
`get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`,
`list_prs`, `get_pr_impact`, `triage_prs`) for multi-project serving. Note that
`graphifyy` requires Python `>=3.10,<3.15` (use `--python 3.14` when default
`python3` is 3.15+).

**How to apply:** When registering or diagnosing `graphify` MCP across Antigravity,
Claude Code (`~/.claude.json`), Codex (`~/.codex/config.toml`), Copilot
(`~/.copilot/mcp-config.json`), or Gemini CLI (`~/.gemini/settings.json`), use
`/home/vaelric/.local/bin/graphify-mcp` installed under `>=3.10,<3.15`.
