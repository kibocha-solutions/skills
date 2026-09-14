# Skill Authoring Standard

## Authority placement

Use one controlling location for each instruction:

1. Put universal commands and prohibitions in `AGENTS.md`.
2. Put the universal skill discovery, reading, tracking, rereading, and final
   compliance procedure in the second section of `AGENTS.md`.
3. Put task-specific execution steps in `<skill>/SKILL.md`.
4. Put optional, variant-specific, or detailed operating specifications in
   `<skill>/references/`.
5. Put reusable output material in `<skill>/assets/`.
6. Put deterministic helpers in `<skill>/scripts/`.

Do not duplicate an instruction. Route to its controlling location.

## `AGENTS.md`

1. Keep `AGENTS.md` below 1,500 words.
2. Start with direct authority and compliance commands.
3. Put the complete skill-use procedure immediately after the general commands.
4. Include only rules that apply across repositories and task types:
   - substantive obedience
   - skill discovery and full-reading requirements
   - continuity and planning gates
   - permission and destructive-action limits
   - tool and dependency installation gates
   - source and confidentiality boundaries
   - deliverable prohibitions
   - exact-final-artifact verification
5. Use `must`, `must not`, `always`, and `never` for absolute obligations.
6. State each rule as a command or prohibition.
7. Exclude task-specific procedures, command catalogues, examples, incident
   histories, justifications, templates, and domain specifications.
8. Keep task-specific mechanics in the activated skill or its references.

## `SKILL.md`

### Frontmatter

1. Include `name` and `description`.
2. Match `name` to the directory name.
3. Put every trigger condition in `description`.
4. State the skill capability and the requests that activate it.
5. Add `compatibility` only when a tool or dependency is required.
6. Do not repeat trigger guidance in the body.

### Body

1. Start with prerequisites or routing checks.
2. Present steps in execution order.
3. Name each required input and output at the step that uses it.
4. State each decision branch where it occurs.
5. State each prohibition beside the affected step.
6. End with exact verification and delivery checks.
7. Use imperative sentences.
8. Keep one action or constraint per sentence.
9. Use numbered lists for sequences.
10. Use bullets for independent checks.
11. Include only text that changes execution.
12. Remove introductions, conclusions, motivation, rationale, persuasion,
    conversational asides, theory, history, incident narratives, and
    explanations of why an instruction matters.
13. Do not use U+2014 em dashes.
14. Do not use diminish-to-elevate constructions, promotional claims, vague
    attribution, purposeless fourth-wall prose, chatbot phrases, or placeholder
    residue.
15. Keep `SKILL.md` below 500 lines.
16. Keep one coherent job per skill.

### References

1. Link each reference from the exact step that requires it.
2. State when to read the reference.
3. Do not require unrelated references.
4. Write references as operating specifications, lookup tables, commands,
   schemas, or variant procedures.
5. Remove background explanation and duplicated rules.
6. Add a table of contents to a reference longer than 300 lines.

### Assets and scripts

1. Store templates, examples, and reusable output shells in `assets/`.
2. Add a script only for deterministic or repeated work.
3. Document the script's inputs, outputs, dependencies, invocation, and failure
   behavior at the calling step.

## Revision procedure

1. Read the governing `AGENTS.md` in full.
2. Read the existing `SKILL.md` from start to finish.
3. Read every reference required for the requested change.
4. Record the skill responsibility, triggers, inputs, outputs, ordered steps,
   prohibitions, and verification checks.
5. Remove content outside the skill responsibility.
6. Rewrite the retained instructions in execution order.
7. Move detail to the correct reference, asset, or script.
8. Preserve verified capabilities and user-locked wording.
9. Re-read the final `SKILL.md` from start to finish.
10. Re-read every changed reference from start to finish.
11. Validate frontmatter, links, scripts, line count, and residue checks.
12. Test representative requests when the change affects behavior.

## Completion checks

- [ ] YAML frontmatter is valid.
- [ ] Directory name and frontmatter `name` match.
- [ ] Every trigger condition appears in `description`.
- [ ] The body follows execution order.
- [ ] Every sentence changes execution.
- [ ] Universal rules are routed to `AGENTS.md`.
- [ ] No explanation or justification remains.
- [ ] No U+2014 em dash remains.
- [ ] No forbidden documentation pattern remains.
- [ ] Every local link resolves.
- [ ] Every required resource exists.
- [ ] No placeholder or chatbot residue remains.
- [ ] `SKILL.md` contains fewer than 500 lines.
- [ ] The final full read is complete.
