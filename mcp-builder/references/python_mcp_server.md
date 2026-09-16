# Python MCP Server

## 1. Verify the SDK

1. Read `https://github.com/modelcontextprotocol/python-sdk`.
2. Confirm the installed major version.
3. Use the documentation for that major version.
4. For SDK v2, import `MCPServer` from `mcp.server`.
5. Migrate v1 `FastMCP` code before adding features.

## 2. Create the project

```text
<service>_mcp/
├── pyproject.toml
├── src/<service>_mcp/
│   ├── __init__.py
│   ├── server.py
│   ├── client.py
│   ├── models.py
│   └── tools.py
└── tests/
```

1. Use supported Python and SDK versions.
2. Pin compatible dependency ranges.
3. Use type hints for every public function.
4. Use Pydantic or the SDK-supported schema mechanism.
5. Separate service calls from MCP decorators.

## 3. Register the server surface

1. Create `MCPServer` with a stable service name.
2. Register tools, resources, and prompts with the current decorators or registration APIs.
3. Use strict typed inputs.
4. Return typed structured outputs when supported.
5. Translate expected failures into safe tool errors.
6. Use lifespan management for persistent clients and connections.

## 4. Connect the transport

1. Use stdio for local subprocess use.
2. Use Streamable HTTP for remote use.
3. Keep stdout protocol-only.
4. Close asynchronous clients and connections.

## 5. Verify

```bash
python -m compileall src
pytest
```

1. Run the official MCP development client or Inspector.
2. List tools, resources, and prompts.
3. Call every tool with valid and invalid input.
4. Verify structured outputs and errors.
5. Verify clean startup and shutdown.
