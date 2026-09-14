# Repository Health Cache

## Location

```text
.agents/brain/git/
  repo-health.json
  branch-ancestry.json
  archives/
    YYYY-MM-DD-HHMM-repo-health.json
```

## Snapshot procedure

1. Check `.agents/brain/git/repo-health.json`.
2. Confirm `schema_version`, `stale`, `branch`, and `captured_at`.
3. Use the snapshot only when `stale` is false and `branch` matches the current branch.
4. Archive an invalid or stale snapshot before replacement.
5. Write the replacement atomically.
6. Keep `branch-ancestry.json` append-only.
7. Keep the project `.agents/` convention and ignore policy unchanged.

## Snapshot schema

```json
{
  "schema_version": 1,
  "captured_at": "ISO-8601 timestamp",
  "branch": "current branch",
  "identity": {
    "user_name": "configured name or null",
    "user_email": "configured email or null"
  },
  "commit_pattern": {
    "minimum_full_commits": 2,
    "full_log_command": "git log --show-signature -2 --date=iso-strict --format=fuller",
    "entries": [
      {
        "raw": "complete commit record"
      }
    ],
    "inferred_convention": "conventional-commits | custom | unknown"
  },
  "remote": {
    "configured": true,
    "name": "origin",
    "url": "remote URL",
    "ssh_host": "remote host",
    "ssh_host_alias": "host alias or null",
    "uses_default_identity": true,
    "auth_handshake_ok": true
  },
  "ssh_signing_path": {
    "path": "bitwarden-windows | onepassword | onepassword-wsl | local-key | unknown",
    "evidence": [],
    "requires_user_action": false
  },
  "provider_cli": {
    "provider": "github | gitlab | other | none",
    "cli": "gh | glab | null",
    "installed": true,
    "authenticated": true,
    "auth_checked_at": "ISO-8601 timestamp or null",
    "preferred_for_remote_operations": true
  },
  "signing": {
    "gpg_format": "ssh | gpg | x509 | null",
    "signing_key": "key value or null",
    "allowed_signers_file": "path or null",
    "signing_expected": true,
    "signing_intentionally_disabled": false
  },
  "branch_ancestry": {
    "current": "current branch",
    "trunk": "resolved trunk",
    "chain": ["trunk", "parent", "current"],
    "chain_source": "log | reflog | fork-point | upstream-tracking | user-confirmed | unknown"
  },
  "stale": false
}
```

## Field rules

### Identity

- Stop before committing when `user_name` or `user_email` is null.
- Do not change Git identity without user authorization.

### Commit pattern

- Store at least two complete commit records.
- Include signatures, author, committer, dates, subject, and body.
- Set `conventional-commits` only when the sample establishes that format.
- Set `custom` for another consistent convention.
- Set `unknown` for sparse or inconsistent evidence.

### Remote

- Record the configured remote without changing it.
- Extract the SSH host or alias from the actual URL.
- Test authentication only when the user-authorized operation requires it.
- Preserve non-default host aliases.
- Do not replace an alias with the provider hostname.

### SSH and signing

- Read the SSH skill before changing SSH or signing state.
- Record configuration and environment evidence.
- Set the path to `unknown` when the evidence is inconclusive.
- Keep `signing_expected` true unless controlling project policy states otherwise.
- Set `signing_intentionally_disabled` only from express user authorization.

### Provider CLI

- Record installation separately from authentication.
- Set `authenticated` true only after the provider status command succeeds.
- Use the authenticated provider CLI for provider-native operations when the user authorizes the operation.

### Derived ancestry

- Derive the current chain from `branch-ancestry.json`.
- Recompute the field after a branch switch or new branch.
- Do not write derived snapshot state back into the ancestry log.

## Branch ancestry log

Schema:

```json
{
  "schema_version": 1,
  "entries": [
    {
      "branch": "child",
      "parent": "parent",
      "recorded_at": "ISO-8601 timestamp",
      "source": "agent-created | discovered-reflog | discovered-fork-point | discovered-upstream-tracking | user-confirmed"
    }
  ]
}
```

Rules:

1. Append an entry immediately after creating a branch.
2. Backfill a missing branch only after resolving its parent.
3. Use reflog, upstream tracking, fork-point, and user confirmation in that order.
4. Ask the user when evidence remains ambiguous.
5. Never edit or delete a past entry.
6. Append a new entry when a branch name is reused.
7. Derive a live chain from the most recent entry for each branch name.
8. Stop traversal at the resolved trunk.

## Discovery commands

```bash
git branch --show-current
git symbolic-ref refs/remotes/origin/HEAD
git reflog show <branch>
git rev-parse --abbrev-ref --symbolic-full-name <branch>@{upstream}
git merge-base --fork-point <candidate-branch> <branch>
git config user.name
git config user.email
git log --show-signature -2 --date=iso-strict --format=fuller
git remote -v
git config core.sshCommand
git config gpg.ssh.program
git config gpg.format
git config user.signingkey
git config gpg.ssh.allowedSignersFile
```

Run only commands within the authorized task scope.

## Staleness triggers

Archive and replace the snapshot after:

- branch switch
- remote addition, removal, or URL change
- SSH host or alias change
- SSH or signing path change
- provider CLI installation, removal, login, logout, or account change
- signing configuration change
- Git identity change
- explicit refresh request
- creation of a child branch

Do not archive or replace `branch-ancestry.json`.

## Archive procedure

1. Set the old snapshot `stale` value to true.
2. Move it to `archives/YYYY-MM-DD-HHMM-repo-health.json`.
3. Write the new active snapshot.
4. Validate both JSON files.
5. Confirm the active branch matches the snapshot.

## Final checks

- [ ] Active snapshot parses.
- [ ] Snapshot branch matches the current branch.
- [ ] Full commit evidence is present.
- [ ] Identity is resolved before committing.
- [ ] Remote and alias match the configured URL.
- [ ] Signing status reflects current evidence.
- [ ] Provider authentication was checked only when needed.
- [ ] Branch ancestry remains append-only.
- [ ] Stale snapshots remain recoverable.
