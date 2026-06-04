# Technical Documentation Routing

Use this reference when the task is software or systems technical
documentation. It routes the agent to migrated documentation guidance without
copying every technical-documentation rule into the always-loaded skill.

## Scope

This reference applies only to technical documentation for software, systems,
APIs, infrastructure, operations, security, databases, testing, configuration,
and developer/user technical guides.

It does not apply to ordinary reports, word-processing documents, letters,
strategy memos, research writeups, or other non-technical prose unless the user
explicitly asks for Writerside.

## Writerside Rule

All new technical documentation artifacts use Writerside-compatible Markdown.
This rule applies even when the technical topic is REST, GraphQL, gRPC,
internal APIs, deployment, operations, security, testing, database,
configuration, changelog, or user-guide documentation.

Do not generate any non-Writerside documentation format or configuration. When
migrating legacy guidance, translate the content shape into the target
Writerside structure.

API contract details belong in Writerside topics for this skill. Do not create
separate contract files unless the user explicitly asks for that work outside
the documentation task.

Use `writerside-technical-documentation.md` for Writerside project structure,
topic design, semantic markup, navigation, API topics, reuse, diagrams, and
validation rules.

Use `technical-documentation-library.md` for the default `docs/` source tree,
required starting documents, Writerside instance trees, document lifecycle
triggers, and path selection.

## Routing Table

Use references for content requirements, lifecycle triggers,
validation concerns, and required facts.

| Task | Migrated reference |
| --- | --- |
| Documentation library structure, required starting docs, path placement, lifecycle triggers | `references/technical-documentation-library.md` |
| Architecture overview, C4 diagrams, system context, containers, components | `references/technical-architecture-documentation.md` |
| ADRs and durable technical decisions | `references/adr-documentation.md` |
| REST API documentation | `references/api-documentation.md` |
| GraphQL API documentation | `references/api-documentation.md` |
| gRPC API documentation | `references/api-documentation.md` |
| Internal service APIs, retries, service discovery, timeouts, circuit breakers | `references/api-documentation.md` |
| Deployment, infrastructure setup, CI/CD, environments | `references/deployment-documentation.md` |
| Documentation hosting and deployment | `references/documentation-deployment.md` |
| Operations, runbooks, incident response, alert handling | `references/operations-runbook-documentation.md` |
| Database schema, migrations, data dictionary, ERDs | `references/database-documentation.md` |
| Security documentation, threat models, controls, compliance | `references/security-documentation.md` |
| Configuration docs, environment variables, feature flags | `references/configuration-documentation.md` |
| Testing strategy, test cases, coverage, test data | `references/testing-documentation.md` |
| User guides, tutorials, FAQs | `references/user-guide-documentation.md` |
| Changelog, release notes, migration notes | `references/changelog-documentation.md` |
| Documentation access classification | `references/access-level-classification.md` |
| Diagrams and visual documentation | Use the `technical-diagrams` skill. |

## Technical Documentation Procedure

1. Identify the documentation type before drafting.
2. Read `technical-documentation-library.md` to choose the default path,
   lifecycle trigger, access level, and Writerside instance.
3. Read the reference for the matching documentation type when it exists.
4. Read `writerside-technical-documentation.md` before choosing output
   structure or markup.
5. Classify the artifact as Public, Internal, Restricted, or Confidential when
   the content or storage location depends on sensitivity.
6. Use reference guidance for required content categories, validation concerns,
   lifecycle triggers, and relevant templates.
7. Prefer the target repository's existing Writerside structure when present.
8. Apply the documentation core checks after applying the technical
   guidance: specificity, economy, neutral tone, citation/source verification,
   and no purposeless medium references.

## Minimum Technical Checks

For technical documentation, verify that the artifact includes the operational
facts a reader needs:

- exact commands, paths, names, parameters, schemas, or endpoints where relevant
- prerequisites and assumptions that change execution
- expected output, success criteria, or validation steps
- failure modes, risks, or rollback steps for operational tasks
- version, environment, access level, or scope when it affects correctness
- source of truth for generated material

Remove narrative filler that does not help the reader perform, verify, operate,
or maintain the system.
