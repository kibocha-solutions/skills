# Implementation Plan: Standing Rules Migration

## Objective

Move every msngi Standing Rule not yet carried by the shared `AGENTS.md` or a
skill into the applicable skill, fix the documentation skill's conflation of
external-deliverable title-only referencing with documentation-library linking,
then delete the msngi repository `AGENTS.md`.

## Coverage map

| msngi rule | Existing home | Gap and target |
|---|---|---|
| 1, 2 | shared AGENTS.md 4 | none |
| 3 | shared AGENTS.md 8.2; documentation 5.4 | financial amounts beyond the request, compliance status, eligibility statement is not a form field: documentation 5.4 |
| 4 | shared AGENTS.md 8.3, 8.4 | none |
| 5 to 8, 10, 12, 19 | shared AGENTS.md 1, 9 | none |
| 9 | documentation 3; legalese Doctrine 4 | no `shall` in procedures or correspondence: documentation 3 |
| 11 | legalese 2.11, Doctrine 1 | none |
| 13, 16 | documentation cso-document-rules | none |
| 14 | documentation letterhead-and-pagination | none |
| 15 | documentation ngo-and-donor-narrative | none |
| 17 | shared AGENTS.md 10.1; documentation 2 | none |
| 18 | documentation 2.7; legalese Doctrine 9 | propose before changing locked wording, other wording editable: documentation 2.7 |
| 20 | system-design 5, 6, 11 | precedent research record, name reuse, plural and snake_case, change tests, illustrative examples: system-design 5, 6, naming reference |

## Acceptance criteria

1. Every gap in the coverage map appears in its target file.
2. Documentation SKILL.md 7.8 and the checklist scope title-only referencing to
   external deliverables and require relative documentation-library links.
3. The Writerside reference removes an unsafe cross-tier reference instead of
   replacing it with plain text.
4. `tools/validate-all.sh` passes; every changed file read in full.
5. msngi `AGENTS.md` deleted; its memory index link removed.

## Files

- [MODIFY] documentation/SKILL.md, documentation/references/writerside-technical-documentation.md, documentation/evals/evals.json
- [MODIFY] system-design/SKILL.md, system-design/references/naming-and-responsibility.md, system-design/evals/evals.json
- msngi: [DELETE] AGENTS.md, [MODIFY] .agents/MEMORY.md

## Verification

Validator run; full reads; diff review against the coverage map.
