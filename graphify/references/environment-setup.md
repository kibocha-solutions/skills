# Environment Setup

Setting up a new environment from zero requires installing Python, `uv`, `pipx`, CodeGraphContext, and `code-review-graph`.

## 1. Verify Prerequisites

Run these commands to verify the system has Python and package managers:

```bash
python3 --version
which uv || true
which pipx || true
```

### Install `uv` (if missing)
- Linux, WSL, or macOS:
  `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows PowerShell:
  `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Install `pipx` (if missing)
- Ubuntu/Debian:
  `sudo apt update && sudo apt install -y pipx && pipx ensurepath`
- macOS:
  `brew install pipx && pipx ensurepath`
- Windows:
  `scoop install pipx` or `py -m pip install --user pipx && py -m pipx ensurepath`

---

## 2. Install Graph Tools

Install both tools with `uv tool install`, not `pipx`. A `pipx`-installed
`code-review-graph` shim has repeatedly failed to resolve reliably when
invoked bare from MCP client subprocesses; registering it as `uvx
code-review-graph serve` instead is the verified working shape — see
`assets/mcp-config-template.json` and
`.agents/memory/gemini-antigravity-mcp-registration.md` in the skills repo.

```bash
# Install CodeGraphContext
uv tool install codegraphcontext

# Install code-review-graph
uv tool install code-review-graph
```

Refresh the shell paths:
```bash
uv tool update-shell
export PATH="$HOME/.local/bin:$PATH"
```

---

## 3. Verify Installations

Run diagnostic commands to ensure both tools are successfully installed:

```bash
cgc doctor
code-review-graph serve --help
```

If both commands return successful status, the environment is ready for repository activation.
