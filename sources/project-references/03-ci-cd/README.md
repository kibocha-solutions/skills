# CI/CD Reference Documentation

This directory contains comprehensive CI/CD (Continuous Integration / Continuous Deployment) standards and best practices.

## Contents

- **cicd-canon.md** - Complete CI/CD standards (9 comprehensive categories)

## Coverage

This CI/CD canon covers:

### 1. Git Workflow and Branching Strategies
- Trunk-Based Development (recommended)
- GitHub Flow (alternative)
- GitFlow (not recommended for CI/CD)
- Commit standards
- **Git Remote & PR Protocol (Aliases)** (See AGENTS.md Section 5A.1)
- **Branch Protection Limitations** (Free Plan awareness)

### 2. Pipeline Architecture and Best Practices
- Core principles (fail fast, single path to production, automate everything)
- Performance optimization (caching, parallel execution, incremental testing)
- Observability (metrics, monitoring, alerting)

### 3. Testing in CI/CD Pipelines
- Test automation pyramid (70/20/10 distribution)
- Testing stages (commit, PR, deployment, nightly)
- Test quality standards

### 4. Deployment Strategies
- Blue-Green deployment
- Canary deployment
- Rolling deployment
- Selection matrix

### 5. Environment Management
- Three environments (dev, staging, production)
- Environment parity
- Best practices

### 6. Versioning and Artifact Management
- Semantic Versioning
- Artifact immutability
- Storage best practices

### 7. Rollback Strategies
- Automated triggers
- Rollback methods
- Decision matrix

### 8. GitHub Actions Security
- Secrets management
- Supply chain security
- Least privilege permissions
- Injection attack prevention
- Runtime monitoring

### 9. CI/CD Anti-Patterns
- Overcomplicated pipelines
- No local testing
- Configuration not in Git
- Tool misuse

## When to Use

**ONLY reference files in this directory when performing CI/CD operations:**
- Setting up new CI/CD pipeline
- Configuring deployment strategies
- Establishing environment structure
- Implementing rollback procedures
- Reviewing pipeline security
- Troubleshooting CI/CD issues
- Optimizing pipeline performance

**Do NOT reference for regular development work.**

---

Version: 1.0 (December 29, 2025)
