# Tasks: Production wrs Writerside Wrapper

State: DONE (537114d pushed and synced to every installed host)

## Phase 0: Orientation

- [x] Read skills repo AGENTS.md, memory, active sessions, relevant handoff
- [x] Read bootstrap, skill-creator, system-init SKILL.md and routed references
- [x] Research builder image, env vars, build groups, CLI conventions

## Phase 1: Tool

- [x] Write `documentation/scripts/wrs` (Python, stdlib)
- [x] Verify builder exit-code behavior under rootless Podman (0 on success, 255 on check failure)
- [x] Test build (all, single, failing case), serve, routing, status, stop, clean
- [x] Browser test
- [x] Install to `~/.local/bin/wrs` with backup of the Bash version

## Phase 2: Skills

- [x] Snapshot documentation skill (scratchpad, from git HEAD); read skill-authoring-standard
- [x] Update install reference and every pinned image tag; add Podman to toolchain; example and evals added
- [x] Validate repo (only the 2 pre-existing errors); read every changed skill file in full
- [!] Stop for user approval before commit, push, bootstrap sync

## Added

- [x] Dev-key mode (Bitwarden `bw`, keyring session, 21-day rotation): approved by user, implemented in second round

### Added 2026-09-24 (user request, second round)

- [x] `serve` builds missing sites for the requested instances (all when none named); `--build` forces rebuild
- [x] Default port base 44190 (portal 44190, instances 44191+)
- [x] `-d/--dev`: Bitwarden-gated local compound mode (key in keyring, 21-day rotation with fresh unlock, TOTP when the item has a seed); non-dev serves public and internal only
- [x] Move background to `-b/--background`; remove `--allow-upward`
- [x] Fix validator errors: communications TBD marker, pdf reference contents
- [x] Update install reference, example, evals for the new flags
- [x] Test (simulated bw; read-only real bw status), browser test, reinstall
- [x] Tier check (`wrs check`, run after every passing build) for lower-to-higher links and title mentions

### Added 2026-09-24 (user request, third round)

- [x] Research 1Password CLI (`op`) item, signin, and OTP commands from primary documentation
- [x] Vault backend abstraction in `wrs`: Bitwarden (`bw`) and 1Password (`op`); selection by config, env, flag, `op://` item, installed CLI (mirrors the recovery toolkit's source selection)
- [x] Spinner animation around non-interactive vault steps (sync, item read, key create or rotate, save)
- [x] Test both backends with simulated CLIs; PTY check that the spinner renders and never overlaps a prompt
- [x] Update install reference, help text, evals; validator; reinstall; full re-read
- [x] Found during testing: bw create/edit took the encoded item (key in base64) as an argument; moved to stdin per Bitwarden CLI docs

### Added 2026-09-24 (user request, fourth round)

- [x] Remove TOTP from the dev gate (user correction: TOTP was agreed off; vault 2FA is the second factor); code, tests, reference
- [x] Confirm the documentation skill's installed copies match the repository state (mirrors equal committed HEAD; working changes reach them only through push and bootstrap)
- [x] Stop all wrs servers (msngi server stopped; no wrs container remains)
- [x] Handoff in each repository
- [x] Single commit per repository including every pending file (ci-cd section 6)
- [x] User approved amend and push (2026-09-24): commit amended with this record and pushed to origin/main
- [x] Bootstrap sync to installed hosts on user request (2026-09-24)

### Added 2026-09-24 (user request, fifth round)

- [x] Clarify in AGENTS.md how documents reference other documents: title only in external deliverables (proposals, correspondence, reports, policies, filed records); relative links inside a technical documentation library; no reference to a higher-sensitivity document
- [x] AGENTS.md word limit: user chose to drop the 9.6 identifier bullet duplicated by 8.2 (1,498 words)
- [x] Validate, word count, full read; amend the pushed commit (includes the session updates); push with lease
- [x] Bootstrap all hosts; verify rule blocks
