---
name: bootstrap
description: >
  Verifies and repairs the link between this shared skills repository and
  each coding agent's own memory file (CLAUDE.md, AGENTS.md, GEMINI.md,
  copilot-instructions.md) after a fresh clone or pull into a new
  environment. Use when setting up a new machine or environment, when this
  repo's skills are visibly present on disk but AGENTS.md's rules don't seem
  to be loading, or when asked to check, fix, verify, or bootstrap the
  skills-repo linking. Trigger: `/bootstrap`.
---

# Bootstrap

This repo (`skills`) is pulled independently into each tool's own home
directory: `~/.claude/skills/`, `~/.codex/skills/`, `~/.gemini/skills/`,
`~/.copilot/skills/`. `AGENTS.md` at the repo root is the single source of
truth for behavioral rules across all four.

The problem this skill exists to catch: none of the four tools auto-load a
memory file that sits one directory level deeper than their native location.
`<tool-home>/skills/AGENTS.md` is never discovered on its own — each tool
needs a one-line pointer in its own real global file, and Codex needs a
symlink instead of a pointer since it speaks the `AGENTS.md` format natively.
If that pointer is missing (new environment, fresh pull, manual edit that
got reverted), the tool runs with none of this repo's rules loaded even
though the skill files are sitting right there on disk — silently.

## What "linked" means, per tool

| Tool | Real global file | Fix |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | first line is `@skills/AGENTS.md` |
| Codex CLI | `~/.codex/AGENTS.md` | is a symlink to `skills/AGENTS.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` | first line is `@skills/AGENTS.md` |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` | first line is `@skills/AGENTS.md` (relative — Copilot rejects `~/`-prefixed imports) |

## Running the check

Run whichever of these exist for the tools in use (missing tool directories
are expected and not an error — skip them):

```bash
bash ~/.claude/skills/bootstrap/scripts/ensure-claude-link.sh
bash ~/.codex/skills/bootstrap/scripts/ensure-codex-link.sh
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-link.sh
bash ~/.copilot/skills/bootstrap/scripts/ensure-copilot-link.sh
```

Each script is idempotent: it does nothing and reports nothing if the link
already holds, and reports the one line it changed if it had to fix
something. This is the pre-authorized exception in `AGENTS.md`'s Tooling and
Dependencies section — these scripts may edit a file outside the current
workspace without asking first, specifically because the edit is narrow,
additive, and always reported.

Codex's script may also back up a pre-existing, non-symlink `AGENTS.md`
before replacing it with the symlink — check for a
`AGENTS.md.pre-bootstrap.<timestamp>` file alongside it if prior content
needs recovering.

## Making the check automatic

Running the scripts by hand only helps if you remember to. For it to catch a
missing link on its own, register the matching script as a `SessionStart`
hook in that tool's settings — see `references/hook-registration.md` for the
exact JSON per tool, including how to merge into an existing hook config
without clobbering other hooks already registered there (e.g. `code-review-graph`
integrations already present in this environment).

Hook registration is a one-time, per-machine step. It is not part of what
`git pull` refreshes, so it survives repo updates and only needs doing once
per environment.

## Also worth knowing on a fresh setup

Once linked, skim what else this repo offers before diving into task work —
in particular `graphify` (`~/.claude/skills/graphify/SKILL.md`, `/graphify`),
which is generally useful for any codebase-impact or architecture question
and is easy to miss if you go looking for task-specific skills only.
