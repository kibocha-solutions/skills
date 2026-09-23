# Walkthrough: Production wrs Writerside Wrapper

## Phase 0

Orientation and research complete; findings recorded in
`implementation_plan.md` (Research record).

## Phase 1: Tool

- `documentation/scripts/wrs` 2.0.0, Python 3.12 stdlib, installed to
  `~/.local/bin/wrs` (identical SHA-256); Bash original kept as
  `~/.local/bin/wrs.bash-backup`.
- Builder exit status probe (2026.08.0328, rootless Podman 4.9.3): 0 on a
  passing build with the JCEF ELEVATED_PRIVILEGES line present; 255 on a
  failing check; failing log still contains "All done, exiting successfully".
- Tests: `wrs doctor --online` all pass; `wrs build` all four msngi instances
  ok (181/181 each, 3m35s, 2 parallel); failing scratch build exits 1 with
  REF002 file and line and log path; PTY run shows 10 spinner frames, 506
  in-place redraws, cursor hidden and restored; serve routing verified with
  curl (start pages 200, higher-tier page 404 with neutral page, lower-tier
  page 302 with query preserved, `--allow-upward` 302 upward); foreground
  serve shows live status line, colored access log, Ctrl-C removes container;
  `status`, `status --json`, `logs`, `open`, `stop`, `clean` verified; zero
  leftover containers.
- Browser: portal renders with correct instance links; internal start page
  renders with images; internal->public redirect lands on public; internal
  request for restricted page shows neutral 404; restricted serves internal
  page with zero broken images.
- Defects found and fixed during testing: project name shown as "docs";
  page count included index.html; pluralization; health probes logged;
  access lines written onto the live status line; failure message order.

## Phase 2: Skills

- Changed: `documentation/references/install-writerside.md` (rewritten),
  `documentation/SKILL.md` (steps 8.6, 8.7, 9.3),
  `technical-diagrams/references/writerside-diagram-export.md` (steps 6, 7),
  `system-init/references/toolchain.md` (Podman). New:
  `documentation/scripts/wrs`, `documentation/examples/writerside-validation.md`,
  `documentation/evals/evals.json`.
- Evaluation: paired with-skill and baseline agent runs not executed
  (independent agents not authorized in this session); cases graded against
  this session's executed evidence: eval 1 install/doctor/build all pass;
  eval 2 403 root cause, serve, 200 and 404 checks pass; eval 3 doctor,
  multi-instance build, completion-line check, served inspection pass.
- `tools/validate-all.sh`: same two pre-existing errors (communications TBD,
  pdf reference contents); none introduced.
- Stopped before commit, push, and bootstrap sync (user approval required).

## Second round (2026-09-24)

- `wrs` 2.1.0: `serve` builds missing sites (named instances, or all); `--build`
  forces a rebuild; port base 44190 (portal) with instances 44191 to 44194;
  `-d/--dev` opens the Bitwarden dev gate; `-b/--background`; `--allow-upward`
  removed; `--lan` exposes ungated tiers only; `--lan-all` requires `--dev` and
  puts gated tiers behind basic auth; `wrs check` and `wrs key status|rotate|lock`
  added; the tier check runs after every passing build.
- Gate tests with simulated `bw` and `secret-tool`: first unlock creates the item
  and caches the key; cached key opens without a prompt; expired key rotates with
  fresh unlock and TOTP; wrong TOTP and wrong password rejected; `key lock` and
  `key status` verified; LAN exposure returns 401 without auth and 200 with the
  dev key. Real `bw` touched read-only (`status`: locked); real keyring holds no
  dev key.
- Serve rules verified: non-dev serves public and internal only; a named gated
  instance without `--dev` exits 2; `--lan-all` without `--dev` exits 2;
  missing-site auto-build verified. Browser: portal with four books under dev,
  confidential topics render in book, internal request for a confidential page
  returns the neutral 404.
- Validator errors fixed: communications correspondence reference reworded to
  state the prohibition without the literal marker token; pdf advanced reference
  given a Contents section. `tools/validate-all.sh`: PASS, 21 skills, zero errors.
- Install reference, validation example, and evals updated to 2.1 flags; each
  changed file re-read in full. Installed `~/.local/bin/wrs` byte-identical to
  the skill copy. No `__pycache__` left in the repository.
- Stopped before commit, push, and bootstrap sync (user approval required).

## Third round (2026-09-24): vault backends and spinner

- `wrs` 2.2.0 (SHA-256 9e83f2c8d62fdcb77b44cebf5a6596864bbe24aac41fb99fb833bc7983305d68),
  installed; 2.1.0 kept as `~/.local/bin/wrs.previous`.
- Backends: Bitwarden (`bw`) and 1Password (`op`). Selection: `--password-manager`,
  `WRS_PASSWORD_MANAGER`, `password_manager` config key, `op://` item, installed
  CLI (Bitwarden first). Mirrors the recovery toolkit's source selection
  (bitwarden, 1password, command, prompt); command and prompt sources not
  carried over because the gate must create and rotate the item.
- 1Password commands from primary docs (1password.dev CLI reference): item
  create from a JSON template on stdin (`-`), item edit `--template /dev/stdin`,
  item get `--format json` and `--otp`, `whoami`, `signin` (export lines parsed
  for `OP_SESSION*`), `signout`. Docs warn that assignment arguments expose
  values to other processes; none are used.
- Spinner draws its first frame immediately; wraps session check, unlock, sync,
  item read, TOTP fetch, and key create or rotate; cleared before every prompt
  (verified in PTY transcripts).
- Tests (simulated `op`, `bw`, `secret-tool`; PTY driver): 1Password manual
  sign-in first key; cached key opens with zero `op` calls; expired key in app
  mode rotates with fresh approval and TOTP, OTP field preserved; wrong TOTP,
  denied approval, wrong password rejected; key never in any argv. Bitwarden
  first key, forced rotation with TOTP, create/edit argv carry no item body.
  Flag and env override, unknown manager exits 2, cached key from another
  manager ignored, non-TTY output has no animation escapes. `serve --dev` on the
  scratch project (port base 44290) served restricted with HTTP 200.
- Real tools read-only: `wrs key status` reads the user's own Bitwarden dev key
  (created by the user's own `serve --dev` run) under 2.2 without re-unlock.
  The user's running msngi server was not touched.
- Limitation: the 1Password backend is verified against a simulator built from
  the documentation; no `op` binary or account exists on this host.
- `tools/validate-all.sh`: PASS. Install reference, example, evals (case 4)
  updated and read in full.

## Fourth round (2026-09-24): TOTP removed, commit

- User correction: TOTP was agreed off on 2026-09-23 (vault two-step login is
  the second factor) and was reintroduced in the gate design without asking.
  Removed from code (item TOTP detection, code prompt, comparison, `hmac`
  import), reference, and tests; recorded in memory (wrs-dev-gate) in the
  skills repo, the msngi repo, and the global store.
- Retest (simulated CLIs, PTY): Bitwarden and 1Password rotation with a TOTP
  seed or OTP field on the item completes with no code prompt; call logs show
  no TOTP fetch; wrong password still rejected.
- Documentation skill step 9.3 now routes gated instances to `wrs serve --dev`
  with the sign-in left to the user.
- Installed mirrors (`~/.claude`, `~/.codex`, `~/.gemini`, `~/.copilot`) hold
  the committed documentation skill of 8603dde, identical in content to HEAD
  12df7f0; they receive this round only after push and bootstrap.
- `wrs` SHA-256 30f4c2694ffc443eb57ba10097f47563bbfab4816d11ddc26806b75710c363f7,
  installed; validator PASS; changed SKILL.md and reference read in full.
- All wrs servers stopped at the user's request.

## Publication (2026-09-24)

- User instruction "fix, amend push": the single commit was amended to carry
  this record and pushed to `origin/main`. Bootstrap sync was not part of the
  instruction; installed mirrors keep the previous skills until it runs.

## Bootstrap sync (2026-09-24)

- Host scripts for Claude Code, Codex, Gemini, and Copilot run from the source
  checkout at `16a3084`; all exited 0.
- Each mirror is at `16a3084` with no local changes; `documentation/` matches
  `origin/main` and ships `wrs` SHA-256 prefix 30f4c2694ffc.
- Each instruction file holds one marker block and is byte-identical to its
  pre-sync copy (shared rules unchanged). Codex `.system/` and the five
  Antigravity builtin skills remain; `~/.gemini/config/skills.json` and its
  symlink point at `~/.gemini/skills`. No WSL host; no root `AGENTS.md` to
  prune. Hook and MCP registration were outside the request.

## Fifth round (2026-09-24): referencing rule in AGENTS.md

- Section 8 item 3 names external deliverables (proposals, correspondence,
  filed records) for the title-only rule; new item 4 requires relative links
  inside a documentation library and forbids referencing a higher-sensitivity
  topic. The 9.6 identifier bullet, duplicated by 8.2, was removed at the
  user's choice to stay under 1,500 words (1,498).
- The commit was amended and pushed with a lease on the previous tip, on the
  user's instruction to amend and push.
- Bootstrap after the push: all four hosts at `537114d`; each instruction
  file holds one block equal to the new `AGENTS.md`, text outside the block
  byte-identical to the pre-sync copy; Codex `.system/` and the five
  Antigravity builtin skills intact.
