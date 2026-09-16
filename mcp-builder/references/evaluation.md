# MCP Evaluation Procedure

## 1. Inspect the public surface

1. List tools, resources, and prompts through the MCP client.
2. Read exposed names, descriptions, schemas, annotations, and instructions.
3. Do not use implementation code as evaluation context.

## 2. Inspect read-only data

1. Use only read-only, non-destructive, idempotent operations.
2. Use bounded limits and pagination.
3. Find closed historical records with stable answers.
4. Record the identifiers and evidence needed to re-verify each answer.

## 3. Write ten tasks

Each task must:

1. Stand alone.
2. Require multiple MCP calls.
3. Represent a realistic user need.
4. Avoid exact-title keyword lookup as the whole solution.
5. Use read-only operations.
6. Resolve to one stable value.
7. Specify the answer format.
8. Remain verifiable by exact comparison.

## 4. Store the evaluation

```xml
<evaluation>
  <qa_pair>
    <question>Question with a fixed time range and one required answer format.</question>
    <answer>Expected value</answer>
  </qa_pair>
</evaluation>
```

1. Escape XML characters.
2. Use one `<qa_pair>` per task.
3. Keep each answer to one value.
4. Do not store credentials or private data.

## 5. Verify answers

1. Solve every task through the public MCP surface.
2. Recompute material aggregates by an independent method.
3. Confirm every tool call was read-only.
4. Replace an incorrect expected answer.
5. Remove an unstable, ambiguous, destructive, or implementation-dependent task.

## 6. Run and review

1. Use a provider-neutral MCP client or the user's selected evaluation host.
2. Record exact-match accuracy, task duration, call count, and failure category.
3. Classify failures as discovery, schema, description, behavior, output, pagination, authorization, or evaluation defects.
4. Fix the responsible surface.
5. Re-run the complete evaluation.
