# Authoritative Sources

Use these sources when a claim in the `ci-cd` skill depends on external
platform behavior rather than on local repository evidence.

## Git

- `git-commit`: `--fixup`, `--fixup=amend:`, `--fixup=reword:`
  - https://git-scm.com/docs/git-commit
- `git-rebase`: `--autosquash`, `rebase.autoSquash`
  - https://git-scm.com/docs/git-rebase

## GitHub Collaboration

- Merge methods on GitHub
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
- About pull request merges
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
- Protected branches
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Status checks
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories/about-status-checks
- Merge queue
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue

## GitHub Actions Security

- Secure use reference
  - https://docs.github.com/actions/reference/security/secure-use
- Security for GitHub Actions
  - https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides
- OIDC reference
  - https://docs.github.com/en/actions/reference/security/oidc

## GitLab Integration Safety

- Merge trains
  - https://docs.gitlab.com/ci/pipelines/merge_trains/
- Merged results pipelines
  - https://docs.gitlab.com/ci/pipelines/merged_results_pipelines/

## Google Cloud Delivery

- Deployment methodology
  - https://cloud.google.com/architecture/enterprise-application-blueprint/deployment-methodology
- Cloud Deploy architecture
  - https://cloud.google.com/deploy/docs/architecture
- Manage rollouts
  - https://cloud.google.com/deploy/docs/deployment-strategies/manage-rollout
- Business continuity with CI/CD
  - https://cloud.google.com/architecture/business-continuity-with-cicd-on-google-cloud

## DORA

- Continuous delivery capability
  - https://dora.dev/capabilities/continuous-delivery/
- Trunk-based development capability
  - https://dora.dev/capabilities/trunk-based-development/

## Usage Rule

Do not present a platform-specific behavior as universal unless the local repo
or these primary sources support it. When a platform limitation, hosting plan,
or merge mode caveat matters, say so explicitly.
