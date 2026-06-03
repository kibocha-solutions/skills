# Changelog

All notable changes to the Vibe Code Canon - Technical Documentation Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-12-29

### Added
- Initial canon framework structure
- Core canon files:
  - `_core_canon.md` - Universal writing rules
  - `_template.md` - Persona template
  - `_docs-canon.md` - Technical documentation standards
- Directory structure for canon-based documentation system
- README.md with comprehensive framework overview
- Original design conversation preserved in `03-reference/docs-conversations.md`

### Structure
- `00-core-canons/` - Foundation rules
- `01-documentation-canons/` - Type-specific documentation rules
- `02-examples/` - Working examples
- `03-reference/` - Quick syntax references

### Philosophy
- Agents need rules and examples, not templates
- Human-readable, agent-executable documentation standards
- Production-grade documentation from consistent canonical rules

---

## [Unreleased]

### Added - Automation & Validation

**Validation & CI/CD:**
- `scripts/validate-docs.sh` - Unified validation script for all documentation types
- `.github/workflows/docs.yml` - GitHub Actions workflow for CI/CD and deployment
- `scripts/pre-commit` - Pre-commit hook for local validation

### Features

**Validation Script:**
- Validates reST, OpenAPI, GraphQL, Proto, Markdown
- Checks formatting rules (no emojis, no emdashes)
- Sphinx build verification
- Access level warning checks
- Selective validation (--rest, --openapi, etc.)

**CI/CD Workflow:**
- Automated validation on PR and push
- Sphinx documentation build
- GitHub Pages deployment (on main branch)
- Multi-language setup (Python, Node.js)

**Pre-commit Hook:**
- Fast local validation before commit
- Checks only changed files
- Formatting rules enforcement

### Planned
- Additional working examples for major canons

---

## [1.5.0] - 2025-12-29

### Added - Syntax Reference Guides

**Reference Materials:**
- `03-reference/rest-syntax.md` - reStructuredText complete syntax guide
- `03-reference/access-levels.md` - 4-level access classification guide
- `03-reference/openapi-syntax.md` - OpenAPI 3.0 specification reference
- `03-reference/graphql-syntax.md` - GraphQL SDL complete reference
- `03-reference/proto3-syntax.md` - Protocol Buffers (proto3) reference

### Features

**reStructuredText Reference:**
- Complete syntax for headings, lists, code blocks, tables
- Cross-referencing and links
- Admonitions (warnings, notes, tips)
- Sphinx directives
- Comparison with Markdown
- Validation commands

**Access Levels Guide:**
- 4-level classification system (Public, Internal, Restricted, Confidential)
- Assignment matrix for all documentation types
- Decision tree for level determination
- Storage and distribution requirements
- Compliance considerations (GDPR, SOC 2, ISO 27001)

**OpenAPI Reference:**
- OpenAPI 3.0.3 syntax (YAML preferred)
- Paths, parameters, request/response bodies
- Schemas and data types
- Security schemes (Bearer, API Key, OAuth 2.0)
- Validation with swagger-cli
- Interactive documentation (Swagger UI, Redoc)

**GraphQL Reference:**
- Complete SDL syntax
- Types, queries, mutations, subscriptions
- Custom scalars, enums, interfaces, unions
- Pagination patterns (Connection/Edge)
- Directives and error handling
- Client query examples

**Protocol Buffers Reference:**
- Proto3 syntax and structure
- Messages, enums, services
- Streaming patterns (server, client, bidirectional)
- Well-known types (Timestamp, Duration, Empty)
- Code generation for Go, Python, Java
- gRPC best practices

### Documentation Standards
- All references provide quick lookups for agents and humans
- Executable examples for all syntax patterns
- Validation commands included
- Best practices documented

---

## [1.4.0] - 2025-12-29

### Added - Batch 3: Process & Quality Documentation Canons

**Documentation Canons:**
- `01-documentation-canons/_testing-canon.md` - Testing documentation rules
- `01-documentation-canons/_adr-canon.md` - Architecture Decision Records rules
- `01-documentation-canons/_changelog-canon.md` - Changelog documentation rules
- `01-documentation-canons/_user-guide-canon.md` - User guide documentation rules

### Features

**Testing Canon:**
- Test pyramid approach (70% unit, 20% integration, 10% E2E)
- Coverage requirements and quality gates
- Unit, integration, and E2E testing guidelines
- Test frameworks (Jest, Go testing)
- Code examples for all test types

**ADR Canon:**
- Michael Nygard ADR template
- Context, decision, consequences, alternatives structure
- Sequential numbering with zero-padding
- Markdown format (exception to reST standard)
- ADR index with status tracking

**Changelog Canon:**
- "Keep a Changelog" v1.1.0 standard
- Semantic Versioning (SemVer 2.0.0)
- Change categories (Added, Changed, Deprecated, Removed, Fixed, Security)
- Breaking changes documentation
- Conventional Commits automation

**User Guide Canon:**
- User-centric language (non-technical)
- Task-oriented structure
- Getting started, features, tutorials, troubleshooting, FAQ
- Screenshot guidelines
- Public (Level 1) access

### Documentation Standards
- All canons follow `_core_canon.md` writing rules
- User-facing content uses simple, clear language
- ADRs document alternatives honestly
- Changelogs use user-readable descriptions

---

## [1.3.0] - 2025-12-29

### Added - Batch 2: Data & Security Documentation Canons

**Documentation Canons:**
- `01-documentation-canons/_database-canon.md` - Database documentation rules
- `01-documentation-canons/_security-canon.md` - Security documentation rules (Level 3 Restricted)
- `01-documentation-canons/_configuration-canon.md` - Configuration documentation rules

### Features

**Database Canon:**
- Entity Relationship Diagram (ERD) standards
- Table and column documentation with constraints
- Index strategy and performance optimization
- Migration procedures with Flyway
- Backup and recovery procedures
- PostgreSQL-focused with SQL examples

**Security Canon:**
- STRIDE threat modeling framework
- Authentication and authorization (JWT, RBAC)
- Data encryption (at rest and in transit)
- Compliance requirements (GDPR, PCI-DSS)
- Security incident response procedures
- Restricted (Level 3) access classification

**Configuration Canon:**
- Environment variable complete reference
- Configuration file formats
- Feature flag documentation
- Environment-specific settings (dev, staging, production)
- Secret handling guidelines (no actual secrets documented)

### Documentation Standards
- All canons follow `_core_canon.md` writing rules
- Security documentation marked as Restricted (Level 3)
- Tables used appropriately for parameter listings
- No actual secrets or credentials in documentation

---

## [1.2.0] - 2025-12-29

### Added - Batch 1: System Documentation Canons

**Documentation Canons:**
- `01-documentation-canons/_architecture-canon.md` - Architecture documentation rules
- `01-documentation-canons/_deployment-canon.md` - Deployment documentation rules
- `01-documentation-canons/_operations-canon.md` - Operations/runbook documentation rules

**Examples:**
- `02-examples/architecture-example/00-overview.rst` - Complete architecture overview example
- `02-examples/architecture-example/README.md` - Architecture example guide

**Reference Materials:**
- `03-reference/diagrams-net-guide.md` - diagrams.net quick reference for C4 diagrams

### Features

**Architecture Canon:**
- C4 model structure (System Context, Containers, Components)
- diagrams.net diagram standards with color scheme
- Technology stack documentation with justifications
- Data flow, scalability, security, integration points
- Complete file structure and directory layout

**Deployment Canon:**
- Local development environment setup
- Staging and production deployment procedures
- Infrastructure as Code documentation
- CI/CD pipeline configuration
- Rollback and disaster recovery procedures
- Deployment checklists and approval gates

**Operations Canon:**
- Incident response workflow with severity levels
- Service-specific runbook structure
- Common issues troubleshooting guide
- Alerting guide with response procedures
- Maintenance procedures documentation
- Escalation paths and war room procedures

**diagrams.net Reference:**
- C4 diagram creation instructions
- Standard color scheme with hex codes
- Export settings for PNG/SVG
- Shape libraries and best practices
- Integration with reStructuredText

### Documentation Standards
- All canons follow `_core_canon.md` writing rules
- Human-readable and agent-executable
- Production-grade procedures and examples
- Consistent structure across all system documentation

---

## [1.1.0] - 2025-12-29

### Added - Phase 2: API Documentation Canons
- `01-documentation-canons/api-documentation/_rest-api-canon.md` - REST API documentation rules
- `01-documentation-canons/api-documentation/_graphql-api-canon.md` - GraphQL API documentation rules
- `01-documentation-canons/api-documentation/_grpc-api-canon.md` - gRPC API documentation rules
- `01-documentation-canons/api-documentation/_internal-api-canon.md` - Internal API documentation rules

### Features
- Complete file structure specifications for each API type
- OpenAPI 3.0 YAML generation rules
- GraphQL SDL generation rules
- Protocol Buffers 3 generation rules
- Internal API specific additions (service discovery, mTLS, circuit breakers, retry policies)
- Validation commands for all API types
- Multi-language code examples (Python, JavaScript, Go, Java, Rust)
- Access level warnings and classifications
- Agent checklists for documentation completion

### Documentation Standards
- All canons follow `_core_canon.md` writing rules (no emojis, no emdashes, varied sentence structure)
- Human-readable and agent-executable format
- Production-grade examples and patterns
- Consistent structure across all API types

---

## Version History

- **1.0.0** (2025-12-29) - Initial release with core structure
