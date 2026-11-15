# Steward Skill and Rule Tiers

## Objective

Agents treat every rule as mandatory, clean up after themselves, rely on versioning instead of leftover copies, and work within the measured capacity of the machine, on every host the bootstrap skill manages.

## Acceptance criteria

1. `AGENTS.md` states that every rule is mandatory, distinguishes no-exception rules from condition-bound rules, routes to `steward`, and stays below 2,500 words with Section 3 to 11 numbering intact.
2. Each `enforce-*-rules.sh` directive states that compliance is mandatory and not advisory, covers steward cleanup, contains no U+2014 em dash, and emits valid output for its host.
3. `steward/SKILL.md` exists with valid frontmatter, imperative steps in execution order, fewer than 500 lines, and links that resolve.
4. `steward/scripts/system-profile.sh` writes a user-level profile without the hostname and prints a summary.
5. `steward/scripts/steward-guard.sh` blocks unlabelled or excess throwaway containers and backup-pattern copies inside a Git worktree, and blocks session end while leftovers remain, verified with real payloads.
6. `maestro` reads the system profile at orientation and requires a clean steward check before completion.
7. `bootstrap` registers the steward hooks for installed hosts and documents them in `references/hook-registration.md`.
8. `steward/evals/evals.json` holds objective cases; `tools/validate-all.sh` passes.

## Proposed changes

- [MODIFY] `AGENTS.md`: rule-strength clause, Section 7 steward routing, Section 9.14 routed to `communications`, Section 13 profile item, checklist item.
- [MODIFY] `bootstrap/scripts/enforce-claude-rules.sh`, `enforce-codex-rules.sh`, `enforce-gemini-rules.sh`, `enforce-gemini-cli-rules.sh`, `enforce-copilot-rules.sh`: stronger directive.
- [NEW] `steward/SKILL.md`, `steward/references/decision-rules.md`, `steward/scripts/system-profile.sh`, `steward/scripts/steward-guard.sh`, `steward/examples/good-vs-bad-stewardship.md`, `steward/evals/evals.json`.
- [MODIFY] `maestro/SKILL.md`: orientation and checklist lines.
- [MODIFY] `bootstrap/SKILL.md`, `bootstrap/references/hook-registration.md`: steward hook registration, skill count.
- [MODIFY] `README.md`: skill list.

## Blocking questions

None. Merging into `main` and running `bootstrap` require the User's authorization.

## Verification

1. `wc -w AGENTS.md`; numbering diff; `tools/validate-all.sh`.
2. Run each enforce script; validate JSON with `python3 -m json.tool`; grep for U+2014.
3. `skill-creator/scripts/quick_validate.py steward`; line count; link check.
4. Run `system-profile.sh`; confirm file written and hostname absent.
5. Pipe real hook payloads through `steward-guard.sh` and create a real leftover container.
6. Full read of `maestro/SKILL.md`.
7. Full read of changed bootstrap files; JSON snippets parse.
8. `python3 -m json.tool steward/evals/evals.json`; `tools/validate-all.sh`.
