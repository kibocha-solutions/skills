# Session Hygiene and Writing Split

## Objective

Agents close and archive Maestro sessions without waiting for new work, keep evidence and environments outside projects, choose between chats and sub-agents by one rule, and route sentence-level prose quality to human-writer.

## Acceptance criteria

1. `sessions.py` closes, archives, indexes, and prunes sessions in Git and non-Git projects, verified in throwaway projects.
2. `steward.py store` creates, lists, and prunes agent-store entries, and `check` flags untracked evidence inside `.agents/`.
3. Coordinator channel selection applies to every agent and `AGENTS.md` routes to it.
4. Documentation routes prose quality to human-writer; legalese needs no change.
5. `quick_validate.py` passes for all changed skills; `tools/validate-all.sh` adds no finding; `AGENTS.md` stays below 2,500 words.
