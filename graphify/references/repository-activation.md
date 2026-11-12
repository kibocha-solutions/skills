# Repository Activation and Extraction Workflow

## 1. Corpus Screening and Exclusions

1. Resolve the target directory path (`INPUT_PATH`) and verify `.gitignore` and `.graphifyignore` patterns before scanning.
2. Add custom noise directories or generated assets to `.graphifyignore` using `.gitignore` glob syntax (`dist/`, `*.min.js`, `vendor/`).
3. Configure defaults (such as `--no-viz` or custom exclusions) in `.graphifyrc` if needed.
4. Detect corpus composition with `graphify.detect.detect(Path(INPUT_PATH))` or `graphify extract --help` flags. If total files exceed 2,000 or total words exceed ~5,000,000, pause and confirm exclusions with the user before building.

## 2. Structural vs Semantic Extraction

1. **Code-only repositories**:
   - Run AST extraction directly with zero LLM API calls:

```bash
graphify extract . --code-only
```

   - Optional flags: `--force` (full rescan), `--no-cluster` (raw extraction only), `--postgres DSN`, `--cargo`, `--global`.
2. **Mixed corpora (Markdown docs, papers, PDFs, Office files, images, video/audio)**:
   - Run AST extraction on code files (`graphify.extract.extract(...)`) and semantic extraction on non-code files in parallel.
   - If `GEMINI_API_KEY` or `GOOGLE_API_KEY` is already set in the environment, use `graphify.llm.extract_corpus_parallel(files, backend="gemini")`.
   - Otherwise, split uncached non-code files (`graphify.cache.check_semantic_cache`) into chunks bounded by both `<=20-25` files and `<=6,000` total lines (one file per chunk if >2,000 lines; one image per chunk) and dispatch write-capable subagents using `references/extraction-spec.md`.
   - Never prompt the user for `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.
   - Verify line coverage from chunk `"coverage"` counts and log partial reads into `.graphify_partial.txt` so the next `--update` retries incomplete files.

## 3. Build, Label, Verify, and Export

1. Build and cluster the merged extraction with `build_from_json(extraction, root=INPUT_PATH, directed=IS_DIRECTED)` and `cluster(G)`.
2. Guard against empty graphs (`G.number_of_nodes() == 0`) or unintended shrinks (`to_json(..., force=IS_FORCE)` returns `False`).
3. Run diagnostics (`graphify diagnose` or `diagnose_extraction`) and report any dangling/missing-endpoint or collapsed-edge warnings.
4. Assign concise 2-5 word plain-language community labels (`{cid: "Label"}`), regenerate `GRAPH_REPORT.md`, and re-export `graph.json`.
5. Export `graph.html` unless `--no-viz` was requested (warn first if nodes exceed 5,000).
6. Save the manifest with `save_manifest(..., root=INPUT_PATH)` and remove `.graphify_*` temporary files.

## 4. Team vs Local Git Hygiene and Hooks

1. Decide whether `graphify-out/` stays local or is shared with teammates:
   - Local-only use: add `graphify-out/` to `.gitignore`.
   - Shared repo workflow: commit `graphify-out/graph.json`, `GRAPH_REPORT.md`, and `.graphify_labels.json`, and configure `graphify merge-driver install` for JSON merge safety.
2. Install the post-commit git hook when ongoing code updates are desired:

```bash
graphify hook install
graphify hook status
```
