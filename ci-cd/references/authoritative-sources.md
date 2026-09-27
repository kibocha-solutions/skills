# Authoritative Sources

Use these primary sources when a claim in the `ci-cd` skill depends on external
platform behavior instead of local repository evidence.

## Git

1. `git-commit`: `--fixup`, `--fixup=amend:`, `--fixup=reword:`: https://git-scm.com/docs/git-commit
2. `git-rebase`: `--autosquash`, `rebase.autoSquash`: https://git-scm.com/docs/git-rebase

## GitHub Collaboration

1. Merge methods on GitHub: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
2. About pull request merges: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
3. Protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
4. Status checks: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories/about-status-checks
5. Merge queue: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue

## GitHub Actions Security

1. Secure use reference: https://docs.github.com/actions/reference/security/secure-use
2. Security for GitHub Actions: https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides
3. OIDC reference: https://docs.github.com/en/actions/reference/security/oidc

## GitLab Integration Safety

1. Merge trains: https://docs.gitlab.com/ci/pipelines/merge_trains/
2. Merged results pipelines: https://docs.gitlab.com/ci/pipelines/merged_results_pipelines/

## Google Cloud Delivery

1. Deployment methodology: https://cloud.google.com/architecture/enterprise-application-blueprint/deployment-methodology
2. Cloud Deploy architecture: https://cloud.google.com/deploy/docs/architecture
3. Manage rollouts: https://cloud.google.com/deploy/docs/deployment-strategies/manage-rollout
4. Business continuity with CI/CD: https://cloud.google.com/architecture/business-continuity-with-cicd-on-google-cloud

## DORA

1. Continuous delivery capability: https://dora.dev/capabilities/continuous-delivery/
2. Trunk-based development capability: https://dora.dev/capabilities/trunk-based-development/

## Google Engineering Practices

1. Writing good CL descriptions: https://google.github.io/eng-practices/review/developer/cl-descriptions.html
2. Small CLs: https://google.github.io/eng-practices/review/developer/small-cls.html

## Microsoft Engineering Standards

1. Submitting bugs and suggestions: Visual Studio Code: https://github.com/microsoft/vscode/wiki/Submitting-Bugs-and-Suggestions
2. Contributing and pull requests: Visual Studio Code: https://github.com/microsoft/vscode/wiki/How-to-Contribute

## Usage Rule

Do not present a platform-specific behavior as universal unless the local repo
or these primary sources support it. When a platform limitation, hosting plan,
or merge mode caveat matters, say so explicitly.
