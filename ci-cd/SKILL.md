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

## Repo Health Pre-Flight

At the start of any commit, branch, or push task — and after any branch switch
the agent itself performs — run a structured health pass and cache the results.
Do not re-parse the repo from scratch on every invocation; read the cache and
validate only the fields that may have changed.

Treat Git operations as authorization-sensitive by default. Any command that
invokes `git`, provider CLIs such as `gh` or `glab`, remote authentication, or
repo-local writes outside the active sandbox root should request elevated
authorization before running. Do not first attempt the Git command in the
sandbox and then retry after a predictable sandbox failure.

**What to collect and cache** (see `references/repo-health-cache.md` for the
full schema and staleness rules):

- Recent commit pattern from at least two full commit records, collected with
  signature, full author and committer dates, subject, and body. Use
  `git log --show-signature -2 --date=iso-strict --format=fuller` as the
  minimum evidence set. A one-line log is not enough for repo health because
  it hides bodies, dates, authorship details, and signature status that the
  agent needs before it creates or amends commits.
- User identity from `git config user.name` and `git config user.email` —
  required before any commit; halt if either is absent and ask the user to
  configure them first.
- Remote connectivity — whether `git remote -v` shows a configured remote and
  whether `ssh -T git@<host>` returns a successful authentication handshake.
- Provider CLI availability and authentication for the remote host. For GitHub,
  record whether `gh` exists and whether `gh auth status` succeeds. For GitLab,
  record whether `glab` exists and whether its auth status check succeeds.
  Prefer the authenticated provider CLI for provider-native push, pull request,
  and review operations when it is available and appropriate for the task.
- Signing configuration from `git config gpg.format`, `git config user.signingkey`,
  and `git config gpg.ssh.allowedSignersFile` — the default assumption is that
  signing is expected; the absence of signing config triggers a pre-commit
  clarification prompt rather than a silent unsigned commit.
- SSH and signing path evidence before any repair or setup. Inspect
  `core.sshCommand`, `gpg.ssh.program`, `SSH_AUTH_SOCK`, available Windows
  OpenSSH binaries, `op-ssh-sign-wsl.exe`, and relevant SSH config files. Do
  not repair SSH from a single failing `ssh-add` result. Use the `ssh` skill
  for SSH agent, host alias, key, and signing setup.
- Default Git identity from the active repo-health cache. Treat
  `identity.user_name` and `identity.user_email` as the default identity for
  the repo. If the cache is absent, stale, or missing identity fields, refresh
  it before deciding which SSH host, key, or signing path belongs to the repo.

**Cache location:** `.agents/brain/git/repo-health.json` in the project root.
When a snapshot becomes stale, archive it to `.agents/brain/git/archives/`
before writing a fresh one. Read `references/repo-health-cache.md` for the
exact schema, archive naming, and staleness triggers.

**When to invalidate:** after any branch switch this agent performs, after a
remote is added or removed, or after any change to `.ssh/config` or signing
configuration made during the current session.

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
   - The `ssh` skill when the work requires SSH authentication, SSH signing,
     SSH host aliases, password-manager SSH agents, or production SSH access.
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
- For SSH key generation, password-manager SSH agents, host aliases, and SSH
  signing setup, use the `ssh` skill. CI/CD work may collect and cache SSH
  evidence, but the SSH skill owns configuration and repair procedures.
- Treat `git@github.com:owner/repo.git` as belonging to the repo's default
  cached identity. When the repo identity differs from that default, or the
  user requests or strictly implies a different GitHub identity, use the `ssh`
  skill to select or verify an SSH host alias before pushing.

## Commit Attempt Discipline

Apply this protocol whenever the agent attempts a `git commit` or `git push`.

**Attempt ceiling:** make at most 3 attempts per logical change. After 3
failures, stop completely — do not retry with a different strategy, do not
modify signing configuration, and do not produce an unsigned commit to work
around the problem.

**Before each attempt:**

1. Read the cached signing config and identity from
   `.agents/brain/git/repo-health.json`. If signing is configured and
   expected, confirm the active SSH signing path from cached evidence before
   repair. Use `references/ssh-signing-relay.md` as the CI/CD bridge and the
   `ssh` skill for the provider-specific procedure.
   - If the active SSH path exposes keys successfully: proceed to step 2.
   - If the path is unclear: ask the user which agent owns the key before
     changing sockets, aliases, signing config, or remotes.
   - If signing config is absent but was previously expected: ask the user
     whether this is intentional before proceeding. Record the answer
     (`signing_intentionally_disabled: true/false`) in the cache. The agent
     never sets this field to `true` unilaterally.
2. Confirm `user.name` and `user.email` are set. If either is missing, halt
   and tell the user exactly which config command to run; do not attempt the
   commit without them.

**On each failure, triage in this order before the next attempt:**

1. **SSH agent reachability and identity path** — identify the active path from
   repo-health, Git config, environment variables, and installed tools before
   repair. Use the `ssh` skill procedure that matches the evidence.
2. **Git signing configuration** — confirm `gpg.format`, `user.signingkey`, and
   (for SSH) `gpg.ssh.allowedSignersFile` are present and consistent. If
   `allowedSignersFile` is absent, create or refresh it through the matching
   procedure in the `ssh` skill.
3. **Remote connectivity and host alias** — inspect the remote URL before
   testing. If the repo uses a non-default identity, test the configured alias
   (`ssh -T git@alias`) and do not substitute `git@github.com`.
4. **Everything else** — capture the exact error text, include it in the halt
   message, and ask the user to inspect it.

**After 3 failed attempts:**

- If the SSH agent was identified as the culprit at any point: halt and ask
  the user to unlock, approve, or load the key in the active agent path
  identified from repo-health and config evidence, then retry from scratch.
- If the SSH agent was not the culprit: halt with a full diagnostic summary
  (triage results from each of the 3 attempts) and do not speculate about the
  cause beyond what the evidence supports.

**What the agent must never do under any failure condition:**

- Remove, override, or bypass SSH signing configuration.
- Commit without a signature when signing is configured and the user has not
  explicitly confirmed this is intentional for the current session.
- Retry silently without reading the failure reason first.

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

- Use Conventional Commits for final commit titles: `type(scope): summary`.
  Match the existing repo commit style only where it does not conflict with
  this format; when there is a conflict, Conventional Commits takes precedence.
- **Scope is the specific unit of change — the skill, module, component, or
  package — not a broad repo-level area.** In a skills repository, scope is
  the skill name. In an application, scope is the affected package or layer.
  When a single commit spans multiple units, list them:
  `feat(graphify, ci-cd): ...`. Avoid generic scopes like `repo`, `skills`,
  or `misc` that carry no useful signal about where the change lives.

  Examples from this repo's convention:
  - `feat(graphify): add 4-stage MCP orchestration lifecycle` — new skill added
  - `fix(ci-cd): tighten relay startup triage in commit discipline` — targeted
    fix to a specific part of an existing skill
  - `feat(graphify, ci-cd): add graphify skill and expand ci-cd discipline` — one
    commit that ships a new skill alongside meaningful updates to another
  - `chore(repo): bootstrap skills repository scaffold` — the rare case where
    the change truly is repo-level infrastructure (scaffolding, CI, `.gitignore`)
    and no single skill is the primary unit of change

- Keep the subject line concise and imperative; the subject is not the place
  for tradeoffs, rationale, or extended context.
- Keep commit and PR messages anchored to the core repo-relevant change. The
  durable message should identify the feature, fix, refactor, documentation
  update, workflow change, or operational improvement that future maintainers
  will care about. Do not include unrelated workspace conditions, submodule
  state, sandbox mechanics, local tooling trivia, or incidental punctuation and
  cleanup details unless the user explicitly asks for those details to appear
  in the message.
- **Include a commit body. It is not optional.** Explain the intent of the
  change, any meaningful tradeoff, or the operational impact. Do not use the
  body to list files changed — the diff does that. Keep each line in the body
  at or below 72 characters. Tone and prose standards from the documentation
  skill apply here; do not use inflated language, circular phrasing, or
  unnecessary filler.
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
- `references/repo-health-cache.md`: brain cache schema for repo health
  snapshots, staleness triggers, archive rules, and field definitions.
- `references/ssh-signing-relay.md`: SSH identity and signing path selection
  for Bitwarden Desktop, 1Password, local keys, host aliases, verification
  steps, and failure-mode diagnostics.
- `references/pull-request-messages.md`: production-grade pull request
  description standards — required sections, title format, tone rules,
  formatting guidance, and prohibited patterns.
- `assets/commit-message-template.md`: compact commit title and body template.
- `examples/branch-cleanup-and-handoff.md`: concrete branch-out, autosquash,
  and handoff continuity example.
- `examples/deployment-hardening-example.md`: concrete CI/CD hardening example
  covering gates, rollback, and Actions security.
