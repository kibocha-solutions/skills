# Security Training

Security awareness is the first line of defense. Technical controls fail when users fall victim to phishing, misconfigure systems, or handle data improperly. This policy establishes mandatory security training requirements aligned with ISO 27001 Annex A 6.3 and NIST SP 800-50.

## Training Requirements by Role

Security training must be role-specific. Developers need different knowledge than executives, and system administrators face different risks than end users.

### All Employees (Mandatory)

**Initial Training:**
Complete within first week of employment, before system access granted.

**Topics:**
- Information security policies (acceptable use, password requirements, data classification)
- Phishing and social engineering recognition
- Physical security (badge access, clean desk, visitor protocols)
- Incident reporting procedures
- Password hygiene (length, complexity, no reuse, password manager usage)
- Mobile device security
- Home/remote work security
- Data handling requirements

**Duration:** 45-60 minutes

**Frequency:** Annually, plus immediate update when policies change

**Delivery:** Interactive e-learning with knowledge check, not passive video

**Pass Requirement:** 80% on final assessment, retake until passed

---

### Developers and Engineers

**Additional Topics:**
- OWASP Top 10 deep dive
- Secure coding practices (input validation, output encoding, parameterized queries)
- Authentication and authorization flaws
- Cryptography best practices (when to use what, common mistakes)
- API security (mass assignment, rate limiting, proper error handling)
- Dependency management (scanning for vulnerabilities, update procedures)
- Secrets management (no hardcoded credentials, use vaults)
- Code review for security issues

**Duration:** 4 hours initial, 2 hours annual refresher

**Hands-On Component:** Capture-the-flag (CTF) exercises, vulnerable code review

**Frequency:** Initial training during onboarding, annual refresher, plus updates when new vulnerability classes emerge

**Vendor Resources:**
- SANS Secure Coding courses
- PortSwigger Web Security Academy (free)
- OWASP Top 10 workshops
- PluralSight/Udemy secure coding paths

---

### System Administrators and DevOps

**Additional Topics:**
- Server hardening (disable unnecessary services, patch management, firewall rules)
- Access control configuration (principle of least privilege, separation of duties)
- Log monitoring and anomaly detection
- Backup verification and restoration procedures
- Incident response procedures specific to infrastructure
- Cloud security (IAM, security groups, encryption, compliance)
- Container security (image scanning, runtime protection)
- Infrastructure as Code security (scanning Terraform/CloudFormation)

**Duration:** 4 hours initial, 2 hours annual refresher

**Hands-On Component:** Simulated incident response, misconfigurated infrastructure detection

**Frequency:** Initial training during onboarding, annual refresher

---

### Security Team

**Specialized Training:**
- Advanced penetration testing (SANS GPEN, Offensive Security OSCP)
- Incident response and forensics (SANS GCIH, GCFA)
- Threat hunting
- Reverse engineering and malware analysis
- Cloud security architecture (AWS/Azure/GCP certifications)
- Compliance frameworks (ISO 27001 Lead Auditor, FedRAMP)

**Certifications Encouraged:**
- CISSP (Certified Information Systems Security Professional)
- CISM (Certified Information Security Manager)
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- GIAC certifications (GSEC, GCIA, GCIH)

**Frequency:** Continuous learning, attend 2-3 conferences annually, maintain certifications

---

### Executives and Management

**Topics:**
- Security program overview (what security team does, why it matters)
- Business risk from security incidents (financial, reputational, regulatory)
- Regulatory compliance requirements (GDPR, CCPA, HIPAA, SOC 2)
- Incident response decision-making (when to notify customers, law enforcement, board)
- Security budget allocation and ROI
- Third-party risk management
- Supply chain security

**Duration:** 90 minutes initial, 60 minutes annual

**Delivery:** Executive briefing format, business-focused language, minimal technical jargon

**Frequency:** Annually, plus briefings before major security decisions

---

## Specialized Training Programs

### Phishing Simulation

Awareness training alone is insufficient. Simulated phishing tests realistic recognition under pressure.

**Frequency:** Monthly simulations

**Escalation:**
- First failure: Immediate remedial training (15-minute module)
- Second failure (within 90 days): Manager notification, 30-minute training
- Third failure: Mandatory in-person security review, potential access restrictions

**Simulation Difficulty:** Start easy (obvious phishing), gradually increase difficulty (sophisticated spear-phishing)

**Metrics:**
- Click rate (target: <5% organization-wide)
- Credential entry rate (target: <1%)
- Reporting rate (target: >30% of recipients report suspicious email)

**No Punishment Culture:** Frame as learning opportunity, not gotcha. Goal is improvement, not embarrassment.

**Vendor Options:**
- KnowBe4
- Proofpoint Security Awareness
- Cofense PhishMe
- SANS Security Awareness

---

### Secure Code Review Training

Developers learn to identify vulnerabilities in peer code reviews.

**Format:** Workshop with real vulnerable code samples

**Exercises:**
- Review code snippet, identify vulnerabilities (SQL injection, XSS, CSRF)
- Propose fixes
- Discuss why vulnerability exists (design flaw, misunderstanding, oversight)

**Outcome:** Developers can spot common flaws before merging to production

**Frequency:** Semi-annually for development team

---

### Incident Response Tabletop Exercises

Practice response procedures without actual incident.

**Scenario Examples:**
- Ransomware encryption of file server
- Data breach notification timeline
- DDoS attack mitigation
- Insider threat investigation
- Supply chain compromise

**Participants:** CSIRT, executives, legal, PR, affected business units

**Duration:** 2-3 hours

**Facilitator:** External security consultant or senior security team member

**Output:** Document gaps in procedures, unclear roles, missing information

**Frequency:** Quarterly

---

## Training Documentation and Compliance

### Record Keeping

**Required Records:**
- Employee name
- Training module completed
- Completion date
- Assessment score
- Certificate of completion

**Retention:** 7 years (compliance requirement)

**System:** Learning Management System (LMS) with automated tracking

**Audit Trail:** Who accessed training, when started, when completed, number of attempts

---

### Compliance Verification

**Quarterly Audit:**
- Identify employees without current training
- Escalate to HR and manager
- Disable access for non-compliant employees (after 30-day grace period)

**New Hire Verification:**
- Security training must be complete before production access granted
- Exception process requires CISO approval and documented risk acceptance

**Contractor Training:**
- Contractors with system access held to same standards as employees
- Training completion verified before account provisioning

---

## Training Content Development

### In-House vs Vendor Content

**Vendor Content (Recommended for General Training):**
- Professionally produced, high quality
- Regular updates for new threats
- Compliance-ready (meets ISO 27001, NIST, etc.)
- Multi-language support
- Cost-effective for large organizations

**In-House Content (Recommended for Specialized Training):**
- Organization-specific policies and procedures
- Technology stack-specific guidance
- Internal tools and systems
- Case studies from actual incidents (anonymized)

**Hybrid Approach:**
Vendor content for foundational awareness, in-house content for organizational specifics.

---

### Content Update Frequency

**Annual Review:** All training content reviewed and updated yearly minimum

**Immediate Updates Required For:**
- New regulatory requirements (GDPR amendment, new state privacy law)
- Major incidents (breach, ransomware attack) triggering policy changes
- New attack techniques (novel phishing, zero-day exploits becoming common)
- Technology changes (new cloud platform, migration to new authentication system)

**Version Control:** Track training content versions, document changes between versions

---

## Measuring Training Effectiveness

### Leading Indicators

**Knowledge Assessment Scores:**
Track pre-test and post-test scores. Effective training shows measurable improvement.

**Target:** 80% post-training assessment pass rate on first attempt

**Phishing Simulation Results:**
- Click rate declining over time
- Reporting rate increasing over time

**Target:** 50% reduction in click rate within 6 months of training program start

---

### Lagging Indicators

**Security Incidents Attributed to Human Error:**
- Password sharing incidents
- Data mishandling (emailing sensitive data unencrypted)
- Misconfiguration causing vulnerability
- Successful phishing attacks

**Target:** 25% year-over-year reduction

**Help Desk Tickets Related to Security:**
- Locked out accounts (may indicate password complexity struggles)
- VPN issues
- Phishing reports (good if increasing)

---

### Continuous Improvement

**Post-Incident Learning:**
After any security incident, review if training gap contributed. Update training to address.

**Example:** If developer introduces SQL injection vulnerability, evaluate if secure coding training covered parameterized queries adequately. If not, add specific examples.

**Feedback Collection:**
Survey training participants for clarity, relevance, engagement. Incorporate feedback into next version.

**Benchmarking:**
Compare metrics to industry averages (phishing click rates, training completion rates). Identify areas for improvement.

---

## Training Technology Stack

### Learning Management System (LMS)

**Required Features:**
- Automated enrollment (triggered by HR system for new hires)
- Progress tracking per user
- Assessment delivery and scoring
- Certificate generation
- Reporting (compliance, completion rates, scores)
- Mobile accessibility
- Integration with identity provider (SSO)

**Vendor Options:**
- Cornerstone OnDemand
- TalentLMS
- Moodle (open-source)
- SAP SuccessFactors

---

### Phishing Simulation Platform

**Required Features:**
- Template library (thousands of realistic phishing emails)
- Customizable landing pages
- Automated remedial training for failures
- Reporting and analytics
- Whitelisting to prevent email filters from blocking
- Spear-phishing simulations (personalized emails)

**Vendor Options:**
- KnowBe4
- Proofpoint
- Cofense
- Infosec IQ

---

## Exemptions and Exceptions

**Role-Based Exemptions:**
Some roles may not require certain training modules.

**Example:** Marketing team may not need secure coding training, but still requires general awareness.

**Process:**
1. Manager requests exemption in writing
2. Security team reviews request
3. CISO approves or denies
4. Document exemption and rationale

**No Exemption From:**
- General security awareness (mandatory for all)
- Phishing simulations (mandatory for all)
- Organizational security policies (mandatory for all)

---

## Security Training Checklist

**Program Design:**
- [ ] Role-based training matrix documented
- [ ] Training content selected (vendor vs in-house)
- [ ] LMS selected and configured
- [ ] Phishing simulation platform selected
- [ ] Training schedule established
- [ ] Assessment criteria defined

**Content:**
- [ ] General awareness training (all employees)
- [ ] Developer secure coding training
- [ ] System administrator hardening training
- [ ] Executive security briefing
- [ ] Phishing simulation library
- [ ] Incident response tabletop scenarios

**Compliance:**
- [ ] Training records system configured
- [ ] Audit process documented
- [ ] Non-compliance escalation process defined
- [ ] Contractor training requirements documented

**Measurement:**
- [ ] Metrics defined (click rate, completion rate, incident rate)
- [ ] Reporting dashboards configured
- [ ] Quarterly review process established
- [ ] Continuous improvement process documented

---

## Common Pitfalls

**"One and Done" Training:**
Annual training alone is insufficient. Security threats evolve constantly. Continuous reinforcement through phishing simulations, newsletters, and micro-learning is essential.

**Boring Content:**
Death by PowerPoint. Use interactive scenarios, gamification, real-world examples. Engagement drives retention.

**No Measurement:**
Training without measurement is hope. Track metrics, identify gaps, iterate.

**Ignoring Feedback:**
If employees report training as irrelevant or confusing, listen. Ineffective training wastes time and budget.

**No Executive Buy-In:**
If executives skip training or dismiss importance, employees follow. Leadership must model security-conscious behavior.

---

## References

- NIST SP 800-50: Building an Information Technology Security Awareness and Training Program
- ISO/IEC 27001:2022 Annex A 6.3: Information Security Awareness, Education and Training
- SANS Security Awareness Maturity Model: https://www.sans.org/security-awareness-training/resources/maturity-model/
- NIST NICE Framework (Cybersecurity Workforce Development): https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center
