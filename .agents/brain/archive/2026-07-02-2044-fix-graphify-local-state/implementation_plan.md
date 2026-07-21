# Implementation Plan: fix(graphify) — project-local graph state

## Goal

Update the Graphify skill so agents keep graph state inside the repo-local
`graphify/` directory, exclude assistant-generated files from CGC and CRG
indexes, and commit/push the change cleanly.

## Confirmed Facts

- CRG `--data-dir` confirmed for `build`, `update`, `status`.
- CGC `--path` / `--db-path` global flag confirmed; uses FalkorDB by default.
- CGC `.cgcignore` file supported (gitignore-style syntax, repo-root discovery).
- CRG `.code-review-graphignore` file supported (glob patterns at any depth).
- Current `.gitignore` does not include `graphify/`.
- Neither `.code-review-graphignore` nor `.cgcignore` exist yet.
- Git identity: JohnKibocha <johnkibocha@outlook.com>
- Signing: SSH key at `C:/Users/codelf/.ssh/SshSigningKey.pub`
- Remote: `origin git@github.com:kibocha-solutions/skills.git`
- Branch: `main`, clean working tree.

## Files to Change

1. `graphify/SKILL.md` — update with local-state layout rules
2. `graphify/references/repository-activation.md` — update commands to use `--data-dir`
3. `.gitignore` — add `graphify/`
4. `.code-review-graphignore` — create with exclusion rules
5. `.cgcignore` — create with exclusion rules

## Commit

Message: `fix(graphify): keep graph indexes in project-local cache`
