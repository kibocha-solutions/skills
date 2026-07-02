# Git Commit Signing with SSH Keys

SSH commit signing attaches a cryptographic signature to a commit or tag. Git
creates the signature with an SSH private key, and Git or the provider verifies
it with the matching public key.

Git clone, pull, push, and remote URL setup are covered in `Version Control SSH
Authentication`. Normal server SSH access is covered in `SSH Access Guide`.
Repository policy, branch protection, deploy keys, and organization controls
are covered in `Securing SSH Access to Critical Infrastructure`.

## Signing Model

SSH authentication and SSH commit signing use similar key material for different
jobs.

| Workflow | Git Operation | What The Key Proves |
| --- | --- | --- |
| Git SSH authentication | `git clone`, `git pull`, `git push` | The workstation can access the repository |
| SSH commit signing | `git commit -S`, signed tags | The commit or tag was signed by a trusted private key |

Commit signing links a commit or tag to a signing key that Git or the provider
trusts. Code review, CI checks, and repository permissions remain separate
controls.

## Requirements

1. **Check Git version.**

   SSH commit signing requires Git 2.34 or newer:

   ```bash
   git --version
   ```

2. **Check OpenSSH.**

   Git's default SSH signing program is `ssh-keygen`. Password-manager signing
   routes may set `gpg.ssh.program` to a vendor-provided signer or to Windows
   `ssh-keygen.exe`.

   ```bash
   git config --show-origin --get gpg.ssh.program
   ssh -V
   ```

   `ssh -V` prints the OpenSSH version available to the current shell.

3. **Check Git author identity.**

   ```bash
   git config --show-origin --get user.name
   git config --show-origin --get user.email
   ```

   Provider verification usually depends on the commit author email matching a
   verified email on the provider account.

## Choose A Signing Method

Manual signing keys store the private key as a local file. This route works on
Windows, WSL, Linux, and macOS with OpenSSH. Use a passphrase and configure
Git with the public key file path.

Bitwarden Desktop SSH Agent stores the signing private key in Bitwarden. On
Windows and WSL2, the selected route uses Microsoft OpenSSH. Git signing uses
Windows `ssh-keygen.exe` as `gpg.ssh.program`, and WSL Git can call that
Windows executable through `/mnt/c/Windows/System32/OpenSSH/ssh-keygen.exe`.

1Password Desktop SSH Agent stores the signing private key in 1Password.
1Password can generate Git config snippets for commit signing. On WSL2, the
current Windows signer path for MSIX installations follows this shape:
`/mnt/c/Users/Ada/AppData/Local/Microsoft/WindowsApps/op-ssh-sign-wsl.exe`.
Replace `Ada` with the Windows account folder name on the workstation.

Use repository-local signing configuration when the workstation has work and
personal identities. Use global signing only when one signing identity applies
to every repository on the workstation.

## Provider Signing Keys

Register the public key as a signing key before relying on provider badges.

| Provider | Settings Path | Key Type |
| --- | --- | --- |
| GitHub | **Settings -> SSH and GPG keys -> New SSH key** | `Signing key` |
| GitLab | **Preferences -> SSH Keys -> Add new key** | `Signing` or `Authentication & Signing` |
| Bitbucket | **Personal Bitbucket settings -> SSH keys** | SSH signing key |

Use a dedicated signing key when repository access and author identity need
separate rotation or audit records. A combined authentication-and-signing key is
acceptable when the team intentionally chooses a simpler personal workstation
setup.

## Manual SSH Signing

### Linux, macOS, And WSL Native OpenSSH

1. **Create a signing key.**

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519_git_signing -C "user@example.com"
   ```

2. **Register the public key with the provider.**

   ```bash
   cat ~/.ssh/id_ed25519_git_signing.pub
   ```

   Paste the public key into the provider settings as a signing key.

3. **Configure Git.**

   Global configuration:

   ```bash
   git config --global gpg.format ssh
   git config --global user.signingkey ~/.ssh/id_ed25519_git_signing.pub
   git config --global commit.gpgsign true
   ```

   Repository-local configuration:

   ```bash
   git config --local gpg.format ssh
   git config --local user.signingkey ~/.ssh/id_ed25519_git_signing.pub
   git config --local commit.gpgsign true
   ```

4. **Create a signed commit.**

   ```bash
   git commit -S -m "Test SSH commit signing"
   ```

5. **Verify the latest commit locally.**

   ```bash
   git log --show-signature -1
   ```

### Windows OpenSSH

1. **Create a signing key.**

   ```powershell
   New-Item -ItemType Directory -Force $env:USERPROFILE\.ssh
   ssh-keygen.exe -t ed25519 -a 100 -f $env:USERPROFILE\.ssh\id_ed25519_git_signing -C "user@example.com"
   ```

2. **Register the public key with the provider.**

   ```powershell
   Get-Content $env:USERPROFILE\.ssh\id_ed25519_git_signing.pub
   ```

3. **Configure Git.**

   ```powershell
   git config --global gpg.format ssh
   git config --global user.signingkey "$env:USERPROFILE\.ssh\id_ed25519_git_signing.pub"
   git config --global gpg.ssh.program "C:/Windows/System32/OpenSSH/ssh-keygen.exe"
   git config --global commit.gpgsign true
   ```

4. **Create and verify a signed commit.**

   ```powershell
   git commit -S -m "Test SSH commit signing"
   git log --show-signature -1
   ```

## Bitwarden Desktop SSH Agent Signing

Bitwarden Desktop can hold the private signing key and authorize Git signing
requests through its SSH agent. The `user.signingkey` value should be the full
public key text copied from Bitwarden, or a public key file that contains that
same public key.

### Windows Native Git

1. **Enable Bitwarden Desktop SSH Agent.**

   Open Bitwarden Desktop, unlock the vault, and enable SSH Agent support.

2. **Disable the Windows OpenSSH Authentication Agent service.**

   Open PowerShell as Administrator:

   ```powershell
   Stop-Service ssh-agent -ErrorAction SilentlyContinue
   Set-Service ssh-agent -StartupType Disabled
   ```

3. **Create or import the signing key in Bitwarden.**

   Copy the public key from the Bitwarden SSH key item.

4. **Register the public key with the provider as a signing key.**

   Use the provider settings in `Provider Signing Keys`.

5. **Configure Git for Bitwarden signing.**

   Replace the public key value with the full public key copied from Bitwarden:

   ```powershell
   git config --global gpg.format ssh
   git config --global user.signingkey "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com"
   git config --global gpg.ssh.program "C:/Windows/System32/OpenSSH/ssh-keygen.exe"
   git config --global commit.gpgsign true
   ```

6. **Create and verify a signed commit.**

   ```powershell
   git commit -S -m "Test Bitwarden SSH signing"
   git log --show-signature -1
   ```

   Expected result: Bitwarden prompts for approval before Git writes the signed
   commit.

### WSL2 Using Windows OpenSSH Tools

WSL2 uses the Bitwarden Windows agent by calling Windows OpenSSH tools. Git SSH
authentication uses `ssh.exe`, and Git signing uses Windows `ssh-keygen.exe`.

1. **Confirm the Windows route works.**

   From PowerShell:

   ```powershell
   ssh-add.exe -L
   git config --global gpg.ssh.program "C:/Windows/System32/OpenSSH/ssh-keygen.exe"
   ```

2. **Configure WSL Git signing.**

   From WSL:

   ```bash
   git config --global gpg.format ssh
   git config --global user.signingkey "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com"
   git config --global gpg.ssh.program "/mnt/c/Windows/System32/OpenSSH/ssh-keygen.exe"
   git config --global commit.gpgsign true
   ```

3. **Keep Git SSH authentication on Windows OpenSSH when the same WSL
   environment pushes to the provider.**

   ```bash
   git config --global core.sshCommand ssh.exe
   ```

4. **Create and verify a signed commit.**

   ```bash
   git commit -S -m "Test Bitwarden SSH signing"
   git log --show-signature -1
   ```

### Linux And macOS

1. **Enable Bitwarden Desktop SSH Agent.**

   Open Bitwarden Desktop, unlock the vault, and enable SSH Agent support.

2. **Copy the public signing key.**

   Use the public key from the Bitwarden SSH key item.

3. **Configure Git.**

   ```bash
   git config --global gpg.format ssh
   git config --global user.signingkey "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com"
   git config --global commit.gpgsign true
   ```

4. **Create and verify a signed commit.**

   ```bash
   git commit -S -m "Test Bitwarden SSH signing"
   git log --show-signature -1
   ```

## 1Password Desktop SSH Agent Signing

1Password can configure Git commit signing from the SSH key item. The generated
configuration sets `gpg.format=ssh`, `user.signingkey`, optional
`commit.gpgsign=true`, and the 1Password signer program when needed.

### Windows Native Git

1. **Enable the 1Password SSH Agent.**

   Open 1Password for Windows, unlock the account, and enable the SSH Agent in
   Developer settings.

2. **Use 1Password's commit-signing configuration.**

   Open the SSH key item in 1Password, choose **Configure Commit Signing**, and
   apply the global or repository-specific configuration.

3. **Register the public key with the provider as a signing key.**

   Use the provider settings in `Provider Signing Keys`.

4. **Inspect the effective Git config.**

   ```powershell
   git config --show-origin --get gpg.format
   git config --show-origin --get user.signingkey
   git config --show-origin --get gpg.ssh.program
   git config --show-origin --get commit.gpgsign
   ```

5. **Create and verify a signed commit.**

   ```powershell
   git commit -S -m "Test 1Password SSH signing"
   git log --show-signature -1
   ```

### WSL2 Using The 1Password Signer

1Password's WSL integration uses Windows OpenSSH for Git SSH authentication and
the 1Password WSL signer for commit signing.

1. **Configure Git SSH authentication for WSL.**

   ```bash
   git config --global core.sshCommand ssh.exe
   ```

2. **Copy the WSL signing snippet from 1Password.**

   On Windows, open the SSH key item in 1Password, choose **Configure Commit
   Signing**, select **Configure for Windows Subsystem for Linux (WSL)**, and
   copy the snippet into WSL `~/.gitconfig`.

3. **Confirm the signer path for current 1Password MSIX installations.**

   The current WSL signer path is:

   ```text
   /mnt/c/Users/Ada/AppData/Local/Microsoft/WindowsApps/op-ssh-sign-wsl.exe
   ```

   Replace `Ada` with the Windows account folder name. Regenerate the snippet
   from 1Password if Git still points to the older
   `/mnt/c/Users/Ada/AppData/Local/1Password/app/8/op-ssh-sign-wsl`
   path.

4. **Inspect the effective Git config.**

   ```bash
   git config --show-origin --get gpg.format
   git config --show-origin --get user.signingkey
   git config --show-origin --get gpg.ssh.program
   git config --show-origin --get commit.gpgsign
   ```

5. **Create and verify a signed commit.**

   ```bash
   git commit -S -m "Test 1Password SSH signing"
   git log --show-signature -1
   ```

### Linux And macOS

1. **Enable the 1Password SSH Agent.**

   Open 1Password, unlock the account, and enable the SSH Agent in Developer
   settings.

2. **Use 1Password's commit-signing configuration.**

   Open the SSH key item, choose **Configure Commit Signing**, and apply the
   global or repository-specific configuration.

3. **Register the public key with the provider as a signing key.**

   Use the provider settings in `Provider Signing Keys`.

4. **Create and verify a signed commit.**

   ```bash
   git commit -S -m "Test 1Password SSH signing"
   git log --show-signature -1
   ```

## Allowed Signers File

Provider verification happens after a commit is pushed. Local verification with
`git log --show-signature`, `git verify-commit`, or `git verify-tag` needs a
trusted signer list.

Git reads `gpg.ssh.allowedSignersFile` as a file of principals followed by SSH
public keys:

```text
user@example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com
```

The principal is usually the commit author email. Git treats the signature as
trusted only when the signing public key appears in the allowed signers file.

### Global Allowed Signers

1. **Create the file.**

   ```bash
   mkdir -p ~/.ssh
   touch ~/.ssh/allowed_signers
   chmod 600 ~/.ssh/allowed_signers
   ```

2. **Configure Git.**

   ```bash
   git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
   ```

3. **Add the trusted signer.**

   ```bash
   nano ~/.ssh/allowed_signers
   ```

   Example entry:

   ```text
   user@example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com
   ```

4. **Verify the latest commit.**

   ```bash
   git log --show-signature -1
   ```

### Repository Allowed Signers

Use a repository allowed signers file when the team wants the trusted signer
list to be reviewed with the repository.

1. **Create a tracked signer file.**

   ```bash
   touch .allowed_signers
   ```

2. **Configure the repository.**

   ```bash
   git config --local gpg.ssh.allowedSignersFile .allowed_signers
   ```

3. **Add trusted signers.**

   ```text
   user@example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGRlbW9uc3RyYXRpb25LZXlGb3JEb2N1bWVudHM= user@example.com
   ```

4. **Verify configuration origin.**

   ```bash
   git config --show-origin --get gpg.ssh.allowedSignersFile
   git log --show-signature -1
   ```

## Per-Repository Identity

Repository-local identity prevents work and personal signing keys from crossing
accounts.

Inside a work repository:

```bash
git config --local user.name "Ada Lovelace"
git config --local user.email "ada@company.example"
git config --local gpg.format ssh
git config --local user.signingkey ~/.ssh/ada_company_signing.pub
git config --local commit.gpgsign true
```

Inspect all signing settings:

```bash
git config --show-origin --get user.name
git config --show-origin --get user.email
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git config --show-origin --get gpg.ssh.program
git config --show-origin --get commit.gpgsign
git config --show-origin --get gpg.ssh.allowedSignersFile
```

## Signing Commands

Create one signed commit:

```bash
git commit -S -m "Add signed commit"
```

Create signed commits by default:

```bash
git config --local commit.gpgsign true
git commit -m "Add signed commit"
```

Create one unsigned commit when automatic signing is enabled:

```bash
git commit --no-gpg-sign -m "Temporary unsigned commit"
```

Sign the latest commit again after changing signing config:

```bash
git commit --amend --no-edit -S
```

Create a signed tag:

```bash
git tag -s v1.0.0 -m "Release v1.0.0"
```

## Troubleshooting

### `unsupported value for gpg.format: ssh`

Upgrade Git to 2.34 or newer:

```bash
git --version
```

### `gpg.ssh.allowedSignersFile needs to be configured and exist`

Create and configure the allowed signers file:

```bash
mkdir -p ~/.ssh
touch ~/.ssh/allowed_signers
chmod 600 ~/.ssh/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
```

### Provider Shows `Unverified`

Check the provider account:

```bash
git config --show-origin --get user.email
git config --show-origin --get user.signingkey
```

The commit author email must be verified on the provider account. The public
key configured as `user.signingkey` must be registered as a signing key for
that provider account.

### Git Signs With The Wrong Identity

Inspect local overrides:

```bash
git config --show-origin --get user.email
git config --show-origin --get user.signingkey
git config --show-origin --get commit.gpgsign
```

Unset incorrect repository values from inside the repository:

```bash
git config --local --unset user.signingkey
git config --local --unset gpg.ssh.program
git config --local --unset commit.gpgsign
```

Then add the intended repository-local values.

### Bitwarden Does Not Prompt During Signing

Check the signing program and key:

```bash
git config --show-origin --get gpg.ssh.program
git config --show-origin --get user.signingkey
```

On Windows, `gpg.ssh.program` should point to:

```text
C:/Windows/System32/OpenSSH/ssh-keygen.exe
```

On WSL2 with the Windows Bitwarden route, it should point to:

```text
/mnt/c/Windows/System32/OpenSSH/ssh-keygen.exe
```

Confirm Bitwarden Desktop is unlocked and its SSH Agent is enabled.

### 1Password WSL Signing Cannot Run The Signer

Inspect the signer path:

```bash
git config --show-origin --get gpg.ssh.program
```

Current MSIX installations should use:

```text
/mnt/c/Users/Ada/AppData/Local/Microsoft/WindowsApps/op-ssh-sign-wsl.exe
```

If Git points to the older 1Password app-data path, regenerate the WSL snippet
from 1Password and replace the old config.

### `No principal matched`

Check the commit author email and allowed signers entry:

```bash
git config --show-origin --get user.email
cat ~/.ssh/allowed_signers
git log --show-signature -1
```

The principal before the public key in `allowed_signers` should match the
commit author identity used by Git.

## Final Verification

Run the checks from the repository where signing is configured:

```bash
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git config --show-origin --get commit.gpgsign
git commit -S -m "Verify SSH commit signing"
git log --show-signature -1
```

Push the commit and inspect the provider commit view. The provider should show
the signed or verified indicator for the commit.
