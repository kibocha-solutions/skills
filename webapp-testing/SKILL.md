---
name: webapp-testing
description: Test local web applications with Playwright by inspecting the application, starting only authorized local servers, exercising user-visible behavior, capturing browser evidence, and reporting exact failures. Use for frontend verification, browser interaction, screenshots, console errors, network failures, responsive behavior, and UI debugging.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

## Procedure

1. Read the project instructions.
2. Inspect the application entrypoint, routes, server command, expected port, and existing test configuration.
3. Inspect every helper script before executing it.
4. Check whether the required server is already running.
5. Start only the server command required by the project.
6. Use `scripts/with_server.py` when the test requires managed server startup and cleanup.
7. Create a temporary Playwright script or add a project test when the user requested a durable test.
8. Navigate to the exact route under test.
9. Wait for a deterministic application-ready condition.
10. Inspect the rendered DOM and take a baseline screenshot.
11. Select elements by accessible role, label, visible name, test identifier, or stable project selector.
12. Perform the user workflow.
13. Assert the visible result and relevant state change.
14. Capture console errors, page errors, failed requests, and response failures.
15. Test each requested viewport and interaction state.
16. Take final screenshots.
17. Open and visually inspect every screenshot used as evidence.
18. Stop managed servers and close the browser.
19. Run existing relevant tests.
20. Report the exact command, route, checks, evidence paths, and failures.

## Server runner

Inspect help before use:

```bash
python3 webapp-testing/scripts/with_server.py --help
```

Run one server:

```bash
python3 webapp-testing/scripts/with_server.py \
  --server "npm run dev" \
  --port 5173 \
  -- python3 /tmp/ui_check.py
```

Run two servers from separate directories:

```bash
python3 webapp-testing/scripts/with_server.py \
  --server "python3 -m uvicorn app:app" --port 8000 --cwd backend \
  --server "npm run dev" --port 5173 --cwd frontend \
  -- python3 /tmp/ui_check.py
```

## Playwright requirements

- Use a fresh browser context for each isolated scenario.
- Set an explicit viewport.
- Close contexts and browsers in `finally` blocks.
- Use `page.goto(..., wait_until="domcontentloaded")`.
- Wait for a stable element or application state.
- Use time-based waits only when testing time-dependent behavior.
- Keep selectors tied to user-visible semantics or stable project identifiers.
- Assert outcomes after every state-changing action.
- Capture browser and application errors before navigation.
- Save evidence outside the repository unless the project prescribes a test-artifact directory.
- Do not expose secrets, tokens, cookies, or private page content in logs or screenshots.

## Coverage checklist

- [ ] Initial page load
- [ ] Primary user path
- [ ] Validation and error state
- [ ] Loading and empty state
- [ ] Keyboard interaction
- [ ] Focus visibility
- [ ] Requested responsive widths
- [ ] Console and page errors
- [ ] Failed requests and responses
- [ ] Final rendered appearance

Read [Playwright test architecture](references/playwright-test-architecture.md) for locator hierarchy and stability patterns.

## Pre-completion checklist

- [ ] The tested server command matches the project.
- [ ] The tested route is recorded.
- [ ] Assertions cover the requested behavior using semantic role locators.
- [ ] Zero unhandled console errors or failed network requests recorded during test execution.
- [ ] Screenshots come from the exact final application state.
- [ ] Every delivered screenshot was visually inspected.
- [ ] No managed server or browser process remains running.
- [ ] Zero AI attribution in test files, logs, or reports.
- [ ] No U+2014 em dashes in normal prose.
- [ ] Reported results match the exact final test run.

