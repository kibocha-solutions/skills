# Handoff: documentation and diagrams skills

## Datetime

2026-06-04 21:18 EAT

## Current objective

Refine the first documentation skill into the broader `documentation` skill and
add a production-grade `technical-diagrams` skill with Draw.io source doctrine,
renderer-backed QA requirements, scripts, assets, references, and examples.

## State of the repo

Current branch: `feat/docs`

Latest commit before this work:

```text
9cc3a26 feat(documentation-drafting): add Writerside documentation skill
```

The working tree now contains an uncommitted rename-style change from
`documentation-drafting/` to `documentation/`, plus a new `technical-diagrams/`
skill.

Pre-existing or separate working tree items remain present:

- `.gitmodules` staged as a new file.
- `sources/anthropic-skills` staged as a new submodule.
- `sources/reports/signs-of-ai-writing.txt` untracked.

Those items were not edited as part of the documentation and diagrams skill
refinement.

## Decisions made

- Rename `documentation-drafting` to `documentation` because the skill covers
  drafting, review, rewriting, Writerside technical docs, and comment
  documentation.
- Keep historical handoffs unchanged even though they mention the old skill
  name.
- Create `technical-diagrams` as a separate skill because diagram work has a
  distinct execution model: Draw.io mxGraph source, layout geometry, palette
  memory, export preservation, scripts, examples, and rendered visual QA.
- Reject Mermaid for this skill. Quick sketches may still be SVG or PNG, but
  not Mermaid.
- Require a Draw.io-compatible renderer for production diagram work. Truthful
  source-only fallback is allowed only when installing or finding a compatible
  renderer is genuinely impossible.
- Make authoritative source and standards research part of production diagram
  generation across all diagram types. Local project truth controls artifact
  content; external standards complement notation, accessibility, visual
  quality, platform correctness, and domain conventions.
- Preserve `.drawio` as editable source of truth and SVG as the default
  documentation export. PNG is temporary QA output unless requested or required.
- Include examples in the skill folder as first-class skill material.
- Keep `technical-diagrams/SKILL.md` concise and move detailed doctrine into
  references and assets.

## Files changed

- `AGENTS.md`: points documentation work to `documentation`, diagram work to
  `technical-diagrams`, and requires `.drawio` source plus SVG export for
  production diagrams.
- `documentation/`: renamed from `documentation-drafting/`; active references
  updated to the new skill name.
- `documentation/references/technical-documentation-routing.md`: routes diagram
  and visual documentation work to the `technical-diagrams` skill.
- `documentation/references/writerside-technical-documentation.md`: removes
  Mermaid and PlantUML guidance and routes production diagrams to exported SVGs
  created by `technical-diagrams`.
- `technical-diagrams/SKILL.md`: adds concise production diagram workflow,
  hard rules, and bundled resource map.
- `technical-diagrams/references/`: adds diagram type routing, source and
  standards research, Draw.io mxGraph generation, layout and geometry, palette
  protocol, renderer environment, visual quality gate, and Writerside export
  guidance.
- `technical-diagrams/assets/`: adds fallback palette, style token, geometry,
  and system-context mxGraph template assets.
- `technical-diagrams/scripts/`: adds `render-drawio.sh`,
  `install-drawio-renderer-ubuntu.sh`, and `check-diagram-bundle.py`.
- `technical-diagrams/examples/system-context/`: adds a complete example
  bundle with `.drawio` source, SVG export, and notes.

## Open questions

- Should the repository later add CI that installs a Draw.io-compatible renderer
  and validates diagram bundles or exports?
- Should `agents/openai.yaml` metadata be added for repo skills in a later pass?
- Should the future AGENTS template include submodule repair guidance for
  `sources/anthropic-skills` using proper `git submodule` commands?
- Should additional example bundles be added for sequence, activity, data flow,
  permission, and threat-model diagrams?

## Next entry point

1. Review the uncommitted `documentation` rename and new `technical-diagrams`
   skill.
2. Decide whether to stage the rename and new skill together or split commits.
3. Handle the separate `.gitmodules` and `sources/anthropic-skills` work.
4. Use a compatible Draw.io renderer before production diagram delivery. The
   current WSL session has official Draw.io installed, but local export remains
   blocked by Electron sandbox constraints on a `nosuid` filesystem.

## Constraints

- Do not delete `sources/` or old handoff documents unless the user explicitly
  requests it.
- Treat `sources/` as source material, not active skill guidance.
- Do not copy source material wholesale into skills.
- Keep skill `SKILL.md` files concise; put detailed guidance in `references/`
  and reusable output material in `assets/`.
- Do not claim rendered visual QA for diagrams unless a rendered image was
  actually inspected.
- After follow-up setup, the current environment has `drawio`, `xvfb-run`, and
  `rsvg-convert` on PATH.
- The official diagrams.net desktop package installed successfully from
  `drawio-amd64-30.0.4.deb`, but Draw.io export still fails in this session
  with Electron `sandbox_host_linux.cc` errors because the filesystem is mounted
  `nosuid`. This may be specific to the current sandboxed WSL profile. Do not
  claim Draw.io render QA in this session unless a compatible host, container,
  CI, or repaired sandbox route succeeds.
- `rsvg-convert` can rasterize existing SVG exports for preview inspection, but
  it does not replace Draw.io export from `.drawio` source.
