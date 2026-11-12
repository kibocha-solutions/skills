# Graphify Environment Setup

## 1. Python and Package Installation

1. Verify Python compatibility (`>=3.10,<3.15` required by `graphifyy`). If default `python3` is 3.15+, target an installed 3.12-3.14 interpreter explicitly:

```bash
uv tool install --python 3.14 "graphifyy[mcp,watch,leiden,pdf,office,svg]"
```

2. Core extras:
   - `mcp`: `graphify-mcp` stdio and HTTP server (`mcp`, `starlette`, `anyio`, `uvicorn`)
   - `watch`: file watcher (`watchdog`)
   - `leiden`: Leiden clustering (`graspologic` or `graspologic-native`)
   - `pdf`, `office`, `svg`: PDF, DOCX/XLSX, and SVG support

3. Verify binaries and runtime:

```bash
which graphify graphify-mcp
graphify --version
graphify-mcp --help
```

4. Check the installed Python interpreter inside the tool environment (`cat graphify-out/.graphify_python` when built inside a repo, or `head -1 "$(which graphify)"`).

## 2. Host MCP Registrations

Register `/home/<USER>/.local/bin/graphify-mcp` (or `uv run --with "graphifyy[mcp]" -m graphify.serve`). Every `graphify-mcp` tool accepts an optional `project_path` pointing to any project containing `graphify-out/graph.json`, so a single global server works across repositories even if the process starts in a directory without `graphify-out/graph.json`.

| Host | Config Path | Key / Format |
|---|---|---|
| Google Antigravity | `~/.gemini/antigravity/mcp_config.json` | `"mcpServers": { "graphify": { "command": "/home/<USER>/.local/bin/graphify-mcp", "args": [] } }` |
| Claude Code | `~/.claude.json` | `"mcpServers": { "graphify": { "command": "/home/<USER>/.local/bin/graphify-mcp", "args": [] } }` |
| Codex CLI / Desktop | `~/.codex/config.toml` | `[mcp_servers.graphify]` with `command = "/home/<USER>/.local/bin/graphify-mcp"`, `args = []` |
| GitHub Copilot CLI | `~/.copilot/mcp-config.json` | `"mcpServers": { "graphify": { "command": "/home/<USER>/.local/bin/graphify-mcp", "args": [], "type": "stdio" } }` |
| Gemini CLI | `~/.gemini/settings.json` | `"mcpServers": { "graphify": { "command": "/home/<USER>/.local/bin/graphify-mcp", "args": [] } }` |

## 3. Host Guard Hooks and Always-On Rules

1. **Claude Code** (`~/.claude/settings.json`):
   - `PreToolUse` matcher `Bash|Grep`: `<abs-graphify> hook-guard search --strict` (`timeout: 10`)
   - `PreToolUse` matcher `Read|Glob`: `<abs-graphify> hook-guard read --strict` (`timeout: 10`)
   - `SessionStart` matcher `compact`: `<abs-graphify> hook-guard compact` (`timeout: 10`)
   - `UserPromptSubmit`: `bootstrap/scripts/enforce-claude-rules.sh` (includes graph-first skill directive)
   In `--strict` mode, the first unqueried raw `Read` of fresh indexed code or `Grep` is denied once per session with a redirect to `graphify`, then downgrades to an `additionalContext` nudge.
2. **Gemini Antigravity** (`~/.gemini/config/hooks.json` and `.agents/rules/graphify.md`):
   - `PreInvocation`: `bootstrap/scripts/enforce-gemini-rules.sh` injects the graph-first directive before model turns.
   - Workspace `.agents/rules/graphify.md` (and host instruction files outside the `BEGIN/END SHARED SKILLS RULES` markers) instructs Antigravity to query `graphify` before raw search.
3. **Gemini CLI** (`~/.gemini/settings.json`):
   - `BeforeTool` matcher `read_file|list_directory`: `<abs-graphify> hook-guard gemini`
4. **Codex CLI / Desktop** (`~/.codex/hooks.json` and `~/.codex/AGENTS.md`):
   - `PreToolUse` matcher `Bash`: conditional check running `graphify hook-check` when installed.
   - `SessionStart` (`startup|resume`): reports active `graphify-out/graph.json` presence and `ensure-codex-link.sh` alignment.
   - `PostToolUse` (`Write|Edit|Bash`): runs `graphify update . --no-cluster` or `graphify update .` when `graphify-out/graph.json` is present (`--skip-flows` is not a `graphify` flag).
   - Always-on rules live outside `BEGIN/END SHARED SKILLS RULES` in `~/.codex/AGENTS.md` (Codex Desktop rejects `additionalContext` on `PreToolUse`).
5. **Repository Git Post-Commit Hook**:
   - Run `graphify hook install` inside any tracked repository to rebuild changed code files automatically after commits (`graphify hook status`, `graphify hook uninstall`).
