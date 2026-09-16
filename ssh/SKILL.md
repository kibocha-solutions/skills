---
name: ssh
description: Configure, diagnose, secure, and document SSH access, SSH agents, host aliases, Git remotes, deploy keys, operator keys, and SSH commit signing across Linux, macOS, Windows, and WSL. Use for SSH keys, ssh-agent, password-manager agents, authorized_keys, bastions, Git SSH authentication, or SSH signing.
---

# SSH

## 1. Classify the task

1. Identify the host environment and the SSH client that will run.
2. Identify whether the task concerns server access, file transfer, tunneling, Git authentication, commit signing, or infrastructure controls.
3. Identify every account, host, repository, key, agent, and configuration file in scope.
4. Use the CI/CD skill for branch, commit, pull request, pipeline, release, or history workflow.
5. Use this skill for SSH transport, identity, key, agent, and signing configuration.

## 2. Inspect before changing

Run the applicable read-only checks:

```bash
ssh -V
type -a ssh
type -a ssh-add
ssh-add -L
git config --show-origin --get-regexp '^(core\.sshCommand|gpg\.format|gpg\.ssh\.program|gpg\.ssh\.allowedSignersFile|user\.signingkey|commit\.gpgsign)$'
```

1. Inspect `SSH_AUTH_SOCK` without printing unrelated environment variables.
2. Inspect the active SSH config file.
3. Inspect the target Git remote when relevant.
4. Identify which configuration layer supplies each effective value.
5. Do not change configuration until the active route is proven.

## 3. Apply safety gates

1. Do not generate a key unless the user explicitly asks for key generation.
2. Do not display, copy, transmit, or store private-key material in chat or repository files.
3. Do not remove or replace a key, host entry, signer, agent, or access rule without explicit authorization for that target.
4. Do not bypass host-key verification.
5. Stop on a host-key mismatch until the expected fingerprint is verified through an independent trusted channel.
6. Do not disable a service, reload SSH, edit a firewall, terminate a session, or change a privileged file unless the user explicitly requested that exact operation and the runtime permits it.
7. Use `sudoedit` for authorized privileged file edits.
8. Preserve a working access session while testing server configuration changes.

## 4. Route to the procedure

1. Read [SSH access](references/ssh-access-guide.md) for hosts, aliases, transfers, tunnels, and agent routing.
2. Read [Git SSH authentication](references/version-control-ssh-auth.md) for provider remotes and multiple accounts.
3. Read [SSH commit signing](references/git-commit-signing-with-ssh-keys.md) for Git signing and allowed signers.
4. Read [critical infrastructure access](references/securing-ssh-access.md) for production, bastions, deploy keys, machine users, rotation, and offboarding.
5. Read only the references required by the current task.

## 5. Configure the selected route

1. Use one SSH client and agent route consistently.
2. Use host aliases for multiple accounts on the same provider or host.
3. Put aliases in the configuration file read by the active SSH client.
4. Use `IdentitiesOnly yes` when the client must offer a specific identity.
5. Use the narrowest key scope that satisfies the task.
6. Prefer repository-local Git identity and signing configuration when accounts differ by repository.
7. Preserve existing signing configuration during authentication troubleshooting.
8. Do not introduce an agent bridge when the selected platform route does not require one.

## 6. Verify

1. Verify agent visibility with `ssh-add -L` or the platform-specific equivalent.
2. Verify the selected host alias with `ssh -G <alias>`.
3. Verify server access with a harmless identity command.
4. Verify provider authentication with the provider's documented SSH test command.
5. Verify repository access with `git ls-remote origin HEAD`.
6. Verify signing configuration with `git config --show-origin`.
7. Verify an existing signed commit with `git log --show-signature -1`.
8. Create a test commit only when the user authorized a commit.
9. Stop and report the exact failing command and error when evidence contradicts the selected route.

## 7. Document

1. Record the active client, agent, config path, alias, public-key fingerprint, owner, scope, and verification command.
2. Record the installation and removal location for infrastructure keys.
3. Record review and rotation dates when required.
4. Do not record private keys, secrets, internal URLs, or credentials.
5. Use direct procedure language.

Inspect [SSH configuration examples](examples/ssh-signing-and-alias-patterns.md) for host alias and signing setups.

## 8. Pre-completion checklist

Before completing any SSH or signing configuration task, confirm evidence exists for each item:

- [ ] Existing SSH and Git configurations inspected with read-only commands.
- [ ] No private keys displayed, transmitted, or logged.
- [ ] Host-key verification preserved; no strict host checking bypassed.
- [ ] Multiple accounts configured with separate host aliases and `IdentitiesOnly yes`.
- [ ] SSH agent reachability verified via `ssh-add -L`.
- [ ] Zero AI attribution in Git commits, author fields, or documentation.
- [ ] No U+2014 em dashes in normal prose.

