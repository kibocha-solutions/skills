# Incident Response

Security incidents are inevitable. Organizations must detect, contain, and recover from security events systematically to minimize damage and prevent recurrence. This policy establishes incident response procedures aligned with NIST SP 800-61 Rev. 2.

## Incident Response Lifecycle

The incident response process follows four phases: Preparation, Detection and Analysis, Containment/Eradication/Recovery, and Post-Incident Activity. Each phase has specific objectives, activities, and success criteria.

---

## Phase 1: Preparation

Preparation is the foundation of effective incident response. Organizations that invest in preparation respond faster, contain threats sooner, and recover with less damage.

### Computer Security Incident Response Team (CSIRT)

**Formation:**
Establish a cross-functional team with clear roles and authority. CSIRT operates 24/7 for critical systems.

**Core Team Members:**
- Incident Commander (decision authority, coordinates response)
- Security Analyst (threat investigation, forensics)
- System Administrator (containment actions, system recovery)
- Network Engineer (network isolation, traffic analysis)
- Legal Counsel (regulatory notification, evidence handling)
- Communications Lead (internal/external messaging)
- Business Owner (impact assessment, business continuity)

**Extended Team:**
- External forensics consultant (severe incidents)
- Law enforcement liaison (criminal activity)
- Public relations (breach disclosure)

**Availability:** Primary contact on-call 24/7, secondary backup designated. Escalation paths documented for after-hours incidents.

---

### Incident Response Tools

**Required Capabilities:**
- Network traffic capture (Wireshark, tcpdump)
- Log aggregation and analysis (SIEM: Splunk, ELK, Sentinel)
- Endpoint detection and response (CrowdStrike, Carbon Black)
- Forensic imaging (FTK Imager, dd)
- Memory analysis (Volatility, Rekall)
- Malware analysis sandbox (Cuckoo, Joe Sandbox)
- Communication platform (Encrypted: Signal, dedicated Slack channel)

**Pre-Configured Access:**
Ensure CSIRT members have elevated privileges for containment actions. Do not wait until an incident to provision access.

**Jump Bags:**
Pre-configured laptops with forensic tools, offline documentation, USB drives for evidence collection. Store in physically secure location with 24/7 access.

---

### Documentation and Procedures

**Runbooks Required:**
- Ransomware response procedure
- Data breach notification procedure
- DDoS mitigation procedure
- Insider threat response procedure
- Supply chain compromise procedure
- Cloud account compromise procedure

**Incident Response Plan Components:**
1. Contact information (CSIRT members, vendors, legal, PR)
2. Classification criteria (severity levels, escalation triggers)
3. Communication templates (internal announcement, breach notification)
4. Evidence collection procedures
5. System isolation procedures
6. Legal and regulatory requirements

**Testing:** Tabletop exercises quarterly, full simulation annually. Update procedures based on exercise findings.

---

### Training

**CSIRT Training Requirements:**
- SANS Incident Response training (SEC504 or equivalent)
- Forensics fundamentals
- Cloud incident response (AWS/Azure/GCP)
- Legal and compliance requirements

**Organizational Training:**
- All employees: Incident recognition and reporting (annually)
- IT staff: Basic incident handling (semi-annually)
- Executives: Crisis communication and decision-making (annually)

**Practice:** Annual purple team exercise. CSIRT responds to simulated attack while observing adversary techniques.

---

## Phase 2: Detection and Analysis

Early detection limits damage. Organizations must monitor continuously, analyze anomalies quickly, and classify incidents accurately.

### Detection Sources

**Automated Detection:**
- Intrusion Detection System (IDS) / Intrusion Prevention System (IPS)
- Security Information and Event Management (SIEM) alerts
- Endpoint Detection and Response (EDR) alerts
- Data Loss Prevention (DLP) triggers
- Antivirus / anti-malware alerts
- Network traffic anomaly detection
- Cloud security monitoring (GuardDuty, Security Center)

**Human Detection:**
- User reports (phishing, suspicious activity)
- Security Operations Center (SOC) analysts
- System administrators noticing anomalies
- Help desk tickets (account lockouts, weird behavior)
- Threat intelligence feeds
- Vulnerability disclosure reports

**Third-Party Notification:**
- Security researchers
- Law enforcement
- Partner organizations
- Credit monitoring services

**Detection Latency Target:** Critical incidents detected within 15 minutes. High-severity incidents within 1 hour. Medium-severity within 24 hours.

---

### Initial Analysis

**Triage Questions:**
1. Is this a true positive or false alarm?
2. What systems/data are affected?
3. Is the incident ongoing or contained?
4. What is the attack vector?
5. What is the business impact?

**Information Gathering:**
- Review alerts and logs
- Interview affected users
- Check network traffic
- Examine endpoint forensics
- Correlate with threat intelligence

**Time-Box Triage:** Spend maximum 30 minutes on initial classification. If unclear, escalate to full investigation.

---

### Incident Classification

**Severity Levels:**

**P0 - Critical (Immediate Response)**
- Active ransomware encryption
- Ongoing data exfiltration
- Production system compromise
- Customer data breach
- Critical infrastructure attack

**Response SLA:** Incident Commander engaged within 15 minutes. Full CSIRT mobilized within 1 hour. Executive notification immediate.

**P1 - High (Urgent Response)**
- Confirmed malware on critical systems
- Privilege escalation detected
- Insider threat indicators
- Failed containment of lower-severity incident

**Response SLA:** Security Analyst assigned within 1 hour. Incident Commander notified within 4 hours.

**P2 - Medium (Scheduled Response)**
- Successful phishing compromise (single user)
- Non-critical system compromise
- Policy violations (data mishandling)
- Scanning/probing activity

**Response SLA:** Investigation begins within 8 business hours. Resolution within 48 hours.

**P3 - Low (Routine Response)**
- Unsuccessful attack attempts
- False positive investigation
- Security hygiene issues

**Response SLA:** Investigation begins within 72 hours. Resolution within 1 week.

---

### Documentation During Analysis

**Incident Log:**
Record every action with timestamp. Use structured format for searchability.

**Example Entry:**
```
2025-01-15 14:23:15 UTC | Analyst: J.Smith | Action: Isolated host 192.168.1.100 from network
2025-01-15 14:25:03 UTC | Analyst: J.Smith | Observation: Outbound connection to 203.0.113.45:443
2025-01-15 14:27:42 UTC | Analyst: M.Jones | Action: Captured memory dump from isolated host
```

**Evidence Chain of Custody:**
Document who collected what evidence, when, from which system, using what tool. Required for legal proceedings.

---

## Phase 3: Containment, Eradication, and Recovery

Containment stops damage. Eradication removes threats. Recovery restores normal operations. Execute these activities systematically to avoid extending the incident or causing additional harm.

### Containment Strategies

**Short-Term Containment (Immediate):**
Stop active damage while preserving evidence.

**Network Isolation:**
- Disconnect compromised systems from network (pull cable, disable network interface)
- Block malicious IPs at firewall
- Disable compromised user accounts
- Revoke access tokens

**Do Not:** Simply shut down compromised systems. This loses volatile memory and active process information.

**Long-Term Containment:**
Maintain business operations while preparing for eradication.

**Segmentation:**
- Move compromised systems to isolated VLAN
- Allow critical business functions to continue on clean systems
- Monitor isolated systems for additional indicators

**Criteria for Containment Success:** Attack stopped spreading. No new systems compromised. Business-critical functions operational (possibly degraded).

---

### Eradication

Remove adversary presence completely. Partial eradication allows re-compromise.

**Actions:**
- Delete malware from all infected systems
- Rebuild compromised systems from known-good images
- Patch vulnerabilities exploited during attack
- Reset all credentials that may have been compromised
- Review and fix misconfigurations
- Remove backdoors, persistence mechanisms, scheduled tasks

**Verification:**
Scan all systems for indicators of compromise (IOCs). Monitor network for callback attempts. Review logs for suspicious authentication.

**Common Mistake:** Eradicating visible malware without finding root cause. Adversary returns through same vulnerability.

---

### Recovery

Restore systems to normal operations with confidence that threat is eliminated.

**Recovery Steps:**
1. Restore data from clean backups (verify backup integrity first)
2. Patch systems fully before reconnecting to network
3. Change all passwords (human and service accounts)
4. Implement additional monitoring for reinfection
5. Gradually restore services (most critical first)
6. Verify functionality through testing
7. Monitor intensively for 72 hours post-recovery

**Recovery Validation:**
- System functionality verified by business owner
- Security monitoring confirms no suspicious activity
- Performance metrics return to normal
- Users can access required resources

**Return to Normal Operations:** Incident Commander formally declares incident resolved. Enhanced monitoring continues for 30 days.

---

## Phase 4: Post-Incident Activity

Learning from incidents strengthens security posture. Organizations that skip post-incident reviews repeat mistakes.

### Lessons Learned Meeting

**Timing:** Within 1 week of incident closure (while details fresh)

**Attendees:**
- Full CSIRT
- Affected system owners
- Executive sponsor
- Anyone who identified gaps during response

**Agenda:**
1. Incident timeline review (what happened, when discovered, how contained)
2. What worked well (preserve these practices)
3. What needs improvement (specific actionable items)
4. Root cause analysis (how did adversary get in?)
5. Preventive measures (how do we stop recurrence?)
6. Action items assigned (owner, due date)

**Facilitation:** Use blameless post-mortem approach. Focus on systemic failures, not individual mistakes. Psychological safety encourages honest discussion.

---

### Incident Report

**Required Sections:**
- Executive summary (2 paragraphs: what happened, what we're doing about it)
- Incident timeline (detailed chronology)
- Impact assessment (systems affected, data compromised, downtime, financial impact)
- Root cause analysis (vulnerability chain that enabled attack)
- Response effectiveness (what worked, what didn't)
- Recommendations (specific improvements with priority)
- Regulatory notifications (if applicable)

**Distribution:**
- Internal: Executive team, affected business units, IT leadership
- External: Regulators (if required), affected customers (if breach)
- Retention: 7 years minimum (compliance requirement)

---

### Preventive Measures Implementation

Track all recommendations to completion. Unfixed vulnerabilities guarantee incident repeat.

**Example Action Items from Ransomware Incident:**
- Deploy EDR to all endpoints (Owner: IT Director, Due: 30 days)
- Enable MFA for VPN access (Owner: Security Team, Due: 14 days)
- Implement application whitelisting (Owner: System Admin, Due: 60 days)
- Conduct phishing simulation (Owner: Security Awareness, Due: 90 days)
- Test backup restoration quarterly (Owner: Backup Team, Due: Ongoing)

**Tracking:** Use Jira, ServiceNow, or dedicated incident management platform. Review progress monthly in security steering committee.

---

### Metrics and Reporting

**Key Performance Indicators:**
- Mean Time to Detect (MTTD): Time from attack start to detection
- Mean Time to Respond (MTTR): Time from detection to containment
- Mean Time to Recover (MTTR): Time from containment to normal operations
- Incident recurrence rate: Same attack type within 90 days
- False positive rate: Alerts investigated that were not incidents

**Trending:**
Track metrics quarterly. Improving MTTD and MTTR indicates maturing program. Increasing incident count may indicate better detection, not worse security.

**Executive Reporting:**
Monthly summary: Total incidents by severity, top attack vectors, status of remediation actions, budget impact.

---

## Communication Protocols

### Internal Communication

**During Incident:**
- Dedicated Slack/Teams channel for CSIRT coordination
- Hourly status updates to stakeholders
- Executive

 briefings every 4 hours for P0/P1 incidents
- Documented decisions and approvals

**Avoid:** Email for time-sensitive coordination. Use synchronous communication (chat, phone).

---

### External Communication

**Customer Notification:**
Required for data breaches affecting personal information. Timeline varies by jurisdiction:
- GDPR: 72 hours from detection
- CCPA: Without unreasonable delay
- HIPAA: 60 days from discovery

**Content:** What happened, what data was affected, what you're doing, what customers should do, contact information for questions.

**Approval:** Legal and PR review mandatory before external communication.

**Law Enforcement:**
Notify FBI/CISA for:
- Nation-state attacks
- Ransomware (regardless of payment decision)
- Large-scale data breaches
- Critical infrastructure attacks

**Partners/Vendors:**
Notify affected third parties. They may need to respond to their own incidents.

---

## Legal and Regulatory Considerations

**Evidence Preservation:**
Maintain chain of custody for all evidence. May be required for criminal prosecution or civil litigation.

**Privileged Communication:**
Route incident communications through legal counsel to preserve attorney-client privilege where possible.

**Regulatory Notification Requirements:**
- SEC (publicly traded companies): Material cybersecurity incidents
- State Attorneys General: Breach of state residents' data
- Industry regulators: PCI DSS (payment cards), HIPAA (health), FINRA (financial)

**Notification Templates:**
Pre-approved templates accelerate compliance. Draft with legal counsel before incident occurs.

---

## Incident Response Checklist

**Detection:**
- [ ] Alert/report received and logged
- [ ] Initial triage completed
- [ ] Severity level assigned
- [ ] CSIRT activated per severity level
- [ ] Incident ticket created

**Containment:**
- [ ] Affected systems identified
- [ ] Containment strategy selected
- [ ] Containment actions executed
- [ ] Spread stopped and verified
- [ ] Evidence preserved

**Eradication:**
- [ ] Root cause identified
- [ ] All malware removed
- [ ] Vulnerabilities patched
- [ ] Compromised credentials reset
- [ ] Persistence mechanisms removed
- [ ] IOC scan completed across environment

**Recovery:**
- [ ] Systems restored from clean backups or rebuilt
- [ ] Functionality testing completed
- [ ] Enhanced monitoring implemented
- [ ] Services gradually restored
- [ ] User access verified
- [ ] Incident formally closed by Incident Commander

**Post-Incident:**
- [ ] Lessons learned meeting scheduled and held
- [ ] Incident report drafted and approved
- [ ] Regulatory notifications submitted (if required)
- [ ] Customer notifications sent (if breach)
- [ ] Action items tracked to completion
- [ ] Incident documentation archived

---

## References

- NIST SP 800-61 Rev. 2: Computer Security Incident Handling Guide
- SANS Incident Handler's Handbook: https://www.sans.org/reading-room/whitepapers/incident
- CISA Incident Response Resources: https://www.cisa.gov/incident-response
- GDPR Breach Notification Guidelines: https://gdpr.eu/data-breach-notification/
