#!/usr/bin/env bash
# bootstrap: legacy forwarder for Gemini Antigravity.
# Direct mutation of ~/.gemini/antigravity/builtin/ is deprecated because
# Antigravity does not discover custom skills from builtin/ (builtin skills are
# mounted explicitly by internal name) and modifying builtin/ corrupts app assets.
# This script forwards execution to ensure-gemini-link.sh, which correctly maintains
# ~/.gemini/skills/, aligns ~/.gemini/GEMINI.md, and registers ~/.gemini/config/skills.json.
set -euo pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$dir/ensure-gemini-link.sh"
