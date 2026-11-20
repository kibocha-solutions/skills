# Tasks: Align AGENTS.md with Coordinator Graduating Wake Rules
## State: DONE (Aligned root operating rules with coordinator graduating wake timer and chat terminology.)
## Gates and Prohibitions
- `AGENTS.md` must stay strictly `< 2500` words (`len(text.split())`), preserve `§1` through `§14` numbering, keep percentage thresholds in `coordinator/`, and avoid U+2014 em dashes and AI attribution.
- Under `approval_mode: ask`, do not modify pre-existing errors in unrelated `ci-cd/` or `communications/` files and do not run `sessions.py prune --apply` on pre-existing archives.

## Phase 1: Create Maestro Session
- [x] Create `.agents/brain/sessions/active/2026-11-20-1139-align-agents-graduating-wake/` with `meta/`, `implementation_plan.md`, `tasks.md`, and `walkthrough.md`

## Phase 2: Edit AGENTS.md and Update Memory
- [x] Update `AGENTS.md` Sections 10.1 and 13.1 through 13.3 to enforce the graduating wake timer (`1m->3m->5m->12m->15m->30m`), forbid fixed 30-minute heartbeats, and align `chat` and `wake tick` wording
- [x] Update `.agents/memory/agents-md-limits-and-cross-references.md` to match updated Sections 10.1 and 13.1 through 13.3

## Phase 3: Verify Repository Edits and Close Maestro Session
- [x] Read modified `AGENTS.md` and `.agents/memory/agents-md-limits-and-cross-references.md` in full from disk
- [x] Verify `AGENTS.md` word count `< 2500`, `tools/validate-all.sh` zero errors on `AGENTS.md`, `git diff --check`, and `steward.py check`
- [x] Finalize `walkthrough.md` and close/archive Maestro session as `DONE`
