# Logging and Monitoring

## 10.1 Tamper-Proof Audit Logging

**Why Critical:**
Tamper-proof logging is cornerstone of robust audit trail management. Required for:
- Legal defensibility
- Compliance demonstrations
- Forensic investigations
- Insider threat detection

**What to Log:**

**Authentication Events:**
- Login attempts (success and failure)
- Logout events
- Password changes
- MFA challenges
- Account lockouts

**Authorization Events:**
- Access granted
- Access denied
- Permission changes
- Role assignments

**Data Access:**
- Who viewed what resource
- When it was accessed
- From what IP address/location

**Data Modification:**
- Who changed what
- Old value → New value
- Timestamp
- Reason (if applicable)

**Administrative Actions:**
- User creation/deletion
- Permission changes
- Configuration changes
- System shutdowns/restarts

**Security Events:**
- Rate limit violations
- Suspicious activity patterns
- Failed authentication patterns
- Unusual access patterns

**Immutability Requirements:**

**Write-Once, Read-Many (WORM) Storage:**
- Logs cannot be modified after writing
- Logs cannot be deleted (only archived after retention period)

**Cryptographic Chaining:**
Each log entry includes hash of previous entry:

```json
{
  "timestamp": "2025-12-29T22:15:30.123Z",
  "user_id": "user_12345",
  "action": "data_modified",
  "resource_id": "record_456",
  "result": "success",
  "ip_address": "192.168.1.100",
  "changes": {
    "field_name": {"old": "value1", "new": "value2"}
  },
  "previous_hash": "a3f2d8e9b1c4...",
  "signature": "digital_signature_here"
}
```

**Storage Requirements:**
- Separate secure location (not same server as application)
- Encrypted at rest and in transit
- Access controls (only authorized audit personnel)
- Disaster recovery (logs must survive system failure)
- Retention policy (comply with legal requirements)

**Fail-Safe Design:**
If logging fails, system must **fail closed** (deny operation), not **fail open** (allow operation without logging).

**Verification:**
- [ ] All sensitive operations logged
- [ ] Logs use cryptographic chaining
- [ ] Logs stored separately and securely
- [ ] Log tampering detected
- [ ] Fail-safe behavior implemented
