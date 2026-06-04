# Writerside Diagram Export

Use this reference when a technical diagram appears in Writerside-compatible
documentation.

## Source And Export Layout

When the target project has no diagram convention, use:

```text
docs/
  diagrams/
    assets/
      palette.json
      style-tokens.json
      geometry.json
    <diagram-family>/
      sources/
        <diagram-name>.drawio
      exports/
        <diagram-name>.svg
```

Create PNG exports only when the user requests them, the target platform
requires raster output, or a temporary QA render is needed. Do not commit
temporary QA PNGs unless the user requests review artifacts.

## Writerside Markdown

Reference the final SVG export from the topic:

```md
![System context showing users, the platform, and external services](../diagrams/architecture/exports/system-context.svg)
```

Use useful alt text. Add nearby prose that explains what the reader should
notice when the diagram has operational or architectural implications.

## Source Preservation

Keep `.drawio` source in the repository beside generated exports. Do not use
the `.drawio` file as the visible image unless the user asks for source access.

If the SVG export disagrees with `.drawio`, regenerate the SVG from source.
