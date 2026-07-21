# Walkthrough — Antigravity MCP Activation

## Context

The user requested to read the `graphify` skill and add the `code-review-graph` MCP server configuration to the Antigravity CLI because it failed to activate there. Web search showed that Antigravity CLI uses `~/.gemini/antigravity-cli/mcp_config.json` for global MCP configurations.

## Changes

- `/home/codelf/.gemini/antigravity-cli/mcp_config.json`: Created configuration for `code-review-graph` stdio MCP server.

## Verification

- Verified JSON syntax using `python3 -m json.tool /home/codelf/.gemini/antigravity-cli/mcp_config.json` which successfully parsed and printed the formatted JSON object.
