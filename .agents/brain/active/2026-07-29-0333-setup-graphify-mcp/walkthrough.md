# Walkthrough - setup-graphify-mcp

## Overview
Successfully installed Graphify CLI tools (`uv`, `codegraphcontext`, `code-review-graph`), built repository knowledge graph under `graphify/`, registered global MCP server configs, cloned the 4-clone skills topology, and cleaned up generated root scaffolding.

## Phase 1: Tool Installation
- Installed `uv` via Astral installer script into `~/.local/bin`.
- Installed `codegraphcontext` (v0.5.3) and `code-review-graph` (v2.3.7) using `uv tool install`.
- Verified `cgc doctor`: 8/8 language parsers verified OK, FalkorDB Lite connection successful.

## Phase 2: Repository Activation & Graph Build
- Verified repo root ignore files (`.gitignore`, `.code-review-graphignore`, `.cgcignore`).
- Built CRG database at `graphify/crg`: 1,964 nodes, 20,488 edges, 202 files across bash, python, and javascript.
- Indexed CGC database at `graphify/cgc`.

## Phase 3: Topology & MCP Server Setup
- Clones established via `git clone git@github.com:kibocha-solutions/skills.git`:
  - `~/.claude/skills`
  - `~/.codex/skills`
  - `~/.gemini/skills`
  - `~/.copilot/skills`
- Aligned global instruction entrypoints (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `copilot-instructions.md`) using `bootstrap/scripts/ensure-*-link.sh`.

## Phase 4: Cleanup & Verification
- Performed mandatory Graphify cleanup pass on repo root: removed `.claude`, `.codebuddy`, `.gemini`, `.mcp.json`, `.qoder`, `opencode.jsonc`.
- Workspace `git status` verified clean.
