---
name: bootstrap
description: Verify and align shared agent rules, skill mirrors, per-host compliance hooks, and graphify hooks for Claude Code, Codex, Gemini CLI, Gemini Antigravity, and GitHub Copilot across Linux, macOS, and WSL. Use for new workstation setup, stale installed skills, shared-rule alignment, session-start or turn-enforcement hook registration, or /bootstrap.
---

# Bootstrap

## Overview

Bootstrap aligns shared agent rules (`AGENTS.md`), skill mirrors, per-host compliance enforcement hooks, and `graphify` codebase-graph hooks across Claude Code, Codex CLI/Desktop, Gemini CLI, Gemini Antigravity, and GitHub Copilot CLI on Linux, macOS, and WSL.

Read `references/hook-registration.md` before modifying host settings or hook files. Inspect `examples/bootstrap-audit-report.md` for the expected verification report format.

## Step 1: Detect Installed Agent Hosts

Check which agent hosts exist on the workstation before running any alignment or hook changes:

1. **Claude Code**: `command -v claude` or `~/.claude/`
2. **Codex**: `command -v codex` or `~/.codex/`
3. **Gemini CLI**: `command -v gemini`, `~/.gemini/settings.json`, or `~/.gemini/hooks/`
4. **Gemini Antigravity**: `command -v agy`, `~/.gemini/antigravity/`, or `~/.gemini/config/`
5. **GitHub Copilot CLI**: `command -v copilot` or `~/.copilot/`
6. **WSL Windows host**: `/mnt/c/Users/<WinUser>/.claude`, `.codex`, `.gemini`, or `.copilot`

Do not create host directories for tools that are not installed on the workstation.

## Step 2: Run the Bootstrap Alignment Scripts

Run only the alignment scripts for the detected hosts from `bootstrap/scripts/`:

```bash
bash bootstrap/scripts/ensure-claude-link.sh
bash bootstrap/scripts/ensure-codex-link.sh
bash bootstrap/scripts/ensure-gemini-link.sh
bash bootstrap/scripts/ensure-copilot-link.sh
```

Each script performs two idempotent actions:
1. Syncs `~/.<tool>/skills/` as a sparse git checkout tracking `origin/main` (including `AGENTS.md` and every top-level `<skill>/` directory).
2. Embeds or updates the shared `AGENTS.md` rules inside the host instruction file (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`, or `~/.copilot/copilot-instructions.md`) between `<!-- BEGIN SHARED SKILLS RULES -->` and `<!-- END SHARED SKILLS RULES -->` while preserving custom content outside those markers.

## Step 3: Register Session-Start, Turn-Enforcement, and Graphify Hooks

Open `references/hook-registration.md` and verify that each installed host has:

1. Its `SessionStart` (`sessionStart`) hook registered to run `ensure-<tool>-link.sh` so rules and skills stay aligned automatically.
2. Its host-specific turn/session compliance enforcement hook registered so the agent is explicitly commanded to obey its governing instruction file (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, or `copilot-instructions.md`), manually read full `SKILL.md` files from disk (never relying on platform loader summaries), consult the user before taking any perceived viable alternative, re-consult the governing `SKILL.md` before claiming completion, and query `graphify` when `graphify-out/graph.json` exists:
   - Claude Code (`~/.claude/settings.json` `UserPromptSubmit`): `enforce-claude-rules.sh`
   - Gemini Antigravity (`~/.gemini/config/hooks.json` `PreInvocation`): `enforce-gemini-rules.sh`
   - Gemini CLI (`~/.gemini/settings.json` `SessionStart`): `enforce-gemini-cli-rules.sh`
   - Codex (`~/.codex/hooks.json` `SessionStart`): `enforce-codex-rules.sh`
   - GitHub Copilot (`~/.copilot/hooks/bootstrap.json` `sessionStart`): `enforce-copilot-rules.sh`
3. Its `graphify` MCP server (`graphify-mcp`) and `graphify` PreToolUse/PostToolUse/BeforeTool hooks configured when `graphify` is installed on the workstation:
   - Run `graphify claude install`, `graphify codex install`, `graphify gemini install`, or `graphify hook install` as appropriate for the host.
   - Ensure the `<!-- graphify -->` always-on rule block is present in the host's instruction file (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `copilot-instructions.md`) so agents invoke the `graphify` skill and query `graphify` MCP/CLI before raw `grep`/`glob`/file reads whenever `graphify-out/graph.json` is present.

Merge JSON and TOML settings non-destructively using `python3` or `jq`; never overwrite existing user permissions, plugins, or unrelated MCP servers.

## Step 4: Verify Alignment and Report

Run the verification checks before reporting completion:

1. Confirm each installed host's instruction file contains both the `<!-- BEGIN SHARED SKILLS RULES --> ... <!-- END SHARED SKILLS RULES -->` block and the `<!-- graphify -->` rule block.
2. Confirm `~/.<tool>/skills/` is a clean git sparse checkout on `main` and all 25 skill directories exist.
3. Execute each `ensure-<tool>-link.sh` and `enforce-<tool>-rules.sh` script once from the shell and confirm exit code `0` and valid output.
4. Validate every modified JSON/TOML settings file (`python3 -m json.tool` / `tomllib`).
5. Present a concise status table patterned after `examples/bootstrap-audit-report.md`.
