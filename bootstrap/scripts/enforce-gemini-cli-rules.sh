#!/usr/bin/env bash
set -euo pipefail
[ -t 0 ] || cat >/dev/null 2>&1 || true
# shellcheck source=directive.sh
. "$(dirname "${BASH_SOURCE[0]}")/directive.sh"

# shellcheck disable=SC2088 # literal tilde shown to the agent
print_directive_json "GEMINI CLI" "~/.gemini/GEMINI.md, the repository GEMINI.md and AGENTS.md," "GEMINI.md or AGENTS.md"
