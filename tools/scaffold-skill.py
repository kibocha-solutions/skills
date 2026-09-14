#!/usr/bin/env python3
"""Create a minimal top-level skill package without overwriting existing files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_DIRECTORIES = ("references", "assets", "scripts")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a minimal skill package that passes repository structure checks."
    )
    parser.add_argument("name", help="Skill name in lowercase kebab-case")
    parser.add_argument(
        "--description",
        required=True,
        help="Frontmatter description containing the skill trigger conditions",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Parent directory for the skill package",
    )
    parser.add_argument(
        "--resource-dir",
        action="append",
        choices=RESOURCE_DIRECTORIES,
        default=[],
        help="Create an empty resource directory; repeat for multiple directories",
    )
    return parser.parse_args()


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def skill_text(name: str, description: str) -> str:
    title = title_from_name(name)
    return f'''---
name: {name}
description: {json.dumps(description, ensure_ascii=False)}
---

# {title}

## Inputs

1. Collect the inputs named in the request.
2. Confirm the requested output and its destination.

## Procedure

1. Perform the requested operation in execution order.
2. Apply each task-specific constraint at the step it governs.

## Verification

1. Verify the final output against the request.
2. Report the output location and validation result.
'''


def main() -> int:
    args = parse_args()
    name = args.name.strip()
    description = args.description.strip()

    if not NAME_PATTERN.fullmatch(name):
        print("error: name must use lowercase kebab-case", file=sys.stderr)
        return 2
    if not description or "\n" in description:
        print("error: description must be one non-empty line", file=sys.stderr)
        return 2

    root = args.root.expanduser().resolve()
    destination = root / name
    if destination.exists():
        print(f"error: destination already exists: {destination}", file=sys.stderr)
        return 1

    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text(
        skill_text(name, description),
        encoding="utf-8",
    )
    for directory in dict.fromkeys(args.resource_dir):
        (destination / directory).mkdir()

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
