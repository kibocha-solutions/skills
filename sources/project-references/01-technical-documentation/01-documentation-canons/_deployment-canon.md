# Canon: Deployment Documentation

## Purpose

Deployment documentation provides complete instructions for deploying the system across all environments (local development, staging, production). It ensures consistent, repeatable deployments and enables rapid disaster recovery.

---

## Scope

**This canon applies to:**
- Production deployment procedures
- Staging environment setup
- Local development environment setup
- Infrastructure provisioning
- CI/CD pipeline configuration
- Rollback and disaster recovery procedures

**This canon does NOT apply to:**
- Code deployment within containers (document in service README)
- Database migrations (use database documentation canon)
- Configuration management (use configuration documentation canon)

---

## Access Level Classification

**Deployment Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** DevOps team, authorized developers, system administrators
- **Storage:** Private repository with authentication
- **Review:** DevOps review, security clearance for production procedures
- **Rationale:** Contains infrastructure details, credentials references, security-sensitive procedures

**Exception:** Local development setup may be Public (Level 1) for open-source projects

---

## When to Generate

### Initial Creation
- **Before First Deployment:** Document deployment process during infrastructure setup
- **Infrastructure as Code:** Create alongside Terraform/CloudFormation templates
- **CI/CD Setup:** Document as pipelines are configured

### Updates
- After infrastructure changes
- When adding new deployment environments
- After CI/CD pipeline modifications
- After security or compliance changes

### Frequency
- **Initial:** During infrastructure setup phase
- **Major Updates:** After significant infrastructure changes
- **Minor Updates:** Monthly for accuracy verification
- **Emergency:** Immediately after production incidents requiring procedure updates

---

## Files to Generate

Agent must create the following files when documenting deployment:

### 1. Deployment Index (Entry Point)
**File:** `/docs/source/deployment/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Deployment documentation entry point linking to all deployment topics

### 2. Local Development Setup
**File:** `/docs/source/deployment/01-local-development.rst`  
**Format:** reStructuredText  
**Purpose:** Step-by-step guide for setting up local development environment

### 3. Staging Deployment
**File:** `/docs/source/deployment/02-staging.rst`  
**Format:** reStructuredText  
**Purpose:** Staging environment deployment procedures

### 4. Production Deployment
**File:** `/docs/source/deployment/03-production.rst`  
**Format:** reStructuredText  
**Purpose:** Production deployment procedures and checklists

### 5. Infrastructure Setup
**File:** `/docs/source/deployment/04-infrastructure.rst`  
**Format:** reStructuredText  
**Purpose:** Infrastructure provisioning guide (Terraform, CloudFormation, Kubernetes)

### 6. CI/CD Pipeline
**File:** `/docs/source/deployment/05-ci-cd-pipeline.rst`  
**Format:** reStructuredText  
**Purpose:** CI/CD pipeline configuration and workflow

### 7. Rollback Procedures
**File:** `/docs/source/deployment/06-rollback.rst`  
**Format:** reStructuredText  
**Purpose:** Rollback procedures for failed deployments

### 8. Disaster Recovery
**File:** `/docs/source/deployment/07-disaster-recovery.rst`  
**Format:** reStructuredText  
**Purpose:** Disaster recovery procedures and business continuity

---

## Directory Structure

```
docs/source/deployment/
├── 00-index.rst                    # Deployment documentation entry point
├── 01-local-development.rst        # Local dev environment setup
├── 02-staging.rst                  # Staging deployment procedures
├── 03-production.rst               # Production deployment procedures
├── 04-infrastructure.rst           # Infrastructure provisioning
├── 05-ci-cd-pipeline.rst           # CI/CD configuration
├── 06-rollback.rst                 # Rollback procedures
└── 07-disaster-recovery.rst        # Disaster recovery guide
```

---

## Generation Rules

### Procedural Documentation

Deployment documentation is inherently procedural. Use numbered lists for step-by-step instructions.

**Format:**
1. Prerequisites
2. Step-by-step instructions
3. Verification steps
4. Troubleshooting common issues

### Code Blocks

Include complete, runnable commands:

```rst
.. code-block:: bash

   # Install dependencies
   npm install

   # Run database migrations
   npm run migrate

   # Start development server
   npm run dev
```

### Environment-Specific Instructions

Clearly separate instructions for different environments:

```rst
Local Development
-----------------

Use Docker Compose:

.. code-block:: bash

   docker-compose up -d

Staging Environment
-------------------

Deploy to AWS ECS:

.. code-block:: bash

   aws ecs update-service --cluster staging --service app --force-new-deployment
```

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice preferred ("Run the command" not "The command should be run")
- Specific over vague (exact commands, not descriptions)
- Vary sentence structure
- No AI clichés
- **Lists ARE appropriate** for deployment procedures (exception to general list avoidance)

---

## Content Guidelines

### Deployment Index (`/docs/source/deployment/00-index.rst`)

```rst
Deployment Documentation
========================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains sensitive infrastructure details.
   Do not share with external parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

This documentation covers deployment procedures for all environments:

- **Local Development**: Docker Compose setup on developer machines
- **Staging**: AWS ECS cluster for pre-production testing
- **Production**: Kubernetes cluster on AWS EKS

Quick Links
-----------

- **First time?** Start with :doc:`01-local-development`
- **Deploying to staging?** See :doc:`02-staging`
- **Production deployment?** Follow :doc:`03-production` checklist
- **Infrastructure changes?** Review :doc:`04-infrastructure`
- **Need to rollback?** See :doc:`06-rollback`

.. toctree::
   :maxdepth: 2

   01-local-development
   02-staging
   03-production
   04-infrastructure
   05-ci-cd-pipeline
   06-rollback
   07-disaster-recovery

Deployment Philosophy
---------------------

**Infrastructure as Code**
All infrastructure is defined in Terraform. No manual changes to production infrastructure.

**Automated Deployments**
All deployments use GitHub Actions. No manual deployments to staging or production.

**Immutable Infrastructure**
Servers are never updated in place. Deploy new versions, then destroy old ones.

**Zero-Downtime Deployments**
All production deployments use blue-green strategy with health checks.

Deployment Checklist
--------------------

Before deploying to production:

1. [ ] All tests pass in CI/CD
2. [ ] Staging deployment successful
3. [ ] Manual QA completed on staging
4. [ ] Database migrations tested
5. [ ] Rollback plan documented
6. [ ] On-call engineer notified
7. [ ] Change request approved (if required)
8. [ ] Deployment window scheduled

Emergency Contacts
------------------

- **DevOps Lead**: devops@example.com
- **On-Call Engineer**: oncall@example.com (PagerDuty)
- **AWS Support**: Premium support (Case ID required)
```

### Local Development Setup (`/docs/source/deployment/01-local-development.rst`)

```rst
Local Development Setup
=======================

This guide explains how to set up a complete development environment on your local machine.

Prerequisites
-------------

Install the following before proceeding:

**Required:**
- Docker Desktop 4.0+ (https://docker.com/products/docker-desktop)
- Node.js 18+ (https://nodejs.org/)
- Git 2.30+ (https://git-scm.com/)

**Optional:**
- PostgreSQL client (`psql`) for database access
- Redis CLI (`redis-cli`) for cache debugging

Verify installations:

.. code-block:: bash

   docker --version
   node --version
   git --version

Initial Setup
-------------

**1. Clone Repository**

.. code-block:: bash

   git clone https://github.com/example/tax-management-system.git
   cd tax-management-system

**2. Install Dependencies**

.. code-block:: bash

   npm install

**3. Configure Environment**

Copy the example environment file:

.. code-block:: bash

   cp .env.example .env.local

Edit `.env.local` with your settings:

.. code-block:: bash

   # Database
   DATABASE_URL=postgres://user:password@localhost:5432/tms_dev

   # Redis
   REDIS_URL=redis://localhost:6379

   # API Keys (development only)
   KRA_API_KEY=dev_test_key
   MPESA_API_KEY=dev_test_key

**4. Start Services**

Start all services with Docker Compose:

.. code-block:: bash

   docker-compose up -d

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- RabbitMQ on port 5672 (management UI on 15672)

Verify services are running:

.. code-block:: bash

   docker-compose ps

Expected output:

.. code-block:: text

   NAME                STATUS
   tms_postgres_1      Up 30 seconds
   tms_redis_1         Up 30 seconds
   tms_rabbitmq_1      Up 30 seconds

**5. Run Database Migrations**

.. code-block:: bash

   npm run migrate

**6. Seed Development Data**

.. code-block:: bash

   npm run seed

This creates:
- Test user accounts
- Sample tax calculations
- Test receipts

**7. Start Development Server**

.. code-block:: bash

   npm run dev

The application is now running at:

- **Web App**: http://localhost:3000
- **API**: http://localhost:3000/api
- **GraphQL Playground**: http://localhost:3000/graphql

Default Credentials
-------------------

Use these credentials for testing:

**Admin User:**
- Email: admin@example.com
- Password: admin123

**Regular User:**
- Email: user@example.com
- Password: user123

Troubleshooting
---------------

**Issue: Port already in use**

If port 5432 (PostgreSQL) or 6379 (Redis) is already in use:

.. code-block:: bash

   # Stop existing services
   docker-compose down

   # Or change ports in docker-compose.yml

**Issue: Database connection failed**

Check PostgreSQL is running:

.. code-block:: bash

   docker-compose logs postgres

Verify connection string in `.env.local` matches docker-compose ports.

**Issue: Migrations fail**

Reset database:

.. code-block:: bash

   docker-compose down -v
   docker-compose up -d
   npm run migrate

Daily Workflow
--------------

**Start working:**

.. code-block:: bash

   docker-compose up -d
   npm run dev

**Stop working:**

.. code-block:: bash

   # Stop dev server (Ctrl+C)
   docker-compose down

**View logs:**

.. code-block:: bash

   # Application logs
   npm run dev

   # Database logs
   docker-compose logs -f postgres

   # All service logs
   docker-compose logs -f
```

### Production Deployment (`/docs/source/deployment/03-production.rst`)

```rst
Production Deployment
=====================

.. danger::
   PRODUCTION DEPLOYMENT - RESTRICTED
   Follow this checklist exactly. Unauthorized deployments are prohibited.
   Contact DevOps lead before proceeding.

Overview
--------

Production deployments use GitHub Actions with manual approval gates.
All deployments follow blue-green strategy for zero-downtime releases.

Deployment Schedule
-------------------

**Allowed Windows:**
- Monday-Thursday: 10:00-16:00 EAT
- Friday: 10:00-14:00 EAT (emergency only after 14:00)
- Saturday-Sunday: Emergency only (requires VP approval)

**Blackout Periods (No Deployments):**
- Dec 20 - Jan 5 (Holiday freeze)
- Last business day of each month (Finance close)
- During active incidents (Sev 1 or Sev 2)

Pre-Deployment Checklist
-------------------------

Before triggering production deployment:

**Code Quality:**

1. [ ] All CI/CD checks pass (tests, lint, security scan)
2. [ ] Code review approved by 2+ senior engineers
3. [ ] No open Sev 1 or Sev 2 bugs related to this change

**Testing:**

4. [ ] Staging deployment successful
5. [ ] Manual QA completed on staging
6. [ ] Load testing completed (if performance-critical)
7. [ ] Security review completed (if touching auth/authz)

**Database:**

8. [ ] Database migrations tested on staging
9. [ ] Migrations are backwards-compatible (if rollback needed)
10. [ ] Database backup completed within last 24 hours

**Coordination:**

11. [ ] Deployment window scheduled and communicated
12. [ ] On-call engineer notified and available
13. [ ] Product owner aware of deployment
14. [ ] Change request approved (if required by compliance)

**Rollback Plan:**

15. [ ] Rollback procedure documented
16. [ ] Rollback tested on staging
17. [ ] Engineer prepared to execute rollback if issues arise

Deployment Procedure
--------------------

**1. Create Deployment Tag**

.. code-block:: bash

   git tag -a v1.5.0 -m "Release v1.5.0: Tax calculation improvements"
   git push origin v1.5.0

**2. Trigger GitHub Actions Workflow**

Navigate to GitHub Actions → "Deploy to Production" workflow.

Click "Run workflow" and enter:

- **Tag**: v1.5.0
- **Environment**: production
- **Approval Required**: Yes

**3. Wait for Approval Gate**

The workflow pauses after building the Docker image.

**Required Approvals**: 2 DevOps engineers

Approvers verify:
- Correct tag version
- All pre-deployment checks complete
- Deployment window active

**4. Monitor Deployment**

Watch GitHub Actions logs in real-time.

Deployment steps:

1. Build Docker image
2. Push to ECR
3. Update Kubernetes deployment (rolling update)
4. Wait for health checks
5. Run smoke tests
6. Route traffic to new pods
7. Drain old pods
8. Complete

Expected duration: 10-15 minutes

**5. Post-Deployment Verification**

Run smoke tests:

.. code-block:: bash

   # API health check
   curl https://api.example.com/health

   # Database connectivity
   curl https://api.example.com/health/db

   # Redis connectivity
   curl https://api.example.com/health/redis

Check monitoring dashboards:

- Grafana: https://grafana.example.com
- Error rate (should be < 0.1%)
- Response time (p95 < 200ms)
- 5xx errors (should be zero)

Verify recent transactions processed successfully:

.. code-block:: bash

   # Check last 10 tax calculations
   kubectl exec -n production deploy/api -- \
     psql $DATABASE_URL -c "SELECT id, created_at FROM calculations ORDER BY created_at DESC LIMIT 10"

Post-Deployment Checklist
--------------------------

After successful deployment:

1. [ ] Smoke tests pass
2. [ ] Error rate within acceptable range
3. [ ] Response times normal
4. [ ] No spike in 5xx errors
5. [ ] Customer-facing features verified
6. [ ] On-call engineer monitors for 1 hour
7. [ ] Deployment announced in #engineering Slack
8. [ ] Release notes published (if customer-visible changes)

Rollback Procedure
------------------

If issues detected, immediately rollback:

.. code-block:: bash

   # Rollback to previous version
   kubectl rollout undo deployment/api -n production

See :doc:`06-rollback` for complete rollback procedures.

Emergency Deployment
--------------------

For Sev 1 incidents requiring immediate deployment:

**Approval Required:**
- VP Engineering (for production outages)
- On-call engineer (execution)

**Abbreviated Checklist:**
1. [ ] Code review (1 senior engineer minimum)
2. [ ] Tests pass
3. [ ] Rollback plan ready

**Communication:**
- Post in #incidents Slack channel
- Page on-call engineer
- Notify customers via status page if customer-impact
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all deployment reST files
rstcheck docs/source/deployment/*.rst
```

**Expected output:** No errors

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

### Command Verification

- [ ] All bash commands are syntactically correct
- [ ] All file paths are accurate
- [ ] All URLs are valid
- [ ] All code blocks specify language for syntax highlighting

---

## Examples Reference

See working example: `02-examples/deployment-example/` (to be created)

**Example includes:**
- Complete deployment documentation set
- Local development setup guide
- Production deployment checklist
- CI/CD pipeline documentation
- Rollback procedures

---

## Access Level Warning

Include at top of `00-index.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains sensitive infrastructure details.
   Do not share with external parties.
```

For production deployment docs, use stronger warning:

```rst
.. danger::
   PRODUCTION DEPLOYMENT - RESTRICTED
   Follow procedures exactly. Unauthorized deployments prohibited.
```

---

## Agent Checklist

Before marking deployment documentation complete, verify:

- [ ] Deployment index (00-index.rst) created
- [ ] Local development setup documented with prerequisites
- [ ] Staging deployment procedures documented
- [ ] Production deployment procedures with checklist
- [ ] Infrastructure provisioning guide created
- [ ] CI/CD pipeline documented
- [ ] Rollback procedures detailed
- [ ] Disaster recovery guide created
- [ ] All commands tested and accurate
- [ ] Access level warnings included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Procedural steps numbered correctly
- [ ] Troubleshooting sections included

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial deployment documentation canon
- Based on DevOps best practices
- Follows `_docs-canon.md` v4 specifications
