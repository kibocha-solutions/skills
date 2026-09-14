#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


parser = argparse.ArgumentParser()
parser.add_argument("html", type=Path)
parser.add_argument("screenshot", type=Path)
args = parser.parse_args()

html = args.html.resolve()
if not html.is_file():
    raise SystemExit(f"HTML file does not exist: {html}")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    try:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(html.as_uri(), wait_until="domcontentloaded")
        page.locator("body").wait_for(state="visible")
        args.screenshot.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(args.screenshot), full_page=True)
    finally:
        browser.close()
