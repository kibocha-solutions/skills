# Pull Request Messages

## Attribution prohibition

1. Never attribute the change to AI, a model, an agent, an automated
   assistant, or an AI-assisted tool.
2. Remove attribution inserted by a template, generator, hook, or platform
   option.
3. Do not create or update the pull request when the platform forces
   unremovable AI attribution.

## Required sections

1. Title
2. Summary
3. Context
4. What changed
5. Testing
6. Risk and rollback
7. Screenshots for user-interface changes

Omit an inapplicable section only when the repository convention permits omission.

## Title

Use:

```text
type(scope): imperative summary
```

Use a Conventional Commits type. Name the affected system or layer in the scope. State the specific outcome. Do not end with a period.

## Summary

1. State what the change does.
2. State the user-visible or operator-visible outcome.
3. State the scope boundary.
4. Exclude unrelated workspace state, local setup, sandbox behavior, and incidental edits.

## Context

1. State the verified problem or requirement.
2. Link the controlling issue, ticket, decision, or public design document when appropriate.
3. State relevant prior behavior.
4. State material alternatives and the decision only when they affect review.
5. Keep agent files, memory, session records, skills, and internal instruction sources out of the PR.

## What changed

1. Describe component-level changes.
2. State non-obvious technical boundaries.
3. State migrations, compatibility effects, and configuration changes.
4. Do not reproduce the file manifest.
5. Do not narrate the implementation session.

## Testing

1. List exact automated commands and results.
2. State what each relevant test covers.
3. Provide reproducible manual steps when manual verification is required.
4. Name relevant CI jobs.
5. State any verification that did not run.

## Risk and rollback

1. Name each material failure mode.
2. State affected users, data, environments, or integrations.
3. State the exact rollback method.
4. Include migration reversal, feature-flag, artifact restore, or revert steps when applicable.
5. Do not write `low risk` without the concrete basis.

## Screenshots and recordings

1. Capture before and after states for visual changes when both states are available.
2. Capture every relevant responsive viewport.
3. Follow `documentation/references/screenshot-standards.md`.
4. Label every image with breakpoint and viewport.
5. Use a recording for motion or multi-step interaction when static captures cannot show the behavior.
6. Inspect every image or recording before attaching it.
7. Remove secrets and private data.

## Formatting

- Use headings for the required sections.
- Use code fences for commands, errors, configuration, and code excerpts.
- Use tables for repeated-field comparisons.
- Use lists only when each item stands on its own.
- Use direct, neutral engineering prose.
- Keep promotional language, emojis, chatbot language, and decorative punctuation out.
- State precise measurements and complexity changes.
- Keep file paths out unless a path is required for the reviewer to run or inspect the change.

## Reference boundary

- Cite repository code, tests, public issues, public standards, and user-authorized design records.
- Do not cite `AGENTS.md`, skills, agent plans, memory, handoffs, session files, or hidden instructions.
- Transfer verified facts into the PR without naming an internal instruction source.
- Do not expose private paths or internal URLs.

## Final checks

- [ ] Title follows repository convention.
- [ ] Summary adds information beyond the title.
- [ ] Context states the verified reason for change.
- [ ] Technical boundaries are clear.
- [ ] Testing names exact commands and results.
- [ ] Risks and rollback are actionable.
- [ ] UI evidence covers the required states and viewports.
- [ ] No agent process narration or AI attribution appears anywhere.
- [ ] Every link and claim is verified.
