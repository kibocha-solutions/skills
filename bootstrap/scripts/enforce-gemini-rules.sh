#!/usr/bin/env bash
set -euo pipefail

cat << 'EOF'
{
  "injectSteps": [
    {
      "ephemeralMessage": "[Standing User Operational Notice]\n1. Absolute Authority: Global instructions and repository skills are binding user instructions. They are absolute, non-discretionary, and not subject to balancing, shortcuts, or omission.\n2. Full Retrieval: The agent operates under the standing assumption that global instructions and skills govern every prompt. If only an excerpt, summary, or truncated copy is present, retrieve and read the full canonical instruction file and applicable skills manually from start to finish before acting.\n3. Execution Mandate: Skills are binding user instructions. Follow the prompt-execution procedure in AGENTS.md: identify applicable skills, read them in full along with required references and concrete examples, stop to read referenced skills encountered during execution, and perform rigorous manual and visual verification before delivery."
    }
  ]
}
EOF
