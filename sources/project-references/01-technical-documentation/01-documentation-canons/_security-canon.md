# Canon: Security Documentation

## Purpose

Security documentation provides comprehensive guidance on threat models, security architecture, authentication mechanisms, encryption strategies, compliance requirements, and incident response procedures. It ensures secure system design, regulatory compliance, and rapid security incident response.

---

## Scope

**This canon applies to:**
- Threat modeling and risk assessment
- Authentication and authorization mechanisms
- Data encryption (at rest and in transit)
- Security architecture and defense-in-depth
- Compliance requirements (GDPR, PCI-DSS, etc.)
- Security incident response procedures
- Vulnerability management

**This canon does NOT apply to:**
- Code security best practices (document in development guidelines)
- Network security configurations (use infrastructure documentation)
- Physical security (separate security domain)

---

## Access Level Classification

**Security Documentation:**
- **Access Level:** Restricted (Level 3)
- **Distribution:** Security team, senior engineers, core development team (need-to-know basis)
- **Storage:** Encrypted private repository with strict access control
- **Review:** Security team review, CISO approval required
- **Rationale:** Contains threat models, vulnerability details, security weaknesses, attack surfaces

**Exception:** General security guidelines may be Internal (Level 2) for all engineers

**Critical:** Threat models and vulnerability details are highly sensitive and must be protected

---

## When to Generate

### Initial Creation
- **Design Phase:** Threat modeling before implementation
- **Architecture Review:** Security architecture design
- **Compliance Planning:** Before handling regulated data

### Updates
- After security audits or penetration tests
- After security incidents
- When adding new attack surfaces
- Quarterly security reviews

### Frequency
- **Initial:** During system design phase
- **Post-Incident:** Within 48 hours of security incident
- **Regular Review:** Quarterly for threat model updates
- **Compliance:** Annual for regulatory requirements

---

## Files to Generate

Agent must create the following files when documenting security:

### 1. Security Documentation Index
**File:** `/docs/source/security/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Security documentation entry point

### 2. Security Overview
**File:** `/docs/source/security/01-security-overview.rst`  
**Format:** reStructuredText  
**Purpose:** High-level security architecture and principles

### 3. Threat Model
**File:** `/docs/source/security/02-threat-model.rst`  
**Format:** reStructuredText  
**Purpose:** STRIDE threat analysis, attack surfaces, mitigations

### 4. Authentication & Authorization
**File:** `/docs/source/security/03-authentication-authorization.rst`  
**Format:** reStructuredText  
**Purpose:** Auth mechanisms, RBAC, session management

### 5. Data Encryption
**File:** `/docs/source/security/04-encryption.rst`  
**Format:** reStructuredText  
**Purpose:** Encryption at rest, in transit, key management

### 6. Compliance
**File:** `/docs/source/security/05-compliance.rst`  
**Format:** reStructuredText  
**Purpose:** Regulatory requirements (GDPR, PCI-DSS, etc.)

### 7. Incident Response
**File:** `/docs/source/security/06-incident-response.rst`  
**Format:** reStructuredText  
**Purpose:** Security incident response playbook

---

## Directory Structure

```
docs/source/security/
├── 00-index.rst                    # Security documentation entry point
├── 01-security-overview.rst        # Security architecture overview
├── 02-threat-model.rst             # STRIDE threat analysis
├── 03-authentication-authorization.rst  # Auth mechanisms
├── 04-encryption.rst               # Encryption strategies
├── 05-compliance.rst               # Regulatory compliance
└── 06-incident-response.rst        # Security incident procedures
```

---

## Generation Rules

### Threat Modeling

Use **STRIDE** framework:
- **S**poofing
- **T**ampering
- **R**epudiation
- **I**nformation Disclosure
- **D**enial of Service
- **E**levation of Privilege

For each threat:
1. Describe attack vector
2. Assess likelihood and impact
3. Document mitigation
4. Assign owner for remediation

### Sensitivity Marking

Mark sensitive sections clearly:

```rst
.. danger::
   RESTRICTED - Level 3 Access
   This section contains vulnerability details.
   Access restricted to security team only.
```

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice
- Specific over vague (exact threats, mitigations)
- Clear, actionable procedures
- **Avoid revealing specific vulnerabilities in examples**

---

## Content Guidelines

### Security Index (`/docs/source/security/00-index.rst`)

```rst
Security Documentation
======================

.. danger::
   RESTRICTED DOCUMENTATION - Level 3 Access
   This documentation contains sensitive security information.
   Access restricted to security team and authorized personnel.
   Do not share externally or with unauthorized internal parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

This documentation covers security architecture, threat models, and incident response for
the Tax Management System.

**Security Classification**: Production System (Financial Data)  
**Last Threat Model Review**: December 2025  
**Last Penetration Test**: November 2025  
**Compliance**: GDPR, PCI-DSS Level 2

Quick Access
------------

**For Security Incidents:**
1. Follow :doc:`06-incident-response` procedures
2. Notify security team: security@example.com
3. Page on-call security engineer (PagerDuty)

**For New Features:**
1. Review :doc:`02-threat-model` for similar features
2. Conduct threat modeling session
3. Update threat model documentation

.. toctree::
   :maxdepth: 2

   01-security-overview
   02-threat-model
   03-authentication-authorization
   04-encryption
   05-compliance
   06-incident-response

Security Principles
-------------------

**Defense in Depth**
- Multiple security layers (network, application, data)
- Assume breach mentality
- Fail securely

**Least Privilege**
- Minimum necessary permissions
- Regular access reviews
- Just-in-time access elevation

**Zero Trust**
- Verify every request
- Assume internal network is hostile
- mTLS for all internal communication

Security Metrics
----------------

**Current Security Posture:**
- Open vulnerabilities: 0 Critical, 2 High, 5 Medium
- Mean Time to Remediate (MTTR): 7 days for High
- Penetration test findings: 3 (all remediated)
- Security incidents (last 12 months): 0

Contact Information
-------------------

- **Security Team**: security@example.com
- **CISO**: ciso@example.com
- **On-Call Security**: security-oncall@pagerduty (24/7)
- **AWS Security**: Premium support
```

### Threat Model (`/docs/source/security/02-threat-model.rst`)

```rst
Threat Model
============

.. danger::
   RESTRICTED - Level 3 Access
   This threat model contains vulnerability analysis.
   Distribution limited to security team and authorized engineers.

Threat Modeling Methodology
----------------------------

**Framework**: STRIDE  
**Last Updated**: December 2025  
**Next Review**: March 2026

System Boundaries
-----------------

**In Scope:**
- Web application
- REST API
- Backend microservices
- Database
- Integration with external systems (KRA, M-Pesa)

**Out of Scope:**
- AWS infrastructure (covered by AWS security)
- Physical security
- End-user devices

Attack Surface Analysis
-----------------------

**External Attack Surface:**

1. **Web Application** (``https://app.example.com``)
   - Entry point: User authentication
   - Attack vectors: XSS, CSRF, credential stuffing
   - Exposed data: User sessions, tax calculations

2. **REST API** (``https://api.example.com``)
   - Entry point: Public API endpoints
   - Attack vectors: API key theft, rate limit bypass, injection attacks
   - Exposed data: User data, tax calculations, receipts

**Internal Attack Surface:**

3. **Backend Services**
   - Entry point: Internal gRPC endpoints
   - Attack vectors: Privilege escalation, lateral movement
   - Exposed data: Database credentials, service tokens

4. **Database**
   - Entry point: SQL connections from backend
   - Attack vectors: SQL injection, credential theft
   - Exposed data: All system data

STRIDE Analysis
---------------

Spoofing Identity
~~~~~~~~~~~~~~~~~

**Threat**: Attacker impersonates legitimate user

**Attack Vectors:**
- Stolen credentials (phishing)
- Session hijacking (XSS, network sniffing)
- API key theft

**Mitigations:**
- ✅ Multi-factor authentication (MFA) enforced for admins
- ✅ HTTP-only, Secure cookies for sessions
- ✅ JWT tokens with 15-minute expiry
- ✅ API key rotation every 90 days
- ⚠️ MFA optional for regular users (TODO: Enforce by Q2 2026)

**Residual Risk**: Medium (until MFA enforced for all users)

Tampering Data
~~~~~~~~~~~~~~

**Threat**: Attacker modifies data in transit or at rest

**Attack Vectors:**
- Man-in-the-middle attacks
- Database injection
- File tampering in S3

**Mitigations:**
- ✅ TLS 1.3 for all external communication
- ✅ mTLS for internal service communication
- ✅ Prepared statements prevent SQL injection
- ✅ S3 object versioning enabled
- ✅ Database audit logging captures all modifications

**Residual Risk**: Low

Repudiation
~~~~~~~~~~~

**Threat**: User denies performing an action

**Attack Vectors:**
- Lack of audit trail
- Shared credentials

**Mitigations:**
- ✅ Comprehensive audit logging (all API calls, database changes)
- ✅ Logs immutable (write-only to CloudWatch)
- ✅ Shared credentials prohibited (enforced in onboarding)

**Residual Risk**: Low

Information Disclosure
~~~~~~~~~~~~~~~~~~~~~~

**Threat**: Unauthorized access to sensitive data

**Attack Vectors:**
- SQL injection revealing user data
- Insecure direct object references (IDOR)
- Exposed error messages revealing system details
- S3 bucket misconfiguration

**Mitigations:**
- ✅ Parameterized queries prevent SQL injection
- ✅ UUID-based identifiers (not sequential integers)
- ✅ Authorization checks on all endpoints
- ✅ Generic error messages (no stack traces in production)
- ✅ S3 buckets private with explicit allow lists
- ✅ Data encryption at rest (AES-256)

**Residual Risk**: Low

Denial of Service
~~~~~~~~~~~~~~~~~

**Threat**: Attacker overwhelms system resources

**Attack Vectors:**
- DDoS attacks on public endpoints
- Resource exhaustion (CPU, memory, database connections)
- Algorithmic complexity attacks

**Mitigations:**
- ✅ AWS Shield Standard (DDoS protection)
- ✅ CloudFlare WAF (rate limiting, bot detection)
- ✅ API rate limiting (100 requests/minute per user)
- ✅ Database connection pooling (max 50 connections)
- ✅ Auto-scaling enabled (target CPU 70%)
- ⚠️ No protection against sophisticated application-layer DoS

**Residual Risk**: Medium (sophisticated attacks possible)

Elevation of Privilege
~~~~~~~~~~~~~~~~~~~~~~~

**Threat**: Attacker gains higher privileges than authorized

**Attack Vectors:**
- Exploiting authorization logic flaws
- JWT token manipulation
- Privilege escalation via API

**Mitigations:**
- ✅ Role-Based Access Control (RBAC) enforced
- ✅ JWT signed with RS256 (asymmetric keys)
- ✅ Authorization checks on every endpoint
- ✅ Principle of least privilege for service accounts
- ✅ Regular access reviews (quarterly)

**Residual Risk**: Low

High-Risk Scenarios
-------------------

**Scenario 1: Database Breach**

**Impact**: CRITICAL (all user data exposed)  
**Likelihood**: Low (encryption, network isolation)  
**Mitigation**:
- Encryption at rest
- Network ACLs (database only accessible from backend)
- Regular security patches

**Scenario 2: API Key Theft**

**Impact**: HIGH (unauthorized access to user accounts)  
**Likelihood**: Medium (phishing, leaked credentials)  
**Mitigation**:
- API key rotation every 90 days
- Anomaly detection on API usage
- MFA for admin accounts

**Scenario 3: Insider Threat**

**Impact**: HIGH (data exfiltration, sabotage)  
**Likelihood**: Low (trusted employees)  
**Mitigation**:
- Principle of least privilege
- Audit logging of all access
- Background checks for employees

Recommended Actions
-------------------

**Priority 1 (Complete by Q1 2026):**
1. Enforce MFA for all users (not just admins)
2. Implement application-layer DoS protection
3. Conduct annual penetration test

**Priority 2 (Complete by Q2 2026):**
1. Implement anomaly detection for API usage
2. Add data loss prevention (DLP) controls
3. Conduct security awareness training

Review Schedule
---------------

- **Threat Model**: Quarterly
- **Penetration Testing**: Annual
- **Vulnerability Scanning**: Continuous (automated)
- **Access Reviews**: Quarterly
```

### Authentication & Authorization (`/docs/source/security/03-authentication-authorization.rst`)

```rst
Authentication & Authorization
===============================

Authentication mechanisms and authorization controls.

Authentication Mechanisms
-------------------------

**Primary**: JWT (JSON Web Tokens)  
**Algorithm**: RS256 (RSA with SHA-256)  
**Token Expiry**: 15 minutes (access token), 7 days (refresh token)

**Login Flow:**

1. User submits email + password
2. Backend validates credentials (bcrypt compare)
3. Backend generates JWT access token (15-minute expiry)
4. Backend generates refresh token (7-day expiry, stored in HTTP-only cookie)
5. Client includes access token in Authorization header
6. When access token expires, client uses refresh token to obtain new access token

**Multi-Factor Authentication (MFA):**

- TOTP-based (Google Authenticator, Authy)
- Enforced for admin accounts
- Optional for regular users (TODO: Enforce by Q2 2026)

Password Requirements
---------------------

**Minimum Length**: 12 characters  
**Complexity**: At least one uppercase, lowercase, digit, special character  
**Hashing**: bcrypt (cost factor 12)  
**Storage**: Hashed passwords only (never plaintext)

**Password Reset:**

1. User requests password reset
2. Backend generates secure token (32 bytes random)
3. Token sent via email (expires in 1 hour)
4. User clicks link, sets new password
5. All existing sessions invalidated

Authorization (RBAC)
--------------------

**Roles:**

========================  ================================================================
Role                      Permissions
========================  ================================================================
``user``                  Access own data, create tax calculations, view receipts
``admin``                 All user permissions + view all users, manage tax brackets
``system_admin``          All admin permissions + system configuration, user management
========================  ================================================================

**Permission Checks:**

Every API endpoint checks:

1. Valid JWT token
2. Token not expired
3. User has required role
4. User has access to requested resource (ownership check)

**Example Authorization Check:**

.. code-block:: python

   @require_role("admin")
   def get_all_users(request):
       # Only admins can list all users
       return User.query.all()

   @require_ownership
   def get_user_calculations(request, user_id):
       # Users can only view their own calculations
       if request.user.id != user_id and request.user.role != "admin":
           raise Forbidden("Access denied")
       return TaxCalculation.query.filter_by(user_id=user_id).all()

Session Management
------------------

**Session Storage**: Redis (in-memory)  
**Session TTL**: 24 hours (idle timeout)  
**Session ID**: 32-byte random (cryptographically secure)

**Session Invalidation:**

- Logout: Immediate invalidation
- Password change: All sessions invalidated
- Role change: All sessions invalidated
- Manual revocation: Admin can revoke user sessions

API Key Authentication
----------------------

**Usage**: Third-party integrations (rare, internal use only)  
**Generation**: 64-byte random (Base64 encoded)  
**Rotation**: Every 90 days (automated)  
**Storage**: Hashed (SHA-256) in database

**Rate Limiting:**

- API keys: 1,000 requests/hour
- User sessions: 100 requests/minute

Security Best Practices
-----------------------

**Avoid:**
- Storing passwords in plaintext
- Using predictable session IDs
- Sharing credentials between users

**Do:**
- Rotate API keys regularly
- Use secure random for tokens
- Validate all inputs
- Log authentication failures
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all security reST files
rstcheck docs/source/security/*.rst
```

**Expected output:** No errors

### Sensitivity Check

- [ ] All threat details marked as Restricted (Level 3)
- [ ] No specific exploitation details included
- [ ] Mitigations documented without revealing vulnerabilities

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

---

## Examples Reference

See working example: `02-examples/security-example/` (to be created)

**Example includes:**
- Complete security documentation
- Threat model (sanitized for example)
- Auth/authorization guide

---

## Access Level Warning

Include at top of ALL security docs:

```rst
.. danger::
   RESTRICTED DOCUMENTATION - Level 3 Access
   This documentation contains sensitive security information.
   Distribution limited to security team and authorized personnel.
```

---

## Agent Checklist

Before marking security documentation complete, verify:

- [ ] Security index created
- [ ] Security overview with principles
- [ ] Threat model using STRIDE framework
- [ ] Authentication mechanisms documented
- [ ] Authorization (RBAC) documented
- [ ] Encryption strategies documented (at rest, in transit)
- [ ] Compliance requirements documented
- [ ] Incident response procedures documented
- [ ] All sections marked as Restricted (Level 3)
- [ ] No specific exploitation details revealed
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial security documentation canon
- Based on STRIDE threat modeling
- Follows `_docs-canon.md` v4 specifications
