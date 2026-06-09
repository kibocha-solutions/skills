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

1. Inspect the workflow files, required secrets, deploy triggers, and current
   environment gates.
2. Reduce workflow permissions:
   - set default `GITHUB_TOKEN` permissions narrowly;
   - expand only per job when needed.
3. Replace long-lived cloud secrets with OIDC and short-lived credentials when
   the target platform supports it.
4. Pin third-party actions to full SHAs where feasible.
5. Introduce a minimal staged release path:
   - build or package once;
   - deploy the same artifact to staging;
   - run smoke or verification checks;
   - gate production on those checks.
6. Define rollback explicitly:
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
