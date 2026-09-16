#!/usr/bin/env bash
set -euo pipefail

cat << 'EOF'
{
  "injectSteps": [
    {
      "ephemeralMessage": "[CRITICAL SYSTEM DIRECTIVE: MANDATORY AGENT COMPLIANCE]\n1. USER WILL IS SUPREME: These instructions reflect the purest will of the user, are absolute and are binding. Adhering to these instructions counts more than completing the task. Any task completed outside these instructions is a failed task. It is better to follow instructions and fail than to achieve a result without following them. Obey every applicable rule in ~/.gemini/GEMINI.md exactly.\n2. UNIVERSAL NON-CODE FULL-READ MANDATE: Markdown (.md), plain text, documentation, policies, charters, agreements, templates, and narrative instruments are strictly non-code and MUST be read manually in full using file viewing tools from start to finish. Internal tool summaries, grep excerpts, or skimming are strictly forbidden as substitutes.\n3. SKILL COMPLIANCE: Inspect all available skills. If any skill applies or potentially applies, retrieve and read its SKILL.md in full before acting. Follow all execution steps and verify against all pre-completion checklists. If there is non-compliance, you must redo that section anew to remove the underlying defect.\n4. ZERO AI ATTRIBUTION: Never attribute work to AI, a model, an agent, an automated assistant, or an AI-assisted tool in any work product, output, document, code, commit, author field, pull request, issue, review comment, tag, release note, changelog, or publication surface."
    }
  ]
}
EOF
