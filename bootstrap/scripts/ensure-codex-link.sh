#!/usr/bin/env bash
# bootstrap: ensure AGENTS.md aligns shared AGENTS.md rules non-destructively
# for Codex CLI, and ensure ~/.codex/skills/ is a git sparse checkout
# tracking this repo's remote (not a local rsync copy) — see lib.sh's
# sync_skills_from_git.
set -euo pipefail
[ -t 0 ] || cat >/dev/null 2>&1 || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

repo_root="$(cd "$dir/../.." && pwd)"

remote_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
[ -n "$remote_url" ] || remote_url="git@github.com:kibocha-solutions/skills.git"

mapfile -t targets < <(get_target_paths ".codex" "AGENTS.md")

changed=0
for target in "${targets[@]}"; do
  # If target is a symlink, remove the symlink so we can maintain a real file
  if [ -L "$target" ]; then
    rm -f "$target"
  fi

  skills_dir="$(dirname "$target")/skills"

  # Codex ships its own bundled skills under skills/.system/ —
  # sync_skills_from_git only ever manages paths it tracks (this repo's
  # skill directories plus AGENTS.md), so .system/ is left untouched.
  res="$(sync_skills_from_git "$skills_dir" "$remote_url" "main" "$repo_root")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi

  source_agents="$skills_dir/AGENTS.md"
  if [ ! -f "$source_agents" ]; then
    source_agents="$repo_root/AGENTS.md"
  fi
  if [ ! -f "$source_agents" ]; then
    source_agents="$HOME/.codex/skills/AGENTS.md"
  fi

  res="$(align_agent_rules "$target" "$source_agents")"
  if [ "$res" = "changed" ]; then
    changed=1
  fi
done

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules and skills in AGENTS.md (Codex)"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
