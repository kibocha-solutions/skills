# Bootstrap Verification Audit Report Example

## Bad

```markdown
Bootstrap ran fine across your tools! Everything looks synced and all hooks are probably working.
```

Defects:
- Claims success without naming detected hosts, commit SHA, or verified files.
- Omits instruction block checks, mirror cleanliness, and hook script exit verification.
- Uses vague reassurance instead of observed evidence.

## Good

```markdown
| Host | Instruction File | Skills Mirror (`HEAD`) | Managed Skills | Compliance and Steward Hooks | MCP and Config |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Claude Code | `~/.claude/CLAUDE.md` (shared rules + `graphify` block) | `~/.claude/skills` (`18a30ed`) | `26/26` | `UserPromptSubmit`, `SessionStart`, `PreToolUse`, `Stop` verified; `enforce-claude-rules.sh` exit `0` | `graphify` in `~/.claude.json` (valid JSON) |
| Codex | `~/.codex/AGENTS.md` (shared rules + `graphify` block) | `~/.codex/skills` (`18a30ed`) | `26/26` | `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop` verified; `enforce-codex-rules.sh` exit `0` | `graphify` in `~/.codex/config.toml` (valid TOML) |
| Gemini Antigravity | `~/.gemini/GEMINI.md` (shared rules + `graphify` block) | `~/.gemini/skills` (`18a30ed`) | `26/26` | `PreInvocation`, `SessionStart`, `PreToolUse`, `Stop` verified; `enforce-gemini-rules.sh` exit `0` | `graphify` in `~/.gemini/antigravity/mcp_config.json` (valid JSON) |
| GitHub Copilot | `~/.copilot/copilot-instructions.md` (shared rules + `graphify` block) | `~/.copilot/skills` (`18a30ed`) | `26/26` | `sessionStart`, `preToolUse`, `agentStop` verified; `enforce-copilot-rules.sh` exit `0` | `graphify` in `~/.copilot/mcp-config.json` (valid JSON) |

Checks:
- `steward.py pre` refused `podman run alpine true` with exit `2` (standard) and `{"decision": "deny"}` (Antigravity).
- `steward.py check` exited `0` (`steward check: clean`); `system-profile.sh --brief` exited `0`.
```
