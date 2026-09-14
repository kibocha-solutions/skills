---
name: xlsx
description: Create, read, analyze, edit, repair, recalculate, render, and verify spreadsheet files when the primary input or output is XLSX, XLSM, CSV, or TSV. Use for formulas, formatting, tables, charts, cleanup, restructuring, and spreadsheet conversion. Do not use when the primary deliverable is a document, presentation, webpage, database pipeline, or standalone program.
license: Proprietary. LICENSE.txt has complete terms
---

# Spreadsheet Files

## Procedure

1. Read the project instructions.
2. Identify every input file and required output file.
3. Preserve original files unless the user explicitly authorizes in-place editing.
4. Inspect the workbook structure, sheet names, used ranges, tables, formulas, named ranges, charts, merged cells, validations, hidden content, links, comments, and styles.
5. Identify the workbook's existing visual and calculation conventions.
6. Define the required cell, range, sheet, table, chart, or file changes.
7. Select the editing path.
8. Make the smallest complete change.
9. Save to the required output path.
10. Reopen the exact saved file.
11. Recalculate formulas when supported.
12. Check formulas, cached values, types, dates, links, validations, and errors.
13. Render every spreadsheet sheet when visual layout matters.
14. Inspect every rendered page or captured sheet.
15. Correct verified defects in the source workbook.
16. Repeat save, recalculation, programmatic validation, rendering, and inspection.
17. Deliver the exact final file and summarize verified results.

## Tool routing

### OpenPyXL

Use OpenPyXL for:

- Cell values and formulas
- Styles and number formats
- Rows, columns, and worksheets
- Tables, filters, validations, comments, and named ranges
- Existing XLSX files
- XLSM files only with `keep_vba=True`

### pandas

Use pandas for:

- Tabular inspection
- Data cleaning
- Joins, grouping, reshaping, and bulk transformations
- CSV and TSV input or output
- DataFrame-to-workbook transfer

Do not use a pandas round trip for a workbook whose formulas, styles, charts, validations, macros, or workbook structure must be preserved.

### LibreOffice

Use an existing LibreOffice installation for:

- Formula recalculation of XLSX files
- PDF rendering
- Format conversion requested by the user

Read `../system-init/SKILL.md` before installing LibreOffice. Use an isolated
profile for automated recalculation and rendering.

## Existing workbook edits

1. Load formulas with `data_only=False`.
2. Use `keep_vba=True` for XLSM files.
3. Record the affected sheet names and ranges.
4. Preserve untouched formulas, styles, dimensions, visibility, validations, tables, names, charts, links, and macros.
5. Insert or delete rows and columns only after checking affected references and merged cells.
6. Save to a new file unless in-place editing was requested.
7. Reopen with `data_only=False` and verify formula preservation.
8. Reopen with `data_only=True` after recalculation and verify cached results.

## New workbook creation

1. Define sheet responsibilities.
2. Use stable, concise sheet names.
3. Put one rectangular data region in each table area.
4. Use one header row per table.
5. Use native dates, numbers, percentages, and booleans.
6. Put assumptions in identified input cells.
7. Use spreadsheet formulas for calculations that must update when inputs change.
8. Use fixed values for source facts and requested snapshots.
9. Apply one coherent style system.
10. Freeze panes and add filters where they improve navigation.
11. Set widths, heights, wrapping, alignment, and print areas.
12. Add charts only when they answer a defined question.
13. Add source metadata where provenance is required.

## Formula rules

- Use references to assumption cells.
- Keep formulas consistent across repeated periods and rows.
- Guard valid zero-denominator cases with the workbook's established convention.
- Check relative and absolute references.
- Check cross-sheet and external references.
- Check range endpoints and row offsets.
- Test zero, negative, blank, and large inputs when relevant.
- Preserve intentional formulas when editing existing workbooks.
- Deliver no unintended `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NULL!`, `#NUM!`, or `#N/A` values.

## Formatting rules

- Follow the supplied template or existing workbook first.
- Use the user's requested font, colors, formats, units, and layout.
- Use project conventions when no explicit instruction exists.
- Keep number formats appropriate to the stored value.
- State units in headers.
- Keep years ungrouped.
- Distinguish inputs, formulas, links, warnings, and outputs only when the workbook convention requires it.
- Do not use color as the only carrier of meaning.
- Keep text readable at normal zoom.
- Keep columns and rows free of clipping.

## Recalculation

Check the helper before use:

```bash
python3 xlsx/scripts/recalc.py --help
```

Recalculate an XLSX file:

```bash
python3 xlsx/scripts/recalc.py path/to/output.xlsx
```

The helper must not be used for XLSM files. Use an application path that preserves macros, or report recalculation as incomplete.

## Visual verification

1. Use an existing LibreOffice installation or the project spreadsheet renderer.
2. Export the exact final workbook to PDF or sheet images.
3. Render every PDF page to an image when PDF is used.
4. Inspect every sheet and page.
5. Check titles, headers, frozen regions, widths, heights, wrapping, page breaks, print areas, number formats, legends, labels, and chart placement.
6. Correct defects in the workbook.
7. Regenerate and inspect the exact final output.

## Final checks

- [ ] The final file exists at the requested path.
- [ ] The file opens after saving.
- [ ] Required sheets and ranges are present.
- [ ] Untouched workbook structures are preserved.
- [ ] Formulas are preserved and recalculate where supported.
- [ ] Formula errors were checked in every used cell.
- [ ] Dates, numbers, percentages, currencies, and identifiers retain correct types.
- [ ] External links and macros were preserved or explicitly handled.
- [ ] Every visually relevant sheet was rendered and inspected.
- [ ] No clipping, overlap, unreadable text, or broken chart remains.
- [ ] Reported validation matches the exact delivered file.
