# SSH Access Guide

SSH access lets a workstation open a secure shell, copy files, or create a
tunnel to another machine. The private key can live as a local file, in
Bitwarden Desktop, or in 1Password Desktop. Choose one route for a workstation
and make the SSH client use that route consistently.

Git provider authentication is covered in `Version Control SSH Authentication`.
SSH commit signing is covered in `Git Commit Signing with SSH Keys`.
Production access policy, rotation, and emergency handling are covered in
`Securing SSH Access to Critical Infrastructure`.

## SSH Access Model

SSH uses four pieces:

| Piece | What It Does | Example |
| --- | --- | --- |
| SSH client | Runs on the workstation and opens the connection | `ssh`, `ssh.exe`, `scp`, `sftp` |
| SSH server | Runs on the remote machine and accepts connections | `sshd` on Ubuntu Server |
| Private key | Secret material used to prove identity | local file, Bitwarden item, 1Password item |
| Public key | Safe-to-copy key installed where access is allowed | `~/.ssh/authorized_keys` on a server |

The private key remains on the workstation or inside the password manager. The
public key is copied to the remote server account. A successful login proves
that the SSH client can use the matching private key and that the remote server
allows that public key for the target account.

## Choose An SSH Method

Manual SSH keys store the private key as a file under `~/.ssh` or
`%USERPROFILE%\.ssh`. This route works on every platform and needs no password
manager. Protect the private key with filesystem permissions and a passphrase.
Use this route for local development machines, disposable lab servers, or
systems where password-manager integration is unavailable.

Bitwarden Desktop SSH Agent stores the private key in Bitwarden and exposes it
through the local SSH agent interface. On Windows, Git and SSH should use
Windows OpenSSH so they can talk to the Bitwarden agent. In WSL2, the working
route is to call Windows OpenSSH commands from WSL with `ssh.exe`,
`ssh-add.exe`, and related Windows tools. WSL does not need `SSH_AUTH_SOCK` for
this route.

1Password Desktop SSH Agent stores the private key in 1Password and exposes it
through its SSH agent. On Windows with WSL2, 1Password's documented integration
also uses Windows OpenSSH from WSL for authentication. 1Password has a separate
WSL helper for Git commit signing, which belongs in `Git Commit Signing with
SSH Keys`.

## SSH Host Aliases

Host aliases make repeated SSH commands predictable. The alias belongs in an
SSH config file and can define the hostname, username, port, key, agent, and
jump host for a connection.

Use the same alias everywhere once it works:

```bash
ssh staging-api
scp ./app.env staging-api:/srv/app/.env
sftp staging-api
```

### Config File Locations

| Environment | SSH Config Path |
| --- | --- |
| Linux | `~/.ssh/config` |
| macOS | `~/.ssh/config` |
| WSL using Linux OpenSSH | `~/.ssh/config` |
| Windows OpenSSH | `%USERPROFILE%\.ssh\config` |
| WSL calling `ssh.exe` | Windows `%USERPROFILE%\.ssh\config` |

When WSL calls `ssh.exe`, Windows OpenSSH reads the Windows config file. Do not
expect WSL's `~/.ssh/config` to control a connection opened by `ssh.exe`.

1. **Create the config directory.**

   Linux, macOS, or WSL native OpenSSH:

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   touch ~/.ssh/config
   chmod 600 ~/.ssh/config
   ```

   Windows PowerShell:

   ```powershell
   New-Item -ItemType Directory -Force $env:USERPROFILE\.ssh
   New-Item -ItemType File -Force $env:USERPROFILE\.ssh\config
   ```

2. **Add a basic server alias.**

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       Port 22
       IdentitiesOnly yes
   ```

   Replace `203.0.113.10` with the server IP address or DNS name. Replace
   `deploy` with the remote Linux account.

3. **Add a non-default port when the server uses one.**

   ```sshconfig
   Host bastion
       HostName bastion.example.com
       User ops
       Port 2222
   ```

4. **Add a jump host when the server is reachable through a bastion.**

   ```sshconfig
   Host private-db
       HostName 10.10.20.15
       User dbadmin
       ProxyJump bastion
   ```

5. **Test the alias.**

   ```bash
   ssh staging-api 'whoami && hostname'
   ```

   Expected result: the command prints the remote account name and hostname,
   then returns to the local prompt.

## Manual SSH Keys

Manual keys are ordinary files. The private key must remain private; the public
key can be copied to servers and services.

### Linux, macOS, And WSL Native OpenSSH

1. **Create the SSH directory.**

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ```

2. **Create an Ed25519 key.**

   ```bash
   ssh-keygen -t ed25519 -C "user@example.com" -f ~/.ssh/id_ed25519
   ```

   Enter a passphrase when prompted. Use the email address that identifies the
   workstation owner.

3. **Start the local agent and load the key.**

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

4. **Print the public key.**

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

5. **Install the public key on the server.**

   If password login is available for the first connection:

   ```bash
   ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@203.0.113.10
   ```

   If `ssh-copy-id` is unavailable, sign in with the server's existing method
   and append the public key to the target account:

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   nano ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

6. **Test the login.**

   ```bash
   ssh deploy@203.0.113.10 'whoami && hostname'
   ```

### Windows OpenSSH

1. **Create the SSH directory.**

   ```powershell
   New-Item -ItemType Directory -Force $env:USERPROFILE\.ssh
   ```

2. **Create an Ed25519 key.**

   ```powershell
   ssh-keygen.exe -t ed25519 -C "user@example.com" -f $env:USERPROFILE\.ssh\id_ed25519
   ```

3. **Start the Windows OpenSSH agent when using local key files.**

   ```powershell
   Set-Service ssh-agent -StartupType Automatic
   Start-Service ssh-agent
   ssh-add.exe $env:USERPROFILE\.ssh\id_ed25519
   ```

   Skip this service step when Bitwarden Desktop or 1Password Desktop owns the
   SSH agent.

4. **Print the public key.**

   ```powershell
   Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
   ```

5. **Install the public key on the server and test the login.**

   ```powershell
   ssh.exe deploy@203.0.113.10 "whoami && hostname"
   ```

## Bitwarden Desktop SSH Agent

Bitwarden Desktop must be unlocked for the SSH agent to answer key requests.
The SSH client receives a key offer from the agent and Bitwarden prompts for
approval according to the Desktop app settings.

### Windows Native SSH

1. **Update Bitwarden Desktop.**

   Use a Bitwarden Desktop release that includes SSH Agent support. Open
   Bitwarden Desktop, sign in, and unlock the vault.

2. **Enable the Bitwarden SSH Agent.**

   Open Bitwarden Desktop settings and enable the SSH Agent option. Keep
   Bitwarden Desktop running.

3. **Disable the Windows OpenSSH Authentication Agent service.**

   Bitwarden needs to own the Windows OpenSSH agent pipe. Open PowerShell as
   Administrator:

   ```powershell
   Stop-Service ssh-agent -ErrorAction SilentlyContinue
   Set-Service ssh-agent -StartupType Disabled
   ```

4. **Create or import an SSH key in Bitwarden.**

   Add an SSH key item in Bitwarden. Use a name that identifies the machine,
   account, or server group, such as `ssh_auth_staging_api`.

5. **Install the public key on the remote server.**

   Copy the public key from the Bitwarden SSH key item and add it to the target
   account's `~/.ssh/authorized_keys` on the server.

6. **Confirm that Windows OpenSSH can see the Bitwarden key.**

   ```powershell
   ssh-add.exe -L
   ```

   Expected result: at least one public key prints. If the command cannot
   connect to an agent, unlock Bitwarden Desktop and confirm the SSH Agent
   option is enabled.

7. **Test server access.**

   ```powershell
   ssh.exe deploy@203.0.113.10 "whoami && hostname"
   ```

### WSL2 Using Windows OpenSSH

WSL can use the Bitwarden Windows agent by calling Windows OpenSSH directly.
The private key stays inside Bitwarden, and WSL does not need an agent socket.

1. **Confirm the Windows route works first.**

   From PowerShell:

   ```powershell
   ssh-add.exe -L
   ssh.exe deploy@203.0.113.10 "whoami && hostname"
   ```

2. **Add WSL command aliases.**

   Add these lines to `~/.bashrc` or the shell profile used by the workstation:

   ```bash
   alias ssh='ssh.exe'
   alias ssh-add='ssh-add.exe'
   ```

   Reload the shell:

   ```bash
   source ~/.bashrc
   ```

3. **Use the Windows SSH config file for aliases.**

   Create or edit `%USERPROFILE%\.ssh\config` from Windows:

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       Port 22
       IdentitiesOnly yes
   ```

4. **Test from WSL.**

   ```bash
   ssh-add -L
   ssh staging-api 'whoami && hostname'
   ```

   Expected result: `ssh-add -L` prints the Bitwarden public key and `ssh`
   reaches the remote server.

5. **Run native WSL diagnostics explicitly when needed.**

   The aliases make `ssh` and `ssh-add` call Windows tools. Use these commands
   when troubleshooting native Linux OpenSSH inside WSL:

   ```bash
   /usr/bin/ssh -V
   /usr/bin/ssh-add -L
   ```

### Linux Desktop

1. **Enable Bitwarden Desktop SSH Agent.**

   Open Bitwarden Desktop, unlock the vault, and enable SSH Agent support in
   settings.

2. **Point OpenSSH at the Bitwarden socket when needed.**

   Bitwarden Desktop exposes a Unix socket. The common Linux path is:

   ```text
   ~/.bitwarden-ssh-agent.sock
   ```

   Flatpak, Snap, and other package formats may use a package-specific socket
   path. Check Bitwarden Desktop's SSH Agent settings when the socket is not at
   the common path.

3. **Add an SSH host entry.**

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       IdentityAgent ~/.bitwarden-ssh-agent.sock
       IdentitiesOnly yes
   ```

4. **Test the key list and login.**

   ```bash
   SSH_AUTH_SOCK="$HOME/.bitwarden-ssh-agent.sock" ssh-add -L
   ssh staging-api 'whoami && hostname'
   ```

### macOS

1. **Enable Bitwarden Desktop SSH Agent.**

   Open Bitwarden Desktop, unlock the vault, and enable SSH Agent support.

2. **Use the Bitwarden socket in SSH config when needed.**

   A common macOS socket path is:

   ```text
   ~/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock
   ```

   The exact path can differ by installation source. Check Bitwarden Desktop's
   SSH Agent settings if `ssh-add -L` cannot connect.

3. **Add a host entry.**

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       IdentityAgent ~/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock
       IdentitiesOnly yes
   ```

## 1Password Desktop SSH Agent

1Password Desktop must be unlocked for the SSH agent to answer key requests.
SSH keys are stored in 1Password items. The public key is copied to the remote
server and the private key remains in 1Password.

### Windows Native SSH

1. **Enable the 1Password SSH Agent.**

   Open 1Password for Windows, unlock the account, and enable the SSH Agent in
   the Developer settings.

2. **Disable the Windows OpenSSH Authentication Agent service.**

   1Password uses the Windows OpenSSH agent interface. Open PowerShell as
   Administrator:

   ```powershell
   Stop-Service ssh-agent -ErrorAction SilentlyContinue
   Set-Service ssh-agent -StartupType Disabled
   ```

3. **Create or import an SSH key in 1Password.**

   Create an SSH key item, or import an existing key. Copy the public key from
   the item.

4. **Install the public key on the remote server.**

   Add the public key to the target account's `~/.ssh/authorized_keys`.

5. **Test from Windows.**

   ```powershell
   ssh-add.exe -L
   ssh.exe deploy@203.0.113.10 "whoami && hostname"
   ```

### WSL2 Using Windows OpenSSH

WSL can use the 1Password Windows agent by calling Windows OpenSSH. The same
command-alias pattern used for Bitwarden applies.

1. **Confirm the Windows route works first.**

   ```powershell
   ssh-add.exe -L
   ssh.exe deploy@203.0.113.10 "whoami && hostname"
   ```

2. **Add WSL command aliases.**

   ```bash
   alias ssh='ssh.exe'
   alias ssh-add='ssh-add.exe'
   ```

   Reload the shell:

   ```bash
   source ~/.bashrc
   ```

3. **Put host aliases in the Windows SSH config file.**

   Edit `%USERPROFILE%\.ssh\config`:

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       IdentitiesOnly yes
   ```

4. **Test from WSL.**

   ```bash
   ssh-add -L
   ssh staging-api 'whoami && hostname'
   ```

### Linux Desktop

1. **Install 1Password for Linux from a supported package.**

   The 1Password SSH agent requires the desktop app and a supported install
   route. Flatpak and Snap Store installations are unsuitable for the SSH agent
   on Linux.

2. **Enable the SSH Agent.**

   Open 1Password, unlock the account, and enable the SSH Agent in Developer
   settings.

3. **Add a host entry.**

   1Password's Linux socket is usually under:

   ```text
   ~/.1password/agent.sock
   ```

   SSH config:

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       IdentityAgent ~/.1password/agent.sock
       IdentitiesOnly yes
   ```

4. **Test access.**

   ```bash
   SSH_AUTH_SOCK="$HOME/.1password/agent.sock" ssh-add -L
   ssh staging-api 'whoami && hostname'
   ```

### macOS

1. **Enable the 1Password SSH Agent.**

   Open 1Password for Mac, unlock the account, and enable the SSH Agent in
   Developer settings.

2. **Add a host entry when explicit socket selection is needed.**

   ```sshconfig
   Host staging-api
       HostName 203.0.113.10
       User deploy
       IdentityAgent "~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
       IdentitiesOnly yes
   ```

3. **Test access.**

   ```bash
   ssh-add -L
   ssh staging-api 'whoami && hostname'
   ```

## Prepare A Remote Server

These commands assume Ubuntu Server and an account with `sudo` access. Run them
on the remote server through the provider console, an existing SSH login, or a
bootstrap account.

1. **Install the OpenSSH server.**

   ```bash
   sudo apt update
   sudo apt install -y openssh-server
   sudo systemctl enable --now ssh
   sudo systemctl status ssh
   ```

2. **Allow SSH through the firewall when UFW is enabled.**

   ```bash
   sudo ufw allow OpenSSH
   sudo ufw status
   ```

3. **Create a deployment account when needed.**

   ```bash
   sudo adduser deploy
   sudo usermod -aG sudo deploy
   ```

4. **Install the public key for the account.**

   ```bash
   sudo -u deploy mkdir -p /home/deploy/.ssh
   sudo chmod 700 /home/deploy/.ssh
   sudo -u deploy nano /home/deploy/.ssh/authorized_keys
   sudo chmod 600 /home/deploy/.ssh/authorized_keys
   sudo chown -R deploy:deploy /home/deploy/.ssh
   ```

5. **Test from the workstation.**

   ```bash
   ssh deploy@203.0.113.10 'whoami && hostname'
   ```

## Copy Files Over SSH

Use `scp` for a small file, `sftp` for interactive file work, and `rsync` for
repeatable directory sync.

Copy one file:

```bash
scp ./local.env staging-api:/srv/app/.env
```

Copy a directory:

```bash
scp -r ./dist staging-api:/srv/app/dist
```

Sync a directory and delete files that no longer exist locally:

```bash
rsync -av --delete ./dist/ staging-api:/srv/app/dist/
```

Open an interactive file session:

```bash
sftp staging-api
```

## SSH Tunnels

Local forwarding exposes a remote service on the workstation.

```bash
ssh -L 15432:127.0.0.1:5432 staging-api
```

The workstation can then connect to `localhost:15432`, and SSH forwards traffic
to `127.0.0.1:5432` from the server's point of view.

Use an SSH config alias for repeated tunnels:

```sshconfig
Host staging-db-tunnel
    HostName 203.0.113.10
    User deploy
    LocalForward 15432 127.0.0.1:5432
```

Open it:

```bash
ssh staging-db-tunnel
```

## Agent Forwarding

Agent forwarding lets a remote server ask the workstation's SSH agent to sign a
challenge. The private key stays on the workstation or in the password manager,
but any process that can use the forwarded agent socket on the remote server can
request signatures while the session is open.

Enable forwarding only for hosts that need it:

```sshconfig
Host deploy-runner
    HostName 203.0.113.20
    User deploy
    ForwardAgent yes
```

Confirm forwarding from inside the remote session:

```bash
ssh-add -L
```

If the remote command does not need to reach another SSH destination, leave
agent forwarding disabled.

## Troubleshooting

### Permission Denied

Run the client in verbose mode:

```bash
ssh -vvv staging-api
```

Check for these lines:

```text
Offering public key
Server accepts key
Permission denied
```

If no key is offered, the SSH client is using the wrong config file or cannot
reach the agent. If the server accepts the key and then denies access, inspect
the remote account shell, account lock state, `authorized_keys` options, and
server logs.

### Too Many Authentication Failures

The agent may offer several keys before the correct one. Add a host-specific
public key file and `IdentitiesOnly yes`:

```sshconfig
Host staging-api
    HostName 203.0.113.10
    User deploy
    IdentityFile ~/.ssh/ssh_auth_staging_api.pub
    IdentitiesOnly yes
```

For password-manager agents, `IdentityFile` can point to a public key file that
matches the private key stored in the manager.

### Host Key Verification Failed

Inspect the old known-host entry before replacing it:

```bash
ssh-keygen -F 203.0.113.10
```

Remove a stale entry only after confirming the server was rebuilt or its host
key changed through an approved maintenance action:

```bash
ssh-keygen -R 203.0.113.10
```

Connect again and verify the new fingerprint through the server provider,
console, or administrator.

### WSL Uses The Wrong SSH Client

Check which command will run:

```bash
type -a ssh
type -a ssh-add
```

With the Windows OpenSSH route, the first entries should be aliases for
`ssh.exe` and `ssh-add.exe`. For native WSL checks, call:

```bash
/usr/bin/ssh -V
/usr/bin/ssh-add -L
```

### Password Manager Key Is Visible But Login Fails

Confirm that the public key installed on the server matches the key listed by
the agent:

```bash
ssh-add -L
```

Compare that output with the line in the server account's
`~/.ssh/authorized_keys`. The key type and key body must match exactly.

## Final Verification

Run one command that proves the selected route can authenticate and execute a
remote command:

```bash
ssh staging-api 'whoami && hostname && uname -a'
```

Successful output includes the remote account name, host name, and kernel
details. Record the host alias in the workstation notes or onboarding checklist
after this command works.
