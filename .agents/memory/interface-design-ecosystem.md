---
name: interface-design-ecosystem
description: Architecture of the three-skill interface ecosystem (interface-design, web-design, mobile-app-design) and autonomous multi-agent MCP onboarding
type: project
---

The design capability in this repository is structured into a two-tier, three-skill ecosystem:

1. `interface-design`: Master entry skill. Establishes the design brief, taste dials (density and variance 1 to 10), platform design system selection (Apple HIG vs Material 3 Expressive vs Web Synthesis), anti-slop rules, and outputs the `DESIGN.md` token contract.
2. `web-design`: Replaces `frontend-design`. Specializes in production web and responsive web app implementation using semantic HTML, CSS custom properties, container queries, fluid typography, WCAG 2.2 AA accessibility, and Emil Kowalski spring motion.
3. `mobile-app-design`: Specializes in mobile phone and tablet applications across both portrait and landscape orientations, safe area insets, touch hit areas (44pt Apple, 48dp M3), and tactile gestures.

When a task requires Figma or Playwright, the agent autonomously inspects and configures the host MCP settings across Claude Code (`settings.json`), Codex (`config.toml`), Gemini Antigravity (`mcp_config.json`), Gemini CLI (`settings.json`), or GitHub Copilot, pausing only for user token authentication.
