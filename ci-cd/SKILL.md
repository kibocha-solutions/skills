---
name: ci-cd
description: >
  Plan, review, and implement Git workflow, commit cleanup, pull request
  hygiene, CI pipelines, deployment automation, release prep, rollback plans,
  and GitHub Actions security checks. Use whenever the user mentions commits,
  squash, fixup, autosquash, rebase, branches, pull requests, CI, CD,
  pipelines, releases, environments, rollback, deploys, GitHub Actions,
  merge queue, merge train, branch protection, OIDC, or history cleanup, even
  if they describe the need in casual Git terms rather than saying "CI/CD."
---

# CI/CD

## Goal

Help the user ship clean history, reliable automation, and auditable delivery
workflows without mixing repo-specific facts, generic folklore, stale
instruction bundles, and platform-specific habits presented as universal law.

Use this skill for workflow design, repo hygiene, CI troubleshooting,
deployment planning, release preparation, and delivery guardrails. When the
main deliverable is documentation, keep `documentation` prevalent for the
artifact itself and use this skill to supply the operational truth.

## Default Procedure

1. Classify the request before acting. Use:
   - `references/git-and-history.md` for commits, branches, PRs, rebases,
     squashing, and publish-ready history.
   - `references/pipelines-and-deployments.md` for CI architecture, deployment
     flow, environments, releases, and rollback.
   - `references/security-and-operations.md` for GitHub Actions security,
     secrets, branch protection, artifacts, and emergency change handling.
   - `references/integration-controls.md` for merge queues, merge trains,
     merged-results style validation, and high-throughput branch controls.
   - `references/authoritative-sources.md` when a claim depends on an external
     standard or platform behavior and needs primary-source grounding.
   - `examples/` when the user would benefit from a concrete branch-cleanup or
     deployment-hardening pattern rather than abstract guidance alone.
2. Inspect repo truth first:
   - Git state: `git status`, branch shape, remotes, protected-history risk.
   - Branch intent: current branch, intended base branch, whether the branch is
     temporary, whether it has been published, and whether local history is
     still procedural.
   - Automation surface: `.github/workflows/`, build scripts, test commands,
     release scripts, deployment manifests.
   - Environment assumptions: required secrets, artifact stores, runners,
     target platforms, rollback hooks.
3. Decide whether the task is primarily:
   - history cleanup,
   - collaboration workflow,
   - CI pipeline change,
   - deployment or release design,
   - security hardening,
   - incident repair.
4. Keep the workflow proportional to the task. A single commit cleanup does not
   need a full release checklist. A production deployment change does.
5. When documentation is part of the deliverable, route prose, guides, and
   readers' structure through the `documentation` skill after the technical
   workflow is settled.
6. Before handing off CI/CD work, record branch-state continuity when history,
   rebasing, temporary branches, or publish readiness matters.

## Hard Rules

- Do not create no-useful-work commits.
- Prefer one meaningful final commit per coherent change unless the user
  explicitly wants several logical commits preserved.
- Temporary local fixup commits are allowed. Clean them up before publishing,
  review handoff, or final delivery.
- Treat many local repair commits after the real change as a cleanup signal.
- When the history is local, procedural, and clearly compressible into one
  coherent change, autonomously isolate or clean it up by default.
- Do not rewrite shared, pushed-for-collaboration, or user-authored history
  without explicit user approval.
- Stage intentionally. Inspect `git status` and `git diff --cached` before each
  commit.
- Do not guess at pipeline behavior when local workflow files, scripts, or
  release tooling can answer the question.
- Keep a single auditable path to production. Avoid undocumented manual deploy
  paths except for explicit emergency procedures.
- Treat secrets, tokens, signing material, and deployment credentials as
  operational risks first and convenience issues second.
- If branch protection, required checks, or permissions are absent, say so
  plainly and propose the narrowest safe guardrail that fits the repo.

## Shared-History Danger Gate

Before recommending rebase, autosquash, or force-push, classify the branch:

| Branch state | Default action |
| --- | --- |
| Local-only procedural branch | Clean up autonomously if the history clearly belongs to one coherent change. |
| Temporary topic branch not yet shared | Clean up before publish or merge back to the intended base. |
| Pushed branch used only by the current agent and not yet reviewed | Clean up only if the user has not signaled that preserving the visible commits matters. |
| Shared or collaboratively used branch | Do not silently rewrite history. Recommend safer alternatives or ask first. |

If branch ownership or push status is unclear, treat the branch as shared until
inspection proves otherwise.

## Autonomous History Cleanup

Use this workflow when the branch is local or safely isolated and the visible
history is clearly procedural:

1. Confirm the intended base branch and whether the current branch is temporary
   or publishable.
2. Decide whether to:
   - clean the current local branch,
   - branch out to a temporary cleanup branch,
   - or open a separate worktree for risky repair.
3. Use `git commit --fixup` for incremental repairs to the intended final
   commit.
4. Use `git rebase -i --autosquash` to fold fixups into one useful commit.
5. Verify the final diff, final commit title, and whether the branch is now
   ready to publish or merge back.
6. Record the cleanup state in the handoff whenever the work will continue in a
   later chat.

## Branch, Merge, And Cleanup Decisions

| Situation | Preferred branch strategy | Preferred history strategy | Notes |
| --- | --- | --- | --- |
| Small coherent fix, local history only | Stay on branch or use a cleanup branch | Autosquash to one final commit | Default autonomous cleanup case |
| Risky debug session with many exploratory edits | Short-lived topic branch or worktree | Autosquash before merge back | Preserves the feature branch signal |
| Shared branch with multiple collaborators | Avoid hidden branch surgery | Preserve or coordinate cleanup explicitly | Safety over neatness |
| Busy protected branch with many PRs | Short-lived PR branches | Use repo-approved merge method plus queue or train controls | Optimize for integration safety |

## Integration And Release Controls

Use queueing or merged-result validation when branch traffic is high enough
that rebasing every PR manually becomes noisy or risky.

| Control | Use when | Main tradeoff |
| --- | --- | --- |
| Squash merge | Review history should keep one useful result and discard repair chatter | Loses per-commit detail |
| Rebase merge | Commit boundaries are meaningful and the repo allows it | Rewrites commit SHAs and may complicate signatures |
| Merge queue | A protected branch has many ready PRs and you need combined-check validation without repeated manual updates | Merge method is controlled by the queue |
| Merge train or merged-results style validation | Busy integration branch needs proof that combined branch state works before merge | Requires extra CI capacity and platform support |

## Handoff Branch-State Recording

When branch or history state matters, include:

- current branch;
- intended base branch;
- branch purpose;
- whether the branch is temporary or meant to survive;
- whether history is cleaned yet;
- approximate procedural commit count when relevant;
- the safest next Git action.

Example:

```text
Current branch: fix/api
Intended base branch: feat/docs
Branch purpose: temporary debug cleanup
History cleaned yet: no
Procedural commits since branch-off: 14
Safe next Git action: autosquash locally, then merge back to feat/docs
```

## Standard Outputs

### Commit Or History Guidance

Provide:

- the intended final commit shape,
- whether autonomous cleanup is appropriate,
- whether the visible history is publish-ready,
- whether to squash or preserve multiple commits,
- the safe cleanup method,
- any history-rewrite risk,
- the final commit title pattern when a commit is needed.

### Pipeline Or Deployment Guidance

Provide:

- the current state,
- the target workflow,
- the gating checks,
- the rollout and rollback path,
- the security or operability risks,
- the smallest safe implementation order.

### CI Review Or Incident Response

Provide:

- the failing stage or workflow,
- the likely cause,
- the confirming evidence to inspect,
- the smallest repair,
- the regression checks,
- whether a revert is safer than a forward fix.

## Commit Hygiene Expectations

- Use Conventional Commits for final commit titles:
  `type(scope): summary`
- Keep the subject concise and imperative.
- Use the commit body for intent, tradeoffs, or risk, not for a raw file list.
- If several commits were required locally, prefer `--fixup` plus
  `rebase -i --autosquash` over leaving behind a trail of repair commits.
- If a cleanup is distinct enough to isolate, create a short-lived topic branch
  or worktree, clean it there, merge or fast-forward the useful result back,
  then delete the temporary branch.
- If the user's branch already contains unrelated work, avoid rewriting their
  commits unless they explicitly ask for it.

## CI/CD Operating Model

- Prefer short-lived branches, continuous testing, and deployment automation as
  the default shape of a healthy delivery system.
- Prefer build-once or artifact-once promotion where the platform supports it.
- Prefer immutable deployment artifacts across environments.
- Prefer explicit environment gates and rollback criteria over optimistic
  production deploys.
- Prefer queueing or merged-result validation on high-throughput branches over
  repeated ad hoc rebases.
- Prefer least-privilege credentials, pinned workflow dependencies, and OIDC
  over long-lived deployment secrets.
- Prefer revert-first incident handling when the root cause is still uncertain.

## Bundled Resources

- `references/git-and-history.md`: clean commit creation, branching, rebasing,
  and PR-ready history.
- `references/pipelines-and-deployments.md`: CI/CD architecture, deployment
  models, environments, release flow, rollback.
- `references/security-and-operations.md`: GitHub Actions security, secrets,
  branch protection, artifacts, and emergency changes.
- `references/integration-controls.md`: merge queues, merge trains,
  merged-results style validation, and linear-history tradeoffs.
- `references/authoritative-sources.md`: primary-source notes and URLs backing
  the normative guidance in this skill.
- `assets/commit-message-template.md`: compact commit title and body template.
- `examples/branch-cleanup-and-handoff.md`: concrete branch-out, autosquash,
  and handoff continuity example.
- `examples/deployment-hardening-example.md`: concrete CI/CD hardening example
  covering gates, rollback, and Actions security.
