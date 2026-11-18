# Steward Examples

## 1. Editing a tracked file

### Bad

```bash
cp config/settings.yaml config/settings.yaml.bak
sed -i 's/workers: 8/workers: 2/' config/settings.yaml
```

Defects:
- Duplicates a file Git already versions.
- Leaves `settings.yaml.bak` in the worktree after the task.

### Good

```bash
git status --short config/settings.yaml
sed -i 's/workers: 8/workers: 2/' config/settings.yaml
git diff config/settings.yaml
```

## 2. Moving a document

### Bad

```bash
cp reports/q3-review.docx archive/q3-review.docx
```

Defects:
- The instruction was to move; the source remains and two copies diverge.

### Good

```bash
git mv reports/q3-review.docx archive/q3-review.docx
```

## 3. Editing a system file outside version control

### Bad

```bash
sudo cp /etc/fstab /etc/fstab.bak
sudo cp /etc/fstab /etc/fstab.orig
sudo cp /etc/fstab /etc/fstab.$(date +%Y%m%d)
```

Defects:
- Three backups of one target.
- No removal condition; the copies stay indefinitely.

### Good

```bash
sudo cp /etc/fstab /etc/fstab.bak
python3 steward/scripts/steward.py ledger add backup /etc/fstab.bak "remove after the next clean reboot"
# after the reboot succeeds
sudo rm /etc/fstab.bak
python3 steward/scripts/steward.py ledger close /etc/fstab.bak
```

## 4. Running a disposable database for a test

### Bad

```bash
podman run -d -e POSTGRES_PASSWORD=x postgres:18
```

Defects:
- No `--rm`; the container and its anonymous data volume outlive the test.
- No throwaway label; nothing can find it for cleanup.

### Good

```bash
podman run -d --rm --label agent.throwaway=true -e POSTGRES_PASSWORD=x --name scratch-db postgres:18
python3 steward/scripts/steward.py ledger add container scratch-db "stop after the migration test passes"
# after the test
podman stop scratch-db
python3 steward/scripts/steward.py ledger close scratch-db
```

## 5. Starting a heavy build

### Bad

Starting a container image build while a test suite and a virtual machine already run, on a machine reporting 1.4 GiB available memory.

### Good

```bash
bash steward/scripts/system-profile.sh --brief
```

The summary reports 1.4 GiB available, below the 2 GiB budget. Stop the idle processes you started, rerun the summary, and report to the user when memory stays below budget.

## 6. Respecting repository approval mode

### Bad

Ignoring the user's directive to auto-handle everything in a repository, asking for permission before cleaning pre-existing `.bak` leftovers, or leaving unrelated pre-existing edits unstaged when the repository `approval_mode` is `true`.

### Good

```bash
python3 steward/scripts/steward.py approval set true "User authorized auto-effected changes and cleanup across this repo"
python3 steward/scripts/steward.py check --fix
```

In `true` mode, `check --fix` and `stop` automatically remove untracked backup files and throwaway containers, move `.agents/` evidence to the store, and commits absorb all repository changes cleanly. In `ask` mode, in-scope throwaway resources are cleaned automatically while pre-existing out-of-scope edits are preserved and confirmed first. In `false` mode, every destructive or committing act waits for explicit user approval.
