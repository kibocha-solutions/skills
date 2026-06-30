# Feature Staging Walkthrough

This walkthrough illustrates a feature staging workflow when designing or implementing a new feature or endpoint (e.g., *"Create the API endpoint for handling projects"*).

## Step 1: Self-Inquiry

Before writing code or configurations, ask these questions:
- *How is a new endpoint created in this project? What patterns already exist?*
- *What database schemas, models, or classes have already been defined that relate to this feature?*
- *Are there existing Entity Relationship Diagrams (ERDs) or design specifications?*

---

## Step 2: Locate Documentation & Requirements (via CodeGraphContext)

Use CodeGraphContext (`find_code`) to locate design documents, ERD specifications, or schema layouts.

### Example Tool Call
```json
{
  "name": "find_code",
  "arguments": {
    "query": "ERD project database schema"
  }
}
```

If the query returns a documentation file such as `docs/database/project_erd.md`, read the file to understand the database structure and business constraints.

---

## Step 3: Map the Codebase Architecture (via code-review-graph)

Use code-review-graph (`query_graph` or `get_impact_radius`) to map out existing implementation patterns and dependencies.

### Example Tool Call
```json
{
  "name": "query_graph",
  "arguments": {
    "pattern": "callers_of",
    "symbol": "ProjectRepository"
  }
}
```

This maps how existing repositories are called, helping you design the new API controller, service, and repository layers in harmony with the rest of the application.
