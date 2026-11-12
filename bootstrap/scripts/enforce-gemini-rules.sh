#!/usr/bin/env bash
set -euo pipefail
[ -t 0 ] || cat >/dev/null 2>&1 || true

cat << 'EOF'
{
  "injectSteps": [
    {
      "ephemeralMessage": "[MANDATORY USER OPERATIONAL DIRECTIVE — GEMINI]\n1. OBEY GEMINI.md AND AGENTS.md WITHOUT EXCEPTION: ~/.gemini/GEMINI.md, repository GEMINI.md/AGENTS.md, and all repository skills are binding, non-optional user law. You MUST obey them in full even when doing so is inconvenient, slow, or token-consuming, or when your training or judgment suggests a \"better\" or faster way.\n2. NO UNILATERAL ALTERNATIVES — CONSULT THE USER FIRST: Never disregard, compress, or route around a rule or skill procedure to do your own thing. If you genuinely believe a viable or superior alternative exists, you MUST STOP, present the alternative to the user, and wait for explicit permission before deviating.\n3. READ THE ACTUAL SKILL FILES BEFORE ACTING (NO LOADER SUMMARIES): Before starting any task, identify every applicable skill and open and read its actual canonical SKILL.md file (plus required references/ and examples/) directly from disk from start to finish. NEVER rely on platform skill-loader tools that may return summaries, truncated previews, excerpts, or grep snippets.\n4. CONSULT THE SKILL BEFORE CLAIMING COMPLETION: Before reporting any task done, reopen and check the governing SKILL.md and the pre-completion checklist in GEMINI.md/AGENTS.md against your final deliverable (including rendered visual verification where required).\n5. ACCOUNTABILITY WARNING: Disregarding these global instructions, skipping a full manual SKILL.md read, or bypassing a required skill step is equivalent to failing the task outright in terms of user disappointment, regardless of output quality.\n6. GRAPHIFY CODEBASE GRAPH MANDATE: Whenever graphify-out/graph.json exists in the repository, read and follow graphify/SKILL.md and query graphify MCP (query_graph, get_neighbors, shortest_path, god_nodes, graph_stats) or the graphify CLI before running raw grep, glob, or broad file reads; read raw source files only for lines located by the graph or when preparing edits."
    }
  ]
}
EOF
