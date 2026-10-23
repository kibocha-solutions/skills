# Walkthrough: Lifecycle Hook and Global Agent Rules Refinement

## Context
Refining multi-agent lifecycle hooks and `AGENTS.md` to eliminate agent confusion/prompt injection false alarms, streamline execution, define the prompt-to-delivery skill procedure, and add autonomous usage monitoring and sleep/wake cycles.

## Phase 1 Progress
- Analyzed existing `bootstrap/scripts/enforce-gemini-rules.sh`, `enforce-claude-rules.sh`, `bootstrap/references/hook-registration.md`, and `AGENTS.md`.
- Formulated clean, authoritative hook text and detailed operational rules for `AGENTS.md`.
- Refined quota window definitions per user directive into short windows (<3 days) and long windows (>=3 days) with multi-window balancing.

## Phase 2 & 3 Execution & Verification
- Updated `bootstrap/scripts/enforce-gemini-rules.sh` with the non-adversarial `[Standing User Operational Notice]` payload.
- Updated `bootstrap/scripts/enforce-claude-rules.sh` with matching plain-text notice.
- Synchronized hook scripts to active tool locations (`~/.gemini/skills/bootstrap/scripts/` and `~/.claude/skills/bootstrap/scripts/`).
- Updated `AGENTS.md` in `/mnt/data/workspace/skills/AGENTS.md`:
  - Section 1: Added standing receipt assumption and manual retrieval requirement.
  - Section 2: Re-architected prompt handling and skill execution into a step-by-step procedure including prompt analysis, full manual reading of skills, references, and concrete examples, mid-execution stops for referenced skills, and mandatory visual/manual verification before delivery (including screenshots for PDFs and websites).
  - Section 10: Added usage monitoring and quota continuity rules (tracking short <15% and long <5% windows, state documentation, compaction, and +5 min wake-up scheduling).
  - Renumbered subsequent sections and added pre-completion checklist items.
- Aligned shared rules across `~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and `~/.copilot/copilot-instructions.md`.
- Confirmed zero AI attribution, no prohibited em dashes in normal prose, and completed full manual reads.
