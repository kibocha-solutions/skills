# Tool Routing Guide

Selecting the appropriate tool depends on the intent and depth of the query.

## Core Routing Table

| Query Type / Intent | Primary Tool | Parameter / Action | Notes |
|---|---|---|---|
| Blast radius of a code change, impact tracking | **code-review-graph** | `get_impact_radius` / `detect_changes` | High-accuracy AST change impact analysis. |
| AST diffs, affected execution flows, PR staging review | **code-review-graph** | `get_affected_flows` / `get_review_context` | Map change-impact on execution paths. |
| Upstream callers, downstream callees, inheritance tree | **code-review-graph** | `query_graph` / `analyze_code_relationships` | Map call chains. |
| Semantic search, keyword search, finding files by description | **CodeGraphContext** | `find_code` | Search codebase semantic/syntax content. |
| Cyclomatic complexity profiling, finding complex functions | **CodeGraphContext** | `calculate_cyclomatic_complexity` | Profile cyclomatic complexity. |
| Dead code, orphaned functions, unused symbols | **CodeGraphContext** | `find_dead_code` | Scan for unused methods. |
| Custom graph querying, relationship exploration | **CodeGraphContext** | `execute_cypher_query` (Cypher queries) | Run Cypher queries on FalkorDB/KùzuDB. |
| Architectural report, overview | **CodeGraphContext** | `generate_report` | Generate `CGC_REPORT.md` overview. |

---

## CodeGraphContext Traversal Capabilities

CodeGraphContext supports five specific methods of codebase traversal:

1.  **Semantic / Keyword Code Search (`find_code`):** Locating files, functions, and variables based on descriptions or names.
2.  **Relationship Analysis (`analyze_code_relationships`):** Tracing callers, callees, and class inheritance.
3.  **Dead Code Detection (`find_dead_code`):** Scanning for unused/orphaned methods.
4.  **Complexity Auditing (`calculate_cyclomatic_complexity` / `find_most_complex_functions`):** Identifying god classes and highly complex functions.
5.  **Cypher Query Traversal (`execute_cypher_query`):** Executing custom Cypher language queries to run traversals on KùzuDB/FalkorDB. For example:
    *   Finding nodes of specific types (e.g. `Function`, `Class`, `File`).
    *   Finding relationships (e.g. `CALLS`, `DEFINES`, `DEPENDS_ON`, `IMPORTS`).
    *   Tracing inheritance paths or deep cyclic dependencies.
