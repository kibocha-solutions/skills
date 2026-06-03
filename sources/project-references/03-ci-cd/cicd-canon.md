# CI/CD Canon: Continuous Integration and Continuous Deployment Standards

This document provides comprehensive, non-negotiable CI/CD standards for all projects following the Vibe Code Canon framework.

**Authority:** These standards have ABSOLUTE AUTHORITY and MUST be followed alongside the CI/CD checklist in agent instructions. All examples provided are for contextual purposes ONLY and should not be assumed to be part of the CI/CD canon or project requirements.

---

## Section 1: Git Workflow and Branching Strategies

### 1.1 Trunk-Based Development (RECOMMENDED)

**Definition:**
Developers commit directly into trunk/main at least once a day with no long-lived feature branches.

**Core Principles:**
- Shared trunk kept in constant releasable state
- Small, frequent changes instead of large batches
- All commits visible immediately
- Feature flags for incomplete features

**Advantages:**
- [APPROVED] Enables true continuous integration
- [APPROVED] Eliminates merge conflicts
- [APPROVED] Better visibility across team
- [APPROVED] Faster releases
- [APPROVED] Easier conflict resolution
- [APPROVED] Encourages collaboration

**Disadvantages:**
- [CAUTION] Requires strong test coverage
- [CAUTION] Requires feature flags infrastructure
- [CAUTION] Team must be disciplined about commit quality

**When to Use:**
- Teams practicing true CI/CD
- Fast-paced development environments
- Mature testing practices in place
- Small to medium teams

**Requirements:**
- [ ] All commits must pass automated tests
- [ ] Commits at least once per day
- [ ] Feature flags for incomplete work
- [ ] Comprehensive test coverage (minimum 80%)
- [ ] Code review before merge (pair programming or async review)

---

### 1.2 GitHub Flow (ALTERNATIVE)

**Definition:**
Feature branch workflow optimized for continuous deployment.

**Workflow:**
1. Create feature branch from main
2. Work on feature with regular commits
3. Open pull request when ready
4. Code review and approval
5. Merge to main
6. Deploy immediately

**Advantages:**
- [APPROVED] Simple and straightforward
- [APPROVED] Supports formal code review
- [APPROVED] Aligns with CI/CD pipelines
- [APPROVED] Good for fast-paced projects

**Disadvantages:**
- [CAUTION] Merge conflicts if branches live too long
- [CAUTION] Deployment tied to merge (less flexible)

**When to Use:**
- Teams requiring formal code review gates
- Open source projects
- Teams new to CI/CD
- Need pull request-based workflows

**Requirements:**
- [ ] Feature branches short-lived (maximum 2-3 days)
- [ ] Pull requests reviewed within 24 hours
- [ ] Automated tests run on every pull request
- [ ] Main branch always deployable
- [ ] Immediate deployment after merge

---

### 1.3 GitFlow (NOT RECOMMENDED for CI/CD)

**Definition:**
Complex branching model with multiple long-lived branches (master, develop, feature, release, hotfix).

**Why NOT Recommended:**
- [REJECTED] Complex and heavyweight
- [REJECTED] Creates merge conflicts
- [REJECTED] Slows down integration
- [REJECTED] NOT suitable for continuous deployment

**When to Use:**
- ONLY if forced to have scheduled releases (quarterly, annually)
- Traditional waterfall processes
- **Avoid for modern CI/CD practices**

---

### 1.4 Commit Standards

**Commit Frequency:**
- Commit small, incremental changes
- Minimum once per day for trunk-based development
- Maximum 400 lines changed per commit (ideal: 50-100 lines)

**Commit Quality:**
- Every commit must pass all tests
- Every commit must be deployable
- Use Conventional Commits format (see Section 5 in AGENTS.md)

**Broken Builds:**
- Fix broken builds immediately (highest priority)
- Revert commit if cannot fix within 10 minutes
- No new features until build is green

---

### 1.5 Branch Protection & Git Identity Standards (MANDATORY)

**1.5.1 Mandatory Alias Usage for Git Operations:**
-   For all standard git operations (`git push`, `git pull`, commit management), you **MUST** use the SSH alias URL (e.g., `git@alias:owner/repo.git`).
-   This is mandatory for identity management and access control.

**1.5.2 Exception for GitHub CLI (`gh`) Users:**
-   The GitHub CLI (`gh`) does not support custom SSH aliases.
-   **ONLY** when performing operations that require `gh` (like creating a Pull Request):
    a. **Temporarily switch** to the standard GitHub URL (`git@github.com:...`).
    b. **Perform the `gh` operation** (e.g., `gh pr create`).
    c. **IMMEDIATELY restore** the SSH alias URL.

**1.5.3 Branch Protection Rules:**
-   [x] **Require a pull request before merging:** No direct commits to main.
-   [x] **Require status checks to pass before merging:**
    - Build must pass
    - Linting must pass
    - Tests must pass
-   [x] **Require branches to be up to date before merging**
-   [x] **Do not allow bypassing the above settings:** Even for admins.
-   [x] **Restrict pushes:** Prevents `git push --force`.

**Handling Branch Protection Failures:**
-   If Branch Protection Rules fail to apply via CLI with a 403/Upgrade error, it is likely because the Organization is on a **GitHub Free** plan with **Private** repositories.
-   **Protocol**: Notify the user immediately. Do not retry endlessly. Proceed with manual discipline.

### 1.6 Forbidden Files Protocol (ZERO TOLERANCE)

**Authority:** The CI pipeline MUST explicitly reject any commit containing Agent Instruction Files.

**Forbidden Files:**
- `AGENTS.md` (in root or any folder)
- `RULE.md`
- `copilot-instructions.md`
- Any file matching `00-project-references/` content structure.

**Action:**
- **Reject Commit**: Check status MUST fail.
- **Rollback**: If pushed, the commit MUST be reverted immediately.
- **Alert**: User must be notified of the security violation.

> [!CRITICAL]
> **NEVER EVER push agent instruction files.** These contain internal logic and must remain local-only or in the `00-project-references` submodule.

---

## Section 2: Pipeline Architecture and Best Practices

### 2.1 Core Pipeline Principles

**1. Fail Fast**

Run fastest tests first, stop on first failure:

```
Pipeline Order:
1. Linting (seconds)
2. Unit tests (< 1 minute)
3. Integration tests (< 10 minutes)
4. Build artifacts
5. E2E tests (< 30 minutes)
6. Deploy to staging
7. Smoke tests
8. Deploy to production
```

**Why:** Provides immediate feedback, saves compute resources.

---

**2. Single Path to Production**

**Critical Rule:** ALL deployments MUST go through the pipeline. No exceptions.

**Forbidden:**
- [REJECTED] Manual deployments
- [REJECTED] SSH into production to fix things
- [REJECTED] Bypassing pipeline for hotfixes
- [REJECTED] Direct database changes in production

**Why:** Enforces standardized, auditable, repeatable process.

---

**3. Automate Everything**

**Automate:**
- Build process
- Test execution
- Artifact creation
- Deployment to all environments
- Rollback procedures
- Environment provisioning

**Manual steps allowed ONLY for:**
- Production deployment approval (if required by compliance)
- Security incident response
- Disaster recovery

---

**4. Maintain Stable Builds**

**Requirements:**
- Master/main branch MUST always be stable
- Every commit MUST pass all tests
- Broken builds fixed within 10 minutes or reverted

**Monitoring:**
- Track build stability percentage (target: 95%+)
- Alert team immediately on failures
- Dashboard showing current build status

---

### 2.2 Pipeline Performance Optimization

**Research Finding:** High-performing teams resolve pipeline issues 45% faster than low-performers.

**Optimization Strategies:**

**1. Intelligent Caching**

```yaml
# Example: npm dependencies
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: node_modules
    key: npm-${{ hashFiles('package-lock.json') }}
```

**Cache:**
- Dependencies (npm, pip, cargo, maven)
- Docker layers
- Build artifacts
- Test results (for incremental testing)

**Benefits:** 50-80% faster build times.

---

**2. Parallel Execution**

```yaml
# Example: Parallel test jobs
test:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
  steps:
    - run: npm test -- --shard=${{ matrix.shard }}/4
```

**Parallelize:**
- Independent test suites
- Multiple environment deployments
- Linting and security scans

**Benefits:** 40-60% faster total pipeline time.

---

**3. Incremental Testing**

Run only tests affected by code changes:

```bash
# Detect changed files
git diff --name-only HEAD~1

# Run affected tests only
jest --findRelatedTests $(git diff --name-only HEAD~1)
```

**Benefits:** 70-90% fewer tests run on typical commits.

---

**4. Resource Management**

- Use workload-based resource provisioning
- Scale runners based on queue depth
- Terminate idle runners
- Use spot instances for cost savings

**Research Finding:** Organizations taking incremental optimization approach show 30% higher success rates.

---

### 2.3 Pipeline Observability

**Key Metrics to Track:**

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Build Time | < 10 minutes | > 20 minutes |
| Test Coverage | > 80% | < 70% |
| Deployment Frequency | Daily | < Weekly |
| Mean Time to Recovery | < 1 hour | > 4 hours |
| Pipeline Failure Rate | < 5% | > 10% |
| Lead Time for Changes | < 1 day | > 1 week |

**Monitoring Dashboard:**
- Real-time build status
- Historical trends
- Failure analysis
- Bottleneck identification

**Alerting:**
- Slack/email on pipeline failures
- Alert on metric threshold violations
- Escalation for critical failures

---

## Section 3: Testing in CI/CD Pipelines

### 3.1 The Test Automation Pyramid

**Structure (recommended distribution):**

```
           E2E Tests (10%)
        Slow, expensive, brittle
        
      Integration Tests (20%)
    Medium speed, moderate cost
    
        Unit Tests (70%)
     Fast, cheap, reliable
```

**Why This Distribution:**
- Faster feedback (unit tests run in seconds)
- Cheaper to maintain
- More reliable (less flaky)
- Scales better with codebase growth

---

### 3.2 Testing Stages in Pipeline

**Stage 1: Every Commit**

**Tests:** Unit tests only  
**Timeout:** Must complete in < 1 minute  
**Purpose:** Immediate feedback on code quality  
**Action on Failure:** Block merge, require fix  

**Requirements:**
- [ ] Run automatically on push
- [ ] Results visible in < 1 minute
- [ ] Zero flaky tests (target: 99.9% stability)

---

**Stage 2: Every Pull Request**

**Tests:** Unit + Integration tests  
**Timeout:** Must complete in < 10 minutes  
**Purpose:** Validate changes before merge  
**Action on Failure:** Block merge, require fix  

**Requirements:**
- [ ] Run automatically on PR creation/update
- [ ] Required status check (cannot merge if failing)
- [ ] Test against main branch to detect conflicts

---

**Stage 3: Every Deployment**

**Tests:** E2E smoke tests  
**Timeout:** Must complete in < 30 minutes  
**Purpose:** Ensure critical paths work  
**Action on Failure:** Block deployment, trigger rollback  

**Requirements:**
- [ ] Run in staging environment
- [ ] Test critical user journeys only
- [ ] Automated rollback on failure

---

**Stage 4: Nightly**

**Tests:** Comprehensive E2E suite  
**Timeout:** Can take hours  
**Purpose:** Deep validation  
**Action on Failure:** Alert team, investigate next day  

**Requirements:**
- [ ] Run full test suite
- [ ] Performance tests
- [ ] Security scans (SAST, DAST)
- [ ] Dependency vulnerability scans

---

### 3.3 Test Quality Standards

**Coverage Requirements:**
- Unit test coverage: Minimum 80%
- Integration test coverage: Minimum 60%
- E2E test coverage: Critical paths only

**Flakiness:**
- Maximum 1% flaky test rate
- Quarantine flaky tests immediately
- Fix or delete within 48 hours

**Test Speed:**
- Unit tests: < 100ms per test
- Integration tests: < 5 seconds per test
- E2E tests: < 2 minutes per test

**Critical Principle:**
"CI/CD pipelines cannot function without continuous testing and automation; without them, they become continuous integration without continuous validation, deploying hope rather than quality."

---

## Verification Checklist

**Before committing to CI/CD pipeline setup:**

### Git Workflow
- [ ] Branching strategy chosen (trunk-based or GitHub Flow)
- [ ] Commit frequency standards defined
- [ ] Merge conflict resolution process established

### Pipeline Architecture
- [ ] Fail fast principle implemented
- [ ] Single path to production enforced
- [ ] All deployment steps automated
- [ ] Stable build policy enforced

### Pipeline Performance
- [ ] Dependency caching configured
- [ ] Parallel execution for independent jobs
- [ ] Incremental testing implemented
- [ ] Resource optimization configured

### Monitoring
- [ ] Key metrics tracked
- [ ] Monitoring dashboard configured
- [ ] Alerting rules established
- [ ] Historical trend analysis enabled

### Testing
- [ ] Test pyramid distribution followed (70/20/10)
- [ ] Test stages configured (commit/PR/deploy/nightly)
- [ ] Coverage requirements met
- [ ] Flaky test management process established

---

---

## Section 4: Deployment Strategies

### 4.1 Blue-Green Deployment

**Definition:**
Two identical environments (Blue and Green) where one serves production traffic while the other is updated.

**How It Works:**
1. Blue environment serves production traffic
2. Deploy new version to Green environment
3. Test Green environment thoroughly
4. Switch traffic from Blue to Green instantly
5. Keep Blue as backup for rollback

**Advantages:**
- [APPROVED] Zero downtime
- [APPROVED] Instant rollback (switch back to Blue)
- [APPROVED] Easy to test new version in production-like environment
- [APPROVED] Perfect for disaster recovery

**Disadvantages:**
- [CAUTION] Requires double infrastructure (expensive)
- [CAUTION] Database migrations complex (must be backward-compatible)
- [CAUTION] All-or-nothing switch (not gradual)

**When to Use:**
- Need zero downtime
- Can afford duplicate infrastructure
- Need instant rollback capability
- Well-tested deployments (low risk)

**Requirements:**
- [ ] Identical infrastructure for both environments
- [ ] Load balancer or DNS for traffic switching
- [ ] Backward-compatible database migrations
- [ ] Automated switch mechanism
- [ ] Rollback procedure tested regularly

---

### 4.2 Canary Deployment

**Definition:**
Gradually roll out new version to subset of users, monitor metrics, then expand or rollback.

**How It Works:**
1. Deploy new version to canary servers (5-10% of capacity)
2. Route small percentage of traffic to canary
3. Monitor metrics (errors, latency, business KPIs)
4. If stable, gradually increase traffic (25% → 50% → 100%)
5. If issues detected, rollback immediately

**Advantages:**
- [APPROVED] Mitigates risk (only small percentage affected)
- [APPROVED] Real-world testing with actual users
- [APPROVED] Gradual rollout enables early issue detection
- [APPROVED] Can rollback at any stage

**Disadvantages:**
- [CAUTION] Complex to implement
- [CAUTION] Requires sophisticated monitoring and metrics
- [CAUTION] Slower than blue-green
- [CAUTION] Session management challenges (sticky sessions needed)

**When to Use:**
- High-risk deployments
- Uncertain about stability
- Want real user feedback before full rollout
- Can tolerate gradual rollout timeline

**Requirements:**
- [ ] Automated traffic splitting capability
- [ ] Comprehensive monitoring and alerting
- [ ] Automated rollback triggers
- [ ] Session affinity (sticky sessions)
- [ ] Clear success/failure criteria

---

### 4.3 Rolling Deployment

**Definition:**
Update instances one-by-one or in batches until all instances run new version.

**How It Works:**
1. Take instance out of load balancer
2. Update instance to new version
3. Run health checks
4. Return instance to load balancer
5. Repeat for next instance

**Advantages:**
- [APPROVED] Resource efficient (no duplicate infrastructure)
- [APPROVED] Continuous availability
- [APPROVED] Gradual rollout

**Disadvantages:**
- [CAUTION] Slow (takes time to update all instances)
- [CAUTION] Rollback complex (must reverse updates instance-by-instance)
- [CAUTION] Mixed versions running simultaneously
- [REJECTED] Not suitable for breaking changes

**When to Use:**
- Resource-constrained environments
- Low-risk deployments
- Backward-compatible changes only
- Can tolerate gradual update process

**Requirements:**
- [ ] Backward-compatible changes only
- [ ] Health check endpoints
- [ ] Load balancer with instance management
- [ ] Automated rollback procedure
- [ ] Monitoring for version compatibility issues

---

### 4.4 Deployment Strategy Selection Matrix

| Strategy | Downtime | Rollback Speed | Infrastructure Cost | Risk Level | Best For |
|----------|----------|----------------|-------------------|-----------|----------|
| **Blue-Green** | Zero | Instant | High (2x) | Low | Production-critical, instant rollback needed |
| **Canary** | Zero | Fast | Medium (1.1-1.2x) | Very Low | High-risk changes, gradual validation |
| **Rolling** | Zero | Slow | Low (1x) | Medium | Resource-constrained, low-risk changes |

---

## Section 5: Environment Management

### 5.1 The Three Environments

**Development (Dev)**

**Purpose:** Create and test new features

**Characteristics:**
- Flexible, frequently changing
- Stability not critical
- Rapid iteration enabled

**Database:**
- Sample/test data only
- [REJECTED] Never use production data
- Can be destructively tested

**Access:**
- All developers
- Automated deployments on commit (optional)

**Infrastructure:**
- Can differ from production
- Optimized for development speed
- Shared resources acceptable

---

**Staging**

**Purpose:** Final validation before production

**Characteristics:**
- **MUST mirror production as closely as possible**
- Stable, controlled changes only
- Production-like workloads for testing

**Database:**
- Anonymized production data OR
- Production-like dataset (realistic volume and complexity)
- [REJECTED] Never actual production data with PII

**Access:**
- QA team
- Developers (for testing and debugging)
- Automated deployments via CI/CD

**Infrastructure:**
- **Must mirror production infrastructure**
- Same software versions as production
- Same network topology
- Can be smaller scale (cost optimization)

---

**Production**

**Purpose:** Live system serving real users

**Characteristics:**
- Stable, changes tightly controlled
- Monitored 24/7
- High availability required

**Database:**
- Real user data
- Fully backed up (automated, tested)
- Encrypted at rest and in transit

**Access:**
- Restricted (admins, on-call engineers only)
- All access logged and audited
- MFA required for all access

**Infrastructure:**
- Production-grade resources
- High availability configuration
- Auto-scaling enabled
- Disaster recovery configured

---

### 5.2 Environment Parity

**Critical Principle:** Staging MUST mirror production.

**Why:**
- Catches environment-specific bugs before production
- Validates deployment procedures
- Reduces "works in staging, fails in production" incidents
- Builds confidence before production deployment

**How to Achieve Parity:**

**Infrastructure as Code:**
- Use Terraform, CloudFormation, or Pulumi
- Same infrastructure code for staging and production
- Different variable values (size, scale) but same topology

**Software Versions:**
- Identical software versions in staging and production
- Same database version
- Same runtime version (Node.js, Python, etc.)

**Configuration Structure:**
- Same configuration structure
- Different values (API keys, database URLs)
- Managed via environment variables

**Network Topology:**
- Same network architecture
- Same security groups/firewall rules
- Same load balancer configuration

---

### 5.3 Environment Best Practices

**1. Separate Databases**

**Critical Rule:** NEVER share databases between environments.

**Why:**
- Prevents production data leaks
- Allows safe testing in dev/staging
- Enables destructive testing
- Isolates failures

**Implementation:**
```
Dev:     dev-database.internal
Staging: staging-database.internal
Prod:    prod-database.internal
```

---

**2. Environment Variables**

**Store environment-specific configuration in variables:**

```bash
# Development
DATABASE_URL=postgresql://localhost:5432/myapp_dev
API_KEY=dev_test_key_12345

# Staging
DATABASE_URL=postgresql://staging-db.internal:5432/myapp
API_KEY=staging_key_67890

# Production
DATABASE_URL=postgresql://prod-db.internal:5432/myapp
API_KEY=prod_key_abcde
```

**Rules:**
- [REJECTED] Never hardcode environment values
- Use secrets manager for staging/production
- Use `.env` files for local development (not committed)
- Document all required environment variables

---

**3. Version Control Everything**

**Track in Git:**
- Infrastructure as Code definitions
- Configuration templates
- Deployment scripts
- Environment setup documentation

**Benefits:**
- Quick rollback capability
- Change history and audit trail
- Reproducible environments

---

**4. Automated Deployments**

**Automate to reduce human error:**

```yaml
# Example: Environment-specific deployments
deploy-dev:
  on: push to main
  environment: development

deploy-staging:
  on: push to main
  environment: staging
  requires: [test-suite]

deploy-production:
  on: manual trigger
  environment: production
  requires: [deploy-staging, approval]
```

---

## Section 6: Versioning and Artifact Management

### 6.1 Semantic Versioning (SemVer)

**Format:** `MAJOR.MINOR.PATCH` (example: `2.1.5`)

**Version Increment Rules:**

**MAJOR:** Breaking changes (incompatible API changes)
```
1.5.3 → 2.0.0
- Removed deprecated endpoints
- Changed response format
- Renamed database tables
```

**MINOR:** New features (backward-compatible)
```
2.0.0 → 2.1.0
- Added new API endpoint
- Added optional parameter
- New feature without breaking existing functionality
```

**PATCH:** Bug fixes (backward-compatible)
```
2.1.0 → 2.1.1
- Fixed calculation error
- Fixed security vulnerability
- Performance improvement
```

---

**Pre-release Versions:**
```
2.1.0-alpha.1  (early testing)
2.1.0-beta.2   (feature complete, testing)
2.1.0-rc.1     (release candidate)
2.1.0          (stable release)
```

**Build Metadata:**
```
v2.1.0+build.456
v2.1.0+sha.a7f3c2d
```

Links artifact to source code, traceable to Git commit.

---

### 6.2 Artifact Immutability

**Critical Principle:** Once an artifact version is created, it NEVER changes.

**Why:**
- Ensures consistency across environments
- Enables reliable rollbacks
- Prevents "works in staging, breaks in production"
- Provides audit trail

**Correct Workflow:**
```
1. Build artifact v2.1.0 from commit abc123
2. Deploy v2.1.0 to staging
3. Test v2.1.0 in staging
4. Deploy SAME v2.1.0 artifact to production
```

**Incorrect Workflow:**
```
[REJECTED]
1. Build artifact v2.1.0 from commit abc123
2. Deploy v2.1.0 to staging
3. Rebuild v2.1.0 from commit abc123
4. Deploy to production
   
Problem: Different binary! Not truly same version!
```

---

### 6.3 Artifact Storage Best Practices

**1. Clear Versioning**
- Use Semantic Versioning
- Include build number: `v2.1.0-build.456`
- Tag with Git commit SHA: `v2.1.0+sha.a7f3c2d`

**2. Access Controls**

| Role | Upload Artifacts | Download Artifacts | Delete Artifacts |
|------|-----------------|-------------------|------------------|
| Developer | Yes | Yes | No |
| QA | No | Yes | No |
| CI/CD System | Yes | Yes | No |
| Admin | Yes | Yes | Yes |

**3. Retention Policies**

```
Production versions: Keep indefinitely
Staging versions: Keep 30-90 days
Development versions: Keep 7 days
Pre-release versions: Keep until stable release
```

**4. Automation**
- Automate artifact creation in CI/CD
- Automate storage and tagging
- Automate cleanup based on retention policy

---

---

## Section 7: Rollback Strategies

### 7.1 Automated Rollback Triggers

**When to Trigger Rollback:**

**1. Fault Rate Spike**
```
Trigger rollback if:
- Error rate > 1% (baseline: 0.1%)
- 5xx errors increase by 200%
- Critical endpoint failures
```

**2. Performance Degradation**
```
Trigger rollback if:
- P95 latency > 2x baseline
- P99 latency > 3x baseline
- Request timeout rate > 5%
```

**3. Resource Exhaustion**
```
Trigger rollback if:
- CPU usage > 90% sustained for 5 minutes
- Memory usage > 90% sustained for 5 minutes
- Disk usage approaching limit
```

**4. Business Metrics Failure**
```
Trigger rollback if:
- Conversion rate drops > 10%
- Payment failures increase > 5%
- User signups drop > 15%
```

**Waiting Period:**
- Monitor system for 15-30 minutes after deployment
- Some issues only appear under sustained load
- Do not declare success immediately

---

### 7.2 Rollback Methods

**1. Redeploy Last Good Version (RECOMMENDED)**

**Most Common Approach:**
```
1. Identify last successful deployment version
2. Deploy that exact artifact to production
3. Use same deployment strategy (rolling, blue-green, canary)
4. Verify system stability
```

**Advantages:**
- [APPROVED] Known good state
- [APPROVED] Uses tested deployment process
- [APPROVED] Traceable and auditable

**Requirements:**
- [ ] Artifact retention policy includes production versions
- [ ] Deployment automation supports version selection
- [ ] Rollback tested regularly (not just theory)

---

**2. Feature Flags (FASTEST)**

**Toggle off new feature without redeployment:**

```
// Feature flag check
if (featureFlags.isEnabled('new-checkout-flow', userId)) {
  return newCheckoutFlow()
} else {
  return oldCheckoutFlow()
}
```

**Advantages:**
- [APPROVED] Instant rollback (no deployment)
- [APPROVED] Granular control (per user, per region)
- [APPROVED] Can toggle multiple times

**Disadvantages:**
- [CAUTION] Requires feature flag infrastructure
- [CAUTION] Code complexity (two code paths)
- [CAUTION] Must clean up old code eventually

---

**3. Database Rollback (HIGH RISK)**

**Only if schema changed:**

[REJECTED] Restore database to previous state

**Why NOT Recommended:**
- Data loss (transactions between deploy and rollback)
- Extremely risky
- Complex with replicas
- Time-consuming

**Alternative:**
- Use forward-compatible migrations
- Never remove columns (mark deprecated instead)
- Add columns as nullable initially
- Prefer code fixes over database rollback

---

### 7.3 Rollback Decision Matrix

**Option 1: Continue and Retry**
- **When:** Transient error (network timeout, temporary resource issue)
- **Outcome:** Leaves system in known state
- **Risk:** Low

**Option 2: Rollback**
- **When:** Code problem detected, cannot proceed safely
- **Outcome:** Leaves system in known state
- **Risk:** Low
- **RECOMMENDED**

**Option 3: Skip Failed Step**
- **When:** Step is non-critical
- **Outcome:** Requires manual intervention to restore expected state
- **Risk:** High
- [REJECTED] Avoid unless absolutely necessary

**Option 4: Cancel Without Rollback**
- **When:** Emergency stop
- **Outcome:** System in unknown state, requires manual intervention
- **Risk:** Very High
- [REJECTED] Last resort only

**Recommended:** Use Options 1 and 2 only (leave system in known state).

---

### 7.4 Proactive Rollback

**Scenario:** Production has issue, staging also deployed same version.

**Action:**
1. Rollback production (customer impact)
2. **Proactively rollback staging too** (even if no issues yet)

**Why:**
- Prevents cascading failures
- Reduces risk of issues spreading
- Maintains environment consistency

---

## Section 8: GitHub Actions Security

### 8.1 Secrets Management

**Problem:** GitHub Actions secrets accessible to ALL workflows and branches. Bad actor can create workflow to exfiltrate secrets.

**Solution: Environment Secrets with Mandatory Reviews**

```yaml
jobs:
  deploy:
    environment: production  # Requires approval
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        env:
          AWS_ACCESS_KEY: ${{ secrets.AWS_ACCESS_KEY }}
```

**Environment Protection Rules:**
- Required reviewers (minimum 1, recommended 2)
- Wait timer (optional delay before deployment)
- Deployment branches (restrict to main/release only)

**Requirements:**
- [ ] Production secrets ONLY in environment secrets
- [ ] Mandatory approval for production environment
- [ ] Authorized reviewers defined
- [ ] Deployment branches restricted

---

### 8.2 Supply Chain Security

**Problem:** Third-party actions can be compromised or contain malicious code.

**Solution 1: Pin to SHA, Not Tags**

```yaml
# [REJECTED] BAD (tags can be changed by attacker)
- uses: actions/checkout@v3

# [APPROVED] GOOD (SHA is immutable)
- uses: actions/checkout@a81bbbf8298c0fa03ea29cdc473d45769f953675
```

**Solution 2: Review Actions Before Use**

**Before using any third-party action:**
- [ ] Check maintainer reputation
- [ ] Verify maintenance activity (recent commits)
- [ ] Review source code
- [ ] Check number of downloads/stars
- [ ] Search for known vulnerabilities

**Solution 3: Fork and Self-Host Critical Actions**

For critical infrastructure:
- Fork action to your organization
- Review code thoroughly
- Pin to your fork's SHA
- Control updates yourself

---

### 8.3 Least Privilege Permissions

**GITHUB_TOKEN Permissions:**

```yaml
# [REJECTED] Default (too permissive)
# No permissions block = full access

# [APPROVED] Explicit minimal permissions
permissions:
  contents: read           # Read repository
  pull-requests: write     # Comment on PRs
  # Don't grant unnecessary permissions
```

**Common Permission Scopes:**
- `contents: read/write` - Repository content
- `pull-requests: read/write` - PRs and comments
- `issues: read/write` - Issues
- `packages: read/write` - GitHub Packages
- `deployments: write` - Deployments

**Self-Hosted Runners:**
- [CAUTION] Do NOT use for public repositories
- Isolate from internal network
- Regularly update and patch
- Monitor for suspicious activity

---

### 8.4 Injection Attack Prevention

**Problem:** Attacker injects malicious code via PR that executes in workflow.

**Vulnerable Pattern:**

```yaml
# [REJECTED] DANGEROUS
name: Comment on PR
on: pull_request
jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - run: echo "PR title: ${{ github.event.pull_request.title }}"
        # Attacker sets title to: "; malicious command; echo "
```

**Safe Pattern:**

```yaml
# [APPROVED] SAFE
name: Comment on PR
on: pull_request
jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - name: Set PR title
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: echo "PR title: $PR_TITLE"
```

**Security Rules:**
- [REJECTED] Never reference untrusted inputs directly in `run:`
- [APPROVED] Always use intermediate environment variables
- [REJECTED] Never use `pull_request_target` with untrusted code checkout
- [APPROVED] Validate all inputs before use

---

### 8.5 Runtime Monitoring

**Implement Security Monitoring:**

```yaml
# Example: StepSecurity harden-runner
- uses: step-security/harden-runner@63c24ba6bd7ba022e95695ff85de572c04a18142
  with:
    egress-policy: audit  # Monitor network calls
    allowed-endpoints: >
      github.com:443
      api.github.com:443
```

**Monitor For:**
- Unauthorized network calls
- File modifications outside designated directories
- Unexpected process spawning
- Unusual resource consumption

---

## Section 9: CI/CD Anti-Patterns to Avoid

### 9.1 Overcomplicated Pipelines

**Problem:**
- Too many stages
- Complex configurations
- Hard to understand and maintain
- New team members take weeks to understand

**Symptoms:**
- Pipeline file > 500 lines
- More than 10 stages
- Nested conditionals and logic
- No documentation

**Solutions:**
- [APPROVED] Modularize: Separate into reusable templates
- [APPROVED] Visual tools: Use pipeline editors/diagrams
- [APPROVED] Regular refactoring: Remove unnecessary complexity
- [APPROVED] Documentation: Explain each stage

**Target:**
- Pipeline understandable in < 30 minutes
- New developer can modify confidently in 1 day

---

### 9.2 No Local Testing for Developers

**Problem:**
- Developers cannot run application locally
- Must push to CI/CD to test
- Slow feedback loop (minutes instead of seconds)
- Pipeline becomes development environment

**Why This Happens:**
- Complex dependencies
- Environment-specific configuration
- Infrastructure requirements

**Solutions:**
- [APPROVED] Docker Compose for local environments
- [APPROVED] Setup scripts for development environment
- [APPROVED] Mock external dependencies
- [APPROVED] Document local setup process

**Requirement:**
Every developer MUST be able to:
- [ ] Run application locally
- [ ] Run tests locally
- [ ] Verify changes before pushing

---

### 9.3 Using CI/CD Parameters Instead of Git

**Problem:**
- Configuration stored in CI/CD system, not Git
- Cannot reproduce deployments
- Violates GitOps principles
- No audit trail for configuration changes

**Bad Example:**
```
# CI/CD system has parameter: IMAGE_TAG
# Developer manually enters tag during deployment
# No record of what was deployed when
```

**Good Example:**
```
# Git repository has config/production.yaml
image_tag: v2.1.0

# CI/CD reads from Git
# All changes tracked in version control
```

**Principle:**
- [APPROVED] Git is single source of truth
- [REJECTED] CI/CD parameters for configuration
- [APPROVED] Environment variables for secrets only

---

### 9.4 Not Understanding Tools Before Adopting

**Problem:**
- Adopting tools without understanding fundamentals
- Misusing features
- Creating fragile systems

**Examples:**
- [REJECTED] Using Argo CD without understanding Kustomize
- [REJECTED] Using Helm without understanding Helm hierarchy
- [REJECTED] Using Kubernetes without understanding containers

**Solution:**
- [APPROVED] Learn tools independently first
- [APPROVED] Understand fundamentals
- [APPROVED] Read documentation thoroughly
- [APPROVED] Start with simple use cases
- [APPROVED] Then integrate into CI/CD

---

### 9.5 Abusing Fields for Unintended Purposes

**Problem:**
- Using tool features for purposes they weren't designed for
- Hacky workarounds instead of proper solutions

**Examples:**
- Using version field for environment promotion
- Using description field to store configuration
- Using tags for orchestration logic

**Solution:**
- [APPROVED] Use tools as designed
- [APPROVED] Follow best practices
- [APPROVED] Read documentation
- [APPROVED] Ask community if unsure

---

## Complete CI/CD Verification Checklist

**Before committing to CI/CD setup, verify ALL of these:**

### Git Workflow
- [ ] Branching strategy chosen and documented (trunk-based or GitHub Flow)
- [ ] Commit frequency standards defined (minimum once per day for trunk-based)
- [ ] Conventional Commits format enforced
- [ ] Merge conflict resolution process established
- [ ] Broken build policy enforced (fix within 10 minutes or revert)

### Pipeline Architecture
- [ ] Fail fast principle implemented (unit → integration → e2e)
- [ ] Single path to production enforced (no manual deployments)
- [ ] All deployment steps automated
- [ ] Stable build policy enforced (main always deployable)
- [ ] Manual steps eliminated (except compliance-required approvals)

### Pipeline Performance
- [ ] Dependency caching configured (npm, pip, cargo, etc.)
- [ ] Parallel execution for independent jobs
- [ ] Incremental testing implemented
- [ ] Resource optimization configured
- [ ] Pipeline completes in < 10 minutes (unit tests < 1 minute)

### Monitoring and Observability
- [ ] Key metrics tracked (build time, failure rate, deployment frequency)
- [ ] Monitoring dashboard configured
- [ ] Alerting rules established (Slack, email)
- [ ] Historical trend analysis enabled
- [ ] Metrics reviewed regularly

### Testing
- [ ] Test pyramid distribution followed (70% unit, 20% integration, 10% e2e)
- [ ] Test stages configured (commit/PR/deploy/nightly)
- [ ] Coverage requirements met (80% minimum)
- [ ] Flaky test management process established (< 1% flaky rate)
- [ ] Test execution time limits enforced

### Deployment Strategy
- [ ] Deployment strategy selected (blue-green, canary, or rolling)
- [ ] Zero downtime deployments implemented
- [ ] Health check endpoints configured
- [ ] Rollback procedure automated and tested
- [ ] Database migrations backward-compatible

### Environment Management
- [ ] Three environments configured (dev, staging, production)
- [ ] Staging mirrors production infrastructure
- [ ] Separate databases per environment (never shared)
- [ ] Environment variables used for configuration
- [ ] Infrastructure as Code implemented (Terraform, CloudFormation)

### Versioning and Artifacts
- [ ] Semantic Versioning enforced (MAJOR.MINOR.PATCH)
- [ ] Artifact immutability enforced (same binary staging → production)
- [ ] Build numbers included in versions
- [ ] Git commit SHA tagged in artifacts
- [ ] Retention policies defined and automated

### Rollback Procedures
- [ ] Automated rollback triggers configured
- [ ] Rollback decision matrix documented
- [ ] Last good version easily identifiable
- [ ] Rollback tested regularly (not just theory)
- [ ] Rollback completes in < 5 minutes

### Security (GitHub Actions)
- [ ] Environment secrets with mandatory reviews for production
- [ ] Actions pinned to SHA (not tags)
- [ ] Least privilege permissions (explicit GITHUB_TOKEN scopes)
- [ ] No injection vulnerabilities (inputs in environment variables)
- [ ] Runtime monitoring configured
- [ ] Self-hosted runners isolated (if used)

### Anti-Patterns Avoided
- [ ] Pipeline complexity managed (< 500 lines, < 10 stages)
- [ ] Local testing enabled for all developers
- [ ] All configuration in Git (not CI/CD parameters)
- [ ] Tools understood before adoption
- [ ] No field abuse or workarounds

**If ANY checkbox fails, address before proceeding to production.**

---

## When to Read This Canon

**ONLY read this CI/CD canon when performing CI/CD operations:**

- Setting up new CI/CD pipeline
- Configuring deployment strategies
- Establishing environment structure
- Implementing rollback procedures
- Reviewing pipeline security
- Troubleshooting CI/CD issues
- Optimizing pipeline performance

**Do NOT read for:**
- Regular feature development
- Bug fixes
- Code reviews (unless CI/CD-related)

This keeps the canon reference brief and targeted.

---

## Version

CI/CD Canon Version: 1.0 - Complete (December 29, 2025)  
Based on industry research and best practices for continuous integration and continuous deployment.

Covers 9 comprehensive categories:
1. Git Workflow and Branching Strategies
2. Pipeline Architecture and Best Practices
3. Testing in CI/CD Pipelines
4. Deployment Strategies
5. Environment Management
6. Versioning and Artifact Management
7. Rollback Strategies
8. GitHub Actions Security
9. CI/CD Anti-Patterns

