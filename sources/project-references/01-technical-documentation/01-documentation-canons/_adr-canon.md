# Canon: Architecture Decision Records (ADR) Documentation

## Purpose

Architecture Decision Records (ADRs) document significant architectural and design decisions, capturing context, alternatives considered, and consequences. ADRs create an immutable decision history enabling teams to understand why systems evolved as they did.

---

## Scope

**This canon applies to:**
- Architectural decisions (technology choices, patterns, frameworks)
- Design decisions with long-term implications
- Trade-off evaluations
- Decisions that are hard to reverse
- Decisions affecting multiple teams or components

**This canon does NOT apply to:**
- Code-level decisions (document in code comments)
- Tactical bug fixes (use issue tracker)
- Temporary workarounds
- Trivial configuration changes

---

## Access Level Classification

**ADR Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Development team, architecture team, technical leadership
- **Storage:** Private repository with authentication (committed to version control)
- **Review:** Architecture review, technical lead approval
- **Rationale:** Contains strategic decisions, rejected alternatives, technical debt acknowledgment

**Exception:** ADRs for open-source projects may be Public (Level 1) to explain project direction

---

## When to Generate

### Triggers for Creating an ADR

Create an ADR when making decisions about:

- **Technology Selection**: Choosing programming language, framework, or major library
- **Architecture Patterns**: Microservices vs monolith, event-driven vs request-response
- **Data Storage**: Database selection, caching strategy, data modeling
- **Security**: Authentication mechanism, encryption approach
- **Integration**: API design, message queue selection
- **Deployment**: Infrastructure as Code tool, container orchestration
- **Breaking Changes**: API versioning, deprecation strategy

### When NOT to Create an ADR

Do not create ADRs for:
- Implementation details (which variable names to use)
- Obvious choices (using HTTPS instead of HTTP)
- Reversible decisions with low impact
- Personal coding preferences

---

## Files to Generate

Agent must create ADRs following this structure:

### ADR Filename Convention
**File:** `/docs/decisions/ADR-{NNNN}-{title-with-dashes}.md`  
**Format:** Markdown (exception to reST standard for ADRs)  
**Numbering:** Sequential, zero-padded to 4 digits

**Examples:**
- `/docs/decisions/ADR-0001-use-postgresql-for-primary-database.md`
- `/docs/decisions/ADR-0002-adopt-microservices-architecture.md`
- `/docs/decisions/ADR-0003-implement-jwt-authentication.md`

### ADR Index File
**File:** `/docs/decisions/README.md`  
**Format:** Markdown  
**Purpose:** Table of contents linking to all ADRs with status

---

## Directory Structure

```
docs/decisions/
├── README.md                                        # ADR index
├── ADR-0001-use-postgresql-for-primary-database.md
├── ADR-0002-adopt-microservices-architecture.md
├── ADR-0003-implement-jwt-authentication.md
├── ADR-0004-choose-react-for-frontend.md
├── ADR-0005-use-redis-for-caching.md
└── ADR-0006-deprecate-rest-api-v1.md
```

---

## Generation Rules

### ADR Template (Michael Nygard Format)

Every ADR must follow this structure:

```markdown
# ADR-{NNNN}: {Title}

**Status**: {Proposed | Accepted | Deprecated | Superseded}  
**Date**: YYYY-MM-DD  
**Authors**: {Name(s)}  
**Deciders**: {Who participated in decision}

## Context

{Describe the forces at play: technical, political, social, project.
What is the issue we're trying to solve? Why does it matter?}

## Decision

{The decision that was made. Use active voice: "We will..."}

## Consequences

### Positive

{Benefits and advantages of this decision}

### Negative

{Drawbacks, costs, and trade-offs}

### Risks

{Potential risks and mitigation strategies}

## Alternatives Considered

### Alternative 1: {Name}

{Description, pros, cons, why rejected}

### Alternative 2: {Name}

{Description, pros, cons, why rejected}

## Related Decisions

{Links to related ADRs that influenced or are influenced by this decision}
```

### Status Values

**Proposed**: Decision under review, not yet finalized  
**Accepted**: Decision approved and active  
**Deprecated**: Decision no longer recommended but still in use  
**Superseded**: Decision replaced by another ADR (link to new ADR)

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice ("We will use PostgreSQL" not "PostgreSQL should be used")
- Specific over vague (exact reasons, metrics, trade-offs)
- Honest about trade-offs (document negatives openly)
- **Markdown format** (exception to reST standard)

---

## Content Guidelines

### ADR Index (`/docs/decisions/README.md`)

```markdown
# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) documenting significant architectural and design decisions.

## Purpose

ADRs capture:
- **What** decision was made
- **Why** it was made (context and forces)
- **What** alternatives were considered
- **What** consequences we accept

## Status Legend

- **Proposed**: Under review
- **Accepted**: Approved and active
- **Deprecated**: No longer recommended
- **Superseded**: Replaced by newer ADR

## ADR Index

| ADR | Title | Status | Date | Authors |
|-----|-------|--------|------|---------|
| [ADR-0001](ADR-0001-use-postgresql-for-primary-database.md) | Use PostgreSQL for Primary Database | Accepted | 2025-01-15 | John Doe |
| [ADR-0002](ADR-0002-adopt-microservices-architecture.md) | Adopt Microservices Architecture | Accepted | 2025-02-10 | Jane Smith |
| [ADR-0003](ADR-0003-implement-jwt-authentication.md) | Implement JWT Authentication | Accepted | 2025-03-05 | John Doe |
| [ADR-0004](ADR-0004-choose-react-for-frontend.md) | Choose React for Frontend | Accepted | 2025-03-20 | Alice Johnson |
| [ADR-0005](ADR-0005-use-redis-for-caching.md) | Use Redis for Caching | Accepted | 2025-04-12 | Bob Lee |
| [ADR-0006](ADR-0006-deprecate-rest-api-v1.md) | Deprecate REST API v1 | Accepted | 2025-11-30 | Jane Smith |

## Creating a New ADR

1. Copy template from this document
2. Number sequentially (next available number)
3. Fill in all sections
4. Submit for architecture review
5. Update this index after approval

## ADR Template

```markdown
# ADR-NNNN: {Title}

**Status**: Proposed  
**Date**: YYYY-MM-DD  
**Authors**: {Name}  
**Deciders**: {Names}

## Context

{Issue and context}

## Decision

{What we decided}

## Consequences

### Positive
{Benefits}

### Negative
{Drawbacks}

### Risks
{Potential risks}

## Alternatives Considered

### Alternative 1
{Description and why rejected}

## Related Decisions

{Links to related ADRs}
```

```

### Example ADR (`ADR-0001-use-postgresql-for-primary-database.md`)

```markdown
# ADR-0001: Use PostgreSQL for Primary Database

**Status**: Accepted  
**Date**: 2025-01-15  
**Authors**: John Doe  
**Deciders**: Architecture Team (John Doe, Jane Smith, Bob Lee)

## Context

We need to select a primary database for the Tax Management System. The system requires:

- ACID compliance for financial data integrity
- Support for complex querying (tax calculations, reporting)
- JSON support for flexible schema parts (receipt metadata)
- Strong consistency guarantees
- Proven track record in production environments
- Good tooling and ecosystem

Our expected scale:
- 500,000 users within 12 months
- 2 million tax calculations per month
- 5 million receipts stored

Budget constraints favor open-source solutions over commercial licenses.

## Decision

We will use PostgreSQL 15 as the primary database for the Tax Management System.

PostgreSQL will store:
- User accounts and authentication data
- Tax calculations and history
- Receipt metadata (files stored in S3)
- Audit logs
- System configuration

## Consequences

### Positive

**ACID Compliance**
PostgreSQL provides strong consistency guarantees critical for financial data.

**JSON Support**
Native JSONB type allows flexible schema for receipt metadata without sacrificing query performance.

**Mature Ecosystem**
Extensive tooling (pgAdmin, pg_dump, replication solutions) and community support.

**Performance**
Handles our expected scale (benchmarks show 10,000+ TPS with proper indexing).

**Cost**
Open-source with no licensing fees reduces operational costs.

**Team Expertise**
Team has 5+ years combined PostgreSQL experience.

### Negative

**Vertical Scaling Limits**
PostgreSQL scales vertically better than horizontally. We may need read replicas for read-heavy workloads.

**Complex Sharding**
If we exceed single-instance capacity, sharding is more complex than distributed databases.

**Operational Overhead**
Self-hosted PostgreSQL requires managing backups, replication, failover (mitigated by using AWS RDS).

### Risks

**Risk**: Single point of failure  
**Mitigation**: Use AWS RDS Multi-AZ deployment with automated failover

**Risk**: Performance degradation at scale  
**Mitigation**: Implement connection pooling, read replicas, query optimization, partitioning

**Risk**: Data loss on hardware failure  
**Mitigation**: Automated daily backups with 30-day retention, point-in-time recovery enabled

## Alternatives Considered

### Alternative 1: MongoDB

**Description**: Document database with flexible schema

**Pros**:
- Flexible schema (no migrations for schema changes)
- Horizontal scaling built-in (sharding)
- JSON-native storage

**Cons**:
- Eventual consistency by default (not ACID)
- Less mature SQL-like query language
- Team has limited MongoDB experience
- Financial data requires strong consistency

**Why Rejected**: ACID compliance is non-negotiable for financial data. MongoDB's eventual consistency model introduces risk for tax calculations.

### Alternative 2: MySQL

**Description**: Popular open-source relational database

**Pros**:
- ACID compliant
- Mature ecosystem
- Wide adoption

**Cons**:
- Weaker JSON support compared to PostgreSQL
- Less advanced features (window functions, CTEs)
- InnoDB storage engine has limitations

**Why Rejected**: PostgreSQL's superior JSON support and advanced SQL features better match our requirements.

### Alternative 3: Amazon DynamoDB

**Description**: Managed NoSQL database

**Pros**:
- Fully managed (no operational overhead)
- Auto-scaling
- High availability

**Cons**:
- Eventual consistency by default
- Limited querying capabilities (no joins, complex filters difficult)
- Vendor lock-in to AWS
- Cost unpredictable at scale

**Why Rejected**: Complex querying requirements (tax reporting, analytics) are difficult in DynamoDB. Relational model better fits our use case.

## Related Decisions

- **ADR-0005**: Use Redis for Caching (complements PostgreSQL for read-heavy loads)
- **ADR-0002**: Adopt Microservices Architecture (each service has dedicated PostgreSQL schema)
```

---

## Validation

Agent must validate documentation before completion:

### Markdown Validation

```bash
# Lint all ADR markdown files
markdownlint docs/decisions/*.md
```

**Expected output:** No errors

### ADR Index Validation

- [ ] All ADRs listed in README.md index
- [ ] All links work
- [ ] Status values are valid (Proposed, Accepted, Deprecated, Superseded)
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Sequential numbering (no gaps)

---

## Examples Reference

See working example: `02-examples/adr-example/` (to be created)

**Example includes:**
- Complete ADR set
- ADR index (README.md)
- Example ADRs for common decisions

---

## Access Level Warning

Include at top of ADR index README.md:

```markdown
> **Warning**: INTERNAL DOCUMENTATION - Level 2 Access  
> This documentation contains strategic architectural decisions.  
> Do not share with external parties.
```

---

## Agent Checklist

Before marking ADR documentation complete, verify:

- [ ] ADR index (README.md) created with table of all ADRs
- [ ] ADRs follow Michael Nygard template
- [ ] All ADRs have sequential numbers (zero-padded 4 digits)
- [ ] All ADRs document alternatives considered
- [ ] Consequences (positive and negative) documented honestly
- [ ] Status values correct (Proposed, Accepted, Deprecated, Superseded)
- [ ] Links between related ADRs included
- [ ] Markdown linting passes
- [ ] Access level warning included
- [ ] No emojis or emdashes present

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial ADR documentation canon
- Based on Michael Nygard ADR template
- Follows `_docs-canon.md` v4 specifications
