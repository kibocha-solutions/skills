# Package, Publish, and Propagate Skills

## Objective

Create verified Claude and Codex upload archives, publish the completed repository changes to `origin/main`, and propagate the current skills and shared rules to Claude, Codex, Gemini CLI, Gemini Antigravity, and Copilot.

## Execution

1. Read the CI/CD and Bootstrap instructions required for this work.
2. Build both upload archives outside the repository.
3. Verify archive topology, contents, and checksums.
4. Audit the repository diff, validate the repository, commit, and push.
5. Run each supported Bootstrap propagation path.
6. Verify installed skill inventories and shared-rule entrypoints.
7. Record the final commit, archive checksums, and propagation results.

## Boundaries

- Include only active top-level skill packages and the target tool's general instruction file in each archive.
- Exclude repository administration, source imports, planning records, and Git metadata from the archives.
- Keep generated archives outside the repository.
- Do not add AI attribution to any publication metadata.
