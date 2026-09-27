# Pull Request Examples

Contrasting examples of pull request descriptions based on Google and Microsoft engineering standards.

## 1. Feature Pull Request

### Bad Example: Flagged Violations

```text
Title: Added some features and fixed bugs
[Defect: Vague title combining unrelated features and fixes]

Generated with AI Assistant v2.
[Defect: Strict violation of the absolute AI-attribution prohibition]

## Summary
In this PR, I worked on the authentication middleware and also fixed an issue where the CSV exporter crashed for John Doe (john.doe@example.com). Also updated dependencies and reformatted gateway.py.
[Defect: Multiple unrelated issues bundled; personal name and email leaked; task narration instead of durable outcome]

## Changes
Modified:
1. auth/middleware.ts
2. export/csv.ts
3. gateway.py
4. package.json
[Defect: File manifest repeats diff without explaining architectural or behavioral changes]

## Context
See chat history from yesterday's session.
[Defect: Citing internal session history instead of linking a durable public issue or requirement]

## Testing
Tested on my laptop and it works fine.
[Defect: Lacks exact automated commands, unit test coverage, and reproducible verification results]
```

### Good Example: Standard Format

```text
Title: feat(auth): enforce token revocation on session expiration

## Summary
Enforces cryptographic token revocation when user sessions reach their expiration deadline, terminating active API access tokens immediately across distributed services.

Resolves #412.

## Context
Previously, expired web sessions left secondary API bearer tokens valid until their independent twelve-hour lifetime elapsed. This permitted continued read access from cached client tokens after a user initiated logout or session timeout. Revoking secondary bearer tokens during session termination closes this exposure without altering background service-to-service credentials.

## What changed
1. Integrated token revocation hook into the session lifecycle termination handler.
2. Added distributed cache invalidation broadcast for active bearer token IDs.
3. Updated token validation middleware to check the revocation registry before accepting claims.
4. Separated token cache invalidation from user database schema migrations.

## Testing
Automated tests executed and passed:
1. `npm run test:unit -- test/auth/revocation.spec.ts`: verified token invalidation on session expiry.
2. `npm run test:integration -- test/auth/distributed-cache.spec.ts`: verified multi-node invalidation broadcast.
3. `npm run lint`: verified zero lint errors across modified auth modules.

## Risk and rollback
1. Risk: High-frequency logouts could increase redis invalidation queue load during peak traffic.
2. Rollback: Invalidate feature flag `AUTH_REVOCATION_BROADCAST_ENABLED` to revert to legacy independent expiration without requiring service redeployment.
```

## 2. Bug Fix Pull Request

### Bad Example: Flagged Violations

```text
Title: Fix bug
[Defect: Inadequate title; fails to specify what was fixed]

Fixed the query parser crash that user Jane reported on Slack.
[Defect: Unverifiable private communication citation; vague description]

Changes:
Changed line 42 from `date.parse()` to `tryParse()`.
[Defect: Narrating single line code edit already evident in diff]
```

### Good Example: Standard Format

```text
Title: fix(query): handle malformed ISO-8601 timestamps in range filters

## Summary
Prevents unhandled runtime exceptions when query range filters receive invalid or incomplete ISO-8601 timestamp inputs, returning a structured 400 Bad Request error instead of a 500 Internal Server Error.

Resolves #589.

## Context
When client applications sent date strings missing timezone indicators, such as `2026-09-27T00:00`, the timestamp parser encountered an unhandled exception that terminated the worker thread. Robust input validation ensures deterministic API error responses for malformed inputs.

## What changed
1. Added validation helper to reject malformed date inputs prior to parser execution.
2. Mapped parse errors to structured 400 Client Error responses with specific field diagnostics.
3. Added boundary test cases covering incomplete ISO-8601 formats.

## Testing
1. Unit: `go test -v ./pkg/query/parser_test.go`, passing all 14 tests, including new malformed timestamp test cases.
2. Integration: `go test -v ./test/integration/api_test.go`, passing all test suites.

## Risk and rollback
1. Risk: Low; affects only invalid input error handling paths.
2. Rollback: Revert commit with `git revert <commit-sha>`.
```
