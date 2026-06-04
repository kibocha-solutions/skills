#!/usr/bin/env python3
"""Check whether a project has the required starting technical docs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = [
    "README.md",
    "docs/writerside/writerside.cfg",
    "docs/writerside/public.tree",
    "docs/writerside/internal.tree",
    "docs/writerside/restricted.tree",
    "docs/writerside/snippets/",
    "docs/product/project-brief.md",
    "docs/product/product-doctrine.md",
    "docs/product/mvp-scope-boundaries.md",
    "docs/product/public-private-visibility.md",
    "docs/planning/decision-log.md",
    "docs/planning/assumptions-register.md",
    "docs/planning/risk-register.md",
    "docs/architecture/architecture-overview.md",
    "docs/architecture/system-context.md",
    "docs/architecture/api-boundary-doctrine.md",
    "docs/architecture/decisions/",
    "docs/domain/domain-model.md",
    "docs/domain/entity-relationship-model.md",
    "docs/domain/document-lifecycle.md",
    "docs/data/object-document-model.md",
    "docs/security/security-baseline.md",
    "docs/security/permission-tenant-isolation.md",
    "docs/diagrams/system-context.drawio",
    "docs/diagrams/system-context.svg",
    "docs/diagrams/permission-model.drawio",
    "docs/diagrams/permission-model.svg",
    "docs/diagrams/entity-relationship.drawio",
    "docs/diagrams/entity-relationship.svg",
]


def exists(root: Path, rel: str) -> bool:
    path = root / rel.rstrip("/")
    return path.is_dir() if rel.endswith("/") else path.is_file()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report missing required starting technical documentation."
    )
    parser.add_argument("root", nargs="?", default=".", help="Project root.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a plain text report.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    missing = [rel for rel in REQUIRED if not exists(root, rel)]

    if args.json:
        print(json.dumps({"root": str(root), "missing": missing}, indent=2))
    elif missing:
        print("Missing required starting technical docs:")
        for rel in missing:
            print(f"- {rel}")
    else:
        print("All required starting technical docs are present.")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
