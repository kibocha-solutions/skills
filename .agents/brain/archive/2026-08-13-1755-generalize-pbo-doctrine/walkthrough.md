# Walkthrough — generalize-pbo-doctrine

## Context

`.agents/prompt.md` was a master spec written while the user was handling a
PBO (public benefit organization) governance drafting task. Its doctrines
were sound but PBO-flavored throughout — vocabulary like `Network Identity
Assets`, `Member Organizations`, and example instruments assumed that one
project. The user wanted the reusable doctrine generalized across all
instruments, split by nature: non-legal drafting discipline into
`documentation`, legal-specific technique into `legalese`, PBO vocabulary
stripped entirely and replaced with universal examples.

Separately, the user had hit recurring friction getting the `code-review-graph`
MCP server working under Google Antigravity, evidenced by three separate
archived brain sessions each rediscovering part of the fix from scratch
(`antigravity-mcp-activation`, `graphify-mcp-correction`,
`setup-graphify-mcp`), including one that registered the config at the wrong
path. Asked to find what actually worked and make sure it's captured
permanently.

## Changes

- `documentation/SKILL.md`: added medium identification for Policy/SOP,
  Proposal/CFP, and Memo/correspondence; a general-first/no-redundancy rule;
  extended the existing Documentation Source Boundary section to cover
  authority-context leakage (deliberation records, derivation chains) and
  self-status narration (`Draft`, `Pending Review` inside a filed artifact);
  a new Economy of Disclosure check; and folded the anti-fluff modal-verb note
  and intern-style-justification test into the existing Economy check. Added
  a step 0 pointing at `.agents/memory/` for previously recorded document
  structure conventions.
- `legalese/SKILL.md`: added the settled-legal-class-over-domain-stacking
  technique to Doctrine 2, and a preamble-vs-operative structural placement
  note to Doctrine 3 — both with universal examples (`Marks`, `Personnel`),
  no PBO vocabulary. Doctrine count and cross-references (CoLT steps,
  post-drafting checklist) were left untouched since nothing was renumbered.
- `AGENTS.md`: one bullet in the Maestro section pointing agents at
  `.agents/memory/` for document/instrument structural conventions before
  re-deriving them — reuses the existing memory mechanism rather than
  inventing the parallel `.agents/document_structures/` registry the
  original spec proposed.
- `.agents/memory/gemini-antigravity-mcp-registration.md` (new): records the
  verified-working MCP config path
  (`~/.gemini/antigravity/mcp_config.json`, not `builtin/`, not
  `antigravity-cli/`) and command shape (`uvx code-review-graph serve`, not
  a bare pipx shim), found by cross-referencing the live `~/.gemini/` and
  `~/.codex/config.toml` state against the three archived sessions.
- `graphify/assets/mcp-config-template.json` and
  `graphify/references/environment-setup.md`: updated to the verified shape
  (`uv tool install`, `uvx ... serve` invocation) so new setups don't
  reproduce the pipx/bare-command failure.
- `.agents/memory/skills-repo-deployment-workflow.md`: fixed — it still
  described the tool `skills/` mirrors as an `rsync` copy; the mechanism
  changed to a real git sparse-checkout in commit `22e61fb`, found while
  reading this file for the propagation step.

## Verification

- `python3 -m json.tool` on the edited MCP config template: valid.
- Confirmed live `~/.gemini/antigravity/mcp_config.json` on this workstation
  already matches the documented working shape — no live config change was
  needed, only the durable record was missing.
- Three commits pushed to `origin/main` (single scope each, per
  `ci-cd/SKILL.md` Commit Hygiene Expectations): `14be961` (documentation),
  `4bb1572` (graphify), `d7ea137` (bootstrap memory fix).
- Ran `ensure-claude-link.sh`, `ensure-codex-link.sh`, `ensure-gemini-link.sh`,
  `ensure-copilot-link.sh`, and `ensure-gemini-builtin-skills.sh`. All five
  reported changes made. Verified all five tool mirrors are at `d7ea137` via
  `git log` and spot-checked the new legalese content landed in each.

## Not Changed

- `.agents/prompt.md` itself was left in place, untouched — it's the user's
  source material, not committed, not part of the propagated skill content.
- `~/.gemini/config/mcp_config.json` (the stale, `.migrated`-marked location)
  was left alone; it isn't what Antigravity actually reads.
