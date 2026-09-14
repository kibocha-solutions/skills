# Git and History

## Procedure

1. Inspect `git status`, the staged diff, and recent full commits.
2. Resolve the current branch, trunk, upstream, and branch ancestry.
3. Determine whether the branch or commits are shared.
4. Preserve shared history.
5. Use a short-lived topic branch or worktree for isolated work.
6. Create temporary local commits only when they support safe iteration.
7. Convert repair commits into fixup commits when appropriate.
8. Run interactive autosquash only on unshared history.
9. Verify the final diff and commit sequence.
10. Publish only when the user requests publication.

## History gates

- Never rewrite shared history without live user approval.
- Never force-push without live user approval.
- Never delete a collaborator-used branch without live user approval.
- Treat uncertain ownership as shared.
- Preserve commit boundaries the user requests.
- Keep one coherent final commit when independent boundaries add no review value.

## Branch procedure

1. Discover the intended base from repository evidence.
2. Create the topic branch from that base.
3. Record the branch and parent in the repository ancestry log when the project uses one.
4. Commit during implementation as needed.
5. Mark repairs with `git commit --fixup=<commit>`.
6. Run `git rebase -i --autosquash <base>` only after the shared-history check passes.
7. Recheck the resulting tree and history.
8. Merge or hand off one ancestry level at a time.
9. Delete a temporary branch only after its work is preserved and its ownership is resolved.

## Final commit

1. Execute section 6 of `../SKILL.md`.
2. Use `../assets/commit-message-template.md`.
3. Verify the delivered commit count from the recorded starting commit.
4. Verify the exact final message before publication.

## Pull request checks

- Keep one coherent goal.
- State user or operator impact.
- State material implementation boundaries.
- List exact tests and results.
- State material risks and the rollback command or procedure.
- Follow the repository merge method and merge queue.
- Preserve multiple commits only when their boundaries are intentional and useful.

## Handoff fields

Record:

- current branch
- intended base
- branch purpose
- shared or isolated status
- temporary or durable status
- history-cleanup status
- safest next Git action

## Prohibited outcomes

- Final commits named `wip`, `misc fixes`, or `address feedback`
- Commit messages that narrate the work session
- New commits that should have been fixups
- Unapproved shared-history rewrites
- Unrelated changes in one commit
- Ancestry assumptions based only on a branch name
