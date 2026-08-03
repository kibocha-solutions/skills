# Tasks — setup-graphify-mcp

## Phase 1: Environment & Tool Verification
- [x] Check system binaries (`python3`, `uv`, `pipx`, `cgc`, `code-review-graph`)
- [x] Install `uv`, `codegraphcontext`, and `code-review-graph` in `~/.local/bin`

## Phase 2: Repository Activation & Indexing
- [x] Verify root ignore files (`.gitignore`, `.code-review-graphignore`, `.cgcignore`)
- [x] Build code-review-graph (CRG) index in `graphify/crg` (1,964 nodes, 20,488 edges)
- [x] Index CodeGraphContext (CGC) in `graphify/cgc`

## Phase 3: MCP Server Registration
- [x] Register `codegraphcontext` and `code-review-graph` stdio tools in global agent configs (`~/.codex/config.toml`, `~/.gemini/antigravity/mcp_config.json`, etc.)
- [x] Git clone `git@github.com:kibocha-solutions/skills.git` into `~/.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`, and `~/.copilot/skills`

## Phase 4: Verification & Cleanup
- [x] Verify diagnostics via `cgc doctor` and `code-review-graph status`
- [x] Execute mandatory graphify cleanup pass on repo root (removed `.claude`, `.codebuddy`, `.gemini`, `.mcp.json`, `.qoder`, `opencode.jsonc`)
- [x] Finalize walkthrough record
