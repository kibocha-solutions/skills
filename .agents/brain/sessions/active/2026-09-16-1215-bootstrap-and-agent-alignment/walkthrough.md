# Walkthrough: Multi-Agent Bootstrap Alignment, MCP Standardization & Rule Enforcement

## Completed Phases

1. **Cleanups & Script Alignment**:
   - Pruned redundant `AGENTS.md` at host roots in `bootstrap/scripts/lib.sh`.
   - Refactored `ensure-gemini-link.sh` to support unified Gemini CLI and Antigravity via `~/.gemini/skills/` and `~/.gemini/config/skills.json` / symlinks, leaving `antigravity/builtin/` clean.
   - Deprecated and forwarded `ensure-gemini-builtin-skills.sh`.

2. **MCP Server Standardization**:
   - Installed `cgc` and `code-review-graph` globally via `uv tool install`.
   - Standardized `~/.copilot/mcp-config.json`, `~/.gemini/config/mcp_config.json`, `~/.claude.json`, and `~/.codex/config.toml`.
   - Verified JSON/TOML parsing for all four host configurations.

3. **Rule Compliance Enforcement Hooks**:
   - Created executable scripts `bootstrap/scripts/enforce-claude-rules.sh` and `bootstrap/scripts/enforce-gemini-rules.sh`.
   - Registered `UserPromptSubmit` hook in `~/.claude/settings.json`.
   - Registered `PreInvocation` hook in `~/.gemini/config/hooks.json`.
   - Registered `SessionStart` hooks in `~/.codex/hooks.json` and `~/.copilot/hooks/bootstrap.json`.
   - Verified hook outputs and JSON payload conformance.

4. **Documentation & Memory**:
   - Updated `bootstrap/SKILL.md` with pre-completion checklist.
   - Rewrote `bootstrap/references/hook-registration.md` as cross-OS reference.
   - Refreshed `.agents/memory/skills-repo-deployment-workflow.md`.

## Verification Evidence
- Hook commands executed successfully with zero errors.
- MCP configurations loaded and validated with Python scripts.
