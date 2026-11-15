#!/usr/bin/env python3
"""Steward guard, completion check, and ledger.

Usage:
  steward.py pre                      Pre-tool hook; reads hook JSON on stdin.
  steward.py stop                     Session-end hook; reads hook JSON on stdin.
  steward.py check                    Completion check for the current directory.
  steward.py ledger add <kind> <target> <removal condition>
  steward.py ledger close <target> [--kept <approval>]
  steward.py ledger list [--all]
  steward.py store path <evidence|env|scratch> <name>   Create and print a store path.
  steward.py store list                                  List store entries with ages.
  steward.py store prune [--apply]                       Remove expired entries (dry run by default).

Exit codes: 0 allowed or clean; 2 refused (reason on stderr);
1 findings in check mode or usage error.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

THROWAWAY_LABELS = ("agent.throwaway=true", "talentsphere.throwaway=true")
PERSISTENT_LABEL = "agent.persistent=true"
MAX_THROWAWAY = 2
AGENTS_HOME = Path.home() / ".agents"
LEDGER = AGENTS_HOME / "steward" / "ledger.tsv"
STORE_KINDS = {"evidence": 90, "env": 30, "scratch": 2}  # retention in days since last use
STORE_DIRS = {"evidence": "evidence", "env": "envs", "scratch": "scratch"}
EVIDENCE_EXT = re.compile(
    r"\.(png|jpe?g|webp|gif|bmp|mp4|webm|mov|pdf|zip|tar|gz|zst|xz|7z|har|trace|log)$", re.I
)
LEDGER_FIELDS = ("created", "root", "kind", "target", "condition", "status", "note")
BACKUP_NAME = re.compile(
    r"(\.(bak|backup|old|orig|save)|~|[-_ ]copy|[-_ .](19|20)\d{6}([-_T]?\d{4,6})?)$", re.I
)
BACKUP_STEM = re.compile(r"(^copy of .+| copy( \d+)?| \(copy\))$", re.I)
WRAPPERS = {"sudo", "env", "nice", "nohup", "command", "time", "doas"}
SEPARATORS = {";", "&&", "||", "|", "&", "\n", "(", ")"}


def run(args: list[str], cwd: str | None = None) -> str:
    try:
        out = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=20)
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def engine() -> str | None:
    for name in ("podman", "docker"):
        if shutil.which(name):
            return name
    return None


def is_backup_name(path: str) -> bool:
    name = os.path.basename(path.rstrip("/"))
    stem = name.rsplit(".", 1)[0] if "." in name[1:] else name
    return bool(BACKUP_NAME.search(name) or BACKUP_STEM.search(stem))


def git_root(directory: str) -> str | None:
    probe = Path(directory)
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    root = run(["git", "rev-parse", "--show-toplevel"], cwd=str(probe)).strip()
    return root or None


def project_root(cwd: str) -> str:
    return git_root(cwd) or os.path.abspath(cwd)


def segments(command: str) -> list[list[str]]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        tokens = command.split()
    result, current = [], []
    for token in tokens:
        if token in SEPARATORS or set(token) <= set(";&|()"):
            if current:
                result.append(current)
            current = []
        else:
            current.append(token)
    if current:
        result.append(current)
    return result


def strip_prefix(tokens: list[str]) -> list[str]:
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", token):
            index += 1
        elif os.path.basename(token) in WRAPPERS:
            index += 1
            while index < len(tokens) and tokens[index].startswith("-"):
                index += 1
        elif os.path.basename(token) == "timeout":
            index += 1
            while index < len(tokens) and tokens[index].startswith("-"):
                index += 1
            index += 1
        else:
            break
    return tokens[index:]


def throwaway_ids(status_filters: tuple[str, ...] = ()) -> set[str]:
    eng = engine()
    if not eng:
        return set()
    ids: set[str] = set()
    for label in THROWAWAY_LABELS:
        args = [eng, "ps", "-a", "-q", "--filter", f"label={label}"]
        for status in status_filters:
            args += ["--filter", f"status={status}"]
        ids.update(lines(run(args)))
    return ids


def labels_of(tokens: list[str]) -> list[str]:
    found = []
    for index, token in enumerate(tokens):
        if token in ("--label", "-l") and index + 1 < len(tokens):
            found.append(tokens[index + 1])
        elif token.startswith("--label="):
            found.append(token.split("=", 1)[1])
    return found


def check_container(tokens: list[str]) -> str | None:
    rest = [t for t in tokens[1:] if not t.startswith("-")]
    if not rest:
        return None
    sub = rest[1] if rest[0] == "container" and len(rest) > 1 else rest[0]
    if sub not in ("run", "create"):
        return None
    labels = labels_of(tokens)
    if PERSISTENT_LABEL in labels:
        return None
    if "--rm" not in tokens and "--rm=true" not in tokens:
        return ("Steward: start a throwaway container with --rm so the engine deletes it and its "
                "anonymous volumes. Add --rm --label agent.throwaway=true, or --label "
                "agent.persistent=true only for a container the user asked to keep.")
    if not any(label in THROWAWAY_LABELS for label in labels):
        return "Steward: label the throwaway container with --label agent.throwaway=true, then retry."
    count = len(throwaway_ids())
    if count >= MAX_THROWAWAY:
        return (f"Steward: {count} throwaway containers already exist and the limit is "
                f"{MAX_THROWAWAY}. Remove one first: {engine()} ps -a --filter "
                "label=agent.throwaway=true, then rm -f <id>.")
    return None


def check_copy(tokens: list[str], cwd: str) -> str | None:
    operands, skip = [], False
    for token in tokens[1:]:
        if skip:
            skip = False
            continue
        if token in ("-t", "--target-directory", "-S", "--suffix", "-e", "--rsh", "--exclude"):
            skip = True
            continue
        if token.startswith("-"):
            continue
        operands.append(token)
    if len(operands) < 2:
        return None
    destination = os.path.join(cwd, os.path.expanduser(operands[-1]))
    if not is_backup_name(destination):
        return None
    root = git_root(os.path.dirname(destination) or cwd)
    if not root:
        return None
    return (f"Steward: '{operands[-1]}' is a backup copy inside a Git worktree. Git is the backup: "
            "commit, stash, or use the checkpoint branch, and edit or move the original in place.")


def host_of(payload: dict) -> str:
    if "toolCall" in payload or "conversationId" in payload or "fullyIdle" in payload:
        return "antigravity"
    if "toolName" in payload or "stopReason" in payload or "sessionId" in payload:
        return "copilot"
    return "standard"


def as_dict(value: object) -> dict:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return {"command": value}
    return value if isinstance(value, dict) else {}


def command_and_cwd(payload: dict, host: str) -> tuple[str, str]:
    if host == "antigravity":
        call = payload.get("toolCall") or {}
        args = as_dict(call.get("args"))
        if call.get("name") not in (None, "run_command"):
            return "", ""
        workspaces = payload.get("workspacePaths") or [os.getcwd()]
        return args.get("CommandLine") or "", args.get("Cwd") or workspaces[0]
    if host == "copilot" and "toolName" in payload:
        if str(payload.get("toolName")).lower() not in ("bash", "shell"):
            return "", ""
        args = as_dict(payload.get("toolArgs"))
        return args.get("command") or "", payload.get("cwd") or os.getcwd()
    args = as_dict(payload.get("tool_input") or payload.get("arguments"))
    return args.get("command") or args.get("cmd") or "", payload.get("cwd") or os.getcwd()


def refuse(host: str, reason: str) -> int:
    if host == "antigravity":
        print(json.dumps({"decision": "deny", "reason": reason}))
        return 0
    if host == "copilot":
        print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": reason}))
    print(reason, file=sys.stderr)
    return 2


def pre(payload: dict) -> int:
    host = host_of(payload)
    command, cwd = command_and_cwd(payload, host)
    if not command:
        return 0
    for raw in segments(command):
        tokens = strip_prefix(raw)
        if not tokens:
            continue
        program = os.path.basename(tokens[0])
        reason = None
        if program in ("podman", "docker"):
            reason = check_container(tokens)
        elif program in ("cp", "rsync", "mv"):
            reason = check_copy(tokens, cwd)
        if reason:
            return refuse(host, reason)
    return 0


def read_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == len(LEDGER_FIELDS):
            rows.append(dict(zip(LEDGER_FIELDS, parts, strict=True)))
    return rows


def write_ledger(rows: list[dict]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    text = "".join("\t".join(row[f] for f in LEDGER_FIELDS) + "\n" for row in rows)
    LEDGER.write_text(text, encoding="utf-8")


def target_exists(row: dict) -> bool:
    kind, target = row["kind"], row["target"]
    eng = engine()
    if kind in ("container", "volume", "image") and eng:
        sub = {"container": "container", "volume": "volume", "image": "image"}[kind]
        return subprocess.run([eng, sub, "exists", target], capture_output=True).returncode == 0
    if kind == "server":
        return True
    path = target if os.path.isabs(target) else os.path.join(row["root"], target)
    return os.path.lexists(path)


def findings(cwd: str) -> list[str]:
    found: list[str] = []
    eng = engine()
    if eng:
        stopped = throwaway_ids(("exited", "created"))
        if stopped:
            found.append(f"{len(stopped)} stopped throwaway containers: {eng} rm -f {' '.join(sorted(stopped))}")
        volumes = [v for v in lines(run([eng, "volume", "ls", "-q", "--filter", "dangling=true"]))
                   if re.fullmatch(r"[0-9a-f]{64}", v)]
        if volumes:
            found.append(f"{len(volumes)} unused unnamed volumes: {eng} volume ls -q --filter dangling=true "
                         f"| grep -E '^[0-9a-f]{{64}}$' | xargs -r {eng} volume rm")
        building = run(["pgrep", "-f", r"(podman|buildah) (build|bud)( |$)"]).strip()
        if eng == "podman" and not building:
            external = set(lines(run([eng, "ps", "-a", "--external", "-q"])))
            regular = set(lines(run([eng, "ps", "-a", "-q"])))
            abandoned = sorted(external - regular)
            if abandoned:
                found.append(f"{len(abandoned)} abandoned build containers: podman rm -f {' '.join(abandoned)}")
    root = git_root(cwd)
    if root:
        untracked = run(["git", "ls-files", "--others", "--exclude-standard"], cwd=root)
        backups = [p for p in lines(untracked) if is_backup_name(p)]
        if backups:
            found.append(f"{len(backups)} untracked backup copies in the worktree: {', '.join(backups[:10])}")
        evidence = [p for p in lines(untracked)
                    if p.startswith(".agents/") and EVIDENCE_EXT.search(p)]
        if evidence:
            found.append(f"{len(evidence)} evidence files inside .agents/; move them to "
                         f"'steward.py store path evidence <project>/<session>': {', '.join(evidence[:10])}")
    project = project_root(cwd)
    open_rows = [r for r in read_ledger() if r["status"] == "open" and r["root"] == project and target_exists(r)]
    for row in open_rows:
        found.append(f"open ledger entry {row['kind']} {row['target']} (remove when: {row['condition']})")
    return found


def stop(payload: dict) -> int:
    host = host_of(payload)
    workspaces = payload.get("workspacePaths") or []
    cwd = payload.get("cwd") or (workspaces[0] if workspaces else os.getcwd())
    found = findings(cwd)
    if not found:
        return 0
    message = ("Steward: leftovers remain. Delete them before finishing, or keep one only with the "
               "user's explicit approval recorded through 'steward.py ledger close <target> --kept "
               "<approval>'. Report what you deleted.\n- " + "\n- ".join(found))
    if host == "antigravity":
        marker = AGENTS_HOME / "steward" / "stop-continued" / re.sub(r"[^A-Za-z0-9_-]", "_", str(payload.get("conversationId") or "default"))
        if marker.exists() and datetime.datetime.now().timestamp() - marker.stat().st_mtime < 600:
            marker.unlink()
            return 0
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
        print(json.dumps({"decision": "continue", "reason": message}))
        return 0
    if payload.get("stop_hook_active"):
        if host == "standard":
            print(json.dumps({"systemMessage": message}))
        return 0
    if host == "copilot":
        print(json.dumps({"decision": "block", "reason": message}))
        return 0
    print(message, file=sys.stderr)
    return 2


def check() -> int:
    found = findings(os.getcwd())
    if not found:
        print("steward check: clean")
        return 0
    print("steward check: findings\n- " + "\n- ".join(found))
    return 1


def ledger(args: list[str]) -> int:
    if not args:
        print(__doc__, file=sys.stderr)
        return 1
    action, rest = args[0], args[1:]
    root = project_root(os.getcwd())
    rows = read_ledger()
    if action == "add" and len(rest) == 3:
        kind, target, condition = rest
        clean = [x.replace("\t", " ").replace("\n", " ") for x in (kind, target, condition)]
        rows.append(dict(zip(LEDGER_FIELDS, (
            datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            root, clean[0], clean[1], clean[2], "open", ""), strict=True)))
        write_ledger(rows)
        print(f"recorded {clean[0]} {clean[1]}")
        return 0
    if action == "close" and rest:
        target, note, status = rest[0], "", "closed"
        if len(rest) == 3 and rest[1] == "--kept":
            note, status = rest[2].replace("\t", " ").replace("\n", " "), "kept"
        matched = 0
        candidates = [r for r in rows if r["status"] == "open" and r["target"] == target]
        scoped = [r for r in candidates if r["root"] == root]
        for row in scoped or candidates:
            row["status"], row["note"] = status, note
            matched += 1
        write_ledger(rows)
        print(f"{status} {matched} entries for {target}")
        return 0 if matched else 1
    if action == "list":
        show_all = "--all" in rest
        for row in rows:
            if row["status"] == "open" and (show_all or row["root"] == root):
                print("\t".join(row[f] for f in ("created", "kind", "target", "condition")))
        return 0
    print(__doc__, file=sys.stderr)
    return 1


def store_root(kind: str) -> Path:
    return AGENTS_HOME / STORE_DIRS[kind]


def last_used(path: Path) -> float:
    marker = path / ".last-used"
    if marker.exists():
        return marker.stat().st_mtime
    newest = path.stat().st_mtime
    for child in path.rglob("*"):
        try:
            newest = max(newest, child.lstat().st_mtime)
        except OSError:
            pass
    return newest


def store_entries(kind: str) -> list[Path]:
    root = store_root(kind)
    if not root.is_dir():
        return []
    depth = 2 if kind == "evidence" else 1
    entries = [p for p in root.glob("/".join(["*"] * depth)) if p.is_dir()]
    return sorted(entries)


def store(args: list[str]) -> int:
    if not args:
        print(__doc__, file=sys.stderr)
        return 1
    action, rest = args[0], args[1:]
    if action == "path" and len(rest) == 2 and rest[0] in STORE_KINDS:
        kind, name = rest
        if ".." in Path(name).parts or name.startswith("/"):
            print("store name must be relative and must not contain '..'", file=sys.stderr)
            return 1
        path = store_root(kind) / name
        path.mkdir(parents=True, exist_ok=True)
        (path / ".last-used").touch()
        print(path)
        return 0
    now = datetime.datetime.now().timestamp()
    if action == "list":
        for kind in STORE_KINDS:
            for entry in store_entries(kind):
                age = (now - last_used(entry)) / 86400
                print(f"{kind}\t{age:5.0f} days\t{entry}")
        return 0
    if action == "prune":
        apply = "--apply" in rest
        for kind, days in STORE_KINDS.items():
            for entry in store_entries(kind):
                age = (now - last_used(entry)) / 86400
                if age > days:
                    print(f"{'removed' if apply else 'would remove'} {kind} {entry} ({age:.0f} days unused)")
                    if apply:
                        shutil.rmtree(entry, ignore_errors=True)
        return 0
    print(__doc__, file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    mode = sys.argv[1]
    if mode in ("pre", "stop"):
        raw = sys.stdin.read() if not sys.stdin.isatty() else ""
        try:
            payload = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            payload = {}
        return pre(payload) if mode == "pre" else stop(payload)
    if mode == "check":
        return check()
    if mode == "ledger":
        return ledger(sys.argv[2:])
    if mode == "store":
        return store(sys.argv[2:])
    print(__doc__, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
