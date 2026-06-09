# Project-References Master Index

This directory contains source reference material for skills and project
standards. It is not the active instruction authority for this repository.

## Structure

```
sources/project-references/
├── README.md (this file)
├── 02-security/                        # Security standards
├── 04-testing/                         # Testing procedures
├── 05-programming-standards/           # Code standards
└── 06-deployment/                      # Infrastructure, deployment
```

## Active Authority

Use the local skills repo `AGENTS.md` and installed skills as the active agent
instruction layer. Do not treat files in this directory as a second authority.
Extract techniques and standards from these references into local skills when a
stable workflow needs to become agent-facing.

## Reference Domains

Each reference directory contains deep-dive canonical instructions for specific domains:

### 02-security/
**Use when:** Authentication, encryption, sensitive data handling  
**Contains:** Security standards, OWASP prevention, secure coding

### 04-testing/
**Use when:** Writing tests (unit, integration, E2E, performance)  
**Contains:** Testing strategies, standards, test data management

### 05-programming-standards/
**Use when:** Writing application code in any language  
**Contains:** Language-specific standards, design principles, error handling

### 06-deployment/
**Use when:** Infrastructure setup, Kubernetes, deployment procedures  
**Contains:** Deployment patterns, IaC standards, monitoring

## Critical Principles

1. Read only the references relevant to the task.
2. Prefer repo truth over generic canon wording.
3. Promote stable workflows into local skills instead of maintaining parallel
   agent overlays.
4. Treat security, deployment, and commit guidance as operational constraints,
   not decorative prose.
5. Do not assume these references are repo-specific until local evidence proves
   it.

---

**Version:** 1.0 (December 29, 2025)
