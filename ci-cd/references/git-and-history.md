# Git And History

Use this reference for commit creation, branch structure, pull requests, and
history cleanup.

Primary-source basis:

- Git `git-commit` and `git-rebase` docs for `--fixup`, `--autosquash`, and
  `rebase.autoSquash`
- GitHub docs for squash vs rebase merge tradeoffs and merge queue behavior
- DORA guidance for short-lived branches and trunk-based development

## Decision Rules

- Prefer one meaningful final commit per coherent change.
- Preserve multiple commits only when each commit is independently reviewable
  and the user wants that shape.
- Temporary local commits are fine. Published procedural commits are not.
- Never rewrite shared history without explicit user approval.
- Visible branch history is not automatically final history.
- If the history is local, procedural, and clearly compressible into one
  coherent fix, default to cleanup rather than preservation.

## Shared-History Check

Before rebasing or autosquashing, inspect:

- whether the branch has been pushed,
- whether other collaborators are using it,
- whether the user asked to preserve commit boundaries,
- whether the branch is a temporary cleanup branch or the intended long-lived
  feature branch.

Treat uncertain ownership as shared-history risk.

## Default Cleanup Flow

1. Inspect `git status`, `git log --oneline --decorate --graph -n <N>`, and
   `git diff --cached`.
2. Decide whether the work belongs in:
   - the current in-progress change,
   - a short-lived topic branch or worktree,
   - or a new logical commit series the user explicitly wants to preserve.
3. If the current branch is noisy and local, decide whether to branch out to a
   temporary cleanup branch before modifying history.
3. If the work is one coherent change:
   - stage only the intended files;
   - create fixup commits as needed while iterating;
   - fold them into the target commit with `git rebase -i --autosquash`.
4. Before publishing:
   - confirm the final diff is correct;
   - confirm the final commit title is concise and useful;
   - confirm no unrelated procedural commits remain;
   - record branch-state continuity if the work will continue later.

## Topic Branch Pattern

Use a short-lived topic branch or worktree when:

- the cleanup is risky,
- the branch already has unrelated work,
- or the branch should not expose procedural debugging history to later agents
  or reviewers.

Recommended pattern:

1. Branch from the intended base.
2. Commit freely while iterating.
3. Autosquash to the final useful commit.
4. Merge or fast-forward the cleaned result back to the target branch.
5. Delete the temporary branch when no longer needed.

## Autonomous Cleanup Default

Autonomous cleanup is appropriate when all of these are true:

- the branch is local or safely isolated;
- the user did not ask to preserve the visible commit trail;
- the commits clearly belong to one coherent outcome;
- cleaning history does not endanger another collaborator's work.

If any of these fail, downgrade from automatic cleanup to explicit warning or
user confirmation.

## Commit Message Format

Use Conventional Commits:

```text
type(scope): summary

Optional body that explains why, tradeoffs, or operational impact.
```

Examples:

- `feat(ci): add deployment smoke test gate`
- `fix(actions): pin checkout action to commit SHA`
- `docs(ci-cd): clarify fixup and autosquash workflow`

## Pull Request Expectations

- Keep the PR aligned to one coherent goal.
- Summarize user-facing or operator-facing impact.
- Call out rollout, rollback, and secret requirements when relevant.
- Prefer squash merge when the branch contains iterative repair commits or when
  the repo wants one useful final result.
- Preserve multiple commits only when the commit boundaries are meaningful and
  intentional.
- If the repo uses a merge queue, align your advice with the queue's merge
  method and required checks instead of assuming the contributor chooses merge
  style manually.

## Branch-State Handoff Minimum

When a later chat must resume Git work, record:

- current branch,
- intended base branch,
- branch purpose,
- whether the branch is temporary,
- whether history is cleaned,
- procedural commit count when relevant,
- safest next Git action.

## Anti-Patterns

- "wip", "misc fixes", or "address feedback" as final published commits.
- Creating a new commit when the right action is to amend or autosquash into
  the existing change.
- Rebasing or force-pushing a branch shared with others without approval.
- Mixing unrelated fixes just because the files were already open.
- Assuming `fix/api` or a similar branch name is the canonical feature branch
  without inspecting its actual purpose and base.
