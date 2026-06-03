# Penetration Testing

Penetration testing validates security controls by simulating real-world attacks. Automated scans find known vulnerabilities. Penetration testing finds exploitable vulnerabilities and chains them into realistic attack paths. This policy establishes penetration testing requirements, methodologies, frequency, and remediation tracking.

## Why Penetration Testing Matters

Security controls exist to prevent attacks. But do they work? Configuration mistakes, design flaws, and implementation bugs create gaps that adversaries exploit. Penetration testing identifies these gaps before real attackers do.

Compliance frameworks mandate penetration testing:
- **PCI DSS:** Annual external and internal penetration tests, plus tests after significant changes
- **ISO 27001:** Annex A 12.6.1 (Technical Vulnerability Management) and A 8.29 (Security Testing in Development) implicitly require penetration testing
- **FedRAMP:** Annual penetration testing for all impact levels
- **SOC 2:** Penetration testing demonstrates security monitoring effectiveness

---

## Testing Scope

### Internal vs External Testing

**External Penetration Testing:**
Simulates attacks from outside the organization (internet-based attacker).

**Scope:**
- Public-facing web applications
- APIs exposed to internet
- Email servers
- VPN endpoints
- Cloud infrastructure (publicly accessible resources)

**Methodology:** Black box (no internal knowledge) or gray box (limited knowledge, like authenticated user)

**Frequency:** Annually minimum, plus after major releases or infrastructure changes

---

**Internal Penetration Testing:**
Simulates insider threats or attackers who have gained initial access (phishing, stolen credentials).

**Scope:**
- Internal network segmentation
- Privilege escalation paths
- Lateral movement opportunities
- Internal applications
- Database access
- File shares and sensitive data exposure

**Methodology:** Assumed compromise (start with standard user credentials), escalate to domain admin

**Frequency:** Annually minimum

---

### Application-Specific Testing

**Web Application Penetration Testing:**
Focus on OWASP Top 10 vulnerabilities specific to web apps.

**Scope:**
- Authentication and session management
- Input validation (SQL injection, XSS, command injection)
- Authorization bypasses (IDOR, privilege escalation)
- Business logic flaws
- File upload vulnerabilities
- API security

**Methodology:** Gray box (authenticated testing with user account)

**Frequency:** Before initial launch, annually, and after major feature releases

---

**API Penetration Testing:**
APIs have unique attack surface (often overlooked compared to UI).

**Scope:**
- OWASP API Top 10 vulnerabilities
- Authentication (broken authentication, JWT issues)
- Authorization (mass assignment, IDOR)
- Rate limiting and resource exhaustion
- Input validation
- Business logic abuse

**Methodology:** Gray box (API documentation provided, test with API keys)

**Frequency:** Annually, plus after API version changes

---

**Mobile Application Penetration Testing:**
Mobile apps present unique risks (insecure local storage, certificate pinning bypasses).

**Scope:**
- Insecure data storage (plaintext credentials in SharedPreferences)
- Certificate pinning bypass
- Hardcoded secrets
- Authentication flaws
- API communication security
- Insecure deep links

**Platforms:** iOS and Android tested separately

**Frequency:** Before app store release, annually, and after major updates

---

**Cloud Infrastructure Testing:**
Cloud misconfigurations are leading cause of data breaches.

**Scope:**
- IAM misconfigurations (overly permissive roles)
- Storage bucket exposure (public S3 buckets)
- Security group rules (open ports)
- Secrets management (hardcoded credentials in Lambda functions)
- Encryption configuration (at rest and in transit)
- Logging and monitoring gaps

**Methodology:** Gray box (cloud account access provided)

**Frequency:** Annually, plus after major infrastructure changes

---

## Testing Methodologies

### Black Box Testing

**Definition:** Testers have zero knowledge of system internals. Simulates external attacker with no insider information.

**Information Provided:** None (only target domain/IP)

**Advantages:**
- Realistic external attacker simulation
- Unbiased assessment (not influenced by knowledge of defenses)

**Disadvantages:**
- Time-consuming reconnaissance phase
- May miss internal vulnerabilities
- Less comprehensive coverage

**Use Case:** Annual external penetration test

---

### White Box Testing

**Definition:** Testers have complete knowledge (source code, architecture diagrams, credentials).

**Information Provided:**
- Source code repositories
- Architecture documentation
- Network diagrams
- Admin credentials
- API documentation

**Advantages:**
- Comprehensive coverage
- Faster testing (no reconnaissance)
- Identifies logic flaws and design issues

**Disadvantages:**
- Less realistic (attackers rarely have this access)
- More expensive

**Use Case:** Pre-production testing, post-incident deep dive

---

### Gray Box Testing (Recommended)

**Definition:** Testers have partial knowledge (user credentials, API docs, but not source code).

**Information Provided:**
- Standard user credentials
- Application documentation
- API specifications

**Advantages:**
- Balances realism and coverage
- Simulates privilege escalation scenarios
- More efficient than black box

**Disadvantages:**
- May miss completely blind spots

**Use Case:** Most application penetration tests

---

## Testing Process

### Pre-Engagement

**Activities:**
1. Define scope (in-scope systems, out-of-scope systems)
2. Establish rules of engagement (testing hours, DoS attacks allowed?, data exfiltration limits)
3. Obtain authorization (signed agreement from asset owner)
4. Set up communication channels (Slack, email, emergency contact)
5. Define success criteria (severity levels to be reported, expected deliverables)

**Scope Documentation:**

```
In Scope:
- example.com and all subdomains
- API endpoints at api.example.com
- Mobile apps (iOS/Android versions 2.x)

Out of Scope:
- third-party vendor integrations
- legacy.example.com (decommissioning in progress)
- IP addresses outside 203.0.113.0/24 range

Rules of Engagement:
- Testing window: Monday-Friday 9 AM - 5 PM EST
- No denial-of-service attacks
- No social engineering (phishing)
- Data exfiltration: Screenshot proof only, no actual data transfer
- Destructive actions: Require explicit approval
```

**Authorization:**
Written approval from system owner mandatory. Penetration testing without authorization is illegal (Computer Fraud and Abuse Act).

---

### Information Gathering (Reconnaissance)

**Passive Reconnaissance:**
Information gathering without directly interacting with target.

**Activities:**
- DNS enumeration (subdomains, mail servers)
- WHOIS lookups
- Search engine discovery (Google dorking)
- Social media intelligence (employee roles, technology stack)
- Public code repositories (GitHub, GitLab for leaked credentials)

**Tools:** theHarvester, recon-ng, Shodan, Google, LinkedIn

---

**Active Reconnaissance:**
Directly interact with target systems.

**Activities:**
- Port scanning (nmap)
- Service enumeration (banner grabbing)
- Technology fingerprinting (Wappalyzer, WhatWeb)
- SSL/TLS configuration testing
- Directory brute-forcing (gobuster, dirbuster)

**Caution:** Active scanning generates logs. Coordinate with security team to avoid triggering alerts and incident response.

---

### Vulnerability Identification

**Manual Testing:**
Core of penetration testing. Automated scanners find known issues. Manual testing finds logic flaws.

**Focus Areas:**
- Authentication bypasses
- Authorization flaws (horizontal/vertical privilege escalation)
- Input validation (injection attacks)
- Business logic abuse
- Session management flaws
- Cryptography misuse

**Tools:**
- Burp Suite Professional (web app testing standard)
- OWASP ZAP (open-source alternative)
- Postman/Insomnia (API testing)
- sqlmap (SQL injection)
- Metasploit (exploitation framework)

---

**Automated Scanning:**
Complements manual testing for broad coverage.

**Tools:**
- Nessus/OpenVAS (vulnerability scanners)
- Qualys (cloud vulnerability management)
- Acunetix/AppScan (web application scanners)
- SonarQube (static code analysis)

**Note:** Automated scanners generate false positives. Manual validation required.

---

### Exploitation

Prove vulnerabilities are exploitable, not just theoretical.

**Activities:**
- Gain initial access (exploit vulnerability)
- Escalate privileges (user to admin)
- Lateral movement (compromise additional systems)
- Data access (demonstrate ability to retrieve sensitive data)

**Limits:**
- Proof-of-concept only (screenshot evidence, no actual data exfiltration)
- Avoid system damage
- Stop escalation if critical production impact risk

**Documentation:**
Capture detailed steps for reproducibility. Screenshots, HTTP requests/responses, command-line output.

---

### Post-Exploitation

Assess potential damage if vulnerability exploited by real attackers.

**Activities:**
- Persistence mechanisms (could attacker maintain access?)
- Data access scope (what sensitive data is accessible?)
- Privilege escalation depth (domain admin? root?)
- Lateral movement potential (how many systems compromised from initial foothold?)

**Purpose:** Quantify business impact for risk prioritization.

---

### Reporting

**Executive Summary:**
- Non-technical overview
- Business risk assessment
- High-level recommendations
- Comparison to previous tests (improving or degrading?)

**Technical Findings:**
For each vulnerability:
- Title and unique ID
- Severity rating (Critical/High/Medium/Low)
- Description (what is the flaw?)
- Impact (what can attacker do?)
- Affected systems (URLs, IP addresses, specific functionality)
- Steps to reproduce (detailed, with screenshots)
- Remediation guidance (specific, actionable)
- References (CVE numbers, OWASP categories)

**Remediation Roadmap:**
Prioritized list of fixes with estimated effort and risk reduction.

---

## Severity Classification

Use consistent severity framework for prioritization.

### CVSS Scoring (Recommended)

Common Vulnerability Scoring System provides standardized severity ratings.

**Scoring Factors:**
- Attack Vector (network, adjacent, local, physical)
- Attack Complexity (low, high)
- Privileges Required (none, low, high)
- User Interaction (none, required)
- Scope (unchanged, changed)
- Impact (confidentiality, integrity, availability)

**Severity Ranges:**
- **Critical (9.0-10.0):** Remote code execution, authentication bypass, full system compromise
- **High (7.0-8.9):** Privilege escalation, sensitive data exposure, significant business impact
- **Medium (4.0-6.9):** Information disclosure, limited access control bypass
- **Low (0.1-3.9):** Informational findings, minimal impact

**Calculator:** https://www.first.org/cvss/calculator/3.1

---

### Business Impact-Based Severity

Complement CVSS with business context.

**Factors:**
- Financial risk (potential fraud, revenue loss)
- Regulatory risk (GDPR fine, PCI DSS non-compliance)
- Reputational risk (customer trust, brand damage)
- Operational risk (system downtime, business disruption)

**Example:**
SQL injection in admin panel (CVSS 8.5) might be Critical for e-commerce site (access to payment data) but High for marketing website (limited sensitive data).

---

## Remediation and Retesting

### Remediation Tracking

**Process:**
1. Penetration test report delivered
2. Security team triages findings, assigns to engineering teams
3. Jira/ServiceNow tickets created for each finding
4. Remediation work scheduled based on severity
5. Fixes implemented and deployed
6. Security team validates fixes

**SLAs by Severity:**
- Critical: 7 days
- High: 30 days
- Medium: 90 days
- Low: 180 days or next major release

**Progress Reporting:**
Weekly status updates to executive team until all Critical and High findings resolved.

---

### Retesting

Validate that remediation efforts actually fixed vulnerabilities.

**Scope:** Only previously identified vulnerabilities, not full penetration test

**Timing:** After remediation work completed (per SLA)

**Outcome:**
- **Fixed:** Vulnerability no longer exploitable
- **Partially Fixed:** Attack difficulty increased but not eliminated
- **Not Fixed:** Vulnerability still exploitable

**Reporting:** Retest report documents verification status for each finding.

---

## Penetration Testing Frequency

### Scheduled Testing

**Annual Full Testing:**
Comprehensive assessment of all in-scope systems.

**Quarterly Targeted Testing:**
Focus on high-risk areas:
- Newly released features
- Systems with recent security incidents
- External-facing APIs
- Payment processing

**Post-Change Testing:**
Triggered by specific events:
- Major application releases
- Infrastructure migrations (on-prem to cloud)
- Architecture changes (new authentication system)
- Compliance requirements (PCI DSS after significant change)

---

### Event-Driven Testing

**After Security Incidents:**
Post-incident penetration test validates that root cause is fixed and no similar vulnerabilities exist.

**After Mergers/Acquisitions:**
Acquired systems inherit security testing requirements.

**Before High-Risk Launches:**
New customer-facing systems tested before production deployment.

---

## In-House vs External Testing

### External Penetration Testing Firms

**Advantages:**
- Unbiased assessment (no organizational loyalty)
- Fresh perspective (not familiar with system internals)
- Specialized expertise
- Compliance-ready reports

**Disadvantages:**
- Higher cost
- Requires NDA and data access agreements
- Less context on business logic

**Use Case:** Annual compliance testing, critical system assessments

**Vendor Selection:**
- CREST certified or OSCP holders
- Industry references
- Experience in your sector (healthcare, finance, e-commerce)
- Insurance coverage (errors and omissionsprotection)

---

### In-House Red Team

**Advantages:**
- Deep business context
- Continuous testing (not annual event)
- Lower cost (no external vendor fees)
- Rapid iteration

**Disadvantages:**
- Potential bias (familiarity with systems)
- Limited expertise in specific attack techniques
- Compliance auditors may require external validation

**Use Case:** Continuous security validation, purple team exercises (red team + blue team collaboration)

---

### Bug Bounty Programs

**Definition:** Crowdsourced security testing where researchers find vulnerabilities for monetary rewards.

**Platforms:**
- HackerOne
- Bugcrowd
- Synack
- Intigriti

**Advantages:**
- Continuous testing (24/7/365)
- Diverse skillsets (global researcher community)
- Pay only for results (valid vulnerabilities)
- Scalable

**Disadvantages:**
- Public disclosure risk (even with private programs)
- Quality variance (wide range of researcher skill)
- Scope creep (researchers testing out-of-scope systems)
- Duplicate reports

**Recommended Approach:** 
Run private bug bounty for 6-12 months (invited researchers only), then transition to public if results good.

**Reward Structure:**
- Critical: $5,000 - $10,000
- High: $1,000 - $3,000
- Medium: $250 - $500
- Low: $50 - $100

Adjust based on asset criticality and budget.

---

## Legal and Ethical Considerations

### Authorization is Mandatory

Penetration testing without explicit written authorization is illegal in most jurisdictions (U.S. Computer Fraud and Abuse Act, UK Computer Misuse Act).

**Required Documentation:**
- Signed agreement from asset owner
- Defined scope (IP ranges, domains)
- Testing window (dates and times)
- Emergency contact information

**Stored:** Legal department, accessible to penetration testers and incident response team

---

### Handling Discovered Data

**Sensitive Data Found During Testing:**
If

 testers discover unprotected PII, payment data, or credentials:
1. Document finding (screenshot, do not save actual data)
2. Notify security team immediately
3. Delete any downloaded data
4. Do not share findings outside agreed channels

**Compliance:** GDPR, CCPA, PCI DSS have specific requirements for handling discovered personal data.

---

## Penetration Testing Checklist

**Planning:**
- [ ] Scope defined (in-scope and out-of-scope systems)
- [ ] Rules of engagement documented
- [ ] Authorization obtained from asset owner
- [ ] Testing window scheduled
- [ ] Communication channels established
- [ ] Emergency contacts documented

**Execution:**
- [ ] Reconnaissance completed
- [ ] Vulnerability identification performed
- [ ] Exploitation executed (proof-of-concept only)
- [ ] Post-exploitation assessed
- [ ] Evidence collected (screenshots, logs)

**Reporting:**
- [ ] Executive summary written
- [ ] Technical findings documented (severity, impact, remediation)
- [ ] Remediation roadmap created
- [ ] Report delivered to stakeholders

**Remediation:**
- [ ] Findings triaged and assigned
- [ ] Tickets created for each finding
- [ ] SLAs established based on severity
- [ ] Progress tracked weekly
- [ ] Retesting scheduled

---

## Common Pitfalls

**Testing Without Authorization:**
Even well-intentioned testing is illegal without proper authorization. Always get written approval.

**Ignoring Business Context:**
A "Critical" vulnerability in a non-production test environment is not actually critical. Consider business impact, not just technical severity.

**No Retesting:**
Fixing vulnerabilities without validation allows false confidence. Always retest to confirm fix effectiveness.

**Annual Testing Only:**
Once-per-year penetration tests provide snapshot in time. Continuous testing (bug bounty, internal red team) provides ongoing assurance.

**Treating Reports as Checklist:**
Penetration test reports should drive security program improvements, not just tactical patches. If same vulnerability class appears in multiple tests, fix root cause.

---

## References

- NIST SP 800-115: Technical Guide to Information Security Testing and Assessment
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- PCI DSS Penetration Testing Guidance: https://www.pcisecuritystandards.org/documents/Penetration-Testing-Guidance-v1_1.pdf
- CREST Penetration Testing Guide: https://www.crest-approved.org/
- PTES (Penetration Testing Execution Standard): http://www.pentest-standard.org/
