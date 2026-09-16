---
name: technical-diagrams
description: Create, edit, validate, render, export, and preserve technical diagrams using Draw.io mxGraph source, project palettes, geometry tokens, SVG exports, and visual inspection. Use for architecture, C4, deployment, sequence, activity, workflow, data-flow, state, ERD, threat-model, permission, authorization, network, infrastructure, Draw.io, diagrams.net, mxGraph XML, and diagram QA tasks.
---

# Technical Diagrams

## Required outputs

Produce each applicable output:

1. Editable `.drawio` source.
2. SVG documentation export.
3. PNG or PDF review export when requested.
4. Validation results for the exact final source and exports.

## Procedure

1. Read the project instructions and applicable documentation rules.
2. Read [diagram-type-routing.md](references/diagram-type-routing.md).
3. Read [source-and-standards-research.md](references/source-and-standards-research.md) when the diagram depends on external standards or supplied sources.
4. Inspect existing diagrams, palettes, geometry, typography, and export conventions.
5. Read [diagram-palette-protocol.md](references/diagram-palette-protocol.md).
6. Read [diagram-layout-and-geometry.md](references/diagram-layout-and-geometry.md).
7. Define the diagram boundary, audience, entities, relationships, direction, and required labels.
8. Select one diagram type and one primary reading direction.
9. Create or update the semantic model before positioning shapes.
10. Assign stable identifiers to nodes and edges.
11. Apply project tokens. Use the bundled defaults only when the project has no established system.
12. Read [drawio-mxgraph-generation.md](references/drawio-mxgraph-generation.md).
13. Create or update the `.drawio` source.
14. Route connectors before finalizing node placement.
15. Validate XML, identifiers, edge references, labels, and required assets.
16. Read [renderer-environment.md](references/renderer-environment.md).
17. Render the exact final source with `scripts/render-drawio.sh` or the project renderer.
18. Read [visual-quality-gate.md](references/visual-quality-gate.md).
19. Inspect every rendered page or canvas at overview and detail scale.
20. Correct every verified defect in the source.
21. Repeat validation, rendering, and inspection until the exact final outputs pass.
22. Read [writerside-diagram-export.md](references/writerside-diagram-export.md) for Writerside delivery.
23. Verify that every delivered export was generated from the delivered source.

## Source requirements

- Keep text editable.
- Keep connectors attached to valid source and target cells.
- Use orthogonal routing unless the diagram type requires another route.
- Keep identifiers stable across revisions.
- Keep project vocabulary unchanged unless the user authorizes renaming.
- Preserve supplied meaning, scope, and approved structure.
- Store source and exports in the project-prescribed locations.

## Renderer boundary

- Inspect existing project, host, container, and CI renderers first.
- Read `../system-init/SKILL.md` before installing a missing renderer or
  dependency.
- If no renderer is available, complete source validation, report the missing capability, and do not claim rendered visual QA.

## Pre-completion checklist

- [ ] Final `.drawio` source exists and parses.
- [ ] Node identifiers are unique.
- [ ] Edge references resolve.
- [ ] Labels are complete and readable.
- [ ] Required SVG exports exist and match the final source.
- [ ] Every rendered output was visually inspected.
- [ ] No clipping, overlap, collision, orphan, or unintended whitespace remains.
- [ ] Project palette, geometry, typography, and naming are preserved.
- [ ] Unsupported validation claims are absent.
- [ ] Zero AI attribution in diagram metadata, comments, or exported SVGs.
- [ ] No U+2014 em dashes in normal prose.

