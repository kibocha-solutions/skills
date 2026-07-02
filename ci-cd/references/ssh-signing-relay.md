# SSH Signing Bridge For CI/CD

This reference keeps CI/CD commit and push work connected to SSH evidence
without duplicating the SSH setup guides.

Use the `ssh` skill for SSH authentication, signing, host aliases,
password-manager agents, local keys, and production SSH access. CI/CD owns the
commit, push, branch, pull request, and release workflow around that SSH path.

---

## CI/CD Responsibilities

Before a commit or push, CI/CD should collect enough evidence to know which
SSH path is active:

```bash
git config --show-origin core.sshCommand
git config --show-origin gpg.format
git config --show-origin gpg.ssh.program
git config --show-origin user.signingkey
git config --show-origin gpg.ssh.allowedSignersFile
printf 'SSH_AUTH_SOCK=%s\n' "$SSH_AUTH_SOCK"
command -v ssh.exe
command -v ssh-add.exe
command -v op-ssh-sign-wsl.exe
```

Also inspect the remote URL and cached repo identity:

```bash
git remote -v
git config user.name
git config user.email
```

Record this evidence in `.agents/brain/git/repo-health.json` when repo-health
is being refreshed.

## When To Use The SSH Skill

Switch to the `ssh` skill before changing:

- SSH config files
- `core.sshCommand`
- `gpg.ssh.program`
- `gpg.ssh.allowedSignersFile`
- `user.signingkey`
- password-manager SSH agent settings
- host aliases
- local SSH key files

After the SSH skill has established the active path, return to CI/CD for:

- staging and commit preparation
- signed commit attempts
- push and pull request workflow
- branch cleanup
- CI checks and release handoff
