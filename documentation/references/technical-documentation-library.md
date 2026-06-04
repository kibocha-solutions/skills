# Technical Documentation Library

Use this reference when creating, auditing, or placing technical documentation
for a software project. It defines the default documentation library structure,
required starting documents, trigger-based documents, and the workflow for
choosing paths and sources.

## Core Model

Treat project documentation as a documentation library.

- `docs/` is the source boundary for documentation in an application
  repository. Keep it unless the whole repository is documentation-only.
- Writerside instances are published books or portals, not source folders.
- Source folders under the configured Writerside topics directory are semantic
  volumes that can feed multiple instances.
- Tree files define navigation order and audience output. Do not encode order
  with numeric folder or file prefixes.
- Topic and folder names use lowercase kebab-case.
- Writerside tree `topic` and `start-page` attributes reference flat topic
  filenames only. Physical folders may organize source files, but tree entries
  must use `security-baseline.md`, not `security/security-baseline.md`.
- Topic basenames must be unique across the help module.
- Technical diagrams are routed to the `technical-diagrams` skill. This skill
  consumes final `.svg` exports and links to editable `.drawio` sources.

## Writerside Instance Trees

Use these instance trees unless the target repository already has equivalent
names:

```text
docs/
|-- writerside.cfg
|-- public.tree
|-- internal.tree
|-- restricted.tree
|-- confidential.tree
|-- cfg/
|-- snippets/
`-- topics/
```

- `public.tree`: public guides, public API docs, public changelog, support
  docs, and sanitized release notes.
- `internal.tree`: engineering docs, architecture, testing, deployment,
  operations, internal APIs, and internal onboarding.
- `restricted.tree`: security, privacy, data classification, threat models,
  precise infrastructure/security internals, and incident-sensitive material.
- `confidential.tree`: executive, client-confidential, financial,
  donor/beneficiary-sensitive, or protected strategy material. Use only when a
  project has a real need for a separate high-sensitivity output.

Use snippet library topics under `docs/snippets/` for reusable prose,
warnings, notes, prerequisites, and other repeated content fragments. A snippet
library topic has `is-library: true`, is managed from the Writerside Snippets
node, and must not be included in any published instance tree.

Create a TOC library tree only when multiple instance trees need to reuse the
same navigation section. A TOC library tree contains reusable `toc-element`
groups and does not produce output.

Sensitivity flows upward. Public topics may appear in internal or restricted
instances. Restricted or confidential topics must not appear in lower-sensitivity
instances unless sanitized and reclassified.

## Confidentiality Ladder

Use this ladder for every path decision:

- Public: safe for external users, public API consumers, changelogs, support
  docs, and sanitized user/admin guides.
- Internal: safe for the engineering or product team, but not intended for
  public release.
- Restricted: security, privacy, infrastructure, data classification, threat
  models, incident-sensitive material, and tenant or permission internals.
- Confidential: executive strategy, client-confidential content, financial
  material, protected intellectual property, donor/beneficiary-sensitive
  material, or private scoring logic.
- Snippet library: reusable fragments. A shared item must carry the highest
  sensitivity of any content it includes and must not appear in a lower
  sensitivity output unless sanitized.

For quick lookup without loading this full reference, use:

- `../assets/technical-docs-required-tree.md`
- `../assets/technical-docs-optional-tree.md`

## Default Source Tree

When creating documentation from scratch, use this predictable source tree.
Only create folders that are needed for the current task or stage.

```text
docs/
|-- writerside.cfg
|-- public.tree
|-- internal.tree
|-- restricted.tree
|-- confidential.tree
|-- cfg/
|-- snippets/
|-- topics/
|   |-- product/
|   |-- project-brief.md
|   |-- product-doctrine.md
|   |-- mvp-scope-boundaries.md
|   |-- assessment-doctrine.md
|   |-- public-private-visibility.md
|   `-- requirements.md
|   |-- planning/
|   |-- decision-log.md
|   |-- assumptions-register.md
|   |-- risk-register.md
|   `-- release-checklist.md
|   |-- architecture/
|   |-- architecture-overview.md
|   |-- system-context.md
|   |-- api-boundary-doctrine.md
|   |-- decisions/
|   |   `-- adr-template.md
|   `-- c4/
|       |-- container-model.md
|       |-- component-model.md
|       `-- deployment-model.md
|   |-- domain/
|   |-- domain-model.md
|   |-- ubiquitous-language.md
|   |-- bounded-contexts.md
|   |-- entity-relationship-model.md
|   `-- document-lifecycle.md
|   |-- data/
|   |-- object-document-model.md
|   |-- database-schema.md
|   |-- data-dictionary.md
|   |-- data-classification.md
|   `-- backup-recovery.md
|   |-- security/
|   |-- security-baseline.md
|   |-- permission-tenant-isolation.md
|   |-- auth-authorization.md
|   |-- threat-model.md
|   `-- privacy-data-handling.md
|   |-- api/
|   |-- api-overview.md
|   |-- rest-api-reference.md
|   |-- graphql-grpc-reference.md
|   |-- internal-api-reference.md
|   `-- integration-guide.md
|   |-- engineering/
|   |-- developer-setup.md
|   |-- configuration-environment.md
|   |-- coding-style-guide.md
|   |-- code-comment-guide.md
|   `-- contribution-guide.md
|   |-- testing/
|   |-- testing-strategy.md
|   |-- test-plan.md
|   |-- test-cases.md
|   `-- test-data.md
|   |-- operations/
|   |-- deployment.md
|   |-- infrastructure.md
|   |-- ci-cd.md
|   |-- monitoring-alerting.md
|   |-- incident-response.md
|   `-- runbooks/
|       `-- runbook-template.md
|   |-- user-guides/
|   |-- admin-guide.md
|   |-- user-guide.md
|   |-- onboarding-guide.md
|   |-- troubleshooting-faq.md
|   `-- support.md
|   `-- releases/
|   |-- changelog.md
|   |-- migration-notes.md
|   `-- upgrade-guide.md
`-- diagrams/
    |-- system-context.drawio
    |-- system-context.svg
    |-- permission-model.drawio
    |-- permission-model.svg
    |-- entity-relationship.drawio
    |-- entity-relationship.svg
    |-- document-lifecycle.drawio
    `-- document-lifecycle.svg
```

## Required Starting Documents

Create or audit these documents for every serious software project beyond a
throwaway prototype:

| Path | Purpose | Instance |
| --- | --- | --- |
| `README.md` | Repository entry point, purpose, setup, and links into `docs/`. | Public or Internal |
| `docs/topics/product/project-brief.md` | Objectives, business context, users, and why the system exists. | Internal |
| `docs/topics/product/product-doctrine.md` | Product principles and non-negotiable direction. | Internal |
| `docs/topics/product/mvp-scope-boundaries.md` | In-scope and out-of-scope boundaries. | Internal |
| `docs/topics/planning/decision-log.md` | Lightweight chronological decisions. | Internal |
| `docs/topics/planning/assumptions-register.md` | Unverified beliefs, validation dates, owners, and status. | Internal |
| `docs/topics/planning/risk-register.md` | Risks, severity, mitigation, and triggers. | Internal |
| `docs/topics/architecture/architecture-overview.md` | System boundaries, major components, dependencies, and rationale. | Internal |
| `docs/topics/architecture/system-context.md` | C4-style context explanation and linked context diagram. | Internal |
| `docs/topics/architecture/api-boundary-doctrine.md` | Stable/public API boundaries and internal-only seams. | Internal |
| `docs/topics/architecture/decisions/` | MADR-style ADRs for foundational technical choices. | Internal |
| `docs/topics/domain/domain-model.md` | Ubiquitous language, entities, relationships, and bounded contexts. | Internal |
| `docs/topics/domain/entity-relationship-model.md` | Entity relationships at the business/domain level. | Internal |
| `docs/topics/domain/document-lifecycle.md` | State changes and lifecycle rules for important records. | Internal |
| `docs/topics/data/object-document-model.md` | Stored objects, documents, records, fields, ownership, and shape. | Internal |
| `docs/topics/security/security-baseline.md` | Secure defaults, secrets, dependency hygiene, and baseline controls. | Restricted |
| `docs/topics/security/permission-tenant-isolation.md` | Access boundaries, roles, tenant isolation, and authorization rules. | Restricted |
| `docs/topics/product/public-private-visibility.md` | What may be public, internal, restricted, or confidential. | Internal |
| `docs/diagrams/system-context.drawio` and `.svg` | Editable and published system context diagram. | Internal |
| `docs/diagrams/permission-model.drawio` and `.svg` | Editable and published permission model diagram. | Restricted |
| `docs/diagrams/entity-relationship.drawio` and `.svg` | Editable and published entity relationship diagram. | Internal |

Add `docs/topics/product/assessment-doctrine.md` when the product evaluates, scores,
ranks, accepts, rejects, matches, reviews, or otherwise assesses users,
documents, entities, or outcomes.

Add `docs/diagrams/document-lifecycle.drawio` and `.svg` when important records
move through states.

## Lifecycle Triggers

Use these stages to avoid premature documentation:

- P0 before coding: required starting documents above.
- P1 during early coding: `developer-setup.md`,
  `configuration-environment.md`, `database-schema.md`, ADRs for locked stack
  decisions, `testing-strategy.md`, and `api-overview.md` when API routes begin.
- P2 before hosted pilot: deployment, backup and recovery, basic runbooks,
  monitoring and alerting, user/admin onboarding draft, and changelog.
- P3 before paying or external users: public user guide, public API or
  integration guide, privacy/data handling explanation, support docs,
  troubleshooting, and release checklist.

## Additional Documentation Catalogue

These documents are good to have or mandatory only when their trigger is met.
Use the path and instance listed here unless the target repository already has a
compatible convention.

| Document | Default path | Trigger or use | Instance |
| --- | --- | --- | --- |
| Requirements documentation | `docs/topics/product/requirements.md` | Formal functional or non-functional requirements exist. | Internal |
| C4 container model | `docs/topics/architecture/c4/container-model.md` | Multiple runtime containers or deployable services exist. | Internal |
| C4 component model | `docs/topics/architecture/c4/component-model.md` | A container has important internal components. | Internal |
| C4 deployment model | `docs/topics/architecture/c4/deployment-model.md` | Deployment topology matters. | Internal |
| Database schema | `docs/topics/data/database-schema.md` | Persistent schema exists. | Internal |
| Data dictionary | `docs/topics/data/data-dictionary.md` | Stored fields need business definitions. | Internal |
| Data classification | `docs/topics/data/data-classification.md` | PII, PCI, regulated, donor, beneficiary, auth, uploads, or financial data exists. | Restricted |
| API overview | `docs/topics/api/api-overview.md` | API routes or service boundaries begin. | Public or Internal |
| REST API reference | `docs/topics/api/rest-api-reference.md` | REST API is consumed by another team or third party. | Public or Internal |
| GraphQL or gRPC reference | `docs/topics/api/graphql-grpc-reference.md` | GraphQL, gRPC, or protobuf schema exists. | Public or Internal |
| Internal API reference | `docs/topics/api/internal-api-reference.md` | Services communicate over internal APIs. | Internal |
| Auth and authorization | `docs/topics/security/auth-authorization.md` | Authentication, OAuth, RBAC, ABAC, or tokens exist. | Public, Internal, or Restricted |
| Threat model | `docs/topics/security/threat-model.md` | PII, auth, uploads, money, or privileged actions exist. | Restricted |
| Privacy and data handling | `docs/topics/security/privacy-data-handling.md` | User data retention, deletion, privacy, or compliance matters. | Restricted |
| Developer setup | `docs/topics/engineering/developer-setup.md` | More than one developer will run the project. | Internal |
| Configuration and environment | `docs/topics/engineering/configuration-environment.md` | Environment variables, secrets, or feature flags exist. | Internal |
| Coding style guide | `docs/topics/engineering/coding-style-guide.md` | Team conventions must be preserved. | Internal |
| Code comment guide | `docs/topics/engineering/code-comment-guide.md` | Source documentation expectations matter. | Internal |
| Contribution guide | `docs/topics/engineering/contribution-guide.md` | External contributors or larger teams need rules. | Public or Internal |
| Testing strategy | `docs/topics/testing/testing-strategy.md` | Tests define merge or release confidence. | Internal |
| Test plan | `docs/topics/testing/test-plan.md` | QA needs planned scenarios. | Internal |
| Test cases | `docs/topics/testing/test-cases.md` | Business logic needs explicit validation cases. | Internal |
| Test data | `docs/topics/testing/test-data.md` | Staging, fixtures, or sanitized data matter. | Internal |
| Deployment | `docs/topics/operations/deployment.md` | Hosted deployment begins. | Internal |
| Infrastructure | `docs/topics/operations/infrastructure.md` | Cloud topology, networking, or IaC matters. | Internal or Restricted |
| CI/CD | `docs/topics/operations/ci-cd.md` | Build and release pipeline exists. | Internal |
| Monitoring and alerting | `docs/topics/operations/monitoring-alerting.md` | Production or pilot monitoring exists. | Internal |
| Incident response | `docs/topics/operations/incident-response.md` | On-call or production support exists. | Internal |
| Runbooks | `docs/topics/operations/runbooks/<incident>.md` | A repeatable incident or operational failure exists. | Internal |
| Backup and recovery | `docs/topics/data/backup-recovery.md` | Hosted data must be restored after failure. | Internal |
| User guide | `docs/topics/user-guides/user-guide.md` | End users operate the product. | Public |
| Admin guide | `docs/topics/user-guides/admin-guide.md` | Admins configure or manage the product. | Public or Internal |
| Onboarding guide | `docs/topics/user-guides/onboarding-guide.md` | New users or developers need a guided first success path. | Public or Internal |
| Troubleshooting and FAQ | `docs/topics/user-guides/troubleshooting-faq.md` | Repeated support issues exist. | Public or Internal |
| Support docs | `docs/topics/user-guides/support.md` | Users need ticket, log, escalation, or contact guidance. | Public |
| Changelog | `docs/topics/releases/changelog.md` | Releases are cut or user-facing changes accumulate. | Public |
| Migration notes | `docs/topics/releases/migration-notes.md` | Breaking API, data, or behavior changes happen. | Public or Internal |
| Upgrade guide | `docs/topics/releases/upgrade-guide.md` | Users or admins must move between versions. | Public or Internal |
| SDK docs | `docs/topics/api/sdk-docs.md` | Language bindings exist. | Public |
| Examples and samples | `docs/topics/api/examples-samples.md` | API or SDK consumers need runnable examples. | Public |

## Document Workflow

1. Identify the requested document and its trigger.
2. Map it to the default path and instance. If the repository already has a
   compatible Writerside layout, follow the local convention.
3. Classify the document as Public, Internal, Restricted, or Confidential.
4. Gather internal sources first:
   - code, routes, schemas, migrations, models, serializers, configs, tests
   - existing docs, ADRs, issues, PRs, release notes, design notes
   - generated API contracts, CLI help, environment files, IaC, dashboards
   - diagrams already produced by `technical-diagrams`
5. If `sources/reports/documentation-reference.md` or an equivalent local
   documentation architecture report exists, read the relevant sections before
   changing structure, required-doc policy, or Writerside instance design.
6. Review online authoritative sources when relevant. Prefer official docs and
   primary standards:
   - Writerside docs for instances, tree files, topics, markup, snippets, and
     redirects
   - Diataxis, Red Hat Modular Docs, or DITA for documentation type boundaries
   - Google and Microsoft style guides for naming, clarity, and developer tone
   - C4 and MADR for architecture and ADRs
   - OWASP for secure coding, threat modeling, and data handling
   - Google SRE for incident response and runbooks
   - Keep a Changelog and SemVer for releases
   - official API/framework docs for project-specific APIs or tools
7. Decide whether diagrams are required. For architecture overview, C4, threat
   model, permission model, entity relationship, lifecycle, deployment, sequence,
   or data-flow diagrams, use `technical-diagrams`.
8. Draft the document with exact facts, explicit assumptions, source-backed
   claims, required commands or schemas, and validation steps.
9. Add the topic to the correct Writerside tree. Use hidden topics for large
   reference indexes, old ADRs, and narrow troubleshooting pages that should be
   searchable but not visible in the main navigation.
10. Run validation:
   - source review for claims, commands, paths, IDs, and links
   - Writerside preview or build when available
   - `documentation/scripts/check_technical_docs_tree.py <repo>` when auditing
     required starting files
11. Report what was created, where it belongs, what sources were used, what was
    not verified, and which trigger-based documents are still missing.

## Placement Checklist

- The path is lowercase kebab-case and has no numeric prefix.
- The folder is semantic, not audience-specific.
- The audience output is controlled by a Writerside tree file.
- The topic has a sensitivity classification when reuse or publication risk
  exists.
- The document is not premature for the project stage.
- Required diagrams exist as editable `.drawio` source plus final `.svg`.
- Public output does not include private scoring logic, security internals, raw
  incident detail, donor/beneficiary-sensitive data, or client-confidential
  material.
- The document cites or links to local source of truth where possible.
- Online sources are official, primary, or clearly identified as secondary.
