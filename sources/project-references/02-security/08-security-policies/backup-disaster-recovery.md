# Backup and Disaster Recovery

System failures are inevitable. Hardware fails. Software has bugs. Natural disasters occur. Human errors happen. Organizations must implement backup and disaster recovery procedures to ensure business continuity and data protection.

This policy establishes backup requirements, recovery objectives, testing procedures, and disaster recovery plans aligned with FedRAMP Contingency Planning controls and NIST SP 800-34.

---

## Recovery Objectives

Recovery objectives define how quickly systems must be restored and how much data loss is acceptable. These targets drive backup frequency, infrastructure redundancy, and disaster recovery procedures.

### Recovery Time Objective (RTO)

**Definition:** Maximum acceptable downtime for a system or service. How long can the business operate without this system?

**Categorization:**

**Tier 1 - Critical Systems (RTO: 1-4 hours)**
- Payment processing
- Customer-facing applications
- Authentication services
- Core business transaction systems

**Tier 2 - Important Systems (RTO: 4-24 hours)**
- Internal applications
- Reporting systems
- Email and collaboration tools
- Customer support platforms

**Tier 3 - Standard Systems (RTO: 1-3 days)**
- Archive systems
- Development environments
- Training platforms
- Internal documentation

**Tier 4 - Non-Critical Systems (RTO: 3-7 days)**
- Test environments
- Deprecated legacy systems
- Seasonal applications

**Assignment:** Business owner determines tier based on revenue impact, regulatory requirements, and operational dependencies.

---

### Recovery Point Objective (RPO)

**Definition:** Maximum acceptable data loss measured in time. How much data can the business afford to lose?

**Categorization:**

**Tier 1 - Zero Data Loss (RPO: 0 minutes)**
- Financial transaction systems
- Medical records
- Mission-critical databases
- Implementation: Synchronous replication, database clustering, continuous data protection

**Tier 2 - Minimal Data Loss (RPO: 15 minutes)**
- Customer relationship management
- E-commerce inventory
- Real-time analytics
- Implementation: Near-real-time replication, frequent snapshots

**Tier 3 - Limited Data Loss (RPO: 1-4 hours)**
- Document management
- Project tracking
- Internal wikis
- Implementation: Hourly backups, asynchronous replication

**Tier 4 - Acceptable Data Loss (RPO: 24 hours)**
- Development databases
- Log archives
- Static content
- Implementation: Daily backups

**Business Impact Analysis:** Determine RPO based on financial loss per hour of data loss, regulatory requirements, and recovery cost.

---

## Backup Strategy

### Backup Types

**Full Backup**
- Complete copy of all data
- Fastest recovery (single restore operation)
- Highest storage cost
- Longest backup window
- Schedule: Weekly or monthly

**Incremental Backup**
- Only data changed since last backup (any type)
- Smallest backup size
- Lowest storage cost
- Slower recovery (must restore full + all incrementals)
- Schedule: Daily or continuous

**Differential Backup**
- Data changed since last full backup
- Moderate backup size
- Moderate storage cost
- Faster recovery than incremental (full + last differential)
- Schedule: Daily

**Recommended Strategy (3-2-1 Rule):**
- 3 copies of data (production + 2 backups)
- 2 different storage media (disk + tape, or local + cloud)
- 1 offsite copy (different geographic location)

---

### Backup Schedules

**Tier 1 Systems:**
- Full backup: Weekly (Sunday 2 AM)
- Incremental backup: Continuous or hourly
- Offsite replication: Real-time synchronous or every 15 minutes
- Snapshot retention: 30 days

**Tier 2 Systems:**
- Full backup: Weekly (Sunday 2 AM)
- Incremental backup: Every 4 hours
- Offsite replication: Every 4 hours
- Snapshot retention: 14 days

**Tier 3 Systems:**
- Full backup: Weekly (Sunday 2 AM)
- Differential backup: Daily (2 AM)
- Offsite replication: Daily
- Snapshot retention: 7 days

**Tier 4 Systems:**
- Full backup: Monthly (first Sunday 2 AM)
- Differential backup: Weekly
- Offsite replication: Weekly
- Snapshot retention: 3 months

**Backup Windows:** Schedule backups during low-traffic periods. Monitor backup duration to ensure completion before business hours.

---

### Data Protection

**Encryption at Rest:**
- All backups encrypted using FIPS 140-2 validated cryptographic modules
- Minimum encryption: AES-256
- Key management: Store keys in Hardware Security Module (HSM) or cloud key management service
- Key rotation: Every 90 days

**Encryption in Transit:**
- TLS 1.3 for all backup data transfers
- Mutual TLS authentication between backup clients and servers
- No cleartext transmission

**Access Control:**
- Backup administrators separate from system administrators (separation of duties)
- Multi-factor authentication required for backup system access
- Principle of least privilege (read-only access default, write requires approval)
- Audit all backup access attempts

**Immutability:**
- Configure immutable backups (cannot be deleted or modified for retention period)
- Protection against ransomware encryption
- Compliance hold for regulatory requirements

**Air-Gapped Backups:**
- Critical systems: Maintain offline backups disconnected from network
- Frequency: Monthly full backups to tape or removable media
- Storage: Secure offsite facility (fireproof safe, different building)

---

### Backup Verification

Backups that cannot be restored are worthless. Regular testing is mandatory.

**Automated Verification:**
- File integrity checks (checksum validation)
- Run immediately after backup completion
- Alert on verification failures

**Restoration Testing:**

**Frequency by Tier:**
- Tier 1: Monthly full restoration test
- Tier 2: Quarterly full restoration test
- Tier 3: Semi-annual full restoration test
- Tier 4: Annual full restoration test

**Test Scope:**
- Restore to isolated environment (not production)
- Validate data integrity
- Verify application functionality
- Measure restoration time (validate RTO)
- Document any issues encountered

**Random Sampling:**
- Monthly: Randomly select 5 files from backups and restore to verify integrity
- Purpose: Catch corruption that full restoration tests miss due to sampling

**Test Documentation:**
- Record restoration time
- Document any failures or errors
- Track RTO/RPO achievement
- Identify gaps in backup procedures

---

## Disaster Recovery Planning

Disaster recovery planning prepares for complete failure of primary infrastructure. Natural disasters, cyberattacks, facility loss, or cascading system failures require switching operations to alternate infrastructure.

### Business Impact Analysis (BIA)

Identify critical business functions and dependencies.

**Process:**
1. Inventory all systems and applications
2. Identify business processes supported by each system
3. Calculate financial impact per hour of downtime
4. Document dependencies (upstream/downstream systems, third parties)
5. Assign recovery priority based on business impact
6. Determine maximum tolerable downtime (MTD)

**Output:** Prioritized list of systems for recovery sequencing.

---

### Disaster Recovery Sites

**Hot Site:**
- Fully operational duplicate environment
- Real-time data replication
- Immediate failover capability
- RTO: Minutes to hours
- Cost: Highest
- Use Case: Tier 1 systems with RPO near zero

**Warm Site:**
- Partially configured infrastructure
- Recent backups available
- Minimal configuration required
- RTO: Hours to a day
- Cost: Moderate
- Use Case: Tier 2 systems

**Cold Site:**
- Physical space with power and network
- No pre-configured hardware
- Requires full setup and data restoration
- RTO: Days to weeks
- Cost: Lowest
- Use Case: Tier 3-4 systems, long-term recovery scenario

**Cloud DR:**
- Infrastructure as Code templates
- Automated provisioning
- Pay-as-you-go pricing
- RTO: Hours (depending on automation)
- Cost: Moderate (only pay during failover)
- Use Case: Modern cloud-native applications

---

### Disaster Declaration Criteria

**Invoke disaster recovery when:**
- Primary data center inaccessible (fire, flood, power outage exceeding 4 hours)
- Ransomware encryption of critical systems exceeds recovery capability
- Corruption across primary and backup systems
- Cascading failures affecting multiple Tier 1 systems
- Natural disaster (hurricane, earthquake) impacting region

**Authority:**
- Tier 1 incident: CTO or VP of Engineering
- Organization-wide incident: CEO or Board of Directors

**Documentation:** Formal disaster declaration triggers insurance claims and regulatory notifications. Document decision rationale.

---

### Failover Procedures

**Pre-Failover Checklist:**
- [ ] Disaster declaration authorized
- [ ] DR team notified and assembled
- [ ] Stakeholders informed of expected downtime
- [ ] Current system state documented
- [ ] Failover runbook retrieved

**Failover Execution:**

1. **Activate DR Infrastructure**
   - Power on DR site servers
   - Verify network connectivity
   - Confirm backup data availability

2. **Restore Data**
   - Mount most recent backups
   - Validate data integrity
   - Verify database consistency

3. **Configure Applications**
   - Update DNS records to point to DR site
   - Reconfigure load balancers
   - Update API endpoints
   - Test application functionality

4. **Validate Recovery**
   - Smoke tests for critical workflows
   - Business owner validation
   - Monitor error rates and performance

5. **Communicate**
   - Notify users of service restoration
   - Update status page
   - Document recovery timeline

**Rollback Plan:** If DR activation fails, document rollback to primary (if available) or alternative recovery approach.

---

### Failback Procedures

Returning operations to primary site after disaster recovery.

**Timing:** Do not rush failback. Ensure primary site is fully repaired, tested, and stable.

**Failback Steps:**
1. Rebuild/repair primary infrastructure
2. Synchronize data from DR site to primary
3. Validate data consistency
4. Schedule failback window (low-traffic period)
5. Execute reverse cutover
6. Monitor primary site for 72 hours
7. Maintain DR site in standby for 30 days

**Risk:** Failback introduces additional risk. Second outage during failback is common if rushed.

---

## Disaster Recovery Testing

Untested plans fail during actual disasters. Regular DR drills are mandatory.

### Testing Frequency

**Full DR Failover Test:**
- Tier 1 systems: Annual
- Tier 2 systems: Every 18 months
- Tier 3 systems: Every 2-3 years

**Tabletop Exercises:**
- Quarterly walkthrough of disaster scenarios
- No actual failover, discuss response steps
- Identify gaps in plan or team knowledge

**Component Testing:**
- Monthly restoration of individual systems
- Validate backup integrity without full DR activation

---

### Test Scenarios

**Scenario 1: Data Center Fire**
- Total loss of primary facility
- Full failover to DR site required
- Tests infrastructure redundancy, data replication, communication

**Scenario 2: Ransomware Attack**
- Primary systems encrypted
- Restore from clean backups
- Tests backup isolation, restoration speed, malware removal

**Scenario 3: Database Corruption**
- Critical database corruption beyond repair
- Point-in-time recovery required
- Tests backup granularity, database recovery procedures

**Scenario 4: Regional Outage**
- Cloud provider region failure
- Failover to alternate region
- Tests multi-region architecture, DNS failover, data synchronization

**Randomization:** Announce some DR tests 24 hours in advance (planned). Execute others without warning (surprise). Surprise tests reveal true readiness.

---

### Test Evaluation

**Success Criteria:**
- RTO achieved (system restored within target time)
- RPO achieved (data loss within acceptable threshold)
- No data corruption during failover
- Business-critical workflows functional
- Team executed plan without significant gaps

**After-Action Report:**
- Actual RTO vs target
- Actual RPO vs target
- Issues encountered
- Runbook updates required
- Training gaps identified
- Infrastructure improvements needed

**Continuous Improvement:** Update DR plan after every test. Increment plan version number. Notify team of changes.

---

## Data Retention and Disposal

### Retention Requirements

**Production Data:**
- Tier 1: 7 years (financial and regulatory compliance)
- Tier 2: 3 years
- Tier 3: 1 year
- Tier 4: 90 days

**Backup Data:**
- Daily backups: 30 days minimum
- Weekly backups: 13 weeks (3 months)
- Monthly backups: 12 months
- Annual backups: 7 years (compliance)

**Audit Logs:**
- Security events: 7 years
- Access logs: 1 year
- Application logs: 90 days

**Legal Hold:** Suspend deletion when litigation or investigation pending. Legal team provides hold notification and release.

---

### Secure Disposal

**End of Retention:**
When retention period expires, data must be securely deleted to comply with privacy regulations.

**Disposal Methods:**

**Logical Deletion (Cloud/Virtual):**
- Cryptographic erasure (destroy encryption keys)
- Overwrite with random data (DoD 5220.22-M standard: 7-pass overwrite)
- Verify deletion completion

**Physical Destruction (On-Premise):**
- Hard drives: Shred or degauss
- Tapes: Incinerate or shred
- SSDs: Cryptographic erasure (overwriting doesn't work on SSDs)

**Certification:**
- Third-party disposal vendor provides certificate of destruction
- Certificate includes: date, method, list of destroyed media, witness signatures
- Retain certificates for 7 years

---

## Contingency Planning Roles

**Contingency Planning Coordinator:**
- Maintains DR plan
- Schedules and coordinates testing
- Tracks RTO/RPO metrics
- Updates plan based on infrastructure changes

**Backup Administrators:**
- Configure and monitor backups
- Verify backup completion
- Execute restoration tests
- Troubleshoot backup failures

**DR Team:**
- Executes failover/failback procedures
- Business continuity during disasters
- Composed of system administrators, network engineers, database administrators

**Business Owners:**
- Define RTO/RPO requirements
- Validate recovery success
- Approve disaster declaration
- Communicate with customers during outages

---

## Contingency Planning Checklist

**Backup Configuration:**
- [ ] All systems assigned to tier
- [ ] Backup schedules configured per tier
- [ ] Encryption enabled (at rest and in transit)
- [ ] Immutability configured for critical systems
- [ ] Offsite replication active
- [ ] Air-gapped backups for Tier 1 systems
- [ ] Access controls implemented (separation of duties)

**Recovery:**
- [ ] RTO/RPO documented for all systems
- [ ] DR site identified and configured
- [ ] Failover procedures documented
- [ ] Failback procedures documented
- [ ] Disaster declaration criteria documented
- [ ] DR team roles assigned

**Testing:**
- [ ] Automated verification enabled
- [ ] Restoration tests scheduled
- [ ] Full DR test scheduled annually
- [ ] Tabletop exercises scheduled quarterly
- [ ] Test results documented
- [ ] Plan updated after tests

**Compliance:**
- [ ] Retention policies documented
- [ ] Disposal procedures documented
- [ ] Audit logs retained per requirements
- [ ] Legal hold procedures documented
- [ ] Certificates of destruction maintained

---

## References

- NIST SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems
- NIST SP 800-184: Guide for Cybersecurity Event Recovery
- FedRAMP Contingency Planning (CP) Control Family
- ISO/IEC 27031: Business Continuity Management
- Uptime Institute Tier Standards: https://uptimeinstitute.com/tiers
