# Multi-Agent MCP Setup and Autonomous Configuration

This reference defines the procedure for discovering, autonomously configuring, and authenticating Figma and Playwright Model Context Protocol (MCP) servers across all supported agent hosts: **Claude Code, OpenAI Codex CLI, Google Gemini (Antigravity & CLI), and GitHub Copilot**.

## 1. Tooling Responsibilities

- **Figma MCP (`@figma/mcp`)**: Extracts design tokens, color variables, typography styles, auto-layout geometry, component variants, and vector assets directly from Figma URLs.
- **Playwright MCP (`@playwright/mcp`)**: Drives headless or headed browsers to capture responsive viewport screenshots, extract structured accessibility tree snapshots, and verify interactive states.

---

## 2. Host Detection and Configuration Target Resolution

Inspect the environment to determine the active agent host and target configuration path:

| Host Environment | Detection Marker | Primary Configuration Path | Format |
|---|---|---|---|
| **Claude Code** | Environment contains `CLAUDE_CODE` or directory `~/.claude/` exists | `~/.claude/settings.json` | JSON |
| **OpenAI Codex CLI** | Directory `~/.codex/` exists or command `codex` active | `~/.codex/config.toml` | TOML |
| **Google Gemini Antigravity** | Workspace contains `.gemini/` or directory `~/.gemini/antigravity/` exists | `~/.gemini/antigravity/mcp_config.json` | JSON |
| **Google Gemini CLI** | Directory `~/.gemini/` exists without Antigravity IDE | `~/.gemini/settings.json` | JSON |
| **GitHub Copilot** | Directory `~/.copilot/` exists or running in VS Code workspace | `.vscode/mcp.json` or `~/.copilot/config.json` | JSON |

---

## 3. Autonomous Server Pre-Configuration (Mode 1 Gate)

When a task requires Figma or browser testing, do not ask the user to manually edit configuration files. Perform the setup autonomously:

### Step 1: Playwright MCP Setup (100% Autonomous)
Playwright MCP requires no authentication credentials.

1. Inspect the host configuration file.
2. If `playwright` is not registered, insert the server block:

**For JSON configurations (Claude, Gemini, Copilot):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

**For TOML configurations (Codex):**
```toml
[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]
```

3. Ensure local Node/npx runtime is available:
   ```bash
   npx --version
   ```
4. Confirm server readiness. Notify the user only that Playwright MCP is configured and active.

---

### Step 2: Figma MCP Setup (Autonomous Config with Gated Authentication)
Figma MCP requires a personal access token with read permissions.

1. Inspect the host configuration file for the `figma` server.
2. If absent, write the server definition into the active configuration file with a placeholder token:

**For JSON configurations (Claude, Gemini, Copilot):**
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "<PENDING_AUTH_TOKEN>"
      }
    }
  }
}
```

**For TOML configurations (Codex):**
```toml
[mcp_servers.figma]
command = "npx"
args = ["-y", "@figma/mcp"]
[mcp_servers.figma.env]
FIGMA_ACCESS_TOKEN = "<PENDING_AUTH_TOKEN>"
```

3. **Gated User Authentication Prompt**:
   Pause execution and prompt the user with this exact procedure:
   > "I have configured the Figma MCP server in `<target_config_path>`. To complete authentication, please generate a Personal Access Token:
   > 1. Open `https://www.figma.com/settings` in your browser.
   > 2. Under the 'Personal access tokens' section, click 'Generate new token'.
   > 3. Provide a name (e.g. 'Agent MCP') and grant the scope: `File content: Read`.
   > 4. Paste your token here or set it in your environment."
4. Once the user provides the token, update the configuration file with the live credential.
5. Verify access by executing a sample node query against the supplied Figma file key.
