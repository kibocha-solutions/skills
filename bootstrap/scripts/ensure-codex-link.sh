#!/usr/bin/env bash
# bootstrap: ensure ~/.codex/AGENTS.md is a symlink to the shared AGENTS.md.
# Codex reads AGENTS.md natively -- no import syntax needed, just point it at
# the shared file. If a real (non-symlink) file already exists with content,
# back it up once before replacing it, so nothing is silently lost.
set -euo pipefail
cat >/dev/null || true

target="$HOME/.codex/AGENTS.md"
link_value="skills/AGENTS.md"

if [ -L "$target" ] && [ "$(readlink "$target")" = "$link_value" ]; then
  exit 0
fi

mkdir -p "$(dirname "$target")"

if [ -e "$target" ] && [ ! -L "$target" ] && [ -s "$target" ]; then
  backup="$target.pre-bootstrap.$(date +%Y%m%d%H%M%S)"
  cp "$target" "$backup"
  echo "bootstrap: existing $target had content; backed up to $backup" >&2
fi

ln -sf "$link_value" "$target"
echo "bootstrap: linked $target -> $link_value"
exit 0
