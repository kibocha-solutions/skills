---
name: skills-repo-deployment-workflow
description: How this repo is deployed across tools and the standard workflow for publishing a change to it
type: project
---

This repository (`git@github.com:kibocha-solutions/skills.git`) is the single
working copy. Each tool's `skills/` directory (`~/.claude/skills`,
`~/.codex/skills`, `~/.gemini/skills`, `~/.copilot/skills`) is a real Git
working copy tracking this repository's remote, initialized in place with a
non-cone sparse checkout (every skill folder plus `AGENTS.md`, nothing else
at repository root). The `bootstrap` skill's `ensure-*-link.sh` scripts populate
it via the shared `sync_skills_from_git` helper in `bootstrap/scripts/lib.sh`.
Every run performs `fetch`, sparse checkout re-apply, and `reset --hard origin/main`.
A skill removed from this repository is automatically removed from every tool's
copy. Re-running the tool's `ensure-*-link.sh` script or allowing its
`SessionStart` hook to fire refreshes the working copy.

For Google Gemini (both CLI and Antigravity), managed skills live in
`~/.gemini/skills/` and are registered in `~/.gemini/config/skills.json` with a
symlink at `~/.gemini/config/skills`. The `~/.gemini/antigravity/builtin/skills/`
directory is reserved strictly for native IDE builtins (`agy-customizations`,
`antigravity_guide`, `generative_ui`, `migrate-workflows`,
`permissioned-github`) and is cleaned of managed repository skills.

`AGENTS.md` at the repository root is the single source of truth for behavioral
rules across all tools. Each tool's canonical global instruction file
(`CLAUDE.md`, `AGENTS.md` for Codex, `GEMINI.md`, `copilot-instructions.md`)
receives this file's full contents embedded between `<!-- BEGIN SHARED SKILLS
RULES -->` and `<!-- END SHARED SKILLS RULES -->` markers via `align_agent_rules`
in `lib.sh`. Redundant `AGENTS.md` files at the root of `~/.gemini/`,
`~/.claude/`, and `~/.copilot/` are automatically removed during alignment.

Standard workflow for publishing a change to this repository:

1. Make the requested change in the working copy.
2. If the change is a new predominant unit of work, create a single commit
   following `ci-cd/SKILL.md` commit hygiene expectations: one canonical type,
   one specific scope, imperative title without trailing period, prose body 72
   words or fewer without bullet lists or file paths, and zero AI attribution.
3. If the change is a direct fix to work not yet pushed, amend the existing
   commit without changing its message (`git commit --amend --no-edit`).
4. Push to `origin main`.
5. Re-run `ensure-*-link.sh` across installed tools.
6. Verify MCP servers and lifecycle hooks (`UserPromptSubmit` for Claude Code,
   `PreInvocation` for Antigravity, and `SessionStart` for Codex and Copilot).

Updates to this memory system (`.agents/MEMORY.md` and `.agents/memory/`)
are included in the in-progress commit and omitted from commit messages.
