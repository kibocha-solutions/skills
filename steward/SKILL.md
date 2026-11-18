---
name: steward
description: "Govern every agent action that creates, copies, moves, backs up, or deletes files, documents, containers, volumes, images, environments, or caches, persist and enforce per-repository approval modes (ask, true, false), and keep work within the measured capacity of the machine. Use before any copy, move, rename, backup, removal, container or pod start, virtual environment or dependency install, scratch or temporary file, screenshot or verification evidence, build, commit scope decision, or cleanup; when reading or updating repository approval modes; when a task risks leaving duplicates or backups behind; at session start to read the system profile and the device record; before installing or first using a shared agent tool such as modern-web-guidance or impeccable; when recording a lasting device default; and before reporting completion to run the steward check."
compatibility: "Requires python3. Uses git, podman or docker, and gio or trash-put when present."
---

# Steward

Run every script with the skill directory as the base path, for example `python3 <skill-dir>/scripts/steward.py`.

## 1. Read the system profile, device record, and approval mode

1. Read `~/.agents/system-profile.md`.
2. Run `bash scripts/system-profile.sh` first when the file is missing or older than 24 hours.
3. Read the capacity budgets in [decision rules](references/decision-rules.md#capacity-budgets).
4. Read `~/.agents/device.md`. Run `python3 scripts/steward.py device` first when the file is missing or its Facts section is older than 30 days.
5. Apply every entry under Defaults in `~/.agents/device.md` unless the user or the project instructions state otherwise.
6. Record a lasting user choice about tools or device use under Defaults, one table row per choice.
7. Never copy the profile or the device record into a project file or record a hostname, user name, or home path in a project file.
8. Read the repository approval mode with `python3 scripts/steward.py approval` (default `ask`). Read [approval modes](references/decision-rules.md#approval-modes).
9. Record an explicit user approval directive immediately with `python3 scripts/steward.py approval set <ask|true|false> "<note>"` and obey it:
   - `true`: auto-act within the repository; include all repository changes, cleanup, and leftover remediation even when not created by this agent, without asking the user.
   - `ask`: auto-act on in-scope work and agent-created throwaway resources; ask the user first before deleting, committing, or absorbing pre-existing or out-of-scope repository items.
   - `false`: request explicit user approval before every state-changing action, deletion, commit, or cleanup.

## 2. Install shared tools

1. Run `python3 scripts/steward.py tool ensure <name>` before the first use of a registered tool in a session. Read the [tool registry](references/decision-rules.md#tool-registry).
2. Let the command install the latest stable release when the tool is missing and refresh it when its record is 30 days old.
3. Never pin a registered tool to a fixed version or install a second copy of it per project.
4. Stop and report the exact error when the command exits 1.

## 3. Choose the recovery mechanism before any change

Use the first mechanism that applies:

1. Inside a Git worktree, rely on Git: commit, stash, or use the checkpoint branch required by `AGENTS.md` Section 4.
2. Outside version control, send removed user files to the system trash with the command for the platform in [decision rules](references/decision-rules.md#trash-commands).
3. Outside version control, for a system or configuration file edited in place, keep exactly one backup copy and record it with `python3 scripts/steward.py ledger add backup <path> "<removal condition>"`.
4. Never keep a second backup of the same target.
5. Delete each backup once its removal condition is met, then run `python3 scripts/steward.py ledger close <path>`.

## 4. Copy, move, rename, and remove

1. Move with `mv` or `git mv` when instructed to move. Never copy and leave the source.
2. Rename in place. Never duplicate a file under a new name.
3. Edit documents in place. Never create `-v2`, `-final`, `-old`, `copy`, `.bak`, `.orig`, or dated duplicates; Git holds the versions.
4. Copy only when the user requests a second copy or the output format differs.
5. Delete intermediate exports and conversions after the final output passes verification.
6. Remove when instructed to remove, under the confirmation rules of `AGENTS.md` Section 7.

## 5. Create throwaway resources

1. Reuse an existing environment, image, cache, or container before creating another.
2. Record each container, pod, volume, virtual environment, dependency cache, scratch directory, server, or build output made only for the current task with `python3 scripts/steward.py ledger add <kind> <target> "<removal condition>"`.
3. Start a throwaway container with `--rm --label agent.throwaway=true`.
4. Keep at most two throwaway containers at any time.
5. Label a container the user asked to keep with `--label agent.persistent=true`, and never use that label for throwaway work.
6. Never keep a throwaway resource as a backup, reference copy, or fallback.
7. Delete each resource when its removal condition is met, then close its ledger entry.

## 6. Place working files outside the project

Read [the agent store](references/decision-rules.md#agent-store) before creating evidence, an environment, or scratch files.

1. Save screenshots, renders, logs, traces, and exports made to verify work under `python3 scripts/steward.py store path evidence <project>/<maestro-session>`. Never save them in the project or its `.agents/` directory.
2. Cite evidence in a walkthrough by its `~/.agents/evidence/...` path.
3. Create Python environments and other toolchain environments under `python3 scripts/steward.py store path env <project>-<purpose>`, unless the project's recipe requires an in-project environment.
4. Reuse an existing store environment for the same project and lock file before creating another.
5. Put scratch files under `python3 scripts/steward.py store path scratch <task>`, and delete them when the task ends.

## 7. Obey the guard hooks

1. Treat a refusal from `steward.py pre` or `steward.py stop` as a binding instruction.
2. Let `steward.py stop` auto-clean permitted leftovers for the active `approval_mode`; resolve any remaining findings according to `approval_mode` instead of ignoring them or escalating in-scope work.
3. Correct the refused action as the refusal directs.
4. Never route around a refusal through another tool, interpreter, file operation, or command form.

## 8. Work within capacity

1. Run one heavy job at a time: build, test suite, container stack, virtual machine, model, or large download.
2. Run `bash scripts/system-profile.sh --brief` before a heavy job.
3. Pause heavy work and report to the user when a budget in [decision rules](references/decision-rules.md#capacity-budgets) is exceeded.
4. Stop servers, watchers, and processes you started once they are no longer needed.

## 9. Verify before completion

1. Run `python3 scripts/steward.py check` from the project root (or `python3 scripts/steward.py check --fix` when `approval_mode` is `true` or in-scope auto-remediation is authorized).
2. Resolve every remaining finding by deleting the leftover (after user approval when `approval_mode` is `false` or when out-of-scope in `ask` mode).
3. Keep a finding only with the user's explicit approval, and record it with `python3 scripts/steward.py ledger close <target> --kept "<approval>"`.
4. Report what you created, what you deleted, and anything kept with approval.

Inspect [examples](examples/good-vs-bad-stewardship.md) for contrasting actions.

## 10. Pre-completion checklist

- [ ] System profile, device record, and repository `approval_mode` (`ask`, `true`, `false`) read and obeyed.
- [ ] Every registered tool used was ensured through `steward.py tool ensure`.
- [ ] No backup, duplicate, or dated copy left inside a Git worktree.
- [ ] Every backup outside version control recorded, then deleted or kept with approval.
- [ ] Every throwaway resource deleted and its ledger entry closed.
- [ ] Evidence, environments, and scratch files kept in the agent store, never in the project or `.agents/`.
- [ ] `steward.py check` reports no findings.
- [ ] Final report lists created, deleted, and approved-kept items.
