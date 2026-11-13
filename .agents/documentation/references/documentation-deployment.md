# Documentation Deployment

Use this reference for building, previewing, publishing, and maintaining the
documentation site itself.

## Required Sources

- Writerside config, tree files, build scripts, CI workflows, hosting config,
  redirects, and existing publication docs.
- Writerside build and publish docs:
  https://www.jetbrains.com/help/writerside/build-and-publish.html
- Writerside redirects:
  https://www.jetbrains.com/help/writerside/redirects.html

## Default Paths

- `docs/writerside.cfg`
- `docs/<instance>.tree`
- `docs/redirection-rules.xml`
- deployment notes in `docs/topics/operations/ci-cd.md` or
  `docs/topics/operations/deployment.md`

## Required Content

- Instances built and where each publishes.
- Build, preview, validation, and publish commands.
- Required tool versions and environment variables.
- Redirect and URL stability policy.
- How snippet library topics and any TOC library trees are reused.
- Where build artifacts are stored.

## Workflow

1. Identify whether the task is authoring docs or deploying docs.
2. Keep docs deployment separate from application deployment unless the same
   pipeline owns both.
3. Preserve existing URLs with redirects when renaming or moving topics.
4. Document build limitations truthfully when local Writerside tooling is not
   available.

## Validation

- Commands match available scripts or official Writerside commands.
- Each published instance has a tree and home page.
- Redirect rules exist for renamed public URLs when needed.
- Build or preview was run, or validation limits are stated.
