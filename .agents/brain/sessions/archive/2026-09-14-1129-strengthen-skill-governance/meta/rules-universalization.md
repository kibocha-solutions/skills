# PBO rules universalization register

Source read in full: `/mnt/data/.Trash-1000/files/RULES.md`

| Rule | Universal form | Shared instruction | Mechanics or examples |
|---:|---|---|---|
| 1 | Yes | Read every mandated durable-memory store before substantial work and before re-deriving a convention. | `maestro/SKILL.md` |
| 2 | Yes | Preserve deliberate duplication across mandated memory systems and read each store independently. | `maestro/SKILL.md` and its memory reference |
| 3 | Yes | Withhold sensitive information unless the user requests the exact item or a controlling form requires it. | `documentation/SKILL.md` |
| 4 | Yes | Keep agent context and repository mechanics out of reader-facing work. Refer to documents by reader-facing title. | `documentation/SKILL.md` |
| 5 | Yes | Include only information required by the reader's task. | `documentation/SKILL.md` |
| 6 | Yes | Keep purpose and rationale out of operative text and metadata. | `documentation/SKILL.md`; `legalese/SKILL.md` |
| 7 | Yes | Never narrate compliance inside a deliverable. | `documentation/SKILL.md` |
| 8 | Yes | Never narrate drafting status, progress, approval state, or production history inside a deliverable. | `documentation/SKILL.md` |
| 9 | Yes | Match mood, tense, voice, and authority register to the actual document type. | `documentation/SKILL.md`; `legalese/SKILL.md` |
| 10 | Yes | Every retained sentence must perform a specific function. Remove filler and defensive justification. | `documentation/SKILL.md`; `documentation/references/weak-ai-writing-patterns.md` |
| 11 | No general form without distortion | Treat an assigned legal register as a floor. | `legalese/SKILL.md` and register reference |
| 12 | Yes | Remove the underlying defect; never substitute punctuation, synonyms, or labels while preserving it. | Early skill-use protocol in `AGENTS.md`; skill-authoring and documentation references |
| 13 | Yes, with a PBO-specific exception map | Do not use U+2014 em dashes in normal prose. | `documentation/references/pbo-document-rules.md` contains the ANCEM and SOP exceptions and stricter paths. |
| 14 | Fixed-layout universal | Use available page space, permit only structurally justified short pages, and inspect the final render. | `documentation/references/letterhead-and-pagination.md` |
| 15 | Proposal-specific mechanics; universal evidence rules | Never fabricate a person, quotation, event, source, or fact. Match citation form and structure to the document type. | `documentation/references/ngo-and-donor-narrative.md` |
| 16 | PBO-only exact defaults | Apply the controlling template. | Exact proposal typography remains only in `documentation/references/pbo-document-rules.md`. |
| 17 | Yes | Verify before writing. Never guess or present an unresolved fact as settled. | `documentation/SKILL.md`; applicable research or legal skill |
| 18 | Yes | Preserve user-supplied and expressly locked wording. Propose changes before applying them. | `documentation/SKILL.md`; `legalese/SKILL.md` |
| 19 | Yes | AI attribution is prohibited in every work product and publication surface. | `ci-cd/SKILL.md`, commit template, Git reference, and pull-request reference |
| 20 | Yes for delivered work | Keep uncertainty markers and approximation language out of delivered artifacts. Tell the user about unresolved facts in chat. | `documentation/SKILL.md` |
| 21 | Yes | Read a narrative or governing instruction in full. Search and summaries never replace the read. | Early skill-use protocol in `AGENTS.md`; `documentation/SKILL.md` |
| 22 | Yes | Keep metadata to structured values. Exclude rationale, status narration, and working notes. | `documentation/SKILL.md` |
| 23 | Yes for derived artifacts | Regenerate every derived output after the final source change. Never hand-patch generated deliverables. | Artifact skills and pagination reference |
| 24 | Yes | Validate the exact final artifact and bind absolute claims to evidence from that artifact. | Artifact skills and their final checklists |

## Result

The PBO source contains 21 directly universal rules, two universal rules with
document-specific mechanics, and one legal-register rule that remains in the
legal skill. Exact PBO proposal formatting remains only in the PBO-specific
reference.
