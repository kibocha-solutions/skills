# Commit Message Examples

Contrasting accepted and rejected commit message examples across common workflow constraints.

## One commit for four completed tasks

Constraint: one final commit.

Accepted:

```text
refactor(governance): enforce repository operating standards

Consolidate rule authority, verification gates, dependency handling, publication safeguards, and package structure into one enforceable workflow.
```

Rejected:

```text
chore(repo): update several files

- Rewrite AGENTS.md
- Update ci-cd/SKILL.md
- Delete pptx-master/
- Add upload packaging
```

## Two authorized commits

Constraint: two final commits.

Accepted first message:

```text
fix(auth): enforce session expiration

Reject expired sessions and clear stale credentials during logout.
```

Accepted second message:

```text
test(auth): cover expired-session handling

Exercise refresh rejection, logout cleanup, and authenticated request failure.
```

## User-specified body limit

Constraint: body of 12 words or fewer.

Accepted:

```text
fix(auth): enforce session expiry

Reject expired sessions and clear stale credentials during logout.
```

## Single-purpose condensation

Constraint: one final commit for configuration cleanup, validation changes, dependency handling, and package removal.

Accepted:

```text
refactor(tooling): standardize repository execution controls

Unify configuration, validation, dependency handling, and package boundaries under the supported operating model.
```

## Written for a new reader

Accepted:

```text
fix(payments): extend retry duration for gateway timeouts

Increase transaction timeout threshold and retry attempts to prevent premature request drops during upstream payment processor latency spikes.
```

Rejected:

```text
fix(payments): fix payment bug for customer

First I modified the retry function in gateway.py, changed timeout from 5 to 10 seconds, added error log, and tested with sandbox account.
```
