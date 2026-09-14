# System Init Checklist

## 1. Permissions

1. Run `sudo -n -l`.
2. Record the allowed command paths, run-as identity, password requirement, and argument restrictions.
3. Confirm privileged edit entries name exact files.
4. Confirm no shell, interpreter, broad editor, or unrestricted command is granted.
5. Do not test a denied command by attempting it.

## 2. Storage

```bash
lsblk -f
findmnt
df -h
sed -n '1,240p' /etc/fstab
```

1. Map each device to its filesystem, label, UUID, mount point, and known purpose.
2. Mark every reserved, boot, recovery, diagnostic, foreign-system, and unknown partition off-limits.
3. Confirm the workspace mount uses a stable identifier.
4. Confirm the operating account can read and write the workspace without privilege.
5. Do not create, format, resize, or mount anything during inspection.

## 3. Toolchain

```bash
java -version
javac -version
kotlinc -version
python3 --version
pip3 --version
python3 -m venv --help
docker --version
docker compose version
node --version
npm --version
git --version
gh --version
glab --version
```

1. Record missing commands without installing them.
2. Record each executable path with `command -v`.
3. Compare versions with official current sources.
4. Record Docker access separately from sudoers scope.

## 4. Report

1. List every check and observed result.
2. Mark each item current, outdated, missing, broken, misconfigured, or unknown.
3. List every requested change that fails the qualifying-installation gate or
   requires a separate destructive, account, security-control, or device
   decision.
4. Do not claim completion until the final checks pass.
