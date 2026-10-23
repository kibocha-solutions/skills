# Walkthrough: Lifecycle Hook and Global Agent Rules Refinement

## Context
Refining multi-agent lifecycle hooks and `AGENTS.md` to eliminate agent confusion/prompt injection false alarms, streamline execution, define the prompt-to-delivery skill procedure, and add autonomous usage monitoring and sleep/wake cycles.

## Phase 1 Progress
- Analyzed existing `bootstrap/scripts/enforce-gemini-rules.sh`, `enforce-claude-rules.sh`, `bootstrap/references/hook-registration.md`, and `AGENTS.md`.
- Formulated clean, authoritative hook text and detailed operational rules for `AGENTS.md`.
- Refined quota window definitions per user directive into short windows (<3 days) and long windows (>=3 days) with multi-window balancing.

## Phase 4 Progress
- Added Section 4 rules 6 to 10 in `AGENTS.md` covering project revertability, identity deduction (inspecting repository clues outward to path context, with fallback to best-guess defaults), baseline snapshots, checkpoint isolation on working branches, and consolidation/pruning before publishing.
- Verified absence of specific examples, real repository names, or private identities in accordance with user instructions.
- Full manual read of `AGENTS.md` completed.

