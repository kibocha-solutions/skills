# Walkthrough: Session Hygiene and Writing Split

Agents now close Maestro sessions with fixed states, archive at close, keep evidence and environments in `~/.agents/`, and pick chats or sub-agents by one shared rule.

- `sessions.py` passed throwaway-project tests: finished sessions archived, a stale session closed as ABANDONED, evidence moved to the agent store, index written, Git retention kept 10 folders with restore commands, and non-Git pruning bundled a quarter.
- `steward.py store` passed path, list, dry-run, and apply tests in an isolated home; the `.agents` evidence check flagged an untracked screenshot.
- All five changed skills pass `quick_validate.py`; `ruff` reports no findings; `tools/validate-all.sh` findings unchanged at 14, none in changed files; `AGENTS.md` is 2,470 words.
- Legalese was inspected in full and holds only legal drafting rules; nothing moved.
