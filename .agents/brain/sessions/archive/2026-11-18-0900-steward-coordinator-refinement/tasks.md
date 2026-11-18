# Tasks: Steward, Coordinator, Maestro, CI/CD, and AGENTS.md Refinement
## State: DONE (Refined steward, maestro, coordinator, ci-cd, bootstrap hooks, and AGENTS.md)
## Phase 1: Baseline & Governance
- [x] Cut checkpoint branch `checkpoint/steward-coordinator-refinement`, update `branch-ancestry.json` and `repo-health.json`, and initialize active Maestro session
- [x] Update `AGENTS.md` with `approval_mode` and coordinator worker-registry/graduating-wake references under 2,500 words

## Phase 2: Steward & Bootstrap Hook Fixes
- [x] Update `steward/scripts/steward.py` (`approval` command, `auto_clean`, `check --fix`, fixed host-aware `stop` hook)
- [x] Update `steward/scripts/system-profile.sh`, `bootstrap/scripts/enforce-gemini-rules.sh`, and `bootstrap/references/hook-registration.md`
- [x] Update `steward/SKILL.md`, `steward/references/decision-rules.md`, `steward/examples/good-vs-bad-stewardship.md`, and `steward/evals/evals.json`

## Phase 3: Maestro, Coordinator, and CI/CD Updates
- [x] Update `maestro/scripts/sessions.py`, `maestro/SKILL.md`, `maestro/references/`, and `maestro/evals/evals.json`
- [x] Update `coordinator/SKILL.md`, `coordinator/references/`, `coordinator/assets/heartbeat-prompts.md`, `coordinator/examples/coordination.md`, and `coordinator/evals/evals.json`
- [x] Update `ci-cd/SKILL.md`, `ci-cd/references/git-and-history.md`, and `ci-cd/evals/evals.json`

## Phase 4: Verification & Handoff
- [x] Run functional CLI and hook payload tests for `steward.py`, `sessions.py`, `system-profile.sh`, and `enforce-gemini-rules.sh`
- [x] Run `quick_validate.py`, `tools/validate-all.sh`, `graphify update .`, and `steward.py check`
- [x] Read all changed non-code files in full, commit checkpoint on `checkpoint/steward-coordinator-refinement`, and report to user
