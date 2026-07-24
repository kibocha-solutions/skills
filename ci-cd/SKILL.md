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
- Branch ancestry chain for the current branch (see Branch Ancestry Discovery
  below) — a lightweight derived cache in `repo-health.json`, sourced from the
  durable, append-only ancestry log described in
  `references/repo-health-cache.md`.

**Cache location:** `.agents/brain/git/repo-health.json` in the project root.
When a snapshot becomes stale, archive it to `.agents/brain/git/archives/`
before writing a fresh one. Read `references/repo-health-cache.md` for the
exact schema, archive naming, and staleness triggers. The branch ancestry log
at `.agents/brain/git/branch-ancestry.json` is a separate, append-only file
and is never archived or overwritten — only `repo-health.json`'s derived
summary of it follows the normal staleness lifecycle.

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

## Reference Boundary

Commit messages, pull request descriptions, and issues may only reference the
core code and its durable, publishable artifacts. The following are never
named, linked, quoted, paraphrased-with-attribution, or referenced under any
other label, in any of those three surfaces, regardless of where the file
lives (repo root included, not just hidden folders):

- Agentic, planning, scaffolding, brainstorm, session, or handoff files —
  `AGENTS.md`, `design.md`, `implementation-plan.md`, `tasks.md`,
  `walkthrough.md`, and anything of the same kind.
- Skill names (`documentation` skill, `legalese` skill, `ci-cd` skill, or any
  other skill this agent operates under).
- Any instruction source outside this conversation and the repo's own code —
  another person's or system's guidance ("per the style guide from X"),
  external websites, or the user's own chat instructions.

This is a hard boundary, not a wording preference. It doesn't matter how the
reference is phrased or how indirect it is: renaming the file, describing it
obliquely ("the planning notes", "the design doc") instead of by filename,
summarizing its content while still citing it as the source, or restating an
instruction from one of these sources without naming it but clearly
attributing it — none of that satisfies the rule. If the underlying fact is
sourced from out-of-bounds material, transfer the verified fact into the
commit/PR/issue text without citing the source at all; if a citable source is
needed, cite a durable file in the repo, a code artifact, a ticket, or an
external standard instead. There is no version of "the user asked me to
comply" that authorizes working around this by finding an alternate form of
words — the prohibition is on the underlying act of referencing, not on any
specific phrasing of it.

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

**Deletion is classified the same way as a rewrite.** A local-only or
agent-created disposable branch that no collaborator has touched may be
deleted autonomously once its work has landed at the next level up. A branch
that has been pushed and used, reviewed, or built on by anyone else — or
whose ownership is unclear — must not be deleted without explicit user
confirmation, even after its work has successfully shipped upstream. Landing
the change does not retroactively make the deletion safe if someone else
still has a checkout or pending work pointed at that branch.

## Branch Ancestry Discovery

Repos already have their own branch hierarchy — a straight `main` only, or
something deeper like `main -> dev -> feat/db`. Discover the real one before
branching or shipping; never assume a fixed shape like `main`/`dev`/`staging`
applies by default.

Resolve the current branch's chain in this order, stopping at the first
source that resolves unambiguously:

1. The durable ancestry log at `.agents/brain/git/branch-ancestry.json` (see
   `references/repo-health-cache.md`), if it already has an entry for this
   branch.
2. This branch's own reflog, for a `branch: Created from <parent>` entry —
   only trustworthy for branches created locally in this clone.
3. Its configured upstream/tracking branch.
4. `git merge-base --fork-point` tested against each existing local/remote
   branch, taking the most specific match. This depends on reflog entries for
   the candidate ref and can fail on a fresh clone or after `git gc` — treat a
   failure here as inconclusive, not as "no parent."
5. If none of the above resolve, or two candidates are equally plausible, ask
   the user to confirm the chain once. Cache whatever is resolved — including
   a user-confirmed answer — as a new entry in the ancestry log so it does not
   need to be re-derived later.

When the agent creates a new branch itself, append a log entry for it
immediately; when it starts work on a pre-existing branch that has no log
entry yet, backfill one using the discovery order above before proceeding.

## Clean Commit Procedure

Use this procedure for work that starts below trunk in a discovered ancestry
chain — most commonly a disposable branch created for a task expected to take
many actions (exploration, iterative design, a multi-file refactor).

1. Discover the branch ancestry chain (above).
2. Branch down from the tip of that chain to a disposable branch. Commit
   however is convenient while iterating: no depth limit, no requirement that
   intermediate commits be individually clean or Conventional-Commits-shaped.
3. Before shipping, restack if the parent branch moved while the work was in
   progress: rebase the disposable branch onto its parent's latest state
   rather than shipping against a stale base.
4. Once the task is genuinely done, squash the disposable branch's history
   into one commit that fully complies with Commit Hygiene Expectations and
   the Reference Boundary. This step is not optional and is not satisfied by
   leaving the disposable history intact with a compliant commit added on
   top — the published state is one commit representing the whole change.
5. Ship the clean commit **one level at a time, trunk-ward** — never skip a
   level in the chain. Each level's own merge method, review requirement, or
   release cadence governs whether it advances further immediately or waits
   (a `dev` branch batching work for a scheduled release is a valid stopping
   point, not a shortcut being skipped).
6. Delete a branch once its work has landed at the next level up, subject to
   the deletion gate above — autonomous only when the branch is confirmed
   local or agent-created and uncollaborated; ask first otherwise.
7. Later work branches fresh from the new tip. Re-run branch ancestry
   discovery at that point instead of reusing a chain cached from a previous
   session.

This procedure does not relax the Shared-History Danger Gate: apply it
independently at each level of the chain. A level that is local-only permits
autonomous squash/ship; a level that is shared or under review does not, even
if lower levels in the same chain were handled autonomously.

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
- **Type is one of the canonical Conventional Commits types:** `feat`, `fix`,
  `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`,
  `revert`. Do not invent a type outside this list; if none fits, the change
  is being mis-scoped, not the type being under-supplied.
- **Structure is fixed:** `type(scope): summary` as a single imperative
  sentence with no trailing period, followed by a body of 72 words or fewer,
  total. This is the complete shape — nothing about the body-content and
  exclusion rules below changes this ceiling.
- **Scope is a single unit of change — the skill, module, component, or
  package — not a broad repo-level area.** In a skills repository, scope is
  the skill name. In an application, scope is the affected package or layer.
  Multiple scopes in one commit title are banned. This has no exception for
  commits whose diff spans several units — that is common and expected, not
  a signal to split the commit or compound the scope.
- **Choosing the scope is a relevance judgment about the message, not a
  measurement of the diff.** When one commit message is requested, that
  commit covers everything currently being committed, however many logical
  strands the diff actually contains — do not propose splitting into
  multiple commits just because the work wasn't monotonic; every file still
  gets committed together regardless of what the title names. Pick the
  scope, and the title, by asking: of everything in this diff, what is the
  one thing a maintainer with no session context, reading this years from
  now, needs to know happened? That is the predominant change — scope to it
  alone. A scope spanning genuinely unrelated ground (true repo-level
  infrastructure with no single skill at the center) is the one case where
  `repo` is correct; that is not the same thing as a commit that merely
  touched several skills while doing one predominant thing. Avoid other
  generic scopes like `skills` or `misc` that carry no useful signal about
  where the change lives.

  Examples from this repo's convention:
  - `feat(graphify): add 4-stage MCP orchestration lifecycle` — new skill added
  - `fix(ci-cd): tighten relay startup triage in commit discipline` — targeted
    fix to a specific part of an existing skill
  - `feat(bootstrap): add cross-tool skills-repo link bootstrap` — the
    predominant change is bootstrap, even though the same commit also hardens
    an unrelated `AGENTS.md` rule and tightens `ci-cd` in passing
  - `chore(repo): bootstrap skills repository scaffold` — the rare case where
    the change truly is repo-level infrastructure (scaffolding, CI, `.gitignore`)
    and no single skill is the primary unit of change

- Keep the subject line concise and imperative; the subject is not the place
  for tradeoffs, rationale, or extended context.
- **Include a commit body. It is not optional.** Describe the predominant
  change's useful work — what it does, not how the work unfolded — in 72
  words or fewer, total. This is a lossy compression by design: a commit
  message is not `docs/`, and secondary or unrelated work swept into the
  same commit is expected to go unmentioned even though every file involved
  is still committed. If a secondary change is worth a pointer at all, name
  it in exactly one closing sentence, highly compressed (e.g. "Also added X
  and refined Y.") — never an itemized list, never its own paragraph, and
  never a reason to split the commit. Do not use the body to list files
  changed — the diff does that — or to narrate process, sandbox mechanics,
  workspace conditions, or how the work unfolded. Tone and prose standards
  from the documentation skill apply here; do not use inflated language,
  circular phrasing, or unnecessary filler.
- This discipline governs the one commit that becomes the durable record —
  whether it is the only commit made for the work, or the result of
  `rebase -i --autosquash` collapsing an exploratory branch. It does not
  constrain intermediate or fixup commits made while work is still in
  progress (see Autonomous History Cleanup below), and it does not apply to
  pull request descriptions, which aggregate however many commits are
  heading into merge-readiness and are allowed more length, more formatting,
  and more context under the separate standard in
  `references/pull-request-messages.md`.
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
