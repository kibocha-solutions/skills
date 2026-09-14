#!/usr/bin/env python3
"""Run a command while one or more local servers are available."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import signal
import socket
import subprocess
import sys
import time


def port_is_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def wait_for_port(port: int, process: subprocess.Popen[bytes], timeout: int) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                f"server process exited with status {process.returncode} before port {port} opened"
            )
        if port_is_open(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open within {timeout} seconds")


def stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    if os.name == "posix":
        os.killpg(process.pid, signal.SIGTERM)
    else:
        process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.wait()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start local servers, wait for their ports, run a command, and stop the servers."
    )
    parser.add_argument(
        "--server",
        action="append",
        required=True,
        help="Server command as a quoted argument string; shell operators are not supported.",
    )
    parser.add_argument(
        "--port",
        action="append",
        required=True,
        type=int,
        help="Readiness port for the corresponding server.",
    )
    parser.add_argument(
        "--cwd",
        action="append",
        default=[],
        help="Working directory for the corresponding server; defaults to the current directory.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Readiness timeout in seconds for each server.",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run after --.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command

    if not command:
        raise SystemExit("a command is required after --")
    if len(args.server) != len(args.port):
        raise SystemExit("each --server requires one matching --port")
    if len(args.cwd) > len(args.server):
        raise SystemExit("--cwd cannot occur more often than --server")

    working_directories = args.cwd + ["."] * (len(args.server) - len(args.cwd))
    processes: list[subprocess.Popen[bytes]] = []

    try:
        for command_text, port, cwd_text in zip(
            args.server, args.port, working_directories, strict=True
        ):
            argv = shlex.split(command_text)
            if not argv:
                raise RuntimeError("server command is empty")

            cwd = Path(cwd_text).resolve()
            if not cwd.is_dir():
                raise RuntimeError(f"server working directory does not exist: {cwd}")
            if port_is_open(port):
                raise RuntimeError(f"port {port} is already in use")

            print(f"Starting server on port {port}: {shlex.join(argv)}")
            process = subprocess.Popen(
                argv,
                cwd=cwd,
                start_new_session=(os.name == "posix"),
            )
            processes.append(process)
            wait_for_port(port, process, args.timeout)
            print(f"Server ready on port {port}")

        return subprocess.run(command, check=False).returncode
    finally:
        for process in reversed(processes):
            stop_process(process)


if __name__ == "__main__":
    raise SystemExit(main())
