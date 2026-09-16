# PDF Generation Examples: Good vs Bad Patterns

## 1. Flowable Document Construction (ReportLab)

### Bad (Hardcoded Canvas Offsets and No Pagination Protection)

```python
# BAD: Hardcoded coordinates, manual page tracking, no widow/orphan control
from reportlab.pdfgen import canvas

def generate_report(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Quarterly Financial Overview")
    y = 720
    for row in get_data():
        c.drawString(100, y, f"{row['item']}: {row['val']}")
        y -= 20
        if y < 50:  # Manual break without headers or page numbering
            c.showPage()
            y = 750
    c.save()
```

Defects:
- Hardcoded coordinates break when content length varies.
- Table and list items split unpredictably across pages.
- Continuation pages lack repeated context headers.
- Total page count and formal folios are absent.

### Good (Platypus Flowables, Repeating Table Headers, and Numbered Canvas)

```python
# GOOD: Flowables, KeepTogether, repeatRows, and two-pass page numbering
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_report(filename, data):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Quarterly Financial Overview", styles['Title']),
        Spacer(1, 14)
    ]
    
    table_data = [["Item", "Value"]] + [[r["item"], r["val"]] for r in data]
    t = Table(table_data, colWidths=[300, 168], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    doc.build(story)
```

Advantages:
- `repeatRows=1` automatically repeats the header on every continuation page.
- Margin boundaries strictly enforced through document template.
- Content reflows cleanly without overlapping text or clipped boundaries.
