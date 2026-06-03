# Canon: Operations & Runbook Documentation

## Purpose

Operations documentation (runbooks) provides step-by-step procedures for monitoring, troubleshooting, and responding to incidents. It enables on-call engineers to quickly diagnose and resolve issues, ensuring system reliability and minimizing downtime.

---

## Scope

**This canon applies to:**
- Production monitoring procedures
- Incident response playbooks
- Troubleshooting guides for common issues
- Escalation procedures
- Maintenance procedures (backups, updates, restarts)
- Health check procedures

**This canon does NOT apply to:**
- Development debugging (document in service README)
- Code-level troubleshooting (use code documentation)
- Performance optimization guides (use performance documentation canon if separated)

---

## Access Level Classification

**Operations/Runbook Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** On-call engineers, DevOps team, system administrators
- **Storage:** Private repository with authentication, also in incident management system (PagerDuty, Opsgenie)
- **Review:** DevOps review, incident response team approval
- **Rationale:** Contains operational procedures, system weaknesses, incident patterns

**Critical:** Runbooks must be accessible during outages (consider offline backup or status page)

---

## When to Generate

### Initial Creation
- **Before Production Launch:** Create runbooks for known failure scenarios
- **During Load Testing:** Document observed issues and resolutions
- **Post-Architecture Review:** Create runbooks for identified risks

### Updates
- After every production incident (capture learnings)
- When adding new services or dependencies
- After infrastructure changes
- Monthly review for accuracy

### Frequency
- **Initial:** Before production launch
- **Post-Incident:** Within 24 hours of incident resolution
- **Regular Review:** Monthly for accuracy
- **Major Updates:** After significant system changes

---

## Files to Generate

Agent must create the following files when documenting operations:

### 1. Operations Index (Entry Point)
**File:** `/docs/source/operations/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Operations documentation entry point

### 2. Runbook Template
**File:** `/docs/source/operations/01-runbook-template.rst`  
**Format:** reStructuredText  
**Purpose:** Template for creating new runbooks (shows correct structure)

### 3. Common Issues
**File:** `/docs/source/operations/02-common-issues.rst`  
**Format:** reStructuredText  
**Purpose:** Troubleshooting guide for frequently occurring issues

### 4. Alerting Guide
**File:** `/docs/source/operations/03-alerting-guide.rst`  
**Format:** reStructuredText  
**Purpose:** Explanation of all alerts, severity levels, and initial response

### 5. Incident Response
**File:** `/docs/source/operations/04-incident-response.rst`  
**Format:** reStructuredText  
**Purpose:** Incident response workflow and escalation procedures

### 6. Maintenance Procedures
**File:** `/docs/source/operations/05-maintenance-procedures.rst`  
**Format:** reStructuredText  
**Purpose:** Regular maintenance tasks (backups, certificate renewal, etc.)

### 7. Service-Specific Runbooks
**Files:** `/docs/source/operations/runbooks/[service-name].rst`  
**Format:** reStructuredText  
**Purpose:** Individual runbook for each critical service

---

## Directory Structure

```
docs/source/operations/
├── 00-index.rst                    # Operations documentation entry point
├── 01-runbook-template.rst         # Runbook template for reference
├── 02-common-issues.rst            # Troubleshooting common issues
├── 03-alerting-guide.rst           # Alert reference and responses
├── 04-incident-response.rst        # Incident response workflow
├── 05-maintenance-procedures.rst   # Regular maintenance tasks
└── runbooks/
    ├── api-gateway.rst             # API Gateway runbook
    ├── tax-calculation-service.rst # Tax service runbook
    ├── database.rst                # Database runbook
    ├── redis-cache.rst             # Redis runbook
    └── rabbitmq.rst                # RabbitMQ runbook
```

---

## Generation Rules

### Runbook Structure

Every runbook must follow this structure:

1. **Service Overview** (what the service does)
2. **Health Indicators** (how to know it's healthy)
3. **Common Failure Scenarios** (what goes wrong)
4. **Troubleshooting Steps** (how to diagnose)
5. **Resolution Procedures** (how to fix)
6. **Escalation Path** (when to escalate)

### Procedural Focus

Runbooks are action-oriented:

- Use imperative mood ("Check the logs", not "The logs should be checked")
- Include exact commands (not descriptions)
- Provide decision trees (if X, then do Y)
- Specify success criteria for each step

### Time-Critical Format

On-call engineers need fast answers:

- Put most common issues first
- Use clear headings
- Include quick health checks at top
- Provide copy-pasteable commands

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice ("Run this command", not "This command should be run")
- Specific over vague (exact commands, metrics, thresholds)
- **Lists ARE appropriate** for procedures
- Short, scannable paragraphs

---

## Content Guidelines

### Operations Index (`/docs/source/operations/00-index.rst`)

```rst
Operations & Runbooks
=====================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains operational procedures.
   Do not share with external parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

This documentation helps on-call engineers monitor, troubleshoot, and resolve
production incidents.

**For new on-call engineers:** Start with :doc:`04-incident-response`

Quick Access
------------

**During an Incident:**

1. Check :doc:`03-alerting-guide` for alert explanation
2. Follow service-specific runbook
3. Escalate using :doc:`04-incident-response` procedures

**Common Issues:**

- :ref:`database-connection-pool-exhausted`
- :ref:`redis-cache-miss-rate-high`
- :ref:`api-gateway-503-errors`

See :doc:`02-common-issues` for full list.

.. toctree::
   :maxdepth: 2

   01-runbook-template
   02-common-issues
   03-alerting-guide
   04-incident-response
   05-maintenance-procedures
   runbooks/index

Service Status
--------------

**Production Health Dashboard:**
https://grafana.example.com/production

**Key Metrics:**

- **API Response Time**: p95 < 200ms (target)
- **Error Rate**: < 0.1% (target)
- **Database Connections**: < 80% pool utilization
- **Redis Hit Rate**: > 95%

On-Call Schedule
----------------

**Current Rotation:** https://pagerduty.com/schedules/production

**Primary On-Call:** Notified for all Sev 1 and Sev 2 alerts  
**Secondary On-Call:** Notified if primary doesn't acknowledge within 5 minutes

Escalation Contacts
-------------------

- **DevOps Lead**: devops-lead@example.com
- **Engineering Manager**: eng-manager@example.com
- **VP Engineering**: vp-eng@example.com (Sev 1 only)
- **AWS Premium Support**: File ticket in AWS console
```

### Common Issues (`/docs/source/operations/02-common-issues.rst`)

```rst
Common Issues & Troubleshooting
================================

This document catalogs frequently occurring issues and their resolutions.

.. _database-connection-pool-exhausted:

Database Connection Pool Exhausted
-----------------------------------

**Symptoms:**

- Error logs: "connection pool exhausted"
- API requests timing out
- Database connection count at maximum

**Quick Check:**

.. code-block:: bash

   # Check current connections
   kubectl exec -n production deploy/postgres -- \
     psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

**Root Causes:**

1. Connection leak (app not closing connections)
2. Traffic spike exceeding pool size
3. Long-running queries holding connections

**Resolution:**

**Step 1: Immediate Mitigation**

Increase connection pool temporarily:

.. code-block:: bash

   # Edit deployment
   kubectl edit deployment api -n production

   # Update environment variable:
   # DB_POOL_SIZE: "50"  (from 20)

   # Trigger rolling restart
   kubectl rollout restart deployment/api -n production

**Step 2: Identify Leaking Connections**

Check for idle connections:

.. code-block:: bash

   kubectl exec -n production deploy/postgres -- \
     psql -U postgres -c \
     "SELECT pid, usename, application_name, state, state_change 
      FROM pg_stat_activity 
      WHERE state = 'idle' 
      AND state_change < now() - interval '5 minutes';"

**Step 3: Fix Root Cause**

- Review recent code changes touching database
- Check for missing `finally` blocks in connection handling
- Verify connection timeout configuration

**Prevention:**

- Monitor connection pool utilization (alert at 80%)
- Implement connection leak detection in tests
- Set max connection lifetime

.. _redis-cache-miss-rate-high:

Redis Cache Miss Rate High
---------------------------

**Symptoms:**

- Cache miss rate > 20%
- Increased database query load
- Slower API response times

**Quick Check:**

.. code-block:: bash

   # Check cache stats
   kubectl exec -n production deploy/redis -- redis-cli INFO stats | grep keyspace

**Root Causes:**

1. Cache key eviction (memory pressure)
2. Cache warming not running
3. Cache invalidation too aggressive
4. Redis restart (data loss if not persisted)

**Resolution:**

**Step 1: Check Redis Memory**

.. code-block:: bash

   kubectl exec -n production deploy/redis -- redis-cli INFO memory

Check `used_memory_peak` and `maxmemory` settings.

**Step 2: Identify Evicted Keys**

.. code-block:: bash

   kubectl exec -n production deploy/redis -- redis-cli INFO stats | grep evicted_keys

If evicted_keys is increasing rapidly, memory is insufficient.

**Step 3: Mitigate**

**Option A: Increase Redis Memory**

.. code-block:: bash

   # Edit Redis deployment
   kubectl edit statefulset redis -n production

   # Update resource limits:
   # memory: "4Gi"  (from 2Gi)

**Option B: Adjust Eviction Policy**

.. code-block:: bash

   kubectl exec -n production deploy/redis -- \
     redis-cli CONFIG SET maxmemory-policy allkeys-lru

**Step 4: Warm Cache**

.. code-block:: bash

   # Trigger cache warming job
   kubectl create job cache-warm-$(date +%s) \
     --from=cronjob/cache-warming -n production

**Prevention:**

- Monitor Redis memory usage (alert at 80%)
- Run cache warming after deployments
- Review TTL settings for frequently accessed keys

.. _api-gateway-503-errors:

API Gateway Returning 503 Errors
---------------------------------

**Symptoms:**

- 503 Service Unavailable responses
- Users unable to access API
- Traffic spike or backend service down

**Quick Check:**

.. code-block:: bash

   # Check backend service health
   kubectl get pods -n production

   # Check Kong Gateway logs
   kubectl logs -n production deploy/kong --tail=100

**Root Causes:**

1. Backend service unavailable
2. Rate limiting triggered
3. Circuit breaker open
4. Kong Gateway overloaded

**Resolution:**

**Step 1: Identify Backend Status**

.. code-block:: bash

   # Check service endpoints
   kubectl get endpoints -n production

   # Verify pods are ready
   kubectl get pods -n production -l app=api

If pods are not ready, check their logs:

.. code-block:: bash

   kubectl logs -n production deploy/api --tail=200

**Step 2: Check Rate Limiting**

.. code-block:: bash

   # Check Kong rate limiting plugin
   kubectl exec -n production deploy/kong -- \
     kong health

   # Verify rate limit settings
   kubectl get kongplugin -n production

**Step 3: Resolve**

**If backend unhealthy:**

.. code-block:: bash

   # Force rollout restart
   kubectl rollout restart deployment/api -n production

   # Monitor rollout
   kubectl rollout status deployment/api -n production

**If rate limit hit:**

Temporarily increase limits (requires approval):

.. code-block:: bash

   # Edit Kong plugin
   kubectl edit kongplugin rate-limiting -n production

   # Increase limit (e.g., 1000 -> 2000 requests/minute)

**If circuit breaker open:**

Circuit breaker closes automatically after timeout.
Verify backend service is healthy, then wait for timeout.

**Escalation:**

If issue persists > 15 minutes and backend appears healthy, escalate to DevOps lead.
```

### Incident Response (`/docs/source/operations/04-incident-response.rst`)

```rst
Incident Response Workflow
===========================

This document defines the incident response process for production issues.

Severity Levels
---------------

**Severity 1 (Critical)**
- Complete service outage
- Data loss or corruption
- Security breach

**Response Time**: 15 minutes  
**Escalation**: Immediate (notify VP Engineering)

**Severity 2 (High)**
- Partial service degradation
- Performance severely impacted
- Single critical feature unavailable

**Response Time**: 30 minutes  
**Escalation**: After 1 hour if unresolved

**Severity 3 (Medium)**
- Minor feature unavailable
- Performance slightly degraded
- Non-critical errors

**Response Time**: Next business day  
**Escalation**: Not required

**Severity 4 (Low)**
- Cosmetic issues
- Documentation errors
- Enhancement requests

**Response Time**: As time permits  
**Escalation**: Not required

Incident Response Steps
-----------------------

**1. Acknowledge Alert (< 5 minutes)**

- Acknowledge in PagerDuty
- Post in #incidents Slack channel:
  
  .. code-block:: text

     INCIDENT: [Brief description]
     SEVERITY: [1-4]
     OWNER: [Your name]
     STATUS: Investigating

**2. Assess Severity (< 5 minutes)**

- How many users affected?
- Is data at risk?
- Is service completely down or degraded?

Update severity if needed.

**3. Communicate Status**

**Sev 1:**
- Update status page: https://status.example.com
- Post in #incidents every 15 minutes

**Sev 2:**
- Post in #incidents every 30 minutes

**4. Investigate Root Cause**

- Check relevant runbook
- Review monitoring dashboards
- Check recent deployments/changes
- Review application logs

**5. Implement Fix**

**Prefer:** Rollback to last known good version  
**If not possible:** Apply hotfix

For rollbacks, see :doc:`/deployment/06-rollback`

**6. Verify Resolution**

- Check health dashboard
- Verify error rate returned to normal
- Confirm user-facing functionality works

**7. Post-Incident**

- Mark incident resolved in PagerDuty
- Update #incidents:

  .. code-block:: text

     RESOLVED: [Brief description]
     DURATION: [X minutes/hours]
     ROOT CAUSE: [Brief explanation]
     NEXT STEPS: Post-mortem scheduled

- Schedule post-mortem meeting (within 48 hours)

Escalation Paths
----------------

**Sev 1 Incidents:**

1. Primary On-Call (PagerDuty notification)
2. Secondary On-Call (if no ack in 5 min)
3. DevOps Lead (call/SMS)
4. VP Engineering (call/SMS)

**Sev 2 Incidents:**

1. Primary On-Call
2. DevOps Lead (if unresolved after 1 hour)

**Contact Information:**

- DevOps Lead: +254-XXX-XXXXXX
- VP Engineering: +254-XXX-XXXXXX

War Room
--------

For Sev 1 incidents, establish war room:

**Zoom Link:** https://zoom.us/j/incident-war-room  
**Slack Channel:** #incident-war-room

Roles during incident:

- **Incident Commander**: Coordinates response
- **Tech Lead**: Implements fixes
- **Communications Lead**: Updates stakeholders
- **Scribe**: Documents timeline for post-mortem
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all operations reST files
rstcheck docs/source/operations/*.rst
rstcheck docs/source/operations/runbooks/*.rst
```

**Expected output:** No errors

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

### Runbook Testing

- [ ] All commands tested in staging environment
- [ ] All links work
- [ ] All referenced dashboards exist
- [ ] Contact information up to date

---

## Examples Reference

See working example: `02-examples/operations-example/` (to be created)

**Example includes:**
- Complete operations documentation
- Service-specific runbook
- Common issues guide
- Incident response procedures

---

## Access Level Warning

Include at top of all operations docs:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains operational procedures.
   Ensure availability during outages (consider offline backup).
```

---

## Agent Checklist

Before marking operations documentation complete, verify:

- [ ] Operations index created
- [ ] Runbook template provided
- [ ] Common issues documented with resolutions
- [ ] Alerting guide created with severity levels
- [ ] Incident response workflow documented
- [ ] Maintenance procedures documented
- [ ] Service-specific runbooks created for critical services
- [ ] All commands tested and accurate
- [ ] Escalation contacts current
- [ ] Links to dashboards working
- [ ] Access level warnings included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Procedures are actionable and time-critical

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial operations/runbook documentation canon
- Based on incident response best practices
- Follows `_docs-canon.md` v4 specifications
