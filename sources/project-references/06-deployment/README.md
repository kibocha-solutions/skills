# Deployment Standards Reference Documentation

This directory contains comprehensive deployment standards and best practices for production deployments.

## Contents

- **deployment-canon.md** - Complete deployment standards (9 comprehensive categories)

## Coverage

This deployment canon covers:

### 1. Infrastructure as Code (IaC)
- Terraform (provisioning, state management)
- Ansible (configuration management)
- Combined workflow
- Best practices (modularity, testing, pipeline integration)

### 2. Containerization & Orchestration
- Docker best practices (multi-stage builds, layer optimization)
- Kubernetes production requirements
- Resource requests/limits
- Secrets management
- GitOps workflows
- Security automation (OPA)

### 3. Production Readiness Checklists
- Monitoring & Observability (7 checks)
- Incident Response (6 checks)
- Security & Compliance (8 checks)
- Performance & Scalability (8 checks)
- Testing (6 checks)
- Documentation (7 checks)
- Deployment Process (7 checks)

### 4. Observability
- Logs (structured logging, when to use)
- Metrics (performance tracking, alerting)
- Traces (distributed tracing, bottleneck identification)
- How they work together
- Best practices (cardinality, ownership, retention)

### 5. Disaster Recovery
- RTO/RPO definitions and calculation
- Business impact analysis
- Backup strategies (3-2-1 rule, immutable backups)
- Automated recovery
- Hot/warm/cold standby
- Testing procedures
- DR plan components

### 6. Scaling Strategies
- Vertical scaling (when, pros/cons)
- Horizontal scaling (when, pros/cons)
- Diagonal scaling (hybrid)
- Decision factors

### 7. Health Checks
- Liveness probes (restart criteria)
- Readiness probes (traffic routing)
- Startup probes (slow containers)
- Probe mechanisms (HTTP/TCP/exec)
- Implementation guidelines
- Best practices

### 8. Database Migration
- Zero downtime principles
- Blue-green deployment
- Canary releases
- Phased rollouts
- Data integrity validation
- Middleware solutions
- Testing and monitoring

### 9. Service Mesh
- Purpose and features
- Linkerd (lightweight, performant)
- Istio (comprehensive, complex)
- When to use each
- Multi-mesh considerations

## When to Use

**ONLY read this deployment canon when performing deployment operations:**

- Setting up infrastructure (IaC)
- Configuring Kubernetes clusters
- Deploying to production
- Implementing observability
- Planning disaster recovery
- Scaling applications
- Database migrations
- Service mesh implementation

**Do NOT read for regular development work.**

---

Version: 1.0 (December 30, 2025)
