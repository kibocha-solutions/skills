---
name: technical-diagrams
description: >
  Create, edit, validate, render, export, and preserve professional technical
  diagrams using Draw.io diagrams.net mxGraph source files, project diagram
  palettes, geometry tokens, SVG documentation exports, and render-backed
  visual QA. Use for architecture diagrams, C4 diagrams, system context,
  container, component, deployment, sequence, activity, workflow, data flow,
  state, ERD, entity relationship, threat model, permission, authorization,
  network, infrastructure, Draw.io, diagrams.net, mxGraph XML, technical
  diagrams, visual documentation, diagram examples, and diagram QA.
---

# Technical Diagrams

## Goal

Create editable technical diagrams that preserve source files, use stable
visual rules, export documentation-ready SVG assets, and pass render-backed
inspection before delivery.

## Non-Circumvention

Diagram rules apply to the underlying visual or documentation defect. The
surface wording that revealed the defect is only evidence. Do not satisfy a
rule by renaming a bad shape, recoloring an unclear diagram without fixing the
semantics, rephrasing an unsupported label, hiding a forbidden relationship in
a caption, or preserving the same defect in a less searchable form.

When a diagram, label, caption, export, or adjacent documentation violates any
prescription or prohibition in this skill or its references, rewrite or redraw
the problematic part so the defect is gone. Quick paraphrase, cosmetic
substitution, and checkbox-style compliance are insufficient.

## Reader Baseline

Design technical diagrams for a careful intern or new contributor unless the
user or repository states a narrower expert audience. The diagram and its
nearby documentation must teach the reader what the nodes mean, why the
relationships matter, what direction or state change is being shown, and where
the diagram fits in the system.

Prefer explicit labels, legends, nearby explanations, and visual hierarchy over
compressed expert shorthand. Keep diagrams readable, but do not omit the
context a new contributor needs to interpret the artifact without private team
memory.

## Default Procedure

1. Identify the diagram type before drawing. Read
   `references/diagram-type-routing.md`.
2. Gather source facts from the target project and authoritative current
   sources before designing the artifact. Read
   `references/source-and-standards-research.md`.
3. Inspect existing project diagrams and diagram assets before inventing
   styles. Read `references/diagram-palette-protocol.md`.
4. Use Draw.io diagrams.net `.drawio` mxGraph XML as the editable source of
   truth. Do not use Mermaid.
5. Use the shared palette, style tokens, and geometry assets when no reliable
   project equivalents exist.
6. Generate or edit the `.drawio` source with stable node and edge IDs. Read
   `references/drawio-mxgraph-generation.md`.
7. Render with `scripts/render-drawio.sh` or an equivalent diagrams.net CLI.
   Production work requires a renderer. If no renderer is available, install
   one or locate a compatible equivalent before continuing. Read
   `references/renderer-environment.md` before declaring setup blocked.
8. Inspect the rendered output and fix source defects. Read
   `references/visual-quality-gate.md`.
9. Export SVG by default for documentation. Keep temporary PNG QA renders out
   of commits unless the user requests review artifacts.
10. Reference final SVG exports from Writerside topics. Read
   `references/writerside-diagram-export.md`.
11. Report source path, export path, renderer used, visual QA status, and any
    validation limit.

## Hard Rules

- Preserve `.drawio` source and final SVG export together.
- Treat SVG and PNG exports as generated from `.drawio`.
- Do not hand off a production diagram on XML validity alone.
- Do not claim visual QA unless a rendered image was inspected.
- Do not give up on rendering after a missing-command failure. Try installation
  or a compatible renderer first; source-only fallback is allowed only after
  setup is genuinely blocked.
- Use pale fills, stronger borders, restrained colors, and semantic colors only
  for semantic meaning.
- Prefer project palettes. Use fallback assets only when no reliable project
  palette exists.
- Do not invent artifact content when local sources or authoritative standards
  can answer it. External standards complement local truth; they do not replace
  project facts.

## Bundled Resources

- `assets/default-palette.json`: fallback diagram-safe color roles.
- `assets/default-style-tokens.json`: fallback typography, stroke, shape, and
  arrow rules.
- `assets/default-geometry.json`: fallback page, spacing, node, and edge
  geometry.
- `assets/mxgraph-templates/`: reusable Draw.io source templates.
- `examples/`: production-style example bundles with `.drawio` source and SVG
  export.
- `references/source-and-standards-research.md`: local-source and
  authoritative-standards research procedure for all production diagrams.
- `scripts/render-drawio.sh`: required render/export wrapper for Draw.io CLI
  compatible tools.
- `scripts/install-drawio-renderer-ubuntu.sh`: official diagrams.net,
  `xvfb`, and SVG preview setup for Ubuntu or WSL environments.
- `scripts/check-diagram-bundle.py`: deterministic bundle and source checks.
