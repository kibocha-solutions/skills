# Configuration Documentation

Use this reference for environment variables, secrets, feature flags, config
files, and runtime settings.

## Required Sources

- `.env.example`, config modules, deployment manifests, CI secrets, README
  setup steps, tests, and runtime validation code.
- Twelve-Factor App config principle: https://12factor.net/config

## Default Paths

- `docs/engineering/configuration-environment.md`
- deployment-sensitive config may also be referenced from
  `docs/operations/deployment.md`

## Required Content

- Variable or setting name.
- Purpose.
- Required or optional status.
- Allowed values or format.
- Default.
- Environment scope.
- Secret or non-secret classification.
- Source of truth and where it is set.
- Example value that is safe to publish.
- Failure behavior when missing or invalid.

## Workflow

1. Extract settings from code and examples, not memory.
2. Document secret names, never secret values.
3. Separate local development setup from production deployment config.
4. Mark secret-store names and production topology as Internal or Restricted.
5. Use tables for reference-heavy config pages.

## Validation

- Every documented setting exists in code/config or is clearly planned.
- Required settings have setup instructions.
- Examples are safe placeholders.
- Defaults match the runtime.
