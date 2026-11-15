#!/usr/bin/env python3
"""Maestro session housekeeping for one project.

Usage (run from anywhere inside the project):
  sessions.py status                          List active sessions with state, idle days, and size.
  sessions.py close <session> <STATE> [note]  Set a closed state and archive the session.
  sessions.py stale [--apply]                 Close sessions idle past the limit as ABANDONED.
  sessions.py index                           Rewrite sessions/archive/INDEX.md.
  sessions.py prune [--keep N] [--apply]      Thin the archive (dry run by default).

Closed states: DONE, PARTIAL, SUPERSEDED, ABANDONED.
Open states: PLANNING, EXECUTING, VERIFYING, BLOCKED.
Exit codes: 0 success; 1 usage error or refused action.
"""
from __future__ import annotations

import datetime
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

OPEN_STATES = ("PLANNING", "EXECUTING", "VERIFYING", "BLOCKED")
CLOSED_STATES = ("DONE", "PARTIAL", "SUPERSEDED", "ABANDONED")
STALE_DAYS = 14
KEEP_ARCHIVED = 10
STATE_LINE = re.compile(r"^\W*state\W*[:=]\s*(.+?)\s*(-->)?\s*$", re.I | re.M)
EVIDENCE_EXT = re.compile(
    r"\.(png|jpe?g|webp|gif|bmp|svg|mp4|webm|mov|pdf|zip|tar|gz|zst|xz|7z|har|trace|log)$", re.I
)
TODAY = datetime.date.today()


def git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def project_root() -> Path:
    out = git(["rev-parse", "--show-toplevel"], Path.cwd())
    root = Path(out.stdout.strip()) if out.returncode == 0 else Path.cwd()
    probe = root
    while not (probe / ".agents").is_dir() and probe != probe.parent:
        probe = probe.parent
    return probe if (probe / ".agents").is_dir() else root


def brain() -> Path:
    return project_root() / ".agents" / "brain"


def in_git(path: Path) -> bool:
    return git(["ls-files", "--error-unmatch", str(path)], path.parent).returncode == 0


def last_change(folder: Path) -> datetime.date:
    stamps = [p.stat().st_mtime for p in folder.rglob("*") if p.is_file()]
    stamp = max(stamps) if stamps else folder.stat().st_mtime
    return datetime.date.fromtimestamp(stamp)


def size_mb(folder: Path) -> float:
    return sum(p.stat().st_size for p in folder.rglob("*") if p.is_file()) / 1048576


def read_state(folder: Path) -> str:
    tasks = folder / "tasks.md"
    if not tasks.exists():
        return "UNKNOWN"
    match = STATE_LINE.search(tasks.read_text(encoding="utf-8", errors="replace"))
    if not match:
        return "UNKNOWN"
    word = re.match(r"[A-Za-z_]+", match.group(1).strip("`* "))
    value = word.group(0).upper() if word else "UNKNOWN"
    return {"CLOSED": "DONE", "COMPLETE": "DONE", "COMPLETED": "DONE"}.get(value, value)


def write_state(folder: Path, state: str, note: str) -> None:
    tasks = folder / "tasks.md"
    text = tasks.read_text(encoding="utf-8", errors="replace") if tasks.exists() else f"# Tasks: {folder.name}\n"
    line = f"## State: {state}" + (f" ({note})" if note else "")
    if STATE_LINE.search(text):
        text = STATE_LINE.sub(line, text, count=1)
    else:
        lines = text.splitlines()
        lines.insert(1 if lines and lines[0].startswith("#") else 0, "\n" + line)
        text = "\n".join(lines) + "\n"
    tasks.write_text(text, encoding="utf-8")


def move(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if in_git(src / "tasks.md") if src.is_dir() else in_git(src):
        result = git(["mv", str(src), str(dst)], src.parent)
        if result.returncode == 0:
            return
    shutil.move(str(src), str(dst))


def move_evidence(folder: Path) -> int:
    project = project_root().name
    dest_root = Path.home() / ".agents" / "evidence" / project / folder.name
    moved = 0
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.name == "EVIDENCE.md":
            continue
        if EVIDENCE_EXT.search(path.name) or path.stat().st_size > 1048576:
            target = dest_root / path.relative_to(folder)
            target.parent.mkdir(parents=True, exist_ok=True)
            tracked = in_git(path)
            shutil.move(str(path), str(target))
            if tracked:
                git(["rm", "--cached", "-q", str(path)], folder)
            moved += 1
    if moved:
        (dest_root / ".last-used").touch()
        note = folder / "meta" / "EVIDENCE.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(f"Evidence moved to ~/.agents/evidence/{project}/{folder.name}/ on {TODAY}.\n",
                        encoding="utf-8")
    return moved


def archive_session(folder: Path) -> Path:
    moved = move_evidence(folder)
    target = brain() / "sessions" / "archive" / folder.name
    move(folder, target)
    print(f"archived {folder.name} ({moved} evidence files moved to the agent store)")
    return target


def status() -> int:
    active = sorted((brain() / "sessions" / "active").glob("*/"))
    archived = list((brain() / "sessions" / "archive").glob("*/"))
    print(f"{'State':<11} {'Idle':>5} {'MB':>6}  Session")
    for folder in active:
        idle = (TODAY - last_change(folder)).days
        flag = "  <- stale" if idle > STALE_DAYS and read_state(folder) not in CLOSED_STATES else ""
        flag = "  <- closed, archive it" if read_state(folder) in CLOSED_STATES else flag
        print(f"{read_state(folder):<11} {idle:>4}d {size_mb(folder):>6.1f}  {folder.name}{flag}")
    print(f"active: {len(active)}  archived: {len(archived)}")
    return 0


def close(args: list[str]) -> int:
    if len(args) < 2 or args[1].upper() not in CLOSED_STATES:
        print(f"usage: sessions.py close <session> <{'|'.join(CLOSED_STATES)}> [note]", file=sys.stderr)
        return 1
    folder = brain() / "sessions" / "active" / args[0].rstrip("/").split("/")[-1]
    if not folder.is_dir():
        print(f"no active session named {folder.name}", file=sys.stderr)
        return 1
    write_state(folder, args[1].upper(), " ".join(args[2:]))
    archive_session(folder)
    index()
    return 0


def stale(args: list[str]) -> int:
    apply = "--apply" in args
    for folder in sorted((brain() / "sessions" / "active").glob("*/")):
        state = read_state(folder)
        idle = (TODAY - last_change(folder)).days
        if state in CLOSED_STATES:
            print(f"{'archive' if apply else 'would archive'} {folder.name} (state {state})")
            if apply:
                archive_session(folder)
        elif idle > STALE_DAYS:
            since = TODAY - datetime.timedelta(days=idle)
            print(f"{'close' if apply else 'would close'} {folder.name} as ABANDONED (idle since {since})")
            if apply:
                write_state(folder, "ABANDONED", f"closed {TODAY}: idle since {since}")
                archive_session(folder)
    if apply:
        index()
    return 0


def index() -> int:
    archive = brain() / "sessions" / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    rows = []
    for folder in archive.glob("*/"):
        walkthrough = folder / "walkthrough.md"
        outcome = "none recorded"
        if walkthrough.exists():
            for line in walkthrough.read_text(encoding="utf-8", errors="replace").splitlines():
                text = line.strip().lstrip("-*0123456789. ")
                if text and not line.lstrip().startswith("#"):
                    outcome = text.replace("|", "/")[:120]
                    break
        rows.append((last_change(folder), folder.name, read_state(folder), outcome))
    existing = archive / "INDEX.md"
    retired = []
    if existing.exists():
        retired = [line for line in existing.read_text(encoding="utf-8").splitlines() if "| retired " in line]
    lines = ["# Archived sessions", "", "| Session | State | Last change | Outcome |", "| :--- | :--- | :--- | :--- |"]
    lines += [f"| {name} | {state} | {date} | {outcome} |" for date, name, state, outcome in sorted(rows, key=lambda r: r[1], reverse=True)]
    lines += retired
    existing.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index: {len(rows)} archived, {len(retired)} retired")
    return 0


def prune(args: list[str]) -> int:
    apply = "--apply" in args
    keep = int(args[args.index("--keep") + 1]) if "--keep" in args else KEEP_ARCHIVED
    archive = brain() / "sessions" / "archive"
    folders = sorted(archive.glob("*/"), key=lambda f: f.name, reverse=True)[keep:]
    root = project_root()
    clean_git = git(["status", "--porcelain", "--", str(archive)], root)
    for folder in folders:
        tracked = in_git(folder / "tasks.md")
        if tracked and clean_git.returncode == 0 and not clean_git.stdout.strip():
            commit = git(["log", "-1", "--format=%h", "--", str(folder)], root).stdout.strip()
            print(f"{'retire' if apply else 'would retire'} {folder.name} (restorable from commit {commit})")
            if apply:
                with (archive / "INDEX.md").open("a", encoding="utf-8") as fh:
                    fh.write(f"| {folder.name} | retired | {last_change(folder)} | restore: git checkout {commit} -- {folder.relative_to(root)} |\n")
                git(["rm", "-r", "-q", str(folder)], root)
        elif tracked:
            print(f"skip {folder.name}: commit the archive before pruning")
        else:
            quarter = f"{last_change(folder).year}-Q{(last_change(folder).month - 1) // 3 + 1}"
            bundle = archive / f"{quarter}.tar.gz"
            print(f"{'bundle' if apply else 'would bundle'} {folder.name} into {bundle.name}")
            if apply:
                tmp = archive / f".{quarter}.tmp"
                shutil.rmtree(tmp, ignore_errors=True)
                tmp.mkdir()
                if bundle.exists():
                    with tarfile.open(bundle, "r:gz") as tar:
                        tar.extractall(tmp, filter="data")
                shutil.move(str(folder), str(tmp / folder.name))
                partial = archive / f".{quarter}.tar.gz.partial"
                with tarfile.open(partial, "w:gz") as tar:
                    for child in sorted(tmp.iterdir()):
                        tar.add(child, arcname=child.name)
                partial.replace(bundle)
                shutil.rmtree(tmp)
    if apply:
        index()
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    command, args = sys.argv[1], sys.argv[2:]
    if not (project_root() / ".agents").is_dir():
        print("no .agents directory found for this project", file=sys.stderr)
        return 1
    handlers = {"status": lambda: status(), "close": lambda: close(args), "stale": lambda: stale(args),
                "index": lambda: index(), "prune": lambda: prune(args)}
    if command not in handlers:
        print(__doc__, file=sys.stderr)
        return 1
    return handlers[command]()


if __name__ == "__main__":
    sys.exit(main())
