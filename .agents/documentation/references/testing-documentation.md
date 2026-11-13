# Testing Documentation

Use this reference for testing strategy, test plans, test cases, coverage, and
test data documentation.

## Required Sources

- Test suites, CI config, coverage reports, QA notes, fixtures, factories,
  staging data scripts, bug reports, and release gates.

## Default Paths

- `docs/testing/testing-strategy.md`
- `docs/testing/test-plan.md`
- `docs/testing/test-cases.md`
- `docs/testing/test-data.md`

## Required Content

- Test levels and responsibilities: unit, integration, end-to-end, manual,
  security, performance, or accessibility when relevant.
- What must pass before merge, pilot, or release.
- Critical user journeys and business rules.
- Test data creation, sanitization, and reset procedures.
- Known gaps and risk acceptance.
- How to run tests and interpret results.

## Workflow

1. Read package scripts, CI jobs, and test directories before documenting.
2. Keep strategy distinct from individual test cases.
3. Use tables for scenario matrices and expected outcomes.
4. Document sanitized data rules when real user, donor, beneficiary, or customer
   data could be copied into test environments.
5. Avoid promising coverage or quality that the suite does not enforce.

## Validation

- Commands work or are tied to existing scripts.
- Release gates match CI or stated team policy.
- Test data docs do not expose sensitive data.
- Known gaps are explicit.
