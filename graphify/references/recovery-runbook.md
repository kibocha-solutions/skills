# Recovery Runbook

## 1. Capture diagnostics

```bash
python3 --version
command -v uv
command -v cgc
command -v code-review-graph
uv tool list
cgc doctor
code-review-graph serve --help
```

## 2. Classify the failure

1. Identify whether the failure concerns availability, configuration, storage, indexing, locking, or the MCP connection.
2. Record the exact command, exit status, and error message.
3. Inspect only the paths named by the error or the configured `.agents/code-graphs/` state directory.

## 3. Repair availability

1. Follow [environment setup](environment-setup.md).
2. Apply the universal installation gate.
3. Re-run the executable checks.

## 4. Repair configuration

1. Inspect the active client configuration without exposing secrets.
2. Compare it with `../assets/mcp-config-template.json`.
3. Change persistent client configuration only when the user requests it.
4. Reconnect the client or restart the configured MCP process when the host permits it.

## 5. Repair storage

1. Confirm the target repository root.
2. Confirm the configured data directory is under `.agents/code-graphs/`.
3. Inspect permissions and free space.
4. Preserve existing databases unless the user authorizes rebuilding them.
5. Do not delete a database, lock, or state directory to bypass an error.

## 6. Repair indexing

1. Run the tool's status or doctor command.
2. Update an existing index before rebuilding it.
3. Rebuild only after the user authorizes replacement of existing graph state.
4. Verify the final index against a known symbol in the repository.

## 7. Repair locking

1. Identify the process holding the lock.
2. Determine whether it is an active graph operation.
3. Wait for an active operation or ask the user before terminating it.
4. Retry once after the lock is released.

## 8. Stop after repeated failure

1. Limit recovery to three distinct attempts.
2. Stop after the third failed attempt.
3. Report the diagnostics, attempted repairs, and remaining blocker.
4. Do not improvise destructive cleanup or privilege escalation.
