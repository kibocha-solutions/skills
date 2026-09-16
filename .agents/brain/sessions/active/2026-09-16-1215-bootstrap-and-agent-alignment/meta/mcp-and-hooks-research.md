# Multi-Agent Hooks & MCP Configuration Specification

## 1. Verified Multi-Agent MCP Server Configuration

Web search verification against official documentation confirms the precise configuration files and top-level schema keys for each host:

| Host | Configuration File | Root Schema Key | Transport & Invocation Format |
|---|---|---|---|
| **Claude Code** | `~/.claude.json` | `"mcpServers"` | Standard JSON dictionary. Command must be directly executable or via `npx`/`uvx`. |
| **GitHub Copilot** | `~/.copilot/mcp-config.json` | `"mcpServers"` | Must use `"mcpServers"`, NOT `"servers"`. Paths must be absolute or valid on host. |
| **Gemini Antigravity** | `~/.gemini/config/mcp_config.json` | `"mcpServers"` | Standard JSON dictionary under `~/.gemini/config/` (or `.agents/mcp_config.json`). |
| **Codex CLI** | `~/.codex/config.toml` | `[mcp_servers.<name>]` | TOML table format using underscore (`mcp_servers`). |

### Concrete Server Configuration Block

#### For `~/.claude.json`, `~/.copilot/mcp-config.json`, and `~/.gemini/config/mcp_config.json`:
```json
{
  "mcpServers": {
    "code-review-graph": {
      "command": "/home/vaelric/.local/bin/code-review-graph",
      "args": ["serve"],
      "cwd": "/mnt/data/workspace"
    },
    "codegraphcontext": {
      "command": "/home/vaelric/.local/bin/cgc",
      "args": ["mcp", "start"],
      "cwd": "/mnt/data/workspace"
    }
  }
}
```

#### For `~/.codex/config.toml`:
```toml
[mcp_servers.code-review-graph]
command = "/home/vaelric/.local/bin/code-review-graph"
args = ["serve"]
cwd = "/mnt/data/workspace"

[mcp_servers.codegraphcontext]
command = "/home/vaelric/.local/bin/cgc"
args = ["mcp", "start"]
cwd = "/mnt/data/workspace"
```

---

## 2. Verified Deterministic Lifecycle Hooks

### Host Lifecycle Event Mapping

1. **Claude Code (`~/.claude/settings.json`)**:
   - `UserPromptSubmit`: Runs on every prompt submission before the model evaluates context. Text printed to `stdout` with exit code `0` is prepended directly to the user prompt.
   - `SessionStart`: Runs on session creation or resumption to ensure file synchronization.
   - `PreToolUse`: Exit code `2` with `stderr` explanation blocks unauthorized execution.

2. **Gemini Antigravity (`~/.gemini/config/hooks.json`)**:
   - `PreInvocation`: Runs before model invocation. Returns JSON payload `{"injectSteps": [{"ephemeralMessage": "..."}]}` to inject unignorable instructions into the conversation turn.
   - `PreToolUse`: Gates file modification commands to enforce prior full reading.

3. **Codex CLI (`~/.codex/hooks.json`)**:
   - `SessionStart`: Runs on `startup|resume` to verify rule and skill mirrors.
   - `PostToolUse`: Runs after `Write|Edit|Bash` steps to update code graphs.

4. **GitHub Copilot (`~/.copilot/hooks/bootstrap.json`)**:
   - `sessionStart`: Runs on session initialization to sync skills and instructions.

### Portability Specification for `bootstrap`
To ensure cross-OS portability when migrating or provisioning a new machine:
- `bootstrap/references/hook-registration.md` documents the precise schema, path resolution, and verification tests for each host across Linux, macOS, and WSL.
- `ensure-*-link.sh` scripts are made idempotent and can register or update the respective hook configuration without destroying unrelated user settings.
