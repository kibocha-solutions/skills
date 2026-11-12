# Implementation Plan: Coordinator Thresholds, Full 25-Skill Audit & Remediation, Graphify Migration, and AGENTS.md + Multi-Host Hook Elevation

## Goal
1. Update `coordinator` skill (`SKILL.md`, `references/delegation.md`, `evals/evals.json`) to raise usage pause thresholds to **95% for the 5-hour window** (5% remaining) and **98% for the weekly window** (2% remaining), and remove hard usage percentage thresholds from `/mnt/data/workspace/skills/AGENTS.md` so thresholds live solely in `coordinator`.
2. Audit all 25 repository skills against `/mnt/data/workspace/skills/skill-creator/SKILL.md` and `skill-creator/references/skill-authoring-standard.md`, and remediate every violation across all 25 skills.
3. Replace `codegraphcontext` and `code-review-graph` on this workstation with `graphifyy` (`graphify` CLI + `graphify-mcp`), update `/mnt/data/workspace/skills/graphify/` and `/mnt/data/workspace/skills/bootstrap/`, configure MCP servers, hooks, and always-on rules across Antigravity, Claude Code, Codex, Gemini CLI, and GitHub Copilot so agents automatically invoke `graphify` and cannot bypass it, and build `graphify-out/graph.json` for this workspace.
4. Elevate `/mnt/data/workspace/skills/AGENTS.md` and the per-host enforcement hooks (`bootstrap/scripts/enforce-*.sh`, `bootstrap/SKILL.md`, `bootstrap/references/hook-registration.md`, and live workstation hooks/mirrors) so autonomous agents are forcefully stopped and required to:
   - Obey their governing instruction file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md`) and every applicable skill even when inconvenient, slow, token-consuming, or contrary to the agent's own training or judgment.
   - Consult the user and obtain explicit permission before deviating whenever the agent believes a viable or superior alternative exists.
   - Manually open and read the actual canonical instruction file and full `SKILL.md` (plus required `references/` and `examples/`) from disk before acting — never relying on platform skill-loader summaries, excerpts, or grep searches.
   - Re-open and consult the governing `SKILL.md` and pre-completion checklist before claiming any task is complete.
   - Recognize that disregarding these mandates or bypassing required skill reads is equivalent to failing the task outright in terms of user disappointment, regardless of output quality.

## Planned Slices
1. **Slice 1 (Completed)**: `AGENTS.md` threshold removal and `coordinator` 95% 5h / 98% weekly threshold update.
2. **Slice 2 (Completed)**: Full 25-skill `skill-creator` compliance remediation (`evals/evals.json`, `examples/`, `references/`, step-by-step `SKILL.md`).
3. **Slice 3 (Completed)**: Workstation uninstallation of `codegraphcontext` and `code-review-graph`, installation of `graphifyy` (`0.9.108`), rewrite of `graphify/` skill and `bootstrap/`, live MCP + hook + always-on rule configuration, and workspace graph generation (`graphify-out/graph.json`).
4. **Slice 4 (In Progress)**:
   - Elevate `/mnt/data/workspace/skills/AGENTS.md` (`§1`, `§2`, `§3`, `§12`) for ironclad authority, mandatory pre-task full manual `SKILL.md` reads (forbidding platform loader summaries), mandatory user consultation on viable alternatives, mandatory pre-completion `SKILL.md` re-read, and explicit task-failure accountability, while preserving all rules in `§4–§12` and keeping total length `< 1,500` words.
   - Upgrade `bootstrap/scripts/enforce-claude-rules.sh` and `bootstrap/scripts/enforce-gemini-rules.sh`, and add `bootstrap/scripts/enforce-codex-rules.sh` and `bootstrap/scripts/enforce-copilot-rules.sh` so each agent host receives a forceful, host-specific enforcement notice naming its instruction file (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `copilot-instructions.md`).
   - Update `bootstrap/SKILL.md` and `bootstrap/references/hook-registration.md` to document all four per-host enforcement hooks.
   - Propagate the updated `AGENTS.md` and `enforce-*.sh` hooks to this workstation's live host configs (`~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`, `~/.gemini/config/hooks.json`, `~/.claude/settings.json`, `~/.codex/hooks.json`, `~/.copilot/hooks/bootstrap.json`, and local `~/.*/skills/bootstrap/scripts/` checkouts).
   - Verify all modified files, word counts, JSON/TOML syntax, hook execution outputs, and skill audits.
