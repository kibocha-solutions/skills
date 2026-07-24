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
        repo-health.json          ← current active snapshot
        branch-ancestry.json      ← durable, append-only branch-creation log
        archives/
          YYYY-MM-DD-HHMM-repo-health.json   ← stale snapshots
```

The `.agents/` tree is project-local. It is not committed (list it in
`.gitignore` if not already excluded). The `archives/` directory holds
snapshots that have been superseded; the agent writes a new archive entry
before overwriting the active file, so the history of health state is
recoverable if needed.

`branch-ancestry.json` is not a snapshot and does not follow the
archive-and-replace lifecycle described above — see Branch Ancestry Log below.
It only ever grows.

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
    "minimum_full_commits": 2,
    "full_log_command": "git log --show-signature -2 --date=iso-strict --format=fuller",
    "entries": [
      {
        "raw": "commit <full-sha>\ngood signature lines when present\nAuthor: ...\nAuthorDate: ...\nCommit: ...\nCommitDate: ...\n\n    type(scope): subject\n\n    Body text when present."
      }
    ],
    "inferred_convention": "conventional-commits | custom | unknown"
  },
  "remote": {
    "configured": true,
    "name": "origin",
    "url": "git@github.com:org/repo.git",
    "ssh_host": "github.com",
    "ssh_host_alias": "github.com | alias | null",
    "uses_default_identity": true,
    "auth_handshake_ok": true
  },
  "ssh_signing_path": {
    "path": "bitwarden-windows | onepassword | onepassword-wsl | local-key | unknown",
    "evidence": [
      "core.sshCommand=ssh.exe",
      "gpg.ssh.program=...",
      "SSH_AUTH_SOCK=...",
      "ssh.exe installed=true",
      "ssh-add.exe installed=true"
    ],
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
    "current": "name of the branch at capture time",
    "trunk": "main | master | other resolved trunk name",
    "chain": ["main", "dev", "feat/db"],
    "chain_source": "log | reflog | fork-point | upstream-tracking | user-confirmed | unknown"
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

**`commit_pattern.entries`** — stores at least two recent full commit records,
not a one-line summary. Capture the exact raw output from
`git log --show-signature -2 --date=iso-strict --format=fuller` or a wider
equivalent. The record must include signature verification output when present,
full author and committer identities, full dates, subject, and body. This gives
the later agent enough evidence to understand commit style, body conventions,
authorship, chronology, and signature status before it commits. Do not replace
this with `git log --oneline`.

**`commit_pattern.inferred_convention`** — derived from the full commit records.
Set to `conventional-commits` only when the majority of subjects clearly follow
`type(scope): summary` format. Use the bodies to infer whether the repo expects
commit bodies and how much operational detail belongs there. Set to `custom`
when the repo uses a recognisable but non-standard convention. Set to
`unknown` when the sample is too sparse or inconsistent to classify. The ci-cd
skill always uses Conventional Commits for new commits regardless of this
field; the field is informational, used to assess whether the repo history is
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

**`remote.ssh_host_alias`** — records the host portion used in the remote URL.
`git@github.com:owner/repo.git` belongs to the default cached identity. A
non-default identity must use an SSH host alias such as
`git@sahil:owner/repo.git`; do not substitute `github.com` for an alias during
push or authentication tests.

**`ssh_signing_path`** — records which SSH authentication and commit-signing
path the repo is using. Populate this from Git config, environment variables,
installed tools, and SSH config before repair. If the evidence cannot
distinguish Bitwarden, 1Password, or local keys, set `path` to `unknown` and
ask the user before changing sockets, Git config, SSH config, remotes, or
signing files.

**`provider_cli`** — records whether the remote host has a usable local CLI.
For GitHub, check `command -v gh` and `gh auth status`. For GitLab, check
`command -v glab` and the matching auth status command. `installed: true` is
not enough; set `authenticated: true` only after the auth check succeeds. When
the CLI is installed and authenticated, prefer it for provider-native push,
pull request, review, and merge-queue operations where it fits the task.

**Authorization note** — all `git`, `gh`, `glab`, remote authentication, and
repo-write commands should be treated as needing elevated authorization at the
start of the operation. Do not spend an attempt on a sandboxed Git command
when the operation is predictably blocked by sandbox boundaries.

**`branch_ancestry`** — a lightweight, disposable cache of the *derived*
chain for the current branch, kept only for fast reads. It follows the same
staleness lifecycle as the rest of this snapshot (invalidated on branch
switch, like every other field here). It is not the source of truth: the
durable record lives in `branch-ancestry.json` (see Branch Ancestry Log
below), and this field is always recomputed from that log, never the other
way around. `chain_source: "log"` means the chain came directly from existing
log entries with no fresh discovery needed.

---

## Branch Ancestry Log

`branch-ancestry.json` is a separate, append-only file recording when each
branch was created and what its parent was — a durable trace ("last month we
branched to `dev`, last week further to `feat/db`"), not a point-in-time
snapshot. It is never archived, overwritten, or pruned; entries are only ever
added.

### Schema — `branch-ancestry.json`

```json
{
  "schema_version": 1,
  "entries": [
    {
      "branch": "dev",
      "parent": "main",
      "recorded_at": "ISO-8601 timestamp",
      "source": "agent-created | discovered-reflog | discovered-fork-point | discovered-upstream-tracking | user-confirmed"
    }
  ]
}
```

### Rules

- **Append on creation.** When the agent creates a new branch, add an entry
  immediately: `branch`, its `parent`, the current timestamp, and
  `source: "agent-created"`.
- **Backfill on first encounter.** When the agent starts work on a
  pre-existing branch that has no entry yet, resolve its parent using the
  discovery order in `SKILL.md`'s Branch Ancestry Discovery section (reflog,
  upstream tracking, `git merge-base --fork-point`, or asking the user), then
  append an entry recording however it was resolved. This is how history gets
  backfilled for branches that predate this log.
- **Never edit or delete a past entry.** Even after a branch is deleted or
  merged, its entry stays — it is a historical record of what happened, not
  live branch state. Do not "clean up" entries for branches that no longer
  exist.
- **Branch name reuse is a known rough edge.** If a branch name is deleted and
  later recreated, append a new entry rather than overwriting the old one;
  `recorded_at` ordering is what disambiguates the two epochs. This is not
  fully solved — avoid reusing branch names where practical instead of relying
  on the log to disambiguate perfectly.
- **Deriving the live chain.** To get the current chain for a branch, walk
  the log from that branch's most recent entry, follow `parent` pointers
  through each parent's most recent entry, until reaching a branch with no
  entry (trunk). This derived result is what gets cached in
  `repo-health.json`'s `branch_ancestry` field.

### Commands Supporting Discovery

```bash
# Current branch
git branch --show-current

# Resolve trunk name
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null   # strip "origin/" prefix
# fall back to checking for local `main` then `master` if the above is unset

# Reflog evidence of where a branch was created from (local-creation only)
git reflog show <branch> | grep -i "branch: Created from"

# Upstream/tracking branch
git rev-parse --abbrev-ref --symbolic-full-name <branch>@{upstream} 2>/dev/null

# Fork-point against a candidate ancestor (requires the candidate's reflog;
# fails inconclusively on a fresh clone or after `git gc` — treat failure as
# "unresolved," not "no parent")
git merge-base --fork-point <candidate-branch> <branch>
```

If none of these resolve unambiguously, or two candidates are equally
plausible, stop and ask the user to confirm the chain rather than guessing.
Cache whatever is resolved — including a user-confirmed answer — as a new log
entry so it does not need to be re-derived later.

---

## Commands to Populate Each Field

```bash
# Identity
git config user.name
git config user.email

# Commit pattern (minimum two full records)
git log --show-signature -2 --date=iso-strict --format=fuller

# Remote
git remote -v
ssh -T git@github.com   # or the appropriate host

# SSH and signing path
git config core.sshCommand
git config gpg.ssh.program
printf 'SSH_AUTH_SOCK=%s\n' "$SSH_AUTH_SOCK"
command -v op-ssh-sign-wsl.exe
command -v ssh.exe
command -v ssh-add.exe

# Provider CLI
command -v gh
gh auth status
command -v glab
glab auth status

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
- The remote host changes between `github.com` and an SSH host alias.
- The active SSH/signing path changes between Bitwarden, 1Password, or local
  keys.
- The provider CLI is installed, removed, authenticated, logged out, or
  changes account.
- The `gpg.format`, `user.signingkey`, or `allowedSignersFile` config is
  modified.
- The `user.name` or `user.email` config is modified.
- The agent explicitly requests a cache refresh (e.g. after the user reports
  that their SSH agent is now loaded).
- A new branch is created off the current one, extending the chain.

These triggers apply to `repo-health.json`, including its derived
`branch_ancestry` field. `branch-ancestry.json` itself is exempt from this
entire lifecycle — it is never marked stale, archived, or replaced; it only
gains new entries over time.

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
