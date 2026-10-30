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
