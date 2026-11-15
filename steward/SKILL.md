---
name: steward
description: "Govern every agent action that creates, copies, moves, backs up, or deletes files, documents, containers, volumes, images, environments, or caches, and keep work within the measured capacity of the machine. Use before any copy, move, rename, backup, removal, container or pod start, virtual environment or dependency install, scratch or temporary file, build, or cleanup; when a task risks leaving duplicates or backups behind; at session start to read the system profile; and before reporting completion to run the steward check."
compatibility: "Requires python3. Uses git, podman or docker, and gio or trash-put when present."
---

# Steward

Run every script with the skill directory as the base path, for example `python3 <skill-dir>/scripts/steward.py`.

## 1. Read the system profile

1. Read `~/.agents/system-profile.md`.
2. Run `bash scripts/system-profile.sh` first when the file is missing or older than 24 hours.
3. Read the capacity budgets in [decision rules](references/decision-rules.md#capacity-budgets).
4. Never copy the profile into a project file or record a hostname, user name, or home path in a project file.

## 2. Choose the recovery mechanism before any change

Use the first mechanism that applies:

1. Inside a Git worktree, rely on Git: commit, stash, or use the checkpoint branch required by `AGENTS.md` Section 4.
2. Outside version control, send removed user files to the system trash with the command for the platform in [decision rules](references/decision-rules.md#trash-commands).
3. Outside version control, for a system or configuration file edited in place, keep exactly one backup copy and record it with `python3 scripts/steward.py ledger add backup <path> "<removal condition>"`.
4. Never keep a second backup of the same target.
5. Delete each backup once its removal condition is met, then run `python3 scripts/steward.py ledger close <path>`.

## 3. Copy, move, rename, and remove

1. Move with `mv` or `git mv` when instructed to move. Never copy and leave the source.
2. Rename in place. Never duplicate a file under a new name.
3. Edit documents in place. Never create `-v2`, `-final`, `-old`, `copy`, `.bak`, `.orig`, or dated duplicates; Git holds the versions.
4. Copy only when the user requests a second copy or the output format differs.
5. Delete intermediate exports and conversions after the final output passes verification.
6. Remove when instructed to remove, under the confirmation rules of `AGENTS.md` Section 7.

## 4. Create throwaway resources

1. Reuse an existing environment, image, cache, or container before creating another.
2. Record each container, pod, volume, virtual environment, dependency cache, scratch directory, server, or build output made only for the current task with `python3 scripts/steward.py ledger add <kind> <target> "<removal condition>"`.
3. Start a throwaway container with `--rm --label agent.throwaway=true`.
4. Keep at most two throwaway containers at any time.
5. Label a container the user asked to keep with `--label agent.persistent=true`, and never use that label for throwaway work.
6. Put scratch files in the platform scratch or temporary directory, never in the project tree.
7. Never keep a throwaway resource as a backup, reference copy, or fallback.
8. Delete each resource when its removal condition is met, then close its ledger entry.

## 5. Obey the guard hooks

1. Treat a refusal from `steward.py pre` or `steward.py stop` as a binding instruction.
2. Correct the refused action as the refusal directs.
3. Never route around a refusal through another tool, interpreter, file operation, or command form.

## 6. Work within capacity

1. Run one heavy job at a time: build, test suite, container stack, virtual machine, model, or large download.
2. Run `bash scripts/system-profile.sh --brief` before a heavy job.
3. Pause heavy work and report to the user when a budget in [decision rules](references/decision-rules.md#capacity-budgets) is exceeded.
4. Stop servers, watchers, and processes you started once they are no longer needed.

## 7. Verify before completion

1. Run `python3 scripts/steward.py check` from the project root.
2. Resolve every finding by deleting the leftover.
3. Keep a finding only with the user's explicit approval, and record it with `python3 scripts/steward.py ledger close <target> --kept "<approval>"`.
4. Report what you created, what you deleted, and anything kept with approval.

Inspect [examples](examples/good-vs-bad-stewardship.md) for contrasting actions.

## 8. Pre-completion checklist

- [ ] System profile read and capacity budgets respected.
- [ ] No backup, duplicate, or dated copy left inside a Git worktree.
- [ ] Every backup outside version control recorded, then deleted or kept with approval.
- [ ] Every throwaway resource deleted and its ledger entry closed.
- [ ] `steward.py check` reports no findings.
- [ ] Final report lists created, deleted, and approved-kept items.
