# Writerside Diagram Export

## Procedure

1. Export the final diagram as SVG.
2. Keep the editable `.drawio` source beside the documentation source or in the project diagram-source directory.
3. Use a stable lowercase filename.
4. Add accessible alt text that states the diagram subject and purpose.
5. Reference the SVG with the project Writerside syntax.
6. Build every affected Writerside instance with `wrs build <instance>` when the builder is available.
7. Open the rendered topic.
8. Check width, scaling, text legibility, theme contrast, and surrounding spacing.
9. Correct the `.drawio` source or documentation placement.
10. Re-export, rebuild, and inspect.
11. Keep generated test output outside the repository.

## Constraints

- Do not embed raster screenshots when an SVG export is available.
- Do not edit the generated SVG as the primary source.
- Do not claim Writerside validation when the builder did not run.
- Do not leave `.idea/`, temporary reports, or generated ZIP files in the worktree.
