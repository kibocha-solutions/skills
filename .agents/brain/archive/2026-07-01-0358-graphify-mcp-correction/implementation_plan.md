# Implementation Plan — graphify MCP correction

## Goal Statement

Correct the graphify skill to match the current Graphify public docs and installed CLI behavior. Done means the skill no longer tells agents to register or probe a nonexistent `graphify serve` MCP server, while still preserving `code-review-graph serve` as the global MCP server and documenting Graphify's supported CLI/skill plus project-scoped `--mcp` mode.

## Acceptance Criteria

1. `graphify/SKILL.md` distinguishes `code-review-graph` as the standalone MCP server from Graphify as a CLI/skill integration.
2. `graphify/SKILL.md` no longer instructs agents to run `graphify ping` or register `graphify serve` globally.
3. `graphify/references/recovery-runbook.md` documents `graphify <path> --mcp` as project/corpus-scoped and warns that `graphify serve` is invalid for current `graphifyy` releases.
4. `graphify/assets/mcp-config-template.json` registers only the working global MCP server and gives Graphify CLI/project-scoped notes separately.
5. Verification confirms no stale `graphify serve` or `graphify ping` references remain in graphify files.

## Proposed Changes

- [MODIFY] `graphify/SKILL.md` — revise server model, discovery, recovery, halt, and examples.
- [MODIFY] `graphify/references/recovery-runbook.md` — correct provider config and failure diagnostics.
- [MODIFY] `graphify/assets/mcp-config-template.json` — remove broken Graphify MCP server entries and add CLI integration notes.

## Open Questions

None blocking. User explicitly requested the update.

## Verification Plan

1. Run `rg` for stale `graphify serve` and `graphify ping` references.
2. Validate JSON template with `python3 -m json.tool`.
3. Run `git diff --check` and inspect changed diff.
