#!/usr/bin/env bash
# bootstrap: ensure GEMINI.md aligns shared AGENTS.md rules non-destructively.
set -euo pipefail
cat >/dev/null || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

source_agents="$(cd "$dir/../.." && pwd)/AGENTS.md"
if [ ! -f "$source_agents" ]; then
  source_agents="$HOME/.gemini/skills/AGENTS.md"
fi

targets=("$HOME/.gemini/GEMINI.md")
if [ -d "/mnt/c/Users/codelf/.gemini" ]; then
  targets+=("/mnt/c/Users/codelf/.gemini/GEMINI.md")
fi

changed=0
for target in "${targets[@]}"; do
  res="$(align_agent_rules "$target" "$source_agents")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi
done

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules in GEMINI.md"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
