# Version Control SSH Authentication

Git over SSH is used for `git clone`, `git pull`, and `git push` against a
version-control provider such as GitHub, GitLab, or Bitbucket. The SSH key
proves the account identity; the provider still decides whether that account
can read or write the repository.

Normal server access is covered in `SSH Access Guide`. Signed commits are
covered in `Git Commit Signing with SSH Keys`. Deploy keys, CI machine keys,
and production access controls are covered in `Securing SSH Access to Critical
Infrastructure`.

## **CRITICAL PREREQUISITE: Git for Windows Installation**

<aside>
⚠️

**MUST DO FIRST:** If you already have Git for Windows installed, you MUST uninstall it completely before proceeding. Incorrect Git SSH configuration is the #1 cause of password manager SSH agent failures.

</aside>

### Why This Matters

Git for Windows bundles its own SSH client that **cannot** communicate with password manager SSH agents (1Password, Bitwarden). You must configure Git to use Windows' native OpenSSH client instead.

### Step 0.1: Uninstall Existing Git for Windows

1. Open **Settings → Apps → Installed Apps**
2. Search for "Git"
3. Click **Uninstall** on "Git for Windows"
4. Restart your computer (optional but recommended)

### Step 0.2: Download Git for Windows

Download the latest version from: https://git-scm.com/download/win

### Step 0.3: Install Git with These EXACT Settings

**Run the installer and configure each screen as follows:**

| **Installer Screen** | **Select This Option** | **Why This Matters** |
| --- | --- | --- |
| Select Components | **Default** (leave as is) | Includes necessary shell extensions and large file support |
| Choosing the default editor | **Use Vim** (or your preferred editor) | Determines what opens for `git commit` without message. Vim is lightweight and universal. |
| Adjusting the name of the initial branch | **Override:** `main` | `main` is the modern standard (replacing `master`). Matches GitHub default. |
| Adjusting your PATH environment | **Git from the command line and also from 3rd-party software** (Recommended) | Allows running `git` from PowerShell, Command Prompt, or terminals |
| **Choosing the SSH executable** | **🔴 Use external OpenSSH** | **CRITICAL FIX.** Forces Git to use Windows 10/11 built-in SSH client, enabling communication with password manager SSH agents. **DO NOT select "Use bundled OpenSSH"** |
| Choosing HTTPS transport backend | **Use the native Windows Secure Channel library** | Uses system security certificates. Enterprise/School friendly. Easier maintenance. |
| Configuring line ending conversions | **Checkout Windows-style, commit Unix-style** | Prevents formatting issues when sharing code between Windows and Linux/Mac |
| Configuring the terminal emulator | **Use MinTTY** (default) | Provides "Git Bash" window option for Linux-like terminal experience |
| Choose default behavior of `git pull` | **Fast-forward or merge** (Default) | Standard behavior. Keeps history clean and warns on diverged branches. |
| Choose a credential helper | **Git Credential Manager** | Handles HTTPS passwords automatically (backup to SSH authentication) |
| Configuring extra options | **Enable file system caching**<br>**(Optional) Enable symbolic links** | Caching speeds up Git on large projects. Symbolic links useful for complex projects. |
| Configuring experimental options | **Leave unchecked** | Experimental features can be unstable |

### Step 0.4: Verify Git Installation

Open a **new** PowerShell window and run:

```powershell
git --version
```

Expected output: `git version 2.x.x.windows.x`

### Step 0.5: Verify SSH Client

Verify Git is using external OpenSSH:

```powershell
git config --global core.sshCommand
```

**If empty or shows Windows OpenSSH:** Git is correctly using system OpenSSH (default behavior when "external OpenSSH" selected).

**If shows path to bundled Git SSH:** Reinstall Git with correct settings.

---

## Git SSH Model

Git providers use a fixed SSH username and a provider host:

```text
git@github.com
git@gitlab.com
git@bitbucket.org
```

The repository owner, namespace, or workspace comes after the host:

```text
git@github.com:OWNER/REPO.git
git@gitlab.com:NAMESPACE/PROJECT.git
git@bitbucket.org:WORKSPACE/REPO.git
```

The SSH key authenticates the provider account. Repository permission is a
separate provider check. If SSH authentication succeeds but Git says the
repository does not exist, the key may belong to an account that lacks access
to that repository.

## Choose A Git SSH Method

Manual SSH keys store the private key as a local file. This route works on
Windows, WSL, Linux, and macOS without a password manager. Use a passphrase,
keep private key permissions strict, and upload only the public key to the Git
provider.

Bitwarden Desktop SSH Agent stores the private key in Bitwarden. Windows Git
must use Windows OpenSSH so the Git SSH process can reach Bitwarden's agent.
WSL2 can use the same Bitwarden agent by calling `ssh.exe` through Git with
`core.sshCommand=ssh.exe`.

1Password Desktop SSH Agent stores the private key in 1Password. Its Windows
and WSL2 authentication route also uses Windows OpenSSH. Commit signing uses a
different 1Password helper and is configured in `Git Commit Signing with SSH
Keys`.

SSH host aliases are required when one workstation uses multiple accounts on
the same provider. The alias tells SSH which provider host, account key, and
agent route to use for each repository.

## Git SSH Host Aliases

A host alias changes only the host part of the remote URL. The provider still
receives `git@github.com`, `git@gitlab.com`, or `git@bitbucket.org` after SSH
applies the config.

Example aliases:

```sshconfig
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/ssh_auth_github_personal.pub
    IdentitiesOnly yes

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/ssh_auth_github_work.pub
    IdentitiesOnly yes
```

Use the alias in the Git remote:

```bash
git clone git@github-work:ORG/REPO.git
```

SSH connects to `github.com`, uses the key selected by `github-work`, and Git
asks GitHub for `ORG/REPO.git`.

### Config File Locations

| Environment | SSH Config Path Used By Git SSH |
| --- | --- |
| Linux | `~/.ssh/config` |
| macOS | `~/.ssh/config` |
| WSL with native Linux OpenSSH | `~/.ssh/config` |
| Windows OpenSSH | `%USERPROFILE%\.ssh\config` |
| WSL Git with `core.sshCommand=ssh.exe` | Windows `%USERPROFILE%\.ssh\config` |

When WSL Git uses `ssh.exe`, Git calls the Windows SSH client. Host aliases and
identity selection must be placed in Windows `%USERPROFILE%\.ssh\config`.

1. **Create public key marker files for password-manager keys when needed.**

   Save each public key as a `.pub` file so OpenSSH can select the intended
   account:

   ```bash
   mkdir -p ~/.ssh
   nano ~/.ssh/ssh_auth_github_work.pub
   chmod 600 ~/.ssh/ssh_auth_github_work.pub
   ```

   On Windows, save the same file under:

   ```text
   %USERPROFILE%\.ssh\ssh_auth_github_work.pub
   ```

2. **Add a provider alias.**

   Linux, macOS, or native WSL:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityFile ~/.ssh/ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

   Windows OpenSSH:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityFile C:\Users\Ada\.ssh\ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

   Replace `Ada` with the Windows account folder name on the workstation.

3. **Test the alias.**

   ```bash
   ssh -T git@github-work
   ```

   GitHub usually responds with a greeting that includes the authenticated
   account name. GitLab and Bitbucket return their own provider-specific
   greeting.

4. **Use the alias in the remote URL.**

   ```bash
   git remote set-url origin git@github-work:ORG/REPO.git
   git remote -v
   ```

## Manual Git SSH Keys

Manual keys are ordinary local files. The provider receives the public key. The
private key remains on the workstation.

### Linux, macOS, And WSL Native OpenSSH

1. **Create a provider key.**

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ssh-keygen -t ed25519 -C "user@example.com" -f ~/.ssh/id_ed25519_github
   ```

2. **Load the key into the local SSH agent.**

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519_github
   ```

3. **Copy the public key.**

   ```bash
   cat ~/.ssh/id_ed25519_github.pub
   ```

4. **Add the public key to the provider.**

   GitHub: open **Settings → SSH and GPG keys → New SSH key**.

   GitLab: open **Preferences → SSH Keys → Add new key**.

   Bitbucket: open **Personal settings → SSH keys → Add key**.

5. **Add an SSH config entry.**

   ```sshconfig
   Host github.com
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_ed25519_github
       IdentitiesOnly yes
   ```

6. **Test provider authentication.**

   ```bash
   ssh -T git@github.com
   ```

7. **Clone or update the remote URL.**

   ```bash
   git clone git@github.com:OWNER/REPO.git
   ```

### Windows OpenSSH

1. **Create a provider key.**

   ```powershell
   New-Item -ItemType Directory -Force $env:USERPROFILE\.ssh
   ssh-keygen.exe -t ed25519 -C "user@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_github
   ```

2. **Start the Windows OpenSSH agent for local key files.**

   ```powershell
   Set-Service ssh-agent -StartupType Automatic
   Start-Service ssh-agent
   ssh-add.exe $env:USERPROFILE\.ssh\id_ed25519_github
   ```

   Skip this service setup when Bitwarden Desktop or 1Password Desktop owns the
   SSH agent.

3. **Copy the public key.**

   ```powershell
   Get-Content $env:USERPROFILE\.ssh\id_ed25519_github.pub
   ```

4. **Add the public key to the provider.**

   Use the provider's SSH key settings and paste the public key as a new
   authentication key.

5. **Test provider authentication.**

   ```powershell
   ssh.exe -T git@github.com
   ```

## Bitwarden Desktop SSH Agent For Git

Bitwarden Desktop owns the private key. Git authenticates through the SSH agent
that Bitwarden exposes to the platform SSH client.

### Windows Native Git

1. **Enable Bitwarden Desktop SSH Agent.**

   Open Bitwarden Desktop, unlock the vault, and enable SSH Agent support in
   settings. Keep the desktop app running.

2. **Disable the Windows OpenSSH Authentication Agent service.**

   Open PowerShell as Administrator:

   ```powershell
   Stop-Service ssh-agent -ErrorAction SilentlyContinue
   Set-Service ssh-agent -StartupType Disabled
   ```

3. **Create or import the Git authentication key in Bitwarden.**

   Name the SSH key item after the provider account, such as
   `ssh_auth_github_work`.

4. **Add the public key to the provider.**

   Copy the public key from Bitwarden and add it to the provider account:

   GitHub: **Settings → SSH and GPG keys → New SSH key**.

   GitLab: **Preferences → SSH Keys → Add new key**.

   Bitbucket: **Personal settings → SSH keys → Add key**.

5. **Confirm Windows OpenSSH sees the key.**

   ```powershell
   ssh-add.exe -L
   ```

   Expected result: the Bitwarden public key prints.

6. **Add a Windows SSH host alias when multiple provider accounts exist.**

   Edit `%USERPROFILE%\.ssh\config`:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityFile C:\Users\Ada\.ssh\ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

7. **Test provider authentication.**

   ```powershell
   ssh.exe -T git@github-work
   ```

8. **Clone or set the remote URL.**

   ```powershell
   git clone git@github-work:ORG/REPO.git
   ```

### WSL2 Git Using Windows OpenSSH

WSL2 can use Bitwarden's Windows agent by making Git call `ssh.exe`. This is
the selected route for Bitwarden-backed Git in WSL2.

1. **Confirm the Windows route works.**

   From PowerShell:

   ```powershell
   ssh-add.exe -L
   ssh.exe -T git@github.com
   ```

2. **Configure WSL Git to use Windows OpenSSH.**

   From WSL:

   ```bash
   git config --global core.sshCommand ssh.exe
   ```

3. **Add convenient WSL aliases.**

   Add these lines to `~/.bashrc` or the shell profile used on the workstation:

   ```bash
   alias ssh='ssh.exe'
   alias ssh-add='ssh-add.exe'
   ```

   Reload the shell:

   ```bash
   source ~/.bashrc
   ```

4. **Put provider host aliases in Windows SSH config.**

   Edit `%USERPROFILE%\.ssh\config` from Windows:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityFile C:\Users\Ada\.ssh\ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

5. **Test from WSL.**

   ```bash
   ssh-add -L
   ssh -T git@github-work
   git ls-remote git@github-work:ORG/REPO.git HEAD
   ```

   Expected result: `ssh-add -L` prints the Bitwarden key, provider SSH
   authentication succeeds, and `git ls-remote` prints the repository HEAD.

6. **Use native WSL SSH diagnostics explicitly.**

   The aliases make `ssh` and `ssh-add` call Windows tools. Use `/usr/bin/ssh`
   and `/usr/bin/ssh-add` when inspecting Linux OpenSSH inside WSL.

### Linux And macOS Git

1. **Enable Bitwarden Desktop SSH Agent.**

   Open Bitwarden Desktop, unlock the vault, and enable SSH Agent support.

2. **Configure the provider host alias.**

   Linux common socket:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityAgent ~/.bitwarden-ssh-agent.sock
       IdentityFile ~/.ssh/ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

   macOS installations can use a package-specific socket path. Check
   Bitwarden Desktop's SSH Agent settings when the common socket path does not
   work.

3. **Test provider authentication.**

   ```bash
   ssh -T git@github-work
   git ls-remote git@github-work:ORG/REPO.git HEAD
   ```

## 1Password Desktop SSH Agent For Git

1Password Desktop owns the private key. Git authenticates through the SSH agent
that 1Password exposes to the platform SSH client.

### Windows Native Git

1. **Enable the 1Password SSH Agent.**

   Open 1Password for Windows, unlock the account, and enable the SSH Agent in
   Developer settings.

2. **Disable the Windows OpenSSH Authentication Agent service.**

   Open PowerShell as Administrator:

   ```powershell
   Stop-Service ssh-agent -ErrorAction SilentlyContinue
   Set-Service ssh-agent -StartupType Disabled
   ```

3. **Create or import the Git authentication key in 1Password.**

   Name the SSH key item after the provider account, such as
   `ssh_auth_github_work`.

4. **Add the public key to the provider.**

   Copy the public key from 1Password and add it to the provider account's SSH
   key settings.

5. **Test provider authentication.**

   ```powershell
   ssh-add.exe -L
   ssh.exe -T git@github.com
   ```

6. **Use host aliases for multiple accounts.**

   Edit `%USERPROFILE%\.ssh\config`:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityFile C:\Users\Ada\.ssh\ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

### WSL2 Git Using Windows OpenSSH

1Password's WSL authentication route uses Windows OpenSSH for Git SSH
connections.

1. **Confirm the Windows route works.**

   From PowerShell:

   ```powershell
   ssh-add.exe -L
   ssh.exe -T git@github.com
   ```

2. **Configure WSL Git to use Windows OpenSSH.**

   ```bash
   git config --global core.sshCommand ssh.exe
   ```

3. **Add convenient WSL aliases.**

   ```bash
   alias ssh='ssh.exe'
   alias ssh-add='ssh-add.exe'
   ```

   Reload the shell:

   ```bash
   source ~/.bashrc
   ```

4. **Place provider host aliases in Windows SSH config.**

   Edit `%USERPROFILE%\.ssh\config`:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityFile C:\Users\Ada\.ssh\ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

5. **Test from WSL.**

   ```bash
   ssh-add -L
   ssh -T git@github-work
   git ls-remote git@github-work:ORG/REPO.git HEAD
   ```

### Linux And macOS Git

1. **Enable the 1Password SSH Agent.**

   Open 1Password, unlock the account, and enable the SSH Agent in Developer
   settings. On Linux, use a 1Password installation route that supports the SSH
   agent.

2. **Configure the provider host alias.**

   Linux:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityAgent ~/.1password/agent.sock
       IdentityFile ~/.ssh/ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

   macOS:

   ```sshconfig
   Host github-work
       HostName github.com
       User git
       IdentityAgent "~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
       IdentityFile ~/.ssh/ssh_auth_github_work.pub
       IdentitiesOnly yes
   ```

3. **Test provider authentication.**

   ```bash
   ssh -T git@github-work
   git ls-remote git@github-work:ORG/REPO.git HEAD
   ```

## Clone And Convert Repositories

Clone with the default provider host:

```bash
git clone git@github.com:OWNER/REPO.git
```

Clone with an account alias:

```bash
git clone git@github-work:ORG/REPO.git
```

Convert an existing repository from HTTPS to SSH:

```bash
git remote -v
git remote set-url origin git@github-work:ORG/REPO.git
git remote -v
```

Verify repository access without changing files:

```bash
git ls-remote origin HEAD
```

Expected result: Git prints the commit hash for the remote `HEAD`.

## Repository Identity After Clone

SSH chooses the provider account. Git author identity controls commit metadata.
Set author identity per repository when a workstation uses personal and work
accounts.

```bash
git config user.name "Ada Lovelace"
git config user.email "ada@example.com"
git config --show-origin --get user.name
git config --show-origin --get user.email
```

For a global default:

```bash
git config --global user.name "Ada Lovelace"
git config --global user.email "ada@example.com"
```

Commit signing is configured separately in `Git Commit Signing with SSH Keys`.

## Automation And Deploy Keys

Repository automation should use a deploy key, machine user, GitHub App, GitLab
deploy token, or Bitbucket access key according to the provider and access
scope. Personal workstation keys should stay tied to the person who owns the
workstation.

For production CI/CD, read `Securing SSH Access to Critical Infrastructure`
before adding keys to runners, servers, repositories, or organization settings.

## Troubleshooting Git SSH

### Git Still Prompts For HTTPS Credentials

Check the remote URL:

```bash
git remote -v
```

If the URL starts with `https://`, switch it to SSH:

```bash
git remote set-url origin git@github-work:ORG/REPO.git
```

### Permission Denied Publickey

Run SSH in verbose mode:

```bash
ssh -vvv -T git@github-work
```

Check whether SSH offers the expected key. If no key is offered, inspect the
SSH config path for the active environment. WSL Git using `ssh.exe` reads the
Windows SSH config file.

### Provider Authenticates The Wrong Account

Provider greetings usually include the authenticated account. If the account is
wrong, create a host alias for the correct account and use that alias in the
remote URL:

```bash
git remote set-url origin git@github-work:ORG/REPO.git
```

### Too Many Authentication Failures

Add `IdentitiesOnly yes` and an `IdentityFile` that points to the intended
private key or public key marker file:

```sshconfig
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/ssh_auth_github_work.pub
    IdentitiesOnly yes
```

### WSL Git Is Using The Wrong SSH Client

Check the configured SSH command:

```bash
git config --global --get core.sshCommand
```

For the Bitwarden and 1Password Windows-agent route, expected output is:

```text
ssh.exe
```

Check shell aliases:

```bash
type -a ssh
type -a ssh-add
```

Call native WSL tools explicitly when troubleshooting Linux OpenSSH:

```bash
/usr/bin/ssh -V
/usr/bin/ssh-add -L
```

### Host Key Verification Failed

Inspect the stored host key:

```bash
ssh-keygen -F github.com
```

Remove a stale key only after confirming the provider's published SSH host key
fingerprint:

```bash
ssh-keygen -R github.com
```

Connect again:

```bash
ssh -T git@github.com
```

## Final Verification

Run these checks from the environment where Git will be used:

```bash
git remote -v
ssh -T git@github-work
git ls-remote origin HEAD
```

Successful output proves that the repository remote uses SSH, the provider
recognizes the account, and Git can read the repository.
