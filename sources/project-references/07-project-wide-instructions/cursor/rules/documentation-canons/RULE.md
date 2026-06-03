# Documentation Canons - Rules for Generating Documentation

## Purpose

Guide generation of documentation following established canons.

## Canon Structure

Every canon defines:
- Files to generate
- Directory structure
- Access level requirements
- Generation rules
- Content examples
- Validation steps

## Critical Rules (From Core Canon)

**Formatting Absolutes:**
- NO emojis (❌ 🎉 ✅)
- NO emdashes (—)
- Active voice preferred
- Specific over vague
- Vary sentence structure

**Primary Format:** reStructuredText (reST)

**Exceptions:** Markdown for README, CHANGELOG, ADRs only

## Access Level Classification

**REQUIRED for all documentation:**
- Level 1: Public (user guides, public APIs)
- Level 2: Internal (architecture, deployment)
- Level 3: Restricted (security threat models)
- Level 4: Confidential (executive only)

**Default:** Level 2 when uncertain

## Workflow

When generating any documentation:

1. **Read canon** in `01-documentation-canons/`
2. **Check syntax** in `03-reference/`
3. **Review example** in `02-examples/`
4. **Follow canon exactly**
5. **Validate** using `scripts/validate-docs.sh`

## Documentation Types

**APIs:**
- REST: OpenAPI YAML + reST (`_rest-api-canon.md`)
- GraphQL: GraphQL SDL + reST (`_graphql-api-canon.md`)
- gRPC: Proto3 + reST (`_grpc-api-canon.md`)

**System:**
- Architecture: C4 model, diagrams.net (`_architecture-canon.md`)
- Deployment: Infrastructure, CI/CD (`_deployment-canon.md`)
- Operations: Runbooks (`_operations-canon.md`)

**Data & Security:**
- Database: Schema, migrations (`_database-canon.md`)
- Security: STRIDE threat models (`_security-canon.md`)
- Configuration: Env vars (`_configuration-canon.md`)

**Process:**
- Testing: Pyramid, coverage (`_testing-canon.md`)
- ADR: Decision records (`_adr-canon.md`)
- Changelog: Keep a Changelog (`_changelog-canon.md`)
- User Guide: End-user docs (`_user-guide-canon.md`)

## Syntax References

Quick lookups in `03-reference/`:
- `rest-syntax.md` - reStructuredText complete syntax
- `openapi-syntax.md` - OpenAPI 3.0 reference
- `graphql-syntax.md` - GraphQL SDL reference
- `proto3-syntax.md` - Protocol Buffers reference
- `access-levels.md` - 4-level classification guide

## Validation

Before completion:

```bash
./scripts/validate-docs.sh
```

Checks:
- reST syntax
- OpenAPI specs
- GraphQL schemas
- Proto files
- No emojis/emdashes
- Access level warnings
