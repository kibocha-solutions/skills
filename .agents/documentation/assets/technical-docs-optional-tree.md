# Optional and trigger-based technical documentation tree.

These paths are optional or trigger-based additions to the required starting set.

| Path | Confidentiality | Trigger or use |
| --- | --- | --- |
| `docs/topics/product/assessment-doctrine.md` | Internal | product evaluates, scores, ranks, accepts, rejects, matches, or reviews outcomes |
| `docs/topics/product/requirements.md` | Internal | formal functional or non-functional requirements exist |
| `docs/topics/architecture/c4/container-model.md` | Internal | multiple runtime containers or deployable services exist |
| `docs/topics/architecture/c4/component-model.md` | Internal | a container has important internal components |
| `docs/topics/architecture/c4/deployment-model.md` | Internal | deployment topology matters |
| `docs/topics/data/database-schema.md` | Internal | persistent schema exists |
| `docs/topics/data/data-dictionary.md` | Internal | stored fields need business definitions |
| `docs/topics/data/data-classification.md` | Restricted | PII, PCI, regulated, donor, beneficiary, auth, uploads, or financial data exists |
| `docs/topics/data/backup-recovery.md` | Internal | hosted data must be restored after failure |
| `docs/topics/security/auth-authorization.md` | Public, Internal, or Restricted | authentication, OAuth, RBAC, ABAC, or tokens exist |
| `docs/topics/security/threat-model.md` | Restricted | PII, auth, uploads, money, privileged actions, or sensitive infrastructure exists |
| `docs/topics/security/privacy-data-handling.md` | Restricted | retention, deletion, privacy, or compliance matters |
| `docs/topics/api/api-overview.md` | Public or Internal | API routes or service boundaries begin |
| `docs/topics/api/rest-api-reference.md` | Public or Internal | REST API is consumed by another team or third party |
| `docs/topics/api/graphql-grpc-reference.md` | Public or Internal | GraphQL, gRPC, or protobuf schema exists |
| `docs/topics/api/internal-api-reference.md` | Internal | services communicate over internal APIs |
| `docs/topics/api/integration-guide.md` | Public | third-party or external-team API consumers need a narrative guide |
| `docs/topics/api/sdk-docs.md` | Public | language bindings exist |
| `docs/topics/api/examples-samples.md` | Public | API or SDK consumers need runnable examples |
| `docs/topics/engineering/developer-setup.md` | Internal | more than one developer will run the project |
| `docs/topics/engineering/configuration-environment.md` | Internal | environment variables, secrets, or feature flags exist |
| `docs/topics/engineering/coding-style-guide.md` | Internal | team conventions must be preserved |
| `docs/topics/engineering/code-comment-guide.md` | Internal | source documentation expectations matter |
| `docs/topics/engineering/contribution-guide.md` | Public or Internal | external contributors or larger teams need rules |
| `docs/topics/testing/testing-strategy.md` | Internal | tests define merge or release confidence |
| `docs/topics/testing/test-plan.md` | Internal | QA needs planned scenarios |
| `docs/topics/testing/test-cases.md` | Internal | business logic needs explicit validation cases |
| `docs/topics/testing/test-data.md` | Internal | staging, fixtures, or sanitized data matter |
| `docs/topics/operations/deployment.md` | Internal | hosted deployment begins |
| `docs/topics/operations/infrastructure.md` | Internal or Restricted | cloud topology, networking, or IaC matters |
| `docs/topics/operations/ci-cd.md` | Internal | build and release pipeline exists |
| `docs/topics/operations/monitoring-alerting.md` | Internal | production or pilot monitoring exists |
| `docs/topics/operations/incident-response.md` | Internal | on-call or production support exists |
| `docs/topics/operations/runbooks/<incident>.md` | Internal | repeatable incident or operational failure exists |
| `docs/topics/user-guides/user-guide.md` | Public | end users operate the product |
| `docs/topics/user-guides/admin-guide.md` | Public or Internal | admins configure or manage the product |
| `docs/topics/user-guides/onboarding-guide.md` | Public or Internal | new users or developers need a guided first success path |
| `docs/topics/user-guides/troubleshooting-faq.md` | Public or Internal | repeated support issues exist |
| `docs/topics/user-guides/support.md` | Public | users need ticket, log, escalation, or contact guidance |
| `docs/topics/releases/changelog.md` | Public | releases are cut or user-facing changes accumulate |
| `docs/topics/releases/migration-notes.md` | Public or Internal | breaking API, data, or behavior changes happen |
| `docs/topics/releases/upgrade-guide.md` | Public or Internal | users or admins must move between versions |
| `docs/diagrams/document-lifecycle.drawio` | Internal | important records move through states |
| `docs/diagrams/document-lifecycle.svg` | Internal | published lifecycle diagram |
| `docs/diagrams/container-model.drawio` | Internal | C4 container diagram is required |
| `docs/diagrams/container-model.svg` | Internal | published C4 container diagram |
| `docs/diagrams/component-model.drawio` | Internal | C4 component diagram is required |
| `docs/diagrams/component-model.svg` | Internal | published C4 component diagram |
| `docs/diagrams/deployment-model.drawio` | Internal or Restricted | deployment topology diagram is required |
| `docs/diagrams/deployment-model.svg` | Internal or Restricted | published deployment topology diagram |
| `docs/diagrams/threat-model.drawio` | Restricted | threat model diagram is required |
| `docs/diagrams/threat-model.svg` | Restricted | published threat model diagram |
