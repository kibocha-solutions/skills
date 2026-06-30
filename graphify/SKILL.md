---
name: graphify
description: >
  Activate this skill whenever the user asks about codebase architecture,
  code-impact analysis, blast-radius mapping, inheritance or dependency chains,
  or compliance / regulatory documentation mapping (e.g., "what changes if I
  touch X?", "show me who calls this module", "does the new code satisfy the
  UN compliance PDF?", "map the architecture of the auth layer"). This skill
  integrates CodeGraphContext (CGC) and code-review-graph (CRG) to support
  codebase-impact and architectural analysis. Trigger proactively whenever the
  query requires structural code understanding.
---

# Code Intelligence Integration

Graphify integrates CodeGraphContext (CGC) and code-review-graph (CRG) to support codebase-impact and architectural analysis.

## Complementary Roles

| Tool | Focus Area | Key Specialty & Strengths |
|---|---|---|
| **code-review-graph (CRG)** | **Change Staging & Impact Analysis** | AST parsing, change detection, blast-radius mapping, callers/callees, affected execution flows, and code reviews. |
| **CodeGraphContext (CGC)** | **Codebase Intelligence & Query Engine** | Semantic code search, dead code detection, cyclomatic complexity profiling, and custom Cypher graph querying. |

---

## Operating Lifecycle

### 1. Verification
Before querying the codebase or running analysis, verify that both MCP servers are reachable. 
- Probe availability using the procedures in [environment-setup.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/environment-setup.md).
- If either tool fails the availability check, follow the recovery instructions.

### 2. Synchronization
Sync the repository indexes before answering the user's prompt:
- Update CRG via `code-review-graph update`.
- Update CGC via `cgc update --quiet`.

### 3. Staging and Implementation Workflow
When designing or implementing a new feature, follow the self-inquiry and documentation-first staging workflow documented in [feature-staging-example.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/examples/feature-staging-example.md).

### 4. Tool Routing
Select the appropriate tool for each query using the routing logic in [tool-routing-guide.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/tool-routing-guide.md).

---

## Reference Documents

*   [environment-setup.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/environment-setup.md) — Installing and setting up the environment from zero.
*   [repository-activation.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/repository-activation.md) — Activating both graph tools in a local repository.
*   [tool-routing-guide.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/tool-routing-guide.md) — Choosing the right tool for specific query types.
*   [recovery-runbook.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/references/recovery-runbook.md) — Detailed troubleshooting steps for common installation and runtime errors.
*   [feature-staging-example.md](file:///home/codelf/workspace/kibocha-solutions/skills/graphify/examples/feature-staging-example.md) — Walkthrough of a feature staging workflow.
