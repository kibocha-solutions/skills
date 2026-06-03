# Security Canon: Modular Structure

## Overview

This directory contains the complete Security Canon for the Vibe Code Canon framework, restructured into 8 modular, numbered folders for government-grade security standards.

**Authority:** These standards have ABSOLUTE AUTHORITY and MUST be followed alongside the security checklist in agent instructions.

**Compliance:** Based on OWASP Top 10 (2024), NIST 800-53, ISO 27001, PCI DSS, FedRAMP, GDPR, and CCPA.

---

## Directory Structure

### [01-access-and-authentication/](./01-access-and-authentication/)
**Code-Level Security: Authentication & Authorization**
- `access-control.md` - Broken Access Control (OWASP #1), RBAC, ABAC, Least Privilege, Separation of Duties
- `mfa.md` - Multi-Factor Authentication (MFA requirements, hardware tokens, authenticator apps)
- `session-management.md` - Token lifespans, refresh flow, storage, revocation
- `token-signing.md` - Signed cookies, JWT verification, session validation, HMAC

### [02-injection-prevention/](./02-injection-prevention/)
**Code-Level Security: Input Validation & Injection**
- `input-validation.md` - Syntactic, semantic, business logic validation, whitelist vs blacklist
- `sql-injection.md` - Parameterized queries, prepared statements, least privilege DB users
- `xss-prevention.md` - Output encoding, CSP headers, HTTPOnly cookies, DOM sanitization

### [03-request-and-file-security/](./03-request-and-file-security/)
**Code-Level Security: Request & File Handling**
- `csrf-ssrf.md` - CSRF tokens, SameSite cookies, SSRF URL validation
- `file-security.md` - File upload validation (magic bytes), path traversal prevention (8 strategies)

### [04-cryptography-and-transport/](./04-cryptography-and-transport/)
**Code-Level Security: Encryption & Secrets**
- `secrets-crypto.md` - Secrets managers, approved algorithms (AES-256-GCM, Argon2id), key rotation
- `transport-security.md` - HTTPS enforcement, HSTS headers, TLS 1.3, encryption at rest/transit

### [05-database-and-rate-limiting/](./05-database-and-rate-limiting/)
**Code-Level Security: Database & Abuse Prevention**
- `database-security.md` - Row Level Security (RLS), PostgreSQL/Supabase policies, tenant isolation
- `rate-limiting.md` - Sliding window rate limiting, CAPTCHA (reCAPTCHA v3), progressive challenges

### [06-operations/](./06-operations/)
**Code-Level Security: Operational Controls**
- `audit-logging.md` - Tamper-proof logging, cryptographic chaining, WORM storage, fail-safe design
- `error-handling.md` - Generic user errors, detailed internal logs, error IDs, environment-specific verbosity
- `dependency-security.md` - npm/cargo/pip audit, supply chain attacks, SRI, lock files

### [07-compliance/](./07-compliance/)
**Standards & Checklists**
- `standards.md` - ISO 27001 (CIA triad), NIST SP 800-53/171/88, PCI DSS (12 requirements), complete security checklist

### [08-security-policies/](./08-security-policies/)
**Operational Policies (Procedures, Not Code)**
- `README.md` - Policy overview, scope, compliance mapping
- `threat-modeling.md` - STRIDE, PASTA, DREAD methodologies, attack trees
- `incident-response.md` - NIST SP 800-61 four-phase lifecycle, playbooks, post-mortems
- `backup-disaster-recovery.md` - RTO/RPO tiers, 3-2-1 rule, FedRAMP contingency planning
- `security-training.md` - Role-based training, phishing simulation, ISO 27001/NIST SP 800-50
- `penetration-testing.md` - Black/white/gray box, CVSS severity, NIST SP 800-115, PCI DSS
- `privacy-compliance.md` - GDPR/CCPA requirements, privacy-by-design, DPIAs, individual rights

### [09-api-security/](./09-api-security/)
**API-Specific Security (GraphQL, REST, gRPC)**
- `graphql-security.md` - Introspection attacks, query depth limits, batch query DoS, field-level auth, N+1 prevention
- `rest-api-security.md` - API versioning/deprecation, mandatory pagination, HTTP method restrictions, UUID vs sequential IDs, idempotency keys
- `grpc-security.md` - Server reflection attacks, TLS 1.3, authentication interceptors, protobuf limits, stream security

---

## How to Use This Structure

### For AI Agents
1. **Security checklist is mandatory** - Review `07-compliance/standards.md` checklist before every commit
2. **Reference specific files** - Link directly to relevant security files in code reviews
3. **Cross-reference policies** - Code-level files (01-07) implement policies from folder 08

### For Developers
1. **Start with the checklist** - `07-compliance/standards.md` contains the complete pre-commit security checklist
2. **Code-level vulnerabilities** - Folders 01-07 provide implementation guidance for secure coding
3. **Operational procedures** - Folder 08 contains organizational security policies and procedures

### For Security Teams
1. **Compliance mapping** - Each policy file maps to relevant standards (NIST, ISO, PCI DSS, GDPR)
2. **Threat modeling** - Use `08-security-policies/threat-modeling.md` for security design reviews
3. **Incident response** - Follow `08-security-policies/incident-response.md` for breach handling

---

## Critical Security Areas Covered

**28 comprehensive security domains:**
- Access Control (5 areas)
- Authentication & Session Management (3 areas)
- Input Validation & Injection Prevention (7 areas)
- Request Security (2 areas)
- File & Upload Security (2 areas)
- Cryptography & Secrets Management (3 areas)
- Transport & Network Security (3 areas)
- Database Security (1 area)
- Rate Limiting & Bot Prevention (2 areas)
- Logging & Monitoring (1 area)
- Error Handling (1 area)  
- Dependency Management (1 area)
- Compliance Standards (3 areas)
- API Security (3 areas: GraphQL, REST, gRPC)

---

## Separation of Concerns

### Code-Level Vulnerabilities (Folders 01-07)
**What:** Technical implementation details for developers
**Examples:** Parameterized queries, output encoding, JWT verification, path traversal prevention
**Audience:** Developers, code reviewers, security engineers

### Operational Policies (Folder 08)
**What:** Organizational procedures and governance
**Examples:** Incident response playbooks, backup schedules, security training programs, penetration testing frequency
**Audience:** Security teams, compliance officers, management

---

## Version

**Security Canon Version:** 2.0 (Modular)  
**Date:** December 30, 2025  
**Based on:** OWASP Top 10 (2024), NIST 800-53, ISO 27001, PCI DSS, FedRAMP, GDPR, CCPA

**Previous Version:** 1.0 (Monolithic `security-canon.md` - 2,953 lines, now archived in `.bkp/`)

---

## Quick Reference

### Most Critical Files
1. **`07-compliance/standards.md`** - Complete security checklist (use before EVERY commit)
2. **`01-access-and-authentication/access-control.md`** - OWASP #1 vulnerability
3. **`03-request-and-file-security/file-security.md`** - Path traversal (CVSS 9.1 CRITICAL)
4. **`08-security-policies/incident-response.md`** - Breach response procedures

### Government/Enterprise Required
- `08-security-policies/threat-modeling.md` (NIST SP 800-154)
- `08-security-policies/backup-disaster-recovery.md` (FedRAMP, NIST SP 800-34)
- `08-security-policies/penetration-testing.md` (NIST SP 800-115, PCI DSS)
- `08-security-policies/privacy-compliance.md` (GDPR, CCPA)

---

**If ANY security requirement is unclear, refer to the specific file. If still unclear, STOP and request clarification.**
