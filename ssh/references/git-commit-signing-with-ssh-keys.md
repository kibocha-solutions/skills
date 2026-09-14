# SSH Commit Signing

## 1. Inspect

```bash
git --version
ssh -V
git config --show-origin --get user.name
git config --show-origin --get user.email
git config --show-origin --get gpg.format
git config --show-origin --get user.signingkey
git config --show-origin --get gpg.ssh.program
git config --show-origin --get gpg.ssh.allowedSignersFile
git config --show-origin --get commit.gpgsign
```

1. Require a Git version that supports SSH signing.
2. Identify the author identity, signing key, signing program, and config scope.
3. Preserve working authentication settings.

## 2. Select a signing key

1. Use a local key or a verified password-manager signing route.
2. Generate a key only after explicit user authorization.
3. Register only the public key with the Git provider.
4. Use a separate signing key when access and signing require separate rotation.
5. Verify password-manager signer paths from the installed application.

## 3. Configure Git

```bash
git config --local gpg.format ssh
git config --local user.signingkey <public-key-path-or-public-key>
git config --local commit.gpgsign true
```

1. Prefer repository-local settings when identities differ by repository.
2. Set `gpg.ssh.program` only when the selected route requires a non-default signer.
3. Do not invent a password-manager signer path.
4. Do not disable signing to make another Git operation pass.

## 4. Configure local trust

1. Create an allowed signers file when local signature verification is required.
2. Add one principal and public key per trusted signer.
3. Match the principal to the intended author identity.
4. Protect a personal signer file with owner-only permissions.
5. Review a repository signer file like source code.
6. Configure `gpg.ssh.allowedSignersFile` at the intended scope.

## 5. Verify

1. Verify an existing signed commit with `git log --show-signature -1`.
2. Use `git verify-commit <commit>` for a named commit.
3. Create or amend a commit only when the user authorized that Git change.
4. Confirm the provider recognizes the signing key after an authorized push.
5. Diagnose an unverified signature by checking author email, public key, signer program, and allowed principal.

## 6. Stop conditions

1. Stop when the signer executable does not exist.
2. Stop when the configured key does not match the intended identity.
3. Stop before unsetting existing signing values without user authorization.
4. Report the exact configuration origin and failing command.
