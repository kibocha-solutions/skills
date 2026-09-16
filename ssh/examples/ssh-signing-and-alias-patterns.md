# SSH Examples: Signing and Host Alias Configuration

## 1. Multiple Git Accounts on Same Host (GitHub)

### Bad (Host Key Collisions and Identity Leaks)

```ssh-config
# BAD: Generic Host without IdentitiesOnly, offering all loaded keys
Host github.com
  User git
  IdentityFile ~/.ssh/id_work
  IdentityFile ~/.ssh/id_personal
```

Defects:
- Omits `IdentitiesOnly yes`, causing ssh-agent to cycle through all loaded keys until the server rejects with "Too many authentication failures".
- Both personal and work identities mixed under the same hostname.

### Good (Dedicated Host Aliases with Strict Identity Isolation)

```ssh-config
# GOOD: Explicit aliases, IdentitiesOnly, strict key mapping
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_work_ed25519
  IdentitiesOnly yes

Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_personal_ed25519
  IdentitiesOnly yes
```

Usage in Git remotes:
```bash
git remote set-url origin git@github-work:company/repo.git
```

## 2. SSH Commit Signing Configuration

```bash
# Configure local repository to sign commits with SSH key
git config user.signingkey ~/.ssh/id_work_ed25519.pub
git config gpg.format ssh
git config commit.gpgsign true

# Allowed signers verification file
git config gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
echo "engineer@company.com $(cat ~/.ssh/id_work_ed25519.pub)" >> ~/.ssh/allowed_signers
```
