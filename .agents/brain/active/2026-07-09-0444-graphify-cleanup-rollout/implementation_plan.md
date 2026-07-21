# Graphify Cleanup Rollout

## Goal Statement

Make graphify's operating instructions explicitly require agents to audit and remove generated agent-client scaffolding after graphify/code-review-graph setup, then roll that corrected behavior into the requested downstream repositories by cleaning root scaffolding and resetting each `.agents/skills` checkout to the latest `origin/main`.

## Acceptance Criteria

1. The graphify skill requires a post-run repository cleanup pass before the skill is considered satisfied.
2. The cleanup rule preserves `graphify/` and `.agents/` only when `.agents/` contains allowed `brain/` and/or `skills/` content, with `skills/` containing the documentation skill.
3. The skills repo change is committed as a new commit without rewriting the previous latest commit, and pushed.
4. `lnp-dataset` has redundant generated root scaffolding removed and `.agents/skills` reset to the latest `origin/main`; the user is notified immediately after this is verified.
5. `msngi` and all M365 target folders under `~/workspace/*` receive the same cleanup and `.agents/skills` reset.

## Proposed Changes

- [MODIFY] `/home/codelf/.codex/skills/graphify/SKILL.md` - add explicit mandatory cleanup requirements after graph generation/setup.
- [MODIFY] skills repository - record Maestro tracking and commit the instruction update without amending history.
- [DELETE] downstream repo generated scaffolding - remove client-specific files such as `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.github/`, `.mcp.json`, and equivalent generated code-review-graph wrappers outside preserved directories.

## Open Questions

None blocking. Interpret "without changing the commit of the latest commit" as "do not amend or rewrite the existing latest commit; create a new commit for the instruction change."

## Verification Plan

- Inspect the graphify skill text for the new mandatory cleanup section.
- Use `git status`, `git log -1`, and `git push` output to verify the skills repo commit/push.
- For each downstream repo, verify listed scaffolding paths are absent, preserved paths remain, `.agents/skills` exists, and `.agents/skills` reports `HEAD == origin/main`.
