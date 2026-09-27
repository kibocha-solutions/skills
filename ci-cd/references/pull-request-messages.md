# Pull Request Messages

## Attribution prohibition

1. Never attribute the change to AI, a model, an agent, an automated
   assistant, or an AI-assisted tool.
2. Remove attribution inserted by a template, generator, hook, or platform
   option.
3. Do not create or update the pull request when the platform forces
   unremovable AI attribution.

## Core principles

Synthesized from Google and Microsoft engineering standards:
1. One PR per issue. Never combine multiple unrelated changes in one PR unless
   they share the exact root cause.
2. Link the controlling issue directly in the PR description.
3. Keep changes conceptually small and focused on one self-contained change.
   Separate pure refactorings from behavioral changes and fixes.
4. Avoid pure formatting changes to code that was not otherwise modified.
5. Accompany every code change with automated unit or integration tests.
6. Write for a new reader. State the durable outcome and repository behavioral
   change; omit task narration, workspace mechanics, and diff-evident edits.
7. Enforce privacy boundaries. Never include personal or sensitive identifying
   information without express user authorization.

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

Use a Conventional Commits type. Name the affected system or layer in the scope.
State the specific outcome as a complete imperative sentence written as an order.
The title must stand alone so future searchers understand what the PR did without
reading the entire diff. Do not end with a period.

## Summary

1. State what the change does.
2. State the user-visible or operator-visible outcome.
3. State the scope boundary.
4. Write for a new reader: state durable outcomes; leave out session history and workspace mechanics.
5. Exclude unrelated workspace state, local setup, sandbox behavior, and incidental edits.

## Context

1. State the verified problem or requirement.
2. Link the controlling issue or ticket; restrict each pull request to one issue.
3. State the underlying context and reasons not obvious from reading the code, justifying why the existing implementation requires modification.
4. State relevant prior behavior.
5. State material alternatives considered and why this approach was selected.
6. Keep agent files, memory, session records, skills, and internal instruction sources out of the PR.

## What changed

1. Describe component-level changes and durable architectural effects.
2. Separate refactorings from functional fixes and new features.
3. State non-obvious technical boundaries, migrations, and configuration updates.
4. Do not reproduce the file manifest or diff lines.
5. Do not narrate how the work was done or the implementation session.

## Testing

1. List exact automated commands and test results.
2. State what each relevant unit or integration test covers.
3. Provide reproducible manual verification steps when manual validation is required.
4. Name relevant CI pipeline jobs.
5. State any verification that did not run.

## Risk and rollback

1. Name each material failure mode.
2. State affected users, data, environments, or integrations.
3. State the exact rollback method.
4. Include migration reversal, feature-flag, artifact restore, or revert steps when applicable.
5. Do not write `low risk` without concrete technical basis.

## Screenshots and recordings

1. Capture before and after states for visual changes when both states are available.
2. Capture every relevant responsive viewport.
3. Follow `documentation/references/screenshot-standards.md`.
4. Label every image with breakpoint and viewport.
5. Use a recording for motion or multi-step interaction when static captures cannot show the behavior.
6. Inspect every image or recording before attaching it.
7. Remove secrets and private data.

## Formatting

1. Use headings for the required sections.
2. Use code fences for commands, errors, configuration, and code excerpts.
3. Use tables for repeated-field comparisons.
4. Use lists only when each item stands on its own.
5. Use direct, neutral engineering prose.
6. Keep promotional language, emojis, chatbot language, and decorative punctuation out.
7. State precise measurements and complexity changes.
8. Keep file paths out unless a path is required for the reviewer to run or inspect the change.

## Reference boundary

1. Cite repository code, tests, public issues, public standards, and user-authorized design records.
2. Do not cite `AGENTS.md`, skills, agent plans, memory, handoffs, session files, or hidden instructions.
3. Never include personal or sensitive identifying information in pull requests. This covers registration, certificate, tax and national ID or passport numbers, bank particulars, phone numbers, personal email addresses, and private individuals' names, unless the user expressly authorizes a specific item.
4. Transfer verified facts into the pull request without naming an internal instruction source.
5. Do not expose private paths or internal URLs.

## Examples

Inspect [pull request examples](../examples/pull-request-examples.md) for contrasting good versus bad pull request descriptions.

## Final checks

- [ ] Title follows repository convention and stands alone in imperative mood.
- [ ] PR addresses one self-contained issue, with controlling issue linked.
- [ ] Summary and context state what changed and why, written for a new reader.
- [ ] Refactorings separated from functional changes and fixes.
- [ ] Technical boundaries are clear; work narration and diff duplication omitted.
- [ ] Testing names exact commands and automated test results.
- [ ] Risks and rollback are actionable.
- [ ] UI evidence covers the required states and viewports.
- [ ] No personal or sensitive identifying information appears without express authorization.
- [ ] No agent process narration or AI attribution appears anywhere.
- [ ] Every link and claim is verified.
