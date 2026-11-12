# Walkthrough: Coordinator Thresholds, 25-Skill Audit, Graphify Migration, and AGENTS.md + Per-Host Hook Elevation

## Summary of Changes

1. **Elevated Universal Agent Rules (`AGENTS.md`)**:
   - Reworked `§1. General commands`, `§2. Working with skills`, `§3. Universal non-code full-read mandate`, and `§12. Pre-completion checklist` in `/mnt/data/workspace/skills/AGENTS.md` (`1,482` words, strictly below the 1,500-word cap in `skill-authoring-standard.md`).
   - Added explicit **Binding Authority** and **Compliance Over Output** mandates stating that skipping, weakening, or routing around any rule or skill step is a complete task failure and causes severe user disappointment regardless of deliverable quality or speed.
   - Added **No Unilateral Overrides** and the **Viable Alternative Consultation Rule**: agents must obey global rules and skills even when inconvenient, slow, token-intensive, or contrary to their training or judgment; if an agent genuinely believes a superior or viable alternative exists, it must STOP, present the alternative in chat, and wait for explicit user approval before deviating.
   - Added **Mandatory Full-File Retrieval**: agents must open and manually read the actual canonical instruction file and full `SKILL.md` (plus routed `references/` and `examples/`) from disk before acting, and must never rely on platform skill-loader summaries, injected excerpts, truncated previews, or grep snippets.
   - Added **Consult the Skill Before Claiming Completion**: agents must reopen and verify the governing `SKILL.md` and pre-completion checklist against the final deliverable before declaring a task done.

2. **Per-Host Forceful Compliance Hooks (`bootstrap/`)**:
   - Created and updated five host-tailored enforcement scripts under `/mnt/data/workspace/skills/bootstrap/scripts/`:
     - `enforce-claude-rules.sh` (`UserPromptSubmit` in `~/.claude/settings.json`, naming `CLAUDE.md` and `AGENTS.md`)
     - `enforce-gemini-rules.sh` (`PreInvocation` in `~/.gemini/config/hooks.json` for Gemini Antigravity, naming `GEMINI.md` and `AGENTS.md`)
     - `enforce-gemini-cli-rules.sh` (`SessionStart` in `~/.gemini/settings.json` for Gemini CLI, naming `GEMINI.md` and `AGENTS.md`)
     - `enforce-codex-rules.sh` (`SessionStart` in `~/.codex/hooks.json` for Codex CLI/Desktop, naming `AGENTS.md`)
     - `enforce-copilot-rules.sh` (`sessionStart` in `~/.copilot/hooks/bootstrap.json` for GitHub Copilot CLI, naming `copilot-instructions.md` and `AGENTS.md`)
   - Updated `bootstrap/scripts/lib.sh` so `align_agent_rules` automatically preserves and ensures the `<!-- graphify -->` always-on block whenever `graphify` is installed.
   - Updated `bootstrap/SKILL.md` and `bootstrap/references/hook-registration.md` to document all five per-host enforcement hooks.

3. **Live Workstation Propagation & Verification**:
   - Synced the elevated `AGENTS.md` and `bootstrap/` scripts into `~/.gemini/skills/`, `~/.claude/skills/`, `~/.codex/skills/`, and `~/.copilot/skills/`.
   - Aligned `~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and `~/.copilot/copilot-instructions.md` with `/mnt/data/workspace/skills/AGENTS.md` and verified the `<!-- graphify -->` mandate block in each.
   - Verified all five `enforce-*.sh` scripts execute cleanly with exit code `0` and valid JSON/text output, and verified all host JSON hook configs (`~/.gemini/config/hooks.json`, `~/.gemini/settings.json`, `~/.claude/settings.json`, `~/.codex/hooks.json`, `~/.copilot/hooks/bootstrap.json`).
