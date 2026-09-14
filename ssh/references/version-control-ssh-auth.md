# Git SSH Authentication

## 1. Inspect

```bash
git remote -v
git config --show-origin --get core.sshCommand
ssh -V
ssh-add -L
```

1. Identify the provider account and repository.
2. Identify the SSH client used by Git.
3. Identify the active agent and offered public keys.
4. Do not uninstall or reinstall Git as a troubleshooting shortcut.

## 2. Select an identity

1. Use a local private key, operating-system agent, or configured password-manager agent.
2. Upload only the public key to the provider.
3. Use a dedicated host alias when multiple provider accounts exist.
4. Put the alias in the config file read by Git's active SSH client.
5. Use a public-key marker only when the selected agent route requires it.

## 3. Configure a provider alias

```sshconfig
Host <provider-alias>
    HostName <provider-host>
    User git
    IdentityFile <verified-key-or-public-marker>
    IdentitiesOnly yes
```

1. Replace the remote host with `<provider-alias>`.
2. Preserve the repository owner and repository path.
3. Verify the new URL with `git remote -v`.

## 4. Configure WSL

1. Determine whether Git uses Linux OpenSSH or Windows OpenSSH.
2. Keep configuration in the matching Linux or Windows SSH config file.
3. Set `core.sshCommand` only when the user selected a non-default client route.
4. Verify the exact executable with `type -a` and `git config --show-origin`.
5. Do not add `npiperelay`, `socat`, or an `SSH_AUTH_SOCK` bridge to a Windows OpenSSH route.

## 5. Verify

1. Run `ssh -G <provider-alias>`.
2. Run the provider's documented authentication test.
3. Confirm the returned account identity.
4. Run `git ls-remote origin HEAD`.
5. Confirm the remote commit identifier is returned.

## 6. Diagnose

1. Use `ssh -vvv -T git@<provider-alias>`.
2. Confirm the expected key is offered.
3. Confirm the provider accepted the intended account.
4. Confirm repository authorization separately from SSH authentication.
5. Inspect host keys before changing `known_hosts`.
6. Preserve commit-signing configuration during authentication repairs.
