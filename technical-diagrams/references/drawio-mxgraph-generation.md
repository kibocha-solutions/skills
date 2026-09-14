# Draw.io mxGraph Generation

## Procedure

1. Start from an existing project source or `assets/mxgraph-templates/system-context.drawio`.
2. Preserve the `mxfile`, `diagram`, `mxGraphModel`, `root`, and base cells.
3. Assign a unique, stable `id` to every `mxCell`.
4. Create vertex cells with `vertex="1"` and a valid parent.
5. Create edge cells with `edge="1"`, valid `source` and `target` identifiers, and relative geometry.
6. Store visible labels in `value`.
7. Encode XML-sensitive characters.
8. Store geometry in `mxGeometry`.
9. Use explicit waypoints for controlled routes.
10. Keep semantic style properties consistent by role.
11. Parse the final XML.
12. Run `scripts/check-diagram-bundle.py`.
13. Open the final source in diagrams.net when available.
14. Render and inspect the final export.

## Cell requirements

### Vertex

- Unique identifier
- Parent identifier
- Editable label
- Semantic style
- Position and dimensions

### Edge

- Unique identifier
- Parent identifier
- Source identifier
- Target identifier
- Connector style
- Relative geometry
- Label and waypoints when required

## Validation command

```bash
python3 technical-diagrams/scripts/check-diagram-bundle.py \
  path/to/diagram.drawio \
  --export path/to/diagram.svg
```
