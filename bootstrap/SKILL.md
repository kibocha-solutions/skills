---
name: bootstrap
description: Verify and align shared agent rules and skill mirrors for Claude Code, Codex, Gemini CLI, Gemini Antigravity, and GitHub Copilot across Linux, macOS, and WSL. Use for new workstation setup, stale installed skills, shared-rule alignment, session-start hook registration, or /bootstrap.
---

# Bootstrap

## 1. Establish scope

1. Identify the installed agent hosts.
2. Identify native Linux, macOS, and WSL target paths.
3. Confirm that the user requested alignment or bootstrap propagation.
4. Read the repository root `AGENTS.md`.
5. Read `references/hook-registration.md` only when registering hooks.
6. Do not run a script for an unrequested host.

## 2. Verify the source repository

1. Resolve the repository root.
2. Verify the configured `origin` URL.
3. Verify that the intended branch is `main`.
4. List every top-level directory containing `SKILL.md`.
5. Confirm that the working tree changes intended for deployment are committed
   and pushed.
6. Stop if the remote state does not contain the intended rules and skills.

## 3. Resolve targets

Use these instruction files:

| Host | Instruction file |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` |
| Codex | `~/.codex/AGENTS.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` |
| Gemini Antigravity | `~/.gemini/antigravity/builtin/GEMINI.md` |
| GitHub Copilot | `~/.copilot/copilot-instructions.md` |

1. Resolve each installed host's home directory.
2. Under WSL, resolve the active Windows user under `/mnt/c/Users/`.
3. Include an existing Windows-host instruction path.
4. Keep Gemini CLI and Gemini Antigravity targets separate.
5. Skip a target whose product directory does not exist.

## 4. Align rules

1. Use these block markers:

```text
<!-- BEGIN SHARED SKILLS RULES -->
<!-- END SHARED SKILLS RULES -->
```

2. Replace the content between the first start marker and the last end marker.
3. Preserve all content outside the marker block.
4. Remove legacy `@skills/AGENTS.md` import pointers.
5. Replace a legacy instruction-file symlink with a regular file when the host
   requires one.
6. Never overwrite unrelated user instructions.

## 5. Synchronize skills

1. Initialize the target `skills/` directory as a Git working copy when
   required.
2. Preserve unrelated untracked host-native skills.
3. Resolve `origin` from the source checkout.
4. Fall back to `git@github.com:kibocha-solutions/skills.git` only when the
   source checkout has no usable `origin`.
5. Configure non-cone sparse checkout.
6. Include `AGENTS.md` and every top-level skill directory.
7. Exclude `sources/`, `docs/`, and unrelated root files.
8. Fetch `origin/main`.
9. Reapply the sparse-checkout patterns.
10. Reset the managed working copy to `origin/main`.
11. Remove a stale collision only when its top-level name matches a managed
    skill.
12. Never remove an unrelated host-native skill.

## 6. Run host scripts

Run only the scripts for confirmed targets:

```bash
bash ~/.claude/skills/bootstrap/scripts/ensure-claude-link.sh
bash ~/.codex/skills/bootstrap/scripts/ensure-codex-link.sh
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-link.sh
bash ~/.copilot/skills/bootstrap/scripts/ensure-copilot-link.sh
bash ~/.gemini/skills/bootstrap/scripts/ensure-gemini-builtin-skills.sh
```

For a source-checkout invocation, use the matching script under
`bootstrap/scripts/`.

## 7. Handle Gemini Antigravity

1. Target `~/.gemini/antigravity/builtin/`.
2. Align `builtin/GEMINI.md`.
3. Synchronize managed skills into `builtin/skills/`.
4. Preserve `agy-customizations`, `antigravity_guide`,
   `permissioned-github`, and other unmanaged native skills.
5. Check for `builtin/.checksum`.
6. Warn the user before modifying `builtin/` when the checksum exists.
7. Stop if Antigravity reports corruption or resets the directory.

## 8. Register automated alignment

1. Read `references/hook-registration.md`.
2. Add only the requested host's `SessionStart` hook.
3. Preserve unrelated hook configuration.
4. Run the registered command once.
5. Confirm that repeated execution produces no unintended change.

## 9. Verify

1. Confirm that each target instruction file contains exactly one complete
   marker block.
2. Confirm that content outside the block is unchanged.
3. Confirm that each managed skill matches `origin/main`.
4. Confirm that deleted repository skills are absent from managed mirrors.
5. Confirm that native skills remain present.
6. Confirm that no `sources/`, `docs/`, or unrelated root files entered a
   mirror.
7. Report changed targets, skipped targets, warnings, and failures.
