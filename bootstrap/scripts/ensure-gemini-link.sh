#!/usr/bin/env bash
# bootstrap: ensure ~/.gemini/GEMINI.md imports the shared AGENTS.md (Gemini CLI hook).
# Gemini CLI defaults to GEMINI.md and does not read AGENTS.md on its own;
# this is the pointer it needs.
# Contract: must print ONLY JSON on stdout. Logs go to stderr. Never blocks.
set -euo pipefail
cat >/dev/null || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

target="$HOME/.gemini/GEMINI.md"
import_line="@skills/AGENTS.md"

result="$(ensure_import_line "$target" "$import_line")" || result="unchanged"

if [ "$result" = "changed" ]; then
  MSG="bootstrap: added '$import_line' to $target (was missing)"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
