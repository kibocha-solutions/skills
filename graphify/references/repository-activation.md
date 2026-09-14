# Repository Activation

## 1. Confirm authorization

1. Confirm that the user requested persistent graph activation.
2. Confirm the repository root.
3. Confirm that `.agents/code-graphs/` is inside the repository.
4. Preserve existing graph state.

## 2. Prepare local storage

```bash
mkdir -p .agents/code-graphs/crg .agents/code-graphs/cgc
```

Add this entry to `.gitignore`:

```gitignore
.agents/code-graphs/
```

## 3. Initialize code-review-graph

Use the installed version's help output to confirm supported flags.

```bash
code-review-graph build --repo . --data-dir .agents/code-graphs/crg
code-review-graph status --repo . --data-dir .agents/code-graphs/crg
```

## 4. Initialize CodeGraphContext

Use the installed version's help output to confirm supported flags.

```bash
cgc --path .agents/code-graphs/cgc index .
cgc --path .agents/code-graphs/cgc update --quiet
```

## 5. Configure exclusions

1. Exclude `.agents/code-graphs/` and other generated build output.
2. Keep source code, tests, durable documentation, and project-owned design records indexed.
3. Do not exclude the entire repository, the root skill directory, or all `.agents/` content.
4. Do not create root-level ignore files unless the tool requires them and the user authorized persistent activation.

## 6. Configure MCP access

1. Start from `../assets/mcp-config-template.json`.
2. Use repository-relative arguments where supported.
3. Do not hardcode another user's home directory.
4. Do not write client configuration outside the workspace without explicit approval.
5. Do not expose tokens, internal URLs, or other secrets.

## 7. Verify activation

1. Query a known symbol.
2. Retrieve one caller or dependency relationship.
3. Confirm the result against source code.
4. Confirm generated state exists only under `.agents/code-graphs/`.
5. Confirm generated state is ignored by version control.
