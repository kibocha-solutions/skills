# Integration Controls

Use this reference for high-throughput protected branches where ordinary PR
checks on a contributor branch are not enough to prove safe merge behavior.

Primary-source basis:

- GitHub merge queue and merge methods docs
- GitHub protected branches and status checks docs
- GitLab merge trains and merged-results pipelines docs
- DORA guidance for trunk-based development and continuous testing

## When To Reach For Extra Controls

Use merge queues, merge trains, or merged-result validation when:

- the protected branch receives many merges per day;
- contributors repeatedly rebase only to be invalidated by newer merges;
- required checks need to validate the combined branch state, not only a head
  branch in isolation;
- integration timing, not unit correctness, is the main source of failure.

## Control Selection

| Control | Best fit | Main caveat |
| --- | --- | --- |
| GitHub merge queue | Busy protected GitHub branch with required checks and frequent concurrent merges | Merge method is queue-controlled and platform availability varies by plan or repo type |
| GitLab merge train | Busy GitLab target branch with many ready merge requests | Requires platform support and extra CI capacity |
| GitLab merged-results pipeline | Need proof against current target-branch state before merge | Uses a temporary merged commit and can affect change-detection rules |
| Standard PR checks only | Lower-volume branches where integration skew is manageable | Contributors may need repeated manual updates |

## Merge Method Guidance

- Prefer squash merge when the branch history is mostly iterative repair
  chatter and the repo wants one useful final result.
- Prefer rebase merge only when commit boundaries are intentionally meaningful
  and the repo accepts the signature and SHA tradeoffs.
- Prefer merge commits only when the repo explicitly values branch topology or
  the platform and policy are built around that model.
- If a merge queue controls merge method, align your recommendations with the
  queue instead of assuming human choice at merge time.

## Status Check Guidance

- Required checks should be unique and unambiguous.
- Combined-state validation should be used when target-branch movement often
  invalidates head-branch-only checks.
- Do not confuse branch protection policy with workflow quality. A required
  check is useful only if it actually proves the relevant behavior.

## Operational Advice

- Use queueing or train controls to reduce integration thrash, not to hide weak
  tests.
- Keep the default branch healthy. Queue systems amplify the cost of a broken
  trunk.
- If the repo does not have the necessary platform feature, say so and fall
  back to the safest available discipline rather than pretending the feature
  exists.
