# Implementation Plan: Align AGENTS.md with Coordinator Graduating Wake Rules

## Objective
Update `AGENTS.md` and `.agents/memory/agents-md-limits-and-cross-references.md` to eliminate fixed 30-minute heartbeat conflicts and align Sections 10 and 13 with `coordinator/SKILL.md`, `coordinator/references/heartbeat-and-wake.md`, and `maestro/SKILL.md`, prior to committing, pushing to `origin/main`, and executing `/bootstrap`.

## Acceptance Criteria
1. `AGENTS.md` Section 10.1 replaces `at least every 30 minutes during active work` with `at start and every graduating wake tick (`coordinator/references/heartbeat-and-wake.md`), balancing limits dynamically`, preserving all `§1` through `§14` numbering and omitting hard-coded percentage thresholds.
2. `AGENTS.md` Section 13.1 replaces `session` with `chat`; Section 13.2 mandates `coordinator/SKILL.md` for both coordinated and standalone sustained work with the single graduating wake timer (`1m->3m->5m->12m->15m->30m`, reset to `1m` on action, `90-120m` user-blocked, cancelled at completion) and explicitly forbids a fixed 30-minute heartbeat; Section 13.3 replaces `scheduled check-in` with `wake tick`.
3. `AGENTS.md` remains strictly below 2,500 words (`len(text.split()) < 2500`), passes `tools/validate-all.sh` with zero errors in `AGENTS.md`, contains zero U+2014 em dashes and zero AI attribution, and passes `git diff --check` and `steward.py check`.
4. `.agents/memory/agents-md-limits-and-cross-references.md` accurately documents the updated Sections 10.1 and 13.1 through 13.3 behavior.

## Proposed Changes
- `[MODIFY] AGENTS.md`
- `[MODIFY] .agents/memory/agents-md-limits-and-cross-references.md`

## Blocking Questions
- None.

## Verification Plan
- **AC 1-2**: Full read of `AGENTS.md` from disk and inspection against `coordinator/SKILL.md`, `coordinator/references/heartbeat-and-wake.md`, and `maestro/SKILL.md`.
- **AC 3**: `python3 -c 'w = len(open("AGENTS.md", encoding="utf-8").read().split()); print(w); assert w < 2500'`, `bash tools/validate-all.sh`, `git diff --check`, and `python3 steward/scripts/steward.py check`.
- **AC 4**: Full read of `.agents/memory/agents-md-limits-and-cross-references.md` from disk.

## Temporary Artifacts
- None.
