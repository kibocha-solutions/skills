---
name: technical-diagrams
description: Create, edit, validate, render, export, and preserve technical diagrams using Draw.io mxGraph source, project palettes, geometry tokens, SVG exports, and visual inspection. Use for architecture, C4, deployment, sequence, activity, workflow, data-flow, state, ERD, threat-model, permission, authorization, network, infrastructure, Draw.io, diagrams.net, mxGraph XML, and diagram QA tasks.
---

# Technical Diagrams

## 1. Establish scope and outputs

1. Read the project instructions and applicable documentation rules.
2. Identify the required outputs: editable `.drawio` source, SVG documentation export, PNG or PDF review export when requested, and validation results for the exact final source and exports.
3. Read [diagram-type-routing.md](references/diagram-type-routing.md) to select one diagram type and one primary reading direction.
4. Read [source-and-standards-research.md](references/source-and-standards-research.md) when the diagram depends on external standards or supplied sources.
5. Inspect existing diagrams, palettes, geometry, typography, and export conventions; preserve project vocabulary and approved structure unless renaming is authorized.
6. Inspect [system context example](examples/system-context) for reference `.drawio` source and export conventions.

## 2. Model and design

1. Read [diagram-palette-protocol.md](references/diagram-palette-protocol.md) and [diagram-layout-and-geometry.md](references/diagram-layout-and-geometry.md).
2. Define the diagram boundary, audience, entities, relationships, direction, and required labels.
3. Create or update the semantic model before positioning shapes.
4. Assign stable identifiers to nodes and edges, and keep identifiers stable across revisions.
5. Apply project tokens; use the bundled defaults only when the project has no established system.

## 3. Author and route `.drawio` source

1. Read [drawio-mxgraph-generation.md](references/drawio-mxgraph-generation.md).
2. Create or update the `.drawio` source in the project-prescribed location.
3. Keep text editable, keep connectors attached to valid source and target cells, and use orthogonal routing unless the diagram type requires another route.
4. Route connectors before finalizing node placement.
5. Validate XML, identifiers, edge references, labels, and required assets.

## 4. Render and inspect

1. Read [renderer-environment.md](references/renderer-environment.md) and inspect existing project, host, container, and CI renderers first.
2. Read `../system-init/SKILL.md` before installing a missing renderer or dependency.
3. If no renderer is available, complete source validation, report the missing capability, and do not claim rendered visual QA.
4. Render the exact final source with `scripts/render-drawio.sh` or the project renderer.
5. Read [visual-quality-gate.md](references/visual-quality-gate.md) and inspect every rendered page or canvas at overview and detail scale.
6. Correct every verified defect in the source and repeat validation, rendering, and inspection until the exact final outputs pass.
7. Read [writerside-diagram-export.md](references/writerside-diagram-export.md) for Writerside delivery.
8. Verify that every delivered export was generated from the delivered source.

## 5. Pre-completion checklist

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
