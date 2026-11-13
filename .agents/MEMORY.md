# Memory Index

Durable, cross-agent knowledge about this repo. Any agent working here —
regardless of tool — should sweep this file (and linked topic files below)
before substantial work. See `maestro/references/memory-conventions.md` for
what belongs here, what doesn't, and how to add an entry.

- [Skills Repo Deployment Workflow](memory/skills-repo-deployment-workflow.md) — rsync mirror topology (not git clones); standard change → commit/amend → push → re-run bootstrap sequence
- [Commit & Destructive-Action Discipline](memory/commit-and-destructive-action-discipline.md) — single-scope 72-word commit rule; enumerate-before-batch-action across repos
- [Gemini Antigravity MCP Registration](memory/gemini-antigravity-mcp-registration.md) - verified config path and `graphify-mcp` setup across workstation hosts
- [wrs dev gate](memory/wrs-dev-gate.md) — one local key in Bitwarden or 1Password, 21-day rotation with fresh sign-in, no TOTP (agreed 2026-09-23); do not re-add gate factors without asking
- [Interface Design Ecosystem](memory/interface-design-ecosystem.md): two-tier three-skill architecture (interface-design, web-design, mobile-app-design) and multi-agent MCP onboarding
- [AGENTS.md Limits & Cross-References](memory/agents-md-limits-and-cross-references.md): 2,500-word cap, preserved §§3-11 numbering (`§9.2`-`§9.14`), and usage threshold separation into `coordinator`
