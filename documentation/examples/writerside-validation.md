# Writerside Validation: Good vs Bad

## 1. Claiming validation

### Bad

```text
Updated the security topics. The Writerside build should be fine; the
builder log says "All done, exiting successfully".
```

Defects:

- Treats the completion line as a pass. The builder prints it after failed
  checks too.
- Builds nothing for the other instances that publish the changed topics.
- Reports no exit status, failed check, or log path.

### Good

```text
wrs build
  restricted  failed  180/181  REF001 api-overview.md in security-baseline.md:57
  log: ~/.local/share/wrs/projects/<project>/logs/<timestamp>-build-restricted.log
exit status 1
```

Advantages:

- Builds every instance, so a link that resolves in one instance and not in
  another surfaces.
- Reports the failed check with file and line, the exit status, and the log.

## 2. Serving output for inspection

### Bad

```bash
podman run -d -p 8000:80 -v ~/.local/share/wrs/build/internal:/usr/share/nginx/html nginx:alpine
```

Defects:

- The build directory holds `webHelp*.zip` and no `index.html`; nginx
  answers `403 Forbidden`.
- One instance per port with no cross-instance rules; a restricted page is
  reachable wherever it is copied.

### Good

```bash
wrs serve -b
wrs open internal
```

Advantages:

- Builds any missing site, then serves the unpacked site of each ungated
  instance on its own port.
- Redirects pages owned by lower-sensitivity instances and answers 404 for
  pages owned by higher-sensitivity instances.
- Keeps gated tiers closed until `wrs serve --dev` opens the dev gate through
  Bitwarden or 1Password.
