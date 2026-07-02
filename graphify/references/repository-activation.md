# Repository Activation

Activating the graph tools in a local repository initializes the local indexes
and builds the initial database files. Both tools store their state under the
repo-local `graphify/` directory to keep graph data out of the home directory
and out of version control.

## 1. Initialize code-review-graph (CRG)

To index AST structures and enable call-graph/blast-radius analysis:

```bash
# Run in the repository root
code-review-graph install
code-review-graph build --repo . --data-dir graphify/crg
```

Subsequent commands use the same `--data-dir` flag:

```bash
code-review-graph update --repo . --data-dir graphify/crg
code-review-graph status --repo . --data-dir graphify/crg
```

`graphify/crg/` stores the graph database. The `--data-dir` flag writes a
`.gitignore` containing `*` inside the data directory; the parent `graphify/`
entry in the repo's root `.gitignore` provides an additional safety net.

---

## 2. Configure `.code-review-graphignore`

Create or update `.code-review-graphignore` at the repo root. CRG reads this
file in addition to the default ignore list. Patterns use glob syntax;
`<dir>/**` matches at any depth.

```
# Generated graph state
graphify/**
.code-review-graph/**

# Generated root instruction and editor config files
AGENTS.md
CLAUDE.md
GEMINI.md
QODER.md
.cursorrules
.windsurfrules
.mcp.json
.opencode.json
.github/**
.idea/**

# Skill packages and agent tooling
**/skills/**
.agents/skills/**

# Transient agent brain folders
.agents/brain/active/**
.agents/brain/archive/**

# Assistant-platform scaffolding
.claude/**
.gemini/**
.kiro/**
.qoder/**
```

---

## 3. Initialize CodeGraphContext (CGC)

CGC version 0.5.1 uses FalkorDB by default. Its database paths are configured
in `~/.codegraphcontext/.env` (`FALKORDB_PATH`, `KUZUDB_PATH`,
`LADYBUGDB_PATH`). To direct a single indexing command to the project-local
path, use the global `--path` flag:

```bash
# Index with project-local storage
cgc --path graphify/cgc index .

# Refresh the existing project-local index
cgc --path graphify/cgc update --quiet
```

To make project-local storage the default for this repo's workflow, set
`FALKORDB_PATH` (or the relevant backend path variable) to an absolute path
under the repo. For example, in `~/.codegraphcontext/.env`:

```dotenv
FALKORDB_PATH=/home/codelf/workspace/kibocha-solutions/skills/graphify/cgc
```

If you change the config path, run `cgc doctor` to confirm the new path is
valid and writable.

---

## 4. Configure `.cgcignore`

Create or update `.cgcignore` at the repo root. CGC discovers this file by
walking from the indexed path up to the git root. The file uses gitignore-style
syntax.

```
# Generated graph state
graphify/
.code-review-graph/

# Generated root instruction and editor config files
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

# Skill packages and agent tooling
**/skills/
.agents/skills/

# Transient agent brain folders
.agents/brain/active/
.agents/brain/archive/

# Assistant-platform scaffolding
.claude/
.gemini/
.kiro/
.qoder/
```

---

## 5. Register MCP Servers

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
