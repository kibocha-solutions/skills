#!/usr/bin/env bash
# bootstrap: mirror this repo's skill folders into Gemini Antigravity's
# builtin skills directory, overwriting per-skill so `git pull` updates in
# this repo propagate on the next run. Antigravity's own native skills
# (anything not present in this repo) are left untouched.
set -euo pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"
repo_root="$(cd "$dir/../.." && pwd)"

target_base="$HOME/.gemini/antigravity/builtin/skills"

if [ ! -d "$target_base" ]; then
  echo '{"suppressOutput": true}'
  exit 0
fi

res="$(mirror_skills "$target_base" "$repo_root")"

if [ "$res" = "changed" ]; then
  MSG="bootstrap: synced builtin skills in Gemini Antigravity"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
