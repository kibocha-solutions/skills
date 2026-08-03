# Setup Graphify MCP

Set up and activate CodeGraphContext (CGC) and code-review-graph (CRG) MCP tools for the current repository per the `graphify` skill instructions.

## User Review Required

> [!NOTE]
> Graph databases will be initialized under `graphify/crg` and `graphify/cgc` within the repo root. Root ignore files (`.code-review-graphignore`, `.cgcignore`) will be verified or updated.

## Proposed Changes

### Configuration & Ignore Files

#### [MODIFY] [.code-review-graphignore](file:///run/media/codelf/data/workspace/skills/.code-review-graphignore)
Ensure glob patterns for CRG exclude generated/transient artifacts.

#### [MODIFY] [.cgcignore](file:///run/media/codelf/data/workspace/skills/.cgcignore)
Ensure gitignore patterns for CGC exclude generated/transient artifacts.

#### [MODIFY] [.gitignore](file:///run/media/codelf/data/workspace/skills/.gitignore)
Ensure `graphify/` directory is ignored.

### Global & Client Settings

#### [MODIFY] [Gemini settings](file:///home/codelf/.gemini/settings.json) / [Codex settings](file:///home/codelf/.codex/config.toml)
Register stdio MCP tools for `code-review-graph` and `codegraphcontext`.

## Verification Plan

### Automated Tests & Checks
- Run `cgc doctor` to verify CGC environment.
- Run `code-review-graph serve --help` to verify CRG binary.
- Run `code-review-graph status --repo . --data-dir graphify/crg` to verify CRG graph status.
- Verify repo root cleanliness via graphify cleanup pass.
