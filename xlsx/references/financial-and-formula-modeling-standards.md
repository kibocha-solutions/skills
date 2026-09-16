# Spreadsheet Financial and Formula Modeling Standards

## 1. Workbook Architecture

1. **Sheet Separation**:
   - `Assumptions` / `Inputs`: Raw inputs, parameters, inflation rates, and unit costs.
   - `Calculations` / `Engine`: Intermediate projections, depreciation schedules, and operating costs.
   - `Summary` / `Outputs`: Financial statements, executive KPIs, and chart staging tables.

2. **Cell Color and Styling Conventions**:
   - Blue text (`#0000FF`) or neutral input cells for variable user assumptions.
   - Black text (`#000000`) for calculated formula cells.
   - Green text (`#008000`) for cross-sheet or external links.

## 2. Formula Hygiene

1. **No Hardcoded Constants in Formulas**:
   - Bad: `=B5 * 1.08`
   - Good: `=B5 * (1 + $C$2)` where `$C$2` contains the explicit 8% tax rate.

2. **Division by Zero Protection**:
   - Use `IFERROR` or `IF(denominator=0, 0, numerator/denominator)`.
   - Never allow `#DIV/0!`, `#REF!`, or `#VALUE!` to persist in completed deliverables.

3. **Dynamic Range Discipline**:
   - Use uppercase for formula names (`SUM`, `VLOOKUP`, `INDEX`, `MATCH`, `XLOOKUP`).
   - Lock reference ranges when copying across periods (`$B$4:$M$4`).

## 3. Exact Artifact Verification

1. Calculate the SHA-256 hash of the final `.xlsx` file upon completion.
2. Verify that recalculated formula values match independent sanity calculations.
