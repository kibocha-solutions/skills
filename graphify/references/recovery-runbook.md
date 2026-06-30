# Recovery Runbook

Detailed recovery procedures for Stage 2 of the `graphify` (CodeGraphContext & code-review-graph) skill. Read this file when any of the three recovery attempts requires deeper investigation.

---

## Environment Diagnostic Checklist

Run these before attempting any recovery to gather baseline state:

```bash
# 1. Python version (requires 3.10+)
python3 --version

# 2. uv availability
which uv && uv --version

# 3. pipx availability
which pipx && pipx --version

# 4. PATH inspection
echo $PATH | tr ':' '\n' | grep -E "(local|bin|uv|pipx)"

# 5. Installed tools via uv
uv tool list

# 6. Installed tools via pipx
pipx list

# 7. Check for cgc and code-review-graph binaries
which cgc 2>/dev/null || echo "cgc not on PATH"
which code-review-graph 2>/dev/null || echo "code-review-graph not on PATH"
```

On native Windows, use:

```powershell
python --version
where.exe uv
where.exe pipx
where.exe cgc
where.exe code-review-graph
$env:Path -split ';'
```

Capture this output and include it in any user-facing error report when halting.

---

## Attempt 1 — Bootstrap Installer Toolchain (Detailed)

**Goal:** Ensure `uv` and `pipx` exist before attempting to install CodeGraphContext and code-review-graph. Do not skip this step just because later commands mention them; missing installer tools are a recoverable failure.

### Detect the host shape

```bash
uname -a
cat /proc/version 2>/dev/null | grep -qi microsoft && echo "WSL detected"
```

Prefer Linux commands inside WSL. Use Windows commands only when the agent host is running natively on Windows.

### Install `uv` if missing

Linux, WSL, and macOS:

```bash
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
```

Native Windows PowerShell:

```powershell
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
}
```

Do not use `apt install uv` as the default recovery path. Some Ubuntu releases do not package `uv`, and a missing apt package should not halt recovery when the official standalone installer is available.

---

## Attempt 2 — Force Install (Detailed)

### Installing codegraphcontext via uv

```bash
uv tool install codegraphcontext
```

Watch the output for any `ERROR` lines about missing system libraries (e.g. `libssl`, `libffi`).

### Installing code-review-graph via pipx

```bash
pipx install code-review-graph
```

If the direct `pipx install` reports that the package is already installed but the binary is broken, use:

```bash
pipx reinstall code-review-graph
```

After install, verify using both `cgc doctor` and `code-review-graph --help`.

---

## Attempt 3 — Initialize & Generate Config (Detailed)

Attempt 3 handles the case where the binaries are installed but the graph databases have not been initialized or mapped to a project context yet.

### code-review-graph

```bash
# Register the MCP server and write graph instructions
code-review-graph install

# Build the knowledge graph for the current repository
code-review-graph build
```

### CodeGraphContext

```bash
# Initialise the database in the current project root
cgc index

# Generate reports or verify status
cgc report
cgc stats
```

If you see `Permission denied` on `.codegraphcontext/` or `.code-review-graph/`, fix with:
```bash
rm -rf .codegraphcontext && cgc index
rm -rf .code-review-graph && code-review-graph build
```

---

## Common Failure Modes and Fixes

### `cgc` or `code-review-graph` MCP connection refused

The binary exists but the MCP server subprocess failed to start.

```bash
# Run the servers manually to see the startup error
cgc mcp start 2>&1 | head -30
code-review-graph serve 2>&1 | head -30
```

Read the first 30 lines of output for the root cause.

### SQLite "database is locked" in code-review-graph

Another process (a previous `code-review-graph update` run) holds the DB lock.

```bash
lsof .code-review-graph/graph.db 2>/dev/null
```

Kill the locking process, then retry.

### "SKILL HALT" after 3 attempts

If all three attempts fail, do not improvise. Output the halt message from SKILL.md Stage 2, include the diagnostic output from the checklist, and stop. The user must fix their environment configuration before the skill can proceed.

---

## MCP Config Verification

Every agent host should register both local stdio MCP servers.

### Codex

```toml
[mcp_servers.codegraphcontext]
command = "cgc"
args = ["mcp", "start"]
type = "stdio"

[mcp_servers.code-review-graph]
command = "code-review-graph"
args = ["serve"]
cwd = "/home/codelf"
type = "stdio"
```

### OpenCode

```json
{
  "mcp": {
    "code-review-graph": {
      "type": "local",
      "command": ["code-review-graph", "serve"],
      "enabled": true
    },
    "codegraphcontext": {
      "type": "local",
      "command": ["cgc", "mcp", "start"],
      "enabled": true
    }
  }
}
```

### Claude Code

```bash
claude mcp add code-review-graph -- code-review-graph serve
claude mcp add codegraphcontext -- cgc mcp start
```
