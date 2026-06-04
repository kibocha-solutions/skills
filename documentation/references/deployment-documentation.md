# Deployment Documentation

Use this reference for deployment, infrastructure setup, CI/CD, environments,
and release operations.

## Required Sources

- Infrastructure as code, Dockerfiles, compose files, Helm charts, CI configs,
  cloud config, deployment scripts, environment files, release workflows, and
  operational dashboards.
- Official provider docs for the specific platform being documented.

## Default Paths

- `docs/operations/deployment.md`
- `docs/operations/infrastructure.md`
- `docs/operations/ci-cd.md`

## Required Content

- Target environment and access level.
- Prerequisites, credentials model, and required permissions.
- Artifact source and version selection.
- Exact deployment commands or pipeline steps.
- Configuration and secrets expected by the deployment.
- Health checks and verification.
- Rollback, restore, or disable procedure.
- Known failure modes and escalation path.

## Workflow

1. Read deployment automation before writing human steps.
2. Prefer documenting the source-of-truth pipeline over inventing manual
   deployment procedures.
3. Separate infrastructure reference from deployment procedure when the page
   becomes too large.
4. Classify precise infrastructure topology, private network details, and
   sensitive cloud identifiers as Restricted.
5. Include diagrams only when topology or flow is easier to verify visually;
   route production diagrams to `technical-diagrams`.

## Validation

- Commands, paths, pipeline names, and environment names match the repo.
- Rollback or recovery steps exist for risky changes.
- Verification has observable success criteria.
- Secrets are named by variable or secret-store key, never exposed as values.
