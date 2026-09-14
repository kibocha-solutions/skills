---
name: pdf
description: Read, extract, create, edit, merge, split, rotate, watermark, encrypt, decrypt, OCR, fill, render, inspect, and verify PDF files. Use whenever a PDF is an input, output, source, or final artifact.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF

## 1. Establish the operation

1. Identify every input PDF and the requested output.
2. Preserve the original input unless the user requests replacement.
3. Work from editable source files when they exist.
4. Treat a PDF as a derived artifact when source Markdown, DOCX, HTML, or generation code exists.
5. Regenerate derived PDFs after every source change.
6. Do not hand-patch a generated final PDF.
7. Read `../system-init/SKILL.md` before installing a missing tool or library.

## 2. Inspect the input

1. Confirm that each file exists and opens.
2. Run `pdfinfo` to record page count, page size, encryption, metadata, and PDF version.
3. Run `qpdf --check` when `qpdf` is available.
4. Check whether text is extractable.
5. Check whether the document contains AcroForm fields.
6. Check page rotation and mixed page sizes.
7. Record passwords or access constraints without exposing them in logs or output.

## 3. Read a text PDF

1. Extract text with `pdftotext` or `pdfplumber`.
2. Preserve page boundaries in the extracted text.
3. Read the complete extracted text in order.
4. Render pages containing tables, figures, signatures, stamps, forms, or ambiguous layout.
5. Compare important text with the rendered page.
6. Cite page numbers when reporting findings.

## 4. Read a scanned PDF

1. Render every page to images with Poppler.
2. Inspect the rendered pages in page order.
3. Run OCR when searchable text is required.
4. Keep OCR output separate from the source PDF.
5. Verify names, numbers, dates, tables, and legal text against page images.
6. Record the page ranges actually inspected.
7. Do not claim the document was read until every required page has been inspected.

## 5. Extract text, tables, or images

1. Use `pdftotext -layout` for layout-preserving text extraction.
2. Use `pdfplumber` for tables and bounding boxes.
3. Use `pdfimages` for embedded images.
4. Preserve page numbers and table order.
5. Validate extracted row and column boundaries against rendered pages.
6. Use the spreadsheet skill when the requested deliverable is a spreadsheet.
7. Do not treat OCR or automated table extraction as verified without visual comparison.

## 6. Merge, split, rotate, crop, or reorder

1. Record the requested page order and page ranges.
2. Use `qpdf` or `pypdf`.
3. Preserve page boxes, orientation, metadata, bookmarks, annotations, and forms when required.
4. Write to a new output path.
5. Verify the final page count and order.
6. Render the first page, last page, every transition, and every modified page.
7. Inspect every page when the operation affects the whole document.

## 7. Add watermarks, annotations, or overlays

1. Confirm the target pages, text, opacity, rotation, position, and layer order.
2. Preserve existing content and annotations.
3. Use embedded fonts with required glyph coverage.
4. Use ReportLab `<sub>` and `<super>` markup in paragraph content.
5. Do not use unsupported Unicode subscript or superscript glyphs with built-in ReportLab fonts.
6. Check overlay placement at each page size and orientation.

## 8. Create a PDF

1. Read the documentation skill.
2. Read [letterhead and pagination](../documentation/references/letterhead-and-pagination.md) for fixed-page documents.
3. Define page size, margins, typography, hierarchy, headers, footers, and folios before generation.
4. Use ReportLab, a source document workflow, or the project generator.
5. Keep generation logic separate from the final PDF.
6. Embed fonts required for all characters.
7. Apply table widow and orphan controls.
8. Scale images proportionally within the content area.
9. Keep body content flowing without unexplained dead gaps.
10. Generate the complete PDF from source.

## 9. Fill a PDF form

Read [form filling](forms.md) in full.

1. Detect fillable fields with `scripts/check_fillable_fields.py`.
2. Use the fillable-field workflow when AcroForm fields exist.
3. Use the annotation workflow only when fillable fields do not exist.
4. Extract field identifiers, types, options, pages, and coordinates.
5. Match every value to the correct field and page.
6. Validate bounding boxes before writing annotations.
7. Preserve unfilled fields unless the user directs otherwise.
8. Render and inspect every filled page.
9. Verify checkbox, radio, choice, signature, and multiline states.

## 10. Encrypt or decrypt

1. Confirm the requested operation and output path.
2. Use a user-provided password or approved secure input path.
3. Do not print or store passwords in repository files.
4. Preserve the original encrypted file.
5. Apply requested printing, copying, and modification permissions.
6. Verify encryption status with `qpdf --show-encryption` or an equivalent check.
7. Open the final PDF with the intended password.

## 11. Repair or optimize

1. Run `qpdf --check` before repair.
2. Preserve the original file.
3. Write repaired or optimized output to a new file.
4. Compare page count, page sizes, metadata, bookmarks, forms, and attachments.
5. Extract text from both versions and compare expected content.
6. Render and inspect the final output.

Use [the advanced reference](reference.md) only for operations not covered above.

## 12. Verify the exact final PDF

1. Confirm the final file exists and is reachable.
2. Run `pdfinfo` on the final file.
3. Run `qpdf --check` when available.
4. Extract text from the final file and search for required and prohibited content.
5. Render every page to PNG or JPEG at a readable resolution.
6. Inspect every rendered page.
7. Check clipping, overlap, blank pages, dead gaps, orphaned headings, split tables, image scaling, headers, footers, folios, letterhead, signatures, and form values.
8. Reopen encrypted output with the intended credentials.
9. Re-run verification after every correction.
10. Deliver only the verified final PDF.
