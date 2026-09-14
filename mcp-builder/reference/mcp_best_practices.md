# MCP Best Practices

## Server

1. Use a stable service-based name without a date or version suffix.
2. Declare only capabilities the server implements.
3. Put cross-tool sequencing rules in server instructions.
4. Keep logs off stdout for stdio servers.
5. Use stdio locally and Streamable HTTP remotely.

## Tools

1. Use service-prefixed snake-case names.
2. Keep one operation per tool.
3. Use strict schemas.
4. Describe every input field.
5. Declare structured output schemas when supported.
6. Return `structuredContent` that matches the schema.
7. Return resource links for large retrievable content.
8. Apply accurate behavior annotations.
9. Return tool failures as tool results.

## Resources and prompts

1. Give each resource a stable URI and MIME type.
2. Use URI templates only for bounded, validated parameters.
3. Use prompts for reusable user-invoked templates.
4. Keep secrets and private configuration out of resources and prompts.

## Pagination

1. Set a bounded default limit.
2. Enforce a maximum limit.
3. Return a cursor or offset for the next page.
4. Return a completion indicator.
5. Apply server-side filters before returning data.
6. Do not load an unbounded result set into memory.

## Security

1. Authenticate every protected request.
2. Authorize every operation.
3. Validate all inputs and external identifiers.
4. Protect local HTTP servers from DNS rebinding.
5. Validate request origins.
6. Bind to loopback by default.
7. Apply timeouts, size limits, and rate limits.
8. Redact secrets and internal error details.
9. Treat annotations as metadata, not enforcement.

## Verification

1. Compare the exposed surface with the documented surface.
2. Exercise every tool with valid and invalid input.
3. Verify every annotation against actual behavior.
4. Test with the official Inspector or SDK client.
5. Pin and record the tested SDK major version.
