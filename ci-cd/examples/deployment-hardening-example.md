# Deployment Hardening Example

Use this example when the user wants concrete CI/CD improvement guidance rather
than a list of principles.

## Situation

- Platform: GitHub Actions deploying to a cloud target
- Current concerns:
  - long-lived deployment credentials;
  - broad workflow permissions;
  - no explicit staging gate;
  - rollback expectations are vague.

## Recommended guidance shape

1. Refresh or read repo health using at least two full commit records:
   `git log --show-signature -2 --date=iso-strict --format=fuller`. Do not
   infer repo commit style or signing expectations from a one-line log.
2. Inspect the workflow files, required secrets, deploy triggers, and current
   environment gates.
3. Reduce workflow permissions:
   - set default `GITHUB_TOKEN` permissions narrowly;
   - expand only per job when needed.
4. Replace long-lived cloud secrets with OIDC and short-lived credentials when
   the target platform supports it.
5. Pin third-party actions to full SHAs where feasible.
6. Introduce a minimal staged release path:
   - build or package once;
   - deploy the same artifact to staging;
   - run smoke or verification checks;
   - gate production on those checks.
7. Define rollback explicitly:
   - what artifact or release is rolled back;
   - what checks prove rollback success;
   - what data or migration constraints may prevent a full revert.

## Example improvement summary

```text
Target workflow:
- Build once on merge-ready changes
- Promote the same artifact to staging
- Run smoke checks in staging
- Require the staging gate before production deploy
- Use OIDC instead of long-lived cloud secrets
- Keep rollback tied to the last known good artifact
```

## Example risks to call out

- If schema changes are not backward-compatible, application rollback may be
  easier than data rollback.
- If the branch is high-throughput, merge queue or merged-result validation may
  be needed so staging checks reflect the combined branch state.
