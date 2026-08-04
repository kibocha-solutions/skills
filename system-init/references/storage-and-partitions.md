# Storage and Partitions

## Workspace Access Is Already Unprivileged — Not a `sudoers`/`EDITFILES` Concern

The operating account has full read/write/delete access to `/mnt/data`
directly — it owns the mount outright — not through `sudo`, not through
`sudoedit`, not through the `EDITFILES` sudoers alias. No privilege is
needed anywhere under `/mnt/data`; any file there can be read, written, or
removed the same way any normally-owned file can. `EDITFILES` exists for a
different, narrower problem entirely — specific files the account does
*not* otherwise own (e.g. under `/etc/`) — see `permissions.md`. Do not
route `/mnt/data` work through `sudoedit` or add `/mnt/data` paths to the
sudoers file; that would be both unnecessary and, since `EDITFILES`
requires exact individual file paths, unworkable for a whole directory
tree anyway.

For convenience, a home-directory symlink `~/data -> /mnt/data` lets the
workspace be referenced as `~/data` instead of the absolute path. Create it
if missing:

```bash
ln -sfn /mnt/data ~/data
```

## Read-Only Inspection First, Always

Before any storage decision, gather the actual current state — never assume
or classify from memory of a prior run:

```bash
lsblk -f
df -h
findmnt
cat /etc/fstab
```

**GParted is the preferred, primary tool for identifying candidate
partitions** — use it (or ask the user to open it and share what it shows)
whenever a partition's purpose is unclear from the command-line tools alone.
GParted shows filesystem type, label, partition-table flags, and mount
point together in one view, which command-line tools can miss or
misrepresent individually. This isn't a stylistic preference — a real case
on this project's own workstation showed why: `lsblk -f` reported an
unmounted, unlabeled partition (`nvme0n1p2`) as filesystem type `ext4`,
which reads like plausible free space. GParted showed the authoritative
truth: it carries the `msftres` flag — a Windows Microsoft Reserved
Partition, system metadata, not usable space, not a workspace candidate,
and not remotely close to "available." The filesystem-type guess was
misleading; the partition-table flag was decisive.

## The Hard Rule

Never run a formatting or partitioning operation against a block device —
`mkfs`, `parted`, `fdisk`, `wipefs`, `dd` targeting a device, or any
equivalent — autonomously. No exception for a confident-looking heuristic,
no matter how thorough the inspection was. The live user must explicitly
name the exact target device and confirm the action in that session, every
time, on every machine.

This rule exists specifically because classification can be wrong in ways
that look right — see the `nvme0n1p2` case above. Confidence is not
evidence.

## Classification Defaults

- An **unmounted** partition is not evidence it's available — it may simply
  not be in current use for an unrelated reason (a dual-boot OS not
  currently running, reserved system metadata, a drive intentionally kept
  offline).
- An **unlabeled** partition is not evidence it's available.
- A partition carrying a **system/reserved flag** — `msftres`, `boot`,
  `esp`, `diag`, `hidden`, or similar — is off-limits, full stop, regardless
  of mount state.
- A partition that **cannot be positively identified** is off-limits by
  default. Silence or uncertainty means "don't touch," never "probably
  fine."
- Partitions belonging to another OS's boot infrastructure (NTFS partitions
  on a dual-boot machine, EFI system partitions, MSR partitions, the
  currently-running Linux root) are always excluded, not just deprioritized.
- A partition with a clearly-named, deliberate purpose that isn't the
  workspace (e.g. a shared bridge/exchange partition between OSes) is
  excluded — it has an existing purpose, it is not spare capacity.

## Existing-Data Safety

If a candidate target already contains data — a `workspace/` directory, a
project directory, anything — preserve it unconditionally:

- Never delete.
- Never overwrite.
- Never reformat.
- Never recreate destructively.

If the target already matches the intended standard, the correct action is
to standardize the mount configuration only (see below), not to touch the
data.

## Mount Standard (When Setting Up From Scratch)

- UUID-based `/etc/fstab` entries only — never a raw `/dev/sdX` path, which
  can shift across reboots or hardware changes.
- Include `nofail` so a missing or failed disk doesn't hang boot.
- `x-systemd.automount` is a reasonable default so the mount doesn't block
  startup.

Example (this workstation's actual working configuration, included as a
concrete pattern to follow, not a value to copy onto a different device):

```fstab
UUID=1fcc973c-455c-4b22-8836-c017075d41c4 /mnt/data ext4 defaults,nofail,x-systemd.automount 0 2
```

## Worked Example (Dated, Illustrative — Re-Verify Live)

On this workstation, as audited during this skill's initial setup:

- `/dev/sda1` (ext4, label `data`) — the workspace disk, correctly mounted
  at `/mnt/data` via the UUID-based fstab entry above, and independently
  also mounted at `/media/codelf/data` (same device, via the desktop
  session's own label-based automount — not a symlink, but functionally
  equivalent).
- `/media/codelf/DataBridge` (`nvme0n1p5`, exfat, labeled `DataBridge`) — a
  deliberately-named shared/dual-boot bridge partition. Excluded: it has an
  existing purpose.
- `nvme0n1p1` (EFI), `p3`/`p4` (NTFS, Windows), `p6` (`/`, the running Linux
  root) — all off-limits per the classification defaults above.
- `nvme0n1p2` — the Microsoft Reserved Partition case described above.

**This is evidence for the policy, not live truth to trust on a future
run.** This skill may run on more than one machine, or after hardware
changes on this one (a new drive, a repartition, a dual-boot change). Always
re-run the read-only inspection commands and re-check with GParted when
storage is actually relevant to the task at hand — never assume this
worked example still describes current reality.
