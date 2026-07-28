#!/usr/bin/env bash
# bootstrap: ensure AGENTS.md aligns shared AGENTS.md rules non-destructively for Codex CLI.
set -euo pipefail
cat >/dev/null || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

source_agents="$(cd "$dir/../.." && pwd)/AGENTS.md"
if [ ! -f "$source_agents" ]; then
  source_agents="$HOME/.codex/skills/AGENTS.md"
fi

targets=("$HOME/.codex/AGENTS.md")
if [ -d "/mnt/c/Users/codelf/.codex" ]; then
  targets+=("/mnt/c/Users/codelf/.codex/AGENTS.md")
fi

changed=0
for target in "${targets[@]}"; do
  # If target is a symlink, remove the symlink so we can maintain a real file
  if [ -L "$target" ]; then
    rm -f "$target"
  fi
  res="$(align_agent_rules "$target" "$source_agents")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi
done

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules in AGENTS.md (Codex)"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
