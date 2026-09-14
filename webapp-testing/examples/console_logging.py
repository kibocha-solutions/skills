#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("output", type=Path)
args = parser.parse_args()

messages: list[str] = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    try:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda message: messages.append(f"[{message.type}] {message.text}"))
        page.on("pageerror", lambda error: messages.append(f"[pageerror] {error}"))
        page.goto(args.url, wait_until="domcontentloaded")
        page.locator("body").wait_for(state="visible")
    finally:
        browser.close()

args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text("\n".join(messages), encoding="utf-8")
print(f"Captured {len(messages)} browser messages in {args.output}")
