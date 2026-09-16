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

  # Prune redundant AGENTS.md in host directory when target is not AGENTS.md
  local target_dir target_base
  target_dir="$(dirname "$target")"
  target_base="$(basename "$target")"
  if [ "$target_base" != "AGENTS.md" ] && [ -f "$target_dir/AGENTS.md" ]; then
    rm -f "$target_dir/AGENTS.md"
  fi

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
    # Replace existing block between start_marker and end_marker. Uses the
    # FIRST start-marker index and the LAST end-marker index (not a regex
    # .*? span) because the rules content itself can legitimately quote
    # these exact marker strings as documentation (e.g. AGENTS.md's own
    # Tooling and Dependencies section does) — a non-greedy regex match
    # would stop at that literal mention instead of the real closing
    # marker, truncating everything after it and making this non-idempotent.
    python3 -c '
import sys
target, source_file, start_m, end_m, tmp_file = sys.argv[1:]
with open(source_file, "r", encoding="utf-8") as f:
    shared_rules = f.read()

replacement = f"{start_m}\n{shared_rules}\n{end_m}"

with open(target, "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find(start_m)
end_idx = content.rfind(end_m)
if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
    new_content = content[:start_idx] + replacement + content[end_idx + len(end_m):]
else:
    new_content = content

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

# sync_skills_from_git <target-dir> <remote-url> [branch] [local-repo-root]
# Makes target-dir a sparse, partial git working copy tracking
# origin/<branch> (default: main) of remote-url, materializing only
# AGENTS.md plus top-level directories that contain a SKILL.md — no other
# repo-root files (README.md, migration-log.md, docs/, sources/, etc.) are
# checked out. Every run does `fetch` + sparse-checkout re-apply +
# `reset --hard origin/<branch>`, so target-dir always exactly matches the
# remote — no local drift, no merge conflicts possible, and a skill removed
# from the repo is automatically removed from target-dir too (sparse-checkout
# re-application drops paths that fall out of the pattern set).
#
# Uses `git init` in place rather than `git clone`, specifically so this
# works when target-dir already has unrelated content sitting alongside
# where the skills belong (e.g. a tool's own bundled/native skills) — `git
# clone` refuses a non-empty directory, `git init` does not, and git only
# ever manages paths in its own tracked tree, leaving untracked neighbors
# alone.
#
# If target-dir isn't a git repo yet and local-repo-root is given, first
# removes any existing top-level entry whose name matches a skill folder in
# local-repo-root (i.e. leftover content from the old rsync-based mirror)
# so the initial checkout has no stale collisions to contend with. Anything
# whose name doesn't match a known skill (a tool's own native content) is
# left untouched.
#
# Prints "changed" or "unchanged" to stdout; never fails the caller.
sync_skills_from_git() {
  local target="$1" remote="$2" branch="${3:-main}" local_repo_root="${4:-}"

  command -v git >/dev/null 2>&1 || { echo "unchanged"; return 0; }
  mkdir -p "$target"

  local before=""
  if [ -d "$target/.git" ]; then
    before="$(git -C "$target" rev-parse HEAD 2>/dev/null || echo "")"
  else
    if [ -n "$local_repo_root" ] && [ -d "$local_repo_root" ]; then
      local skill_dir skill_name
      for skill_dir in "$local_repo_root"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name="$(basename "$skill_dir")"
        [ -e "$target/$skill_name" ] && rm -rf "$target/$skill_name"
      done
      [ -f "$target/AGENTS.md" ] && [ ! -L "$target/AGENTS.md" ] && rm -f "$target/AGENTS.md"
    fi
    git -C "$target" init --quiet >/dev/null 2>&1
    git -C "$target" remote add origin "$remote" >/dev/null 2>&1 \
      || git -C "$target" remote set-url origin "$remote" >/dev/null 2>&1
    # Non-cone mode: cone mode always includes root-level files regardless
    # of the directory pattern list (README.md, LICENSE.txt, .gitignore,
    # etc. would leak through). Non-cone gives exact, explicit-only paths.
    git -C "$target" sparse-checkout init --no-cone >/dev/null 2>&1
  fi

  git -C "$target" fetch --quiet --filter=blob:none origin "$branch" 2>/dev/null \
    || { echo "unchanged"; return 0; }

  local skill_dirs pattern_args=("/AGENTS.md")
  skill_dirs="$(git -C "$target" ls-tree -r --name-only "origin/$branch" \
    | grep '/SKILL\.md$' \
    | sed 's#/SKILL\.md$##' \
    | cut -d/ -f1 \
    | sort -u)"
  local d
  while IFS= read -r d; do
    [ -n "$d" ] && pattern_args+=("/$d/")
  done <<< "$skill_dirs"

  git -C "$target" sparse-checkout set --no-cone "${pattern_args[@]}" >/dev/null 2>&1
  git -C "$target" checkout --quiet -B "$branch" "origin/$branch" >/dev/null 2>&1
  git -C "$target" reset --quiet --hard "origin/$branch" >/dev/null 2>&1

  local after
  after="$(git -C "$target" rev-parse HEAD 2>/dev/null || echo "")"

  if [ "$before" != "$after" ]; then
    echo "changed"
  else
    echo "unchanged"
  fi
}
