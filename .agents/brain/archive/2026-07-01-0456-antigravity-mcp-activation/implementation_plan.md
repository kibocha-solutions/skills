# Implementation Plan — Antigravity MCP Activation

## Goal Statement

Enable the `code-review-graph` MCP server in the Antigravity CLI (`agy`) by adding its configuration to the CLI's global MCP settings file.

## Acceptance Criteria

1. A global MCP configuration file is created/updated at `/home/codelf/.gemini/antigravity-cli/mcp_config.json`.
2. The config file correctly defines `code-review-graph` using the stdio transport, with command `code-review-graph` and arguments `["serve"]`.
3. The configuration is valid JSON.

## Proposed Changes

- [CREATE] `/home/codelf/.gemini/antigravity-cli/mcp_config.json` — Add `code-review-graph` MCP server settings.

## Verification Plan

1. Verify JSON syntax of `/home/codelf/.gemini/antigravity-cli/mcp_config.json` using `python3 -m json.tool`.
