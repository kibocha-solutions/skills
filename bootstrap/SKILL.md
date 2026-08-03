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

Each `ensure-*-link.sh` script also mirrors this repo's skill folders (anything
with a top-level `SKILL.md`) into `<tool-home>/skills/`, using the shared
`mirror_skills` helper in `lib.sh`. Every skill is overwritten by name on each
run — so a `git pull` in this repo propagates to every tool's mirror the next
time bootstrap runs — while anything already in `<tool-home>/skills/` that
doesn't match a skill name from this repo is left alone (e.g. Codex CLI's own
bundled skills under `~/.codex/skills/.system/`).

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

## Gemini Antigravity Builtin Skills Mirror

Google Antigravity (`~/.gemini/antigravity/`) is a separate product from
Gemini CLI. It ships its own default skills in
`~/.gemini/antigravity/builtin/skills/` (e.g. `agy-customizations`,
`antigravity_guide`, `permissioned-github`) rather than reading `~/.gemini/skills/`.

`ensure-gemini-builtin-skills.sh` mirrors every skill folder in this repo
(anything with a top-level `SKILL.md`) into that directory, overwriting each
skill by name on every run so `git pull` changes in this repo propagate the
next time it runs. It never touches Antigravity's own native skills, since
none of them share a name with a skill in this repo. It no-ops silently if
`~/.gemini/antigravity/builtin/skills/` doesn't exist (Antigravity not
installed).

```bash
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-builtin-skills.sh
```

Note: `~/.gemini/antigravity/builtin/.checksum` sits alongside this
directory and appears to be an integrity check written at install time.
Mirroring skills into `builtin/skills/` will make the on-disk contents no
longer match that checksum. Whether Antigravity enforces this at runtime is
unconfirmed — the app binary wasn't available to inspect. If Antigravity
ever reports corruption or resets its builtin skills after this runs, that
checksum is the likely cause.

## Automated Alignment

Register the scripts as a `SessionStart` hook in each tool's settings to run alignment automatically when a session starts. See `references/hook-registration.md` for hook JSON configurations.
