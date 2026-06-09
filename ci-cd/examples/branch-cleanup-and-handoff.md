# Branch Cleanup And Handoff Example

Use this example when the user has a noisy local branch and wants one useful
final commit without losing branch intent.

## Situation

- Current branch: `fix/api`
- Intended base branch: `feat/docs`
- Branch purpose: temporary debug cleanup
- Local commit state: 14 small debug or repair commits after the real fix
- Publish state: not pushed for collaborative review

## Recommended guidance shape

1. Confirm that `fix/api` is a temporary cleanup branch, not the canonical
   feature branch.
2. Confirm that the history is still local and safe to rewrite.
3. Use `git commit --fixup` for any last targeted repairs.
4. Use `git rebase -i --autosquash feat/docs` or the appropriate base-point
   equivalent to compress the repair trail into one meaningful commit.
5. Verify:
   - the final diff is correct;
   - the final commit title is useful;
   - no unrelated procedural commits remain.
6. Merge or fast-forward the cleaned result back to `feat/docs`.
7. Delete `fix/api` if it was only a temporary cleanup branch.

## Example final recommendation

```text
Current branch: fix/api
Intended base branch: feat/docs
Branch purpose: temporary debug cleanup
History cleaned yet: no
Procedural commits since branch-off: 14
Safe next Git action: autosquash locally, verify the final diff, then merge the cleaned result back to feat/docs
```

## Example commit title

```text
fix(api): correct rate limiting behavior for burst traffic
```

## Why this example matters

The later agent must not assume `fix/api` is the long-lived feature branch or
that the 14 visible commits are meant to survive review.
