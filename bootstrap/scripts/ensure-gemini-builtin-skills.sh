#!/usr/bin/env bash
# bootstrap: align shared AGENTS.md rules and sync this repo's skill folders
# into Gemini Antigravity's own builtin directory via git (not rsync) — see
# lib.sh's sync_skills_from_git. Antigravity is a separate product from
# Gemini CLI and does not read ~/.gemini/GEMINI.md or ~/.gemini/skills/ — it
# reads ~/.gemini/antigravity/builtin/ instead, so this script gives it its
# own copy of both rather than relying on the Gemini CLI location
# ensure-gemini-link.sh maintains. Antigravity's own native skills (anything
# not present in this repo) are left untouched.
set -euo pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"
repo_root="$(cd "$dir/../.." && pwd)"

target_base="$HOME/.gemini/antigravity/builtin"

if [ ! -d "$target_base" ]; then
  echo '{"suppressOutput": true}'
  exit 0
fi

remote_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
[ -n "$remote_url" ] || remote_url="git@github.com:kibocha-solutions/skills.git"

changed=0

res="$(sync_skills_from_git "$target_base/skills" "$remote_url" "main" "$repo_root")"
if [ "$res" = "changed" ]; then
  changed=1
fi

source_agents="$target_base/skills/AGENTS.md"
if [ ! -f "$source_agents" ]; then
  source_agents="$repo_root/AGENTS.md"
fi
if [ ! -f "$source_agents" ]; then
  source_agents="$HOME/.gemini/skills/AGENTS.md"
fi

res="$(align_agent_rules "$target_base/GEMINI.md" "$source_agents")"
if [ "$res" = "changed" ]; then
  changed=1
fi

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules and synced builtin skills in Gemini Antigravity"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
