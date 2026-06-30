# Repository Activation

Activating the graph tools in a local repository initializes the local indexes and builds the initial database files.

## 1. Initialize code-review-graph (CRG)

To index AST structures and enable call-graph/blast-radius analysis:

```bash
# Run in the repository root
code-review-graph install
code-review-graph build
```

This generates `.code-review-graph/graph.db` in the repository root and adds the path to `.gitignore`.

---

## 2. Initialize CodeGraphContext (CGC)

To index code symbols and enable semantic search/Cypher queries:

```bash
# Run in the repository root
cgc index
```

This creates the `.codegraphcontext/` configuration and embedded KùzuDB/FalkorDB storage files in the directory.

---

## 3. Register MCP Servers

Register both stdio servers in your AI editor or client settings:

### Codex (`~/.codex/config.toml`)
```toml
[mcp_servers.codegraphcontext]
command = "cgc"
args = ["mcp", "start"]
type = "stdio"

[mcp_servers.code-review-graph]
command = "code-review-graph"
args = ["serve"]
cwd = "/home/codelf"
type = "stdio"
```

### OpenCode (`~/.config/opencode/opencode.jsonc`)
```json
{
  "mcp": {
    "code-review-graph": {
      "type": "local",
      "command": ["code-review-graph", "serve"],
      "enabled": true
    },
    "codegraphcontext": {
      "type": "local",
      "command": ["cgc", "mcp", "start"],
      "enabled": true
    }
  }
}
```

### Claude Code
```bash
claude mcp add code-review-graph -- code-review-graph serve
claude mcp add codegraphcontext -- cgc mcp start
```
