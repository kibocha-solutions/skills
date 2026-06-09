# Security And Operations

Use this reference for GitHub Actions security, secret handling, branch
protection, artifact integrity, and emergency delivery practices.

Primary-source basis:

- GitHub secure-use reference and Actions security guides
- GitHub OIDC reference
- GitHub protected branches and required status checks docs
- Cloud-provider deployment hardening guidance where OIDC and ephemeral
  credentials are supported

## GitHub Actions Security

- Pin third-party actions to a full commit SHA when feasible.
- Scope workflow permissions as narrowly as the job allows.
- Set the default `GITHUB_TOKEN` permission model as narrowly as the repo can
  tolerate, then widen only per job when required.
- Treat untrusted input in workflow commands, matrix values, and shell
  interpolation as injection risk.
- Keep secrets out of logs, generated artifacts, and pull request comments.
- Prefer dedicated deploy credentials over broad personal tokens.
- Prefer OIDC with short-lived cloud credentials over long-lived repository
  secrets when the target platform supports it.

## Branch Protection Expectations

Prefer:

- required pull requests for protected branches;
- required status checks;
- up-to-date branch requirements where the team uses them;
- linear history where the repo relies on squash, rebase, or queue-based merge
  enforcement;
- restricted force-push and bypass permissions;
- explicit admin bypass policy, not silent exceptions.

If a repo does not support or currently use these controls, distinguish:

- what the repo already enforces,
- what is merely recommended,
- what the current hosting plan may block.

## Artifact And Release Integrity

- Build once, promote the same artifact forward where the platform allows it.
- Make artifact provenance traceable to commit, workflow run, and environment.
- Do not rebuild a supposedly identical release artifact in each environment
  unless the platform requires it and the variance is understood.
- Where the platform supports provenance or attestations, prefer enabling them
  over relying only on convention and naming.

## Emergency Changes

- Prefer revert over hurried forward-fix when user impact is active and the
  root cause is still uncertain.
- If manual intervention is required, document:
  - what changed,
  - who approved it,
  - how the system returns to the normal pipeline path.
- Treat emergency shell access as an exception to close, not a deployment
  strategy.
- After an emergency bypass, restore the standard gated delivery path and record
  the branch, release, and operator context that justified the bypass.

## Sensitive Content Checks

Before commit or release, inspect for:

- `.env` files,
- raw credentials or private keys,
- accidental instruction files that should stay local,
- debug logs or artifacts containing tokens,
- generated files that expose internal-only operational data.
