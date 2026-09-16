---
name: ci-cd
description: Plan, review, and implement Git workflows, commit cleanup, branches, pull requests, CI pipelines, deployment automation, release preparation, rollback, merge queues, branch protection, OIDC, GitHub Actions security, and history repair. Use whenever a request mentions commits, squash, fixup, autosquash, rebase, branches, pull requests, CI, CD, pipelines, releases, environments, rollback, deployment, merge trains, signing, or history cleanup.
---

# CI/CD

## 1. Classify the task

1. Identify the repository, requested action, intended result, and publication
   boundary.
2. Read the matching references:
   - Git and history: `references/git-and-history.md`
   - pipelines and deployment: `references/pipelines-and-deployments.md`
   - security and operations: `references/security-and-operations.md`
   - integration controls: `references/integration-controls.md`
   - external standards: `references/authoritative-sources.md`
   - repository health: `references/repo-health-cache.md`
   - pull request text: `references/pull-request-messages.md`
   - SSH signing bridge: `references/ssh-signing-relay.md`
3. Activate `ssh/SKILL.md` for SSH authentication, agents, keys, aliases,
   signing configuration, bastions, or production access.
4. Activate `documentation/SKILL.md` for a documentation deliverable.
5. Inspect `examples/` only when a concrete implementation pattern is
   required.

## Absolute AI-attribution prohibition

1. Never attribute repository work to AI, a model, an agent, an automated
   assistant, or an AI-assisted tool.
2. Apply the prohibition to commits, author fields, co-author trailers,
   signatures, pull requests, issues, review comments, tags, release notes,
   changelogs, deployment records, generated-by fields, and publication
   metadata.
3. Remove optional AI attribution inserted by a template, tool, hook, or
   generator before publication.
4. Do not replace explicit attribution with coded, abbreviated, indirect, or
   euphemistic attribution.
5. If a platform forces attribution that cannot be removed, do not publish
   through that path. Report the platform requirement to the user.

## 2. Build the repository-health snapshot

1. Read `.agents/brain/git/repo-health.json` when present.
2. Apply the staleness rules in `references/repo-health-cache.md`.
3. Archive a stale snapshot under `.agents/brain/git/archives/`.
4. Collect at least two complete commit records:

```bash
git log --show-signature -2 --date=iso-strict --format=fuller
```

5. Collect:
   - `git status`
   - current branch
   - configured upstream
   - local and remote branches
   - `git remote -v`
   - `git config user.name`
   - `git config user.email`
   - `git config gpg.format`
   - `git config user.signingkey`
   - `git config gpg.ssh.allowedSignersFile`
   - `git config core.sshCommand`
   - `git config gpg.ssh.program`
   - `SSH_AUTH_SOCK`
6. Check the provider CLI and authentication for the remote host.
7. Test the configured SSH host or alias.
8. Store the refreshed snapshot at
   `.agents/brain/git/repo-health.json`.
9. Invalidate the snapshot after a branch switch, remote change, SSH
   configuration change, or signing configuration change.

## 3. Resolve branch ancestry

1. Read `.agents/brain/git/branch-ancestry.json`.
2. Use an existing entry for the current branch when valid.
3. Otherwise inspect, in order:
   - the branch creation entry in its reflog
   - its configured upstream
   - `git merge-base --fork-point` against candidate branches
4. Ask the user when no source resolves the parent unambiguously.
5. Append the resolved ancestry to the durable log.
6. Append an entry immediately after creating a branch.
7. Never overwrite or archive the ancestry log.

## 4. Inspect the delivery surface

1. Inspect the staged and unstaged diff.
2. Inspect workflow files, build scripts, test commands, release scripts,
   deployment manifests, runner configuration, environment gates, artifact
   stores, secrets interfaces, and rollback hooks.
3. Identify protected or shared history.
4. Identify the current branch, intended base, publication state, review state,
   and collaborator use.
5. Identify required checks and release gates.
6. Stop when the requested mutation lacks authorization.

## 5. Select the workflow

Choose the matching path:

- commit creation or amendment
- local history cleanup
- shared branch collaboration
- pull request preparation
- CI repair
- pipeline design
- deployment or release
- security hardening
- incident rollback
- merge queue or merge train

Keep the steps limited to the selected path.

## 6. Create a final commit

1. Confirm that `user.name` and `user.email` are set.
2. Confirm the expected signing configuration.
3. Ask the user when signing was previously expected and is now absent.
4. Record `signing_intentionally_disabled` only from the user's answer.
5. Record the starting commit before creating any commit.
6. Determine the final commit count authorized by the user.
7. Treat that count as an absolute maximum and the required delivered count
   when there are changes to commit.
8. Use one final commit when the user does not specify a count.
9. Never create an extra final commit for a secondary task, cleanup,
   validation record, generated artifact, or session record.
10. When one final commit is authorized, include the entire intended change set
    in that one commit.
11. Stage only the intended files.
12. Inspect:

```bash
git status --short
git diff --cached
```

13. Select one predominant durable purpose for the complete staged change set.
14. Use that purpose for one type, one scope, and one subject.
15. Do not assign a separate subject, sentence, paragraph, or bullet to each
    completed task.
16. Use `assets/commit-message-template.md` for the template and accepted and
    rejected examples.
17. Write the title as `type(scope): summary`.
18. Use one canonical type:
   - `feat`
   - `fix`
   - `docs`
   - `style`
   - `refactor`
   - `perf`
   - `test`
   - `build`
   - `ci`
   - `chore`
   - `revert`
19. Use one specific scope.
20. Use `repo` only for repository infrastructure with no specific component
    at its center.
21. Write a concise imperative subject without a trailing period.
22. Use one optional prose paragraph for the body.
23. Keep the body at 72 words or fewer unless the user sets a stricter limit.
24. Obey every user-specified word, character, line, title, body, or total
    message limit exactly.
25. Never use bullets, numbered lists, headings, checklists, or tables in a
    commit message.
26. Never put filenames, directory names, repository paths, or line references
    in a commit message.
27. Omit task-by-task summaries, file lists, process narration, workspace
    mechanics, and unnecessary implementation detail.
28. Mention secondary work only when it materially changes the durable purpose.
29. Condense that secondary work into the same prose paragraph.
30. Do not split the final history solely because the change set contains
    several tasks or strands.
31. Do not create temporary or fixup commits when they would cause the
    delivered history to exceed the authorized count.
32. Inspect the exact final message with:

```bash
git log -1 --format=%B
```

33. Count commits from the recorded starting commit to `HEAD`.
34. Stop before pushing when the count or message violates any rule above.

## 7. Enforce the publication boundary

Never name, cite, quote, or attribute any of these in a commit message, pull
request description, or issue:

- `AGENTS.md`
- skills or skill instructions
- implementation plans
- task registers
- walkthroughs
- memory files
- handoffs
- sessions
- chat instructions
- temporary or scaffolding files
- internal drafting guidance

State the verified repository fact without citing an excluded source. Use
durable code, documentation, schemas, tickets, or external standards when a
citation is required.

Apply the absolute AI-attribution prohibition to every publication surface.

## 8. Handle commit and push failures

1. Make no more than three attempts per logical change.
2. Read the exact failure before each retry.
3. Triage in this order:
   - SSH agent reachability and identity path
   - Git signing configuration
   - remote connectivity and configured host alias
   - remaining exact error
4. Use the cached repository identity as the default identity.
5. Use `ssh/SKILL.md` for every SSH repair.
6. Never substitute `git@github.com` for a configured non-default alias.
7. Never remove, override, or bypass signing configuration.
8. Never create an unsigned commit when signing is expected without live user
   authorization.
9. Stop after the third failure.
10. Report all three attempts and triage results.
11. Ask the user to unlock, approve, or load the identified key when the SSH
    agent blocks the operation.

## 9. Clean local history

1. Confirm the intended base and current branch ownership.
2. Treat unclear ownership or publication state as shared.
3. Use a disposable branch or worktree for risky cleanup.
4. Use `git commit --fixup` for repair commits.
5. Use `git rebase -i --autosquash` to produce the intended final history.
6. Rebase onto the latest parent before shipping.
7. Verify the final diff and final commit.
8. Advance one level at a time through the recorded ancestry chain.
9. Apply each level's merge and review requirements.
10. Obtain live confirmation before rewriting shared or reviewed history.
11. Obtain live confirmation before deleting a shared, reviewed, published, or
    ambiguously owned branch.
12. Delete a confirmed local disposable branch only after its work lands at the
    next ancestry level.
13. Record the final ancestry and cleanup state.

## 10. Prepare a pull request

1. Read `references/pull-request-messages.md`.
2. Inspect the complete diff and commit range.
3. Verify required tests and checks.
4. Use the repository's pull request template.
5. State the change, verification, operational impact, rollout, and rollback
   information required by the template.
6. Keep excluded internal sources out of the title and description.
7. Use the authenticated provider CLI when authorized and available.
8. Verify the created pull request and its checks.

## 11. Implement CI, deployment, or release work

1. Read the matching pipeline, security, and integration references.
2. Define the current state and target flow.
3. Use one auditable production path.
4. Build an artifact once and promote the same immutable artifact.
5. Define required tests, approvals, environment gates, rollout criteria,
   rollback criteria, and observability checks.
6. Use least-privilege credentials.
7. Prefer OIDC to long-lived deployment secrets.
8. Pin workflow dependencies.
9. Use merge queues or merged-result validation for high-throughput protected
   branches.
10. Use the repository-approved merge method.
11. Use revert-first incident handling while the cause remains unresolved.
12. Verify the rollback path before release.
13. Run the pipeline and inspect the exact final result.

## 12. Record handoff state

Record these fields when work continues in another session:

- current branch
- intended base branch
- branch purpose
- branch lifetime
- publication and review state
- history cleanup state
- procedural commit count when relevant
- required checks
- safest next Git action

## 13. Verify completion

1. Reinspect `git status`.
2. Reinspect the final diff or commit.
3. Verify signatures when required.
4. Verify remote state after a push.
5. Verify pull request checks after creation or update.
6. Verify pipeline, deployment, release, and rollback results against the exact
   run and artifact.
7. Update the repository-health cache when its fields changed.
8. Report the completed action, checks, warnings, and remaining blockers.

## 14. Pre-completion checklist

- [ ] Repository health snapshot refreshed and verified.
- [ ] Staged change set matches single predominant purpose.
- [ ] Commit message conforms to `type(scope): summary` and <= 72 words in one prose paragraph.
- [ ] No bullets, numbered lists, file paths, or line numbers in commit message.
- [ ] Zero AI attribution across commits, author fields, PR text, release notes, or tags.
- [ ] No U+2014 em dashes in normal prose.
- [ ] Verification commands passed against exact final commit.

