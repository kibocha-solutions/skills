# Bootstrap Hook and Graphify Registration Reference

## Contents

1. [Per-Host Compliance Enforcement Scripts](#1-per-host-compliance-enforcement-scripts)
2. [Claude Code](#2-claude-code-claudesettingsjson-and-claudejson)
3. [Codex CLI / Desktop](#3-codex-cli--desktop-codexconfigtoml-and-codexhooksjson)
4. [Gemini Antigravity and Gemini CLI](#4-gemini-antigravity-and-gemini-cli-gemini)
5. [GitHub Copilot CLI](#5-github-copilot-cli-copilothooksbootstrapjson-and-copilotmcp-configjson)
6. [Steward Guard and System Profile Hooks](#6-steward-guard-and-system-profile-hooks)
7. [Always-On Graphify Instruction Block](#7-always-on-graphify-instruction-block)

Register only the hooks for agent hosts actually installed on the workstation. Always merge JSON and TOML files non-destructively so existing user settings, permissions, plugins, and MCP servers remain intact.

## 1. Per-Host Compliance Enforcement Scripts

Each agent host has a dedicated enforcement script in `bootstrap/scripts/` that names its exact governing instruction file and outputs the host's native hook payload:

| Agent Host | Governing Instruction File | Enforcement Script | Hook Event | Output Format |
| :--- | :--- | :--- | :--- | :--- |
| Claude Code | `~/.claude/CLAUDE.md` + repo `CLAUDE.md`/`AGENTS.md` | `enforce-claude-rules.sh` | `UserPromptSubmit` | Plain text directive injected into prompt context |
| Gemini Antigravity | `~/.gemini/GEMINI.md` + repo `GEMINI.md`/`AGENTS.md` | `enforce-gemini-rules.sh` | `PreInvocation` | `{"injectSteps":[{"ephemeralMessage":"..."}]}` |
| Gemini CLI | `~/.gemini/GEMINI.md` + repo `GEMINI.md`/`AGENTS.md` | `enforce-gemini-cli-rules.sh` | `SessionStart` | `{"systemMessage":"...","suppressOutput":false}` |
| Codex CLI / Desktop | `~/.codex/AGENTS.md` + repo `AGENTS.md` | `enforce-codex-rules.sh` | `SessionStart` (`startup\|resume`) | `{"systemMessage":"...","suppressOutput":false}` |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` + repo `AGENTS.md` | `enforce-copilot-rules.sh` | `sessionStart` | `{"systemMessage":"...","suppressOutput":false}` |

Every enforcement script prints the single directive defined in `bootstrap/scripts/directive.sh`, wrapped in its host's output format. Edit the directive there only. It commands the agent to:
1. **Treat compliance as the task**: obey the governing instruction file and every skill in full; output that breaks a rule is a failed task.
2. **Treat no rule as optional**: `must`, `must not`, `always`, and `never` rules admit no exception; condition-bound rules bind equally and permit departure only when their own condition holds.
3. **Consult the user on alternatives**: stop and obtain explicit approval before deviating.
4. **Read canonical `SKILL.md` files from disk in full**: loader summaries, excerpts, and grep snippets never count.
5. **Obey `steward/SKILL.md`**: rely on version control instead of copies, move without leaving copies, delete temporary artifacts, and work within the system profile.
6. **Verify before claiming completion**: reread the governing skills and pre-completion checklist, check the exact final deliverable, and confirm the steward check is clean.
7. **Use `graphify` first**: whenever `graphify-out/graph.json` exists, query `graphify` before raw grep, glob, or broad file reads.

## 2. Claude Code (`~/.claude/settings.json` and `~/.claude.json`)

### Hooks in `~/.claude/settings.json`

Merge the following into `hooks`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "graphify hook-guard search --strict",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Read|Glob",
        "hooks": [
          {
            "type": "command",
            "command": "graphify hook-guard read --strict",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "bash \"$HOME/.claude/skills/bootstrap/scripts/enforce-claude-rules.sh\"",
        "timeout": 10
      }
    ],
    "SessionStart": [
      {
        "type": "command",
        "command": "bash \"$HOME/.claude/skills/bootstrap/scripts/ensure-claude-link.sh\"",
        "timeout": 10
      },
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "graphify hook-guard compact",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### MCP Server in `~/.claude.json`

```json
{
  "mcpServers": {
    "graphify": {
      "command": "graphify-mcp",
      "args": []
    }
  }
}
```

## 3. Codex CLI / Desktop (`~/.codex/config.toml` and `~/.codex/hooks.json`)

### Feature Flag and MCP Server in `~/.codex/config.toml`

Ensure `[features]` has `codex_hooks = true` and `[mcp_servers.graphify]` is registered:

```toml
[features]
codex_hooks = true

[mcp_servers.graphify]
command = "graphify-mcp"
args = []
```

### Hooks in `~/.codex/hooks.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "graphify hook-check",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "cat >/dev/null || true; if [ -f graphify-out/graph.json ] && command -v graphify >/dev/null 2>&1; then graphify update . >/dev/null 2>&1 || true; fi",
            "timeout": 30,
            "statusMessage": "Updating graphify knowledge graph"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.codex/skills/bootstrap/scripts/ensure-codex-link.sh\"",
            "timeout": 10,
            "statusMessage": "Aligning AGENTS.md rules and skills"
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.codex/skills/bootstrap/scripts/enforce-codex-rules.sh\"",
            "timeout": 10,
            "statusMessage": "Loading AGENTS.md compliance directive"
          }
        ]
      }
    ]
  }
}
```

## 4. Gemini Antigravity and Gemini CLI (`~/.gemini/`)

### Gemini Antigravity Turn Hook (`~/.gemini/config/hooks.json`)

```json
{
  "compliance-guard": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "bash ~/.gemini/skills/bootstrap/scripts/enforce-gemini-rules.sh"
      }
    ]
  }
}
```

### Gemini Antigravity MCP Server (`~/.gemini/antigravity/mcp_config.json`)

```json
{
  "mcpServers": {
    "graphify": {
      "command": "graphify-mcp",
      "args": []
    }
  }
}
```

### Gemini CLI Settings (`~/.gemini/settings.json`)

```json
{
  "mcpServers": {
    "graphify": {
      "command": "graphify-mcp",
      "args": []
    }
  },
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "bash \"$HOME/.gemini/skills/bootstrap/scripts/ensure-gemini-link.sh\"",
        "timeout": 10000
      },
      {
        "type": "command",
        "command": "bash \"$HOME/.gemini/skills/bootstrap/scripts/enforce-gemini-cli-rules.sh\"",
        "timeout": 10000
      }
    ],
    "BeforeTool": [
      {
        "matcher": "read_file|list_directory",
        "hooks": [
          {
            "type": "command",
            "command": "graphify hook-guard gemini"
          }
        ]
      }
    ]
  }
}
```

## 5. GitHub Copilot CLI (`~/.copilot/hooks/bootstrap.json` and `~/.copilot/mcp-config.json`)

### Hooks in `~/.copilot/hooks/bootstrap.json`

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "bash": "bash \"$HOME/.copilot/skills/bootstrap/scripts/ensure-copilot-link.sh\" 2>/dev/null || true",
        "timeoutSec": 10
      },
      {
        "type": "command",
        "bash": "bash \"$HOME/.copilot/skills/bootstrap/scripts/enforce-copilot-rules.sh\" 2>/dev/null || true",
        "timeoutSec": 10
      }
    ]
  }
}
```

### MCP Server in `~/.copilot/mcp-config.json`

```json
{
  "mcpServers": {
    "graphify": {
      "command": "graphify-mcp",
      "args": []
    }
  }
}
```

## 6. Steward Guard and System Profile Hooks

Register these hooks on every installed host. `steward.py pre` refuses a command and `steward.py stop` refuses to end a turn while leftovers remain, each in the host's format below; `system-profile.sh` prints a capacity summary on stdout.

| Host | Configuration | Pre-tool event | End-of-turn event | Session-start event |
| :--- | :--- | :--- | :--- | :--- |
| Claude Code | `~/.claude/settings.json` | `PreToolUse`, matcher `Bash` | `Stop` | `SessionStart` |
| Codex (CLI and the ChatGPT app) | `~/.codex/hooks.json` | `PreToolUse`, matcher `Bash` | `Stop` | `SessionStart` (`startup\|resume`) |
| Antigravity | `~/.gemini/config/hooks.json`, group `steward-guard` | `PreToolUse`, matcher `run_command` | `Stop` | `SessionStart` |
| GitHub Copilot CLI | `~/.copilot/hooks/steward.json` | `preToolUse`, matcher `bash` | `agentStop` | `sessionStart` |

`steward.py` detects the host from its input and answers in that host's format: exit code `2` with the reason on stderr for Claude Code and Codex, `{"decision": "deny"}` and `{"decision": "continue"}` for Antigravity, and `{"permissionDecision": "deny"}` and `{"decision": "block"}` for Copilot. Gemini CLI is registered only when the `gemini` command is installed.

Codex skips new or changed hooks until the user trusts them in the `/hooks` review; tell the user to approve the steward hooks there after registration.

Claude Code entries to merge into `hooks`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.claude/skills/steward/scripts/steward.py\" pre",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.claude/skills/steward/scripts/steward.py\" stop",
            "timeout": 60
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/skills/steward/scripts/system-profile.sh\"",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

For other hosts, replace `$HOME/.claude/skills` with the host's skills directory and use the host's hook schema from Sections 3 to 5.

Remove a project-level guard that duplicates these hooks after the user-level hooks are verified.

## 7. Always-On Graphify Instruction Block

Ensure the following block (wrapped in `<!-- graphify --> ... <!-- /graphify -->`) is present at the bottom of `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`, and `~/.copilot/copilot-instructions.md`:

```markdown
<!-- graphify -->
## Graphify Codebase Knowledge Graph Mandate

This workstation has **graphify** (`graphify` CLI + `graphify-mcp` MCP server) and the `graphify` skill installed.
Whenever a repository contains `graphify-out/graph.json` (or `graphify-out/GRAPH_REPORT.md`):
1. Read and follow the `graphify` skill (`SKILL.md`) before exploring code, tracing dependencies, or reviewing architecture.
2. Query the `graphify` MCP tools (`query_graph`, `get_neighbors`, `get_node`, `shortest_path`, `god_nodes`, `graph_stats`, `explain_node`, `get_community`) or read `graphify-out/GRAPH_REPORT.md` **before** running raw `grep`, `ripgrep`, `glob`, or broad file reads.
3. Read raw source files only for the specific files and line ranges identified by the graph, or when preparing an exact edit.
4. After modifying source files in a graphed repository, run `graphify update .` (or rely on the active post-edit / git hook) so `graphify-out/` stays synchronized.
<!-- /graphify -->
```
