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

Install or expose one of these commands before production diagram handoff:
  drawio-cli
  drawio
  diagrams.net
  diagramsnet

Do not stop at this missing-command failure. Try installing a compatible
diagrams.net renderer and headless support such as xvfb before falling back.
Render-backed visual QA is required for production diagrams. If installation
and compatible replacement are genuinely impossible, report source-only
validation instead of claiming visual QA, and name the setup attempts.
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

Do not treat this as a source-only validation pass yet. Check:
  - whether xvfb is installed when running headless
  - whether the filesystem blocks the Electron setuid sandbox with nosuid
  - whether /opt/drawio/chrome-sandbox has usable ownership and permissions
  - whether a project, CI image, container, or host command provides an
    alternate diagrams.net renderer

Only report source-only validation after those setup paths are genuinely
blocked, and include the failed command and error.
MSG
  exit "$status"
fi

printf 'Rendered %s -> %s using %s\n' "$source_file" "$output_file" "$renderer"
