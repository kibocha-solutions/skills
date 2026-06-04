#!/usr/bin/env python3
"""Validate a Draw.io source/export bundle before visual inspection.

The script checks source XML parseability, obvious mxGraph edge references,
matching export presence, and bundled JSON assets. It does not replace rendered
visual QA.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_xml(path: Path) -> ET.Element:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{path} is not valid XML: {exc}")


def validate_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")


def check_drawio(path: Path) -> None:
    root = load_xml(path)
    cells = root.findall(".//mxCell")
    if not cells:
        fail(f"{path} contains no mxCell elements")

    ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for cell in cells:
        cell_id = cell.attrib.get("id")
        if not cell_id:
            fail(f"{path} contains an mxCell without an id")
        if cell_id in ids:
            duplicate_ids.add(cell_id)
        ids.add(cell_id)

    if duplicate_ids:
        fail(f"{path} contains duplicate ids: {', '.join(sorted(duplicate_ids))}")

    for cell in cells:
        if cell.attrib.get("edge") == "1":
            edge_id = cell.attrib.get("id", "<unknown>")
            for attr in ("source", "target"):
                ref = cell.attrib.get(attr)
                if ref and ref not in ids:
                    fail(f"edge {edge_id} has invalid {attr}: {ref}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to .drawio source")
    parser.add_argument("--export", type=Path, help="Expected SVG or PNG export")
    parser.add_argument(
        "--asset",
        action="append",
        type=Path,
        default=[],
        help="JSON asset to validate; repeat for multiple assets",
    )
    args = parser.parse_args()

    if not args.source.is_file():
        fail(f"source file does not exist: {args.source}")
    check_drawio(args.source)

    if args.export and not args.export.is_file():
        fail(f"export file does not exist: {args.export}")

    for asset in args.asset:
        if not asset.is_file():
            fail(f"asset file does not exist: {asset}")
        validate_json(asset)

    print("Bundle checks passed. Rendered visual QA is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
