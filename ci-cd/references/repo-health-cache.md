# Repo Health Cache

This reference covers the schema, location, staleness triggers, and archive
rules for the repo health snapshot used by the ci-cd skill.

---

## Cache Location

```
<project-root>/
  .agents/
    brain/
      git/
        repo-health.json       ← current active snapshot
        archives/
          YYYY-MM-DD-HHMM-repo-health.json   ← stale snapshots
```

The `.agents/` tree is project-local. It is not committed (list it in
`.gitignore` if not already excluded). The `archives/` directory holds
snapshots that have been superseded; the agent writes a new archive entry
before overwriting the active file, so the history of health state is
recoverable if needed.

---

## Schema — `repo-health.json`

```json
{
  "schema_version": 1,
  "captured_at": "ISO-8601 timestamp",
  "branch": "name of the branch at capture time",
  "identity": {
    "user_name": "value from git config user.name, or null if absent",
    "user_email": "value from git config user.email, or null if absent"
  },
  "commit_pattern": {
    "sample": [
      "short-sha subject author",
      "..."
    ],
    "inferred_convention": "conventional-commits | custom | unknown"
  },
  "remote": {
    "configured": true,
    "name": "origin",
    "url": "git@github.com:org/repo.git",
    "auth_handshake_ok": true
  },
  "signing": {
    "gpg_format": "ssh | gpg | x509 | null",
    "signing_key": "key value or null",
    "allowed_signers_file": "path or null",
    "signing_expected": true,
    "signing_intentionally_disabled": false
  },
  "stale": false
}
```

### Field notes

**`identity`** — if either `user_name` or `user_email` is `null`, the agent
must halt before any commit and instruct the user to run `git config
--global user.name "..."` and `git config --global user.email "..."` (or the
local variant if the repo uses a per-repo identity). Do not attempt a commit
with a null identity field.

**`commit_pattern.inferred_convention`** — derived from the subject lines of
the sampled commits. Set to `conventional-commits` only when the majority of
subjects clearly follow `type(scope): summary` format. Set to `custom` when
the repo uses a recognisable but non-standard convention. Set to `unknown`
when the sample is too sparse or inconsistent to classify. The ci-cd skill
always uses Conventional Commits for new commits regardless of this field;
the field is informational, used to assess whether the repo history is
consistent with what the skill produces.

**`signing.signing_expected`** — defaults to `true` on every fresh snapshot.
The absence of signing configuration in `gpg_format` or `signing_key` does
not change this default; instead it triggers a pre-commit clarification
prompt.

**`signing.signing_intentionally_disabled`** — the agent never sets this field
to `true` unilaterally. It is set only after the user explicitly confirms, in
the current session, that unsigned commits are acceptable. This confirmation
must be re-obtained in each new session unless the user has set it as a
persistent project policy and that policy is documented in this file under a
`policy` key.

**`remote.auth_handshake_ok`** — populated by running `ssh -T git@<host>`. A
`false` value here means push attempts will fail regardless of commit signing
status; the agent should address connectivity before attempting a push.

---

## Commands to Populate Each Field

```bash
# Identity
git config user.name
git config user.email

# Commit pattern (last 20 commits)
git log --oneline -20 --format="%h %s %an"

# Remote
git remote -v
ssh -T git@github.com   # or the appropriate host

# Signing
git config gpg.format
git config user.signingkey
git config gpg.ssh.allowedSignersFile
```

---

## Staleness Triggers

Mark the current snapshot as stale and archive it when any of the following
occur during the active session:

- The agent switches branches (run `git switch` or `git checkout`).
- A remote is added, removed, or its URL is changed.
- The `gpg.format`, `user.signingkey`, or `allowedSignersFile` config is
  modified.
- The `user.name` or `user.email` config is modified.
- The agent explicitly requests a cache refresh (e.g. after the user reports
  that their SSH agent is now loaded).

A stale snapshot is **never deleted** — it is moved to `archives/` before
the replacement is written. Use the `captured_at` timestamp in the filename:

```
archives/2026-07-01-0045-repo-health.json
```

---

## Read-Before-Write Rule

On every invocation that involves a commit, branch switch, or push:

1. Check whether `repo-health.json` exists and `stale` is `false`.
2. If valid, read from it — do not re-run all discovery commands.
3. If absent, stale, or if the `branch` field does not match the current
   branch, archive the old file (if any) and write a fresh snapshot.

This prevents repeated expensive `ssh -T` and `git log` calls on every
agent turn within the same session.
