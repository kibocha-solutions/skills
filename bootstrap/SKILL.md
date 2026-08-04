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
- The block is located by the *first* start marker and the *last* end marker, not a naive non-greedy regex span — needed because the rules content itself legitimately quotes these exact marker strings as documentation (this section, for one), which would otherwise fool a `.*?`-style match into stopping at that literal mention instead of the real closing marker.

Each `ensure-*-link.sh` script also syncs this repo's skill folders (anything
with a top-level `SKILL.md`) into `<tool-home>/skills/`, using the shared
`sync_skills_from_git` helper in `lib.sh`. **This is a real git working
copy, not a file copy**: each `<tool-home>/skills/` is `git init`'d in place
and tracks this repo's actual remote (`git remote get-url origin`, resolved
from the local checkout the bootstrap scripts run from, falling back to
`git@github.com:kibocha-solutions/skills.git`), branch `main`. Every run does
`fetch` + re-apply sparse-checkout + `reset --hard origin/main`, so each
tool's copy always exactly matches what's actually pushed to the remote —
never a possibly-uncommitted or stale local working-tree state, and a skill
removed from the repo is automatically removed from every tool's copy too
(sparse-checkout re-application drops paths that fall out of the pattern
set).

The sparse-checkout uses **non-cone mode** with an explicit pattern per
skill directory plus `AGENTS.md` — cone mode was tried first and rejected,
since cone mode always includes every root-level file regardless of the
directory pattern list (`README.md`, `LICENSE.txt`, `.gitignore`,
`migration-log.md`, and this repo's two code-review-graph ignore files would
all have leaked into every tool's `skills/` folder). Non-cone mode checks
out exactly what's listed and nothing else — no `sources/`, no `docs/`, no
repo-root clutter in any tool's skills directory.

Because `git init` is used in place rather than `git clone` (which refuses
a non-empty directory), this works even when `<tool-home>/skills/` already
has unrelated content sitting in it — a tool's own bundled/native skills —
since git only ever manages paths in its own tracked tree and leaves
untracked neighbors alone (e.g. Codex CLI's own bundled skills under
`~/.codex/skills/.system/`, or Antigravity's native skills — see below). On
the first run against a directory that isn't a git repo yet (i.e. was
previously populated by the old rsync-based mirror), any existing top-level
entry whose name matches a known skill folder in the local checkout is
removed first, so the initial checkout has no stale collisions to contend
with; anything whose name doesn't match a known skill is left untouched.

### Environment & Platform Resolution

- **Native Linux & macOS**: Target paths resolve dynamically to `$HOME/.<tool>/<filename>`.
- **WSL (Windows Subsystem for Linux)**: In addition to `$HOME/.<tool>/<filename>`, scripts inspect `/mnt/c/Users/`, resolve the active Windows host username dynamically, and align `/mnt/c/Users/<win_user>/.<tool>/<filename>` if present.

| Tool | Target Global Instruction File | Rule Integration Method |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | Non-destructive block alignment |
| Codex CLI | `~/.codex/AGENTS.md` | Non-destructive block alignment |
| Gemini CLI | `~/.gemini/GEMINI.md` | Non-destructive block alignment |
| Gemini Antigravity | `~/.gemini/antigravity/builtin/GEMINI.md` | Non-destructive block alignment (separate product from Gemini CLI, separate file — see below) |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` | Non-destructive block alignment |

## Running the Bootstrap Verification & Alignment

Run the alignment scripts for whichever tools are installed:

```bash
bash ~/.claude/skills/bootstrap/scripts/ensure-claude-link.sh
bash ~/.codex/skills/bootstrap/scripts/ensure-codex-link.sh
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-link.sh
bash ~/.copilot/skills/bootstrap/scripts/ensure-copilot-link.sh
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-builtin-skills.sh
```

Each script is idempotent and reports only when changes are made.

## Gemini Antigravity Builtin Rules & Skills Mirror

Google Antigravity (`~/.gemini/antigravity/`) is a separate product from
Gemini CLI. It does not read `~/.gemini/GEMINI.md` or `~/.gemini/skills/` —
confirmed directly on-disk (Antigravity has never picked up rules placed at
the CLI location). It ships its own default skills in
`~/.gemini/antigravity/builtin/skills/` (e.g. `agy-customizations`,
`antigravity_guide`, `permissioned-github`), and reads its own rules file at
`~/.gemini/antigravity/builtin/GEMINI.md`.

`ensure-gemini-builtin-skills.sh` handles both, targeting
`~/.gemini/antigravity/builtin/` directly:

- Aligns `~/.gemini/antigravity/builtin/GEMINI.md` with this repo's
  `AGENTS.md` non-destructively (same `align_agent_rules` mechanism and
  block markers `ensure-gemini-link.sh` uses for the CLI location) — this is
  a *separate* copy from `~/.gemini/GEMINI.md`, not a symlink, since the two
  products read different files.
- Syncs every skill folder in this repo (anything with a top-level
  `SKILL.md`) into `~/.gemini/antigravity/builtin/skills/` via
  `sync_skills_from_git` (see above — a real git sparse checkout tracking
  the remote, not a file copy). It never touches Antigravity's own native
  skills (`agy-customizations`, `antigravity_guide`, `permissioned-github`),
  since git only manages paths in its own tracked tree.

It no-ops silently if `~/.gemini/antigravity/builtin/` doesn't exist
(Antigravity not installed).

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
