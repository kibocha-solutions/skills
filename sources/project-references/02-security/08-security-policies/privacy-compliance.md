# Privacy Compliance

Privacy regulations protect individual rights over personal data. Organizations that collect, process, or store personal information must comply with applicable privacy laws. This policy establishes requirements for GDPR (European Union), CCPA (California), and privacy-by-design principles.

## Privacy Regulations Overview

### GDPR (General Data Protection Regulation)

**Jurisdiction:** European Union, European Economic Area (all 27 EU member states plus Iceland, Liechtenstein, Norway)

**Applicability:**
- Organizations established in the EU
- Organizations offering goods/services to EU residents
- Organizations monitoring behavior of EU residents

**Key Principles:**
1. Lawfulness, fairness, transparency
2. Purpose limitation
3. Data minimization
4. Accuracy
5. Storage limitation
6. Integrity and confidentiality
7. Accountability

**Penalties:** Up to €20 million or 4% of global annual revenue (whichever is higher)

---

### CCPA (California Consumer Privacy Act)

**Jurisdiction:** California, United States

**Applicability:**
Businesses that:
- Have gross revenue over $25 million, OR
- Process personal information of 100,000+ California residents, OR
- Derive 50%+ revenue from selling personal information

**Key Rights:**
1. Right to know what personal information is collected
2. Right to delete personal information
3. Right to opt-out of sale of personal information
4. Right to non-discrimination for exercising rights

**Penalties:** Up to $7,500 per intentional violation, $2,500 per unintentional violation

---

### Other Privacy Laws

**HIPAA (United States):** Health information privacy
**PIPEDA (Canada):** Personal information protection
**LGPD (Brazil):** General Data Protection Law
**PDPA (Singapore):** Personal Data Protection Act

Organizations must comply with all applicable laws based on customer location and data processing location.

---

## Personal Data Definitions

### GDPR Personal Data

**Definition:** Any information relating to an identified or identifiable natural person.

**Examples:**
- Name, email address, phone number
- IP address, cookie identifiers, device IDs
- Location data (GPS coordinates, WiFi triangulation)
- Biometric data (fingerprints, facial recognition)
- Health information
- Racial or ethnic origin, political opinions, religious beliefs (special category data, higher protection)

**Not Personal Data:**
- Anonymized data (irreversibly de-identified)
- Aggregate statistics with no individual identification
- Data about corporations or organizations

---

### CCPA Personal Information

**Definition:** Information that identifies, relates to, describes, or could reasonably be linked with a California resident or household.

**Categories:**
- Identifiers (name, address, email, SSN)
- Commercial information (purchase history, browsing behavior)
- Biometric information
- Internet activity (browsing history, search history)
- Geolocation data
- Professional or employment information
- Education information
- Inferences (consumer preferences, characteristics, behavior)

**Exemptions:**
- Publicly available information
- De-identified or aggregated consumer information
- Information covered by sector-specific privacy laws (HIPAA, GLBA, FCRA)

---

## Lawful Bases for Processing (GDPR)

Processing personal data requires at least one lawful basis.

### 1. Consent

**Definition:** Individual freely given, specific, informed, and unambiguous agreement.

**Requirements:**
- Opt-in (not pre-checked boxes)
- Separate consent for each purpose
- Easy to withdraw consent
- Clear language (no legalese)
- Record of consent (who, when, what they agreed to)

**Use Case:** Marketing emails, cookies for analytics

**Withdrawing Consent:** Must be as easy as giving consent (single click unsubscribe).

---

### 2. Contract Performance

**Definition:** Processing necessary to fulfill a contract with the individual.

**Example:** Processing shipping address to deliver purchased goods

**Not Applicable:** Processing for purposes unrelated to contract (marketing based on purchase history).

---

### 3. Legal Obligation

**Definition:** Processing required by law.

**Example:** Tax record retention, financial transaction reporting, court orders

---

### 4. Vital Interests

**Definition:** Processing necessary to protect someone's life.

**Example:** Emergency medical treatment using health data without prior consent

**Rare:** Only applies when person cannot give consent and life is at risk.

---

### 5. Public Task

**Definition:** Processing necessary for public interest or official authority.

**Example:** Government census, law enforcement investigations

**Generally Not Applicable:** Private sector companies rarely use this basis.

---

### 6. Legitimate Interests

**Definition:** Processing necessary for legitimate interests of organization, unless individual rights override.

**Balancing Test Required:**
- Is interest legitimate?
- Is processing necessary?
- Does individual's interest/rights override? (children, vulnerable persons get higher protection)

**Example:** Fraud prevention, network security, direct marketing to existing customers

**Risk:** Subject to challenge. If individual objects, must demonstrate compelling grounds.

**Not Applicable:** Public authorities, special category data

---

## Individual Rights

### Right to Access (GDPR Article 15, CCPA Right to Know)

**Individual Can Request:**
- What personal data is processed
- Why it's being processed
- Who it's shared with
- How long it will be retained
- Copy of the data

**Response Deadline:**
- GDPR: 1 month (extendable to 3 months for complex requests)
- CCPA: 45 days (extendable to 90 days)

**Format:** Structured format (JSON, CSV), easily readable

**Implementation:**
Automated data export functionality. Do not rely on manual extraction.

---

### Right to Rectification (GDPR Article 16)

**Individual Can Request:** Correction of inaccurate or incomplete data

**Response Deadline:** 1 month

**Implementation:** User profile edit functionality, verification process to prevent abuse

---

### Right to Erasure / Right to Delete (GDPR Article 17, CCPA)

**Individual Can Request:** Deletion of their personal data

**Grounds for Deletion:**
- Data no longer necessary for purpose collected
- Consent withdrawn (no other lawful basis)
- Individual objects to processing
- Data processed unlawfully
- Legal obligation to erase

**Exceptions (Can Refuse Deletion):**
- Legal obligation to retain (tax records, financial regulations)
- Legal claims defense
- Public interest (archiving, research)

**Response Deadline:**
- GDPR: 1 month
- CCPA: 45 days

**Implementation:** 
- Hard delete from production databases
- Anonymize in backups (or exclude from restores)
- Delete from all systems (CRM, analytics, marketing platforms)
- Notify third parties who received data

---

### Right to Data Portability (GDPR Article 20)

**Individual Can Request:** Personal data in machine-readable format to transfer to another provider

**Scope:** Data processed based on consent or contract, automated processing only

**Format:** JSON, XML, CSV (structured, commonly used)

**Response Deadline:** 1 month

**Use Case:** Switching email providers, moving to competitor service

---

### Right to Object (GDPR Article 21)

**Individual Can Object:**
- Processing based on legitimate interests
- Direct marketing (absolute right, no balancing test)
- Scientific/historical research
- Profiling

**Response:** Stop processing unless compelling legitimate grounds override individual's interests.

---

### Right to Restrict Processing (GDPR Article 18)

**Individual Can Request:** Temporary halt of processing while:
- Accuracy of data is disputed
- Processing is unlawful (but individual opposes deletion)
- Data no longer needed but individual needs it for legal claims

**Effect:** Data stored but not processed (except with consent or for legal claims).

**Response Deadline:** 1 month

---

## Privacy-by-Design

Privacy protection integrated into system design from start, not bolted on later.

### Principles

**1. Proactive not Reactive**
Anticipate privacy risks before they materialize. Threat modeling for privacy.

**2. Privacy as Default**
Maximum privacy settings out of the box, no user action required.

**Example:** Cookies disabled by default, user opts in for analytics.

**3. Privacy Embedded into Design**
Core functionality, not add-on. Privacy requirements equivalent to security requirements.

**4. Full Functionality (Positive-Sum)**
Privacy and functionality are not zero-sum. Achieve both.

**Example:**  End-to-end encryption in messaging (privacy) with excellent UX (functionality).

**5. End-to-End Security**
Data protected throughout entire lifecycle (collection, storage, processing, deletion).

**6. Visibility and Transparency**
Users know what data is collected, how it's used, and can verify.

**7. Respect for User Privacy**
User-centric. Build systems users trust.

---

### Implementation

**Data Minimization:**
Collect only data necessary for stated purpose. Do not collect "just in case."

**Example:**
- Need: Email for account recovery
- Don't Need: Phone number, birthdate, full address (if not required for service)

**Purpose Limitation:**
Use data only for purpose disclosed at collection. No repurposing without new consent.

**Example:** Email collected for order confirmation cannot be used for marketing without separate consent.

**Storage Limitation:**
Delete data when no longer needed. Define retention periods.

**Example:** User account deleted, data purged after 30-day grace period.

**Anonymization:**
When analysis needed but individual identification is not, anonymize.

**Example:** Aggregate analytics (number of users per country) instead of individual tracking.

**Pseudonymization:**
Replace identifying fields with pseudonyms. Reduces risk if data breached.

**Example:** User ID instead of email in application logs.

---

## Data Protection Impact Assessment (DPIA)

Required for high-risk processing under GDPR Article 35.

### When DPIA is Required

**Mandatory:**
- Systematic profiling with legal effects
- Large-scale processing of special category data (health, biometric, race)
- Systematic monitoring of publicly accessible areas

**Recommended:**
- New technologies
- Processing that combines data from multiple sources
- Processing preventing individuals from exercising rights

---

### DPIA Process

**Step 1: Describe Processing**
- What data is collected?
- Why is it collected?
- How is it collected, stored, processed?
- Who has access?
- Third-party sharing?

**Step 2: Assess Necessity and Proportionality**
- Is processing necessary for stated purpose?
- Could purpose be achieved with less data?
- Is retention period appropriate?

**Step 3: Identify Risks**
- Unauthorized access
- Data breach
- Profiling leading to discrimination
- Function creep (data used for unanticipated purposes)

**Step 4: Mitigate Risks**
- Encryption
- Access controls
- Anonymization/pseudonymization
- Audit logging
- Data retention limits

**Step 5: Document and Review**
- DPIA documented and signed by DPO (Data Protection Officer)
- Reviewed annually or when processing changes

**Consultation:** If risks cannot be mitigated, consult supervisory authority (data protection regulator) before proceeding.

---

## Data Breach Notification

### GDPR Breach Notification (Article 33-34)

**Notification to Supervisory Authority:**
- Deadline: 72 hours from breach discovery
- Content: Nature of breach, categories and approximate number of individuals affected, likely consequences, measures taken, contact information

**Notification to Individuals:**
- Required if: High risk to rights and freedoms (identity theft, financial loss, discrimination)
- Not required if: Encryption makes data unintelligible, measures taken to remove high risk, disproportionate effort (public communication acceptable)
- Deadline: Without undue delay
- Content: Nature of breach, contact for information, likely consequences, measures taken

**Penalties for Non-Compliance:** Up to €10 million or 2% global revenue

---

### CCPA Breach Notification

**CCPA Does Not Add Breach Notification Requirement**
California's existing breach notification law (Cal. Civ. Code § 1798.82) applies.

**Notification Required:**
- When: Unencrypted personal information compromised
- To: California residents affected
- Deadline: Without unreasonable delay, consistent with law enforcement needs

**Content:** Date of breach, types of information compromised, contact information, toll-free number

---

## Cookies and Consent

### EU Cookie Law (ePrivacy Directive)

Requires consent before storing or accessing information on user's device.

**Exempt (No Consent Required):**
- Strictly necessary cookies (authentication, shopping cart, security)

**Requires Consent:**
- Analytics cookies
- Advertising cookies
- Third-party tracking cookies

**Implementation:**
- Cookie banner on first visit
- Opt-in for non-essential cookies (pre-checked boxes invalid)
- Granular consent (separate checkboxes for analytics vs advertising)
- Easy to change preferences later

**Documentation:** Maintain record of consent (user ID, timestamp, cookies accepted).

---

## Children's Privacy

Special protections for children's data.

### GDPR

**Age of Consent:** 16 years (member states can lower to 13)

**Parental Consent Required:** For online services offered directly to children under age of consent

**Verification:** Reasonable efforts to verify parental consent.

---

### COPPA (Children's Online Privacy Protection Act, USA)

**Applicability:** Services directed to children under 13, or with actual knowledge of users under 13

**Requirements:**
- Parental consent before collecting personal information from children
- Clear privacy policy
- Data security
- Retention limits
- Parental access to child's data

**Penalties:** Up to $43,280 per violation

---

## Cross-Border Data Transfers

GDPR restricts transfers of personal data outside the EU unless adequate protections exist.

### Adequacy Decisions

EU Commission recognizes certain countries as providing adequate protection.

**Adequate Countries:** UK, Switzerland, Canada (commercial orgs), Japan, Argentina, others

**Transfer Mechanism:** No additional safeguards needed.

---

### Standard Contractual Clauses (SCCs)

Pre-approved contract templates for data transfers.

**Use:** When transferring to countries without adequacy decision (e.g., United States)

**Requirements:**
- Execute SCCs with data processor
- Conduct Transfer Impact Assessment (TIA) to ensure local laws don't undermine protections
- Implement supplementary measures if necessary (encryption, pseudonymization)

---

### Binding Corporate Rules (BCRs)

Internal policies for multinational organizations transferring data within corporate group.

**Use:** Simplifies intra-company transfers across countries

**Approval:** Requires supervisory authority approval (lengthy process).

---

## Data Protection Officer (DPO)

### When DPO is Mandatory (GDPR)

**Required For:**
- Public authorities (except courts)
- Organizations whose core activities involve large-scale systematic monitoring
- Organizations whose core activities involve large-scale processing of special category data

**Recommended:** Even when not mandatory, DPO demonstrates accountability.

---

### DPO Responsibilities

**Tasks:**
- Advise organization on GDPR compliance
- Monitor compliance
- Conduct DPIAs
- Serve as contact point for supervisory authority
- Serve as contact point for individuals exercising rights

**Independence:** Must report to highest management, no conflicts of interest, cannot be fired for performing DPO tasks.

**Expertise:** Professional qualifications, knowledge of data protection law, ability to fulfill tasks.

---

## Privacy Compliance Checklist

**Governance:**
- [ ] DPO appointed (if required) or privacy team established
- [ ] Privacy policy published and easily accessible
- [ ] Data inventory maintained (what data, why, where, how long)
- [ ] Lawful bases documented for all processing
- [ ] Vendor contracts reviewed for data processing terms

**Individual Rights:**
- [ ] Data subject access request (DSAR) process documented
- [ ] Automated data export functionality implemented
- [ ] Data deletion process implemented (hard delete, not soft)
- [ ] Right to rectification process established
- [ ] Consent management system implemented (if using consent)

**Security:**
- [ ] Encryption at rest and in transit
- [ ] Access controls (role-based, least privilege)
- [ ] Audit logging
- [ ] Data breach response plan documented
- [ ] Data breach notification procedures (72-hour timeline)

**Design:**
- [ ] DPIA completed for high-risk processing
- [ ] Privacy-by-design principles applied
- [ ] Data minimization practiced
- [ ] Retention periods defined and enforced
- [ ] Anonymization/pseudonymization where possible

**Cookies and Tracking:**
- [ ] Cookie banner implemented (opt-in for non-essential)
- [ ] Cookie policy published
- [ ] Consent management platform integrated
- [ ] Third-party trackers reviewed and minimized

**Cross-Border:**
- [ ] Data transfer mechanisms established (SCCs, adequacy, BCRs)
- [ ] Transfer Impact Assessment conducted
- [ ] Data processing agreements with vendors

---

## Common Pitfalls

**Treating Privacy as Legal Problem Only:**
Privacy is technical, design, and operational. Legal team cannot comply alone. Engineering, product, and operations must commit.

**Collecting Data Without Clear Purpose:**
"We might need it later" is not a lawful basis. Define purpose before collection.

**Relying on Legitimate Interests Without Balancing Test:**
Legitimate interests are not a blank check. Document balancing test, be prepared to defend.

**Ignoring Children's Privacy:**
If your service attracts children, comply with COPPA/GDPR child protections. Age verification is difficult but required.

**Assuming Consent Solves Everything:**
Consent is one lawful basis, not a cure-all. Must be freely given, specific, informed, unambiguous. Pre-checked boxes fail.

**No Plan for Data Subject Requests:**
First GDPR request should not be a surprise. Automate where possible, document process, train staff.

---

## References

- GDPR Full Text: https://gdpr-info.eu/
- CCPA Full Text: https://oag.ca.gov/privacy/ccpa
- NIST Privacy Framework: https://www.nist.gov/privacy-framework
- IAPP (International Association of Privacy Professionals): https://iapp.org/
- ICO (UK Information Commissioner's Office) Guidance: https://ico.org.uk/for-organisations/guide-to-data-protection/
- EDPB (European Data Protection Board) Guidelines: https://edpb.europa.eu/our-work-tools/general-guidance/gdpr-guidelines-recommendations-best-practices_en
