#!/usr/bin/env python3
"""Steward guard, completion check, approval policy, and ledger.

Usage:
  steward.py pre                                   Pre-tool hook; reads hook JSON on stdin.
  steward.py stop                                  Session-end hook; reads hook JSON on stdin.
  steward.py check [--fix]                         Completion check (with optional auto-remediation).
  steward.py approval [get]                        Print the approval mode (ask, true, false) for the project.
  steward.py approval set <ask|true|false> [note]  Set the persistent approval mode for the project.
  steward.py approval list                         List recorded project approval modes.
  steward.py ledger add <kind> <target> <removal condition>
  steward.py ledger close <target> [--kept <approval>]
  steward.py ledger list [--all]
  steward.py store path <evidence|env|scratch> <name>   Create and print a store path.
  steward.py store list                                  List store entries with ages.
  steward.py store prune [--apply]                       Remove expired entries (dry run by default).
  steward.py device                                      Rewrite the Facts section of ~/.agents/device.md.
  steward.py tool ensure <name>... [--update]            Install or refresh shared tools and record them.
  steward.py tool list                                   List registered tools and their records.

Exit codes: 0 allowed or clean; 2 refused (reason on stderr);
1 findings in check mode, a failed install, or usage error.
"""
from __future__ import annotations

import datetime
import json
import os
import platform
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
APPROVALS = AGENTS_HOME / "steward" / "approvals.tsv"
APPROVAL_MODES = ("ask", "true", "false")
APPROVAL_FIELDS = ("updated", "root", "mode", "note")
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
DEVICE = AGENTS_HOME / "device.md"
TOOL_REFRESH_DAYS = 30
TOOL_FIELDS = ("tool", "version", "source", "installed", "checked")
# Shared agent tools, installed once per device at the latest stable release.
TOOLS = {
    "modern-web-guidance": {"npm": "modern-web-guidance", "command": "modern-web-guidance"},
    "impeccable": {"npm": "impeccable", "command": "impeccable"},
}
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


def read_tsv(path: Path, fields: tuple[str, ...]) -> list[dict]:
    """Read a tab-delimited table into a list of field dictionaries."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == len(fields):
            rows.append(dict(zip(fields, parts, strict=True)))
    return rows


def write_tsv(path: Path, fields: tuple[str, ...], rows: list[dict]) -> None:
    """Write a list of field dictionaries to a tab-delimited file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join("\t".join(row[f] for f in fields) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def read_ledger() -> list[dict]:
    return read_tsv(LEDGER, LEDGER_FIELDS)


def write_ledger(rows: list[dict]) -> None:
    write_tsv(LEDGER, LEDGER_FIELDS, rows)


def read_approvals() -> list[dict]:
    return read_tsv(APPROVALS, APPROVAL_FIELDS)


def write_approvals(rows: list[dict]) -> None:
    write_tsv(APPROVALS, APPROVAL_FIELDS, rows)


def approval_json_path(root: str) -> Path:
    """Return the project-local approval policy path under .agents/brain/."""
    return Path(root) / ".agents" / "brain" / "approvals.json"


def get_approval_mode(cwd: str) -> tuple[str, str]:
    """Return (mode, note) from approvals.json, approvals.tsv, or default 'ask'."""
    root = project_root(cwd)
    local = approval_json_path(root)
    if local.is_file():
        try:
            data = json.loads(local.read_text(encoding="utf-8"))
            mode = str(data.get("approval_mode", "")).strip().lower()
            if mode in APPROVAL_MODES:
                return mode, str(data.get("note", "")).strip()
        except (OSError, json.JSONDecodeError, AttributeError):
            pass
    for row in reversed(read_approvals()):
        if row["root"] == root and row["mode"] in APPROVAL_MODES:
            return row["mode"], row["note"]
    return "ask", "default"


def set_approval_mode(cwd: str, mode: str, note: str = "") -> dict:
    """Persist repository approval mode to approvals.tsv and .agents/brain/approvals.json."""
    normalized = mode.strip().lower()
    if normalized not in APPROVAL_MODES:
        raise ValueError(f"invalid approval mode {mode!r}; expected one of {', '.join(APPROVAL_MODES)}")
    root = project_root(cwd)
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    clean_note = note.replace("\t", " ").replace("\n", " ").strip()
    rows = [r for r in read_approvals() if r["root"] != root]
    rows.append({"updated": stamp, "root": root, "mode": normalized, "note": clean_note})
    write_approvals(rows)
    record = {
        "schema_version": 1,
        "root": root,
        "approval_mode": normalized,
        "updated_at": stamp,
        "note": clean_note,
    }
    if (Path(root) / ".agents").is_dir():
        local = approval_json_path(root)
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


def approval(args: list[str]) -> int:
    """Handle 'steward.py approval [get|set|list]'."""
    action = args[0] if args else "get"
    rest = args[1:]
    if action == "get" and not rest:
        mode, note = get_approval_mode(os.getcwd())
        print(f"{mode}\t{note}" if note else mode)
        return 0
    if action == "set" and rest and rest[0].lower() in APPROVAL_MODES:
        record = set_approval_mode(os.getcwd(), rest[0], " ".join(rest[1:]))
        print(f"approval_mode={record['approval_mode']} ({record['root']})")
        return 0
    if action == "list" and not rest:
        for row in read_approvals():
            print("\t".join(row[f] for f in APPROVAL_FIELDS))
        return 0
    print(__doc__, file=sys.stderr)
    return 1


def remove_target(path: Path) -> bool:
    """Remove a leftover file or directory via system trash when available, else unlink/rmtree."""
    if not path.exists() and not path.is_symlink():
        return True
    for cmd in (["gio", "trash", str(path)], ["trash-put", str(path)], ["trash", str(path)]):
        if shutil.which(cmd[0]):
            try:
                if subprocess.run(cmd, capture_output=True, timeout=15).returncode == 0:
                    return True
            except (OSError, subprocess.SubprocessError):
                pass
    try:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
        return True
    except OSError:
        return False


def _clean_containers(eng: str, cleaned: list[str]) -> None:
    """Remove stopped throwaway containers, dangling unnamed volumes, and abandoned build containers."""
    stopped = throwaway_ids(("exited", "created"))
    if stopped:
        subprocess.run([eng, "rm", "-f", *sorted(stopped)], capture_output=True, timeout=30)
        cleaned.append(f"removed {len(stopped)} stopped throwaway container(s)")
    volumes = [v for v in lines(run([eng, "volume", "ls", "-q", "--filter", "dangling=true"]))
               if re.fullmatch(r"[0-9a-f]{64}", v)]
    if volumes:
        subprocess.run([eng, "volume", "rm", *volumes], capture_output=True, timeout=30)
        cleaned.append(f"removed {len(volumes)} unused unnamed volume(s)")
    building = run(["pgrep", "-f", r"(podman|buildah) (build|bud)( |$)"]).strip()
    if eng == "podman" and not building:
        external = set(lines(run([eng, "ps", "-a", "--external", "-q"])))
        regular = set(lines(run([eng, "ps", "-a", "-q"])))
        abandoned = sorted(external - regular)
        if abandoned:
            subprocess.run([eng, "rm", "-f", *abandoned], capture_output=True, timeout=30)
            cleaned.append(f"removed {len(abandoned)} abandoned build container(s)")


def auto_clean(cwd: str, mode: str, fix_all: bool = False) -> list[str]:
    """Auto-clean safe leftovers permitted by the project's approval mode or --fix."""
    if mode == "false" and not fix_all:
        return []
    cleaned: list[str] = []
    project = project_root(cwd)
    rows = read_ledger()
    ledger_changed = False

    for row in rows:
        if row["status"] == "open" and row["root"] == project and not target_exists(row):
            row["status"], row["note"] = "closed", "auto-closed: target removed"
            ledger_changed = True
            cleaned.append(f"closed stale ledger entry {row['kind']} {row['target']}")

    eng = engine()
    if eng and (mode in ("true", "ask") or fix_all):
        _clean_containers(eng, cleaned)

    if mode == "true" or fix_all:
        root = git_root(cwd)
        if root:
            untracked = lines(run(["git", "ls-files", "--others", "--exclude-standard"], cwd=root))
            for rel in untracked:
                if is_backup_name(rel) and remove_target(Path(root) / rel):
                    cleaned.append(f"removed backup copy {rel}")
                elif rel.startswith(".agents/") and EVIDENCE_EXT.search(rel):
                    dest_root = store_root("evidence") / Path(root).name / "steward-auto"
                    dest = dest_root / Path(rel).relative_to(".agents")
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(Path(root) / rel), str(dest))
                    (dest_root / ".last-used").touch()
                    cleaned.append(f"moved evidence {rel} to store")
        for row in rows:
            if row["status"] != "open" or row["root"] != project:
                continue
            if row["kind"] == "container" and eng:
                subprocess.run([eng, "rm", "-f", row["target"]], capture_output=True, timeout=30)
                if not target_exists(row):
                    row["status"], row["note"] = "closed", "auto-cleaned"
                    ledger_changed = True
                    cleaned.append(f"removed container {row['target']} and closed ledger entry")
            elif row["kind"] in ("backup", "scratch"):
                target_path = Path(row["target"]) if os.path.isabs(row["target"]) else Path(row["root"]) / row["target"]
                if remove_target(target_path):
                    row["status"], row["note"] = "closed", "auto-cleaned"
                    ledger_changed = True
                    cleaned.append(f"removed {row['kind']} {row['target']} and closed ledger entry")

    if ledger_changed:
        write_ledger(rows)
    return cleaned


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


def allow_stop(host: str) -> int:
    """Emit valid empty JSON for hosts expecting structured stop responses."""
    if host in ("antigravity", "copilot"):
        print(json.dumps({}))
    return 0


def stop(payload: dict) -> int:
    """Run end-of-turn steward checks and auto-remediation per host and approval mode."""
    host = host_of(payload)
    workspaces = payload.get("workspacePaths") or []
    cwd = payload.get("cwd") or (workspaces[0] if workspaces else os.getcwd())
    marker = (
        AGENTS_HOME
        / "steward"
        / "stop-continued"
        / re.sub(r"[^A-Za-z0-9_-]", "_", str(payload.get("conversationId") or "default"))
    )

    if host == "antigravity":
        term = payload.get("terminationReason")
        if payload.get("continuationActive") or (term and term != "NO_TOOL_CALL") or payload.get("fullyIdle") is False:
            if marker.exists():
                marker.unlink()
            return allow_stop(host)
        if marker.exists() and datetime.datetime.now().timestamp() - marker.stat().st_mtime < 600:
            marker.unlink()
            return allow_stop(host)
    elif payload.get("stop_hook_active"):
        return allow_stop(host)

    mode, _ = get_approval_mode(cwd)
    auto_clean(cwd, mode)
    found = findings(cwd)
    if not found:
        if host == "antigravity" and marker.exists():
            marker.unlink()
        return allow_stop(host)

    action_hint = (
        "Ask the user for approval before removing or keeping any item."
        if mode == "false"
        else "Run 'steward.py check --fix' for in-scope leftovers or 'steward.py ledger close <target> "
        "--kept \"<approval>\"'; ask the user only for pre-existing or out-of-scope items."
    )
    items = "\n".join(f"- {item}" for item in found)
    message = f"Steward (approval_mode={mode}): {len(found)} finding(s) remain.\n{items}\n{action_hint}"

    if host == "antigravity":
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
        print(json.dumps({"decision": "continue", "reason": message}))
        return 0
    if host == "copilot":
        print(json.dumps({"decision": "block", "reason": message}))
        return 0
    print(message, file=sys.stderr)
    return 2


def check(args: list[str] | None = None) -> int:
    """Run completion check, auto-remediating when --fix or approval_mode=true."""
    fix_all = "--fix" in (args or [])
    cwd = os.getcwd()
    mode, _ = get_approval_mode(cwd)
    if fix_all or mode == "true":
        for item in auto_clean(cwd, mode, fix_all=fix_all):
            print(f"steward auto-clean: {item}")
    found = findings(cwd)
    if not found:
        print("steward check: clean")
        return 0
    print(f"steward check (approval_mode={mode}): findings\n- " + "\n- ".join(found))
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


def today() -> str:
    return datetime.date.today().isoformat()


def first_line(text: str) -> str:
    return text.strip().splitlines()[0].strip() if text.strip() else ""


def device_facts() -> list[tuple[str, str]]:
    facts: list[tuple[str, str]] = []
    os_name = platform.system()
    release = Path("/etc/os-release")
    if release.exists():
        match = re.search(r'^PRETTY_NAME="?([^"\n]+)', release.read_text(encoding="utf-8"), re.M)
        os_name = match.group(1) if match else os_name
    elif shutil.which("sw_vers"):
        os_name = "macOS " + run(["sw_vers", "-productVersion"]).strip()
    facts.append(("Operating system", os_name))
    facts.append(("Kernel and architecture", f"{platform.release()} {platform.machine()}"))
    cpu = ""
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        match = re.search(r"^model name\s*:\s*(.+)$", cpuinfo.read_text(encoding="utf-8"), re.M)
        cpu = match.group(1).strip() if match else ""
    elif shutil.which("sysctl"):
        cpu = run(["sysctl", "-n", "machdep.cpu.brand_string"]).strip()
    facts.append(("Processor", f"{cpu or 'unknown'}, {os.cpu_count()} threads"))
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        info = meminfo.read_text(encoding="utf-8")
        for label, key in (("Memory", "MemTotal"), ("Swap", "SwapTotal")):
            match = re.search(rf"^{key}:\s+(\d+)", info, re.M)
            if match:
                facts.append((label, f"{int(match.group(1)) / 1048576:.1f} GiB"))
    if shutil.which("lspci"):
        gpus = [re.sub(r"^\S+\s+[^:]+:\s*", "", line) for line in lines(run(["lspci"]))
                if re.search(r"VGA|3D controller|Display controller", line)]
        if gpus:
            facts.append(("Graphics", "; ".join(gpus)))
    facts.append(("Home filesystem size", f"{shutil.disk_usage(Path.home()).total / 1073741824:.0f} GiB"))
    versions = (("Container engine", [engine() or "none", "--version"]),
                ("Node.js", ["node", "--version"]), ("npm", ["npm", "--version"]),
                ("Python", ["python3", "--version"]), ("Git", ["git", "--version"]))
    for label, args in versions:
        found = shutil.which(args[0]) if args[0] != "none" else None
        facts.append((label, first_line(run(args)) if found else "not installed"))
    hosts = [name for name, path in (("Claude Code", ".claude"), ("Codex", ".codex"),
                                     ("Gemini CLI", ".gemini/settings.json"),
                                     ("Antigravity", ".gemini/antigravity"), ("Copilot", ".copilot"))
             if (Path.home() / path).exists()]
    facts.append(("Agent hosts", ", ".join(hosts) or "none"))
    cache = Path.home() / ("Library/Caches/ms-playwright" if sys.platform == "darwin" else ".cache/ms-playwright")
    browsers = sorted(p.name for p in cache.glob("*-[0-9]*") if p.is_dir()) if cache.is_dir() else []
    facts.append(("Playwright browser cache", f"{cache} ({', '.join(browsers) or 'empty'})"))
    return facts


def read_device() -> tuple[list[dict], str]:
    """Return the tool rows and the preserved Defaults section text."""
    if not DEVICE.exists():
        return [], ""
    text = DEVICE.read_text(encoding="utf-8")
    rows = []
    tools = re.search(r"^## Tools\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    for line in (tools.group(1).splitlines() if tools else []):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == len(TOOL_FIELDS) and cells[0] not in ("Tool", "") and not set(cells[0]) <= set("-: "):
            rows.append(dict(zip(TOOL_FIELDS, cells, strict=True)))
    defaults = re.search(r"^## Defaults\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return rows, defaults.group(1).strip() if defaults else ""


def write_device(rows: list[dict], defaults: str) -> None:
    out = ["# Device record", "",
           "Stable facts about this device and the shared agent tools installed on it. "
           "`steward.py device` and `steward.py tool` rewrite the Facts and Tools sections. "
           "Agents add lasting choices under Defaults by hand. Live load, memory, and temperature "
           "are in system-profile.md.", "",
           "## Facts", "", f"Updated {today()}.", "", "| Fact | Value |", "| :--- | :--- |"]
    out += [f"| {k} | {v.replace('|', '/')} |" for k, v in device_facts()]
    out += ["", "## Tools", "", "| Tool | Version | Source | Installed | Checked |",
            "| :--- | :--- | :--- | :--- | :--- |"]
    out += ["| " + " | ".join(r[f] for f in TOOL_FIELDS) + " |" for r in sorted(rows, key=lambda r: r["tool"])]
    out += ["", "## Defaults", "", defaults or "No defaults recorded.", ""]
    DEVICE.parent.mkdir(parents=True, exist_ok=True)
    DEVICE.write_text("\n".join(out), encoding="utf-8")


def device(_args: list[str]) -> int:
    rows, defaults = read_device()
    write_device(rows, defaults)
    print(DEVICE)
    return 0


def npm_installed_version(package: str) -> str:
    data = run(["npm", "ls", "-g", "--depth=0", "--json", package])
    try:
        return json.loads(data or "{}").get("dependencies", {}).get(package, {}).get("version", "")
    except json.JSONDecodeError:
        return ""


def ensure_tool(name: str, rows: list[dict], force: bool) -> bool:
    spec = TOOLS[name]
    package = spec["npm"]
    if not shutil.which("npm"):
        print(f"{name}: npm is not installed; install Node.js through system-init, then retry", file=sys.stderr)
        return False
    row = next((r for r in rows if r["tool"] == name), None)
    installed = npm_installed_version(package) if shutil.which(spec["command"]) else ""
    stale = row is None or force or (
        datetime.date.today() - datetime.date.fromisoformat(row["checked"])).days >= TOOL_REFRESH_DAYS
    if installed and not stale:
        print(f"{name}: {installed} present, checked {row['checked']}")
        return True
    latest = first_line(run(["npm", "view", package, "version"]))
    if installed and latest and installed == latest:
        action = "current"
    else:
        result = subprocess.run(["npm", "install", "-g", f"{package}@latest"],
                                capture_output=True, text=True, timeout=900)
        if result.returncode != 0:
            print(f"{name}: install failed\n{result.stderr.strip()[-600:]}", file=sys.stderr)
            return False
        action = "updated" if installed else "installed"
        installed = npm_installed_version(package)
    if row is None:
        row = {"tool": name, "installed": today()}
        rows.append(row)
    elif action != "current":
        row["installed"] = today()
    row.update(version=installed or "unknown", source=f"npm -g {package}@latest", checked=today())
    print(f"{name}: {installed} {action}")
    return True


def tool(args: list[str]) -> int:
    if not args or args[0] not in ("ensure", "list"):
        print(__doc__, file=sys.stderr)
        return 1
    rows, defaults = read_device()
    if args[0] == "list":
        for name in TOOLS:
            row = next((r for r in rows if r["tool"] == name), None)
            print(f"{name}\t" + ("\t".join(row[f] for f in TOOL_FIELDS[1:]) if row else "not recorded"))
        return 0
    names = [a for a in args[1:] if not a.startswith("--")]
    unknown = [n for n in names if n not in TOOLS]
    if not names or unknown:
        print(f"registered tools: {', '.join(TOOLS)}" + (f"; unknown: {', '.join(unknown)}" if unknown else ""),
              file=sys.stderr)
        return 1
    ok = all([ensure_tool(n, rows, "--update" in args) for n in names])
    write_device(rows, defaults)
    return 0 if ok else 1


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
        return check(sys.argv[2:])
    if mode == "approval":
        return approval(sys.argv[2:])
    if mode == "ledger":
        return ledger(sys.argv[2:])
    if mode == "store":
        return store(sys.argv[2:])
    if mode == "device":
        return device(sys.argv[2:])
    if mode == "tool":
        return tool(sys.argv[2:])
    print(__doc__, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
