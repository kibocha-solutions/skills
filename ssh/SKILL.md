---
name: ssh
description: >
  Configure, troubleshoot, and document SSH authentication, SSH access, SSH
  config, password-manager SSH agents, Git SSH remotes, SSH commit signing,
  host aliases, deploy keys, operator keys, and SSH security controls. Use
  whenever the user mentions SSH keys, ssh-agent, Bitwarden SSH Agent,
  1Password SSH Agent, WSL SSH, core.sshCommand, gpg.ssh.program,
  allowedSignersFile, authorized_keys, bastions, deploy keys, or signed
  commits.
---

# SSH

## Goal

Help the user configure, diagnose, and document SSH access and SSH signing
with platform-specific accuracy. Keep SSH concerns separate from CI/CD
workflow concerns: this skill owns SSH methods, key paths, agents, host
aliases, signing configuration, remote authentication, and infrastructure SSH
controls.

When the task also involves commits, branches, pull requests, CI pipelines,
deployment, releases, or history cleanup, use the `ci-cd` skill for that
workflow and this skill for the SSH portion.

## Reference Routing

Read only the reference needed for the current SSH task:

- `references/ssh-access-guide.md` for general SSH use, server access, host
  aliases, `scp`, `rsync`, `sftp`, tunnels, agent forwarding, Bitwarden, and
  1Password agent setup.
- `references/version-control-ssh-auth.md` for Git provider SSH
  authentication, GitHub/GitLab/Bitbucket remote URLs, account aliases,
  Windows OpenSSH, WSL, Bitwarden, 1Password, and local SSH keys for clone,
  fetch, pull, and push.
- `references/git-commit-signing-with-ssh-keys.md` for SSH commit signing,
  `gpg.format ssh`, `user.signingkey`, `gpg.ssh.program`,
  `gpg.ssh.allowedSignersFile`, provider verification, Bitwarden signing,
  1Password signing, and local-key signing.
- `references/securing-ssh-access.md` for critical infrastructure, operator
  keys, deploy keys, service accounts, emergency access, rotation,
  offboarding, `authorized_keys`, bastions, and production SSH controls.

## Operating Rules

- Inspect the active environment before changing it. Prefer evidence from
  `ssh -V`, `ssh-add -L`, `type -a ssh`, `type -a ssh-add`, `git config
  --show-origin --get-regexp '^(core\.sshCommand|gpg\.format|gpg\.ssh\.program|gpg\.ssh\.allowedSignersFile|user\.signingkey|commit\.gpgsign)$'`,
  `SSH_AUTH_SOCK`, and the relevant SSH config files.
- Do not generate SSH keys unless the user explicitly asks for key generation.
  When key generation is requested, do not print private-key material in chat.
- Do not remove, replace, or bypass signing configuration just to make a Git
  operation succeed. If signing is configured and fails, diagnose the active
  signing path.
- Do not introduce `npiperelay`, `socat`, `rbw`, or a WSL `SSH_AUTH_SOCK`
  bridge for the selected Bitwarden-on-WSL method. The documented method uses
  Windows OpenSSH from WSL with `core.sshCommand ssh.exe`,
  `gpg.ssh.program /mnt/c/Windows/System32/OpenSSH/ssh-keygen.exe`, and shell
  aliases for interactive convenience.
- For 1Password on WSL, follow 1Password's WSL signing helper path from the
  user's 1Password configuration. Do not invent the `op-ssh-sign-wsl.exe`
  path if it is not visible in the environment or provided by the user.
- When writing documentation, use direct procedure language. Avoid changelog
  narration, fourth-wall commentary, unsupported design rationale, and
  historical struggle notes.
- If a later reference has already covered a concept in an earlier reference,
  cross-reference the document by title instead of duplicating the full
  explanation.

## Verification Pattern

Use the narrowest verification set that proves the requested path:

- Agent visibility: `ssh-add -L` or, on WSL with Windows OpenSSH,
  `ssh-add.exe -L`.
- Provider authentication: `ssh -T git@github.com`, `ssh -T git@gitlab.com`,
  `ssh -T git@bitbucket.org`, or the configured host alias.
- Git remote use: `git ls-remote origin HEAD`.
- SSH signing config: `git config gpg.format`,
  `git config user.signingkey`, `git config gpg.ssh.program`, and
  `git config gpg.ssh.allowedSignersFile`.
- Commit verification: `git log --show-signature -1` after a signed test or
  real commit.

Stop and report the exact failing command and error text when the evidence no
longer supports the selected path.
