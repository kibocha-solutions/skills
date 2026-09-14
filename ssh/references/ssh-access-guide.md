# SSH Access

## 1. Inspect the client route

1. Run `ssh -V`.
2. Run `type -a ssh` and `type -a ssh-add`.
3. Run `ssh-add -L`.
4. Identify the active SSH config path.
5. Identify whether a local file, operating-system agent, Bitwarden, or 1Password owns the private key.
6. Verify vendor-specific paths against the installed application or current official documentation.

## 2. Configure a host alias

```sshconfig
Host <alias>
    HostName <host>
    User <account>
    Port 22
    IdentitiesOnly yes
```

1. Add `IdentityFile` only after identifying the correct key or public-key marker.
2. Add `IdentityAgent` only after verifying the active socket.
3. Add `ProxyJump` only for an approved bastion route.
4. Add `ForwardAgent yes` only for a named host with a verified need.
5. Validate the resolved configuration with `ssh -G <alias>`.

## 3. Generate a key

Perform this section only after the user explicitly requests key generation.

1. Select Ed25519 unless the target requires another supported type.
2. Use a unique path and identifying comment.
3. Use a passphrase for a human-operated key.
4. Protect the private key with owner-only permissions.
5. Share only the `.pub` content.
6. Record the public-key fingerprint.

## 4. Install a public key

1. Confirm the target account and host.
2. Confirm the exact public key and fingerprint.
3. Preserve existing `authorized_keys` entries.
4. Add a clear owner and purpose comment.
5. Apply server-side restrictions required by the key's purpose.
6. Verify directory and file permissions.
7. Test in a separate session before closing working access.

## 5. Transfer files

1. Use `scp` for a small bounded transfer.
2. Use `sftp` for interactive transfer.
3. Use `rsync` for repeatable synchronization.
4. Do not use deletion flags without explicit user authorization.
5. Verify the destination path and transferred file hashes when integrity matters.

## 6. Create a tunnel

1. Confirm the local port, remote address, remote port, and target host.
2. Use local forwarding for a remote service exposed on the workstation.
3. Use remote forwarding only with explicit authorization.
4. Bind forwarded ports to loopback unless broader exposure is required.
5. Verify the listening address and target service.

## 7. Diagnose

1. Run `ssh -vvv <alias>`.
2. Identify the config file, resolved host, offered keys, accepted key, and final failure.
3. Use `IdentitiesOnly yes` for excess key offers.
4. Compare the offered public key with the installed key.
5. Inspect a stored host key with `ssh-keygen -F <host>`.
6. Remove a stored host key only after independently verifying an authorized host-key change.
7. Do not bypass verification with permissive host-key options.

## 8. Verify

1. Run a harmless remote command that prints the remote account and hostname.
2. Confirm the result matches the intended target.
3. Record the alias and public-key fingerprint.
