---
name: skills-repo-deployment-workflow
description: How this repo is deployed across tools and the standard workflow for publishing a change to it
type: project
---

This repo (`git@github.com:kibocha-solutions/skills.git`) is independently
cloned into four tool-specific locations on each machine: `~/.claude/skills`,
`~/.codex/skills`, `~/.gemini/skills`, `~/.copilot/skills`. These are
separate `git clone`s of the same remote, not symlinks — pushing from the
working copy does not update them; each needs its own `git pull --ff-only`.

`AGENTS.md` at the repo root is the single source of truth for behavioral
rules across all four tools. Each tool's own global memory file points at it
via a one-line pointer (`@skills/AGENTS.md` for Claude Code, Gemini CLI, and
GitHub Copilot CLI; a symlink for Codex CLI, since Codex reads `AGENTS.md`
natively). See the `bootstrap` skill for the mechanics and the `SessionStart`
hooks registered in each tool's own config that keep the link self-healing.

**Standard workflow for publishing a change to this repo:**

1. Make the requested change(s) in the working copy.
2. Where the change is a new predominant unit of work, create a new commit
   following `ci-cd/SKILL.md`'s Commit Hygiene Expectations: single scope
   (never compound), title names the predominant change only, body 72 words
   or fewer focused on the useful work, one compressed trailing sentence for
   any secondary change swept in — never a split into multiple commits just
   because the diff had more than one strand.
3. Where the change is instead a direct fix to work that hasn't become its
   own story yet (e.g. correcting something just committed), amend the
   existing commit without changing its message (`git commit --amend
   --no-edit`) instead of creating a new one. Ask if it's unclear which
   applies.
4. Push to `origin main` — this repo's history is almost entirely
   direct-to-main commits, not PRs.
5. Pull into all four tool directories: `git -C ~/.claude/skills pull
   --ff-only`, and the same for `~/.codex/skills`, `~/.gemini/skills`,
   `~/.copilot/skills`.
6. Re-run the relevant `ensure-*-link.sh` script per tool (idempotent, safe
   to run unconditionally) to confirm the pointer or symlink still holds.

Updates to this memory system (`.agents/MEMORY.md` and `.agents/memory/`)
are swept into whatever commit is already in progress and are not called out
in the commit message.
