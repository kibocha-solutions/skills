# Pipelines And Deployments

Use this reference for CI workflow changes, deployment design, release flow,
environment strategy, and rollback planning.

Primary-source basis:

- Google Cloud deployment methodology and Cloud Deploy docs for immutable
  artifacts, releases, staged rollouts, and business continuity
- DORA continuous delivery and trunk-based development guidance
- GitHub and GitLab docs where pipeline behavior depends on merge queues or
  merged-result validation

## Pipeline Principles

- Keep a single auditable path to production.
- Fail fast with the cheapest, most diagnostic checks first.
- Keep `main` or the protected release branch deployable.
- Make the path from local validation to CI to deployment legible.
- Prefer deterministic automation over manual heroics.
- Build or package once, then promote the same artifact forward where the
  platform supports it.
- Treat deployment automation, continuous testing, and short-lived branches as
  reinforcing practices, not separate programs.

## Recommended Stage Order

1. Formatting and static checks
2. Unit tests
3. Build or package creation
4. Integration tests
5. Security or dependency scans
6. Deploy to non-production target
7. Smoke checks
8. Production deployment gate
9. Post-deploy verification

Adjust the order only when repo reality justifies it.

## Busy-Branch Validation

When many changes land on the same protected branch each day:

- prefer merge queues or merged-result validation over repeated manual rebases;
- ensure required checks reflect the combined branch state, not only the head
  branch in isolation;
- keep job names unique where the hosting platform requires unambiguous status
  checks.

## Environment Guidance

- Keep at least clear separation between development, validation, and
  production concerns, even if the repo has fewer formal environments.
- Document which secrets, variables, and approvals differ by environment.
- Avoid environment-specific logic hidden in ad hoc shell fragments.
- If the platform uses formal release objects or rollout phases, preserve those
  concepts in the pipeline design instead of flattening everything into one
  shell step.

## Deployment Strategy Selection

- Rolling deploy:
  - Use when the platform handles incremental replacement well and rollback is
    straightforward.
- Blue-green:
  - Use when traffic switching is cheap and rollback speed matters.
- Canary:
  - Use when gradual exposure and metric-based validation matter more than raw
    simplicity.
- Linear:
  - Use when the platform exposes progressive rollout percentages without a
    full canary analysis layer and you want controlled expansion.

If the platform does not support the safer strategy cleanly, say so and choose
the simplest reliable alternative.

## Rollback Rules

- Define rollback before changing the deployment path.
- Prefer reversible releases and immutable artifacts.
- If diagnosis is unclear during an incident, revert to the last known good
  state before chasing a complex forward fix.
- Record which checks prove rollback success.
- If schema, shared data, or external state complicates rollback, say so
  explicitly and separate application rollback from data rollback.

## Release Checklist

Confirm:

- required checks are green;
- the artifact or release object being promoted is the intended one;
- artifact versioning is clear;
- environment variables and secrets are present;
- migration or data-risk steps are understood;
- smoke tests exist for the target deployment;
- rollback path is documented and feasible.

## Anti-Patterns

- Manual production deploys as the normal path.
- Hidden deploy logic split across chat instructions and unchecked scripts.
- Pipelines that pass without proving the artifact can actually start.
- Production-only fixes with no rollback plan.
- Rebuilding a supposedly identical artifact independently in each environment
  when a promote-forward model is available.
