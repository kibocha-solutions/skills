System Architecture: Tax Management System (TMS)
================================================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This document contains proprietary system architecture.
   Do not share with external parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

The Tax Management System (TMS) is a cloud-based platform for calculating Kenyan taxes
using Kenya Revenue Authority rules. The system processes tax calculations, stores
receipts, and integrates with KRA eTIMS for compliance reporting.

The architecture follows a **microservices approach**, designed for horizontal scalability,
high availability (99.9% uptime), and regulatory compliance.

.. figure:: diagrams/system-context.png
   :alt: TMS system context diagram
   :width: 800px
   
   Figure 1: TMS system context showing users and external integrations.

Architecture Principles
-----------------------

The architecture follows these core principles:

**Scalability**
- Horizontal scaling for stateless services (API Gateway, Tax Service)
- Vertical scaling for PostgreSQL database
- Auto-scaling based on CPU metrics (target: 70%)

**Reliability**
- 99.9% uptime target
- Multi-AZ deployment on AWS
- Automated health checks and failover

**Security**
- Defense in depth (network, application, data layers)
- Zero-trust network model (mTLS between services)
- Encryption at rest (AES-256) and in transit (TLS 1.3)

**Maintainability**
- Clear service boundaries (single responsibility)
- Comprehensive logging (ELK stack)
- Automated deployment pipelines (GitHub Actions)

Architecture Layers
-------------------

The system is organized into four layers:

**Presentation Layer**
- Web application (React 18 with TypeScript)
- Admin dashboard (React with MUI framework)

**API Layer**
- Kong API Gateway (rate limiting, authentication)
- REST API endpoints (public-facing)
- gRPC services (internal communication)

**Business Logic Layer**
- Tax Calculation Service (Go)
- User Management Service (Go)
- Receipt Service (Go)
- Integration Service (Go)

**Data Layer**
- PostgreSQL 15 (primary database)
- Redis 7 (caching and session storage)
- AWS S3 (receipt storage)
- RabbitMQ (asynchronous messaging)

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

- **ADR-001:** PostgreSQL over MongoDB (ACID compliance for financial data)
- **ADR-002:** Microservices over Monolith (independent scaling, team autonomy)
- **ADR-003:** gRPC for internal communication (performance, type safety)
- **ADR-004:** Redis for session storage (speed, TTL support)
- **ADR-005:** AWS S3 for receipt storage (durability, compliance requirements)

System Metrics
--------------

**Current Scale (as of December 2025):**
- 50,000 registered users
- 200,000 tax calculations per month
- 500,000 receipts stored
- Average API response time: 120ms (p95)
- Database size: 15 GB

**Target Scale (12 months):**
- 500,000 registered users
- 2,000,000 tax calculations per month
- 5,000,000 receipts stored
- Target API response time: <150ms (p95)

Technology Summary
------------------

**Languages:** Go, TypeScript, SQL  
**Frameworks:** React, MUI, gRPC  
**Databases:** PostgreSQL, Redis  
**Infrastructure:** Kubernetes (EKS), AWS  
**Monitoring:** Prometheus, Grafana  
**Logging:** ELK Stack
