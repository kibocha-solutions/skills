# Install and Run the Writerside Builder

Use this reference when Writerside validation is required and the `wrs`
command, a container runtime, or the Writerside builder image is unavailable,
or when building, serving, or inspecting Writerside output.

Read `../../system-init/SKILL.md` before installing a container runtime, the
builder image, or the wrapper. Apply the universal installation gate.

## Contents

- Requirements
- Install
- Verify
- Pin project settings
- Build
- Check tier references
- Serve and inspect
- Open the dev gate
- Maintain
- Builder behavior
- Official references

## Requirements

| Component | Requirement |
|---|---|
| Python | 3.11 or later. `wrs` uses the standard library only. |
| Container runtime | Podman (preferred, rootless) or Docker. `wrs` selects Podman first, then Docker. Force one with `WRS_RUNTIME` or `--runtime`. |
| Builder image | `docker.io/jetbrains/writerside-builder:2026.08.0328`. The image is published for `amd64` only; `wrs` adds `--platform linux/amd64` on `arm64` hosts. |
| Server image | `docker.io/library/nginx:alpine`. `wrs serve` pulls it on first use. |
| Wrapper | `scripts/wrs` from this skill, installed as `~/.local/bin/wrs`. |
| Dev gate | Bitwarden CLI (`bw`) logged in, or 1Password CLI (`op`) with an added account or desktop app integration; `secret-tool` with an unlocked login keyring. Required only for `wrs serve --dev` and `wrs key`. |

## Install

1. Install Podman, or Docker when Podman is unavailable, through the host
   package manager and the system-init installation gate.
2. Confirm the runtime is reachable:

   ```bash
   podman info
   ```

3. Pull the builder image:

   ```bash
   podman pull docker.io/jetbrains/writerside-builder:2026.08.0328
   ```

4. Keep the previous wrapper when `~/.local/bin/wrs` exists:

   ```bash
   cp -p "$HOME/.local/bin/wrs" "$HOME/.local/bin/wrs.previous"
   ```

5. Install the wrapper from this skill:

   ```bash
   install -D -m 0755 <skills-root>/documentation/scripts/wrs "$HOME/.local/bin/wrs"
   ```

6. Add `~/.local/bin` to `PATH` when `command -v wrs` prints nothing:

   ```bash
   grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" \
     || printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
   ```

7. Check for a newer builder image:

   ```bash
   wrs update
   ```

   `wrs update --pull` pulls the newest dated tag and verifies that the local
   digest matches the Docker Hub digest.

## Verify

Run from the project root or any directory inside the documentation source:

```bash
wrs --version
wrs doctor --online
```

Expected result: every line of `wrs doctor` shows a pass mark, including
`writerside.cfg`, `instances`, `runtime`, `builder image`, `ports`, and
`latest image`. The command exits `0`. `wrs` finds `writerside.cfg` in the
current directory, a parent directory, or a `docs/` or `Writerside/` child.

## Pin project settings

Commit a `.wrs.toml` beside `writerside.cfg` so every contributor builds with
the same image and ports:

```toml
image_tag = "2026.08.0328"
port_base = 44190
jobs = 2
sensitivity = ["public", "internal", "restricted", "confidential"]
gated_from = "restricted"
dev_item = "wrs-dev"
```

Settings resolve in this order, highest first: command flags, `WRS_*`
environment variables (`WRS_RUNTIME`, `WRS_IMAGE_TAG`, `WRS_PORT_BASE`,
`WRS_JOBS`, `WRS_STATE_DIR`, `WRS_GATED_FROM`, `WRS_DEV_ITEM`,
`WRS_PASSWORD_MANAGER`), `.wrs.toml`, `~/.config/wrs/config.toml`.

| Key | Meaning |
|---|---|
| `sensitivity` | Instance IDs from lowest to highest tier. An instance missing from the list ranks above every listed instance. |
| `gated_from` | The first tier behind the dev gate. That tier and every higher tier are served only with `--dev`. |
| `dev_item` | The login item that holds the dev key: an item name, or `op://<vault>/<item>` for 1Password. Default `wrs-dev`. |
| `password_manager` | `bitwarden` or `1password`. When unset, an `op://` item selects 1Password; otherwise `wrs` uses the installed CLI, Bitwarden first. |

## Build

Build every instance declared in `writerside.cfg`:

```bash
wrs build
```

Build selected instances:

```bash
wrs build internal restricted
```

| Option | Effect |
|---|---|
| `-j N`, `--jobs N` | Parallel builder containers. The default derives from CPU count and available memory, from 1 to 4. |
| `--image-tag TAG` | Builder image tag for this run. |
| `--keep-src` | Keep the temporary source copy after a successful build. |
| `--json` | Print per-instance results as JSON on stdout. |
| `--plain`, `--no-color` | Plain output. `NO_COLOR` and `TERM=dumb` also disable color. |

Build results:

1. `wrs` copies the documentation source to a temporary directory for each
   instance and excludes `output/`, `.idea/`, and `.git/`.
2. The summary table lists status, passed checks, warnings, published topic
   pages, and duration for each instance.
3. A failed instance lists each failed check with file and line, and the
   build log path.
4. Exit status is `0` when every instance passes, `1` when any instance fails,
   `2` for a usage or environment error, and `130` after Ctrl-C.
5. Output lives under `~/.local/share/wrs/projects/<project>-<hash>/`:
   `site/<instance>/` holds the unpacked website, `artifacts/<instance>/`
   holds the web ZIP, `report.json`, and `build.json`, and `logs/` holds build
   logs.
6. After every instance passes, `wrs` runs the tier check described below. An
   upward link fails the build with exit status `1`.

## Check tier references

Apply the tier and linking rules in `writerside-technical-documentation.md`,
Access and Sensitivity. `wrs check` enforces them on the built sites:

```bash
wrs check
```

| Finding | Result |
|---|---|
| A lower-tier page links to a higher-tier page in any built book | Failure. Exit status `1`. |
| A lower-tier page names the title of a higher-tier page (titles of 12 or more characters) | Warning. Review the text and remove the title when it discloses the higher-tier topic. |

`wrs check --json` prints `pages`, `links`, and `mentions`. The check reads the
article region of each built page, so navigation and table-of-contents links
do not count.

## Serve and inspect

Serve the ungated instances and follow requests in the terminal:

```bash
wrs serve
```

`wrs serve` builds any selected instance that has no built site, then starts
the server. Press Ctrl-C to stop the server and remove its container.

| Option | Effect |
|---|---|
| `-d`, `--dev` | Open the dev gate and serve every tier locally. |
| `-b`, `--background` | Run in the background. Stop with `wrs stop`. |
| `--build` | Rebuild the selected instances before serving. |
| `--port-base N` | Portal port. Instances use the following ports. |
| `--lan` | Expose the ungated instances and the portal on all interfaces. |
| `--lan-all` | With `--dev`, also expose gated instances on all interfaces behind HTTP basic authentication. |
| `--password-manager NAME` | With `--dev`, read the dev key from `bitwarden` or `1password`. |

Serving rules:

1. Without `--dev`, `wrs serve` serves every instance below `gated_from`. With
   the default configuration: `public` and `internal`.
2. Naming a gated instance without `--dev` exits with status `2`.
3. `--lan-all` without `--dev` exits with status `2`.
4. A gated instance exposed by `--lan-all` requires the user name `wrs-dev`
   and the current dev key as the password. The health endpoint stays open.

Ports: the portal listens on the port base (default `44190`). Each instance
listens on the port base plus one plus its sensitivity rank: `public` 44191,
`internal` 44192, `restricted` 44193, `confidential` 44194. Every port binds
to `127.0.0.1` unless `--lan` or `--lan-all` applies.

Cross-instance routing:

1. A page published by the requested instance is served from that instance.
2. A page published only by a lower-sensitivity instance redirects to the
   highest such instance being served, preserving the query string.
3. A page published only by a higher-sensitivity instance returns the same
   404 page as a missing page, so the lower instance does not reveal it.

Inspect rendered output:

1. Open the portal or an instance:

   ```bash
   wrs open internal
   ```

2. Check `wrs status` for build results, page counts, and served URLs.
3. Read `wrs logs --serve -f` for the server access log.

## Open the dev gate

The dev gate is one local key for the whole documentation set. It has no
per-tier permissions. Production access control needs a separate
role-based credential service.

```bash
wrs serve --dev
```

Select the password manager:

| Manager | `dev_item` | Sign-in |
|---|---|---|
| Bitwarden | Item name, default `wrs-dev` | `bw login` once. `wrs` reuses the session in the login keyring, or `BW_SESSION`, and prompts for the master password when the vault is locked. |
| 1Password | `op://<vault>/<item>`, or an item name in the default vault | `op account add` once, or desktop app integration. `wrs` runs `op signin` when no session is active; `op` prompts for the password or asks the app for approval. |

Gate behavior:

1. `wrs` reads the dev key from the login keyring. A cached key from the
   selected manager and item, younger than 21 days, opens the gate without a
   prompt.
2. Without a usable cached key, `wrs` signs in to the password manager and
   reads the item.
3. On first use, `wrs` creates the login item with user name `wrs-dev`, a
   random key as the password, and a `WRS_DEV_KEY_CREATED` field.
4. A key 21 days old or older rotates. Rotation requires a fresh sign-in to
   the password manager. `wrs` writes the new key to the item and caches it in
   the keyring.
5. `wrs` sends item values to the password manager on standard input. The
   master password, session tokens, and the dev key never appear in command
   arguments or plain-text files.
6. A spinner shows each vault step on a terminal and clears before every
   prompt.

| Command | Effect |
|---|---|
| `wrs key status` | Show the password manager, the item, and the cached key's creation time and days until rotation. |
| `wrs key rotate` | Rotate the key now. Requires a fresh sign-in. |
| `wrs key lock` | Remove the cached key from the login keyring. The next `--dev` run signs in again. |

`wrs key` accepts `--password-manager NAME`.

## Maintain

| Command | Effect |
|---|---|
| `wrs status` | Build result, build time, pages, and URL for each instance. |
| `wrs logs` | List recent build logs. `wrs logs <instance>` prints the newest log for an instance; `-f` follows it. |
| `wrs stop` | Stop this project's server. `--all` stops every `wrs` server. |
| `wrs clean` | Remove temporary source copies, exited `wrs` containers, and logs beyond the newest 40. |
| `wrs clean --all` | Also remove built sites, artifacts, logs, and server files for the project. |
| `wrs update` | Compare the configured image with the newest dated tag on Docker Hub. |

## Builder behavior

Verified with builder `2026.08.0328` on rootless Podman 4.9.3:

- The builder exits `0` after a passing build and `255` when a check fails.
  Treat every non-zero status as failure.
- The log contains a JCEF sandbox line with
  `LoggedError ... ELEVATED_PRIVILEGES` on rootless Podman. The line does not
  affect the build result.
- `report.json` in the output directory records `testsTotal`,
  `testsErrorsCount`, and `testsWarningsCount`. `wrs` also fails an instance
  on any `Inspection failed:` log line.
- The builder writes `.idea/` files into its source directory. Build from a
  copy; a read-only source mount can hang at shutdown.
- Mount a parent directory and set `OUTPUT_DIR` to a child path. The builder
  deletes and recreates `OUTPUT_DIR`.
- `IS_GROUP=true` with `cfg/build-groups.xml` merges instances into one
  website. `wrs` builds instances separately to keep each sensitivity level in
  its own site.

## Official references

- https://www.jetbrains.com/help/writerside/build-with-docker.html
- https://www.jetbrains.com/help/writerside/build-groups.html
- https://www.jetbrains.com/help/writerside/build-and-publish.html
- https://www.jetbrains.com/help/writerside/local-build.html
- https://hub.docker.com/r/jetbrains/writerside-builder/tags
- https://bitwarden.com/help/cli/
- https://www.1password.dev/cli/reference/management-commands/item
