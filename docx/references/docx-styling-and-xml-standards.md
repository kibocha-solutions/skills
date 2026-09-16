# DOCX Styling and XML Standards

## 1. Dimensional Constants

All DOCX measurements rely on twentieths of a point (DXA). 1 inch = 1440 DXA. 1 pt = 20 DXA.

| Dimension | Standard DXA |
|---|---:|
| Letter Width | 12,240 |
| Letter Height | 15,840 |
| A4 Width | 11,906 |
| A4 Height | 16,838 |
| Standard 1-inch Margin | 1,440 |
| Content Width (Letter, 1-in margins) | 9,360 |
| Content Width (A4, 1-in margins) | 9,026 |

## 2. Paragraph and Text Hierarchy

1. **Paragraph Structure**:
   - Never insert raw newline characters (`\n`) within text runs. Each distinct block must be an independent `Paragraph` element (`w:p`).
   - Paragraph properties (`w:pPr`) must precede run elements (`w:r`).

2. **Heading Conventions**:
   - Explicitly define `Heading1`, `Heading2`, and `Heading3` with associated `outlineLevel` (0, 1, 2) to ensure table of contents generators correctly discover entries.

3. **Character Run Discipline**:
   - Wrap distinct styles, weights, or colors in dedicated text runs (`w:r`).
   - Add `xml:space="preserve"` to any text run containing leading or trailing whitespace.

## 3. Table Construction Rules

1. Use explicit DXA widths for all table cells (`w:tcW`) and total table width (`w:tblW`).
2. Sum of individual `columnWidths` must equal total table width.
3. Apply `cantSplit` to rows that must not break across page boundaries.
4. Apply `tblHeader` to the first row of multi-page tables to repeat headers on subsequent pages.
5. Do not use borderless tables as a substitute for horizontal rules or multi-column text layouts.

## 4. Exact Artifact Verification

1. Compiled deliverables must be converted to PDF and rendered to images (`pdftoppm -jpeg -r 150`) for visual page-by-page inspection.
2. Calculate the SHA-256 hash of the final `.docx` deliverable and record it in verification reports.
