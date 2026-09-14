# Tool Routing Guide

| Request | Primary tool | Operation |
|---|---|---|
| Changed files and symbols | code-review-graph | `detect_changes` |
| Change context | code-review-graph | `get_review_context` |
| Blast radius | code-review-graph | `get_impact_radius` |
| Affected execution paths | code-review-graph | `get_affected_flows` |
| Callers, callees, imports, tests | code-review-graph | `query_graph` |
| Architecture overview | code-review-graph | `get_architecture_overview` |
| Semantic code discovery | CodeGraphContext | `find_code` |
| Complexity | CodeGraphContext | `calculate_cyclomatic_complexity` |
| Dead code | CodeGraphContext | `find_dead_code` |
| Custom relationships | CodeGraphContext | `execute_cypher_query` |

## Routing steps

1. Use the tool named in the table.
2. Check whether its index covers the current repository and revision.
3. Use the other graph tool when the first result leaves a structural gap.
4. Read the exact source passages needed to verify consequential findings.
5. Use `rg` only for graph gaps or exact text matching.
