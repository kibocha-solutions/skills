---
name: doc-coauthoring
description: Guide collaborative creation of documentation, proposals, technical specifications, decision records, PRDs, RFCs, and other structured documents. Use when the user wants an interactive context-gathering, section-refinement, and reader-testing workflow. Use documentation with this skill for content quality and document structure.
license: Apache-2.0, adapted from the upstream skill of the same name
---

# Document Co-Authoring

## 1. Start the workflow

1. Apply `documentation/SKILL.md`.
2. Identify the document type, audience, intended result, template, format, and
   deadline.
3. Offer these stages:
   - context gathering
   - section drafting and refinement
   - reader testing
4. Continue with the staged workflow when the user accepts.
5. Work freeform when the user declines.
6. Follow the user's request to skip or reorder a stage.

## 2. Gather context

1. Ask:
   - What document type is required?
   - Who is the primary audience?
   - What should the reader know, decide, or do?
   - What template or format controls?
   - What constraints apply?
2. Read every supplied template, file, shared document, and relevant source.
3. Use an available connector when the user authorizes access to a shared
   source.
4. Ask the user to paste inaccessible source content.
5. Check supplied images for alt text.
6. Offer alt-text drafting for missing descriptions.
7. Ask the user to provide:
   - project or problem background
   - prior decisions and alternatives
   - architecture and dependencies
   - stakeholder requirements
   - timeline and operational constraints
   - source documents and data
8. Track confirmed facts, preferences, unknowns, and conflicts.
9. Ask five to ten numbered questions after the initial context is available.
10. Accept shorthand, numbered answers, freeform additions, files, and links.
11. Repeat targeted questions until the document's edge cases and tradeoffs are
    clear.
12. Ask whether to add context or begin drafting.

## 3. Establish the structure

1. Apply the controlling template.
2. Propose three to five sections when no structure is supplied.
3. Ask the user to confirm or change the structure.
4. Start with the section containing the most unresolved substance.
5. Leave summaries and executive overviews until the underlying sections are
   stable.
6. Create the document in the available artifact tool or an appropriately
   named working file.
7. Add placeholders for the confirmed sections.
8. Tell the user where the working document is stored.

## 4. Draft each section

Repeat this sequence for every section:

1. Name the section being drafted.
2. Ask five to ten section-specific questions.
3. Generate five to twenty numbered content options.
4. Include relevant context that has not yet been placed.
5. Ask the user which options to keep, remove, combine, or change.
6. Accept numbered or freeform curation.
7. Ask for a brief reason when a choice changes later sections.
8. Ask whether an important point is missing.
9. Replace the section placeholder with drafted content.
10. Edit the stored document directly.
11. Show the location of the updated draft.
12. Ask for targeted change instructions.
13. Apply targeted edits without reprinting the complete document.
14. Record the user's style and structure preferences.
15. Continue until the user accepts the section.
16. After three refinement passes, test whether any content can be removed.
17. Move to the next section only after confirming the transition.

## 5. Review the complete draft

1. Re-read the complete document after most sections are stable.
2. Check:
   - flow
   - consistency
   - completeness
   - duplicated content
   - contradictions
   - undefined terms
   - weak transitions
   - generic filler
   - unsupported claims
   - unnecessary sentences
3. Correct defects in the source document.
4. Repeat the complete read.
5. Ask whether to refine further or begin reader testing.

## 6. Predict reader questions

1. Generate five to ten questions the intended reader would ask.
2. Cover retrieval, interpretation, required action, assumptions, edge cases,
   and missing context.
3. Use only the document and the intended audience when writing the questions.

## 7. Test with an independent reader

When an independent agent is available:

1. Give the agent only the document and one reader question at a time.
2. Do not provide conversation history or drafting notes.
3. Record the answer, ambiguity, assumed knowledge, and incorrect inference.
4. Repeat for every reader question.
5. Run one additional review for:
   - ambiguous language
   - missing definitions
   - false assumptions
   - internal contradictions
   - inconsistent terminology
6. Summarize each failed reader test.
7. Return failed sections to the refinement sequence.
8. Repeat reader testing after corrections.

## 8. Use the manual fallback

When no independent agent is available:

1. Give the user the reader questions.
2. Ask the user to open a new context-free conversation.
3. Ask them to provide only the document.
4. Ask the fresh reader for:
   - an answer to each question
   - ambiguous or unclear passages
   - assumed prior knowledge
   - contradictions and inconsistencies
5. Collect the results.
6. Return failed sections to the refinement sequence.
7. Repeat the manual test after corrections.

## 9. Finalize

1. Require the independent reader to answer consistently without new gaps.
2. Apply the full verification sequence in `documentation/SKILL.md`.
3. Verify facts, figures, citations, links, commands, and technical details.
4. Remove placeholders and drafting residue.
5. Keep drafting history and conversation references out of the document.
6. Render and inspect the exact final artifact when layout matters.
7. Ask the user whether one final review is required.
8. Deliver the verified document and its location.
