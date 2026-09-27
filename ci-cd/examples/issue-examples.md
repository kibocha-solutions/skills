# Issue Examples

Contrasting examples of bug reports and feature requests based on Google and Microsoft open-source engineering standards.

## 1. Bug Report

### Bad Example: Flagged Violations

```text
Title: Broken date parsing
[Defect: Vague title; doesn't specify defect mode or affected component]

Hey, the API crashed when our customer John (john@example.com) tried to submit this:
[Defect: Leaked personal name and email; missing environment facts]

[Screenshot of Python code]
[Defect: Code provided as an image instead of copyable text in a code fence]

Also, the user profile page has a misaligned button.
[Defect: Combining multiple unrelated bugs into one issue]
```

### Good Example: Standard Format

```markdown
Title: Query API: unhandled exception when parsing date ranges without timezone offset

### Environment
1. Version: 2.14.0
2. OS: Ubuntu 24.04 LTS on x86_64 architecture
3. Runtime: Node.js v22.8.0
4. Database: PostgreSQL 16.3

### Problem description
When submitting a date range filter query without an explicit ISO-8601 UTC offset, such as `2026-09-27T00:00:00`, the query parser encounters an unhandled runtime error and returns HTTP 500 Internal Server Error instead of validating the input or defaulting to UTC.

### Steps to reproduce
1. Start the API service with default configuration: `npm run start`.
2. Send a POST request to `/api/v1/records/search` with the payload below:

```json
{
  "filter": {
    "date_from": "2026-09-27T00:00:00",
    "date_to": "2026-09-27T23:59:59"
  }
}
```

3. Observe HTTP 500 response with message `Unhandled exception in timestamp parser`.

### Expected behavior
The API should accept valid ISO-8601 strings and treat offset-free timestamps as UTC, or return HTTP 400 Bad Request with a clear validation error indicating that a timezone offset is required.

### Minimal reproducible example

```typescript
import { parseDateFilter } from './src/query/parser';

// Throws UnhandledException: Invalid ISO string missing offset
const result = parseDateFilter('2026-09-27T00:00:00');
```

### Logs

```text
ERROR [parser]: Unhandled exception in timestamp parser: OffsetMissingError
    at parseDateFilter (/app/src/query/parser.ts:42:11)
    at SearchHandler.handle (/app/src/handlers/search.ts:18:24)
```
```

## 2. Feature Request

### Bad Example: Flagged Violations

```text
Title: Add new auth methods
[Defect: Imprecise title]

We should add OIDC and SAML and WebAuthn because everyone uses them.
[Defect: Bundling three distinct authentication systems into one request without use cases or boundaries]
```

### Good Example: Standard Format

```markdown
Title: Add OIDC token exchange support for GitLab CI pipeline runners

### Problem or use case
CI/CD workflows executed on external GitLab runners currently authenticate to our API using long-lived bearer tokens stored in repository secrets. Rotating these long-lived secrets across multiple projects creates operational overhead and credential leakage risks.

### Proposed solution
Support RFC 8693 OAuth 2.0 Token Exchange using GitLab's native JSON Web Token OIDC provider:
1. Accept the runner's signed OIDC token at `/api/v1/auth/oidc-exchange`.
2. Validate the token against GitLab's published JSON Web Key Set.
3. Issue a short-lived scoped session token with 15-minute validity.

### Non-goals and boundaries
1. Supporting self-hosted non-OIDC GitLab runners without public JWKS endpoints is excluded from this change.
2. User-interactive OIDC login is covered separately and is not affected by runner token exchange.
```
