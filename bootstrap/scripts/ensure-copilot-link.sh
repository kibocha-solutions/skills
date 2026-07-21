#!/usr/bin/env bash
# bootstrap: ensure ~/.copilot/copilot-instructions.md imports the shared AGENTS.md.
# Copilot CLI's one true global file is copilot-instructions.md; its AGENTS.md
# discovery is project-scoped only, so the global file needs its own pointer.
# Import path must stay relative -- Copilot CLI rejects ~/-prefixed imports.
set -euo pipefail
cat >/dev/null || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

target="$HOME/.copilot/copilot-instructions.md"
import_line="@skills/AGENTS.md"

result="$(ensure_import_line "$target" "$import_line")"
if [ "$result" = "changed" ]; then
  echo "bootstrap: added '$import_line' to $target (was missing)"
fi
exit 0
