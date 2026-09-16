---
name: docx
description: Create, read, edit, convert, validate, render, and inspect Microsoft Word .docx documents. Use for Word documents, DOCX files, reports, memos, letters, templates, headings, tables of contents, page numbers, letterheads, tracked changes, comments, images, text replacement, content extraction, and polished Word deliverables. Do not use for PDFs, spreadsheets, Google Docs, or unrelated code tasks.
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX

## 1. Establish the operation

1. Identify the input file, requested edits, output file, page size, template,
   author metadata, tracked-change requirement, and final delivery format.
2. Apply `documentation/SKILL.md`.
3. Read `../documentation/references/letterhead-and-pagination.md` for every
   multi-page document.
4. Preserve the source file unless the user requests in-place replacement.
5. Confirm that required dependencies are available:
   - Pandoc for extraction
   - `docx` for JavaScript generation
   - LibreOffice through `scripts/office/soffice.py`
   - Poppler for page rendering
6. Read `../system-init/SKILL.md` before installing a missing dependency.

## 2. Read or convert an existing document

1. Convert legacy `.doc` files before editing:

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

2. Extract readable Markdown with tracked changes:

```bash
pandoc --track-changes=all document.docx -o output.md
```

3. Unpack for XML inspection:

```bash
python scripts/office/unpack.py document.docx unpacked/
```

4. Read the extracted content from start to finish.
5. Inspect headers, footers, comments, relationships, numbering, styles, and
   media when they affect the task.

## 3. Create a document

1. Use the JavaScript `docx` package.
2. Set page size and margins explicitly.
3. Use DXA values:

| Paper | Width | Height | Content width with 1 inch margins |
|---|---:|---:|---:|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 | 11,906 | 16,838 | 9,026 |

4. Pass portrait dimensions with `PageOrientation.LANDSCAPE` for landscape
   sections.
5. Define the default font and paragraph styles.
6. Override built-in headings with exact IDs such as `Heading1` and
   `Heading2`.
7. Set `outlineLevel` for headings used by a table of contents.
8. Use `HeadingLevel` on table-of-contents headings.
9. Use separate `Paragraph` elements instead of newline characters.
10. Use numbering configuration for bullets and numbered lists.
11. Use a new numbering reference when a sequence must restart.
12. Put every `PageBreak` inside a `Paragraph`.
13. Add page headers, footers, and numbering through section definitions.
14. Use paragraph borders for divider rules.
15. Use tab stops for aligned header or footer text.
16. Use `ExternalHyperlink`, `Bookmark`, and `InternalHyperlink` for
    links.
17. Use `FootnoteReferenceRun` with document-level footnotes.
18. Use `Column` and `SectionType.NEXT_COLUMN` for multi-column layouts.
19. Write the output through `Packer.toBuffer`.

## 4. Build tables

1. Use `WidthType.DXA`.
2. Set the table width.
3. Set `columnWidths`.
4. Make the table width equal the sum of `columnWidths`.
5. Set each cell width to its corresponding column width.
6. Set cell margins.
7. Use `ShadingType.CLEAR` for cell shading.
8. Do not use percentage table widths.
9. Do not use tables as divider lines.
10. Apply the page-break and repeating-header rules in
    `../documentation/references/letterhead-and-pagination.md`.

## 5. Insert images

1. Set `ImageRun.type`.
2. Supply image bytes.
3. Set width and height.
4. Add `title`, `description`, and `name` in `altText`.
5. Add an unpacked image to `word/media/`.
6. Add its relationship to the applicable `.rels` file.
7. Add its extension and content type to `[Content_Types].xml`.
8. Reference the relationship ID from the drawing element.
9. Apply the image page-break and scaling rules in
   `../documentation/references/letterhead-and-pagination.md`.

## 6. Edit an existing document

1. Unpack the document:

```bash
python scripts/office/unpack.py document.docx unpacked/
```

2. Edit the required files under `unpacked/word/`.
3. Use targeted text edits.
4. Do not create a one-off script for a direct string replacement.
5. Preserve namespaces, relationships, element order, IDs, and formatting.
6. Use smart-quote XML entities for new text:
   - `&#x2018;`
   - `&#x2019;`
   - `&#x201C;`
   - `&#x201D;`
7. Add `xml:space="preserve"` to text nodes with leading or trailing
   whitespace.
8. Use eight-digit hexadecimal RSIDs.
9. Keep `w:pPr` children in schema order.
10. Pack the edited document:

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

11. Use `--validate false` only for isolated diagnosis.
12. Inspect every validation repair.
13. Correct malformed XML, invalid nesting, missing relationships, and schema
    violations manually in the unpacked source.

## 7. Add tracked changes

1. Preserve the existing author when the document establishes one.
2. Use the author supplied by the user when specified.
3. Use `Editor` when no author is established.
4. Never use an AI product, model, agent, automated assistant, or AI-assisted
   tool name as the author.
5. Replace the complete affected `w:r` with sibling `w:del` and `w:ins`
   elements.
6. Copy the original `w:rPr` into changed runs.
7. Use unique change IDs and ISO timestamps.
8. Use `w:delText` inside `w:del`.
9. Use `w:delInstrText` for deleted instruction text.
10. Mark the paragraph mark deleted when removing an entire paragraph or list
    item.
11. Nest a deletion inside another author's insertion when rejecting it.
12. Add an insertion after another author's deletion when restoring it.
13. Keep each tracked change limited to the changed text.

## 8. Add comments

1. Create the comment:

```bash
python scripts/comment.py unpacked/ 0 "Comment text"
```

2. Use `--parent <id>` for a reply.
3. Use `--author <name>` for a user-specified author.
4. Use pre-escaped XML in comment text.
5. Place `w:commentRangeStart` and `w:commentRangeEnd` as children of
   `w:p`.
6. Never place comment range markers inside `w:r`.
7. Place reply markers inside the parent range.
8. Add the matching `w:commentReference`.

## 9. Accept tracked changes

Run:

```bash
python scripts/accept_changes.py input.docx output.docx
```

Validate and render the resulting clean document separately.

## 10. Validate the package

1. Run:

```bash
python scripts/office/validate.py output.docx
```

2. Treat a nonzero result as failure.
3. Unpack and correct the source XML.
4. Repack and rerun validation.
5. Confirm that the intended content, comments, changes, links, styles, and
   media exist in the exact final package.

## 11. Render and inspect

1. Convert the exact final DOCX to PDF:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
```

2. Render every PDF page:

```bash
pdftoppm -jpeg -r 150 output.pdf page
```

3. Open and inspect every page image.
4. Check text, typography, headings, lists, tables, images, links, headers,
   footers, page numbers, page breaks, continuation pages, and final-page flow.
5. Check the last page of every table.
6. Check the first page after each letterhead, front-matter, body, or section
   transition.
7. Correct the generation source or unpacked XML.
8. Rebuild, validate, render, and inspect again after every correction.
9. Deliver only the exact final verified DOCX.

## 12. Pre-completion checklist

Before delivering any DOCX deliverable, confirm evidence exists for each item:

- [ ] Source documents and requested content read manually in full from start to finish.
- [ ] Explicit DXA dimensions used for all page margins, tables, and column widths.
- [ ] No raw newline characters inside text runs; paragraphs separated into distinct `w:p` elements.
- [ ] Multi-page tables include `tblHeader` and row-level `cantSplit` protection.
- [ ] Package validation passes with zero errors via `validate.py`.
- [ ] Converted to PDF and rendered to page images (`pdftoppm -jpeg -r 150`).
- [ ] Every rendered page visually inspected for layout, table breaks, and text clipping.
- [ ] Exact final `.docx` deliverable verified and bound to its SHA-256 hash.
- [ ] Zero AI attribution in metadata, document content, or author properties.
- [ ] No U+2014 em dashes in normal prose.

