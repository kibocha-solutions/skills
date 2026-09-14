#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

python3 - "$repo_root" <<'PY'
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote

root = Path(sys.argv[1])
errors: list[str] = []
skill_dirs = sorted(path.parent for path in root.glob("*/SKILL.md"))

agents_file = root / "AGENTS.md"
agents_text = agents_file.read_text(encoding="utf-8")
agents_words = len(agents_text.split())
if agents_words >= 1500:
    errors.append(f"AGENTS.md: {agents_words} words; limit is 1499")

agents_sections = re.findall(r"^## (.+)$", agents_text, re.MULTILINE)
required_opening_sections = ["1. General commands", "2. Working with skills"]
if agents_sections[:2] != required_opening_sections:
    errors.append("AGENTS.md: general commands and skill procedure must be first")

if (root / "docs" / "SKILL_AUTHORING_GUIDE.md").exists():
    errors.append("docs/SKILL_AUTHORING_GUIDE.md: authoring standard must live in skill-creator")
if not (root / "skill-creator" / "references" / "skill-authoring-standard.md").is_file():
    errors.append("skill-creator: missing references/skill-authoring-standard.md")

if not skill_dirs:
    errors.append("no top-level skills found")

frontmatter_name = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
frontmatter_description = re.compile(r"^description:\s*(.+?)\s*$", re.MULTILINE)
markdown_link = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
forbidden = {
    "U+2014 em dash": "—",
    "cross mark emoji": "❌",
    "check mark emoji": "✅",
    "warning emoji": "⚠",
}
residue_patterns = {
    "TODO marker": re.compile(r"\bTODO\b", re.IGNORECASE),
    "TBD marker": re.compile(r"\bTBD\b", re.IGNORECASE),
    "FIXME marker": re.compile(r"\bFIXME\b", re.IGNORECASE),
    "placeholder declaration": re.compile(r"not implemented yet", re.IGNORECASE),
    "lorem ipsum": re.compile(r"lorem ipsum", re.IGNORECASE),
    "AI author residue": re.compile(r"AI Assistant", re.IGNORECASE),
    "mandatory subagent routing": re.compile(
        r"(?:always|must|use)\s+(?:a\s+)?subagents?\s+here", re.IGNORECASE
    ),
    "conditional AI attribution exception": re.compile(
        r"(?:AI attribution|attribute the work to AI).{0,80}"
        r"(?:unless|if|when)\s+the user",
        re.IGNORECASE | re.DOTALL,
    ),
    "obsolete installation permission gate": re.compile(
        r"(?:ask|obtain (?:user )?approval)\s+before\s+"
        r"(?:an? |any )?(?:network |global )?(?:dependency )?"
        r"(?:installation|installing|download)",
        re.IGNORECASE,
    ),
    "obsolete installation prohibition": re.compile(
        r"do not (?:install|download).{0,60}without "
        r"(?:separate )?(?:user )?authorization",
        re.IGNORECASE | re.DOTALL,
    ),
}

for label, token in forbidden.items():
    if token in agents_text:
        errors.append(f"AGENTS.md: contains {label}")
for label, pattern in residue_patterns.items():
    if pattern.search(agents_text):
        errors.append(f"AGENTS.md: contains {label}")

for skill_dir in skill_dirs:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not text.startswith("---\n"):
        errors.append(f"{skill_file.relative_to(root)}: missing opening frontmatter delimiter")
        continue
    parts = text.split("---", 2)
    if len(parts) != 3:
        errors.append(f"{skill_file.relative_to(root)}: missing closing frontmatter delimiter")
        continue

    frontmatter = parts[1]
    name_match = frontmatter_name.search(frontmatter)
    description_match = frontmatter_description.search(frontmatter)
    if not name_match:
        errors.append(f"{skill_file.relative_to(root)}: missing name")
    else:
        name = name_match.group(1).strip().strip("'\"")
        if name != skill_dir.name:
            errors.append(
                f"{skill_file.relative_to(root)}: name {name!r} does not match directory"
            )
    if not description_match or not description_match.group(1).strip().strip("'\""):
        errors.append(f"{skill_file.relative_to(root)}: missing description")
    if len(lines) >= 500:
        errors.append(f"{skill_file.relative_to(root)}: {len(lines)} lines; limit is 499")

    for markdown_file in sorted(skill_dir.rglob("*.md")):
        relative = markdown_file.relative_to(root)
        content = markdown_file.read_text(encoding="utf-8")

        for label, token in forbidden.items():
            if token in content:
                errors.append(f"{relative}: contains {label}")

        for label, pattern in residue_patterns.items():
            if pattern.search(content):
                errors.append(f"{relative}: contains {label}")

        if "references" in markdown_file.parts and len(content.splitlines()) > 300:
            if not re.search(
                r"^## (?:Contents|Table of [Cc]ontents)\s*$",
                content,
                re.MULTILINE,
            ):
                errors.append(f"{relative}: reference exceeds 300 lines without contents")

        for match in markdown_link.finditer(content):
            target = match.group(1).strip()
            if target.startswith("<"):
                close = target.find(">")
                target = target[1:close] if close >= 0 else target[1:]
            else:
                target = target.split(maxsplit=1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "codex:")):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (markdown_file.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{relative}: broken local link {target}")

    for token in re.findall(
        r"`((?:references|assets|scripts)/[A-Za-z0-9_.\/-]+)`",
        text,
    ):
        if not (skill_dir / token).exists():
            errors.append(f"{skill_file.relative_to(root)}: missing routed resource {token}")

for json_file in sorted(
    path for skill_dir in skill_dirs for path in skill_dir.rglob("*.json")
):
    try:
        json.loads(json_file.read_text(encoding="utf-8"))
    except Exception as error:
        errors.append(f"{json_file.relative_to(root)}: invalid JSON: {error}")

for drawio_file in sorted(
    path for skill_dir in skill_dirs for path in skill_dir.rglob("*.drawio")
):
    try:
        ET.parse(drawio_file)
    except Exception as error:
        errors.append(f"{drawio_file.relative_to(root)}: invalid XML: {error}")

python_files = [
    path for skill_dir in skill_dirs for path in skill_dir.rglob("*.py")
]
python_files.extend((root / "tools").glob("*.py"))
for python_file in sorted(python_files):
    python_text = python_file.read_text(encoding="utf-8")
    if "AI Assistant" in python_text:
        errors.append(f"{python_file.relative_to(root)}: contains AI author residue")
    try:
        compile(
            python_text,
            str(python_file),
            "exec",
        )
    except Exception as error:
        errors.append(f"{python_file.relative_to(root)}: Python syntax error: {error}")

if errors:
    print(f"FAILED: {len(errors)} validation error(s)")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"PASS: {len(skill_dirs)} skills passed structural, prose, link, JSON, XML, and Python checks")
PY

while IFS= read -r script; do
  bash -n "$script"
done < <(find . -mindepth 2 -type f -name '*.sh' -not -path './sources/*' -print | sort)

git diff --check

printf 'PASS: shell syntax and git whitespace checks\n'
