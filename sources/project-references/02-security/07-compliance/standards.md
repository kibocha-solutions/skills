# Compliance Standards

## 13.1 ISO 27001

**Definition:**
International standard for Information Security Management Systems (ISMS).

**CIA Triad:**
1. **Confidentiality:** Prevent unauthorized access
2. **Integrity:** Prevent unauthorized modification
3. **Availability:** Ensure systems accessible when needed

**Requirements:**
- Information Security Management System (ISMS)
- Risk assessment process
- Security controls implementation
- Regular audits
- Incident response procedures
- Business continuity planning
- Management commitment
- Continual improvement

**Benefits:**
- Demonstrates security commitment to clients
- Required for government/enterprise contracts
- Supports GDPR, HIPAA, PCI-DSS compliance
- Reduces risk of data breaches
- Improves organizational security culture

**Implementation:**
- Document security policies
- Conduct risk assessments
- Implement security controls
- Train employees
- Monitor and review
- Maintain audit trail
- Annual certification audit

---

## 13.2 NIST Standards

**NIST SP 800-53:** Security and Privacy Controls

Comprehensive catalog covering:
- Access control
- Awareness and training
- Audit and accountability
- Security assessment and authorization
- Configuration management
- Contingency planning
- Identification and authentication
- Incident response
- Maintenance
- Media protection
- Physical and environmental protection
- Planning
- Personnel security
- Risk assessment
- System and services acquisition
- System and communications protection
- System and information integrity

**NIST SP 800-171:** Protecting Controlled Unclassified Information (CUI)

Required for:
- Government contractors
- Organizations handling CUI
- Defense industrial base

**NIST SP 800-88:** Media Sanitization

Guidelines for:
- Secure data deletion
- Hardware disposal
- Clear, Purge, Destroy methods

**NIST Cybersecurity Framework:**
- Identify
- Protect
- Detect
- Respond
- Recover

---

## 13.3 PCI DSS (Payment Card Security)

**Critical for any system that processes, stores, or transmits payment card data.**

**12 Requirements:**

1. Install and maintain firewall configuration to protect cardholder data
2. Do not use vendor-supplied defaults for system passwords and security parameters
3. Protect stored cardholder data
4. Encrypt transmission of cardholder data across open, public networks
5. Protect all systems against malware and regularly update anti-virus software
6. Develop and maintain secure systems and applications
7. Restrict access to cardholder data by business need-to-know
8. Identify and authenticate access to system components
9. Restrict physical access to cardholder data
10. Track and monitor all access to network resources and cardholder data
11. Regularly test security systems and processes
12. Maintain a policy that addresses information security for all personnel

**Critical Change (March 31, 2025):**
Multi-Factor Authentication (MFA) is **MANDATORY** for all access to cardholder data environment.

**Requirements for Payment Systems:**
- Never store CVV/CVC codes (forbidden)
- Encrypt cardholder data at rest (AES-256)
- Encrypt in transit (TLS 1.2 minimum, TLS 1.3 recommended)
- Mask card numbers (show only last 4 digits)
- Implement MFA for all access
- Log all access to payment data
- Quarterly vulnerability scans
- Annual penetration testing
- Network segmentation
- Firewall between internet and cardholder data
- Regular security awareness training

**Compliance Levels:**
- Level 1: 6M+ transactions/year - Annual on-site audit
- Level 2: 1M-6M transactions/year - Annual Self-Assessment Questionnaire
- Level 3: 20K-1M e-commerce transactions/year - Annual SAQ
- Level 4: <20K e-commerce transactions/year - Annual SAQ

**Verification:**
- [ ] PCI DSS compliance level determined
- [ ] All 12 requirements implemented
- [ ] MFA implemented
- [ ] Quarterly scans scheduled
- [ ] Annual audit/SAQ completed
- [ ] Compliance maintained continuously

---

## Complete Security Checklist

**Before EVERY commit, verify ALL of these:**

### Access Control
- [ ] Every endpoint checks authentication and authorization
- [ ] Users cannot access other users' data
- [ ] Admin functions reject non-admin users
- [ ] Least privilege principle applied
- [ ] Separation of duties enforced (where applicable)
- [ ] Row Level Security (RLS) enabled on user-data tables

### Secrets Management
- [ ] No hardcoded API keys, passwords, tokens
- [ ] All secrets in environment variables or Secret Manager
- [ ] `.env` files in `.gitignore`
- [ ] Encryption keys stored securely
- [ ] Key rotation schedule implemented

### Input Validation
- [ ] All user inputs validated (frontend + backend)
- [ ] SQL queries use parameterized statements (NEVER string concatenation)
- [ ] File uploads validated (type, size, content, magic bytes)
- [ ] HTML output escaped (XSS prevention)
- [ ] Whitelist validation used where possible

### Authentication & Session Management
- [ ] MFA implemented for administrative access
- [ ] Session tokens properly managed (HttpOnly, Secure, SameSite)
- [ ] Access tokens expire in 15-30 minutes
- [ ] Password change invalidates all tokens
- [ ] CSRF tokens on all state-changing forms

### Encryption & Transport
- [ ] HTTPS enforced on all endpoints
- [ ] HTTP redirects to HTTPS
- [ ] HSTS headers set (max-age >= 1 year)
- [ ] Data encrypted at rest and in transit
- [ ] Using approved encryption algorithms (AES-256-GCM, ChaCha20-Poly1305)
- [ ] TLS 1.3 or TLS 1.2 minimum enforced
- [ ] Passwords hashed with Argon2id or bcrypt

### Request Security
- [ ] CSRF protection implemented
- [ ] SameSite cookie attribute set
- [ ] SSRF prevention (URL whitelist)
- [ ] Internal IPs blacklisted for user-provided URLs

### Rate Limiting & Bot Prevention
- [ ] Rate limiting on authentication endpoints
- [ ] Rate limiting on API endpoints
- [ ] CAPTCHA on registration
- [ ] CAPTCHA on password reset
- [ ] CAPTCHA on contact forms
- [ ] CAPTCHA after multiple failed login attempts

### Logging & Monitoring
- [ ] All sensitive operations logged
- [ ] Logs are tamper-proof (cryptographic chaining)
- [ ] Logs stored securely separately
- [ ] Access attempts logged
- [ ] Failed authentication attempts logged
- [ ] Fail-safe logging (fail closed if logging fails)

### Error Handling
- [ ] No stack traces exposed to users
- [ ] No database errors exposed to users
- [ ] No file paths exposed to users
- [ ] No library versions exposed to users
- [ ] Error IDs used for tracking
- [ ] Detailed errors logged internally only
- [ ] Different error verbosity per environment

### Dependencies
- [ ] Dependencies up-to-date (no critical vulnerabilities)
- [ ] Run `npm audit` / `cargo audit` / `pip-audit` before commit
- [ ] Dependabot or Renovate enabled
- [ ] Lock files committed
- [ ] Unused dependencies removed

### Data Protection
- [ ] Sensitive data encrypted
- [ ] Data sanitization on deletion (NIST 800-88)
- [ ] Secure disposal procedures documented
- [ ] Field-level encryption for highly sensitive data

**If ANY checkbox fails → STOP and fix before committing.**

---

## Version

Security Canon Version: 1.0 (December 29, 2025)  
Based on OWASP Top 10 (2024), NIST 800-53, ISO 27001, PCI DSS

Covers 25 comprehensive security areas across all domains of application security.
