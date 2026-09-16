#!/usr/bin/env bash
# bootstrap: ensure GEMINI.md aligns shared AGENTS.md rules non-destructively,
# ensure ~/.gemini/skills/ is a git sparse checkout tracking this repo's
# remote (not a local rsync copy), and ensure Antigravity discovers it via
# ~/.gemini/config/skills.json and symlinks.
#
# This unifies both Gemini CLI and Gemini Antigravity under ~/.gemini/skills/
# and ~/.gemini/GEMINI.md. Antigravity's own internal builtin directory
# (~/.gemini/antigravity/builtin/) is left clean and never mutated.
set -euo pipefail
[ -t 0 ] || cat >/dev/null 2>&1 || true

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$dir/lib.sh"

repo_root="$(cd "$dir/../.." && pwd)"

remote_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
[ -n "$remote_url" ] || remote_url="git@github.com:kibocha-solutions/skills.git"

gemini_product_present() {
  local home_dir="$1"
  command -v gemini >/dev/null 2>&1 && return 0
  [ -f "$home_dir/.gemini/settings.json" ] && return 0
  [ -d "$home_dir/.gemini/hooks" ] && return 0
  [ -d "$home_dir/.gemini/antigravity" ] && return 0
  [ -d "$home_dir/.gemini/config" ] && return 0
  return 1
}

mapfile -t targets < <(get_target_paths ".gemini" "GEMINI.md")

changed=0
for target in "${targets[@]}"; do
  target_home="$(dirname "$(dirname "$target")")"
  gemini_product_present "$target_home" || continue

  gemini_dir="$(dirname "$target")"
  skills_dir="$gemini_dir/skills"

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

  # Explicitly prune redundant AGENTS.md in Gemini root
  if [ -f "$gemini_dir/AGENTS.md" ]; then
    rm -f "$gemini_dir/AGENTS.md"
    changed=1
  fi

  # Configure Antigravity discovery if Antigravity is present
  config_dir="$gemini_dir/config"
  if [ -d "$gemini_dir/antigravity" ] || [ -d "$config_dir" ]; then
    mkdir -p "$config_dir"
    
    # 1. Ensure config/skills symlink exists
    if [ ! -e "$config_dir/skills" ]; then
      ln -s "$skills_dir" "$config_dir/skills"
      changed=1
    fi

    # 2. Ensure config/skills.json explicitly registers the skills path
    skills_json="$config_dir/skills.json"
    if [ ! -f "$skills_json" ] || ! grep -q "$skills_dir" "$skills_json" 2>/dev/null; then
      python3 -c '
import json, os, sys
path, target_dir = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        data = {}
entries = data.get("entries", [])
paths = [e.get("path") for e in entries if isinstance(e, dict)]
if target_dir not in paths:
    entries.append({"path": target_dir})
data["entries"] = entries
with open(path, "w") as f:
    json.dump(data, f, indent=2)
' "$skills_json" "$skills_dir"
      changed=1
    fi

    # 3. Clean up any legacy mutation in antigravity/builtin
    builtin_skills="$gemini_dir/antigravity/builtin/skills"
    if [ -d "$builtin_skills/.git" ]; then
      rm -rf "$builtin_skills/.git"
      changed=1
    fi
    if [ -f "$gemini_dir/antigravity/builtin/GEMINI.md" ]; then
      rm -f "$gemini_dir/antigravity/builtin/GEMINI.md"
      changed=1
    fi
  fi
done

if [ "$changed" -eq 1 ]; then
  MSG="bootstrap: aligned shared rules and skills in GEMINI.md and configured Antigravity"
  MSG="$MSG" python3 -c '
import json, os
print(json.dumps({"systemMessage": os.environ.get("MSG", ""), "suppressOutput": False}))
' 2>/dev/null || echo '{"suppressOutput": true}'
else
  echo '{"suppressOutput": true}'
fi
exit 0
