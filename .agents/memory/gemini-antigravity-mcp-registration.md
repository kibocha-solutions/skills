---
name: gemini-antigravity-mcp-registration
description: Verified working MCP server registration path and command shape for Google Antigravity on this workstation, after three prior sessions guessed wrong
type: project
---

Google Antigravity (`~/.gemini/antigravity/`) reads its MCP server config
from `~/.gemini/antigravity/mcp_config.json` — a top-level file sibling to
`builtin/`, not inside it, and not at the earlier-guessed
`~/.gemini/antigravity-cli/mcp_config.json`. `~/.gemini/antigravity/builtin/`
holds only the rules file (`GEMINI.md`) and skill mirror; it does not hold
MCP config. `~/.gemini/config/mcp_config.json` is a separate, superseded
location (marked by a `.migrated` file alongside it) — do not target it.

The working `code-review-graph` entry invokes it through `uvx`, not the bare
pipx shim:

```json
{
  "code-review-graph": {
    "command": "uvx",
    "args": ["code-review-graph", "serve"],
    "cwd": "<repo-root>"
  }
}
```

A bare `"command": "code-review-graph"` entry (calling the pipx-installed
shim directly) is what's in `graphify/assets/mcp-config-template.json` and
what `~/.codex/config.toml` used before it was corrected — it does not
reliably work. Installing the tool via `uv tool install code-review-graph`
(not `pipx install`) and invoking it through `uvx` in the MCP config is the
combination confirmed working in both `~/.codex/config.toml` and
`~/.gemini/antigravity/mcp_config.json` on this machine. `codegraphcontext`
does not need this treatment — its `cgc` shim works fine invoked bare.

**Why:** three separate sessions (`antigravity-mcp-activation`,
`graphify-mcp-correction`, `setup-graphify-mcp`) each rediscovered part of
this from scratch, including one that wrote the config to the wrong path
(`antigravity-cli/`) before the correct path was found empirically.

**How to apply:** when registering `code-review-graph` as an MCP server for
Gemini Antigravity (or diagnosing why it isn't reachable there), use the path
and command shape above directly instead of re-deriving them.
