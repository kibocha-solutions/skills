# DOCX Generation Examples: Good vs Bad Patterns

## 1. Table Construction

### Bad (Percentage Widths and Broken Flow)

```javascript
// BAD: Uses auto/percentage widths and allows row splitting
const table = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  rows: [
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph("Item")] }),
        new TableCell({ children: [new Paragraph("Cost")] }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph("Service\nContinuation\nNotes")] }),
        new TableCell({ children: [new Paragraph("$5,000")] }),
      ],
    }),
  ],
});
```

Defects:
- Uses percentage width instead of explicit DXA units, leading to rendering inconsistencies across Word and LibreOffice.
- Omits `cantSplit` on multi-line rows, causing ugly breaks across page margins.
- Embeds raw newline characters (`\n`) instead of distinct `Paragraph` elements.
- Omits header repetition (`tblHeader`).

### Good (Explicit DXA Dimensions and Page Break Control)

```javascript
// GOOD: Precise DXA dimensions, cantSplit, and repeating headers
const table = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [6000, 3360],
  rows: [
    new TableRow({
      tableHeader: true,
      cantSplit: true,
      children: [
        new TableCell({
          width: { size: 6000, type: WidthType.DXA },
          children: [new Paragraph({ text: "Item", style: "TableHeader" })],
        }),
        new TableCell({
          width: { size: 3360, type: WidthType.DXA },
          children: [new Paragraph({ text: "Cost", style: "TableHeader" })],
        }),
      ],
    }),
    new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          width: { size: 6000, type: WidthType.DXA },
          children: [
            new Paragraph("Service"),
            new Paragraph("Continuation"),
            new Paragraph("Notes"),
          ],
        }),
        new TableCell({
          width: { size: 3360, type: WidthType.DXA },
          children: [new Paragraph("$5,000")],
        }),
      ],
    }),
  ],
});
```

Advantages:
- Explicit column and table DXA dimensions guarantee exact alignment.
- Rows marked `cantSplit: true` prevent mid-row fragmentation across page breaks.
- Multi-line cell content constructed with separate `Paragraph` elements.
- Header row marked `tableHeader: true` to repeat cleanly on subsequent pages.
