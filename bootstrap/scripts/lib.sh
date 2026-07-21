#!/usr/bin/env bash
# Shared helper for the bootstrap link-check scripts.
# ensure_import_line <target-file> <import-line>
# Prepends import-line (plus a blank line) to target if not already present.
# Prints "changed" or "unchanged" to stdout; never fails the caller.
ensure_import_line() {
  local target="$1" import_line="$2"
  mkdir -p "$(dirname "$target")"
  touch "$target"

  if grep -qxF "$import_line" "$target" 2>/dev/null; then
    echo "unchanged"
    return 0
  fi

  { echo "$import_line"; echo; cat "$target"; } > "$target.tmp" && mv "$target.tmp" "$target"
  echo "changed"
}
