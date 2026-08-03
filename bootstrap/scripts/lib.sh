#!/usr/bin/env bash
# Shared helper for the bootstrap alignment scripts.
# align_agent_rules <target-file> <source-agents-file>
# Safely embeds or updates the shared AGENTS.md rules inside target-file using
# HTML comment delimiters, preserving any existing custom user instructions.
# Prints "changed" or "unchanged" to stdout; never fails the caller.

get_target_paths() {
  local tool="$1"      # e.g., ".claude"
  local filename="$2"  # e.g., "CLAUDE.md"
  local paths=("$HOME/$tool/$filename")

  # Detect WSL / Windows Host User Profile dynamically without hardcoding usernames
  if [ -d "/mnt/c/Users" ]; then
    local win_user=""
    if command -v cmd.exe >/dev/null 2>&1; then
      win_user="$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r\n')"
    fi
    if [ -z "$win_user" ] && [ -n "${USER:-}" ]; then
      win_user="$USER"
    fi
    if [ -n "$win_user" ] && [ -d "/mnt/c/Users/$win_user/$tool" ]; then
      paths+=("/mnt/c/Users/$win_user/$tool/$filename")
    fi
  fi

  printf "%s\n" "${paths[@]}"
}

align_agent_rules() {
  local target="$1" source="$2"
  if [ ! -f "$source" ]; then
    echo "unchanged"
    return 0
  fi

  mkdir -p "$(dirname "$target")"
  touch "$target"

  local start_marker="<!-- BEGIN SHARED SKILLS RULES -->"
  local end_marker="<!-- END SHARED SKILLS RULES -->"

  # Remove legacy import pointer line if present
  if grep -qxF "@skills/AGENTS.md" "$target" 2>/dev/null; then
    sed -i '/^@skills\/AGENTS\.md$/d' "$target"
  fi

  local rules_content
  rules_content="$start_marker"$'\n'"$(cat "$source")"$'\n'"$end_marker"

  local tmp_file
  tmp_file="$(mktemp)"

  if grep -qF "$start_marker" "$target" 2>/dev/null && grep -qF "$end_marker" "$target" 2>/dev/null; then
    # Replace existing block between start_marker and end_marker
    python3 -c '
import sys
target, source_file, start_m, end_m, tmp_file = sys.argv[1:]
with open(source_file, "r", encoding="utf-8") as f:
    shared_rules = f.read()

replacement = f"{start_m}\n{shared_rules}\n{end_m}"

with open(target, "r", encoding="utf-8") as f:
    content = f.read()

import re
pattern = re.escape(start_m) + r".*?" + re.escape(end_m)
new_content = re.sub(pattern, lambda m: replacement, content, flags=re.DOTALL)

with open(sys.argv[5], "w", encoding="utf-8") as f:
    f.write(new_content)
' "$target" "$source" "$start_marker" "$end_marker" "$tmp_file"
  else
    # Append block to end of file
    cp "$target" "$tmp_file"
    if [ -s "$tmp_file" ] && [ "$(tail -c 1 "$tmp_file" | wc -l)" -eq 0 ]; then
      echo "" >> "$tmp_file"
    fi
    echo "$rules_content" >> "$tmp_file"
  fi

  if cmp -s "$target" "$tmp_file"; then
    rm -f "$tmp_file"
    echo "unchanged"
    return 0
  else
    mv "$tmp_file" "$target"
    echo "changed"
    return 0
  fi
}

# mirror_skills <target-skills-dir> <repo-root>
# Mirrors every top-level skill (any directory with a SKILL.md) from the
# skills repo into target-skills-dir, overwriting each skill by name so repo
# updates propagate on the next run. Anything already in target-skills-dir
# that isn't a skill folder name from this repo (e.g. a tool's own bundled
# skills) is left untouched. Prints "changed" or "unchanged"; never fails the
# caller.
mirror_skills() {
  local target_base="$1" repo_root="$2"
  command -v rsync >/dev/null 2>&1 || { echo "unchanged"; return 0; }
  mkdir -p "$target_base"

  local changed=0 skill_dir skill_name target out
  for skill_dir in "$repo_root"/*/; do
    skill_name="$(basename "$skill_dir")"
    [ -f "$skill_dir/SKILL.md" ] || continue
    target="$target_base/$skill_name"
    mkdir -p "$target"
    out="$(rsync -a --delete --checksum --itemize-changes "$skill_dir" "$target/")"
    if [ -n "$out" ]; then
      changed=1
    fi
  done

  if [ "$changed" -eq 1 ]; then
    echo "changed"
  else
    echo "unchanged"
  fi
}
