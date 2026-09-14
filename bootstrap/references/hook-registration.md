# SessionStart Hook Registration

## Preconditions

1. Read the target tool's current hook documentation.
2. Inspect the existing settings file.
3. Preserve unrelated hooks and settings.
4. Register only the matching bootstrap script.
5. Validate the final JSON or shell file.
6. Start a new session and verify one real hook execution.

## Claude Code

Target: `~/.claude/settings.json`

Merge this object into `hooks.SessionStart`:

```json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "bash \"$HOME/.claude/skills/bootstrap/scripts/ensure-claude-link.sh\"",
      "timeout": 10
    }
  ]
}
```

Do not replace existing `SessionStart` entries.

## Codex CLI

Target: `~/.codex/hooks.json`

Merge this object into `hooks.SessionStart`:

```json
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
```

Do not replace existing `SessionStart` entries.

## Gemini CLI

Targets:

- `~/.gemini/settings.json`
- `~/.gemini/hooks/`

Merge this object into `hooks.SessionStart`:

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

Requirements:

- Keep the command path relative to `~/.gemini/`.
- Use milliseconds for `timeout`.
- Keep hook stdout valid JSON.

## GitHub Copilot CLI

Target: `~/.copilot/hooks/bootstrap.json`

Use the current Copilot hook schema. Confirm these fields against the installed client before writing:

- `version`
- `hooks.sessionStart`
- `type`
- `bash` or `powershell`
- `timeoutSec`

Example:

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

Do not claim execution verification until a Copilot session runs the hook.

## Final checks

- [ ] Existing hooks remain.
- [ ] JSON parses.
- [ ] Script path resolves.
- [ ] Script is executable.
- [ ] Timeout uses the target tool's unit.
- [ ] Hook output matches the target schema.
- [ ] A new session executed the hook.
