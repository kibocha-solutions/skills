# Draw.io mxGraph Generation

Use this reference when authoring or editing `.drawio` source files.

## Source Rule

Use Draw.io diagrams.net mxGraph XML as the editable source of truth for
production technical diagrams. Store the source as `.drawio`. Do not use
Mermaid. Do not hand-edit SVG as the maintenance source.

## Stable IDs

Use stable semantic IDs for nodes and edges where Draw.io permits it:

```text
node:public_api
node:document_store
edge:user_submits_document
edge:api_writes_metadata
```

If Draw.io tooling requires opaque internal IDs, preserve semantic identifiers
in labels, metadata, or custom properties where feasible.

## Source Structure

- Keep one diagram per source file unless the user requests multiple pages.
- Keep node labels concise and relationship labels meaningful.
- Use containers for system, trust, environment, or ownership boundaries.
- Use edge styles consistently. Prefer orthogonal routing for architecture,
  deployment, data-flow, and permission diagrams.
- Attach edges to node boundaries or ports. Do not leave edges floating or
  buried inside nodes.
- Use shape selection semantically: cylinder for data stores, actor/person for
  humans, container/group shapes for boundaries, rectangles for components.

## Style Discipline

Build style strings from palette, geometry, and style token assets. Do not
invent one-off saturated fills, random borders, or inconsistent fonts.

Minimum style expectations:

- pale fill colors for large node backgrounds
- stronger borders or headers for color identity
- dark readable text
- 2 px edge strokes by default
- consistent rounded corners by semantic role
- no heavy shadows unless the project style requires them

## Common Failures

Fix these in source before handoff:

- duplicate IDs
- invalid edge source or target
- orphaned nodes
- clipped labels
- labels detached from relationships
- edges crossing through nodes
- arrows stopping before a target or extending inside a target
- nodes outside page bounds
- inconsistent style strings for equivalent objects

## Export Doctrine

Regenerate exports from `.drawio`. If SVG disagrees with source, the source
wins. Do not patch generated SVG unless the user explicitly accepts a one-off
asset that may drift.
