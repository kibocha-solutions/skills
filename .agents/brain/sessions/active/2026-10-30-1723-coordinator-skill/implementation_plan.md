# Implementation Plan: Coordinator Skill Proposal

## Objective
Research and record a detailed design for a future coordinator skill and update the repository's checkpoint authorization rules.

## Acceptance Criteria
1. A persistent proposal addresses every requested coordination constraint and provides operational workflows, assignment contracts, stop conditions, handoffs, resource controls, and evaluation cases.
2. The proposal identifies the research and distinguishes evidence from design recommendations.
3. The repository rules authorize scoped checkpoint commits and checkpoint pushes without separate approval, and require authorization for merging, squashing, and consolidation.
4. Conflicting Git guidance is aligned with the requested checkpoint boundary.
5. All changed files are read in full and reviewed against these criteria.

## Proposed Changes
- `AGENTS.md` [MODIFY]: Update checkpoint and history authorization boundaries.
- `ci-cd/SKILL.md` [MODIFY]: Align history and publication rules.
- `ci-cd/references/git-and-history.md` [MODIFY]: Align Git procedure.
- `meta/coordinator-proposal.md` [NEW]: Record research and the proposed coordinator skill design.
- Session plan, tasks, and walkthrough [NEW]: Track scope and evidence.

## Verification
Read each changed file and the proposal in full. Check the checkpoint authorization, scope, publication, and history clauses for consistency. Trace each requested coordinator requirement to the proposal and verify its source links.

## Blocking Questions
None for the proposal or source rule edits.
