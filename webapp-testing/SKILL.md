---
name: webapp-testing
description: Test local web applications with Playwright by inspecting the application, starting only authorized local servers, exercising user-visible behavior, capturing browser evidence, and reporting exact failures. Use for frontend verification, browser interaction, screenshots, console errors, network failures, responsive behavior, and UI debugging.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

## 1. Inspect and start the server

1. Read the project instructions.
2. Inspect the application entrypoint, routes, server command, expected port, and existing test configuration.
3. Inspect every helper script before executing it.
4. Check whether the required server is already running.
5. Start only the server command required by the project.
6. Use `scripts/with_server.py` when the test requires managed server startup and cleanup; inspect `python3 webapp-testing/scripts/with_server.py --help` before use:

```bash
python3 webapp-testing/scripts/with_server.py \
  --server "npm run dev" \
  --port 5173 \
  -- python3 /tmp/ui_check.py
```

For two servers from separate directories, pass repeated `--server`, `--port`, and `--cwd` flags.

## 2. Author and execute Playwright checks

1. Read [Playwright test architecture](references/playwright-test-architecture.md) for locator hierarchy, stability patterns, and server-runner details.
2. Inspect [element discovery](examples/element_discovery.py), [console logging](examples/console_logging.py), and [static HTML automation](examples/static_html_automation.py) when concrete Playwright script patterns are needed.
3. Create a temporary Playwright script, or add a project test when the user requested a durable test.
4. Use a fresh browser context with an explicit viewport for each isolated scenario, and close contexts and browsers in `finally` blocks.
5. Capture console errors, page errors, failed requests, and response failures before navigation.
6. Navigate with `page.goto(..., wait_until="domcontentloaded")` and wait for a deterministic application-ready condition; use time-based waits only when testing time-dependent behavior.
7. Inspect the rendered DOM and take a baseline screenshot.
8. Select elements by accessible role, label, visible name, test identifier, or stable project selector.
9. Perform the user workflow and assert visible outcomes after every state-changing action across initial load, primary path, validation/error, loading/empty, keyboard interaction, focus visibility, and requested responsive widths.
10. Launch Playwright's bundled Chromium from the shared browser cache unless the project names another browser; never require an installed Google Chrome.
11. When the change used a Modern Web Guidance guide, assert the behavior the guide specifies, including its fallback in a browser outside the Baseline target when the project tests one.
12. When the change affects loading, rendering, or interaction, record a lab performance trace and compare LCP, INP, and CLS with the thresholds in the [web standards catalogue](../interface-design/references/web-standards-catalogue.md#2-universal-floor).
13. Save final screenshots under `steward.py store path evidence <project>/<maestro-session>` unless the project prescribes a test-artifact directory; do not expose secrets, tokens, cookies, or private page content in logs or screenshots.

## 3. Verify and clean up

1. Open and visually inspect every screenshot used as evidence.
2. Stop managed servers and close the browser.
3. Run existing relevant tests.
4. Report the exact command, route, checks, evidence paths, and failures.

## 4. Pre-completion checklist

- [ ] The tested server command matches the project.
- [ ] The tested route is recorded.
- [ ] Assertions cover the requested behavior using semantic role locators.
- [ ] Zero unhandled console errors or failed network requests recorded during test execution.
- [ ] Behavior specified by each applied Modern Web Guidance guide asserted.
- [ ] Core Web Vitals compared with the catalogue thresholds when loading, rendering, or interaction changed.
- [ ] Screenshots come from the exact final application state.
- [ ] Every delivered screenshot was visually inspected.
- [ ] No managed server or browser process remains running.
- [ ] Zero AI attribution in test files, logs, or reports.
- [ ] No U+2014 em dashes in normal prose.
- [ ] Reported results match the exact final test run.
