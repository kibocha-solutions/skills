# PptxGenJS Reference

## Start

Use the project's existing PptxGenJS dependency. Read
`../system-init/SKILL.md` before installing or upgrading the package.

```javascript
const pptxgen = require("pptxgenjs");

const deck = new pptxgen();
deck.layout = "LAYOUT_16x9";
deck.title = "Quarterly Operations";
deck.subject = "Quarterly operating results";

const slide = deck.addSlide();
slide.addText("Quarterly Operations", {
  x: 0.6, y: 0.4, w: 8.8, h: 0.5,
  margin: 0, fontSize: 30, bold: true, color: "202124"
});

await deck.writeFile({ fileName: "quarterly-operations.pptx" });
```

Do not add author metadata unless the user supplies it.

## Layouts

| Layout | Width | Height |
|---|---:|---:|
| `LAYOUT_16x9` | 10 | 5.625 |
| `LAYOUT_16x10` | 10 | 6.25 |
| `LAYOUT_4x3` | 10 | 7.5 |
| `LAYOUT_WIDE` | 13.333 | 7.5 |

Use inches for coordinates and dimensions.

## Text

```javascript
slide.addText("Status", {
  x: 0.6, y: 1.0, w: 2.0, h: 0.4,
  margin: 0, fontFace: "Arial", fontSize: 18,
  bold: true, color: "202124"
});

slide.addText([
  { text: "Completed", options: { bold: true, breakLine: true } },
  { text: "All scheduled checks passed." }
], {
  x: 0.6, y: 1.5, w: 4.2, h: 1.0,
  margin: 0, fontSize: 16, color: "202124"
});
```

Rules:

- Use `charSpacing` for character spacing.
- Use `breakLine: true` between rich-text lines.
- Set `margin: 0` for edge alignment.
- Keep a fresh options object for every call.
- Use a supported project font.
- Measure text after final content is inserted.

## Lists

```javascript
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true } }
], { x: 0.8, y: 1.2, w: 4.0, h: 1.4, fontSize: 16 });
```

- Use `bullet: true` or `bullet: { type: "number" }`.
- Use `indentLevel` for nested items.
- Do not insert Unicode bullet characters.
- Use `paraSpaceAfter` for paragraph spacing.

## Shapes

```javascript
const makeShadow = () => ({
  type: "outer",
  color: "000000",
  blur: 6,
  offset: 2,
  angle: 135,
  opacity: 0.15
});

slide.addShape(deck.ShapeType.rect, {
  x: 0.6, y: 1.0, w: 3.8, h: 2.0,
  fill: { color: "FFFFFF" },
  line: { color: "DADCE0", width: 1 },
  shadow: makeShadow()
});
```

Rules:

- Use six-character hexadecimal colors without `#`.
- Use `opacity` for shadow transparency.
- Keep shadow `offset` non-negative.
- Create a fresh shadow object for every shape.
- Use rectangular containers when a rectangular accent edge must align with the container.
- Use `ROUNDED_RECTANGLE` only when no square overlay must cover its corners.

## Images

```javascript
slide.addImage({
  path: "assets/chart.png",
  x: 5.0, y: 1.0, w: 4.3, h: 2.8,
  altText: "Quarterly output by region"
});
```

Rules:

- Use project-local or user-supplied images.
- Do not fetch remote images without authorization.
- Preserve aspect ratio.
- Use contain, cover, or crop intentionally.
- Add useful alternative text.
- Inspect every crop in the rendered slide.
- Use SVG when the target PowerPoint version supports it.
- Use PNG or JPG when compatibility requires raster output.

## Tables

```javascript
slide.addTable([
  ["Region", "Output"],
  ["North", "42"],
  ["South", "37"]
], {
  x: 0.8, y: 1.2, w: 8.4, h: 2.0,
  border: { pt: 1, color: "DADCE0" },
  fill: { color: "FFFFFF" },
  color: "202124",
  fontSize: 15
});
```

- Keep source values and labels exact.
- Apply explicit column widths for dense tables.
- Use cell objects for merged cells and cell-specific formatting.
- Verify row heights and wrapping after rendering.

## Charts

```javascript
slide.addChart(deck.ChartType.bar, [{
  name: "Output",
  labels: ["Q1", "Q2", "Q3", "Q4"],
  values: [45, 55, 62, 71]
}], {
  x: 0.7, y: 1.0, w: 8.6, h: 3.8,
  barDir: "col",
  chartColors: ["0D9488"],
  showLegend: false,
  showValue: true,
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" }
});
```

- Match chart type to the comparison.
- Keep scales honest.
- Label units.
- Use the project palette.
- Remove unnecessary legends and grid lines.
- Verify labels, ticks, and data values against the source.

## Masters

```javascript
deck.defineSlideMaster({
  title: "TITLE",
  background: { color: "FFFFFF" },
  objects: [{
    placeholder: {
      options: {
        name: "title", type: "title",
        x: 0.7, y: 0.5, w: 8.6, h: 0.6
      }
    }
  }]
});

const titleSlide = deck.addSlide("TITLE");
titleSlide.addText("Quarterly Operations", { placeholder: "title" });
```

- Define repeated geometry in masters.
- Keep placeholder names stable.
- Do not duplicate master content as independent slide objects.

## Package guards

- Do not use eight-character hexadecimal colors.
- Do not reuse mutated option objects.
- Do not use negative shadow offsets.
- Do not use unsupported properties such as `letterSpacing`.
- Do not use Unicode bullets.
- Do not write outside the slide bounds.
- Do not rely on source inspection for layout validation.

## Final procedure

1. Write the presentation.
2. Reopen it with the package validator.
3. Render every slide.
4. Inspect every rendered slide.
5. Correct the JavaScript source.
6. Regenerate the presentation.
7. Repeat validation and inspection.
