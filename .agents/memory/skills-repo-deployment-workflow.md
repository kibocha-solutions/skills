---
name: skills-repo-deployment-workflow
description: How this repo is deployed across tools and the standard workflow for publishing a change to it
type: project
---

This repo (`git@github.com:kibocha-solutions/skills.git`) is the single
working copy. Each tool's `skills/` directory (`~/.claude/skills`,
`~/.codex/skills`, `~/.gemini/skills`, `~/.copilot/skills`) is **not** a
separate `git clone` — it's a plain-file mirror that the `bootstrap` skill's
`ensure-*-link.sh` scripts populate directly from this working copy via the
shared `mirror_skills` helper in `bootstrap/scripts/lib.sh` (an `rsync
--delete --checksum` per skill folder, overwriting by name). There is nothing
to `git pull` in those locations — re-running the tool's `ensure-*-link.sh`
(or letting its `SessionStart` hook fire) is what refreshes them. Google
Antigravity is a separate case: it has its own default skills at
`~/.gemini/antigravity/builtin/skills/`, distinct from Gemini CLI's
`~/.gemini/skills/`, kept in sync by the dedicated
`ensure-gemini-builtin-skills.sh` script using the same `mirror_skills`
helper — see `bootstrap/SKILL.md`.

`AGENTS.md` at the repo root is the single source of truth for behavioral
rules across all four tools. Each tool's own global memory file
(`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `copilot-instructions.md`) gets this
file's full contents non-destructively embedded between `<!-- BEGIN SHARED
SKILLS RULES -->` / `<!-- END SHARED SKILLS RULES -->` markers by
`align_agent_rules` in `lib.sh` — not a one-line `@skills/AGENTS.md` pointer
or a symlink (both are legacy; `align_agent_rules` actively cleans up the old
pointer line and `ensure-codex-link.sh` replaces a pre-existing symlink with
a real file). Content outside the markers is preserved untouched.

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
5. Re-run the relevant `ensure-*-link.sh` script per installed tool (and
   `ensure-gemini-builtin-skills.sh` if Antigravity is present) — idempotent,
   safe to run unconditionally. This refreshes both the embedded rules block
   and every tool's skill mirror in one pass; no separate per-location `git
   pull` step exists in this workflow.

Updates to this memory system (`.agents/MEMORY.md` and `.agents/memory/`)
are swept into whatever commit is already in progress and are not called out
in the commit message.
