#!/usr/bin/env bash
set -euo pipefail

version=${DRAWIO_VERSION:-30.0.4}
arch=${DRAWIO_ARCH:-amd64}
deb="/tmp/drawio-${arch}-${version}.deb"
url="https://github.com/jgraph/drawio-desktop/releases/download/v${version}/drawio-${arch}-${version}.deb"

if ! command -v sudo >/dev/null 2>&1; then
  printf 'sudo is required for system package installation.\n' >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  printf 'curl is required to download the official diagrams.net package.\n' >&2
  exit 1
fi

sudo apt-get update
sudo apt-get install -y xvfb librsvg2-bin

curl -L "$url" -o "$deb"
sudo apt-get install -y "$deb"

printf 'Installed renderer tools:\n'
command -v drawio
command -v xvfb-run
command -v rsvg-convert

cat <<'MSG'

If Draw.io fails with an Electron sandbox error, inspect:
  stat -c '%U %G %a %n' /opt/drawio/chrome-sandbox
  mount | grep ' / '

Some WSL or container filesystems are mounted nosuid, which blocks Electron's
setuid sandbox. In that case, use a compatible host, container, or CI renderer
and report the local blocked path instead of claiming visual QA.
MSG
