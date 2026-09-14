# Feature Staging Example

## 1. Identify the requested feature

Example: add a project API endpoint.

## 2. Find established patterns

1. Search for existing endpoint implementations.
2. Find related schemas, models, repositories, and services.
3. Find design records and requirements.

## 3. Map dependencies

1. Trace callers of the related repository or service.
2. Trace downstream persistence and integration calls.
3. Locate tests for the affected symbols.
4. Record the affected flows.

## 4. Plan the change

1. Name each file and symbol to change.
2. Name each interface or schema constraint to preserve.
3. Name the tests to add or update.
4. Name the documentation to update.

## 5. Implement and verify

1. Implement within the approved scope.
2. Run focused tests.
3. Refresh the graph.
4. Re-run impact and affected-flow queries.
5. Verify graph results against the final source.
