# Visual Quality Gate

Use this reference before declaring a production technical diagram complete.

## Required Renderer

Production diagram work requires rendering through `drawio-cli`, `drawio`, or a
compatible diagrams.net CLI. Use `scripts/render-drawio.sh` unless the target
project already has an equivalent command.

If no renderer is available, do not stop at the missing command. Try these setup
paths before falling back:

1. Check whether the target project already has a render command, package
   script, dev container, or CI image with Draw.io support.
2. Check common compatible commands: `drawio-cli`, `drawio`, `diagrams.net`,
   and `diagramsnet`.
3. Install or expose a compatible diagrams.net renderer for the environment.
   For Ubuntu or WSL, read `renderer-environment.md` and use
   `scripts/install-drawio-renderer-ubuntu.sh` when appropriate.
4. Install headless support such as `xvfb` when the renderer needs a display.
5. Install an SVG rasterizer such as `rsvg-convert` or an equivalent only for
   previewing already-exported SVGs; this does not replace Draw.io export.

If installation and a compatible equivalent are genuinely impossible, report:

```text
Source reviewed only. Render-backed visual QA was blocked because no compatible
Draw.io renderer was available.
```

Do not claim visual QA in that state. Name the setup attempts that failed so
the next agent can resume from evidence instead of rediscovering the same
blocked path.

## Quality Layers

1. Diagram-type correctness
2. Deterministic source and geometry checks
3. Rendered visual inspection
4. Documentation export check

Run `scripts/check-diagram-bundle.py` for deterministic bundle checks when the
bundle exists.

## Visual Inspection Questions

Inspect the rendered PNG or SVG and answer these before delivery:

- Is there a clean margin between the diagram and page edge?
- Are arrows visible, thick enough, routed cleanly, and properly terminated?
- Are labels readable and close to the relationship they describe?
- Do arrows stop at valid node boundaries or ports?
- Is negative space used effectively?
- Are components spaced with enough room?
- Does the layout match the diagram type?
- Does the diagram look modern, clean, and professional without decoration?
- Are there line crossings, label overlaps, clipping, or tangled flows?
- Does every color carry meaning or hierarchy?
- Is the diagram readable at the documentation size where it will be consumed?

## Debug Renders

When source mapping is hard, create a temporary debug source or debug render
with node IDs, edge IDs, bounding boxes, ports, or container boundaries. Remove
debug overlays from final documentation exports.

## Failure Reports

Report failures by ID when possible:

```text
edge:user_uploads_document crosses node:document_map.
label:deadline_alert_label overlaps edge:notification_sent.
node:public_api has insufficient right margin.
```

Fix the `.drawio` source, then regenerate exports.
