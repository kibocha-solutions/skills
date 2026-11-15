# Walkthrough: Steward Skill and Rule Tiers

## Context

Branch `checkpoint/steward-skill` cut from `main` at `4628df9`. Worktree was clean. Commits are SSH-signed.

## Log

- Read `bootstrap/SKILL.md`, `bootstrap/references/hook-registration.md`, `maestro/SKILL.md`, `AGENTS.md`, `skill-creator/SKILL.md`, `skill-creator/references/skill-authoring-standard.md`, `ci-cd/SKILL.md`, and the repository memory entries in full.
- `AGENTS.md` measured 2,479 words before changes.
- `communications/SKILL.md` already covers every element of `AGENTS.md` Section 9.14, so 9.14 is reduced to a routing line with its number preserved.
- `AGENTS.md`: added Section 1.9 rule strength, Section 7.1 recovery wording, Section 7.6 steward routing, Section 13.4 system profile, and a checklist line; routed 9.14 to `communications` and 10.2 to `coordinator`. Final count 2,480 words; Section 3 to 11 numbering unchanged.
- Enforcement hooks: one directive in `bootstrap/scripts/directive.sh`; all five host scripts pass shellcheck and emit valid output for their host.
- `steward`: `steward.py` pre-hook refused 6 of 6 violating commands and allowed 9 of 9 legitimate ones; stop hook blocked on a real leftover container, an untracked `.bak`, and an open ledger entry, warned without blocking on a repeated stop, and allowed finish after cleanup. `system-profile.sh` wrote the profile with no hostname, user name, or home path.
- Validation: `quick_validate.py` reports the skill valid; `tools/validate-all.sh` findings fell from 15 on `main` to 14, all in unchanged skills.
- Limitation: Codex, Gemini, and Copilot are not installed here; their steward event names are documented with a mandatory verification step before registration.
