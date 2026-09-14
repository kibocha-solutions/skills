# Visual Quality Gate

## Procedure

1. Render the exact final `.drawio` source.
2. Open every rendered page or canvas.
3. Inspect the complete view.
4. Inspect dense regions at detail scale.
5. Inspect boundaries, labels, connectors, legends, and page edges.
6. Record every verified defect.
7. Correct defects in the `.drawio` source.
8. Render again.
9. Repeat inspection until every check passes.
10. Verify the delivered export modification time against the final render.

## Content checks

- Every required entity is present.
- Every relationship has the correct direction.
- Every required label is present.
- No placeholder or drafting note remains.
- Project terminology is unchanged.

## Geometry checks

- No nodes overlap.
- No labels clip.
- No connector crosses a label.
- No arrowhead enters a node.
- No boundary cuts through a node.
- Repeated nodes align and use consistent dimensions.
- Spacing is consistent.
- No unintended empty region remains.

## Legibility checks

- Text is readable at normal delivery size.
- Contrast is sufficient.
- Color is not the only carrier of meaning.
- The primary path is visually clear.
- Legends and annotations remain subordinate.

## Artifact checks

- The source opens.
- The export opens.
- The export was generated from the final source.
- Every page or canvas was inspected.
- The final reported status matches the exact delivered files.
