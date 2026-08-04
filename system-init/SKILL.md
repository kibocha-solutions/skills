---
name: system-init
description: >
  Verifies and maintains a workstation's privileged-command scope (sudoers
  grant on the operating account), workspace storage partition, and
  standard development toolchain (Java, Kotlin, Python, Docker, Node) at
  current LTS. One unified verification-and-maintenance package, run end to
  end via its checklist. Use whenever setting up a workstation's sudoers
  scope for the first time, or whenever touching any of what this skill
  governs: sudoers/permission scope, workspace partitions, or toolchain
  state.
---

# System Init

## Goal

Take a workstation from whatever state it's actually in — nothing set up,
partially set up, or fully set up — to a fully verified, safely-scoped
operating environment: a sudoers grant that's exactly as wide as intended
and no wider, a workspace storage partition, and the standard dev toolchain
at current LTS. This is the single source of truth behind `AGENTS.md`'s
"Privileged Command Discipline" section — that stays short and usable on
its own, this is the full procedure behind it.

Run as one pass, not as separate unrelated steps.

## How This Works

Every phase in the checklist is independently in one of three states.
Diagnose per item, not per machine — a workstation is rarely uniformly "new"
or "done":

- **From scratch** — the phase's target doesn't exist yet. Follow the full
  setup procedure in the relevant reference.
- **Partially available** — some of it works. Identify exactly what's
  missing via the checklist item and close only that specific gap — do not
  redo pieces that already work.
- **Mostly available** — everything looks present. Run the checklist item
  to confirm rather than assuming it's still correct; state can drift
  (a sudoers file edited by hand, a mount unplugged, a package upgraded
  past LTS).

## Reference Routing

- `references/checklist.md` — the sequential, runnable checklist that is
  the operational spine of this skill. Start here for an actual pass;
  everything else is remediation detail this points into.
- `references/permissions.md` — for sudoers: how to set up a scoped grant
  from scratch, and the full command-level behavioral boundaries (what
  never to do even when technically permitted).
- `references/storage-and-partitions.md` — for finding, identifying, and
  mounting a workspace storage partition safely, and the hard rules around
  never formatting or partitioning autonomously.
- `references/toolchain.md` — for detecting the standard dev stack (Java,
  Kotlin, Python, Docker, Node), checking it against current LTS/stable,
  and the ask-before-resolving rule for anything missing or outdated.

## Checklist

The actual run is `references/checklist.md`: four phases in order
(sudoers/permissions, storage, toolchain, completion report). Each item
states the command to run, the expected result, where to go for remediation
if it fails, and an instruction to re-run that exact check after fixing
anything — before moving to the next item. The pass isn't done until every
item is confirmed; a completion report that omits an unresolved item is
wrong, not just incomplete.

## Hard Rules

- Never claim success on a phase without actually running its check command
  and seeing the expected result — no assuming.
- Never use a dangerous invocation form of a permitted command (config
  overrides, pager-shelling subcommands, untrusted package sideloading) —
  see `permissions.md` for the specific list.
- Never format, partition, or wipe a block device without the live user
  naming the exact target and confirming in that session — no exception for
  a confident-looking heuristic.
- An unmounted, unlabeled, or system-reserved-flagged partition is not
  evidence it's available — default to off-limits.
- Never attempt a command outside the granted sudoers scope, and never
  chain through an allowed shell/interpreter to reach the same effect.
- An install (package or toolchain) proceeds without asking only when the
  user explicitly requested that specific thing in its own dedicated
  message, it's clearly relevant to the project, and nothing about it looks
  compromised — otherwise, ask first.
- A permission-denied result is a real boundary: stop, report exactly what
  was attempted and why it was blocked, don't retry through another path.
