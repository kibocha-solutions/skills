# Walkthrough - graphify-cleanup-rollout

## Start

- Read `AGENTS.md`, graphify skill instructions, and Maestro references.
- No matching active Maestro session existed for this rollout.
- Created this session to track the instruction update and downstream repository cleanup/reset work.

## Blockers

- Attempted to patch `/home/codelf/.codex/skills/graphify/SKILL.md` with a mandatory post-run cleanup gate naming generated root scaffolding to remove and preserved `graphify/` / `.agents/` layouts.
- The approvals reviewer rejected the patch because it is a persistent global skill change outside the workspace that mandates future repo cleanup/deletions.
- Do not attempt to bypass this via another write mechanism. Continue only after explicit user approval for that global skill behavior change, or use a safer alternative chosen by the user.

## Instruction Update

- User explicitly approved the global graphify behavior change.
- Added Step 9.5 to `/home/codelf/.codex/skills/graphify/SKILL.md`, requiring a final repository-root cleanup pass before graphify is considered satisfied.
- The new gate preserves `graphify/`, `.agents/brain/`, and `.agents/skills/` only when the documentation skill is present, and names the generated agent scaffolding to remove.
- Updated tracked `graphify/SKILL.md` with the same mandatory cleanup semantics and resolved the root-ignore-file conflict by limiting durable root ignore files to explicit activation.
- Created new commit `06637e3 fix(graphify): require generated scaffolding cleanup`; did not amend or rewrite previous commit `281f765`.
- Pushed `main` to `origin/main` (`281f765..06637e3`).

## lnp-dataset

- Removed generated root scaffolding from `/home/codelf/workspace/dhanush/lnp-dataset`: duplicated agent rule files, agent-client config folders, generated MCP/editor configs, generated GitHub CRG instruction folder, generated CRG ignore files, generated report, and generated `.gitignore`.
- Preserved `/home/codelf/workspace/dhanush/lnp-dataset/graphify` and `.agents/skills`.
- Verified `.agents/skills/documentation/SKILL.md` exists.
- Ran `git fetch origin && git reset --hard origin/main` in `.agents/skills`; HEAD and `origin/main` both resolved to `281f765ae3abfa669236f38814c1f728c4050ecc`.
- Final generated-scaffolding root scan returned no paths.
- User-facing readiness message was sent for `lnp-dataset`.

## msngi

- Removed generated untracked root files `.cgcignore` and `.code-review-graphignore`.
- Preserved the dirty parent worktree and did not reset unrelated repo changes.
- Ran `git fetch origin && git reset --hard origin/main` in `.agents/skills`; it advanced to `06637e3 fix(graphify): require generated scaffolding cleanup`.

## M365 Mapping

- Found `.agents/skills` checkouts:
  - `/home/codelf/workspace/kibocha-solutions/M365/Assignments/7017-MANA/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/AYNI/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/invoices/.agents/skills`
- Found legacy `skills/` checkouts:
  - `/home/codelf/workspace/kibocha-solutions/M365/ANCEM-Budget-Proposal/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/UNTF/skills`
- Root generated-scaffolding scan for likely M365 project roots returned no root-level candidates.

## Current Blocker

- Bulk reset of M365 skills checkouts was rejected by the approvals reviewer because several targets are on feature branches with local modifications and untracked files:
  - `Assignments/7017-MANA/.agents/skills`: `feat/docs`, modified `AGENTS.md`, untracked `.brain/`, `legalese/`, `sources/ppt-master/`.
  - `FODDAJ/AYNI/.agents/skills`: `main`, modified `AGENTS.md`, documentation files, untracked `documentation/references/install-writerside.md`, `jupyter-notebook/`.
  - `ANCEM-Budget-Proposal/skills`: `feat/docs`, untracked `ppt-master/`, pycache.
  - `FODDAJ/UNTF/skills`: `feat/docs`, modified `AGENTS.md`, untracked `legalese/`, `sources/ppt-master/`, pycache.
- Need explicit user approval for destructive branch checkout/hard reset of these M365 skills checkouts despite the risk of destroying unpushed work.

## M365 Completion

- User approved destructive reset limited to skills checkouts only.
- Reset and cleaned all real M365 skills checkouts to `origin/main` at `06637e3`:
  - `/home/codelf/workspace/kibocha-solutions/M365/Assignments/7017-MANA/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/Assignments/WBU/week-2/essay-1/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/Assignments/WBU/week-5/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/AYNI/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/SPOTLIGHT/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/invoices/.agents/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/ANCEM-Budget-Proposal/skills`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/UNTF/skills`
- Removed generated CGC/CRG artifacts outside allowed graph locations:
  - `/home/codelf/workspace/kibocha-solutions/M365/Assignments/WBU/week-2/essay-1/.cgcignore`
  - `/home/codelf/workspace/kibocha-solutions/M365/Assignments/WBU/week-2/essay-1/references/.cgcignore`
  - `/home/codelf/workspace/kibocha-solutions/M365/FODDAJ/SPOTLIGHT/.code-review-graph`
- Verified every listed skills checkout reports `main...origin/main`, `HEAD == origin/main == 06637e3`, and `documentation/SKILL.md` exists.
- Final generated-scaffolding scan across `lnp-dataset`, `msngi`, and `M365`, excluding `graphify/`, skills checkouts, and Git internals, returned no paths.

## Final Verification

- Global installed graphify skill contains Step 9.5 cleanup gate.
- Tracked `graphify/SKILL.md` contains the mandatory cleanup requirement and documentation-skill condition.
- Skills repo is on `main...origin/main`, with `HEAD == origin/main == 06637e3`.
- `lnp-dataset`, `msngi`, and all found M365 skills checkouts are reset to `origin/main` at `06637e3`.
