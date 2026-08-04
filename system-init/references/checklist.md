# Checklist

The operational spine of `system-init`. Run these four phases in order. For
each item: run the command, compare against the expected result, and if it
doesn't match, follow the remediation pointer, **then re-run that exact
check** before moving to the next item — don't assume a fix worked. Do not
skip ahead on the assumption that a later phase is fine because an earlier
one was; each phase is independently in one of the three states described
in `SKILL.md`'s "How This Works."

## Phase 1 — Sudoers / Permissions

```bash
sudo -n ss -tln
sudo -n apt-get update
sudo -n systemctl status ssh
```
Expected:
- `ss` succeeds with no password prompt (`INSPECT` alias).
- `apt-get` succeeds with no password prompt if `SOFTWARE` has been granted
  on this account, or fails with "a password is required" if it hasn't —
  either is consistent, confirm it matches what was actually intended.
- `systemctl` always fails with "a password is required" — it is never in
  scope. If it succeeds, the grant is wider than intended; stop and report
  this immediately, do not proceed to later phases.

If the sudoers file doesn't exist yet or scope doesn't match intent: follow
`permissions.md` → "Sudoers Setup — From Scratch," then re-run all three
checks above. Read "Prohibited Invocation Forms," "Install Approval,"
"Out-of-Scope Commands," "Editing Privileged Files," and "Permission Denied
Is a Boundary" in that same file before using any granted command — the
grant existing is not the same as every invocation of it being safe.

## Phase 2 — Storage

```bash
lsblk -f
findmnt
cat /etc/fstab
ls -ld /mnt/data   # confirm this account owns the workspace mount directly
test -L ~/data && readlink -f ~/data
```
Expected: the intended workspace partition is mounted, UUID-based in
`/etc/fstab` with `nofail`, no raw `/dev/sdX` entries; the operating account
owns the workspace mount directly (unprivileged read/write/delete, not a
sudoers concern — see `storage-and-partitions.md` → "Workspace Access Is
Already Unprivileged"); `~/data` resolves to the workspace mount.

If the expected mount is absent, or any partition's purpose is unclear:
follow `storage-and-partitions.md` in full — start with "Read-Only
Inspection First, Always" (GParted for anything ambiguous), respect "The
Hard Rule" and "Classification Defaults" at every step, and never proceed
past "Existing-Data Safety" without explicit live user confirmation of the
exact target device. If `~/data` is missing, create it per that file's
symlink instruction. Re-run the inspection commands above after any change.

## Phase 3 — Toolchain

```bash
java -version && javac -version
kotlinc -version
python3 --version && pip3 --version && python3 -m venv --help >/dev/null
docker --version && docker compose version && groups
node --version && npm --version
git --version
gh --version
glab --version
```
Expected: each tool present and on its current LTS/stable line (see
`toolchain.md` → "Compare Against Current LTS/Stable, Not Whatever's
Installed" for what "current" means per tool).

If anything is missing or outdated: do not install or upgrade. Follow
`toolchain.md` → "Ask Before Resolving — Always" — stop and ask the user
for leave, citing the specific tool and version gap found.

## Phase 4 — Completion Report

Assemble the report from the actual pass/fail state of Phases 1–3 as just
run — not from memory of a previous pass, not from assumption. Include:

- Sudoers scope as just confirmed via Phase 1 (note: "confirmed via `sudo
  -l`/the checks above," not asserted from memory of what was intended).
- Storage status (Phase 2 result, including the specific mount point and
  device).
- Toolchain versions and any gaps (Phase 3 result, per tool).
- **Unresolved items, enumerated explicitly.** Never state or imply full
  success if anything above required the user's action and hasn't been
  confirmed resolved yet. A report that omits an open item is incorrect,
  not just incomplete.
