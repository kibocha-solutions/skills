# Deployment Standards Canon: Comprehensive Production Deployment Standards

This document provides comprehensive, non-negotiable deployment standards for all projects following the Vibe Code Canon framework.

**Authority:** These standards have ABSOLUTE AUTHORITY and MUST be followed for production deployments. All examples provided are for contextual purposes ONLY and should not be assumed to be part of the deployment standards or project requirements.

---

## Section 1: Infrastructure as Code (IaC)

### 1.1 Core Philosophy

**Definition:**
Managing infrastructure through code instead of manual processes or interactive configuration tools.

**Benefits:**
- [APPROVED] Version-controlled infrastructure (track all changes)
- [APPROVED] Reproducible environments
- [APPROVED] Automated provisioning
- [APPROVED] Eliminates configuration drift
- [APPROVED] Documentation through code

---

### 1.2 Terraform: Provisioning Infrastructure

**What Terraform Does:**
- Provisions infrastructure (networks, VMs, databases, cloud services)
- Declarative: Define desired state, Terraform figures out how to get there
- Plan-then-apply model: Preview changes before applying
- Encourages immutable infrastructure: Create new resources, terminate old ones (reduces drift)

**Key Features:**

**1. Declarative Configuration**

```hcl
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  
  tags = {
    Name        = "WebServer"
    Environment = "Production"
  }
}
```

---

**2. State Management**

**Terraform tracks resources in state file. Critical for knowing what's deployed.**

[APPROVED] **Best Practice:** Remote state storage

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"  # Prevent concurrent modifications
  }
}
```

**Requirements:**
- [ ] Use remote state storage (S3, Azure Blob, GCS)
- [ ] Enable state locking
- [ ] Encrypt state files
- [ ] Never commit state files to Git

---

**3. Preview Changes Before Applying**

```bash
# See what will change BEFORE applying
terraform plan

# Only apply if plan looks correct
terraform apply
```

**Prevents accidental resource destruction or downtime.**

---

### 1.3 Ansible: Configuration Management

**What Ansible Does:**
- Configures provisioned infrastructure
- Installs software
- Updates configuration files
- Deploys applications

**After Terraform provisions servers, Ansible configures them.**

**Key Features:**

**1. Agentless**
- Uses SSH (no agent installation required)
- Simple to set up

**2. Playbooks (YAML)**

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: Copy application config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Reload nginx
  
  handlers:
    - name: Reload nginx
      service:
        name: nginx
        state: reloaded
```

---

### 1.4 Terraform + Ansible Workflow

**Typical Pipeline:**

```
1. Terraform provisions infrastructure
   → Creates VMs, networks, load balancers
   → Outputs IP addresses

2. Ansible configures infrastructure
   → Uses Terraform outputs
   → Installs software, configures services
   → Deploys application

3. CI/CD automation
   → terraform plan → review → terraform apply
   → ansible-playbook site.yml
```

---

### 1.5 IaC Best Practices

**1. Modularize Infrastructure Code**

**DRY Principle: Reuse common configurations**

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
}

# environments/production/main.tf
module "vpc" {
  source   = "../../modules/vpc"
  vpc_cidr = "10.0.0.0/16"
}
```

**Benefits:**
- [APPROVED] Reuse across projects
- [APPROVED] Easier maintenance
- [APPROVED] Consistent patterns

---

**2. Version Control Everything**

**Requirements:**
- [ ] All infrastructure code in Git
- [ ] Track changes
- [ ] Code reviews for infrastructure changes
- [ ] Rollback capability
- [ ] Never make manual changes outside code

[REJECTED] Manual changes create drift from code and make infrastructure non-reproducible.

---

**3. Use Infrastructure Testing**

**Test infrastructure like application code:**

**Tools:**
- Terratest (Terraform testing)
- Molecule (Ansible testing)

**Benefits:**
- [APPROVED] Catch errors before deployment
- [APPROVED] Ensure configurations meet requirements
- [APPROVED] Reduce deployment risks

---

**4. Pipeline Integration**

**Automate execution in CI/CD:**

```yaml
# GitLab CI example
stages:
  - validate
  - plan
  - apply
  - configure

terraform_validate:
  stage: validate
  script:
    - terraform init
    - terraform validate
    - terraform fmt -check

terraform_plan:
  stage: plan
  script:
    - terraform plan -out=plan.tfplan
  artifacts:
    paths:
      - plan.tfplan

terraform_apply:
  stage: apply
  script:
    - terraform apply plan.tfplan
  when: manual  # Require approval
  only:
    - main

ansible_configure:
  stage: configure
  script:
    - ansible-playbook -i inventory site.yml
  dependencies:
    - terraform_apply
```

**Ensures consistent, repeatable deployments.**

---

## Section 2: Containerization & Orchestration

### 2.1 Docker Best Practices

**1. Multi-Stage Builds**

**Optimize image layers and reduce final image size:**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Benefits:**
- [APPROVED] Smaller production images (no build tools)
- [APPROVED] Faster deployments
- [APPROVED] Reduced attack surface

---

**2. Keep Dependencies Up-to-Date**

**Regularly update base images and packages:**
- Security patches
- Bug fixes
- Performance improvements

**Use automated tools:**
- Dependabot
- Renovate

---

**3. Avoid Unnecessary Layers**

```dockerfile
# [REJECTED] BAD: Creates multiple layers
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2

# [APPROVED] GOOD: Single layer
RUN apt-get update && \
    apt-get install -y \
      package1 \
      package2 && \
    rm -rf /var/lib/apt/lists/*
```

---

### 2.2 Kubernetes Production Best Practices

**1. Resource Requests and Limits**

**Specify CPU/memory for every deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: web
        image: myapp:1.0.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Why Critical:**
- **Requests:** Kubernetes scheduler uses this to place pods
- **Limits:** Prevents single pod consuming all node resources
- **Optimal cluster utilization**

**Requirements:**
- [ ] All deployments have resource requests
- [ ] All deployments have resource limits
- [ ] Limits based on actual usage patterns

---

**2. Secrets Management**

[REJECTED] Never hardcode sensitive data

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQxMjM=

---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: password
```

[APPROVED] **Production:** Use external secrets management:
- AWS Secrets Manager
- Google Secret Manager
- HashiCorp Vault

---

**3. GitOps Workflows**

**Declarative infrastructure management:**

**How It Works:**
- All Kubernetes manifests stored in Git repository
- GitOps operators (Argo CD, Flux) continuously poll repository
- Automatically apply changes to cluster
- Reduces configuration drift

**Repository Structure:**

```
Repository Structure:
environments/
├── dev/
│   ├── deployment.yaml
│   └── service.yaml
├── staging/
│   ├── deployment.yaml
│   └── service.yaml
└── production/
    ├── deployment.yaml
    └── service.yaml
```

**Benefits:**
- [APPROVED] Single source of truth (Git)
- [APPROVED] Audit trail (all changes tracked)
- [APPROVED] Easy rollback (Git revert)
- [APPROVED] Declarative (desired state, not imperative steps)

---

**4. Environment-Specific Deployments**

**Manage configurations across dev/staging/production:**

**Promotion Workflow:**
```
1. Developer commits to feature branch
2. CI runs tests
3. Merge to develop → Auto-deploy to dev environment
4. Promote to staging branch → Auto-deploy to staging
5. Manual approval → Promote to main → Deploy to production
```

---

**5. Security Automation (Open Policy Agent)**

**OPA for policy enforcement:**

**What OPA Does:**
- Declarative security policies
- Admission controller (validates resources before creation)
- Prevents non-compliant resources

**Example Policy:**

```rego
# All containers must not run as root
deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot
  msg = "Containers must not run as root"
}

# All containers must have resource limits
deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.resources.limits
  msg = sprintf("Container %s missing resource limits", [container.name])
}
```

**Ensures consistent security posture without manual review.**

---

## Section 3: Production Readiness Checklists

### 3.1 Monitoring & Observability

| Check | Done |
|-------|------|
| Metrics collection configured (CPU, memory, latency) | ☐ |
| Logging infrastructure in place | ☐ |
| Distributed tracing configured (for microservices) | ☐ |
| Dashboards created for key metrics | ☐ |
| Alerts configured for critical thresholds | ☐ |
| Alert routing configured (PagerDuty, Slack) | ☐ |
| Runbooks linked from dashboards/alerts | ☐ |

---

### 3.2 Incident Response

| Check | Done |
|-------|------|
| On-call team aware of deployment | ☐ |
| Runbook exists for common failure modes | ☐ |
| Escalation paths documented | ☐ |
| Rollback steps defined and tested | ☐ |
| Post-mortem template ready | ☐ |
| Communication plan established | ☐ |

**Pressure Test:** "What happens when this gets popular?" Often reveals design assumptions that don't hold.

---

### 3.3 Security & Compliance

| Check | Done |
|-------|------|
| Authentication/authorization implemented | ☐ |
| Secrets stored securely (not in code) | ☐ |
| HTTPS enforced | ☐ |
| Security scanning completed (SAST, DAST) | ☐ |
| Compliance requirements met (GDPR, PCI-DSS, etc.) | ☐ |
| Dependency vulnerabilities checked | ☐ |
| Access controls reviewed | ☐ |
| Security canon requirements met | ☐ |

---

### 3.4 Performance & Scalability

| Check | Done |
|-------|------|
| Load testing performed | ☐ |
| Caching implemented where appropriate | ☐ |
| Rate limiting configured | ☐ |
| Resource usage within acceptable limits | ☐ |
| Graceful degradation for downstream failures | ☐ |
| Auto-scaling configured (if applicable) | ☐ |
| Database indexes optimized | ☐ |
| Performance baselines established | ☐ |

---

### 3.5 Testing

| Check | Done |
|-------|------|
| Unit tests passing (minimum 85% coverage) | ☐ |
| Integration tests passing | ☐ |
| E2E smoke tests passing | ☐ |
| Performance tests baseline established | ☐ |
| Security tests completed | ☐ |
| Infrastructure tests passing (Terratest/Molecule) | ☐ |

---

### 3.6 Documentation

| Check | Done |
|-------|------|
| Architecture diagrams up-to-date | ☐ |
| API documentation current | ☐ |
| Deployment procedures documented | ☐ |
| Troubleshooting guide available | ☐ |
| Configuration parameters documented | ☐ |
| Change log maintained | ☐ |
| Runbooks created | ☐ |

---

### 3.7 Deployment Process

| Check | Done |
|-------|------|
| Deployment script tested in staging | ☐ |
| Rollback procedure tested | ☐ |
| Database migrations reviewed | ☐ |
| Feature flags configured (if applicable) | ☐ |
| Deployment window communicated | ☐ |
| Stakeholders notified | ☐ |
| Health checks configured | ☐ |

---

## Verification Checklist - Part 1

**Before proceeding, verify:**

### Infrastructure as Code
- [ ] Terraform/Ansible used for infrastructure
- [ ] Remote state storage configured
- [ ] State locking enabled
- [ ] Infrastructure code modularized
- [ ] All infrastructure in version control
- [ ] Infrastructure testing implemented
- [ ] CI/CD pipeline for infrastructure

### Containerization
- [ ] Multi-stage Docker builds used
- [ ] Dependencies up-to-date
- [ ] Minimal image layers
- [ ] Resource requests/limits configured
- [ ] Secrets management implemented
- [ ] GitOps workflow established
- [ ] Security policies enforced (OPA)

### Production Readiness
- [ ] Monitoring configured
- [ ] Logging infrastructure ready
- [ ] Alerts configured
- [ ] Runbooks created
- [ ] Security requirements met
- [ ] Load testing completed
- [ ] Documentation current

---

## Section 4: Observability (Logs, Metrics, Traces)

### 4.1 The Three Pillars

**Definition:**
Observability is the ability to measure a system's internal state based on the data it produces.

**Three data types provide different insights:**

---

### 4.2 Logs

**What They Are:**
Historical records of system events and errors.

**Formats:**
- Plain text
- Binary
- Structured (JSON) with metadata

**Purpose:**
- [APPROVED] Explain WHY something happened
- [APPROVED] Detailed debugging information
- [APPROVED] Audit trail

**Example:**

```json
{
  "timestamp": "2025-12-30T00:15:32Z",
  "level": "ERROR",
  "service": "payment-service",
  "message": "Payment processing failed",
  "error": "Connection timeout to payment gateway",
  "user_id": "12345",
  "transaction_id": "txn_abc123",
  "duration_ms": 30000
}
```

**When to Use:**
- Debugging specific issues
- Understanding what happened inside a function
- Compliance/audit requirements

**Challenges:**
- [CAUTION] Data privacy: Can contain sensitive data. Mask fields at source
- [CAUTION] High volume
- [CAUTION] Storage costs

---

### 4.3 Metrics

**What They Are:**
Numerical measurements of system performance and behavior.

**Examples:**
- CPU usage
- Memory utilization
- Response time (p50, p95, p99)
- Request rate
- Error rate

**Purpose:**
- [APPROVED] Point to trouble
- [APPROVED] Compress activity into trend lines
- [APPROVED] Alert when thresholds exceeded
- [APPROVED] Performance monitoring

**Example:**

```
http_requests_total{method="POST", status="200"} 15234
http_request_duration_seconds{quantile="0.95"} 0.234
database_connections_active 42
memory_usage_bytes 2147483648
```

**When to Use:**
- Real-time monitoring
- Alerting
- Capacity planning
- SLO tracking

**Best Practice:**
- Tie alerts to Service Level Objectives (SLOs)
- Only alert on customer-facing issues
- Avoid alert fatigue

---

### 4.4 Traces

**What They Are:**
Representations of individual requests or transactions flowing through system.

**Purpose:**
- [APPROVED] Show WHERE trouble starts
- [APPROVED] Connect spans to prove cause and effect
- [APPROVED] Identify bottlenecks
- [APPROVED] Understand dependencies

**Example (Distributed Trace):**

```
Request ID: abc123
│
├─ API Gateway (15ms)
│  │
│  ├─ Auth Service (8ms)
│  │
│  └─ Order Service (120ms)
│     │
│     ├─ Database Query (85ms) ← Bottleneck identified
│     │
│     └─ Payment Service (30ms)
│        │
│        └─ External Payment Gateway (25ms)
```

**When to Use:**
- Debugging microservices
- Finding performance bottlenecks
- Understanding request flow
- Root cause analysis

**Implementation Requirement:**
- [ ] Propagate request IDs across services
- [ ] Use correlation IDs in logs
- [ ] Instrument code with tracing library (OpenTelemetry)

---

### 4.5 How They Work Together

**Typical Investigation Flow:**

```
1. METRICS detect problem
   → "Error rate spiked to 5%"

2. TRACES show where it starts
   → "Errors originate from payment service → database query"

3. LOGS explain why
   → "Database connection pool exhausted: max connections 100, current 100"

Solution: Increase connection pool size
```

[APPROVED] **Best Practice:** Use metrics for trends, traces for context, logs for detail.

---

### 4.6 Observability Best Practices

**1. Manage Cardinality**
- [CAUTION] Too many unique label combinations explode storage
- [APPROVED] Keep metric labels to minimum necessary
- [APPROVED] Use logs for high-cardinality data (user IDs, transaction IDs)

**2. Maintain Ownership**
- [APPROVED] Every dashboard, query, and alert needs a named maintainer
- [APPROVED] Store mappings in code
- [APPROVED] Updates follow code review process

**3. Structured Logging**
- [APPROVED] Use JSON format
- [APPROVED] Include context (request ID, user ID, service name)
- [APPROVED] Consistent field names across services

**4. Set Retention Policies**
- Logs: 30-90 days (compliance may require longer)
- Metrics: 1 year (aggregated data longer)
- Traces: 7-30 days (high volume)

---

## Section 5: Disaster Recovery

### 5.1 Recovery Time Objective (RTO)

**Definition:**
Maximum acceptable time to restore service after disruption.

**Example:**
```
RTO = 4 hours
Means: Service must be back online within 4 hours of outage
```

**Low RTO = Fast recovery = Minimal service disruption**

**Factors Affecting RTO:**
- Backup/restore speed
- Network bandwidth
- Automation level
- Team training and preparedness
- Infrastructure complexity

---

### 5.2 Recovery Point Objective (RPO)

**Definition:**
Maximum acceptable data loss measured in time.

**Example:**
```
RPO = 1 hour
Means: Can tolerate up to 1 hour of data loss
```

**Low RPO = Frequent backups = Minimal data loss**

**Factors Affecting RPO:**
- Backup frequency
- Database replication lag
- Storage performance

---

### 5.3 Business Impact

**Both RTO and RPO must be defined by business considering:**
- Business impact
- Technical constraints (backup capabilities, production limits)
- Cost implications

**Trade-offs:**

```
Lower RTO/RPO = Higher Cost

Low RTO requires:
- Hot standby systems
- Real-time replication
- Automated failover

Low RPO requires:
- Frequent/continuous backups
- High-performance storage
- Large storage capacity
```

---

### 5.4 Setting Appropriate RTO/RPO

**Process:**

**1. Identify Mission-Critical Applications**
- Which systems are essential?
- Revenue-generating systems
- Customer-facing systems
- Compliance-critical systems

**2. Risk Assessment**
- What's acceptable downtime?
- What's acceptable data loss?
- Consider business impact AND technical capabilities

**3. Calculate Costs**
- Infrastructure requirements
- Storage costs
- Operational overhead

**Example Matrix:**

| System Type | RTO | RPO | Strategy |
|-------------|-----|-----|----------|
| E-commerce checkout | 15 minutes | 5 minutes | Hot standby, real-time replication |
| Analytics dashboard | 4 hours | 1 hour | Warm standby, hourly backups |
| Internal wiki | 24 hours | 24 hours | Cold backup, daily backups |

---

### 5.5 Disaster Recovery Strategies

**1. Frequent Backups and Snapshots**

**The more often you back up, the less data you lose.**

**Types:**
- **Full backups:** Complete system copy
- **Incremental backups:** Only changes since last backup
- **Continuous backups:** Real-time replication

[APPROVED] **Best Practice:** 3-2-1 Rule

```
3 copies of data
2 different media types
1 copy offsite
```

**Immutable Backups:**
- [APPROVED] Cannot be altered or deleted (ransomware protection)
- [APPROVED] Critical for data integrity

---

**2. Automated Recovery Tasks**

**Automate everything possible:**
- [APPROVED] Backup scheduling with retention policies
- [APPROVED] Infrastructure-as-Code for system rebuild
- [APPROVED] Recovery scripts for automated failover

**Benefits:**
- Drastically reduces RTO
- Eliminates human error
- Consistent recovery process

---

**3. Offsite and Distributed Backups**

**Why Offsite:**
- Protects against site-specific disasters (fire, flood)
- Protects against regional outages

**Options:**
- Remote data center
- Cloud storage (S3, Google Cloud Storage, Azure Blob)
- Geographic distribution across regions

[APPROVED] **Air Gap Practices:**

**Critical:** Don't store backup media in same location as primary data.

**Example:** Storing backup tapes in same data center defeats purpose if fire destroys entire facility.

---

**4. Hot/Warm/Cold Standby**

**Hot Standby:**
- Parallel system running in real-time
- Immediate failover (RTO: minutes)
- Real-time replication (RPO: seconds)
- **Most expensive**

**Warm Standby:**
- System partially running
- Data synced periodically
- Faster activation than cold (RTO: hours)
- Moderate cost

**Cold Standby:**
- Offline backup
- Must restore from backups
- Slowest recovery (RTO: days)
- **Least expensive**

---

**5. Test Recovery Procedures**

**Regular testing is critical:**
- [ ] Verify backups are restorable
- [ ] Practice recovery procedures
- [ ] Train team
- [ ] Identify gaps in process

**Frequency:**
- Critical systems: Quarterly
- Important systems: Semi-annually
- All systems: Annually minimum

**Document results and update procedures.**

---

### 5.6 Disaster Recovery Plan Components

**Required Components:**

1. **Backup schedule** aligned with RPO
2. **Automated failover strategies** to support RTO
3. **Air gap practices** for critical backups
4. **Regular testing** to validate plan
5. **Communication plan** (who to notify, escalation paths)
6. **Recovery procedures** (step-by-step runbooks)

---

## Section 6: Scaling Strategies

### 6.1 Vertical Scaling (Scale Up)

**Definition:**
Adding more resources (CPU, RAM, storage) to existing server.

**Example:**
```
Before: Server with 4 CPU cores, 8GB RAM
After:  Server with 16 CPU cores, 64GB RAM
```

**Pros:**
- [APPROVED] Simple to implement
- [APPROVED] No application changes needed
- [APPROVED] Easy to manage (single server)
- [APPROVED] Lower complexity

**Cons:**
- [REJECTED] Hardware limits (can't scale infinitely)
- [REJECTED] Single point of failure
- [REJECTED] Requires downtime for upgrades
- [REJECTED] Expensive at high end

**When to Use:**
- Just starting, traffic is low
- Quick, low-cost performance boost needed
- Application not built for distributed systems
- Downtime acceptable
- Predictable, stable workloads
- High computational power needed per instance

---

### 6.2 Horizontal Scaling (Scale Out)

**Definition:**
Adding more servers/instances to distribute load.

**Example:**
```
Before: 1 server handling 1000 requests/sec
After:  5 servers each handling 200 requests/sec
```

**Pros:**
- [APPROVED] No hard limit (add more servers indefinitely)
- [APPROVED] High availability (one server fails, others continue)
- [APPROVED] No downtime for updates (rolling updates)
- [APPROVED] Cost-effective (use commodity hardware)
- [APPROVED] Better fault tolerance

**Cons:**
- [CAUTION] More complex to manage
- [CAUTION] Requires load balancer
- [CAUTION] Application must support distributed architecture
- [CAUTION] Session management challenges
- [CAUTION] Data consistency complexity

**When to Use:**
- Users spread across regions
- Uptime critical
- Rapid or steady growth expected
- Containerized/microservices architecture
- Avoid downtime during updates
- Large, growing datasets
- High concurrent user load

---

### 6.3 Diagonal Scaling (Hybrid)

**Definition:**
Combination of vertical and horizontal scaling.

**How It Works:**
```
Start: Vertical scaling (upgrade server)
Growth continues: Add horizontal scaling (more servers)
```

**Benefits:**
- [APPROVED] Flexibility
- [APPROVED] Start simple, grow complex as needed
- [APPROVED] Balance cost and capability

**When to Use:**
- Uncertain growth trajectory
- Need adaptability
- Want to optimize costs

---

### 6.4 Decision Factors

**Location Needs:**
- Users spread globally → Horizontal/diagonal
- Local users → Vertical acceptable

**Reliability:**
- Mission-critical → Horizontal (backup systems)
- Internal tools → Vertical acceptable

**Flexibility:**
- Frequent updates → Horizontal (no downtime)
- Stable system → Vertical acceptable

**Complexity:**
- Small team → Vertical (simpler)
- Large DevOps team → Horizontal manageable

**Performance:**
- CPU-intensive → Vertical
- I/O-intensive, distributed → Horizontal

---

## Section 7: Health Checks (Kubernetes Probes)

### 7.1 Three Types of Probes

---

### 7.2 Liveness Probe

**Purpose:**
Determines when to **restart a container**.

**Use Case:**
Detects when application is **deadlocked or hung**.
- Process running but unable to make progress
- Application stops serving requests but container still alive

**Example Scenario:**
Your app has deadlock, causing it to hang indefinitely. Process continues running, so Kubernetes thinks everything is fine. **Liveness probe detects app is unresponsive and restarts pod**.

**Configuration:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: web
    image: myapp:1.0.0
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 30  # Wait 30s after startup
      periodSeconds: 10         # Check every 10s
      timeoutSeconds: 5         # 5s timeout per check
      failureThreshold: 3       # Restart after 3 failures
```

[CAUTION] Liveness probe does NOT wait for readiness. If you need startup delay, use `initialDelaySeconds` or startup probe.

---

### 7.3 Readiness Probe

**Purpose:**
Determines when container is **ready to accept traffic**.

**Use Case:**
Application takes time to warm up, load data, establish connections.

**Example Scenario:**
Your app takes 1 minute to start. Without readiness probe, Kubernetes sends traffic immediately, resulting in errors. **Readiness probe ensures traffic only sent when app fully ready**.

**Behavior:**
- If readiness probe fails, **Kubernetes removes pod from service endpoints**
- Pod not restarted, just marked "not ready"
- **Runs throughout container lifecycle**

**Also useful during lifecycle:**
- Recovering from temporary faults
- Temporarily overloaded
- Performing maintenance

**Configuration:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: web
    image: myapp:1.0.0
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
      failureThreshold: 3
```

---

### 7.4 Startup Probe

**Purpose:**
Handles **slow-starting containers**.

**Use Case:**
Legacy applications or containers requiring significant startup time.

**How It Works:**
- Disables liveness and readiness checks until startup probe succeeds
- Once succeeds, liveness/readiness take over

**Configuration:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: legacy-app
spec:
  containers:
  - name: app
    image: legacy:1.0.0
    startupProbe:
      httpGet:
        path: /startup
        port: 8080
      initialDelaySeconds: 0
      periodSeconds: 10
      failureThreshold: 30  # 30 * 10s = 5 minutes max startup time
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      periodSeconds: 5
```

**Benefits:**
- [APPROVED] Prevents liveness probe from killing slow-starting container
- [APPROVED] Once started, normal liveness/readiness checks apply

---

### 7.5 Probe Mechanisms

**Three ways to check health:**

**1. HTTP GET** (Most common)

```yaml
httpGet:
  path: /health
  port: 8080
  httpHeaders:
  - name: Authorization
    value: Bearer token
```
Success: HTTP status 200-399

**2. TCP Socket**

```yaml
tcpSocket:
  port: 3306
```
Success: TCP connection established

**3. Command Execution**

```yaml
exec:
  command:
  - cat
  - /tmp/healthy
```
Success: Exit code 0

---

### 7.6 Implementing Health Endpoints

**Application developer's responsibility:**
Expose URL that kubelet can check.

**Example (Node.js):**

```javascript
app.get('/health', (req, res) => {
  // Check dependencies
  const dbHealthy = checkDatabaseConnection()
  const cacheHealthy = checkCacheConnection()
  
  if (dbHealthy && cacheHealthy) {
    res.status(200).json({ status: 'healthy' })
  } else {
    res.status(503).json({ status: 'unhealthy' })
  }
})

app.get('/ready', (req, res) => {
  // Check if app finished initialization
  if (appInitialized && dataLoaded) {
    res.status(200).json({ status: 'ready' })
  } else {
    res.status(503).json({ status: 'not ready' })
  }
})
```

---

### 7.7 Health Check Best Practices

**1. Separate Liveness and Readiness Endpoints**
- Liveness: Basic health (is process working?)
- Readiness: Full readiness (can handle traffic?)

**2. Keep Checks Lightweight**
- [APPROVED] Should complete quickly (<1 second)
- [REJECTED] Don't perform expensive operations
- [REJECTED] Don't check external dependencies in liveness (may cause cascading restarts)

**3. Set Appropriate Thresholds**

```yaml
failureThreshold: 3    # Not too sensitive
successThreshold: 1    # Default
periodSeconds: 10      # Frequent enough but not excessive
timeoutSeconds: 5      # Reasonable timeout
```

**4. Use Startup Probes for Slow Apps**
- Prevents premature liveness failures
- Allows adequate startup time

---

## Section 8: Database Migration Strategies

### 8.1 Zero Downtime Migration Principles

**Key Principles:**
1. **Backward Compatibility**
2. **Data Integrity**
3. **Performance Optimization**

---

### 8.2 Blue-Green Deployment

**How It Works:**

```
Setup:
- Blue environment: Current production (old database)
- Green environment: New environment (new database)

Process:
1. Traffic routes to Blue (production continues)
2. Green environment prepared with new database
3. Data migrated to Green
4. Green extensively tested
5. Traffic switched from Blue to Green
6. Blue kept as backup

Rollback: Instant (switch back to Blue)
```

**Benefits:**
- [APPROVED] Zero downtime
- [APPROVED] Easy rollback
- [APPROVED] Can test thoroughly before switch
- [APPROVED] No data loss if issues arise

**Challenges:**
- [CAUTION] Requires double infrastructure (expensive)
- [CAUTION] Database synchronization during cutover
- [CAUTION] All-or-nothing switch

**Best For:**
- Mission-critical systems
- Need instant rollback capability
- Can afford duplicate infrastructure

---

### 8.3 Canary Releases

**How It Works:**

```
Process:
1. Deploy new database version to small subset (5-10% traffic)
2. Monitor metrics closely
3. Gradually increase traffic (25% → 50% → 100%)
4. Rollback if issues detected

Gradual, risk-mitigating approach
```

**Benefits:**
- [APPROVED] Limits blast radius
- [APPROVED] Real-world validation
- [APPROVED] Can rollback at any stage
- [APPROVED] Smooth transition

**Best For:**
- High-risk changes
- Want gradual rollout
- Need production validation

---

### 8.4 Phased Rollouts

**How It Works:**

```
Phases:
1. Migrate read-only tables first
2. Then migrate low-traffic tables
3. Finally migrate high-traffic tables
4. Each phase validated before next
```

**Benefits:**
- [APPROVED] Incremental risk
- [APPROVED] Can pause/rollback at phase boundaries
- [APPROVED] Learn from each phase

**Best For:**
- Large databases
- Complex migrations
- Need conservative approach

---

### 8.5 Migration Best Practices

**1. Data Integrity**

**Implement robust validation:**
- [APPROVED] Automated checksums
- [APPROVED] Data verification scripts
- [APPROVED] Compare old vs new databases
- [APPROVED] Rollback capabilities as safety nets

**Example Validation:**

```sql
-- Compare row counts
SELECT 'old_db' as source, COUNT(*) FROM old_db.users
UNION ALL
SELECT 'new_db' as source, COUNT(*) FROM new_db.users;

-- Checksum validation
SELECT 'old_db' as source, MD5(CONCAT_WS('|', id, name, email)) FROM old_db.users
UNION ALL
SELECT 'new_db' as source, MD5(CONCAT_WS('|', id, name, email)) FROM new_db.users;
```

---

**2. Resource Management**

**Balance migration workload against normal operations:**
- [APPROVED] Throttle migration speed during peak hours
- [APPROVED] Use read replicas for migration source
- [APPROVED] Monitor resource utilization
- [APPROVED] Maintain optimal performance without overtaxing

---

**3. Middleware Solutions**

**For bridging old and new databases:**
- Dual-write to both databases temporarily
- Read from old, write to both
- Validate consistency
- Switch reads to new database
- Remove old database

**Handles feature discrepancies.**

---

**4. Testing in Staging**

**Test migration in environment mirroring production:**
- [APPROVED] Same data volume
- [APPROVED] Same schema complexity
- [APPROVED] Same workload patterns

**Identify issues before production.**

---

**5. Monitoring During Migration**

**Essential for successful migration:**
- [ ] Query performance
- [ ] Error rates
- [ ] Replication lag
- [ ] Resource utilization
- [ ] Data consistency checks

**Automated alerts for anomalies.**

---

## Section 9: Service Mesh

### 9.1 What is a Service Mesh?

**Purpose:**
Add reliability, security, and observability to microservices by adding transparent "sidecar proxies" alongside application instances.

**Common Features:**
- Automatic retries and timeouts
- Load balancing
- Traffic splitting (canary deployments)
- Circuit breaking
- Mutual TLS (mTLS) encryption
- Distributed tracing

---

### 9.2 Linkerd

**Architecture:**
- **Ultra-lightweight Rust proxies**
- Fine-tuned specifically for service mesh
- Simplified control plane (fewer components)
- Streamlined architecture

**Performance:**
- **40-60% less CPU/memory than Istio**
- **40-400% less latency than Istio**
- Optimized for service mesh use case

**Ease of Use:**
- [APPROVED] Faster setup
- [APPROVED] Easier maintenance
- [APPROVED] Smaller learning curve
- [APPROVED] Reasonable defaults that work immediately

**Features:**
- Automated retry and timeout handling
- Load balancing
- Traffic splitting for canary
- Circuit breaking
- Request routing
- **Minimal configuration needed**

**When to Use Linkerd:**
- Startups and medium-sized businesses
- Need basic service mesh features without complexity
- Performance-sensitive applications
- Financial trading platforms, real-time apps
- **Every millisecond counts**

---

### 9.3 Istio

**Architecture:**
- Envoy proxies (feature-rich but heavier)
- More complex control plane
- More configuration options

**Features:**
- Comprehensive feature set
- Advanced routing capabilities
- Extensive customization
- Mature ecosystem
- Enterprise-grade

**When to Use Istio:**
- Large enterprises
- Complex routing requirements
- Need extensive customization
- Already invested in Envoy ecosystem

---

### 9.4 Running Multiple Service Meshes

[REJECTED] **Generally NOT recommended:**
- Complicated operational environment
- Few teams can manage effectively

[APPROVED] **Better approach:**
- **Standardize on single solution**
- Evaluate thoroughly first
- Test before committing

**Exception:**
Incremental migration from one mesh to another:
- Run in separate namespaces
- Clear boundaries
- Temporary during migration

---

## Complete Deployment Standards Verification Checklist

**Before deploying to production, verify ALL of these:**

### Infrastructure as Code
- [ ] Terraform/Ansible used for infrastructure
- [ ] Remote state storage configured
- [ ] State locking enabled
- [ ] Infrastructure code modularized (DRY)
- [ ] All infrastructure in version control
- [ ] Infrastructure testing implemented (Terratest/Molecule)
- [ ] CI/CD pipeline for infrastructure
- [ ] Plan reviewed before apply

### Containerization & Orchestration
- [ ] Multi-stage Docker builds used
- [ ] Base images and dependencies up-to-date
- [ ] Minimal image layers
- [ ] Resource requests configured
- [ ] Resource limits configured
- [ ] Secrets management implemented (external)
- [ ] GitOps workflow established
- [ ] Security policies enforced (OPA)
- [ ] Environment-specific configurations

### Production Readiness
- [ ] Metrics collection configured
- [ ] Logging infrastructure in place
- [ ] Distributed tracing configured
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] Runbooks created and linked
- [ ] On-call team aware
- [ ] Rollback procedures tested
- [ ] Security requirements met
- [ ] Load testing completed
- [ ] Documentation current

### Observability
- [ ] Structured logging implemented (JSON)
- [ ] Correlation IDs propagated
- [ ] Metrics with appropriate cardinality
- [ ] Alerts tied to SLOs
- [ ] Traces instrumented (OpenTelemetry)
- [ ] Retention policies defined
- [ ] Dashboard/alert ownership assigned

### Disaster Recovery
- [ ] RTO defined for each system
- [ ] RPO defined for each system
- [ ] Backup schedule aligned with RPO
- [ ] 3-2-1 backup rule followed
- [ ] Immutable backups configured
- [ ] Offsite backups configured
- [ ] Recovery procedures documented
- [ ] DR plan tested (last 12 months)

### Scaling
- [ ] Scaling strategy defined (vertical/horizontal/diagonal)
- [ ] Auto-scaling configured (if applicable)
- [ ] Load balancer configured (if horizontal)
- [ ] Session management addressed
- [ ] Performance baselines established

### Health Checks
- [ ] Liveness probes configured
- [ ] Readiness probes configured
- [ ] Startup probes configured (if slow-starting)
- [ ] Health endpoints implemented
- [ ] Checks lightweight (<1s)
- [ ] Appropriate thresholds set

### Database Migration
- [ ] Migration strategy chosen (blue-green/canary/phased)
- [ ] Data integrity validation implemented
- [ ] Migration tested in staging
- [ ] Resource throttling configured
- [ ] Monitoring during migration planned
- [ ] Rollback procedure defined

### Service Mesh (if applicable)
- [ ] Service mesh chosen (Linkerd/Istio)
- [ ] mTLS configured
- [ ] Traffic policies defined
- [ ] Observability integrated
- [ ] Performance impact assessed

**If ANY checkbox fails, address before deploying to production.**

---

## When to Read This Canon

**ONLY read this deployment canon when performing deployment operations:**

- Setting up infrastructure (IaC)
- Configuring Kubernetes clusters
- Deploying to production
- Implementing observability
- Planning disaster recovery
- Scaling applications
- Database migrations
- Service mesh implementation

**Do NOT read for:**

- Regular development work
- Writing application code
- Code reviews (unless deployment-related)

This keeps the canon reference brief and targeted.

---

## Version

Deployment Canon Version: 1.0 - Complete (December 30, 2025)  
Based on industry research and best practices for production deployments.

Covers 9 comprehensive categories:
1. Infrastructure as Code (Terraform, Ansible, workflows)
2. Containerization & Orchestration (Docker, Kubernetes, GitOps)
3. Production Readiness Checklists (monitoring, incident response, security, performance, testing, documentation, deployment)
4. Observability (Logs, Metrics, Traces)
5. Disaster Recovery (RTO/RPO, backup strategies, testing)
6. Scaling Strategies (vertical, horizontal, diagonal)
7. Health Checks (Kubernetes liveness/readiness/startup probes)
8. Database Migration (blue-green, canary, phased rollouts)
9. Service Mesh (Linkerd vs Istio)

