# Spreadsheet Examples: Good vs Bad Patterns

## 1. Financial Projection Model

### Bad (Hardcoded Constants, Broken References, and Missing Types)

```python
# BAD: Hardcoding formulas, numbers as strings, no explicit error guards
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Projections"

ws["A1"] = "Revenue"
ws["B1"] = "$100,000"  # Stored as string, cannot be summed cleanly
ws["A2"] = "Growth"
ws["B2"] = "5%"

# Hardcoded multiplier inside formula without cell reference
ws["A3"] = "Year 2 Projected"
ws["B3"] = "=B1 * 1.05"  # Fails if B1 is string!

# Direct division without zero check
ws["A4"] = "Margin"
ws["B4"] = "=C1 / B1"  # Results in #DIV/0! or #VALUE!
```

Defects:
- Currency and percentage values formatted as text strings rather than numeric types with number formats.
- Growth rate hardcoded (`1.05`) rather than referencing input cell `B2`.
- Unguarded division throws formula error.

### Good (Native Numeric Types, Formula References, and Error Guards)

```python
# GOOD: Numeric values, number_format, dynamic formula references, error handling
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Financial_Summary"

# Inputs Block
ws["A1"] = "Base Revenue"
ws["B1"] = 100000
ws["B1"].number_format = '"$"#,##0'

ws["A2"] = "Annual Growth Rate"
ws["B2"] = 0.05
ws["B2"].number_format = '0.0%'

# Calculations Block
ws["A3"] = "Year 2 Projected Revenue"
ws["B3"] = "=B1 * (1 + $B$2)"
ws["B3"].number_format = '"$"#,##0'

ws["A4"] = "Net Margin Ratio"
ws["B4"] = '=IFERROR(B5 / B3, 0.0)'
ws["B4"].number_format = '0.0%'

# Style header
ws.column_dimensions["A"].width = 28
ws.column_dimensions["B"].width = 16
```

Advantages:
- Uses native numeric data types with explicit OpenPyXL number formatting.
- Formula dynamically links to assumption cell `$B$2`.
- Zero-division safely caught via `IFERROR`.
- Column widths adjusted to eliminate cell truncation or `###` display errors.
