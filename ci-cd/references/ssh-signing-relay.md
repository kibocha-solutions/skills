# SSH Signing Relay — Bitwarden and 1Password on Windows and WSL2

This reference explains how to route SSH signing keys managed by a Windows
password manager (Bitwarden or 1Password) into WSL2, so that `git commit -S`
and `ssh` commands inside WSL2 use those keys without copying private key
material into the Linux filesystem.

---

## How It Works

Bitwarden and 1Password expose their SSH agent through a Windows named pipe:

```
//./pipe/openssh-ssh-agent
```

WSL2 cannot natively speak to Windows named pipes, so a relay is required:

- **npiperelay.exe** (Windows) reads from the named pipe and forwards data
  over stdio.
- **socat** (WSL2) listens on a Unix socket and pipes data to `npiperelay.exe`
  via `EXEC:`.
- **SSH config** (WSL2) points `IdentityAgent` at that Unix socket, so every
  `ssh` and `git` call in WSL2 uses the Windows-managed keys.

The private key material never leaves the Windows side.

---

## Prerequisites

**On Windows:**
- Bitwarden or 1Password installed with SSH Agent feature enabled and at least
  one SSH key loaded.
- `npiperelay.exe` downloaded from
  `https://github.com/jstarks/npiperelay/releases` and placed in a permanent
  location, e.g. `C:\bin\npiperelay.exe`.

**In WSL2:**
- `socat` installed: `sudo apt update && sudo apt install socat`

---

## Step 1 — Windows SSH Config

Store public keys in `C:\Users\<username>\.ssh\` and create or update
`C:\Users\<username>\.ssh\config` to map each host to its identity. The
`IdentityAgent` line in the global block tells SSH to delegate to the password
manager's named pipe rather than the local key store.

```
# ==================================================
# GLOBAL CONFIGURATION
# Forces SSH to use the password manager agent for all hosts.
# ==================================================
Host *
  IdentityAgent //./pipe/openssh-ssh-agent

# ==================================================
# GITHUB ACCOUNTS
# ==================================================

# Kibocha GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/ssh_auth_github_kibocha.pub
  IdentitiesOnly yes
```

Key points:
- `IdentityFile` here points to the **public** key (`.pub`), not the private
  key. The private key stays inside the password manager; the `.pub` file
  is used only for identity matching.
- `IdentitiesOnly yes` prevents SSH from offering any other keys, which avoids
  confusing authentication failures when multiple identities are loaded.
- If you have multiple GitHub accounts, add a separate `Host` block for each,
  using a unique alias (e.g. `Host github-personal`) and update the remote URL
  in the affected repos accordingly.

---

## Step 2 — Symlink npiperelay into WSL2

Inside WSL2, create a symlink so `npiperelay.exe` is accessible on the PATH:

```bash
sudo ln -s /mnt/c/bin/npiperelay.exe /usr/local/bin/npiperelay.exe
```

Adjust `/mnt/c/bin/` to wherever you placed the binary on Windows. Verify
with `which npiperelay.exe`.

---

## Step 3 — WSL2 SSH Agent Bridge Script

Add the following to `~/.bashrc` or `~/.zshrc` (inside WSL2). It starts the
`socat` relay once per session, creating the Unix socket that WSL2's SSH
client will use.

```bash
export SSH_AUTH_SOCK="$HOME/.ssh/agent.sock"

if ! ss -a 2>/dev/null | grep -q "$SSH_AUTH_SOCK"; then
    rm -f "$SSH_AUTH_SOCK"
    (setsid socat \
        UNIX-LISTEN:"$SSH_AUTH_SOCK",fork \
        EXEC:"npiperelay.exe -ei -s //./pipe/openssh-ssh-agent",nofork \
        &) >/dev/null 2>&1
fi
```

What each part does:
- `SSH_AUTH_SOCK` is the socket path WSL2 processes will use to find the SSH
  agent. Setting it here ensures it is consistent across all shell sessions.
- The `ss -a` check prevents launching a duplicate relay if one is already
  running from a previous terminal session.
- `setsid` detaches the relay from the current shell so it survives terminal
  closure.
- `npiperelay.exe -ei -s //./pipe/openssh-ssh-agent` connects to Bitwarden's
  (or 1Password's) named pipe and streams data over stdio to socat.

After saving, apply with `source ~/.bashrc` or open a new terminal.

---

## Step 4 — WSL2 SSH Config

Update `~/.ssh/config` inside WSL2 to point at the relay socket rather than
any local key file:

```
Host *
  IdentityAgent ~/.ssh/agent.sock
```

This overrides the Windows-side config for WSL2 SSH sessions. The socket path
must match `SSH_AUTH_SOCK` set in Step 3.

---

## Step 5 — Git Signing Configuration

For SSH commit signing, set these in the repo (or globally):

```bash
git config --global gpg.format ssh
git config --global user.signingkey "$(cat /mnt/c/Users/<username>/.ssh/SshSigningKey.pub)"
git config --global commit.gpgsign true
```

### allowedSignersFile — cross-platform setup

The `allowedSignersFile` is needed for local signature *verification* (what
`git log --show-signature` reads). The file must be accessible to git in
both environments. The strategy that works reliably is:

**1. Write the canonical file on the Windows side** (via WSL2's `/mnt/c` mount):

```bash
SIGNERS="/mnt/c/Users/<username>/.ssh/allowed_signers"
echo "your@email.com $(cat /mnt/c/Users/<username>/.ssh/SshSigningKey.pub)" > "$SIGNERS"
```

**2. Copy it into WSL2 home with correct Unix permissions:**

```bash
cp /mnt/c/Users/<username>/.ssh/allowed_signers ~/.ssh/allowed_signers
chmod 600 ~/.ssh/allowed_signers
```

The `/mnt/c` path is readable from WSL2 but `ssh-keygen -Y verify` enforces
strict Unix permissions on the file. Because Windows-mounted files cannot have
those permissions set, the copy into `~/.ssh/` is required for WSL2.

**3. Point WSL2 git at the local copy:**

```bash
git config --global gpg.ssh.allowedSignersFile "$HOME/.ssh/allowed_signers"
```

**4. Point Windows git at the Windows-side file** (run from PowerShell or cmd):

```
git config --global gpg.ssh.allowedSignersFile "C:/Users/<username>/.ssh/allowed_signers"
```

When you add a new key to the password manager, update the Windows file first
(`/mnt/c/.../allowed_signers`), then re-copy it to `~/.ssh/allowed_signers`
in WSL2. The two files stay in sync manually; automating this copy as a
login script (in `.bashrc`) is recommended for environments where keys change
often.

```bash
# Add to ~/.bashrc — keeps WSL2 copy in sync with Windows source on login
if [ -f /mnt/c/Users/<username>/.ssh/allowed_signers ]; then
  cp /mnt/c/Users/<username>/.ssh/allowed_signers ~/.ssh/allowed_signers
  chmod 600 ~/.ssh/allowed_signers
fi
```

---

## Verification

```bash
# Confirm the relay is running and keys are visible
ssh-add -l

# Test GitHub authentication
ssh -T git@github.com

# Make a signed test commit and verify
git commit --allow-empty -m "test: verify ssh signing"
git log --show-signature -1
```

A successful `ssh-add -l` lists the keys from the password manager. A
successful `ssh -T` prints `Hi <username>! You've successfully authenticated`.
The signed commit log shows `Good "git" signature`.

---

## Failure Diagnostics

**`ssh-add -l` returns "Could not open a connection to your authentication agent"**

The socat relay is not running. Check whether the process is alive:
```bash
ss -a | grep agent.sock
```
If the socket is absent, re-run the bridge script manually or open a new
terminal (which sources `.bashrc`). If the socket exists but `ssh-add -l`
still fails, the Windows SSH Agent service may not be running — start it
from Windows Services or from the password manager settings.

**`ssh-add -l` returns "The agent has no identities"**

The relay is running but the password manager has no key loaded or is locked.
Unlock Bitwarden or 1Password on the Windows side and ensure the SSH agent
feature is enabled and the key is added to the agent.

**`ssh -T git@github.com` returns "Permission denied (publickey)"**

Authentication is failing even though the relay is up. Check that:
- The key loaded in the password manager matches the public key registered in
  GitHub's SSH keys settings.
- The `IdentityFile` in `C:\Users\<username>\.ssh\config` points to the
  correct `.pub` file for this host.
- `IdentitiesOnly yes` is set so SSH is not trying other keys first.

**Commit fails with "error: gpg failed to sign the data"**

Git cannot reach the SSH agent during signing. Confirm `SSH_AUTH_SOCK` is
exported and points to an active socket (`ls -la $SSH_AUTH_SOCK`). If the
variable is unset, the bridge script did not run — source `.bashrc` and retry.

**Commit succeeds but `git log --show-signature` shows "No signature"**

`commit.gpgsign` is not set or `gpg.format` is not `ssh`. Verify with
`git config --list | grep gpg`. Re-run the signing config commands from
Step 5 and amend the commit.

---

## Alternative: wsl-ssh-agent

`wsl-ssh-agent` is a community tool that provides a similar bridge without
requiring `socat`. It has not been tested against this skill's setup. If you
choose to try it, verify independently that:
- It correctly bridges `//./pipe/openssh-ssh-agent` (not the standard OpenSSH
  pipe).
- SSH signing via `git commit -S` works end-to-end, not just SSH authentication.
- The socket path it creates is consistent and survives terminal restarts.

Do not assume the `socat` instructions above transfer directly to a
`wsl-ssh-agent` setup; the socket paths and relay startup commands differ.
