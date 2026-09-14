---
name: mcp-builder
description: Design, implement, test, and document provider-neutral Model Context Protocol servers in TypeScript or Python. Use when creating or revising MCP tools, resources, prompts, transports, authorization, schemas, structured outputs, pagination, or server evaluations.
license: Complete terms in LICENSE.txt
---

# MCP Builder

## 1. Define the server

1. Identify the service, users, deployment target, client hosts, and required operations.
2. Identify the service API, authentication method, authorization model, rate limits, pagination, and error contract.
3. Separate read operations, reversible writes, destructive operations, and administrative operations.
4. List required tools, resources, prompts, and server instructions.
5. Record explicit exclusions.

## 2. Verify the current protocol and SDK

1. Read the current MCP specification at `https://modelcontextprotocol.io/specification/`.
2. Read the current official SDK documentation for the selected language.
3. Verify the installed SDK major version.
4. Use only APIs documented for that major version.
5. Record the protocol revision and SDK versions in the implementation plan.
6. Do not copy examples from an older major version without migrating them.

Use [TypeScript implementation](reference/node_mcp_server.md) or [Python implementation](reference/python_mcp_server.md).

## 3. Choose the transport

1. Use stdio for a local subprocess integration.
2. Use Streamable HTTP for a remote server.
3. Do not use a retired transport for a new server.
4. Keep protocol messages on stdout for stdio.
5. Send logs and diagnostics to stderr for stdio.
6. Bind local HTTP servers to loopback unless remote access is required.

## 4. Design the MCP surface

Read [MCP best practices](reference/mcp_best_practices.md).

1. Use tools for actions and parameterized operations.
2. Use resources for retrievable content with stable identifiers.
3. Use prompts for reusable user-invoked prompt templates.
4. Use server instructions for cross-tool order and constraints.
5. Keep instructions out of tool descriptions when they apply to the whole server.
6. Cover the complete user workflow with composable operations.
7. Do not mirror every upstream API endpoint without a user workflow.

## 5. Design each tool

1. Name tools `<service>_<verb>_<resource>` in snake case.
2. Give each tool one bounded operation.
3. Write a direct description that states the operation and selection criteria.
4. Define a strict input schema with types, constraints, defaults, and field descriptions.
5. Define an output schema for structured results when supported.
6. Return structured content that matches the declared output schema.
7. Return concise text content when clients require it.
8. Add accurate `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` annotations.
9. Add filters and cursor or offset pagination to unbounded list operations.
10. Return stable identifiers needed by follow-up operations.

## 6. Enforce security

1. Keep credentials outside source code and tool output.
2. Validate token audience, issuer, expiry, scopes, and signature when applicable.
3. Enforce authorization inside every protected operation.
4. Validate all external input at the server boundary.
5. Reject path traversal, command injection, unsafe URLs, oversized input, and unsupported schemes.
6. Set request timeouts and response-size limits.
7. Apply rate limits where abuse or service limits require them.
8. Validate the HTTP `Origin` and enable DNS rebinding protection for local HTTP servers.
9. Mark destructive tools accurately and require explicit target identifiers.
10. Do not expose stack traces, secrets, internal paths, or private service responses.

## 7. Implement shared infrastructure

1. Create one authenticated service client.
2. Centralize retries, timeouts, pagination, error translation, and response shaping.
3. Separate MCP handlers from service-domain logic.
4. Reuse schemas and domain types.
5. Use async I/O for network and filesystem operations.
6. Clean up clients, files, subprocesses, and connections.
7. Keep tool handlers small and deterministic.

## 8. Implement errors and outputs

1. Return tool-level failures with `isError: true` when the SDK supports it.
2. Give the caller the failed operation, safe cause, and corrective input.
3. Preserve upstream status categories without exposing sensitive bodies.
4. Distinguish empty results from failed requests.
5. Indicate truncation and provide the next cursor or narrower filter.
6. Keep output field names and types consistent across related tools.

## 9. Test the server

1. Test schema acceptance and rejection.
2. Test authentication and authorization failures.
3. Test pagination boundaries and empty results.
4. Test rate limits, timeouts, unavailable dependencies, and malformed upstream data.
5. Test every annotation against actual behavior.
6. Test destructive operations in an isolated environment.
7. Test stdio for protocol-clean stdout.
8. Test Streamable HTTP origin, authentication, concurrency, and shutdown behavior.
9. Run the official MCP Inspector or SDK test client.
10. Run the language build, type check, linter, and test suite.

## 10. Evaluate usability

Read [evaluation procedure](reference/evaluation.md).

1. Create ten independent, read-only tasks with stable answers.
2. Cover discovery, pagination, multi-step retrieval, ambiguity resolution, and output interpretation.
3. Solve each task through the public MCP surface.
4. Verify each expected answer independently.
5. Remove tasks that require hidden implementation knowledge or mutable current state.
6. Record failures by tool, schema, description, output, or server behavior.
7. Revise the server and repeat the evaluation.

## 11. Document and verify

1. Document installation, configuration, authentication, permissions, transports, and startup commands.
2. Document every tool, resource, prompt, and output schema.
3. Document destructive behavior and external side effects.
4. Include tested client configuration examples without credentials.
5. Re-run all verification against the final code.
6. Confirm the documentation matches the final exposed MCP surface.
