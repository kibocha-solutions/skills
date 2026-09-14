#!/usr/bin/env bash
# bootstrap: ensure GEMINI.md aligns shared AGENTS.md rules non-destructively,
# and ensure ~/.gemini/skills/ is a git sparse checkout tracking this repo's
# remote (not a local rsync copy) — see lib.sh's sync_skills_from_git.
#
# This targets standalone Gemini CLI, which reads ~/.gemini/GEMINI.md and
# ~/.gemini/skills/ directly. Gemini Antigravity is a separate product with
# its own target (ensure-gemini-builtin-skills.sh) and does not read this
# location. On a machine that only has Antigravity installed — no `gemini`
# binary and no prior ~/.gemini/settings.json or ~/.gemini/hooks/ — there is
# no real Gemini CLI product to serve here, so this script skips the root
# target entirely rather than maintaining an unused, easily-stale copy.
set -euo pipefail
cat >/dev/null || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

repo_root="$(cd "$dir/../.." && pwd)"

remote_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
[ -n "$remote_url" ] || remote_url="git@github.com:kibocha-solutions/skills.git"

gemini_cli_present() {
  local home_dir="$1"
  command -v gemini >/dev/null 2>&1 && return 0
  [ -f "$home_dir/.gemini/settings.json" ] && return 0
  [ -d "$home_dir/.gemini/hooks" ] && return 0
  return 1
}

mapfile -t targets < <(get_target_paths ".gemini" "GEMINI.md")

changed=0
for target in "${targets[@]}"; do
  target_home="$(dirname "$(dirname "$target")")"
  gemini_cli_present "$target_home" || continue

  skills_dir="$(dirname "$target")/skills"

  res="$(sync_skills_from_git "$skills_dir" "$remote_url" "main" "$repo_root")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi

  source_agents="$skills_dir/AGENTS.md"
  if [ ! -f "$source_agents" ]; then
    source_agents="$repo_root/AGENTS.md"
  fi
  if [ ! -f "$source_agents" ]; then
    source_agents="$HOME/.gemini/skills/AGENTS.md"
  fi

  res="$(align_agent_rules "$target" "$source_agents")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi
done

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules and skills in GEMINI.md"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
