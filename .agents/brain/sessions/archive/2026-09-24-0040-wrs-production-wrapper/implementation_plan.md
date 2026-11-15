# Plan: Production wrs Writerside Wrapper

## Objective

Replace the single-instance Bash `wrs` wrapper with a team-grade tool that
builds every Writerside instance, serves all of them at once with
sensitivity-aware cross-instance routing, and presents live progress and
clear results; then ship it in the `documentation` skill with the current
builder image and Podman support.

## Requirements (user, 2026-09-24)

1. Build all trees in one command.
2. Serve all trees at once, each exposed appropriately.
3. A reference to a page that lives in another tree maps cleanly to that
   tree and opens it.
4. By default a lower-permission tree does not reach a higher-permission
   tree.
5. Modern UX: live spinner while working, clear status and summaries.
6. Fix the nginx 403 (serve pointed at a folder holding only the zip).
7. Test, including in the browser.
8. Update skills (bootstrap, documentation, skill-creator procedures):
   latest builder image, Podman support, ship the new wrapper.

## Research record

- Latest builder tag `2026.08.0328` (Docker Hub API, 2026-09-24; digest
  `sha256:122f6b1d...533a`, matches local image). amd64 only.
- Builder env vars (JetBrains "Build with Docker"): `SOURCE_DIR`,
  `MODULE_INSTANCE`, `OUTPUT_DIR`, `RUNNER`, `PDF`, `IS_GROUP`.
- Build groups (`cfg/build-groups.xml`, `IS_GROUP=true`) merge instances into
  one site under path prefixes: rejected as the default because it removes
  the sensitivity boundary between instances.
- CLI conventions from clig.dev: output within 100 ms, spinner only on TTY,
  `NO_COLOR`/`TERM=dumb`/`--no-color`, data on stdout and diagnostics on
  stderr, `--json`, suggested next commands, Ctrl-C cleanup, config
  precedence flags > env > project config > user config.
- `report.json` carries `testsErrorsCount`, `testsWarningsCount`,
  `testsTotal`, `testsErrors`.

## Design

- Language: Python 3.11+ standard library only (single executable file).
- Commands: `doctor`, `build`, `serve`, `status`, `stop`, `open`, `logs`,
  `clean`, `update`, `version`.
- Build: default all instances; `--jobs`; source copy excluding `output/`
  and `.idea/`; success from `report.json` plus the completion log line;
  unpack the web ZIP atomically into `site/<instance>/`.
- Serve: one nginx container, one port per instance (base 8000 + rank),
  generated config; `try_files`; cross-instance pages redirect to the owning
  instance when it is equal or lower sensitivity, and return a 403 page when
  it is higher unless `--allow-upward`; a portal page lists instances.
  Loopback bind by default; `--lan` exposes public and internal only.
- Sensitivity order: public < internal < restricted < confidential;
  overridable in `.wrs.toml`; unknown instances rank highest.
- Config: flags > `WRS_*` env > `.wrs.toml` beside `writerside.cfg` >
  defaults.

## Acceptance criteria

1. `wrs build` builds all four msngi instances; summary shows per-instance
   status, checks, pages, duration, log path; exit 0.
2. A failing instance gives a non-zero exit and names the failed checks.
3. `wrs serve` starts all instances; each URL returns 200 for its start page.
4. Cross-instance: a restricted-only page requested on the internal port is
   refused (403 page); an internal page requested on the restricted port is
   served; a page unique to a lower tree requested on a higher tree
   redirects.
5. Spinner animates on TTY; plain output when piped or `NO_COLOR` is set.
6. Browser check: portal, instance pages, redirect, and refusal render.
7. `wrs stop`, `status`, `clean` behave and leave no stray containers.
8. Skills updated: image tag, Podman, wrapper shipped; validator shows no new
   errors; skill files read in full.
9. No commit, push, or bootstrap propagation without user approval.

## Proposed changes

- [NEW] `documentation/scripts/wrs`
- [MODIFY] `documentation/references/install-writerside.md`
- [MODIFY] other skill files that pin the old image tag (to locate)
- [MODIFY] `~/.local/bin/wrs` (backup kept as `wrs.bash-backup`)
