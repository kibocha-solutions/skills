# Tasks — generalize-pbo-doctrine

## Phase 1: Split .agents/prompt.md doctrine (non-legal → documentation, legal → legalese)
- [x] Read prompt.md, legalese/SKILL.md, documentation/SKILL.md, AGENTS.md
- [x] Add medium-agnostic doctrines to documentation/SKILL.md (general-first, authority-context/self-status exclusion, economy of disclosure, anti-fluff modal note, intern-style test), PBO vocab stripped, universal examples
- [x] Add legal-specific doctrines to legalese/SKILL.md (settled legal class technique, preamble-vs-operative voice separation), PBO vocab stripped, universal examples
- [x] Add short pointer in AGENTS.md Maestro section: check `.agents/memory/` for recorded document/instrument structural conventions before re-deriving them

## Phase 2: Gemini Antigravity MCP registration fix (recurring pain point)
- [x] Investigate live ~/.gemini state, ~/.codex/config.toml, and archived brain sessions to find what actually worked
- [x] Confirm working shape: `command: uvx, args: [code-review-graph, serve]` (not bare `code-review-graph`), config at `~/.gemini/antigravity/mcp_config.json` (not `builtin/`, not `antigravity-cli/`); installed via `uv tool install`, not pipx
- [x] Write durable memory entry `.agents/memory/gemini-antigravity-mcp-registration.md`, index in MEMORY.md
- [x] Update graphify/assets/mcp-config-template.json and graphify/references/environment-setup.md to match verified working shape
- [x] Fix stale rsync reference in .agents/memory/skills-repo-deployment-workflow.md (mechanism changed to git sparse-checkout per commit 22e61fb)

## Phase 3: Ship
- [x] Commit 1 (scope: documentation) — doctrine generalization
- [x] Commit 2 (scope: graphify) — MCP registration fix + memory entry
- [x] Commit 3 (scope: bootstrap) — stale memory doc correction
- [x] Push to origin/main
- [x] Re-run ensure-*-link.sh + ensure-gemini-builtin-skills.sh for all installed tools, verify each mirror
- [x] Finalize walkthrough, archive session
