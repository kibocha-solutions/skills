---
name: xlsx
description: Create, read, analyze, edit, repair, recalculate, render, and verify spreadsheet files when the primary input or output is XLSX, XLSM, CSV, or TSV. Use for formulas, formatting, tables, charts, cleanup, restructuring, and spreadsheet conversion. Do not use when the primary deliverable is a document, presentation, webpage, database pipeline, or standalone program.
license: Proprietary. LICENSE.txt has complete terms
---

# Spreadsheet Files

## 1. Establish scope and route tools

1. Read the project instructions.
2. Identify every input file and required output file; preserve original files unless in-place editing is explicitly authorized.
3. Inspect the workbook structure, sheet names, used ranges, tables, formulas, named ranges, charts, merged cells, validations, hidden content, links, comments, and styles.
4. Identify the workbook's existing visual and calculation conventions.
5. Select the tool by operation:
   - Use **OpenPyXL** for cell values, formulas, styles, number formats, tables, filters, validations, comments, named ranges, existing XLSX files, and XLSM files (`keep_vba=True`).
   - Use **pandas** for tabular inspection, cleaning, joins, grouping, reshaping, CSV/TSV I/O, and DataFrame-to-workbook transfer; never use a pandas round trip when formulas, styles, charts, validations, macros, or workbook structure must be preserved.
   - Use **LibreOffice** (isolated profile) for XLSX formula recalculation, PDF rendering, and requested format conversions; read `../system-init/SKILL.md` before installing LibreOffice.

## 2. Edit an existing workbook

1. Record the affected sheet names and ranges and make the smallest complete change.
2. Load formulas with `data_only=False` and pass `keep_vba=True` for XLSM files.
3. Preserve untouched formulas, styles, dimensions, visibility, validations, tables, names, charts, links, and macros.
4. Insert or delete rows and columns only after checking affected references and merged cells.
5. Save to a new file unless in-place editing was requested.
6. Reopen with `data_only=False` to verify formula preservation and with `data_only=True` after recalculation to verify cached results.

## 3. Create a new workbook

1. Read [financial modeling standards](references/financial-and-formula-modeling-standards.md) before building complex calculation workbooks, and inspect [model examples](examples/good-vs-bad-financial-model.md) for formula design patterns.
2. Define sheet responsibilities and use stable, concise sheet names.
3. Put one rectangular data region and one header row per table, using native dates, numbers, percentages, and booleans.
4. Put assumptions in identified input cells, use spreadsheet formulas for calculations that must update when inputs change, and use fixed values for source facts and snapshots.
5. Apply formula hygiene: reference assumption cells, keep formulas consistent across periods/rows, guard zero-denominator cases per workbook convention, verify relative/absolute/cross-sheet references and range endpoints, test boundary inputs, and deliver zero unintended `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NULL!`, `#NUM!`, or `#N/A` values.
6. Apply formatting hygiene: follow the supplied template or project convention, keep number formats matched to stored values, state units in headers, keep years ungrouped, do not rely on color alone for meaning, freeze panes, add filters where helpful, set widths/heights/wrapping/print areas, and keep columns/rows free of clipping.
7. Add charts only when they answer a defined question, and add source metadata where provenance is required.

## 4. Recalculate and verify visually

1. Inspect `python3 xlsx/scripts/recalc.py --help` and recalculate XLSX files with `python3 xlsx/scripts/recalc.py path/to/output.xlsx`; do not use this helper for XLSM files (use a macro-preserving application path or report recalculation as incomplete).
2. Check formulas, cached values, types, dates, links, validations, and errors in the reopened saved file.
3. Export the exact final workbook to PDF or sheet images using LibreOffice or the project renderer, render every PDF page to an image, and inspect every sheet and page.
4. Check titles, headers, frozen regions, widths, heights, wrapping, page breaks, print areas, number formats, legends, labels, and chart placement.
5. Correct defects in the source workbook, regenerate, and re-inspect the exact final output before delivery.

## 5. Pre-completion checklist

- [ ] Source facts and data read manually in full from start to finish.
- [ ] The final file exists at the requested path and opens cleanly.
- [ ] Required sheets, tables, and ranges are present with native data types.
- [ ] Untouched workbook structures are preserved.
- [ ] Formulas are preserved and recalculate cleanly without `#REF!`, `#DIV/0!`, or `#VALUE!`.
- [ ] Every visually relevant sheet rendered to image or PDF and inspected.
- [ ] No clipping, truncated column text (`###`), overlap, or unreadable styling.
- [ ] Exact final `.xlsx` deliverable verified and bound to its SHA-256 hash.
- [ ] Zero AI attribution in document properties, comments, or metadata.
- [ ] No U+2014 em dashes in normal prose.
