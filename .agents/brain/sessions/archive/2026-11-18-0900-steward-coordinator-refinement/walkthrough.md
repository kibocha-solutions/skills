# Walkthrough: Steward, Coordinator, Maestro, CI/CD, and AGENTS.md Refinement

Refined `steward`, `maestro`, `coordinator`, `ci-cd`, `bootstrap`, and `AGENTS.md` to support persistent per-repository approval modes (`ask`, `true`, `false`), silent/JSON-compliant host-aware `stop` and `SessionStart` hooks with auto-cleanup, thorough `maestro` pre-session project orientation, coordinator assumption of the user's mantle with `.agents/brain/workers.json` and Worker Rules, and the graduating algorithmic wake timer (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`).

## 2026-11-18 09:16
- Cut branch `checkpoint/steward-coordinator-refinement` from `main` (`a75c3e1e`), archived stale `repo-health.json` to `.agents/brain/git/archives/2026-11-13-0213-repo-health.json`, refreshed `.agents/brain/git/repo-health.json`, and appended the branch to `.agents/brain/git/branch-ancestry.json`.
- Baseline checks before edits: `AGENTS.md` was 2,470 words; `tools/validate-all.sh` had 14 pre-existing errors in unchanged `ci-cd` and `communications` files; `steward.py check` reported clean.

## 2026-11-18 09:30
- `AGENTS.md` updated to 2,488 words (strictly below the 2,500-word limit, §§1-14 numbering preserved).
- `steward/scripts/steward.py` now implements `approval [get|set <ask|true|false>|list]`, `auto_clean`, `check [--fix]`, valid `{}` exit output for Antigravity/Copilot, and loop/cancel guards (`continuationActive`, `terminationReason`, `fullyIdle`, `stop_hook_active`).
- `steward/scripts/system-profile.sh` and `bootstrap/scripts/enforce-gemini-rules.sh` emit host-compatible `systemMessage` JSON payloads when invoked as hooks.
- `maestro/scripts/sessions.py` implements `approval [get|set]`, prints `approval_mode` in `status`, and respects `approval_mode=true` in `wake_verdict`; `maestro/SKILL.md` mandates reading global rules, mapping via `graphify` or docs/configs, and reading applicable skills before forming or resuming any Maestro session.
- `coordinator` mandates `.agents/brain/workers.json`, four-tier decision lookup before escalating, mandatory Worker Rules, exact worker pointer on user-gated approvals, graduating algorithmic wake timer (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`), `90m-120m` user-blocked wake timer, and cancelling all wake timers on completion.
- `ci-cd` applies `approval_mode` (`true` auto-stages/commits/cleans all repo changes; `ask` isolates out-of-scope and major rewrites; `false` requires per-action approval).
- Verification: isolated functional test suite (`task-242`) passed all assertions (`steward.py`, `sessions.py`, `system-profile.sh`, `enforce-gemini-rules.sh`); `/usr/bin/python3 skill-creator/scripts/quick_validate.py` returned `Skill is valid!` on `steward`, `maestro`, `coordinator`, `ci-cd`, and `bootstrap`; `tools/validate-all.sh` reported zero errors in `AGENTS.md` and all modified skills (only the 14 baseline errors in unchanged files); `graphify update .` updated `graphify-out` (822 nodes, 2,011 edges, 54 communities); `steward.py check` reported clean.
