# Tasks: Multi-Agent Bootstrap Alignment, MCP Standardization & Rule Enforcement

State: IN_PROGRESS

## Phase 1: Cleanups & Script Alignment
- [x] Implement host `AGENTS.md` cleanup helper in `bootstrap/scripts/lib.sh`
- [x] Refactor `bootstrap/scripts/ensure-gemini-link.sh` for unified Gemini CLI & Antigravity support
- [x] Forward `ensure-gemini-builtin-skills.sh` to `ensure-gemini-link.sh`
- [x] Update `ensure-claude-link.sh` and `ensure-copilot-link.sh` to prune redundant `AGENTS.md`

## Phase 2: MCP Server Standardization
- [x] Install global binaries for `codegraphcontext` (`cgc`) and `code-review-graph` via `uv tool install`
- [x] Standardize Copilot MCP configuration in `~/.copilot/mcp-config.json` (correct `cwd` and command)
- [x] Standardize Gemini Antigravity MCP configuration in `~/.gemini/config/mcp_config.json`
- [x] Standardize Claude Code MCP configuration in `~/.claude/settings.json` / `~/.claude.json`
- [x] Add MCP entries to Codex in `~/.codex/config.toml`

## Phase 3: Rule Compliance Enforcement Hooks
- [x] Implement Claude Code `UserPromptSubmit` / `SessionStart` compliance hook in `~/.claude/settings.json`
- [x] Implement Gemini Antigravity `PreInvocation` compliance hook in `~/.gemini/config/hooks.json`
- [x] Implement Codex CLI `SessionStart` compliance hook in `~/.codex/hooks.json`
- [x] Implement GitHub Copilot `sessionStart` compliance hook in `~/.copilot/hooks/bootstrap.json`
- [x] Verify hook execution and non-interference with normal agent tools

## Phase 4: Documentation, Skill Governance & Memory
- [x] Update `bootstrap/SKILL.md` following `/skill-creator` authoring standards
- [x] Rewrite `bootstrap/references/hook-registration.md` as cross-OS portability reference
- [x] Update `.agents/memory/skills-repo-deployment-workflow.md`

## Phase 5: Verification & Propagation
- [x] Test execution of all `ensure-*-link.sh` scripts and hook validation
- [x] Verify host rule files (`GEMINI.md`, `CLAUDE.md`, `copilot-instructions.md`, `AGENTS.md`)
- [/] Await user signing & remote resolution to create `/ci-cd` compliant commit
- [ ] Propagate via `/bootstrap`

