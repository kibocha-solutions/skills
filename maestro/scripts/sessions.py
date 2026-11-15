#!/usr/bin/env python3
"""Maestro session housekeeping for one project.

Usage (run from anywhere inside the project):
  sessions.py status                          List active sessions with state, idle days, and size.
  sessions.py close <session> <STATE> [note]  Set a closed state and archive the session.
  sessions.py stale [--apply]                 Close sessions idle past the limit as ABANDONED.
  sessions.py index                           Rewrite sessions/archive/INDEX.md.
  sessions.py prune [--keep N] [--apply]      Thin the archive (dry run by default).
  sessions.py dormant <session> <reason> [--wake <condition>]...
                                              Park an active session under sessions/dormant/.
  sessions.py wake-check                      Evaluate the wake conditions of every dormant session.
  sessions.py wake <session> [note]           Move a dormant session back to active (after user approval).

Closed states: DONE, PARTIAL, SUPERSEDED, ABANDONED.
Open states: PLANNING, EXECUTING, VERIFYING, BLOCKED.
Parked state: DORMANT. Stale, close, and prune never touch a dormant session.
Wake conditions: "date: YYYY-MM-DD", "after: <session> closes", "exists: <project path>",
or any other text, which the agent judges. A session is ready when every checkable
condition is met, or when it has no condition.
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
DORMANT = "DORMANT"
STALE_DAYS = 14
KEEP_ARCHIVED = 10
STATE_LINE = re.compile(r"^\W*state\W*[:=]\s*(.+?)\s*(-->)?\s*$", re.I | re.M)
EVIDENCE_EXT = re.compile(
    r"\.(png|jpe?g|webp|gif|bmp|svg|mp4|webm|mov|pdf|zip|tar|gz|zst|xz|7z|har|trace|log)$", re.I
)
TEXT_SOURCE = re.compile(
    r"\.(md|markdown|txt|rst|json|jsonl|csv|tsv|ya?ml|toml|html?|xml|docx?|xlsx?|pptx?|odt|ods|odp)$", re.I
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
        large_binary = path.stat().st_size > 1048576 and not TEXT_SOURCE.search(path.name)
        if EVIDENCE_EXT.search(path.name) or large_binary:
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
    dormant = sorted((brain() / "sessions" / "dormant").glob("*/"))
    for folder in dormant:
        verdict = wake_verdict(folder)[0]
        print(f"{DORMANT:<11} {'':>5} {size_mb(folder):>6.1f}  {folder.name}  ({verdict})")
    print(f"active: {len(active)}  dormant: {len(dormant)}  archived: {len(archived)}")
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
        if state == DORMANT:
            print(f"{'park' if apply else 'would park'} {folder.name} under sessions/dormant/ (state DORMANT)")
            if apply:
                if not (folder / "wake.md").exists():
                    (folder / "wake.md").write_text(
                        f"# Wake record: {folder.name}\n\nParked {TODAY} from state PLANNING.\n\n## Reason\n\n"
                        "Marked DORMANT in tasks.md; ask the user for the reason.\n\n## Wake conditions\n\n- none\n\n"
                        f"## History\n\n- {TODAY}: parked by stale.\n", encoding="utf-8")
                move(folder, brain() / "sessions" / "dormant" / folder.name)
            continue
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


def wake_conditions(folder: Path) -> list[str]:
    wake = folder / "wake.md"
    if not wake.exists():
        return []
    text = wake.read_text(encoding="utf-8", errors="replace")
    section = re.search(r"^## Wake conditions\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    items = re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+?)\s*$", section.group(1) if section else "", re.M)
    return [i for i in items if i.lower() not in ("none", "none.")]


def check_condition(condition: str) -> str:
    """Return 'met', 'not met', or 'judge'."""
    root = project_root()
    match = re.match(r"(?i)date:\s*(\d{4}-\d{2}-\d{2})$", condition)
    if match:
        return "met" if TODAY >= datetime.date.fromisoformat(match.group(1)) else "not met"
    match = re.match(r"(?i)after:\s*(\S+)\s+closes$", condition)
    if match:
        name = match.group(1)
        archived = (brain() / "sessions" / "archive" / name).is_dir()
        index_file = brain() / "sessions" / "archive" / "INDEX.md"
        listed = index_file.exists() and f"| {name} |" in index_file.read_text(encoding="utf-8")
        return "met" if archived or listed else "not met"
    match = re.match(r"(?i)exists:\s*(.+)$", condition)
    if match:
        return "met" if (root / match.group(1).strip()).exists() else "not met"
    return "judge"


def wake_verdict(folder: Path) -> tuple[str, list[tuple[str, str]]]:
    results = [(c, check_condition(c)) for c in wake_conditions(folder)]
    if any(r == "not met" for _, r in results):
        return "waiting", results
    if any(r == "judge" for _, r in results):
        return "judge conditions", results
    return "ready: ask the user", results


def dormant(args: list[str]) -> int:
    if len(args) < 2:
        print('usage: sessions.py dormant <session> "<reason>" [--wake "<condition>"]...', file=sys.stderr)
        return 1
    folder = brain() / "sessions" / "active" / args[0].rstrip("/").split("/")[-1]
    if not folder.is_dir():
        print(f"no active session named {folder.name}", file=sys.stderr)
        return 1
    reason, conditions, rest = args[1], [], args[2:]
    while rest:
        if rest[0] == "--wake" and len(rest) > 1:
            conditions.append(rest[1].replace("\n", " "))
            rest = rest[2:]
        else:
            print(f"unexpected argument: {rest[0]}", file=sys.stderr)
            return 1
    previous = read_state(folder)
    lines = [f"# Wake record: {folder.name}", "", f"Parked {TODAY} from state {previous}.", "",
             "## Reason", "", reason, "", "## Wake conditions", ""]
    lines += [f"- {c}" for c in conditions] or ["- none"]
    lines += ["", "## History", "", f"- {TODAY}: parked from {previous}.", ""]
    (folder / "wake.md").write_text("\n".join(lines), encoding="utf-8")
    write_state(folder, DORMANT, f"parked {TODAY}")
    move(folder, brain() / "sessions" / "dormant" / folder.name)
    print(f"parked {folder.name} under sessions/dormant/ with {len(conditions)} wake conditions")
    return 0


def wake_check() -> int:
    folders = sorted((brain() / "sessions" / "dormant").glob("*/"))
    if not folders:
        print("no dormant sessions")
    for folder in folders:
        verdict, results = wake_verdict(folder)
        print(f"{folder.name}: {verdict}")
        for condition, result in results or [("no wake condition", "met")]:
            print(f"  [{result}] {condition}")
    return 0


def wake(args: list[str]) -> int:
    if not args:
        print("usage: sessions.py wake <session> [note]", file=sys.stderr)
        return 1
    folder = brain() / "sessions" / "dormant" / args[0].rstrip("/").split("/")[-1]
    if not folder.is_dir():
        print(f"no dormant session named {folder.name}", file=sys.stderr)
        return 1
    note = " ".join(args[1:])
    wake_file = folder / "wake.md"
    match = re.search(r"from state (\w+)", wake_file.read_text(encoding="utf-8")) if wake_file.exists() else None
    previous = match.group(1) if match and match.group(1) in OPEN_STATES else "PLANNING"
    if wake_file.exists():
        with wake_file.open("a", encoding="utf-8") as fh:
            fh.write(f"- {TODAY}: woken to {previous}" + (f": {note}" if note else "") + ".\n")
    write_state(folder, previous, f"woken {TODAY}")
    move(folder, brain() / "sessions" / "active" / folder.name)
    print(f"woke {folder.name} into state {previous}")
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
                "index": lambda: index(), "prune": lambda: prune(args), "dormant": lambda: dormant(args),
                "wake-check": lambda: wake_check(), "wake": lambda: wake(args)}
    if command not in handlers:
        print(__doc__, file=sys.stderr)
        return 1
    return handlers[command]()


if __name__ == "__main__":
    sys.exit(main())
