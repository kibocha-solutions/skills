# Graphify Recovery Runbook

## 1. Stale Graph or Commit Drift

1. Symptom: `graph_stats` reports `built_at_commit` behind `HEAD`, `graphify-out/needs_update` exists, or `hook-guard` warns that source files are newer than `graph.json`.
2. Fix:
   - Code-only changes: run `graphify update .`.
   - Documentation, paper, image, or deletion changes: run full incremental merge (`detect_incremental` + semantic pass on changed non-code files + `build_merge`) or rebuild cleanly (`graphify extract .`).
   - Run `graphify reflect --if-stale` after rebuilds to refresh `graphify-out/reflections/LESSONS.md`.

## 2. Shrink-Guard Refusal

1. Symptom: Export prints `ERROR: refused to shrink graphify-out/graph.json (existing graph has more nodes; #479)`.
2. Cause: Deleted files, stricter `.graphifyignore`, or an incomplete extraction produced fewer nodes than the existing graph.
3. Fix:
   - First check whether extraction failed or dropped semantic chunks (inspect `graphify diagnose` and `.graphify_partial.txt`).
   - If the shrink is intentional (files removed or ignored), re-run with `--force` (`graphify update . --force` or `to_json(..., force=True)`).

## 3. MCP Server Missing Graph or Tool Errors

1. Symptom: `graphify-mcp` fails to connect, crashes on import, or returns missing-graph errors.
2. Checks:
   - Verify the binary was installed with the `[mcp]` extra (`which graphify-mcp` and `graphify-mcp --help`).
   - Verify Python version is `<3.15` (`head -1 "$(which graphify-mcp)"`).
   - Verify `graphify-out/graph.json` exists at `cwd` or pass `project_path="<repo-root>"` to the MCP tool call.
   - Check `graph.json` size limits and valid JSON via `python3 -m json.tool graphify-out/graph.json >/dev/null`.

## 4. Strict `hook-guard` Blocking Raw Read or Grep

1. Symptom: Claude Code or Gemini CLI blocks or nudges on raw `Grep` or `Read` calls.
2. Expected behavior: Do not disable `hook-guard`; satisfy it properly:
   - Query `graphify` MCP (`query_graph`, `get_neighbors`, `shortest_path`) or `graphify query "<terms>"` first.
   - Subsequent targeted `Read` calls for files located by the graph succeed (strict mode blocks only the first unqueried `Read`/`Grep` per session or compaction cycle).
   - If stale timestamps trigger false freshness warnings after `git checkout`, verify manifest hashes or run `graphify update .`.

## 5. Empty Graph or Legacy Node-ID Scheme

1. Symptom: `0 nodes` extracted or `[graphify] note: this graph uses the pre-#1504 node-ID scheme`.
2. Fix:
   - Inspect `.graphifyignore` and `.gitignore` for over-broad exclusions matching source folders.
   - Rebuild cleanly with `graphify extract --force .` to upgrade legacy IDs to full path-qualified `{stem}_{entity}` IDs.
