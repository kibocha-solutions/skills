---
name: pptx
description: Read, create, edit, combine, split, convert, render, and verify PowerPoint `.pptx` and template `.potx` files. Use for presentations, decks, slides, templates, layouts, speaker notes, comments, or any task with a PowerPoint file as input or output.
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX

## 1. Establish the task

1. Identify every source deck, template, reference, data source, and requested output.
2. Confirm the audience, purpose, delivery setting, slide count, aspect ratio, language, and brand constraints.
3. Preserve original files unless the user requests replacement.
4. Distinguish source facts, template structure, examples, and proposed content.
5. Read `../system-init/SKILL.md` before installing a missing dependency.

## 2. Inspect an existing deck

1. Extract text with `python -m markitdown <deck.pptx>`.
2. Create a slide overview with `python scripts/thumbnail.py <deck.pptx>`.
3. Render full-resolution slide images when layout matters.
4. Read every slide in order.
5. Read speaker notes and comments when they are in scope.
6. Record slide size, masters, layouts, fonts, theme colors, logos, recurring elements, charts, tables, and media.
7. Identify placeholders, sample data, stale dates, broken links, and hidden slides.

## 3. Select the build path

### Existing template or deck

1. Read [editing](references/editing.md) in full.
2. Map each requested slide to an existing layout.
3. Preserve the template's masters, theme, typography, spacing, and brand system.
4. Complete structural slide changes before editing slide content.
5. Use the bundled unpack, add, clean, pack, and validate scripts.

### New deck

1. Read [PptxGenJS](references/pptxgenjs.md) in full.
2. Define the aspect ratio and slide master.
3. Create shared theme, typography, color, spacing, and component helpers.
4. Use a fresh presentation instance.
5. Use fresh option objects for every PptxGenJS call.

## 4. Build the storyboard

1. State one communication objective per slide.
2. Put slides in a clear narrative order.
3. Give each slide an assertion title.
4. Assign the supporting evidence, visual, and source to each slide.
5. Remove slides that do not advance the narrative or satisfy a requested function.
6. Keep appendix and reference slides separate from the main narrative.

## 5. Define the design system

1. Derive colors and typography from the template, brand, or subject.
2. Use one dominant color, supporting neutrals, and a restrained accent set.
3. Use readable fonts available in the rendering environment.
4. Set minimum slide-edge margins of 0.5 inches unless the template requires another grid.
5. Set consistent gaps between related components.
6. Use high contrast for text, icons, charts, and controls.
7. Use full branding on the title slide only.
8. Use a reduced identity and slide number on content slides when branding is required.
9. Do not add decorative title underlines.
10. Do not add ungrounded decorative elements.

Read [letterhead and pagination](../documentation/references/letterhead-and-pagination.md) when the deck carries formal branding.

## 6. Lay out each slide

1. Choose a layout that matches the content relationship.
2. Vary layouts without breaking the design system.
3. Use left-aligned body text.
4. Use centered text only where the composition requires it.
5. Keep text within the assigned box and margin grid.
6. Remove unused template elements completely.
7. Keep each list item in a separate paragraph.
8. Use native bullets or numbering.
9. Do not type Unicode bullet characters into bulleted text.
10. Preserve image aspect ratios.
11. Add useful alternative text to images.

## 7. Add content

1. Use verified source facts only.
2. Keep titles concise and specific.
3. Keep body text scannable at presentation distance.
4. Use full titles for people, organizations, programmes, and instruments when required.
5. Put citations in a consistent source area.
6. Keep internal paths, drafting notes, approval status, and production commentary out of slides.
7. Remove all placeholder and sample text.
8. Preserve user-supplied wording when locked.

## 8. Add visuals and data

1. Use charts for quantitative relationships.
2. Use diagrams for process, hierarchy, architecture, or causality.
3. Use tables only when exact comparison requires them.
4. Use images only when they support the slide's claim or required design.
5. Label chart units, time periods, categories, and sources.
6. Use consistent scales for comparable charts.
7. Avoid misleading axes, truncated context, or decorative data marks.
8. Verify every value against its source.
9. Recompute material figures independently.

## 9. Edit package content

1. Unpack the deck with `scripts/office/unpack.py`.
2. Change slide order in `ppt/presentation.xml`.
3. Duplicate or add slides with `scripts/add_slide.py`.
4. Edit only the required slide, relationship, notes, comments, theme, or media files.
5. Preserve XML namespaces and relationship identifiers.
6. Use XML entities for smart quotation marks when editing raw XML.
7. Run `scripts/clean.py` after structural changes.
8. Repack with `scripts/office/pack.py` and the original deck.

## 10. Validate content and structure

1. Run `python -m markitdown <output.pptx>`.
2. Compare extracted text with the approved storyboard and sources.
3. Search for placeholder residue, sample names, stale dates, and missing content.
4. Validate the Office package with `scripts/office/validate.py`.
5. Open the final deck with LibreOffice or PowerPoint-compatible software.
6. Confirm slide order, hidden-slide state, links, notes, comments, charts, tables, and media.

## 11. Render and inspect

1. Convert the final deck to PDF with `scripts/office/soffice.py`.
2. Render every slide to an individual image with `pdftoppm`.
3. Inspect every slide at readable resolution.
4. Check overlap, clipping, overflow, broken glyphs, wrapping, alignment, spacing, margins, contrast, chart labels, citations, footer collisions, image quality, and placeholder residue.
5. Compare each rendered slide with its storyboard objective.
6. Correct every verified defect.
7. Re-render every corrected slide.
8. Re-run full content and package validation after the last correction.
9. Deliver only the exact verified `.pptx` file.

Inspect [deck examples](examples/good-vs-bad-deck-patterns.md) for assertion-evidence layout patterns.

## 12. Pre-completion checklist

Before delivering any PowerPoint presentation, confirm evidence exists for each item:

- [ ] Source facts, data, and storyboard read manually in full from start to finish.
- [ ] Every slide has an assertion title delivering the core takeaway.
- [ ] Office package validates without errors via `validate.py`.
- [ ] Converted to PDF and rendered to slide images (`pdftoppm -jpeg -r 150`).
- [ ] Every slide image visually inspected for contrast, alignment, text clipping, and wrapping.
- [ ] All sample data, placeholder residue, and template defaults removed.
- [ ] Exact final `.pptx` deliverable verified and bound to its SHA-256 hash.
- [ ] Zero AI attribution in slides, speaker notes, author properties, or metadata.
- [ ] No U+2014 em dashes in normal prose.

