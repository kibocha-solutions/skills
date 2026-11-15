# Tasks: Steward Skill and Rule Tiers

## State: AWAITING USER AUTHORIZATION (merge into main, bootstrap rollout)

## Phase 1: Shared rules
- [x] Add rule-strength clause and steward routing to `AGENTS.md` below 2,500 words
- [x] Strengthen the five enforce-rules directives

## Phase 2: Steward skill
- [x] Write `steward/SKILL.md` and decision reference
- [x] Write `system-profile.sh` and `steward.py`
- [x] Write examples and evals

## Phase 3: Integration
- [x] Wire steward into `maestro`
- [x] Register steward hooks in `bootstrap` and its reference
- [x] Update `README.md`

## Phase 4: Verification
- [x] Guard tests with real payloads
- [x] `tools/validate-all.sh` and skill validation
- [x] Full read of every changed file
- [x] Checkpoint commit on `checkpoint/steward-skill`

## Phase 5: Rollout (requires authorization)
- [ ] Consolidate into one durable commit on `main` and push
- [ ] Run `bootstrap` alignment and register steward hooks for installed hosts
- [ ] Verify hooks fire in a fresh session
- [ ] Retire the TalentSphere project-level container guard
