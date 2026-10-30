# Walkthrough: Coordinator Skill Proposal

## Completed
Researched primary guidance and published failure analysis. Recorded the coordinator skill proposal with team limits, role separation, bounded assignments, resource ownership, succession, quota monitoring, chat lifecycle, and evaluation cases.

Updated the repository's source rules to permit checkpoint commits and pushes to a dedicated checkpoint branch without separate authorization and to require explicit authorization for merges, squashes, and consolidation. Aligned the CI/CD skill and Git history reference.

## Evidence and Limitations
Read the proposal, repository rules, CI/CD skill, and Git history reference. `git diff --check` passed. The repository rule file contains 2,787 words, exceeding the skill-authoring standard's 1,500-word limit; reducing unrelated rules would exceed this change's scope. Visual rendering has not been performed. Installed global instruction files still contain the prior rules: bootstrap requires source changes to be committed and pushed before alignment. No commit, push, or alignment was performed.

## Resume Point
Review the proposal with the user. Resolve the rule-file length and visual verification requirements. When publication is authorized, follow the CI/CD and bootstrap procedures, preserving unrelated work, and verify each installed target. Create and evaluate the coordinator skill only when its design is accepted and implementation is requested.

## Implementation and Evaluation
The authorized scope now includes creating both skills and publishing and synchronizing them. The coordinator design was corrected to one coordinator, with a successor replacing that coordinator, and a shared limit for sub-agents. Both skill directories contain instructions, references, examples, and three evaluation prompts.

Independent paired simulations covered three coordinator scenarios and three writing scenarios. The coordinator with-skill responses preserved the chat cap, role separation, bounded retry response, and shared heavy-worker limit. The writing responses retained the time, chronological order, and instruction sequence. The factual writing baseline produced the same output as the skill run. These are small qualitative checks, not a benchmark; per-run token metrics were not available.

The skill-creator quick validator passed for both skills. Packages were generated in `/tmp`. The StoryScope PDF was retrieved as version 6 and its extracted text was read in full; PDF pages 6, 7, and 26 were visually inspected for its metrics and feature table.

## Coordination ID Amendment
Added role-based IDs and a shared registry: coordinators `0000` to `0009`, inspectors `1000` to `1999`, and executors `2000` to `2999`. The role prefix follows the user's stated values; the example calling `1000` an executor conflicts with that mapping. Added coordinator approval for worker-created children, completion cleanup, confirmed-deletion ID release, and a combined retained-child threshold of more than ten with up to seven eligible deletions. Active chat and heavy-worker caps remain in force.

The quick validator and JSON parsing passed, and the amended skill was packaged at `/tmp/coordinator.skill`. A paired read-only scenario found that the amended instructions assign the requested prefixes and release only confirmed-deleted IDs; the prior snapshot lacked these provisions. This is one qualitative comparison, not a complete benchmark, and per-run token metrics were unavailable. No actual child tasks were deleted. The amendment has not been committed, pushed, or deployed.

## Coordinator Rollover Amendment
Added the `0009` rollover sequence: preserve evidence and delete eligible retired predecessors; when `0000` is confirmed free, create its successor with instructions to delete the retired `0009` after handoff. If deletion of the previous `0000` is unavailable or unconfirmed, the ID remains reserved and rollover is reported as blocked. Added success and unavailable-deletion evaluation cases. The skill validator passed and the package was rebuilt. The complete evaluation suite has not been run. Changes remain local and undeployed.

## Worker Reporting Amendment
Required workers to notify their parent on completion, blockage, or a required decision and to pass that duty to their children. Parents acknowledge and relay unresolved concerns to the coordinator, who is the user-facing contact. Credential requests specify the access needed without transmitting secrets. Added reporting examples and two evaluation cases. The skill validator and JSON check passed. A paired read-only scenario confirmed the amended reporting chain; the previous version did not explicitly require proactive parent notification. Full benchmark and token metrics were not available.

## Mandatory Child Model Routing
Required explicit selection of a suitable lighter model for routine child work when the platform supports it. Added stronger-model exception and unavailable-selection reporting, examples, and evaluation cases. The skill validator, JSON parsing, and diff check passed. A paired read-only scenario returned Luna for the routine task in both versions; the amendment adds an explicit override requirement and fallback. Full benchmark and token metrics were unavailable.
