---
name: commit-and-destructive-action-discipline
description: Validated standards for commit messages and for handling batch/irreversible actions across multiple repos
type: feedback
---

**Commit messages: single predominant scope, not diff-driven.** A commit
title takes exactly one scope, even when the diff spans several skills or
concerns — never a compound scope like `feat(a, b): ...`. Choose the scope
by asking "of everything in this diff, what is the one thing a maintainer
with no session context, reading this years from now, needs to know
happened" — not by which part of the diff is largest. The body is capped at
72 words, focused on the useful work behind that predominant change;
secondary or unrelated work swept into the same commit is expected to go
unmentioned, or at most gets one compressed closing sentence — never its own
paragraph, never a reason to split the commit. This is deliberately lossy: a
commit message is not documentation, and losing the itemization is the
intended tradeoff. This rule is written into `ci-cd/SKILL.md`'s Commit
Hygiene Expectations; this entry records the reasoning and the mistake that
led to it — an agent initially defaulted to splitting a diff into multiple
commits whenever it had more than one logical strand, which is wrong: one
requested commit message means one commit, everything else absorbed.

PR descriptions are not held to this same cap — they aggregate however many
commits are heading into merge-readiness and are allowed more length,
formatting, and context. The 72-word/single-scope discipline governs only
the one commit that becomes the durable record (the sole commit made, or the
result of squashing an exploratory branch via `rebase -i --autosquash`),
never intermediate or fixup commits made while work is still in progress.

**Batch or irreversible actions spanning multiple repos: always enumerate
and get explicit confirmation before acting, even under a direct, explicit
instruction.** When asked to delete or move files/directories across several
repos (e.g. everything under a workspace root), first do a read-only scan,
present the exact list of what matches, flag anything ambiguous in how the
instruction was worded, and exclude `.git/` internals and anything outside
the stated scope by default (e.g. backup snapshots) unless told otherwise.
"The instruction was explicit" is not sufficient on its own to skip this
when the operation is irreversible, spans repos outside the current
workspace, or the instruction has any real ambiguity in scope. See
`AGENTS.md`, Destructive and privileged actions, for the controlling rule.
