# Tasks: Lifecycle Hook and Global Agent Rules Refinement

## State: DONE

## Phase 1: Drafting Proposals for User Approval
- [x] Formulate cleaner, clearer, non-adversarial text for turn enforcement hooks (`enforce-gemini-rules.sh` and `enforce-claude-rules.sh`)
- [x] Formulate updated `AGENTS.md` rules for prompt-handling workflow (step-by-step skill execution, examples/references, mid-task stops, visual verification)
- [x] Formulate updated `AGENTS.md` rules for quota/usage window monitoring (dynamic short <15%, long <5%, multi-window balancing, state document, compaction, wake-up timer)
- [x] Present proposals and architectural separation (hook vs `AGENTS.md`) to the user and receive feedback/approval

## Phase 2: Implementation
- [x] Update `bootstrap/scripts/enforce-gemini-rules.sh` and `enforce-claude-rules.sh`
- [x] Update `AGENTS.md` with approved manual rules
- [x] Update `bootstrap/references/hook-registration.md` to reflect updated hook contracts and payloads
- [x] Execute alignment to propagate shared rules across host files (`GEMINI.md`, `CLAUDE.md`, etc.) and test hook scripts
- [x] Verify hook outputs and alignment across all tool configurations

## Phase 3: Verification and Initial Delivery
- [x] Full read of all modified files
- [x] Confirm no em dashes in normal prose
- [x] Confirm zero AI attribution
- [x] Record results in `walkthrough.md`
- [x] Commit and push changes via `ci-cd` (`1338be2`)
- [x] Run `bootstrap` scripts to align rules and sparse checkout mirrors across all agent platforms (Claude, Codex, Gemini, Copilot)

## Phase 4: Revertability, Identity Deduction, and Checkpoint Rules
- [x] Draft and integrate revertability, identity deduction, and checkpoint rules into `AGENTS.md`
- [x] Add explicit 30-minute quota check cadence to Section 10 in `AGENTS.md`
- [x] Full read of updated `AGENTS.md`
- [x] Commit and push via `ci-cd`
- [x] Re-run `bootstrap` scripts to align all agent platforms
