# Implementation Plan: Lifecycle Hook and Global Agent Rules Refinement

## Objective
Refine the multi-agent pre-invocation lifecycle hook messages and global instructions (`AGENTS.md`) across all tool configurations (Antigravity, Gemini CLI, Claude Code, Codex, Copilot) to eliminate prompt injection false alarms, streamline execution procedures, establish rigorous skill workflow rules, and integrate autonomous usage window monitoring and scheduled resumption.

## Acceptance Criteria
1. Turn enforcement hook scripts (`enforce-gemini-rules.sh`, `enforce-claude-rules.sh`) are rewritten to be clean, authoritative, non-repetitive, and clearly framed as legitimate user operational mandates.
2. `AGENTS.md` Section 1 and Section 2 are updated with the exact step-by-step prompt lifecycle: skill discovery, full manual reading, mandatory reference/example review, mid-execution stops for referenced skills, and final visual/manual verification (including PDF and web screenshots).
3. `AGENTS.md` adds an autonomous usage and quota monitoring section defining the 5-hour (<15% available) and weekly (<5% available) thresholds, graceful state document generation, context compaction, and 5-minute post-reset wake-up scheduling.
4. Pre-completion checklists in `AGENTS.md` and related documentation reflect the new requirements.
5. All tool targets are synchronized and verified via `bootstrap/scripts/ensure-*-link.sh` without regression.
6. Proposals are presented cleanly for user approval before modifying operative scripts and shared rules.

## Proposed Changes
- `bootstrap/scripts/enforce-gemini-rules.sh` [MODIFY]
- `bootstrap/scripts/enforce-claude-rules.sh` [MODIFY]
- `bootstrap/references/hook-registration.md` [MODIFY]
- `AGENTS.md` [MODIFY]
- `bootstrap/scripts/lib.sh` [INSPECT/VERIFY]
- Mirror synchronization to `~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`, etc. [MODIFY via sync]

## Blocking Questions
None currently. Proposals will be presented to the user for formal approval prior to editing.

## Verification Method
- Execute hook scripts directly and inspect stdout/JSON schema validity.
- Verify `AGENTS.md` formatting and absence of banned em dashes in normal prose.
- Run bootstrap alignment scripts and verify propagation across target files.
