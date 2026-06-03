# Threat Modeling

Threat modeling is the systematic process of identifying, evaluating, and mitigating security threats during system design and throughout the application lifecycle. This policy establishes when threat modeling is required, which methodologies to use, and how to document findings.

## Why Threat Modeling Matters

Security failures often stem from design flaws, not implementation bugs. A system designed without considering adversarial threats will accumulate vulnerabilities faster than teams can patch them. Threat modeling shifts security left by embedding threat thinking into architecture decisions.

## When Threat Modeling is Required

Mandatory threat modeling triggers:

**New Systems**
- All greenfield applications before implementation begins
- Cloud infrastructure provisioning
- API design and external integrations
- Authentication and authorization systems

**Major Changes**
- Architecture refactoring (monolith to microservices, database migrations)
- New attack surface addition (public API, mobile app, admin panel)
- Third-party integrations with external services
- Privilege escalation features (new administrator capabilities)

**Periodic Review**
- Annual review of existing critical systems
- Quarterly review of high-risk systems (payment processing, PII handling)
- Post-incident review after security breaches

Do not wait for implementation. Threat models inform architecture, not just mitigate existing design.

---

## Methodologies

### STRIDE (Recommended for General Applications)

**Mnemonic:** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege

**Process:**
1. Create data flow diagram (DFD) showing all components, data stores, and boundaries
2. For each DFD element, ask if vulnerabilities exist in each STRIDE category
3. Document threats and assign risk ratings
4. Propose mitigations

**Example:**

```
Component: User Authentication API

S - Spoofing: Can attackers impersonate users? (JWT forgery, session hijacking)
T - Tampering: Can credentials be modified in transit? (MITM attacks)
R - Repudiation: Can users deny their actions? (Audit logging gaps)
I - Information Disclosure: Can auth tokens leak? (Logs, error messages)
D - Denial of Service: Can auth system be overwhelmed? (Brute force attacks)
E - Elevation of Privilege: Can users escalate roles? (IDOR, mass assignment)
```

**Strengths:** Systematic, comprehensive, suitable for most applications

**Weaknesses:** Can be time-consuming for large systems

---

### PASTA (Recommended for Risk-Focused Organizations)

**Mnemonic:** Process for Attack Simulation and Threat Analysis

**Seven Stages:**
1. Define business objectives (What matters most?)
2. Define technical scope (Attack surface enumeration)
3. Application decomposition (Architecture understanding)
4. Threat analysis (Industry threat intelligence)
5. Vulnerability analysis (Known weaknesses)
6. Attack modeling (Simulate attack paths)
7. Risk and impact analysis (Prioritize mitigations)

**Example:**

```
Business Objective: Protect customer payment data

Technical Scope:
- Payment processing API (Node.js)
- PostgreSQL database
- Stripe integration
- Admin dashboard

Threats Identified:
- Payment data exposure (OWASP API03 - Broken Object Property Authorization)
- Stripe API key leakage (CWE-798 - Hardcoded credentials)

Attack Path:
Attacker → Admin CSRF → Metadata API → Stripe key exfiltration → Charge fraud

Risk: HIGH (Financial + Reputational damage)
Impact: $500K potential fraud + regulatory fines

Mitigation Priority: Immediate
```

**Strengths:** Business-context aware, risk-prioritized

**Weaknesses:** Requires more security expertise

---

### DREAD (Risk Rating Framework)

Used alongside STRIDE or PASTA to quantify threat severity.

**Scoring (1-10 scale):**
- **D**amage potential: How bad if exploited?
- **R**eproducibility: How easy to reproduce?
- **E**xploitability: How much effort to exploit?
- **A**ffected users: How many users impacted?
- **D**iscoverability: How easy to find?

**Total Risk Score:** (D + R + E + A + D) / 5

**Example:**

```
Threat: SQL Injection in search endpoint

D: 10 (Full database compromise)
R: 10 (Works every time)
E: 7 (Moderate skill required)
A: 10 (All users affected)
D: 8 (Easily found through fuzzing)

Risk Score: 9.0 / 10 (CRITICAL)
```

**Application:** Prioritize mitigations for threats scoring 7+ first.

---

## Threat Modeling Process

### Step 1: Define Scope and Assumptions

**Document:**
- System boundaries (What's in scope? What's out of scope?)
- Trust boundaries (DMZ, internal network, admin vs user)
- Assets at risk (Customer data, financial records, API keys)
- Assumptions (Attackers have internet access, insiders are trusted)

**Example:**

```
Scope: Tax Management System - Tax Calculation Service
In Scope: Tax Rule Engine API, PostgreSQL database, gRPC service mesh
Out of Scope: Frontend (separate threat model), payment processing
Assets: Tax calculation rules (proprietary), taxpayer records (PII)
Assumptions: Network assumed secure (VPN), Kubernetes cluster hardened
```

---

### Step 2: Create Data Flow Diagram (DFD)

**Elements:**
- External entities (users, external systems)
- Processes (services, functions)
- Data stores (databases, caches)
- Data flows (API calls, database queries)
- Trust boundaries (network zones)

**Tools:**
- Microsoft Threat Modeling Tool
- OWASP Threat Dragon
- Draw.io with threat modeling templates
- Lucidchart

**Minimum Detail:** Show all components that cross trust boundaries or handle sensitive data.

---

### Step 3: Identify Threats

Apply chosen methodology (STRIDE, PASTA) systematically. For each DFD element, enumerate potential threats.

**Anti-Pattern:** "We use HTTPS so network threats don't apply"
- Insider threats still exist
- Certificate validation can fail
- Compromised CAs are possible

Assume paranoia. Consider what adversaries could do, not just what seems l

ikely.

---

### Step 4: Document and Rate Threats

**Required Fields:**
- Threat ID (unique identifier)
- Threat category (STRIDE letter or CWE number)
- Description (2-3 sentences)
- Attack scenario (step-by-step)
- Risk rating (DREAD score or High/Medium/Low)
- Affected components
- Proposed mitigation

**Template:**

```
Threat ID: TM-AUTH-001
Category: Elevation of Privilege
Description: Mass assignment vulnerability in user update endpoint allows
attackers to modify their role field and escalate to administrator
privileges.

Attack Scenario:
1. Attacker registers as regular user
2. Intercepts PUT /api/users/:id request
3. Adds "role": "admin" to JSON body
4. Server blindly accepts all fields
5. Attacker gains admin access

Risk: CRITICAL (DREAD: 9.6/10)
Affected: User Management Service
Mitigation: Implement field allowlist, use DTOs for user updates
Status: Open
Owner: Backend team
```

---

### Step 5: Propose and Implement Mitigations

**Mitigation Categories:**

**Eliminate:** Remove the threat entirely
- Example: Don't store credit cards, use Stripe tokens

**Mitigate:** Reduce likelihood or impact
- Example: Rate limiting, input validation, WAF

**Transfer:** Move risk to another party
- Example: Use third-party auth (OAuth), PCI-compliant payment processor

**Accept:** Acknowledge risk but take no action
- Example: Low-severity informational disclosure in non-critical systems
- Requires management approval and documentation

**Track:** Mitigation implementation status and validation.

---

## Threat Model Documentation

**Minimum Artifacts:**
1. Threat model document (PDF or Markdown)
2. Data flow diagram (visual)
3. Threat register (spreadsheet or database)
4. Mitigation tracking (Jira, GitHub Issues)

**Storage:** Version-controlled repository, accessible to development and security teams.

**Review Frequency:**
- New systems: Before implementation
- Existing systems: Annually or after major changes
- Critical systems: Quarterly

---

## Threat Modeling Checklist

- [ ] Scope and boundaries clearly defined
- [ ] Data flow diagram created showing all components
- [ ] All trust boundaries identified
- [ ] Assets at risk documented
- [ ] Methodology selected (STRIDE, PASTA, or hybrid)
- [ ] Threats enumerated for each DFD element
- [ ] Risk ratings assigned (DREAD or equivalent)
- [ ] Mitigations proposed for all high/critical threats
- [ ] Threat register created and maintained
- [ ] Mitigation owners assigned
- [ ] Threat model reviewed by security team
- [ ] Threat model approved before implementation

---

## Common Pitfalls

**Threat modeling too late:** Design is finalized, mitigations become expensive retrofits. Threat model during architecture design, not after implementation.

**Insufficiently paranoid:** "Users wouldn't do that" or "That's unrealistic." Assume intelligent adversaries with time and motivation.

**Analysis paralysis:** Spending months on perfect threat models. Better to have approximate threat awareness quickly than perfect documentation later.

**No follow-through:** Threat model sits unused. Mitigations must be tracked, implemented, and validated.

**Forgetting insiders:** External attackers get all the attention. Insider threats (malicious or negligent) are equally important.

---

## Automation and Tools

**Microsoft Threat Modeling Tool:** Free, Windows-only, STRIDE-focused, generates threat reports
**OWASP Threat Dragon:** Open-source, cross-platform, web-based, supports STRIDE
**IriusRisk:** Commercial, integrates with development workflows, risk-quantified
**ThreatModeler:** Commercial, collaborative, enterprise-focused

Use tools to accelerate threat identification, but don't rely on them exclusively. Tools miss context-specific threats that humans identify through domain knowledge.

---

## References

- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
- Microsoft SDL Threat Modeling: https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling
- NIST SP 800-154: Guide to Data-Centric System Threat Modeling
- PASTA Framework: https://versprite.com/pasta-threat-modeling/
