# TypeScript MCP Server

## 1. Verify the SDK

1. Read `https://github.com/modelcontextprotocol/typescript-sdk`.
2. Confirm the installed major version.
3. Use the documentation for that major version.
4. For SDK v2, use the current `@modelcontextprotocol/server`, transport, and integration packages named by the official guide.
5. Use Zod 4 or another supported Standard Schema implementation.

## 2. Create the project

```text
<service>-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── client.ts
│   ├── schemas.ts
│   └── tools/
└── test/
```

1. Enable strict TypeScript.
2. Use ECMAScript modules when required by the selected SDK.
3. Separate service calls from MCP registration.
4. Pin compatible dependency ranges.

## 3. Register the server surface

1. Create `McpServer` with a stable name and version.
2. Use `registerTool`, `registerResource`, and `registerPrompt` for SDK v2.
3. Pass complete schema objects.
4. Type every handler result.
5. Return `CallToolResult` or the current SDK equivalent.
6. Return `isError: true` for controlled tool failures.

## 4. Connect the transport

1. Use the Node stdio transport for local subprocess use.
2. Use the Node or web-standard Streamable HTTP transport for remote use.
3. Create per-request transport state when the selected SDK requires it.
4. Close transports when requests or processes end.
5. Keep stdout protocol-only.

## 5. Verify

```bash
npm run build
npm test
```

1. Run the official MCP Inspector or SDK test client.
2. List tools, resources, and prompts.
3. Call every tool with valid and invalid input.
4. Verify structured outputs and errors.
5. Verify clean startup and shutdown.
