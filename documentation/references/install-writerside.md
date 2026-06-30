# Install Writerside Builder

Use this reference when Writerside validation is required but the `wrs` command,
Docker, or the Writerside builder image is unavailable.

## Expected Tooling

- Docker is installed and reachable from the current shell.
- The JetBrains builder image is available:
  `jetbrains/writerside-builder:2026.06.8817`.
- The `wrs` wrapper is installed at `~/.local/bin/wrs`.
- `~/.local/bin` is on `PATH`.
- `writerside` may be a shell alias for `wrs`.

## Verify Availability

Run these commands from the project or documentation directory:

```bash
command -v wrs
wrs doctor
docker image inspect jetbrains/writerside-builder:2026.06.8817
```

Expected result:

- `command -v wrs` prints a path such as `/home/codelf/.local/bin/wrs`.
- `wrs doctor` finds `writerside.cfg`, lists the available instances, and
  reports Docker and image status as `ok`.
- `docker image inspect` exits with status `0`.

If Docker is installed but not reachable from WSL, start Docker Desktop and
enable WSL integration for the active distribution. On Linux, start the Docker
service or add the user to the Docker group according to the host policy.

## Install From Zero

1. Install Docker Desktop on Windows or macOS, or Docker Engine on Linux.
2. Start Docker and confirm it is reachable:

   ```bash
   docker version
   ```

3. Pull the Writerside builder image:

   ```bash
   docker pull jetbrains/writerside-builder:2026.06.8817
   ```

4. Install the wrapper in the user bin directory:

   ```bash
   mkdir -p "$HOME/.local/bin"
   install -m 0755 /tmp/wrs "$HOME/.local/bin/wrs"
   ```

   If `/tmp/wrs` is unavailable, recreate the wrapper from the project
   operations notes or ask for the maintained copy before continuing.

5. Add the command and alias to the shell profile:

   ```bash
   grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" \
     || printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
   grep -qxF 'alias writerside="wrs"' "$HOME/.bashrc" \
     || printf 'alias writerside="wrs"\n' >> "$HOME/.bashrc"
   ```

6. Reload the shell or source the profile:

   ```bash
   . "$HOME/.bashrc"
   ```

7. Verify:

   ```bash
   wrs doctor
   ```

## Build Documentation

Run a build from any directory inside a Writerside project:

```bash
wrs build internal
```

Use another instance when needed:

```bash
wrs build public
wrs build restricted
wrs build confidential
```

The wrapper searches upward for `writerside.cfg`. For a repository with
`docs/writerside.cfg`, it builds module instances such as `docs/internal`.

The wrapper copies the project to a temporary source directory before building.
This prevents the JetBrains builder from leaving `.idea/` files in the real
workspace. Build output, logs, reports, and generated ZIP files are written
under `~/.local/share/wrs/` by default.

## Serve Output

After a successful build:

```bash
wrs serve internal
```

Stop the background server:

```bash
wrs stop internal
```

Use `wrs logs` to list recent build and server logs.

## Clean Temporary Files

Run cleanup after testing:

```bash
wrs clean
```

The command removes stale temporary source copies and labeled leftover
Writerside containers.

After a temporary verification run, remove same-day output, logs, and source
copies:

```bash
wrs clean --all
```

## Known Builder Behavior

- The builder may print IntelliJ plugin warnings before it starts compiling
  topics. Treat the final exit status and inspection output as authoritative.
- Mount an output parent directory, then set `OUTPUT_DIR` to a child such as
  `/opt/out/build`. Mounting the exact output directory at `OUTPUT_DIR` can
  fail because Writerside tries to delete and recreate that directory.
- A read-only source mount prevents workspace writes, but the current builder
  can hang while trying to save `.idea/workspace.xml` during shutdown. Use the
  temporary source-copy workflow instead.
- A non-zero exit status means the build failed even if the log contains
  `All done, exiting successfully`. Report the inspection failures and log path.

## Official References

- https://www.jetbrains.com/help/writerside/build-with-docker.html
- https://www.jetbrains.com/help/writerside/build-and-publish.html
- https://www.jetbrains.com/help/writerside/local-build.html
