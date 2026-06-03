# Canon: Architecture Documentation

## Purpose

Architecture documentation explains how the system is structured, why design decisions were made, and how components interact. It serves as the blueprint for understanding system organization, technology choices, scaling strategy, and integration patterns.

---

## Scope

**This canon applies to:**
- Overall system architecture (entire platform or product)
- Individual microservice architecture (if complex, 10+ services)
- Infrastructure architecture (deployment topology, networking)
- Data architecture (data flow, storage strategy)

**This canon does NOT apply to:**
- Code-level design patterns (document in code comments)
- API specifications (use API documentation canons)
- Database schema details (use database documentation canon)

---

## Access Level Classification

**Architecture Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Internal teams, authorized personnel only
- **Storage:** Private repository with authentication
- **Review:** Technical review, architecture board approval
- **Rationale:** Contains proprietary design decisions, technology stack details, and competitive advantages

**Exception:** High-level architecture overview may be Public (Level 1) for marketing or recruiting purposes, but technical implementation details remain Internal.

---

## When to Generate

### Initial Creation
- **Design Phase:** Before implementation begins (highly recommended)
- **Architecture Design Review:** Document proposed architecture for team review
- **Technology Selection:** Document choices and trade-offs

### Updates
- After major architectural changes
- When adding new services or components
- After technology stack changes
- Quarterly architecture reviews

### Frequency
- **Initial:** During system design phase
- **Major Updates:** After significant architectural changes
- **Minor Updates:** Quarterly reviews for accuracy
- **Refactoring:** Document before and after major refactoring

---

## Files to Generate

Agent must create the following files when documenting system architecture:

### 1. Architecture Overview (Entry Point)
**File:** `/docs/source/architecture/00-overview.rst`  
**Format:** reStructuredText  
**Purpose:** Main architecture document linking to all architecture sections

### 2. System Context (C4 Model Level 1)
**File:** `/docs/source/architecture/01-system-context.rst`  
**Format:** reStructuredText  
**Purpose:** Explain system in relation to users and external systems

### 3. Container Architecture (C4 Model Level 2)
**File:** `/docs/source/architecture/02-containers.rst`  
**Format:** reStructuredText  
**Purpose:** Document major containers (applications, databases, message brokers)

### 4. Component Architecture (C4 Model Level 3)
**File:** `/docs/source/architecture/03-components.rst`  
**Format:** reStructuredText  
**Purpose:** Break down key containers into components

### 5. Technology Stack
**File:** `/docs/source/architecture/04-technology-stack.rst`  
**Format:** reStructuredText  
**Purpose:** Document all technologies used and justification for choices

### 6. Data Flow
**File:** `/docs/source/architecture/05-data-flow.rst`  
**Format:** reStructuredText  
**Purpose:** Explain how data moves through the system

### 7. Scalability Architecture
**File:** `/docs/source/architecture/06-scalability.rst`  
**Format:** reStructuredText  
**Purpose:** Document horizontal/vertical scaling strategy

### 8. Security Architecture
**File:** `/docs/source/architecture/07-security.rst`  
**Format:** reStructuredText  
**Purpose:** Document security layers, authentication, authorization

### 9. Integration Points
**File:** `/docs/source/architecture/08-integration-points.rst`  
**Format:** reStructuredText  
**Purpose:** Document all external system integrations

### 10. Architecture Diagrams
**Directory:** `/docs/source/architecture/diagrams/`  
**Format:** diagrams.net (formerly draw.io) `.drawio` files  
**Purpose:** Visual representations of architecture (C4 diagrams, data flow diagrams)

---

## Directory Structure

```
docs/source/architecture/
├── 00-overview.rst                 # Architecture entry point
├── 01-system-context.rst           # C4 Context diagram explanation
├── 02-containers.rst               # Container-level architecture
├── 03-components.rst               # Component-level details
├── 04-technology-stack.rst         # Technology choices and rationale
├── 05-data-flow.rst                # Data movement through system
├── 06-scalability.rst              # Scaling strategy
├── 07-security.rst                 # Security architecture
├── 08-integration-points.rst       # External system integrations
└── diagrams/
    ├── system-context.drawio       # C4 Context diagram
    ├── system-context.png          # Exported PNG for docs
    ├── containers.drawio           # C4 Containers diagram
    ├── containers.png              # Exported PNG
    ├── components.drawio           # C4 Components diagram
    ├── components.png              # Exported PNG
    ├── data-flow.drawio            # Data flow diagram
    └── data-flow.png               # Exported PNG
```

---

## Generation Rules

### C4 Model Architecture

Follow the C4 model for consistent architecture documentation:

**Level 1: System Context**
- System boundary
- Users (personas)
- External systems
- High-level interactions

**Level 2: Containers**
- Web applications
- Mobile applications
- Backend services
- Databases
- Message brokers
- File storage

**Level 3: Components**
- Major components within containers
- Responsibilities
- Interactions

**Level 4: Code** (optional, usually in code documentation)
- Class diagrams
- Sequence diagrams

### Diagram Standards

1. **Use diagrams.net** (formerly draw.io) for all architecture diagrams
2. **Export to PNG** for embedding in documentation
3. **Store both .drawio and .png** files
4. **Use consistent colors** across diagrams
5. **Include legend** explaining shapes and colors
6. **Keep diagrams simple** (max 15-20 elements per diagram)
7. **Use standard C4 notation** for system, container, component diagrams

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice preferred
- Specific over vague
- Vary sentence structure
- No AI clichés
- Lists only for true itemization or procedures

---

## Content Guidelines

### Architecture Overview (`/docs/source/architecture/00-overview.rst`)

```rst
System Architecture
===================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This document contains proprietary system architecture.
   Do not share with external parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

[Service/System Name] is a [brief description of what the system does].

The architecture follows a [monolithic / microservices / serverless / hybrid] approach,
designed for [scalability / performance / maintainability / specific business goals].

.. figure:: diagrams/system-context.png
   :alt: System context diagram
   :width: 800px
   
   Figure 1: System context showing external entities and interactions.

Architecture Principles
-----------------------

The architecture follows these core principles:

**Scalability**
- Horizontal scaling for stateless services
- Vertical scaling for databases
- Auto-scaling based on CPU/memory metrics

**Reliability**
- 99.9% uptime target
- Multi-region deployment
- Automated failover

**Security**
- Defense in depth
- Zero-trust network model
- Encryption at rest and in transit

**Maintainability**
- Clear service boundaries
- Comprehensive logging and monitoring
- Automated deployment pipelines

Architecture Layers
-------------------

The system is organized into these layers:

**Presentation Layer**
- Web application (React)
- Mobile applications (iOS, Android)
- Admin dashboard

**API Layer**
- REST API gateway
- GraphQL API (internal)
- gRPC services (microservice communication)

**Business Logic Layer**
- User service
- Payment service
- Notification service
- Reporting service

**Data Layer**
- PostgreSQL (primary database)
- Redis (caching)
- S3 (file storage)

.. toctree::
   :maxdepth: 1

   01-system-context
   02-containers
   03-components
   04-technology-stack
   05-data-flow
   06-scalability
   07-security
   08-integration-points

Key Design Decisions
--------------------

Major architectural decisions are documented as Architecture Decision Records (ADRs).

See :doc:`/decisions/index` for detailed decision records:

- ADR-001: Choice of PostgreSQL over MongoDB
- ADR-002: Microservices vs Monolith
- ADR-003: gRPC for internal service communication
- ADR-004: Redis for session storage
```

### System Context (`/docs/source/architecture/01-system-context.rst`)

```rst
System Context
==============

The system context diagram shows [System Name] in relation to users and external systems.

.. figure:: diagrams/system-context.png
   :alt: System context diagram
   :width: 900px
   
   System context showing users and external integrations.

Users
-----

**End Users**
- Web browser access via HTTPS
- Mobile app access via REST API
- Authentication required

**Administrators**
- Admin dashboard access
- Read/write permissions
- Audit logging enabled

**System Administrators**
- Infrastructure access via VPN
- SSH access to servers
- Database access (restricted)

External Systems
----------------

**Kenya Revenue Authority (KRA) eTIMS**
- Integration: REST API
- Purpose: Tax compliance reporting
- Authentication: OAuth 2.0
- Data exchanged: Tax calculations, receipts

**M-Pesa Payment Gateway**
- Integration: REST API
- Purpose: Mobile money payments
- Authentication: API key + signature
- Data exchanged: Payment requests, confirmations

**SendGrid Email Service**
- Integration: SMTP / REST API
- Purpose: Transactional emails
- Authentication: API key
- Data exchanged: Email templates, delivery status

**AWS S3**
- Integration: AWS SDK
- Purpose: File storage (receipts, documents)
- Authentication: IAM credentials
- Data exchanged: Uploaded files, retrieval requests

System Boundary
---------------

The system boundary includes:

- Web application (user-facing)
- Mobile applications (iOS, Android)
- API gateway
- Backend microservices
- Databases and caching layer
- Message queue

The system boundary excludes:

- Payment processors (external)
- Email delivery (external)
- File storage infrastructure (AWS S3)
- Tax authority systems (KRA eTIMS)
```

### Technology Stack (`/docs/source/architecture/04-technology-stack.rst`)

```rst
Technology Stack
================

This document lists all technologies used in the system and justification for each choice.

Frontend
--------

**Web Application**
- **Technology:** React 18 with TypeScript
- **Rationale:** Component-based architecture, strong typing, large ecosystem
- **Alternatives Considered:** Vue.js (smaller community), Angular (steeper learning curve)

**Mobile Applications**
- **Technology:** React Native
- **Rationale:** Code sharing between iOS and Android, faster development
- **Alternatives Considered:** Native (higher cost), Flutter (Dart learning curve)

**UI Framework**
- **Technology:** Material-UI (MUI)
- **Rationale:** Production-ready components, accessibility support
- **Alternatives Considered:** Ant Design, Chakra UI

Backend
-------

**API Gateway**
- **Technology:** Kong Gateway
- **Rationale:** Plugin ecosystem, rate limiting, authentication
- **Alternatives Considered:** AWS API Gateway (vendor lock-in), Nginx (less features)

**Microservices**
- **Technology:** Go (Golang)
- **Rationale:** High performance, concurrency support, small binaries
- **Alternatives Considered:** Node.js (slower), Java (larger memory footprint)

**API Protocols**
- **REST:** Public APIs (OpenAPI 3.0)
- **gRPC:** Internal microservice communication (Protocol Buffers)
- **GraphQL:** Internal data federation

Data Storage
------------

**Primary Database**
- **Technology:** PostgreSQL 15
- **Rationale:** ACID compliance, JSON support, mature ecosystem
- **Alternatives Considered:** MySQL (less feature-rich), MongoDB (schema flexibility not needed)

**Caching Layer**
- **Technology:** Redis 7
- **Rationale:** In-memory speed, pub/sub support, persistence options
- **Alternatives Considered:** Memcached (less features)

**Message Queue**
- **Technology:** RabbitMQ
- **Rationale:** Reliable message delivery, dead letter queues
- **Alternatives Considered:** Kafka (overkill for our scale), AWS SQS (vendor lock-in)

**File Storage**
- **Technology:** AWS S3
- **Rationale:** Durability (99.999999999%), scalability, cost-effective
- **Alternatives Considered:** Google Cloud Storage, Azure Blob Storage

Infrastructure
--------------

**Container Orchestration**
- **Technology:** Kubernetes (EKS on AWS)
- **Rationale:** Industry standard, portability, scaling capabilities
- **Alternatives Considered:** Docker Swarm (less features), AWS ECS (vendor lock-in)

**CI/CD**
- **Technology:** GitHub Actions
- **Rationale:** Tight Git integration, free for public repos, YAML pipelines
- **Alternatives Considered:** GitLab CI, Jenkins (maintenance overhead)

**Monitoring**
- **Technology:** Prometheus + Grafana
- **Rationale:** Open-source, extensive ecosystem, Kubernetes integration
- **Alternatives Considered:** Datadog (cost), New Relic (vendor lock-in)

**Logging**
- **Technology:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Rationale:** Full-text search, log aggregation, visualization
- **Alternatives Considered:** Splunk (cost), CloudWatch (vendor lock-in)

Security
--------

**Authentication**
- **Technology:** JWT (JSON Web Tokens)
- **Rationale:** Stateless, scalable, industry standard
- **Alternatives Considered:** Session tokens (less scalable)

**Secrets Management**
- **Technology:** HashiCorp Vault
- **Rationale:** Dynamic secrets, encryption as a service, audit logs
- **Alternatives Considered:** AWS Secrets Manager (vendor lock-in)

**TLS Certificates**
- **Technology:** Let's Encrypt + cert-manager
- **Rationale:** Free, automated renewal, trusted CA
- **Alternatives Considered:** Commercial CAs (cost)
```

### Data Flow (`/docs/source/architecture/05-data-flow.rst`)

```rst
Data Flow
=========

This document explains how data moves through the system.

.. figure:: diagrams/data-flow.png
   :alt: Data flow diagram
   :width: 900px
   
   Data flow through the system from user request to response.

User Authentication Flow
-------------------------

1. User submits credentials (email, password) via web/mobile app
2. Request hits API gateway
3. API gateway forwards to Auth Service
4. Auth Service validates credentials against PostgreSQL
5. Auth Service generates JWT token (15-minute expiry)
6. JWT token returned to client
7. Client includes JWT in Authorization header for subsequent requests

Data Write Flow (Example: Create Invoice)
------------------------------------------

1. User creates invoice via web app
2. POST request to API gateway with JWT token
3. API gateway validates JWT, forwards to Invoice Service
4. Invoice Service validates request data
5. Invoice Service writes to PostgreSQL (invoices table)
6. Invoice Service publishes "invoice.created" event to RabbitMQ
7. Tax Service consumes event, calculates taxes asynchronously
8. Tax Service writes tax data to PostgreSQL
9. Notification Service consumes event, queues email via SendGrid
10. Invoice Service returns HTTP 201 with invoice ID to client

Data Read Flow (Example: Fetch User Dashboard)
-----------------------------------------------

1. User requests dashboard via web app
2. GET request to API gateway with JWT token
3. API gateway validates JWT, forwards to Dashboard Service
4. Dashboard Service checks Redis cache for user data
5. **Cache Hit:** Return cached data (response time: 10ms)
6. **Cache Miss:**
   - Query PostgreSQL for user data (response time: 50ms)
   - Write data to Redis cache (TTL: 5 minutes)
   - Return data to client
7. Client renders dashboard

Background Job Flow
-------------------

1. Scheduler triggers daily report generation (00:00 UTC)
2. Report Service queries PostgreSQL for aggregated data
3. Report Service generates PDF using wkhtmltopdf
4. Report Service uploads PDF to AWS S3
5. Report Service writes record to PostgreSQL (reports table)
6. Report Service publishes "report.generated" event to RabbitMQ
7. Notification Service consumes event, emails report link to users

Real-Time Update Flow (WebSocket)
----------------------------------

1. Client establishes WebSocket connection to Notification Service
2. Notification Service authenticates JWT, subscribes to user's channel (Redis pub/sub)
3. Backend service publishes update to Redis channel
4. Notification Service receives update from Redis
5. Notification Service pushes update to client via WebSocket
6. Client updates UI in real-time
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all architecture reST files
rstcheck docs/source/architecture/*.rst
```

**Expected output:** No errors

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

### Diagram Validation

- [ ] All .drawio files open successfully in diagrams.net
- [ ] All .png files exported from .drawio sources
- [ ] Diagrams embedded correctly in reST files
- [ ] Diagrams render in Sphinx HTML build

---

## diagrams.net Best Practices

### Export Settings

When exporting diagrams to PNG:

1. **Resolution:** 300 DPI minimum
2. **Background:** Transparent or white
3. **Border Width:** 10px padding
4. **Format:** PNG (not JPEG)
5. **Naming:** [diagram-name].png (same as .drawio filename)

### Diagram Standards

**Colors:**
- Users: #4A90E2 (blue)
- System boundaries: #7ED321 (green)
- External systems: #F5A623 (orange)
- Databases: #BD10E0 (purple)
- Services: #50E3C2 (teal)

**Shapes:**
- Users: Stick figures
- External systems: Boxes with dashed border
- Internal systems: Boxes with solid border
- Databases: Cylinder shape
- Message queues: Horizontal parallelogram

---

## Examples Reference

See working example: `02-examples/architecture-example/`

**Example includes:**
- Complete architecture documentation set
- C4 model diagrams (system context, containers, components)
- Data flow diagrams
- Technology stack justification
- All diagrams in both .drawio and .png formats

---

## Access Level Warning

Include at top of `00-overview.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This document contains proprietary system architecture.
   Do not share with external parties.
```

---

## Agent Checklist

Before marking architecture documentation complete, verify:

- [ ] Architecture overview (00-overview.rst) created
- [ ] System context documented with C4 diagram
- [ ] Container architecture documented with C4 diagram
- [ ] Component architecture documented (if applicable)
- [ ] Technology stack listed with justifications
- [ ] Data flow documented with diagram
- [ ] Scalability strategy documented
- [ ] Security architecture documented
- [ ] Integration points documented
- [ ] All diagrams exported as PNG and embedded
- [ ] Access level warning included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Sentence structure varies naturally
- [ ] No AI clichés detected
- [ ] ADRs referenced for major decisions

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial architecture documentation canon
- Based on C4 model
- Follows `_docs-canon.md` v4 specifications
