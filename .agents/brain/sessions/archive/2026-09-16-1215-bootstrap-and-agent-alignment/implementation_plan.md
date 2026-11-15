# Implementation Plan: Multi-Agent Bootstrap Alignment, MCP Standardization & Rule Enforcement

## Objective
Unify agent alignment across Gemini (Antigravity and CLI), Claude Code, Codex, and GitHub Copilot. Fix Antigravity skill discovery, prune redundant host-level rule files, standardize MCP server loading (`code-review-graph` and `codegraphcontext`), deploy deterministic enforcement hooks across all four agents, and document hook creation standards in `bootstrap` for cross-OS portability.

## Acceptance Criteria
1. Gemini Antigravity discovers user skills via `~/.gemini/skills/` and `~/.gemini/config/skills.json`; `~/.gemini/antigravity/builtin/` is left clean and untouched.
2. Extraneous `AGENTS.md` files at the root of host directories (`~/.gemini/`, `~/.claude/`, `~/.copilot/`) are removed on propagation, keeping only host-canonical instruction files (`GEMINI.md`, `CLAUDE.md`, `copilot-instructions.md`). Only Codex retains `AGENTS.md`.
3. `bootstrap/scripts/ensure-gemini-link.sh` handles both Gemini CLI and Antigravity; `ensure-gemini-builtin-skills.sh` is deprecated and redirects to `ensure-gemini-link.sh`.
4. `code-review-graph` and `codegraphcontext` MCP configurations are standardized with valid commands and working directories across Claude, Codex, Copilot, and Gemini.
5. Deterministic hooks are registered to reinforce mandatory skill/rule compliance across Claude Code (`UserPromptSubmit`, `SessionStart`), Gemini Antigravity (`PreInvocation`), Codex (`SessionStart`), and Copilot (`sessionStart`).
6. `bootstrap/SKILL.md` and `bootstrap/references/hook-registration.md` are updated conforming strictly to `/skill-creator` and `/documentation` authoring standards.
7. Single git commit conforming to `/ci-cd` guidelines.

## Proposed Changes
### Components & Files
* `[MODIFY]` `bootstrap/scripts/lib.sh`: Add logic to prune redundant host `AGENTS.md` when native instruction file is different.
* `[MODIFY]` `bootstrap/scripts/ensure-gemini-link.sh`: Support Gemini Antigravity and CLI; sync `~/.gemini/skills/`, align `~/.gemini/GEMINI.md`, update `config/skills.json`.
* `[MODIFY]` `bootstrap/scripts/ensure-gemini-builtin-skills.sh`: Deprecate and forward to `ensure-gemini-link.sh`.
* `[MODIFY]` `bootstrap/scripts/ensure-claude-link.sh`: Add cleanup of `~/.claude/AGENTS.md`.
* `[MODIFY]` `bootstrap/scripts/ensure-copilot-link.sh`: Add cleanup of `~/.copilot/AGENTS.md`.
* `[MODIFY]` `bootstrap/SKILL.md`: Update target tables, remove `builtin/` mutation rules, document Antigravity setup, add hook/MCP standards.
* `[MODIFY]` `bootstrap/references/hook-registration.md`: Document hook standards and templates across all 4 agents.
* `[MODIFY]` `.agents/memory/skills-repo-deployment-workflow.md`: Update architecture documentation.

## Verification Method
1. Run all 4 `ensure-*-link.sh` scripts and verify exit code 0 and idempotence.
2. Confirm host directories:
   - `~/.gemini/`: only `GEMINI.md` exists.
   - `~/.claude/`: only `CLAUDE.md` exists.
   - `~/.copilot/`: only `copilot-instructions.md` exists.
   - `~/.codex/`: `AGENTS.md` exists.
3. Verify MCP configurations parse and point to valid paths/executables.
4. Verify hooks fire and inject compliance directives across agents.
5. Verify `git status` in `/mnt/data/workspace/skills` is clean and commit message meets `/ci-cd` limits.
