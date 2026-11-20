Aligned `AGENTS.md` Sections 10.1 and 13.1 through 13.3 and `.agents/memory/agents-md-limits-and-cross-references.md` with the `coordinator` graduating wake timer (`1m->3m->5m->12m->15m->30m`), explicit prohibition on fixed 30-minute heartbeats, and `chat`/`wake tick` terminology.

# Walkthrough: Align AGENTS.md with Coordinator Graduating Wake Rules

## 2026-11-20 11:39
- Baseline repository state recorded: branch `main` at `30419ec2f5657666f4a2dbf309d8701f40760577` (`origin/main`), clean worktree, `approval_mode: ask`, `AGENTS.md` at 2,488 words, `tools/validate-all.sh` showing 14 pre-existing baseline errors in unchanged `ci-cd/` and `communications/` files and zero errors in `AGENTS.md`.
- Verified workstation hosts: Claude Code (`~/.claude`), Codex (`~/.codex`), Gemini Antigravity/CLI (`~/.gemini`), and GitHub Copilot (`~/.copilot`), with all existing JSON/TOML hook and MCP config files valid.
- Verified Git signing (`JohnKibocha <johnkibocha@outlook.com>`, SSH key `/home/vaelric/.ssh/ssh-signing-key-universal.pub`, Bitwarden SSH program) and SSH push access to `git@github.com:kibocha-solutions/skills.git`.

## 2026-11-20 11:41
- Updated `AGENTS.md` Section 10.1 to require usage-window checks at start and every graduating wake tick (`coordinator/references/heartbeat-and-wake.md`) instead of `at least every 30 minutes during active work`, preserving `§1` through `§14` numbering and excluding hard-coded usage percentages.
- Updated `AGENTS.md` Section 13.1 (`chat` instead of `session`), Section 13.2 (mandating `coordinator/SKILL.md` for coordinated and standalone sustained work with the single graduating wake timer `1m->3m->5m->12m->15m->30m`, reset to `1m` on action, `90-120m` user-blocked, cancelled at completion, and explicitly forbidding a fixed 30-minute heartbeat), and Section 13.3 (`wake tick` instead of `scheduled check-in`).
- Updated `.agents/memory/agents-md-limits-and-cross-references.md` to reflect the Section 10.1 and Section 13.1 through 13.3 changes.
- Verification: read both modified files in full from disk; confirmed zero U+2014 em dashes and zero AI attribution; `python3` word-count check returned `AGENTS.md words: 2498` (`assert w < 2500` passed); `tools/validate-all.sh` reported zero errors in `AGENTS.md` and `.agents/` (only the 14 unchanged baseline errors in `ci-cd/` and `communications/`); `git diff --check` exited `0`; `python3 steward/scripts/steward.py check` output `steward check: clean`.
- Note on user query reference: `/mnt/data/workspace/skills/AGENTS.md` has Sections 1 through 14 and no Section 3.6; the `AGENTS.md section 3.6` fixed 30-minute heartbeat cited by the user belongs to a separate frontend-rebuild repository outside this workspace.
- Following session close, changes will be committed as one signed commit, pushed to `origin/main`, and synced across all installed hosts via `/bootstrap`.
