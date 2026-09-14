# Storage and Partitions

## 1. Inspect

```bash
lsblk -f
findmnt
df -h
sed -n '1,240p' /etc/fstab
```

1. Record the model, device path, partition table, filesystem, label, UUID, size, mount point, flags, and known purpose.
2. Use a trusted graphical partition view or platform management console when command output is ambiguous.
3. Reconcile conflicting evidence before classifying a device.

## 2. Classify

1. Mark the running system, boot, EFI, reserved, recovery, diagnostic, encrypted, RAID, LVM, and foreign-system partitions off-limits unless the user explicitly places them in scope.
2. Mark every unknown partition off-limits.
3. Do not treat an unmounted or unlabeled partition as free space.
4. Do not treat a filesystem signature as proof of purpose.
5. Preserve every device containing existing data.

## 3. Authorize a destructive operation

1. Name the exact device path and stable hardware identifiers.
2. Name the exact operation and expected data loss.
3. Obtain the user's current-session confirmation naming that device and operation.
4. Re-run the inspection immediately before execution.
5. Stop if any identifier changed or any ambiguity remains.
6. Do not substitute a different device, partition, or command.

## 4. Configure a non-destructive mount

1. Confirm the filesystem already exists and contains the expected data.
2. Confirm the target mount point.
3. Use the filesystem UUID in persistent configuration.
4. Preserve existing mount options unless the user requests changes.
5. Add failure-tolerant boot options when required by the platform and use case.
6. Apply privileged changes only through an authorized exact-file edit path.
7. Validate the configuration before relying on it.

## 5. Verify

1. Confirm the expected device is mounted at the expected path.
2. Confirm the mounted UUID matches the persistent rule.
3. Confirm the operating account owns or can use the workspace as intended.
4. Confirm a read, write, rename, and delete test inside a dedicated temporary test directory.
5. Remove only that test directory after verification.
6. Reboot verification requires user coordination and explicit authorization.
