# Session Tasks: Coordinator, 25-Skill Audit, Graphify Migration, and AGENTS.md + Hook Elevation

- Session ID: `2026-11-12-2258-coordinator-graphify-skill-audit`
- State: `DONE`

## Checklist
- [x] Read governing skills (`skill-creator`, `coordinator`, `graphify`, `maestro`, `documentation`, `system-init`, `bootstrap`, `legalese`) in full.
- [x] Update `coordinator` thresholds to 95% 5-hour / 98% weekly and remove percentage thresholds from `AGENTS.md`.
- [x] Audit and remediate all 25 skills against `skill-creator/SKILL.md` and `skill-creator/references/skill-authoring-standard.md`.
- [x] Remove `codegraphcontext` and `code-review-graph` on this workstation and install `graphifyy` (`0.9.108`) with MCP, watch, Leiden, PDF, Office, and SVG extras.
- [x] Rewrite `graphify/` skill (`SKILL.md`, `references/`, `examples/`, `evals/evals.json`) and update `bootstrap/` for `graphify`.
- [x] Configure `graphify` MCP servers, hooks, and always-on rules across Antigravity, Claude Code, Codex, Gemini CLI, and GitHub Copilot, and build `/mnt/data/workspace/skills/graphify-out/graph.json`.
- [x] Elevate `/mnt/data/workspace/skills/AGENTS.md` (`§1`, `§2`, `§3`, `§12`) with non-optional compliance commands, mandatory full manual `SKILL.md` file reads (forbidding platform loader summaries), mandatory user consultation on viable alternatives, mandatory pre-completion `SKILL.md` re-reads, and `<1,500`-word compliance (`1,482` words).
- [x] Elevate `bootstrap/scripts/enforce-claude-rules.sh` and `bootstrap/scripts/enforce-gemini-rules.sh`, add `bootstrap/scripts/enforce-gemini-cli-rules.sh`, `bootstrap/scripts/enforce-codex-rules.sh`, and `bootstrap/scripts/enforce-copilot-rules.sh`, and update `bootstrap/SKILL.md` and `bootstrap/references/hook-registration.md`.
- [x] Propagate the elevated `AGENTS.md` rules and per-host `enforce-*.sh` scripts to live workstation configs (`~/.gemini/`, `~/.claude/`, `~/.codex/`, `~/.copilot/`).
- [x] Re-read all modified non-code files in full and run programmatic verification checks.
