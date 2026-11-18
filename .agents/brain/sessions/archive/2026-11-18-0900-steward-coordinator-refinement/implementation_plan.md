# Implementation Plan: Steward, Coordinator, Maestro, CI/CD, and AGENTS.md Refinement

## Objective
Refine `steward`, `maestro`, `coordinator`, `ci-cd`, `bootstrap`, and `AGENTS.md` to add persistent per-repository approval tracking (`ask`, `true`, `false`), fix `steward.py stop` and `system-profile.sh` hook output/presentation/auto-remediation across hosts, make `coordinator` assume the user's mantle with a worker registry (`.agents/brain/workers.json`), worker escalation rules, and a graduating algorithmic wake timer (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`), and require `maestro` orientation to map the project via `graphify` (or docs/configs) and read global rules and applicable skills before creating or resuming a session.

## Acceptance Criteria
1. `AGENTS.md` integrates `approval_mode` (`ask`, `true`, `false`) and coordinator worker-registry/graduating-wake references while remaining strictly below 2,500 words and preserving `§1` through `§14` numbering.
2. `steward/scripts/steward.py` implements `approval [get|set <ask|true|false>|list]` (persisting to `<repo>/.agents/brain/approvals.json` and `~/.agents/steward/approvals.tsv`), `check [--fix]`, and `auto_clean`, and fixes `stop` across Antigravity, Copilot, Claude Code, and Codex to emit valid `{}` when allowing stop, respect `continuationActive`, `terminationReason`, and `fullyIdle`, and avoid noisy loops.
3. `steward/scripts/system-profile.sh` and `bootstrap/scripts/enforce-gemini-rules.sh` emit host-compatible JSON payloads when invoked as lifecycle hooks.
4. `maestro/scripts/sessions.py` implements `approval [get|set <ask|true|false>]`, shows `approval_mode` in `status`, and respects `approval_mode == "true"` in `wake_verdict`; `maestro/SKILL.md` Section 1 requires global rules, project mapping (`graphify` or docs/configs), and applicable skill reads before session creation/resumption.
5. `coordinator` (`SKILL.md`, `references/`, `assets/`, `examples/`, `evals/`) mandates `.agents/brain/workers.json`, worker escalation rules, four-tier decision resolution before escalating, avoiding user go-ahead prompts, and the graduating algorithmic wake timer (`1m -> 3m -> 5m -> 12m -> 15m -> 30m`, resetting to `1m` on action, `90m-120m` when waiting on user action, and stopped on completion).
6. `ci-cd` (`SKILL.md`, `references/git-and-history.md`, `evals/evals.json`) honors `approval_mode` (`true` auto-stages/commits/cleans all repo changes; `ask` isolates out-of-scope and major rewrites; `false` requires approval per action).
7. `quick_validate.py` passes on `steward`, `maestro`, `coordinator`, `ci-cd`, and `bootstrap`; `tools/validate-all.sh` passes with zero errors in `AGENTS.md` and all modified skills; `steward.py check` is clean; `graphify update .` succeeds.

## Proposed Changes
- `[MODIFY] AGENTS.md`
- `[MODIFY] steward/scripts/steward.py`
- `[MODIFY] steward/scripts/system-profile.sh`
- `[MODIFY] steward/SKILL.md`, `steward/references/decision-rules.md`, `steward/examples/good-vs-bad-stewardship.md`, `steward/evals/evals.json`
- `[MODIFY] bootstrap/scripts/enforce-gemini-rules.sh`, `bootstrap/references/hook-registration.md`
- `[MODIFY] maestro/scripts/sessions.py`, `maestro/SKILL.md`, `maestro/references/brain-conventions.md`, `maestro/references/session-lifecycle.md`, `maestro/references/goal-protocol.md`, `maestro/evals/evals.json`
- `[MODIFY] coordinator/SKILL.md`, `coordinator/references/delegation.md`, `coordinator/references/task-ids.md`, `coordinator/references/contracts.md`, `coordinator/references/heartbeat-and-wake.md`, `coordinator/assets/heartbeat-prompts.md`, `coordinator/examples/coordination.md`, `coordinator/evals/evals.json`
- `[MODIFY] ci-cd/SKILL.md`, `ci-cd/references/git-and-history.md`, `ci-cd/evals/evals.json`

## Temporary Artifacts
- None expected inside the workspace; any temporary test directories will be created via `steward.py store path scratch` or deleted immediately after test assertions pass.

## Verification Plan
- Unit/CLI tests for `steward.py` (`approval`, `check --fix`, `stop` payloads for Antigravity/Copilot/Claude/Codex), `sessions.py` (`approval`, `status`, `wake-check`), `system-profile.sh` (CLI and hook stdin JSON), and `enforce-gemini-rules.sh`.
- `python3 skill-creator/scripts/quick_validate.py` on `steward`, `maestro`, `coordinator`, `ci-cd`, and `bootstrap`.
- `bash tools/validate-all.sh`, `wc -w AGENTS.md`, `graphify update .`, and `python3 steward/scripts/steward.py check`.
