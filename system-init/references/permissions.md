# Privileged Command Scope

## 1. Inspect

1. Run `sudo -n -l`.
2. Treat its output as the live authority for available privileged commands.
3. Record exact executable paths, allowed arguments, run-as identity, and password requirements.
4. Do not infer permission from group membership, documentation, or a prior machine state.

## 2. Reject broad grants

Do not accept these as scoped agent grants:

1. Shells.
2. General interpreters.
3. Editors with shell escapes.
4. Unrestricted file-copy or file-deletion commands.
5. Wildcard privileged paths.
6. Unrestricted service, firewall, disk, mount, account, or permission management.
7. Package-manager grants presented as safe by command name alone.

## 3. Use exact file editing

1. Require an exact file path in the live sudoers grant.
2. Use `sudoedit <exact-path>`.
3. Do not use `sudo nano`, `sudo vim`, `sudo sed`, or a privileged interpreter.
4. Validate the resulting configuration with its dedicated checker.
5. Keep a rollback copy only when the user authorized it and the target policy permits it.

## 4. Use package managers

1. Apply the qualifying-installation gate in `AGENTS.md`.
2. Use trusted configured repositories.
3. Do not use arbitrary configuration overrides or pre-invoke hooks.
4. Do not install an untrusted local package.
5. Do not use flags that bypass signature or confinement controls.
6. Do not add or replace package sources unless the current task separately
   requires that change.

## 5. Handle a missing or excessive grant

1. Report the exact mismatch.
2. Prepare a candidate least-privilege rule in the workspace when the user requests it.
3. Do not install or broaden the sudoers grant through an unlisted route.
4. Require an authorized administrator to apply a new grant through the platform's validated sudoers workflow.
5. Re-run `sudo -n -l` after the administrator's change.

## 6. Stop on denial

1. Record the exact command and error.
2. Stop the privileged action.
3. Do not retry with another command, flag, shell, interpreter, or service path.
4. Ask the user for the required authority or an operator-run action.
