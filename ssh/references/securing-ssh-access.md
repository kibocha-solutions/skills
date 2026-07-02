# Securing SSH Access to Critical Infrastructure

Critical SSH access covers production servers, deployment runners, privileged
repositories, bastion hosts, database hosts, and automation accounts. The
control objective is simple: every SSH key must have an owner, a purpose, a
scope, a review path, and a removal path.

Workstation setup for normal server access is covered in `SSH Access Guide`.
Git clone, pull, push, and provider account keys are covered in `Version
Control SSH Authentication`. Commit and tag signatures are covered in `Git
Commit Signing with SSH Keys`.

## Access Classes

Classify each SSH key before installing it.

| Class | Example | Storage | Review Cadence |
| --- | --- | --- | --- |
| Personal workstation key | Developer access to a staging server | Local key file, Bitwarden, or 1Password | At onboarding, role change, and offboarding |
| Production operator key | Named engineer access through a bastion | Password manager or hardware-backed workstation route | Monthly or before high-risk maintenance |
| Deploy key | Read-only repository access for one deployment target | CI secret store or server secret path | Each release cycle or quarterly |
| Machine user key | Automation account with cross-repository access | CI secret store with named owner | Monthly |
| Break-glass key | Emergency access when normal identity systems fail | Restricted vault item with dual-control access | After every use and quarterly |

Shared human keys are unsuitable for critical infrastructure. A server or
repository should identify whether a key belongs to a person, a machine, or an
emergency procedure.

## Minimum Controls

Use these controls before a key reaches production infrastructure.

1. **Assign an owner.**

   Record the human owner, team owner, or service owner. For automation, record
   both the owning team and the maintainer responsible for rotation.

2. **Limit the scope.**

   A key should unlock only the account, host, repository, or automation path it
   needs. Prefer one deploy key per repository or deployment target.

3. **Prefer named accounts.**

   Use `ada`, `deploy-web`, or `ci-release` instead of shared accounts such as
   `admin` for routine access. Keep `root` login disabled for SSH unless the
   environment has a documented emergency exception.

4. **Require a removal path.**

   Record where the public key is installed and how to remove it. A key without
   a known removal path becomes a long-term incident risk.

5. **Separate authentication from signing.**

   Git provider authentication keys are covered in `Version Control SSH
   Authentication`. Commit signing keys are covered in `Git Commit Signing with
   SSH Keys`. Use separate keys when repository access and author identity need
   separate rotation or evidence.

6. **Record verification evidence.**

   Keep the command output or provider screen that proves the key works, the
   scope is correct, and old access was removed.

## Key Inventory

Maintain an inventory for production and privileged SSH keys. A spreadsheet,
ticket table, password-manager item, or internal asset record is acceptable
when it is searchable and reviewed.

Required fields:

| Field | Example |
| --- | --- |
| Key ID | `ssh-prod-bastion-ada-2026-07` |
| Public key fingerprint | `SHA256:V7Lk4cS8h9Nq2pR6tYw3AaBbCcDdEeFfGgHhIiJjKkL` |
| Owner | `Ada Lovelace` |
| Team | `Platform` |
| Purpose | `Production bastion access` |
| Scope | `bastion-prod-01, user ada` |
| Storage location | `1Password item: SSH / Ada prod bastion` |
| Installed location | `/home/ada/.ssh/authorized_keys on bastion-prod-01` |
| Created date | `2026-07-03` |
| Review date | `2026-08-03` |
| Rotation or expiry date | `2026-10-03` |
| Emergency removal command | `sudo sed -i '/ada@company.example 2026-07 prod-bastion/d' /home/ada/.ssh/authorized_keys` |

Capture a fingerprint from a public key:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

Capture a fingerprint from a pasted public key:

```bash
printf '%s\n' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com' | ssh-keygen -lf -
```

## Server-Side Hardening

These examples assume Ubuntu Server with OpenSSH. Test changes in a second
session before closing the current working SSH session.

1. **Back up the server SSH configuration.**

   ```bash
   sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.$(date +%Y%m%d%H%M%S).bak
   ```

2. **Edit the OpenSSH server configuration.**

   ```bash
   sudo nano /etc/ssh/sshd_config
   ```

3. **Use a restrictive baseline.**

   ```sshconfig
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   KbdInteractiveAuthentication no
   X11Forwarding no
   AllowAgentForwarding no
   AllowTcpForwarding no
   MaxAuthTries 3
   ```

   Enable `AllowAgentForwarding` or `AllowTcpForwarding` only in host-specific
   or account-specific exceptions where the operational need is documented.

4. **Validate the configuration.**

   ```bash
   sudo sshd -t
   ```

   Expected result: no output and exit status `0`.

5. **Reload OpenSSH.**

   ```bash
   sudo systemctl reload ssh
   ```

6. **Test from a new terminal before ending the existing session.**

   ```bash
   ssh deploy@203.0.113.10 'whoami && hostname'
   ```

## Authorized Keys Controls

The `authorized_keys` file is the server-side access list for a Linux account.
Protect it with ownership, permissions, and optional restrictions.

1. **Set safe permissions.**

   ```bash
   sudo chown -R deploy:deploy /home/deploy/.ssh
   sudo chmod 700 /home/deploy/.ssh
   sudo chmod 600 /home/deploy/.ssh/authorized_keys
   ```

2. **Add a key with an owner comment.**

   ```text
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= ada@company.example 2026-07 prod-bastion
   ```

3. **Restrict a deploy key to one command when possible.**

   ```text
   command="/usr/local/bin/deploy-web",no-agent-forwarding,no-X11-forwarding,no-pty ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= deploy-web@ci
   ```

4. **Restrict a key to known source addresses when the network is stable.**

   ```text
   from="198.51.100.10,198.51.100.11",no-agent-forwarding,no-X11-forwarding ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= ada@company.example
   ```

5. **List installed keys during review.**

   ```bash
   sudo awk '{print NR ": " $1 " " $2 " " $3}' /home/deploy/.ssh/authorized_keys
   ```

## Bastion Hosts

A bastion should be the controlled entry point for private infrastructure.

1. **Use named user accounts.**

   Each operator should authenticate with an individual key. Avoid shared
   bastion users for human access.

2. **Keep private hosts off the public internet.**

   Private hosts should accept SSH only from the bastion or management network.

3. **Use `ProxyJump` from the workstation.**

   Workstation SSH config:

   ```sshconfig
   Host prod-bastion
       HostName bastion.example.com
       User ada

   Host prod-app-01
       HostName 10.20.30.41
       User deploy
       ProxyJump prod-bastion
   ```

4. **Disable agent forwarding by default.**

   Use `ProxyJump` for transport. Enable `ForwardAgent yes` only for a named
   host where the remote session must authenticate to another SSH destination.

## Password-Manager-Backed Operator Keys

Bitwarden Desktop SSH Agent and 1Password Desktop SSH Agent can hold operator
private keys. The public key still belongs in server `authorized_keys`, Git
provider settings, or automation configuration.

### Bitwarden Operator Keys

1. **Store the private key in Bitwarden.**

   Use an SSH key item with a title that identifies the owner and scope, such as
   `Ada prod bastion SSH`.

2. **Install only the public key on infrastructure.**

   Add the public key to the target account's `authorized_keys` file.

3. **Use the Windows OpenSSH route for WSL workstations.**

   WSL operator access uses `ssh.exe` and `ssh-add.exe` as described in `SSH
   Access Guide`. Native WSL diagnostics should call `/usr/bin/ssh` and
   `/usr/bin/ssh-add`.

4. **Remove the public key when access ends.**

   Deleting the vault item alone does not remove server-side access if the
   public key remains in `authorized_keys`.

### 1Password Operator Keys

1. **Store the private key in 1Password.**

   Use an SSH key item with an owner and infrastructure scope in the title.

2. **Install only the public key on infrastructure.**

   Add the public key to the target account's `authorized_keys` file.

3. **Use Windows OpenSSH for WSL authentication.**

   WSL operator access uses Windows `ssh.exe`. Windows SSH config owns host
   aliases and key selection for that route.

4. **Review 1Password item access with server access.**

   A user who can read or use the SSH key item may be able to authenticate as
   the corresponding server account while the server public key remains active.

## Git Provider And CI Keys

Provider keys used by CI/CD should be scoped to the automation need.

### Repository Deploy Keys

Use a deploy key when one repository needs access to one deployment target or
one external automation path.

1. **Create a dedicated key.**

   ```bash
   ssh-keygen -t ed25519 -a 100 -f ./deploy_key_repo_web_readonly -C "deploy-key repo-web readonly 2026-07"
   ```

2. **Add the public key to the provider as a deploy key.**

   Prefer read-only access when the automation only pulls code.

3. **Store the private key in the CI secret store.**

   Name the secret after the repository and scope, such as
   `REPO_WEB_DEPLOY_KEY`.

4. **Record the public key fingerprint in the key inventory.**

   ```bash
   ssh-keygen -lf ./deploy_key_repo_web_readonly.pub
   ```

5. **Delete the local private key copy after installing the secret.**

   Keep the durable private key only in the approved secret store.

### Machine User Keys

Use a machine user when automation needs access across several repositories and
the provider lacks a better application or token model.

1. **Create a provider account owned by the team.**

   The account should use a team mailbox or managed identity process.

2. **Give the account the narrowest provider role that works.**

   Avoid organization-wide admin privileges for repository automation.

3. **Store the private key in the CI secret store.**

   Record the owner, repositories, and rotation date in the key inventory.

4. **Review repository membership on the same cadence as the key.**

   Removing the key while leaving the machine user in privileged groups leaves
   the next key able to regain broad access.

## Commit Signing Enforcement

Commit signing proves that a trusted signing key produced a commit or tag
signature. Code review, CI checks, and branch protection remain separate
controls.

1. **Configure developer signing first.**

   Use `Git Commit Signing with SSH Keys` to configure signing keys,
   `gpg.format=ssh`, `user.signingkey`, and `allowedSignersFile`.

2. **Enable provider-side protection.**

   Use GitHub, GitLab, or Bitbucket branch protection features to require signed
   commits where the repository policy demands it.

3. **Keep signing keys separate from deploy keys.**

   Deploy keys identify automation access. Signing keys identify commit authors
   or release automation.

4. **Record bot signing identities.**

   Automation that signs release commits or tags should have a named bot
   identity, a provider account or signing-key record, and a rotation owner.

## Rotation Procedure

Rotate a key when a person changes role, a workstation is replaced, a provider
or server scope changes, the key reaches its rotation date, or compromise is
suspected.

1. **Create the replacement key.**

   Use the same storage route as the original key unless the rotation is caused
   by storage compromise.

2. **Install the replacement public key.**

   Add it to `authorized_keys`, provider settings, or the CI secret store.

3. **Test the replacement.**

   ```bash
   ssh prod-app-01 'whoami && hostname'
   ```

   For Git provider keys:

   ```bash
   ssh -T git@github.com
   git ls-remote origin HEAD
   ```

4. **Remove the old public key.**

   Delete it from `authorized_keys`, provider settings, deploy key settings, or
   machine-user SSH keys.

5. **Verify the old key no longer works.**

   Use a workstation or CI dry run that still has the old key available. Record
   the failed authentication result.

6. **Update the inventory.**

   Record the new fingerprint, installation location, review date, and removal
   evidence for the old key.

## Offboarding Procedure

Run offboarding for every person or automation identity that leaves a role with
SSH access.

1. **Find owned keys.**

   Search the inventory by person, team, provider account, email address, key
   comment, and fingerprint.

2. **Remove server access.**

   Remove the person's public keys from every relevant `authorized_keys` file
   and bastion configuration.

3. **Remove provider access.**

   Remove Git provider SSH keys, deploy keys, machine-user access, and team
   memberships tied to the person or automation identity.

4. **Remove password-manager access.**

   Remove access to Bitwarden or 1Password items that contain operator keys.

5. **Invalidate active sessions where the platform supports it.**

   Restart SSH sessions, revoke provider sessions, or disable the account when
   immediate removal is required.

6. **Record evidence.**

   Capture command output, provider settings screenshots, tickets, or audit-log
   links that prove access was removed.

## Emergency Disablement

Use emergency disablement when a key, workstation, password-manager account,
CI secret, or provider account may be compromised.

1. **Remove the public key first.**

   Remove the key from `authorized_keys`, provider SSH settings, deploy keys, or
   machine-user keys.

2. **Disable the account when key ownership is uncertain.**

   Lock the Linux user, disable the provider account, or pause the CI runner
   when the key cannot be isolated quickly.

3. **Restart exposed sessions where necessary.**

   ```bash
   sudo pkill -KILL -u deploy
   ```

   Use this only when the account should lose active sessions immediately.

4. **Rotate dependent secrets.**

   Rotate deploy keys, host credentials, cloud credentials, and tokens that may
   have been reachable from the compromised session.

5. **Preserve evidence.**

   Keep logs, key fingerprints, command history, and timestamps needed for the
   incident record.

## Review Checklist

Run this checklist during access review.

1. **Inventory completeness.**

   Every installed production key has an owner, scope, fingerprint, creation
   date, review date, and removal path.

2. **Server access.**

   Each production `authorized_keys` entry maps to an inventory record.

   ```bash
   sudo find /home -path '*/.ssh/authorized_keys' -type f -print
   ```

3. **Provider access.**

   Git provider SSH keys, deploy keys, machine users, and bot accounts match
   the inventory.

4. **CI/CD access.**

   CI secret names, repository permissions, runner access, and deployment
   targets match the documented scope.

5. **Password-manager access.**

   Bitwarden and 1Password item access matches the server or repository access
   granted by the public key.

6. **Signing enforcement.**

   Protected branches that require signed commits have a documented signer
   onboarding and recovery process.

7. **Expired access.**

   Keys past their review or rotation date are removed or rotated.

## Verification Commands

List local fingerprints:

```bash
find ~/.ssh -name '*.pub' -type f -exec ssh-keygen -lf {} \;
```

List server authorized-key entries:

```bash
sudo awk '{print FILENAME ":" FNR ": " $1 " " $2 " " $3}' /home/*/.ssh/authorized_keys
```

Check OpenSSH server configuration:

```bash
sudo sshd -T | rg 'permitrootlogin|passwordauthentication|pubkeyauthentication|allowagentforwarding|allowtcpforwarding|maxauthtries'
```

Test a bastion path:

```bash
ssh prod-app-01 'whoami && hostname'
```

Verify a Git provider deploy key or machine key:

```bash
ssh -T git@github.com
git ls-remote origin HEAD
```

Verify latest signed commit:

```bash
git log --show-signature -1
```

## Final Access Record

A completed access change should leave these records behind:

| Record | Required Evidence |
| --- | --- |
| Key creation | Public key fingerprint and owner |
| Key installation | Server path, provider setting, or CI secret name |
| Scope | Host, repository, account, and permission level |
| Verification | Successful SSH, Git, or signing command |
| Review date | Next scheduled review |
| Removal path | Command or provider location used to revoke access |
