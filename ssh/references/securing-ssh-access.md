# Critical Infrastructure SSH Access

## 1. Define scope

1. Identify every host, account, repository, runner, key, owner, and requested change.
2. Classify each key as personal, operator, deploy, machine, or emergency.
3. Record the public-key fingerprint, purpose, scope, storage location, installation location, review date, and removal path.
4. Do not use shared human keys.

## 2. Inspect read-only state

1. Inventory existing authorized keys and provider keys.
2. Map each key to an owner and purpose.
3. Identify expired, orphaned, duplicate, overbroad, or unexplained keys.
4. Inspect effective SSH server configuration with a permitted read-only command.
5. Do not change access during the audit phase.

## 3. Plan changes

1. List every key to add, restrict, rotate, or remove.
2. List every account, service, firewall, and server configuration change.
3. Define the verification and rollback path.
4. Obtain explicit authorization for each privileged or access-removal operation.
5. Preserve a working administrative session during server changes.

## 4. Apply minimum controls

1. Use named accounts.
2. Disable direct root access unless a documented emergency exception requires it.
3. Disable password authentication only after key access is verified for every required operator.
4. Restrict agent forwarding, port forwarding, X11 forwarding, source addresses, and commands by default.
5. Use a bastion or management network for private infrastructure.
6. Give deploy and machine keys the narrowest repository and host scope.
7. Keep signing keys separate from deployment keys.

## 5. Validate server changes

1. Validate the configuration syntax with the platform's supported command.
2. Do not reload or restart SSH without explicit user authorization and permitted command access.
3. Test new access from a separate session.
4. Confirm old access remains available until replacement access passes.
5. Roll back through the approved path when verification fails.

## 6. Rotate or remove access

1. Create and install the replacement public key.
2. Verify replacement access.
3. Remove the exact old public key only after explicit authorization.
4. Verify the old key no longer works.
5. Update the inventory and evidence.
6. Remove password-manager access and provider membership when offboarding requires it.

## 7. Handle suspected compromise

1. Preserve evidence.
2. Identify the exact key, account, host, and reachable secrets.
3. Obtain the authority required for access revocation, account disablement, session termination, and secret rotation.
4. Revoke the narrowest exact target first.
5. Rotate dependent credentials within the approved incident scope.
6. Record timestamps, commands, fingerprints, and verification results.

## 8. Verify the final state

1. Confirm every installed key has an inventory record.
2. Confirm every removed key is absent.
3. Confirm every required operator and automation path works.
4. Confirm restricted keys cannot exceed their assigned scope.
5. Confirm review and rotation dates are recorded.
6. Confirm no private key material entered the repository or report.
