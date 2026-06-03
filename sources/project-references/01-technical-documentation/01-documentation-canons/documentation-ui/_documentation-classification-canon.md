# Canon: Documentation Classification (Public vs Private)

## Purpose

This canon defines criteria and procedures for classifying technical documentation as public, internal, restricted, or confidential. It addresses security risks, intellectual property protection, trade secret considerations, and competitive advantage preservation.

---

## Scope

**This canon applies to:**
- All technical documentation (API specs, architecture, deployment, security)
- Configuration files and environment documentation
- Operational runbooks and incident response plans
- Database schemas and data models
- Design system documentation
- Admin panel specifications

**This canon does NOT apply to:**
- Source code (covered by code repository access controls)
- Binary artifacts (covered by artifact repository policies)
- Communication (covered by communication policies)

---

## Access Level Framework

### Level 1: Public

**Definition:** Content safe for unrestricted public access.

**Characteristics:**
- No security vulnerabilities exposed
- No proprietary business logic revealed
- No competitive advantage disclosed
- No internal infrastructure details
- No authentication/authorization mechanisms
- No sensitive data schemas
- No operational procedures

**Examples:**
- Product feature documentation (user-facing)
- Public API reference (read-only endpoints)
- Getting started guides
- General architecture overview (high-level only)
- Public design system (UI components, not implementation)
- Open source project documentation

**Distribution:**
- Public website (no authentication)
- Search engine indexed
- Cach permittedable by CDN
- Shareable without restriction

---

### Level 2: Internal

**Definition:** Content for employees and authorized personnel only.

**Characteristics:**
- Contains implementation details
- Reveals technology stack choices
- Shows internal service dependencies
- Describes development workflows
- Includes non-critical security patterns
- Contains internal API documentation
- Shows database schema (without sensitive data)

**Examples:**
- Complete architecture documentation
- Deployment procedures (standard)
- Internal API specifications
- Database schema documentation
- Development environment setup
- Testing strategies
- Design system implementation

**Distribution:**
- Private repository (Git, internal wiki)
- VPN-only access
- Employee SSO authentication
- NDAs required for contractors

**Security Controls:**
- Authentication required
- Session management (8-24 hours)
- Audit logging
- Access review quarterly

---

### Level 3: Restricted

**Definition:** Need-to-know basis only. Core team, leadership, security personnel.

**Characteristics:**
- Contains security vulnerabilities or mitigations
- Reveals proprietary algorithms
- Shows attack surface details
- Includes incident response procedures
- Contains privileged access procedures
- Describes moderation/ban workflows
- Shows rate limiting strategies

**Examples:**
- Security architecture (threat models, attack mitigations)
- Admin panel specifications
- Incident response playbooks
- Disaster recovery procedures
- Penetration testing reports
- Vulnerability assessments
- Trade secret algorithms
- Competitive intelligence

**Distribution:**
- Encrypted storage only
- Multi-factor authentication required
- IP allowlist (office networks only)
- Individual access approval
- No downloads (view-only)
- Watermarked per-user

**Security Controls:**
- MFA mandatory
- Session timeout: 1 hour
- Audit logging with tamper detection
- Access review monthly
- Automatic session termination on IP change

---

### Level 4: Confidential

**Definition:** Executive, board, or legal only.

**Characteristics:**
- Contains financial projections
- Reveals M&A plans
- Shows strategic roadmaps
- Includes legal strategies
- Contains executive compensation
- Reveals customer data analysis
- Shows compliance violations

**Examples:**
- Financial models
- Strategic business plans
- Legal case files
- Customer PII aggregation reports
- Executive performance reviews
- Board meeting minutes

**Distribution:**
- Air-gapped systems (offline-only)
- Physical documents in secured locations
- Encrypted with individual decryption keys
- No electronic transmission
- Printed copies numbered and tracked

**Security Controls:**
- Hardware tokens required
- Biometric authentication
- Physical access logs
- Document destruction procedures
- No copy/paste, no screenshots

---

## Classification Criteria

### Security Risk Assessment

**Ask these questions:**

1. **Attack Surface Exposure**
   - Does this documentation reveal admin endpoints?
   - Does it show authentication mechanisms?
   - Does it describe authorization logic?
   - Does it expose API rate limits or thresholds?
   - Does it detail input validation rules?
   
   **If YES to any:** Minimum Level 3 (Restricted)

2. **Infrastructure Disclosure**
   - Does this show internal network topology?
   - Does it reveal server configurations?
   - Does it expose database connection strings?
   - Does it describe disaster recovery procedures?
   - Does it show backup locations?
   
   **If YES to any:** Minimum Level 2 (Internal)

3. **Business Logic**
   - Does this contain proprietary algorithms?
   - Does it reveal pricing calculations?
   - Does it show recommendation systems?
   - Does it describe fraud detection rules?
   - Does it expose moderation workflows?
   
   **If YES to any:** Minimum Level 3 (Restricted)

4. **Competitive Advantage**
   - Does this reveal unique features before launch?
   - Does it show technology stack choices?
   - Does it describe optimization techniques?
   - Does it expose performance metrics?
   - Does it detail scaling strategies?
   
   **If YES to any:** Minimum Level 2 (Internal)

5. **Compliance and Legal**
   - Does this contain customer PII schemas?
   - Does it show data retention policies?
   - Does it describe GDPR/CCPA implementation?
   - Does it reveal audit findings?
   - Does it expose compliance gaps?
   
   **If YES to any:** Minimum Level 3 (Restricted)

### Trade Secret Evaluation

**DAAS (Data as a Service) Protection:**

**Definition:** Documentation that, if disclosed, would enable competitors to replicate proprietary systems, algorithms, or processes that provide competitive advantage.

**Examples of Trade Secrets in Documentation:**

1. **Proprietary Algorithms**
   - Custom recommendation engines
   - Fraud detection models
   - Search ranking algorithms
   - Optimization techniques
   - Machine learning model architectures

2. **Business Logic**
   - Pricing calculation formulas
   - Discount tier structures
   - Loyalty program mechanics
   - Moderation decision trees
   - Content ranking systems

3. **Integration Patterns**
   - Third-party API orchestration
   - Data transformation pipelines
   - Real-time processing workflows
   - Cache invalidation strategies

4. **Performance Optimizations**
   - Database query optimizations
   - Caching layer strategies
   - CDN configuration patterns
   - Load balancing algorithms

**Classification:** All trade secrets are **Level 3 (Restricted)** minimum.

**Protection Measures:**
- Watermark with user ID on each page
- Audit log all access
- Require written justification for access
- Annual access re-approval
- Non-compete agreements for viewers

---

## Specific Documentation Type Classification

### API Documentation

**Public API (Read-Only):**
- Access Level: **Level 1 (Public)**
- Examples: GET /articles, GET /projects, GET /comments
- Excludes: Rate limits, authentication details

**Public API (Write Operations):**
- Access Level: **Level 2 (Internal)**
- Examples: POST /contact, POST /testimonials/submit
- Rationale: Shows input validation requirements

**Admin API:**
- Access Level: **Level 3 (Restricted)**
- Examples: POST /admin/articles, DELETE /admin/comments
- Rationale: Attack surface for privilege escalation

**Internal API:**
- Access Level: **Level 2 (Internal)**
- Examples: Service-to-service communication
- Rationale: Reveals system architecture

---

### Architecture Documentation

**High-Level Overview:**
- Access Level: **Level 1 (Public)**
- Contents: "We use microservices on AWS"
- Purpose: Marketing, recruiting

**System Architecture:**
- Access Level: **Level 2 (Internal)**
- Contents: Component diagrams, service dependencies
- Purpose: Development team reference

**Security Architecture:**
- Access Level: **Level 3 (Restricted)**
- Contents: Threat models, attack mitigations
- Purpose: Security team, compliance audits

---

### Deployment Documentation

**Public Cloud Deployment:**
- Access Level: **Level 2 (Internal)**
- Contents: Terraform configs, Kubernetes manifests
- Rationale: Reveals infrastructure choices

**Self-Hosted Deployment:**
- Access Level: **Level 1 (Public)** if offering self-hosting
- Access Level: **Level 2 (Internal)** if internal-only

**Disaster Recovery:**
- Access Level: **Level 3 (Restricted)**
- Contents: Backup procedures, failover processes
- Rationale: Attack vector for data exfiltration

---

### Database Documentation

**Schema (Public API Data):**
- Access Level: **Level 2 (Internal)**
- Contents: Tables for articles, projects, comments
- Rationale: Shows data model design

**Schema (Sensitive Data):**
- Access Level: **Level 3 (Restricted)**
- Contents: Users, sessions, audit logs
- Rationale: Contains PII structures

**Migration Scripts:**
- Access Level: **Level 2 (Internal)**
- Rationale: Shows database evolution

---

### Security Documentation

**General Security Practices:**
- Access Level: **Level 1 (Public)**
- Contents: "We use HTTPS, encrypt data at rest"
- Purpose: Trust building

**Security Controls:**
- Access Level: **Level 3 (Restricted)**
- Contents: Specific implementations, rate limits
- Rationale: Reveals evasion opportunities

**Vulnerability Assessments:**
- Access Level: **Level 3 (Restricted)**
- Contents: Pentest results, findings
- Rationale: Direct attack blueprint

**Incident Response:**
- Access Level: **Level 3 (Restricted)**
- Contents: Playbooks, escalation procedures
- Rationale: Shows organizational weaknesses

---

### Operations Documentation

**Monitoring:**
- Access Level: **Level 2 (Internal)**
- Contents: Metrics, dashboards, alert thresholds
- Rationale: Shows system health visibility

**Runbooks:**
- Access Level: **Level 3 (Restricted)**
- Contents: Incident response, troubleshooting
- Rationale: Could reveal vulnerabilities

**Backup Procedures:**
- Access Level: **Level 3 (Restricted)**
- Contents: Backup frequency, retention, restore
- Rationale: Data exfiltration vector

---

### Design System Documentation

**UI Component Library:**
- Access Level: **Level 1 (Public)**
- Contents: React components, CSS, usage examples
- Purpose: Open source, recruiting

**Design Tokens:**
- Access Level: **Level 1 (Public)**
- Contents: Colors, typography, spacing
- Purpose: Consistency, third-party integrations

**Implementation Details:**
- Access Level: **Level 2 (Internal)**
- Contents: Build process, optimization techniques
- Rationale: Competitive advantage

---

### Admin Panel Documentation

**Feature Overview:**
- Access Level: **Level 2 (Internal)**
- Contents: "Admin can ban users, delete comments"
- Purpose: Product documentation

**Admin API Endpoints:**
- Access Level: **Level 3 (Restricted)**
- Contents: POST /admin/users/:id/ban
- Rationale: Privilege escalation attack vector

**Moderation Workflows:**
- Access Level: **Level 3 (Restricted)**
- Contents: Ban criteria, appeal process
- Rationale: Evasion techniques

---

## Additional Classification Constraints

### 1. Geographic and Regulatory Compliance

**GDPR (Europe):**
- Documentation showing PII processing: **Level 3 (Restricted)**
- Data retention policies: **Level 3 (Restricted)**
- User consent mechanisms: **Level 2 (Internal)**

**CCPA (California):**
- Data sale disclosures: **Level 3 (Restricted)**
- User rights implementation: **Level 2 (Internal)**

**HIPAA (Healthcare):**
- PHI handling: **Level 3 (Restricted)**
- Audit logs: **Level 3 (Restricted)**

### 2. Vendor and Third-Party Considerations

**SaaS Provider Documentation:**
- Integration guides: **Level 1 (Public)** if officially partnered
- API keys/secrets: **Never document** (use secret management)
- Rate limits: **Level 2 (Internal)**

**Open Source Dependencies:**
- Usage documentation: **Level 1 (Public)**
- Customizations: **Level 2 (Internal)**
- Security patches: **Level 3 (Restricted)** until applied

### 3. Time-Based Classification

**Pre-Launch Features:**
- Minimum: **Level 2 (Internal)**
- After public launch: **Re-evaluate for Level 1**

**Deprecated Features:**
- Minimum: **Level 2 (Internal)**
- Never downgrade to Public (reveals historical vulnerabilities)

### 4. Aggregated Data

**Individual Metrics:**
- User-specific: **Level 3 (Restricted)**
- Anonymized aggregates: **Level 1 (Public)** if marketing-appropriate

### 5. Error Messages and Debugging

**Error Code Documentation:**
- User-facing errors: **Level 1 (Public)**
- Internal error codes: **Level 2 (Internal)**
- Stack traces: **Never document** (debug logs only)

### 6. Configuration and Environment Variables

**Public Configuration:**
- Feature flags (boolean): **Level 1 (Public)**
- Default settings: **Level 1 (Public)**

**Internal Configuration:**
- Timeout values: **Level 2 (Internal)**
- Connection pool sizes: **Level 2 (Internal)**

**Secret Configuration:**
- API keys: **Never document** (use secret management)
- Encryption keys: **Never document**

---

## Implementation Guidelines

### Documentation Tagging

**In RST Files:**

```rst
:Access Level: Internal (Level 2)
:Classification: Trade Secret
:Review Date: 2026-07-01
:Approved By: John Kibocha
```

**In OpenAPI Specs:**

```yaml
info:
  title: Admin API
  x-access-level: restricted  # Level 3
  x-classification: trade-secret
```

### Build Configuration

**Separate Builds:**

```python
# public-conf.py
exclude_patterns = [
    'admin/**',
    'security/**',
    '**/private/**',
]

# private-conf.py
include_patterns = [
    'admin/**',
    'security/**',
]
```

### Deployment Structure

```
docs.example.com/
├── /                  # Public documentation
├── /internal/         # Internal (Level 2) - Employee SSO
└── /restricted/       # Restricted (Level 3) - MFA + IP allowlist
```

---

## Declassification Procedures

**When to Declassify:**
- Feature launched publicly
- Security vulnerability patched and disclosed
- Competitive advantage no longer relevant
- Regulatory requirement expired

**Approval Process:**
1. Request declassification in writing
2. Security team review (1 week)
3. Legal team approval (if Level 3+)
4. Executive sign-off (if Level 4)
5. Update documentation metadata
6. Redeploy with new classification

**Never Declassify:**
- User PII schemas
- Authentication mechanisms
- Encryption implementations
- Audit log structures

---

## Reclassification Triggers

**Immediate Reclassification to Level 3:**
- Security vulnerability discovered
- Trade secret litigation
- Regulatory investigation
- Competitor replication

**Process:**
1. Immediate removal from public access
2. Security incident investigation
3. Legal review
4. Update classification
5. Notify affected teams

---

## Audit and Compliance

### Annual Review

**Process:**
- Review all Level 1 (Public) documentation
- Verify no Level 2+ content leaked to public
- Check all Level 3 (Restricted) access logs
- Update classifications based on business changes

### Access Audits

**Frequency:**
- Level 2: Quarterly
- Level 3: Monthly
- Level 4: Weekly

**Procedure:**
- Review access logs
- Verify user roles still appropriate
- Remove access for departed employees
- Check for anomalous access patterns

---

## Exceptions and Overrides

**When Public Disclosure Required:**
- Open source project documentation
- Security vulnerability disclosure (coordinated)
- Regulatory compliance (SOC 2, ISO 27001 reports)
- Legal subpoena

**Approval Process:**
1. Written request with justification
2. Legal review
3. Executive approval
4. Limited-time access grant
5. Audit trail maintained

---

## Tools and Automation

**Automated Classification:**
- Scan for keywords: "admin", "secret", "private", "internal"
- Flag potential misclassifications
- Require manual review

**Access Control:**
- Cloudflare Access (OAuth + MFA)
- IP allowlisting
- Session management
- Audit logging

**Watermarking:**
- Per-user watermarks on Level 3+ docs
- Tracking pixel for view detection
- Download prevention (view-only)

---

## Examples

See `02-examples/documentation-classification-example/` for:
- Sample classification matrix
- Build configuration examples
- Deployment structure
- Access control setup

---

## References

- **NIST SP 800-53:** Security Controls
- **ISO 27001:** Information Security Management
- **OWASP ASVS:** Application Security Verification Standard
- **Trade Secrets Act (US):** Legal framework for trade secret protection

---

**Version:** 1.0.0
**Last Updated:** January 19, 2026
