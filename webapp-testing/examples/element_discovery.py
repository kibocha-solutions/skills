#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("screenshot", type=Path)
args = parser.parse_args()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    try:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(args.url, wait_until="domcontentloaded")
        page.locator("body").wait_for(state="visible")

        for selector in ("button", "a[href]", "input", "textarea", "select"):
            locator = page.locator(selector)
            print(f"{selector}: {locator.count()}")

        args.screenshot.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(args.screenshot), full_page=True)
    finally:
        browser.close()
