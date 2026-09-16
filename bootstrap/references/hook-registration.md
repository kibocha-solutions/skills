# Multi-Agent Lifecycle Hook Registration

## 1. Overview

Agent hooks enforce repository rules, maintain skill links, and inject compliance directives before model inference. This document defines the registration schemas and paths across Claude Code, Gemini Antigravity, Gemini CLI, Codex CLI, and GitHub Copilot.

## 2. Hook Types and Contracts

### SessionStart Hooks
Run once at agent launch or session resumption to ensure instruction files and skill directories match repository state.

### Turn Enforcement Hooks
Run before model evaluation on every turn to inject mandatory compliance directives into the model context:
- Claude Code: `UserPromptSubmit` hook prints text to stdout, prepended directly to the user prompt.
- Gemini Antigravity: `PreInvocation` hook outputs a JSON payload with `injectSteps` containing an `ephemeralMessage`.

## 3. Host Configurations

### Claude Code

Target: `~/.claude/settings.json`

```json
{
  "agentPushNotifEnabled": true,
  "hooks": {
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
      }
    ]
  }
}
```

Behavior:
- `enforce-claude-rules.sh` outputs the plain text compliance mandate.
- `ensure-claude-link.sh` verifies `~/.claude/CLAUDE.md` and sparse checkout.

### Gemini Antigravity

Target: `~/.gemini/config/hooks.json`

```json
{
  "compliance-guard": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "bash \"$HOME/.gemini/skills/bootstrap/scripts/enforce-gemini-rules.sh\""
      }
    ]
  }
}
```

Behavior:
- Handler receives context on stdin.
- Script outputs JSON matching the `PreInvocation` schema:
  `{"injectSteps": [{"ephemeralMessage": "..."}]}`

### Gemini CLI

Targets: `~/.gemini/settings.json` or `~/.gemini/hooks/`

```json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "bash skills/bootstrap/scripts/ensure-gemini-link.sh",
      "name": "bootstrap: AGENTS.md link check",
      "timeout": 10000
    }
  ]
}
```

### Codex CLI

Target: `~/.codex/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.codex/skills/bootstrap/scripts/ensure-codex-link.sh\"",
            "timeout": 10,
            "statusMessage": "Checking AGENTS.md link"
          }
        ]
      }
    ]
  }
}
```

### GitHub Copilot CLI

Target: `~/.copilot/hooks/bootstrap.json`

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "bash": "bash \"$HOME/.copilot/skills/bootstrap/scripts/ensure-copilot-link.sh\" 2>/dev/null || true",
        "timeoutSec": 10
      }
    ]
  }
}
```

## 4. Cross-OS Portability

1. Under Linux and macOS, paths resolve relative to `$HOME`.
2. Under WSL, scripts target `$HOME` within the Linux environment and map `/mnt/c/Users/<user>/` when managing Windows-side installations.
3. Hook scripts must be marked executable (`chmod +x`).
4. Scripts must use `set -euo pipefail` to fail fast on unexpected conditions.

## 5. Verification Checklist

- [ ] Target configuration files exist and contain valid JSON or TOML.
- [ ] Registered script paths resolve and have executable permissions.
- [ ] Scripts produce exit code 0 when run standalone.
- [ ] Turn enforcement scripts produce valid stdout matching the host contract.
- [ ] Pre-existing hooks in target configuration files remain intact.
