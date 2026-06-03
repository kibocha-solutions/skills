# Access Levels Classification Guide

## Purpose

This guide defines the four-level access classification system for all documentation. Every document must be assigned an access level determining who can view it, where it's stored, and how it's distributed.

---

## Access Level Overview

```
┌─────────────────────────────────────────────────┐
│  Level 1: PUBLIC                                 │
│  ├─ End users, customers, general public        │
│  ├─ Public repositories, documentation sites    │
│  └─ No authentication required                  │
├─────────────────────────────────────────────────┤
│  Level 2: INTERNAL                              │
│  ├─ Employees, authorized personnel             │
│  ├─ Private repositories, intranet              │
│  └─ Authentication required                     │
├─────────────────────────────────────────────────┤
│  Level 3: RESTRICTED                            │
│  ├─ Core team, leadership (need-to-know)        │
│  ├─ Encrypted repositories, access control      │
│  └─ Strict authentication + authorization       │
├─────────────────────────────────────────────────┤
│  Level 4: CONFIDENTIAL                          │
│  ├─ Executive/board level only                  │
│  ├─ Encrypted storage, audit logs               │
│  └─ Highest security controls                   │
└─────────────────────────────────────────────────┘
```

---

## Level 1: Public

### Definition

Information suitable for public consumption without authentication or authorization.

### Audience

- End users and customers
- Third-party developers
- General public
- Open-source contributors

### Content Examples

**User-Facing:**
- User guides
- Getting started tutorials
- Public API documentation
- FAQs
- Changelogs (for public products)

**Developer-Facing:**
- REST API reference (public APIs)
- SDK documentation
- Integration guides
- Code samples

### Storage

- Public GitHub repositories
- Public documentation sites (Read the Docs, GitHub Pages)
- Company website (docs.example.com)

### Distribution

- No restrictions
- Searchable by search engines
- Shareable publicly

### Document Marking

```rst
.. note::
   PUBLIC DOCUMENTATION - Level 1 Access
   This documentation is publicly available.
```

```markdown
> **Note**: PUBLIC DOCUMENTATION - Level 1 Access  
> This documentation is publicly available.
```

---

## Level 2: Internal

### Definition

Information for internal use by employees and authorized personnel only.

### Audience

- All employees
- Contractors with NDA
- Authorized partners
- Internal developers

### Content Examples

**Technical:**
- Internal API documentation
- Architecture documentation
- Deployment procedures
- Database schema documentation
- Configuration documentation
- Testing documentation

**Operational:**
- Operations runbooks
- Incident response procedures
- Maintenance procedures

**Process:**
- ADRs (Architecture Decision Records)
- Internal changelogs
- Development workflows

### Storage

- Private GitHub repositories
- Internal wiki/Confluence
- Intranet documentation portal
- SharePoint/Google Drive (with authentication)

### Distribution

- Requires company email/SSO
- VPN access may be required
- Not shared outside organization

### Document Marking

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains internal information.
   Do not share with external parties.
```

```markdown
> **Warning**: INTERNAL DOCUMENTATION - Level 2 Access  
> This documentation contains internal information.  
> Do not share with external parties.
```

---

## Level 3: Restricted

### Definition

Highly sensitive information on a need-to-know basis. Access granted only to core team and leadership.

### Audience

- Security team
- Core development team
- Senior engineers
- Technical leadership
- Product leadership

### Content Examples

**Security:**
- Threat models
- Vulnerability assessments
- Penetration test results
- Security incident details
- Cryptographic key management

**Strategic:**
- Competitive analysis
- Unreleased feature plans
- Financial data
- Customer data schemas

### Storage

- Encrypted private repositories
- Secrets management systems (HashiCorp Vault)
- Encrypted cloud storage with access control
- Offline encrypted backups

### Distribution

- Explicit access grants only
- Access logged and audited
- Time-limited access
- Revoked when no longer needed

### Document Marking

```rst
.. danger::
   RESTRICTED DOCUMENTATION - Level 3 Access
   This documentation contains highly sensitive information.
   Distribution limited to authorized personnel only.
   Do not share without explicit approval.
```

```markdown
> **DANGER**: RESTRICTED DOCUMENTATION - Level 3 Access  
> This documentation contains highly sensitive information.  
> Distribution limited to authorized personnel only.  
> Do not share without explicit approval.
```

---

## Level 4: Confidential

### Definition

Extremely sensitive information for executive and board level only.

### Audience

- CEO, CTO, CISO
- Board of directors
- Legal counsel
- Auditors (when required)

### Content Examples

**Executive:**
- M&A documentation
- Financial forecasts
- Compensation structures
- Legal proceedings
- Regulatory compliance details

**Note:** This framework primarily covers Level 1-3. Level 4 typically handled by executive/legal teams.

### Storage

- Highly encrypted systems
- Air-gapped storage
- Physical safes (for extremely sensitive docs)
- Lawyer-held documents

### Distribution

- Explicit CEO/board approval required
- Physical delivery only (no email)
- NDA required before viewing
- Access fully audited

### Document Marking

```rst
.. danger::
   CONFIDENTIAL - Level 4 Access
   EXECUTIVE/BOARD LEVEL ONLY
   Unauthorized access or distribution prohibited.
   Legal consequences apply.
```

---

## Access Level Assignment Matrix

Use this matrix to determine correct access level:

| Documentation Type | Typical Access Level | Notes |
|-------------------|---------------------|-------|
| **User Guide** | Level 1 (Public) | Unless internal tool |
| **REST API (Public)** | Level 1 (Public) | For third-party developers |
| **REST API (Internal)** | Level 2 (Internal) | Service-to-service only |
| **GraphQL API (Public)** | Level 1 (Public) | For third-party developers |
| **GraphQL API (Internal)** | Level 2 (Internal) | Internal data federation |
| **gRPC API** | Level 2 (Internal) | Typically internal only |
| **Architecture** | Level 2 (Internal) | Design details internal |
| **Deployment** | Level 2 (Internal) | Infrastructure details |
| **Operations/Runbooks** | Level 2 (Internal) | Operational procedures |
| **Database Schema** | Level 2 (Internal) | Data structures |
| **Security (General)** | Level 2 (Internal) | Security practices |
| **Security (Threat Model)** | Level 3 (Restricted) | Vulnerability details |
| **Configuration** | Level 2 (Internal) | Parameter details |
| **Testing** | Level 2 (Internal) | Test strategies |
| **ADRs** | Level 2 (Internal) | Strategic decisions |
| **Changelog (Public Product)** | Level 1 (Public) | User-facing changes |
| **Changelog (Internal Tool)** | Level 2 (Internal) | Internal changes |

---

## Decision Tree

Use this flowchart to determine access level:

```
START
  ↓
Is this for end users/customers?
  ├─ YES → Level 1 (Public)
  │
  └─ NO
      ↓
  Contains security vulnerabilities or threats?
      ├─ YES → Level 3 (Restricted)
      │
      └─ NO
          ↓
  For internal employees only?
          ├─ YES → Level 2 (Internal)
          │
          └─ NO → Level 4 (Confidential)
```

---

## Access Control Implementation

### Git Repository Access

**Level 1 (Public):**
```yaml
# .github/workflows/deploy-docs.yml
  - name: Deploy to GitHub Pages
    uses: peaceiris/actions-gh-pages@v3
    with:
      github_token: ${{ secrets.GITHUB_TOKEN }}
      publish_dir: ./docs/build
```

**Level 2 (Internal):**
```yaml
# Requires authentication
# Private repository settings:
# - Private visibility
# - Branch protection enabled
# - Require PR reviews
```

**Level 3 (Restricted):**
```yaml
# Additional controls:
# - Limited team access
# - Audit logging enabled
# - Encryption at rest
# - 2FA required for all users
```

### Documentation Site Access

**Level 1:** Open to public (no auth)

**Level 2:** SSO required

```nginx
# nginx.conf
location /docs {
    auth_request /auth;
    proxy_pass http://docs-server;
}
```

**Level 3:** SSO + IP whitelist + VPN

```nginx
location /docs/restricted {
    satisfy all;
    allow 10.0.0.0/8;  # Internal network
    deny all;
    auth_request /auth;
    proxy_pass http://docs-server;
}
```

---

## Reclassification

### When to Reclassify

Reclassify documents when:

**Upgrade to Higher Level:**
- Security vulnerability discovered
- Competitive sensitivity increases
- Regulatory requirements change

**Downgrade to Lower Level:**
- Information becomes public through other channels
- Threat mitigated and patched
- Product publicly launched

### Reclassification Procedure

1. **Review:** Technical lead reviews document
2. **Approval:** Security team approves (for Level 3)
3. **Update:** Change access level marking in document
4. **Migrate:** Move to appropriate storage location
5. **Notify:** Inform relevant stakeholders
6. **Audit:** Log reclassification decision

---

## Compliance

### GDPR Considerations

**Level 1:** No personal data  
**Level 2:** Anonymized/aggregated data only  
**Level 3:** May contain personal data (need lawful basis)  
**Level 4:** Customer data (highest protection)

### Industry Standards

**SOC 2 Compliance:**
- Level 3+ requires audit logs
- Access reviews quarterly
- Encryption required

**ISO 27001:**
- Document classification mandatory
- Access controls enforced
- Regular reviews required

---

## Best Practices

### General

1. **Default to higher level** when uncertain
2. **Clearly mark all documents** with access level
3. **Review access annually** (or after major changes)
4. **Audit access logs** for Level 3+
5. **Train employees** on classification system

### Red Flags (Require Upgrade)

🚩 Contains customer data  
🚩 Includes authentication credentials  
🚩 Describes security vulnerabilities  
🚩 Contains financial projections  
🚩 Reveals competitive advantages  
🚩 Includes M&A information  

### Never in Documentation

❌ Production passwords or API keys  
❌ Customer PII (personally identifiable information)  
❌ Encryption keys  
❌ Social Security Numbers  
❌ Credit card numbers  

*(Use secrets management systems instead)*

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial access levels classification guide
- Four-level system (Public, Internal, Restricted, Confidential)
- Assignment matrix and decision tree
