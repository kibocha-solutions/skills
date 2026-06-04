# Changelog and Release Documentation

Use this reference for changelogs, release notes, migration notes, and upgrade
guides.

## Required Sources

- Merged PRs, issues, commits, version tags, migration scripts, API changes,
  schema changes, release checklists, and support notes.
- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/

## Default Paths

- `docs/releases/changelog.md`
- `docs/releases/migration-notes.md`
- `docs/releases/upgrade-guide.md`

## Required Content

- Version or release identifier.
- Release date or unreleased status.
- Human-readable change categories.
- Breaking changes.
- Migration or upgrade steps.
- Known issues and compatibility notes.
- Links to source PRs, issues, or tags when available.

Use `../assets/keep-a-changelog-template.md` for new changelog files.

## Workflow

1. Do not use raw commit logs as a changelog.
2. Group user-visible changes under stable categories such as Added, Changed,
   Deprecated, Removed, Fixed, and Security.
3. Move operational upgrade steps into migration notes or upgrade guides.
4. State breaking changes plainly.
5. Keep public release notes sanitized.

## Validation

- Each change is backed by a PR, issue, tag, or local source.
- Breaking changes and migrations are not hidden inside generic categories.
- Dates and versions are consistent.
- Security details are public-safe.
