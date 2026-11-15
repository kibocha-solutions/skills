# Implementation Plan: Non-Blocking Writerside Serve Wrapper and Bootstrap Deployment

## Objective
Update the Writerside (`wrs`) CLI tool so that `wrs serve` operates non-blocking by default. Once the server container starts, passes its HTTP health checks, and displays the served instance URLs, control returns immediately to the calling shell with exit code 0 so additional commands can execute in the same terminal. After validating this behavior locally with live smoke tests, propagate the updated script template in `documentation/scripts/wrs` (and nothing else) across `/mnt/data/workspace/skills`, commit and push per `ci-cd/SKILL.md`, and deploy via `/bootstrap` host synchronization scripts across all configured agent host mirrors.

## Acceptance Criteria
1. `wrs serve` starts the documentation server container, verifies health endpoints, prints the served instances table and hint lines, and exits immediately with code 0 without blocking the terminal.
2. An optional `-f` / `--follow` flag is supported to allow interactive log streaming and foreground lifecycle management when explicitly requested.
3. The existing `-b` / `--background` flag remains supported without error (functioning as default non-blocking).
4. Running `wrs status` after `wrs serve` confirms the server container is actively running and reports the live instance URLs.
5. Running `wrs stop` cleanly terminates and removes the running server container.
6. Only `documentation/scripts/wrs` in `/mnt/data/workspace/skills` is modified; no other documentation files, templates, or skills are altered.
7. Changes are committed and pushed to `origin/main` in `/mnt/data/workspace/skills` adhering to `ci-cd/SKILL.md` (atomic commit, new reader perspective, no AI attribution).
8. `bootstrap` propagation scripts (`ensure-claude-link.sh`, `ensure-codex-link.sh`, `ensure-gemini-link.sh`, `ensure-copilot-link.sh`) run and verify synchronization of managed skills across installed hosts.

## Proposed Changes
- `~/.local/bin/wrs` [MODIFY]: Update `cmd_serve` and argparse definition to run non-blocking by default with `--follow` option.
- `/mnt/data/workspace/skills/documentation/scripts/wrs` [MODIFY]: Apply the identical tested non-blocking changes to the canonical script in the skills repository.

## Verification Method
- Execute `wrs serve` in `msngi` project: verify that the command exits 0, the shell prompt returns immediately, and other shell commands can run.
- Execute `wrs status`: confirm server is running and instances are reachable via curl.
- Execute `wrs stop`: confirm server container is stopped.
- Run git diff in `skills`: confirm only `documentation/scripts/wrs` has diffs.
- Execute bootstrap synchronization scripts and verify zero drift.
