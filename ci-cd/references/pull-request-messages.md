# Pull Request Messages

Use this reference when writing or reviewing a pull request description.
These standards apply to all PRs opened from work managed under this skill.
They are grounded in established industry practice and layered with
project-specific constraints that take precedence where they differ.

> Pull request descriptions are not commit messages. A commit message
> records what changed and why at the code level, within the constraints
> of the commit format. A PR description communicates the intent, impact,
> and context of a set of changes to a reviewer who may not have followed
> the day-to-day work. They serve different readers and should be written
> accordingly.

---

## Required Sections

A PR description is incomplete without all of the following. Omit a section
only when it genuinely does not apply (for example, a pure-documentation PR
has no rollback concern) and note the omission explicitly rather than leaving
the section blank.

### Title

The title follows the same Conventional Commits convention as the skill's
commit format: `type(scope): summary`. It should name the specific change
without restating it in a vague generalisation. A title like
`feat(auth): add email-based MFA to the login flow` is useful; a title like
`feat: improve authentication` tells the reviewer almost nothing before they
open the diff.

### Summary

State what this PR does and what user-facing or operator-facing outcome it
produces. Write for the reviewer who is about to approve this for production,
not for someone who has been following the branch since day one. The summary
is the right place to surface the change's scope: whether it is a narrow
targeted fix, a broad refactor, or the final leg of a multi-PR feature.

### Context and Motivation

Explain why the change is being made. Link to the issue, ticket, or
architectural decision that prompted it. If the change addresses a specific
failure mode or a known gap in the previous implementation, describe that
failure mode clearly so the reviewer understands what the old behaviour was
and why it was insufficient. If there were alternative approaches considered,
name them briefly and explain what ruled them out — this prevents the review
from relitigating decisions that were already made.

### What Changed

Describe the high-level technical approach: which components were touched,
what the key structural decisions were, and where the boundary of this PR
ends. The diff answers *exactly* what changed line by line; this section
answers *why the implementation looks the way it does*. Do not reproduce the
diff in prose. Do not list files. Focus on decisions that are not obvious
from the code.

### Testing Plan

Describe how the change was verified. Name the specific tests added or
modified and what they cover. If the change requires manual verification,
give the reviewer precise steps they can follow to reproduce the happy path
and any edge cases that were tested. If CI runs relevant checks automatically,
note which jobs validate this change and whether any new checks were added.
A testing plan that says only "CI passes" is not sufficient when the change
touches production behaviour.

### Risk and Rollback

Identify what could go wrong and how to recover. For changes that modify
data schemas, authentication flows, external integrations, or deployment
configuration, this section is never optional. State the rollback method
explicitly: revert the PR, run a migration reversal, toggle a feature flag,
or restore a previous artifact — whichever applies. If the risk is genuinely
low and the rollback is trivially "revert the merge commit," say so directly
rather than leaving the section absent.

### Screenshots and Recordings (UI changes only)

For any change that affects a user-visible interface, include at least one
screenshot of the relevant state before and after. A recording is preferable
when the change involves interactive behaviour such as animations, transitions,
or form flows. Text descriptions of visual changes are not a substitute.

---

## Title Format

```
type(scope): concise imperative summary
```

The same types used in commit messages apply here: `feat`, `fix`, `docs`,
`chore`, `refactor`, `test`, `ci`, `perf`, `build`. The scope names the
system or layer affected. The summary is written in the imperative mood
("add", "fix", "remove") and does not end with a period.

Good examples:
- `fix(auth): resolve session token expiry bypass on concurrent logins`
- `feat(ci): add artifact provenance attestation to the release workflow`
- `refactor(api): replace manual pagination with cursor-based implementation`

Avoid titles that are vague (`fix: update stuff`), that restate the type
redundantly (`fix(bug): fix a bug in auth`), or that name files instead of
intent (`feat: update auth.py and session.py`).

---

## Formatting Rules

Standard Markdown is available in full and its use is expected where it
improves clarity. Headings, code blocks, blockquotes, tables, and lists are
all appropriate tools. Use them deliberately.

- Use code blocks (` ``` `) for any commands, configuration snippets, error
  messages, or code excerpts that appear in the description. Inline
  backticks apply to short references like variable names or file paths.
- Use a table when comparing options, listing items with multiple attributes,
  or mapping inputs to expected outputs. A table communicates structure
  efficiently; a prose paragraph covering the same content is harder to scan.
- Use a blockquote (`>`) to distinguish a reviewer note, a caveat, or a
  quoted requirement from the main body of the description.
- Use headings only for the standard sections above or to break a long
  "What Changed" section into named sub-areas when the PR spans several
  independent components.

Lists are appropriate when the items genuinely form a collection. A list
item must carry enough context to stand on its own. A bare bullet like
"- Updated the auth module" without any explanation of what was updated,
why, or what the effect is offers the reviewer less than nothing — it implies
there is information while withholding it. Either expand the item to give it
substance or fold it into a prose paragraph.

---

## Tone and Language Rules

The following constraints take precedence over any external convention this
reference may cite.

**Prohibited:**

- Emojis in the PR title, section headings, or any structural position.
  Emojis in body prose are acceptable only if they carry meaning that plain
  text cannot convey as concisely, which in practice means almost never.
- Em dashes used decoratively or as a stylistic tic. An em dash that
  separates a clause where a comma or period would serve equally well is
  unnecessary. Em dashes used for genuine syntactic clarity (a genuine
  parenthetical that cannot be set off with commas) are not prohibited.
- Inflated language that overstates the change: words like "revolutionary",
  "seamless", "robust", "state-of-the-art", or "lightning-fast" belong in
  marketing copy, not in a PR description read by engineers evaluating a diff.
- Circular phrasing that references the review process itself: "as you can
  see in the diff", "this PR fixes the issue", "please review this change".
  Write about the code, not about the act of reviewing it.
- Fourth-wall breaks that address the reviewer as an audience: "I hope this
  is clear", "let me know if you have questions", "feel free to ask for
  clarification". These add length without adding information.

**Expected:**

- Plain, direct prose that states facts and reasoning. If the change is
  significant, say so by describing its significance, not by asserting that
  it is significant.
- Precise technical language over approximation. "Replaces the O(n²) nested
  loop with a hash-map lookup" is more useful than "improves performance."
- Honest acknowledgement of gaps, incomplete testing, or known limitations.
  A PR that documents its own rough edges builds more reviewer trust than one
  that presents every decision as settled.

---

## Anti-Patterns

These patterns appear in PR descriptions regularly and should be avoided.

A summary that restates the title without adding information wastes the
reviewer's first read before they have even reached the details. If the title
is `fix(session): resolve token expiry bypass`, a summary that says "This PR
fixes the session token expiry bypass issue" has contributed nothing.

A testing plan that only says "tested locally" or "CI passes" does not tell
the reviewer whether the relevant code paths were exercised. Local testing
and passing CI are the baseline expectation, not a testing plan.

A risk section that says "low risk" without explanation does not help a
reviewer who needs to sign off on production. Low risk means something: the
change is isolated, has a trivial rollback, does not touch shared state.
State what makes it low risk.

A "What Changed" section that lists file names instead of decisions ("Updated
`auth.py`, `session.py`, and `middleware.py`") tells the reviewer nothing
they could not read from the file list in the diff view. Use this section
to explain the reasoning, not to reproduce the manifest.

---

## Annotated Example

```markdown
## feat(auth): add email-based MFA to the login flow

### Summary

Adds a time-based one-time password (TOTP) step to the login flow for users
who have enrolled MFA. Users without MFA configured are unaffected and see no
change. This completes the MFA rollout tracked in issue #412.

### Context and Motivation

The previous login implementation validated credentials in a single step with
no second factor. Following the Q2 security review, MFA was listed as a
required control for all production accounts. TOTP was chosen over SMS-based
OTP because it does not depend on carrier reliability and avoids SIM-swap
risk. A hardware key option was considered but deferred pending procurement
of test devices.

### What Changed

The authentication middleware now performs a two-phase check: credential
validation followed by a TOTP verification step for enrolled accounts. The
TOTP library selected (RFC 6238-compliant) is isolated behind an interface
so that alternative second-factor implementations can be substituted later
without touching the middleware. The user enrolment flow is not part of this
PR; it was shipped in #398 and is already in production.

### Testing Plan

Unit tests cover the TOTP verification logic against known test vectors from
RFC 6238. Integration tests confirm that:
- an enrolled user who provides a valid TOTP proceeds to the authenticated
  session;
- an enrolled user who provides an expired or incorrect TOTP receives a 401
  and is not granted a session;
- a user without MFA enrolment bypasses the TOTP step entirely.

Manual testing was performed against the staging environment with a Bitwarden
TOTP entry. The CI `auth-integration` job validates these paths on every
push.

### Risk and Rollback

If the TOTP middleware causes unexpected failures in production, revert this
merge commit and redeploy. The TOTP check is additive — it wraps the existing
credential validation and does not modify the session token structure, so a
revert restores the previous login behaviour without a data migration.

Users currently mid-enrolment at the time of a rollback will see their
enrolment state preserved (it lives in a separate table untouched by this PR)
but the TOTP prompt will disappear until the fix is redeployed.
```
