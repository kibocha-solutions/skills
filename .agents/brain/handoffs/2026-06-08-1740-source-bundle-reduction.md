# Handoff: Source Bundle Reduction

## Datetime

2026-06-08 17:40 EAT

## Current objective

Reduce the skills repository so local top-level skills are the source of truth,
remove moot source bundles, and keep only the project-reference material that
has not yet been replaced by local skills.

## State of the repo

The local skills repo is retaining and routing these additional first-class
skills:

- `docx`
- `pdf`
- `pptx`
- `xlsx`
- `frontend-design`
- `webapp-testing`
- `internal-comms`

The Anthropic source bundle is being treated as migration source material, not
as a permanent dependency. The `sources/anthropic-skills/` bundle has now been
removed after localizing the keeper skills. Skills judged off-process or too
provider-specific for this repo are not being localized in this pass.

Project references considered moot for this repo phase have now been removed:

- `00-core-canons/`
- `01-technical-documentation/`
- `03-ci-cd/`
- `07-project-wide-instructions/`

## Decisions made

- Keep broadly useful document, frontend, testing, and internal communication
  skills.
- Drop Anthropic-specific, Claude-specific, and art-only source skills from the
  permanent local set unless they later earn a real cross-agent rewrite.
- Keep `mcp-builder` out of the permanent set for now because its helper
  evaluation tooling is still too Anthropic-specific.
- Treat local top-level skills and `AGENTS.md` as the active operating layer.
- Remove the stale `sources/anthropic-skills` submodule metadata so the repo
  no longer advertises a dependency that has been intentionally retired.

## Files changed

- `.agents/skills/AGENTS.md`: skill routing expanded to new local skills.
- `.agents/skills/README.md`: active skill inventory updated.
- `.agents/skills/sources/README.md`: reduced-source intent clarified.
- `.agents/skills/sources/project-references/README.md`: moot folders removed
  from the index.
- `.agents/skills/skill-creator/`: wording generalized away from Claude-only
  framing.
- `.agents/skills/.gitmodules`: removed because the Anthropic source bundle is
  no longer a live dependency.

## Open questions

- Whether `mcp-builder` should later be rewritten as a fully cross-agent local
  skill.
- Whether the retained document skills should later gain local repo-specific
  evals and house examples.

## Next entry point

1. Verify the final kept-skill set is present at the top level of
   `.agents/skills/`.
2. Re-check the final repo state so only the remaining source-reference folders
   survive.
3. Continue localizing or replacing the remaining retained reference areas only
   when they gain a real top-level skill replacement.

## Constraints

- Do not leave a top-level skill dependent on a soon-to-be-deleted source
  bundle path.
- Keep the skills repo usable by agents beyond Claude-specific hosts.
- Preserve the remaining `project-references` folders because they have not yet
  been replaced by local skills.
