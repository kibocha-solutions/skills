# Renderer Environment

Use this reference when Draw.io rendering tools are missing or fail. Production
diagram work requires an actual Draw.io-compatible render/export path; do not
give up after the first missing command.

## Required Capabilities

A production environment needs:

- a Draw.io-compatible exporter, preferably the official diagrams.net desktop
  CLI command `drawio`
- headless display support, usually `xvfb` on Linux
- SVG preview support such as `rsvg-convert` for inspecting exported SVGs

SVG rasterizers help inspect exports. They do not replace Draw.io export from
`.drawio` source.

## Ubuntu Or WSL Setup

Use `scripts/install-drawio-renderer-ubuntu.sh` from this skill when the target
environment is Ubuntu-like and the user allows system package installation.
The script installs:

- `xvfb`
- `librsvg2-bin`
- the configured official amd64 diagrams.net `.deb` from
  `jgraph/drawio-desktop`; set `DRAWIO_VERSION` to choose a different release

After setup, verify:

```bash
command -v drawio
command -v xvfb-run
command -v rsvg-convert
```

Then render:

```bash
technical-diagrams/scripts/render-drawio.sh source.drawio export.svg
technical-diagrams/scripts/render-drawio.sh source.drawio /tmp/preview.png
```

## Electron Sandbox Failures

In some WSL or container profiles, Draw.io may install but fail with an Electron
sandbox error. Common causes:

- the filesystem is mounted with `nosuid`
- `/opt/drawio/chrome-sandbox` has unusable ownership or permissions
- the container blocks sandbox syscalls
- WSL interop or GUI bridging is disabled

Try these before falling back:

1. Run through `xvfb-run -a`.
2. Check `/opt/drawio/chrome-sandbox` ownership and mode.
3. Check `mount` output for `nosuid`.
4. Check whether a host-side diagrams.net command, project container, or CI
   image can perform the export.
5. Use `rsvg-convert` only to inspect an SVG that already exists.

If every compatible export route is blocked, report source-only validation and
name the exact setup attempts and errors.

## Unacceptable Shortcut

Do not switch to Mermaid because Draw.io setup is inconvenient. The diagram
source remains `.drawio`; the task is to repair the renderer path, use a
compatible Draw.io exporter, or state the blocked validation truthfully.
