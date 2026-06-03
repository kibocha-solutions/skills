# Framework Overview - Technical Documentation Canons

## Purpose

Provide comprehensive understanding of the Technical Documentation Framework structure and usage.

## Project Overview

This framework provides canonical standards for generating production-grade technical documentation.

**Core Principle:** Agents need rules + examples, not templates.

## Structure

```
01-technical-documentation/
├── 00-core-canons/              # Universal rules
├── 01-documentation-canons/     # 14 type-specific canons
├── 02-examples/                 # Working examples
├── 03-reference/                # Syntax quick references
└── scripts/                     # Validation tools
```

## Core Rules

From `00-core-canons/_core_canon.md`:

**NEVER:**
- Use emojis
- Use emdashes (—)
- Use AI clichés ("delve," "tapestry," etc.)
- Use meta-commentary

**ALWAYS:**
- Active voice
- Specific examples
- Vary sentence structure
- Validate output

## Documentation Types (14 Canons)

1. REST API
2. GraphQL API
3. gRPC API
4. Internal API
5. Architecture
6. Deployment
7. Operations
8. Database
9. Security
10. Configuration
11. Testing
12. ADR
13. Changelog
14. User Guide

## Primary Format

reStructuredText (reST) with Sphinx for all narrative documentation.

**Exceptions:** Markdown for README, CHANGELOG, ADRs only.

## Access Levels

All documentation MUST be classified:
- Level 1: Public
- Level 2: Internal
- Level 3: Restricted
- Level 4: Confidential

## Workflow

1. Read core canons
2. Read specific canon
3. Check syntax reference
4. Generate following canon rules
5. Validate with scripts

## Key Files

- Core canon: `00-core-canons/_core_canon.md`
- Docs canon: `00-core-canons/_docs-canon.md`
- reST syntax: `03-reference/rest-syntax.md`
- Access levels: `03-reference/access-levels.md`
