#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s SOURCE.drawio OUTPUT.(svg|png|pdf) [--format svg|png|pdf]\n' "$0" >&2
}

if [ "$#" -lt 2 ]; then
  usage
  exit 2
fi

source_file=$1
output_file=$2
format=${3:-}

if [ ! -f "$source_file" ]; then
  printf 'Source file not found: %s\n' "$source_file" >&2
  exit 2
fi

case "$output_file" in
  *.svg) inferred_format=svg ;;
  *.png) inferred_format=png ;;
  *.pdf) inferred_format=pdf ;;
  *)
    printf 'Output extension must be .svg, .png, or .pdf: %s\n' "$output_file" >&2
    exit 2
    ;;
esac

if [ -n "$format" ]; then
  if [ "$format" != "--format" ] || [ "$#" -ne 4 ]; then
    usage
    exit 2
  fi
  inferred_format=$4
fi

case "$inferred_format" in
  svg|png|pdf) ;;
  *)
    printf 'Unsupported format: %s\n' "$inferred_format" >&2
    exit 2
    ;;
esac

renderer=
for candidate in drawio-cli drawio diagrams.net diagramsnet; do
  if command -v "$candidate" >/dev/null 2>&1; then
    renderer=$candidate
    break
  fi
done

if [ -z "$renderer" ]; then
  cat >&2 <<'MSG'
No compatible Draw.io renderer found.

Expose one of these existing commands before production diagram handoff:
  drawio-cli
  drawio
  diagrams.net
  diagramsnet

Check project, host, container, and CI render commands. Apply the dependency
installation procedure in system-init when the renderer is required. Report
source-only validation and do not claim rendered visual QA while no renderer
is available.
MSG
  exit 127
fi

mkdir -p "$(dirname "$output_file")"

runner=()
if command -v xvfb-run >/dev/null 2>&1; then
  runner=(xvfb-run -a)
fi

set +e
"${runner[@]}" "$renderer" \
  --export \
  --format "$inferred_format" \
  --output "$output_file" \
  "$source_file"
status=$?
set -e

if [ "$status" -ne 0 ]; then
  cat >&2 <<'MSG'
Draw.io rendering failed after a compatible command was found.

Check:
  - whether xvfb is installed when running headless
  - whether the filesystem blocks the Electron setuid sandbox with nosuid
  - whether /opt/drawio/chrome-sandbox has usable ownership and permissions
  - whether a project, CI image, container, or host command provides an
    alternate diagrams.net renderer

Do not change sandbox permissions, mounts, services, or system packages.
Report the failed command and error. Do not claim rendered visual QA.
MSG
  exit "$status"
fi

printf 'Rendered %s -> %s using %s\n' "$source_file" "$output_file" "$renderer"
