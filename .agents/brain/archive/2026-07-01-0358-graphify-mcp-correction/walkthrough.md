# Walkthrough — graphify MCP correction

## Context

User pointed to Graphify public docs and then supplied local `graphify --help` output. The installed `graphifyy` CLI exposes commands such as `install`, `extract`, `update`, `query`, `path`, and `explain`, but does not expose `graphify serve`, `graphify ping`, or a documented `--mcp` flag.

## Changes

- `graphify/SKILL.md`: changed the model from two local MCP servers to one standalone `code-review-graph` MCP server plus Graphify CLI/skill integration. Replaced `graphify ping` and pseudo-MCP examples with `graphify --version` / `graphify --help` and CLI query examples.
- `graphify/references/recovery-runbook.md`: removed global `graphify serve` registration guidance, removed assumed project-scoped `--mcp` guidance, and added warnings to verify local CLI help before assuming Graphify MCP support.
- `graphify/assets/mcp-config-template.json`: rewrote the template to register only `code-review-graph serve` as MCP, with Graphify install/query commands documented separately.

## Verification

- `python3 -m json.tool graphify/assets/mcp-config-template.json`: passed.
- `git diff --check`: passed.
- Targeted search confirms no positive Graphify MCP registration remains (`[mcp_servers.graphify]`, `claude mcp add graphify`, `command = "graphify"`, `graphify ping`, and `search_multimodal_graph` are absent). Remaining `graphify serve` / `--mcp` mentions are negative warnings only.

## Remaining

Run CI/CD preflight, amend current commit with preserved message/signing, and force-push with lease.

## Git Delivery

- CI/CD preflight used the existing repo-health cache for `main`.
- Verified user identity and SSH signing config.
- Restarted/checked the WSL SSH signing relay; `ssh-add -l` listed `SshSigningKey`.
- Staged only the three graphify files.
- `git diff --cached --check`: passed.
- Amended current commit with `git commit --amend --no-edit`; commit message preserved.
- New commit: `3f772c373e009e19bc781e14a0c4183aaf35d522`.
- Commit object contains an SSH `gpgsig` block.
- Force-pushed with lease: `2d9d0c6...3f772c3 main -> main (forced update)`.
- Final status: `main` aligned with `origin/main`; worktree clean.
