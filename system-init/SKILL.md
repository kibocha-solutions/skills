---
name: system-init
description: Audit and maintain workstation sudoers scope, workspace storage, partitions, mounts, tools, libraries, and the Java, Kotlin, Python, Docker, Node, Git, GitHub CLI, and GitLab CLI toolchain. Use for workstation setup, missing dependency installation, package-manager work, global or system installation, privileged-command scope, block devices, workspace mounts, or development tool versions.
---

# System Init

## 1. Establish scope

1. Identify the host, operating account, operating system, and requested outcome.
2. Identify whether the request covers permissions, storage, toolchain, or all three.
3. Separate read-only audit from requested changes.
4. List every privileged file, command, device, mount, package, and version that may change.
5. Do not infer authority for one category from authority for another.

## 2. Run the read-only audit

Read [the checklist](references/checklist.md).

1. Inspect the current sudoers grant.
2. Inspect block devices, filesystems, mounts, and persistent mount configuration.
3. Inspect installed tool versions and executable origins.
4. Compare current LTS and stable versions with official sources.
5. Record pass, gap, conflict, and unknown states.
6. Do not mutate the system during the audit.

## 3. Apply permission rules

Read [permissions](references/permissions.md).

1. Use only commands present in the live sudoers grant.
2. Use only the plain invocation required by the task.
3. Do not use config overrides, shell escapes, arbitrary package files, unsafe confinement flags, or interpreter chaining.
4. Use `sudoedit` only for exact files present in the live grant.
5. Do not use a privileged editor or interpreter.
6. Stop after a permission-denied or not-allowed result.
7. Do not seek another route to the same privileged effect.

## 4. Apply installation rules

Read [dependency installation](references/dependency-installation.md).

1. Apply the qualifying-installation gate in `AGENTS.md`.
2. Verify the exact package identity, publisher, source, version, and scope.
3. Install a qualifying dependency without requesting separate permission.
4. Stop when any integrity, identity, relevance, or safety gate fails.
5. Stop on a privilege denial and ask the user to run the exact command.
6. Verify and record the installed result before using it.

## 5. Apply storage rules

Read [storage and partitions](references/storage-and-partitions.md).

1. Treat every unidentified device or partition as off-limits.
2. Treat unmounted, unlabeled, reserved, boot, recovery, diagnostic, and foreign-system partitions as unavailable.
3. Preserve all existing data.
4. Do not format, partition, wipe, resize, or overwrite a block device unless the live user names the exact device and confirms the exact operation in the current session.
5. Re-inspect the exact device immediately before an authorized destructive operation.
6. Stop when device identity, ownership, or purpose is uncertain.
7. Use UUID-based persistent mounts.
8. Verify the mount and unprivileged workspace access after any authorized change.

## 6. Apply toolchain rules

Read [toolchain](references/toolchain.md).

1. Inspect Java, Kotlin, Python, Docker, Node, Git, GitHub CLI, and GitLab CLI separately.
2. Compare each version with its official current LTS or stable line.
3. Keep the operating system's managed Python intact.
4. Distinguish Docker group access from sudoers access.
5. Distinguish a stale version from a broken installation.
6. Apply the installation gate before changing any component.
7. Re-run version, path, build, and smoke checks after each authorized change.

## 7. Verify and report

1. Re-run every check affected by a change.
2. Confirm the exact sudoers commands and files available.
3. Confirm the exact device, filesystem, UUID, mount point, owner, and persistence rule.
4. Confirm every tool version and executable path.
5. List unresolved gaps explicitly.
6. Do not report full success while any required item is unverified.
7. Do not include passwords, private keys, tokens, internal URLs, or unrelated system data.
