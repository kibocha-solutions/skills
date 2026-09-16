#!/usr/bin/env bash
# bootstrap: ensure CLAUDE.md aligns shared AGENTS.md rules non-destructively,
# and ensure ~/.claude/skills/ is a git sparse checkout tracking this repo's
# remote (not a local rsync copy) — see lib.sh's sync_skills_from_git.
set -euo pipefail
[ -t 0 ] || cat >/dev/null 2>&1 || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

repo_root="$(cd "$dir/../.." && pwd)"

remote_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
[ -n "$remote_url" ] || remote_url="git@github.com:kibocha-solutions/skills.git"

mapfile -t targets < <(get_target_paths ".claude" "CLAUDE.md")

changed=0
for target in "${targets[@]}"; do
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
    source_agents="$HOME/.claude/skills/AGENTS.md"
  fi

  res="$(align_agent_rules "$target" "$source_agents")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi

  # Explicitly prune redundant AGENTS.md in Claude root
  if [ -f "$(dirname "$target")/AGENTS.md" ]; then
    rm -f "$(dirname "$target")/AGENTS.md"
    changed=1
  fi
done

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules and skills in CLAUDE.md"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
