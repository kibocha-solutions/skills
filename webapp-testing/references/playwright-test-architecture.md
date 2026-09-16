# Playwright Test Architecture

## 1. Clean Testing Principles

Web application testing must exercise real user-visible behavior through accessible locators rather than brittle CSS or XPath selectors.

## 2. Locator Hierarchy

1. **Role Locators (Preferred)**:
   - `page.get_by_role("button", name="Save")`
   - `page.get_by_role("heading", name="Dashboard", level=1)`
   - `page.get_by_role("checkbox", name="Accept terms")`

2. **Label and Text Locators**:
   - `page.get_by_label("Email Address")`
   - `page.get_by_placeholder("Search documents...")`
   - `page.get_by_text("Changes saved successfully")`

3. **Explicit Test IDs (Fallback)**:
   - `page.get_by_test_id("account-dropdown-menu")`

4. **Prohibited Selectors**:
   - Do not use brittle class strings (e.g. `.css-19v2k3f-button`).
   - Do not use deep DOM tree paths (e.g. `div > div:nth-child(3) > button`).

## 3. Asynchronous Stability

1. **Auto-Waiting**:
   - Playwright auto-waits for actionability (visible, stable, enabled) before clicks and fills.
   - Do not introduce arbitrary sleep calls (`time.sleep(3)`). Use locator assertions:
     `expect(locator).to_be_visible()` or `page.wait_for_load_state("networkidle")`.

2. **Network and Console Trapping**:
   - Attach console and network error listeners before calling `page.goto()`.
   - Assert zero unhandled JavaScript errors occur during interaction workflows.
