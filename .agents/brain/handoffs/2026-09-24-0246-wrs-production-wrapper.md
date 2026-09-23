# Handoff: wrs Production Wrapper and Documentation Skill Update

**Date:** 2026-09-24
**Repository:** `/mnt/data/workspace/skills` (`git@github.com:kibocha-solutions/skills.git`)
**Session:** `.agents/brain/sessions/active/2026-09-24-0040-wrs-production-wrapper/`

## Objective

Replace the Bash `wrs` wrapper with a production Python tool shipped in the
`documentation` skill, move the skill to builder image `2026.08.0328` with
Podman support, and clear the repository validator.

## Completed work

- `documentation/scripts/wrs` 2.2.0 (Python standard library): parallel build
  of every instance with a live board, tier check after every passing build,
  `serve` that builds missing sites, ports 44190 (portal) to 44194, `-d/--dev`
  dev gate, `-b/--background`, `--lan` for ungated tiers, `--lan-all` behind
  basic auth with `--dev`, and `check`, `key`, `status`, `stop`, `open`,
  `logs`, `clean`, `update`, `doctor`.
- Dev gate: one local key for the whole compound, held in a Bitwarden or
  1Password login item, cached in the login keyring, rotated every 21 days
  after a fresh sign-in. No TOTP (agreed 2026-09-23; see memory
  `wrs-dev-gate`). Item values reach `bw` and `op` on stdin only. A spinner
  covers every non-interactive vault step and clears before each prompt.
- Skill files: install reference rewritten, SKILL.md steps 8.6, 8.7, and 9.3,
  validation example, four eval cases, diagram-export steps, Podman toolchain
  row.
- Validator errors fixed: correspondence reference TBD token, PDF reference
  contents section.

## Verification

- `tools/validate-all.sh`: PASS (21 skills; shell and whitespace checks).
- `wrs` SHA-256 `30f4c2694ffc443eb57ba10097f47563bbfab4816d11ddc26806b75710c363f7`,
  byte-identical to `~/.local/bin/wrs`; prior builds kept as
  `~/.local/bin/wrs.previous` and `~/.local/bin/wrs.bash-backup`.
- Builds of the msngi documentation: four instances, 181/181 checks each;
  tier check 66 pages, no upward link.
- Dev gate tested against simulated `bw`, `op`, and `secret-tool` on a PTY:
  first key, cached key with zero vault calls, forced and expired rotation,
  wrong password, denied app approval, manager selection, no key in any argv.
  The user's own `wrs serve --dev` run created the real Bitwarden dev key; no
  `op` binary or 1Password account exists on this host, so the 1Password
  backend is verified against a documentation-derived simulator only.
- All `wrs` servers stopped.

## Git state

| Field | Value |
|---|---|
| Current branch | `main` |
| Intended base | `origin/main` (trunk; the repository takes direct commits) |
| Branch purpose | Shared skills source for every agent host |
| Branch lifetime | Durable trunk |
| Publication and review state | One signed commit pushed to `origin/main` on user approval |
| History cleanup state | Clean; one commit authorized and delivered |
| Procedural commit count | 1 from starting commit `12df7f0` |
| Required checks | `bash tools/validate-all.sh` |
| Safest next Git action | Run the bootstrap `ensure-*-link.sh` scripts for the installed hosts when the user requests the sync |

## Blockers

- Bootstrap sync needs an explicit user request. Until it runs, the installed
  mirrors (`~/.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`,
  `~/.copilot/skills`) keep the previous documentation skill.

## Next action

On request: run bootstrap for the installed hosts, confirm each mirror's
`documentation/` matches `origin/main`, then set the session state to DONE and
archive it at the next task.
