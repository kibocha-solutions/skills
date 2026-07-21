#!/usr/bin/env bash
# bootstrap: ensure ~/.claude/CLAUDE.md imports the shared AGENTS.md.
# Claude Code never reads AGENTS.md natively; this is the pointer it needs.
set -euo pipefail
cat >/dev/null || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

target="$HOME/.claude/CLAUDE.md"
import_line="@skills/AGENTS.md"

result="$(ensure_import_line "$target" "$import_line")"
if [ "$result" = "changed" ]; then
  echo "bootstrap: added '$import_line' to $target (was missing)"
fi
exit 0
