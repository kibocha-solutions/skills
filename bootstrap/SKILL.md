---
name: bootstrap
description: >
  Verifies and aligns shared agentic rules between this skills repository and
  each coding agent's own instruction file (CLAUDE.md, AGENTS.md, GEMINI.md,
  copilot-instructions.md) across native Linux, macOS, and WSL environments. Use
  when setting up a new environment, when shared rules need aligning, or when
  running /bootstrap.
---

# Bootstrap

This repository (`skills`) is mirrored into each tool's home directory:
`~/.claude/skills/`, `~/.codex/skills/`, `~/.gemini/skills/`, `~/.copilot/skills/`
(as well as dynamically detected Windows host paths under `/mnt/c/Users/<username>/` when running in WSL). `AGENTS.md` at the repo root is the master source of truth for shared behavioral rules across all tools.

## Rule Alignment & Cross-Platform Support

Rather than using import pointers (`@skills/AGENTS.md`) or symlinks—or overwriting pre-existing user instructions—bootstrapping aligns each target tool's native instruction file non-destructively:

- Embedded block markers (`<!-- BEGIN SHARED SKILLS RULES -->` and `<!-- END SHARED SKILLS RULES -->`) delineate the shared rules block.
- Pre-existing custom user instructions outside the block are fully preserved.
- Legacy import pointers are safely cleaned up.

### Environment & Platform Resolution

- **Native Linux & macOS**: Target paths resolve dynamically to `$HOME/.<tool>/<filename>`.
- **WSL (Windows Subsystem for Linux)**: In addition to `$HOME/.<tool>/<filename>`, scripts inspect `/mnt/c/Users/`, resolve the active Windows host username dynamically, and align `/mnt/c/Users/<win_user>/.<tool>/<filename>` if present.

| Tool | Target Global Instruction File | Rule Integration Method |
|---|---|---|
| Claude Code | `CLAUDE.md` | Non-destructive block alignment |
| Codex CLI | `AGENTS.md` | Non-destructive block alignment |
| Gemini CLI | `GEMINI.md` | Non-destructive block alignment |
| GitHub Copilot CLI | `copilot-instructions.md` | Non-destructive block alignment |

## Running the Bootstrap Verification & Alignment

Run the alignment scripts for whichever tools are installed:

```bash
bash ~/.claude/skills/bootstrap/scripts/ensure-claude-link.sh
bash ~/.codex/skills/bootstrap/scripts/ensure-codex-link.sh
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-link.sh
bash ~/.copilot/skills/bootstrap/scripts/ensure-copilot-link.sh
```

Each script is idempotent and reports only when changes are made.

## Automated Alignment

Register the scripts as a `SessionStart` hook in each tool's settings to run alignment automatically when a session starts. See `references/hook-registration.md` for hook JSON configurations.
