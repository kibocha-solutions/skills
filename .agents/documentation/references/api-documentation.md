# API Documentation

Use this reference for REST, GraphQL, gRPC, public integration, SDK, and
internal service API documentation.

## Required Sources

- OpenAPI files, route definitions, controllers, serializers, schemas, tests,
  generated clients, SDKs, examples, auth config, and error handling code.
- Official specs and framework docs:
  - OpenAPI: https://spec.openapis.org/oas/latest.html
  - GraphQL: https://spec.graphql.org/
  - gRPC core concepts: https://grpc.io/docs/what-is-grpc/core-concepts/
  - Protocol Buffers: https://protobuf.dev/

## Default Paths

- `docs/api/api-overview.md`
- `docs/api/rest-api-reference.md`
- `docs/api/graphql-grpc-reference.md`
- `docs/api/internal-api-reference.md`
- `docs/api/integration-guide.md`
- `docs/api/sdk-docs.md`
- `docs/api/examples-samples.md`

## Required Content

- API purpose, audience, stability, and access level.
- Base URLs, environments, versions, and deprecation policy.
- Authentication and authorization.
- Endpoints, operations, methods, paths, request fields, response fields, and
  status codes for REST.
- Schema, query/mutation/subscription shape, pagination, and error model for
  GraphQL.
- Services, RPC methods, messages, streaming behavior, deadlines, and status
  codes for gRPC.
- Rate limits, quotas, retries, idempotency, timeouts, and pagination.
- Error model and remediation.
- Runnable examples and expected output.
- Source of truth for generated or contract-backed sections.

## Workflow

1. Identify API style and source of truth before writing.
2. Prefer generated contract material where it exists, but add manual topics for
   auth, examples, error handling, versioning, and operational constraints.
3. For public APIs, classify as Public only after removing internal endpoints,
   secrets, infrastructure names, private scoring logic, and restricted fields.
4. For internal APIs, document retries, service discovery, timeouts, circuit
   breakers, ownership, and failure modes.
5. Do not create or change API contracts unless the user explicitly asks for
   contract generation.

## Validation

- Every endpoint, method, field, status code, and example matches code or a
  contract.
- Auth and permission requirements are explicit.
- Examples are runnable or clearly marked as illustrative.
- Public docs do not expose internal-only behavior.
