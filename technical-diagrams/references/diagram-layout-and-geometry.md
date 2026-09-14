# Diagram Layout and Geometry

## Procedure

1. Set the canvas size and margins.
2. Select one grid increment.
3. Select standard node widths, heights, corner radii, and spacing.
4. Place the primary path first.
5. Place boundaries and containers around completed internal groups.
6. Place secondary paths.
7. Route connectors.
8. Align nodes to the grid.
9. Equalize spacing within repeated groups.
10. Resize nodes to fit final labels.
11. Check overview density.
12. Check detail-scale alignment and collisions.

## Geometry rules

- Use consistent dimensions for nodes with the same role.
- Use larger dimensions only for additional content or hierarchy.
- Keep connector labels clear of nodes and other connectors.
- Keep arrowheads outside node interiors.
- Avoid connector crossings.
- Use explicit waypoints when automatic routing produces ambiguity.
- Keep loops and exception paths outside the main path.
- Keep page edges clear of labels and arrowheads.
- Remove unintended empty regions.

## Density limits

- Split the diagram when labels become unreadable at normal documentation width.
- Split the diagram when one canvas contains multiple unrelated reading directions.
- Split the diagram when boundaries obscure rather than clarify ownership.
