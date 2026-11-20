# `AGENTS.md` Word Limit and Cross-References

- `AGENTS.md` is capped at **< 2,500 words** (enforced by `tools/validate-all.sh` and documented in `skill-creator/references/skill-authoring-standard.md`).
- Sections 3 through 11 preserve their original numbering from `cdc8647` so cross-references in `documentation`, `legalese`, `communications`, `pdf`, and `doc-coauthoring` (such as `§9.2`, `§9.3`, `§9.11`, and `§9.12`) remain accurate.
- Section 10 omits hard-coded percentage thresholds; Section 10.1 tracks usage at start and on every graduating wake tick, while usage thresholds (`95%` 5-hour / `98%` weekly) live exclusively in `coordinator/SKILL.md` and `coordinator/references/heartbeat-and-wake.md`.
- Section 9.14 routes external correspondence to `communications/SKILL.md`, Section 10.2 routes the controlled pause to `coordinator/references/heartbeat-and-wake.md`, and Section 13.2 enforces the single graduating wake timer (`1m->3m->5m->12m->15m->30m`, never a fixed 30-minute heartbeat) while Section 13.1 uses `chat` rather than `session`; `AGENTS.md` holds no em dash.
- Section 1.9 defines rule strength: `must`/`never` rules admit no exception; condition-bound rules bind under their own condition. Stewardship rules route to `steward/SKILL.md` from Sections 7.6 and 13.4.
