# Registering the SessionStart link-check hook per tool

Each tool discovers this repo's `AGENTS.md` at a different native location.
Once pulled into `<tool-home>/skills/AGENTS.md`, none of the four tools load
it automatically — that path is one directory too deep for any of their
native memory-file discovery rules. A `SessionStart` hook that calls the
matching `ensure-*-link.sh` script closes that gap without depending on
anyone remembering to run `/bootstrap` by hand.

Registration is a one-time, per-machine step — it lives in each tool's own
settings file, not in this repo, so pulling a new version of this repo never
touches it.

## Claude Code — `~/.claude/settings.json`

Add a hook entry under `hooks.SessionStart`. If a `SessionStart` array
already exists (e.g. from another integration), add this as another object
inside its `hooks` list rather than replacing the array.

```json
{
  "hooks": {
    "SessionStart": [
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
    ]
  }
}
```

## Codex CLI — `~/.codex/hooks.json`

Same shape as Claude Code. Merge into the existing `SessionStart` hooks list
if one is already present.

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

## Gemini CLI — `~/.gemini/settings.json` + `~/.gemini/hooks/`

Gemini CLI hooks must be shell scripts that print only JSON to stdout
(`{"systemMessage": "...", "suppressOutput": false}` or
`{"suppressOutput": true}`); `ensure-gemini-link.sh` already does this.
Gemini resolves the `command` path relative to `~/.gemini/`, not to the
script's own location, so the registered command is just the relative path:

```json
{
  "hooks": {
    "SessionStart": [
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
    ]
  }
}
```

Note the timeout unit: Gemini CLI takes milliseconds here, not seconds.

## GitHub Copilot CLI — `~/.copilot/hooks/*.json`

Copilot CLI uses a different schema from the other three: `version`,
`hooks.sessionStart`, `bash`/`powershell` instead of `command`, `timeoutSec`
instead of `timeout`, and no `matcher` field. Any `.json` file dropped in
`~/.copilot/hooks/` is picked up — one dedicated file per concern is fine.

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

Schema confirmed against GitHub's own Copilot CLI hooks documentation. What's
still unverified: this repo had no pre-existing Copilot hook in place to
confirm execution against (unlike the other three tools, where an existing
`code-review-graph` hook proved the schema by example), and Copilot CLI
itself wasn't available to run in this environment. Treat this one as
schema-correct but execution-unconfirmed until it's been seen firing in a
real Copilot CLI session. The `copilot-instructions.md` pointer itself needs
no hook at all — Copilot reads that file natively on every session.
