# Editing Presentations

## Template procedure

1. Read the project instructions.
2. Inspect the template with:

```bash
python3 pptx/scripts/thumbnail.py template.pptx
python3 -m markitdown template.pptx
```

3. Open and inspect the thumbnail output.
4. Map each required content unit to an existing layout.
5. Use layout variation that matches the content.
6. Keep template masters, theme, typography, palette, and geometry.
7. Remove unused template slides and placeholder objects.
8. Render and inspect the exact final deck.

## Package procedure

1. Unpack the source:

```bash
python3 pptx/scripts/office/unpack.py input.pptx unpacked/
```

2. Complete structural changes before text replacement.
3. Reorder slides through `ppt/presentation.xml` and `p:sldIdLst`.
4. Delete a slide by removing its `p:sldId`.
5. Add or duplicate a slide with:

```bash
python3 pptx/scripts/add_slide.py unpacked/ slide2.xml
python3 pptx/scripts/add_slide.py unpacked/ slideLayout2.xml
```

6. Insert the returned `p:sldId` at the intended position.
7. Edit each slide XML.
8. Run:

```bash
python3 pptx/scripts/clean.py unpacked/
python3 pptx/scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

9. Reopen, render, and inspect `output.pptx`.

## Slide content procedure

1. Read the complete slide XML.
2. Identify every placeholder text run, image, chart, icon, caption, note, and relationship.
3. Replace every placeholder with final content.
4. Delete unused shapes and their relationships.
5. Keep one `a:p` element for each independent paragraph or list item.
6. Use `a:buChar` or `a:buAutoNum` for lists.
7. Do not insert a Unicode bullet character into text.
8. Preserve `a:pPr` when retaining the source paragraph style.
9. Use `b="1"` only where the template or design requires bold text.
10. Use `xml:space="preserve"` for intentional leading or trailing spaces.
11. Encode smart quotation marks with XML entities when direct XML editing requires them.
12. Validate relationships and content types after every structural edit.

## Layout checks

- Match layout to content type.
- Keep text within established content regions.
- Remove complete groups when the source has fewer items than the template.
- Split content when it exceeds the available region.
- Do not shrink body text below the deck's established minimum.
- Keep image crops, chart bounds, and captions aligned.
- Avoid repeating one layout when the content requires distinct structures.
- Do not add decorative variation unsupported by the template.

## Smart quotation entities

| Character | Entity |
|---|---|
| Left double quotation mark | `&#x201C;` |
| Right double quotation mark | `&#x201D;` |
| Left single quotation mark | `&#x2018;` |
| Right single quotation mark | `&#x2019;` |

## Script reference

| Script | Operation |
|---|---|
| `scripts/thumbnail.py` | Create a labeled slide overview |
| `scripts/office/unpack.py` | Extract and format package XML |
| `scripts/add_slide.py` | Add a slide from a slide or layout |
| `scripts/clean.py` | Remove orphaned package parts |
| `scripts/office/pack.py` | Repack and validate the presentation |

## Final checks

- [ ] Slide order matches the requested narrative.
- [ ] Every placeholder is removed.
- [ ] Every relationship resolves.
- [ ] Every list uses native list markup.
- [ ] Text, images, charts, and captions fit.
- [ ] The package validator passes.
- [ ] The exact final deck opens.
- [ ] Every final slide was rendered and visually inspected.
