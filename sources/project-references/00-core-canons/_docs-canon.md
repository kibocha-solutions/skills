# Documentation Canon v5: Production-Grade Standards for Technical Documentation

## Overview

This document serves as the authoritative guide for generating production-grade technical documentation across all projects. It specifies documentation types, required structures, format languages, access levels, and integration patterns. Agents generating documentation should reference this canon before creating any technical document.

This canon is built on **JetBrains Writerside** as the primary documentation platform, using **Markdown with semantic markup** for narrative documentation and **API-specific standards** (OpenAPI YAML for REST, GraphQL SDL for GraphQL, Protocol Buffers for gRPC). All documentation is authored in Writerside and exported to static HTML or PDF.

---

## Part 1: Documentation Access Levels & Classification

All documentation must be classified by access level to ensure proper handling, distribution, and security.

### Access Level Definitions

**Level 1: Public**
- Distributed to end users, third-party developers, and general public
- Safe to share on public repositories and documentation sites
- Examples: User guides, API reference (for external APIs), FAQs, tutorials
- Storage: Public GitHub, Read the Docs, public documentation sites
- Review: Standard review process

**Level 2: Internal (Employees/Authorized Personnel)**
- Shared within organization only
- Contains implementation details, architecture decisions, internal processes
- Not shared with external parties (including customers)
- Examples: System architecture, deployment procedures, internal API documentation, operations runbooks
- Storage: Private repository, internal documentation sites with authentication
- Review: Technical review, security clearance may be required

**Level 3: Restricted (Leadership/Core Team)**
- Limited to decision-makers and core technical staff
- Contains strategic information, vendor lock-in details, IP protection measures
- Shared on need-to-know basis only
- Examples: Threat models, security vulnerabilities, IP protection architecture, revenue strategies
- Storage: Encrypted storage, highly restricted access control
- Review: Security review, encryption required

**Level 4: Confidential (Executive/Board)**
- Highly sensitive business and technical information
- Shared only with executive leadership and board members
- Contains financial projections, competitive advantages, long-term strategy
- Examples: Deployment cost analysis, revenue models, customer contracts references
- Storage: Encrypted, air-gapped storage if sensitive
- Review: Executive review, encryption and access logging required

### Access Level Assignment Matrix

| Documentation Type | Default Level | Notes |
|-------------------|---------------|-------|
| User Guides | Public | End-user facing, no internal details |
| API Reference (Public APIs) | Public | Third-party developer documentation |
| API Reference (Internal APIs) | Internal | Service-to-service communication |
| System Architecture | Internal | Implementation details, IP sensitive |
| Deployment Documentation | Internal | Infrastructure details, security risk if public |
| Operations/Runbooks | Internal | Operational procedures, incident response |
| Database Schema | Internal | Data structure, business logic exposed |
| Configuration | Internal | Secrets references, infrastructure details |
| Security Documentation | Restricted | Threat models, vulnerability information |
| ADRs (Architecture Decisions) | Internal | Technical decisions, may contain strategic info |
| Testing Documentation | Internal | Test coverage, edge cases, security implications |
| Onboarding Documentation | Internal | Internal processes, code organization |
| CHANGELOG/Release Notes | Public | User-facing changes, version history |
| Threat Models | Restricted | Security sensitive, breach information |
| Incident Postmortems | Restricted | Contains vulnerability details |
| IP Protection Architecture | Confidential | Revenue model, protection mechanisms |

---

## Part 2: Core Documentation Languages & Technologies

### 2.1 Writerside with Markdown: Primary Documentation Platform

**Standard:** JetBrains Writerside with Markdown (CommonMark) and semantic XML markup is the primary format for all narrative technical documentation.

**Rationale:**
- Modern authoring experience with live preview in IDE
- Markdown ease-of-use with semantic structure when needed
- Integrates API specifications (OpenAPI) with narrative documentation
- Smart completion, validation, and inspections built-in
- Multiple output formats: HTML, PDF from single source
- Version-control friendly (plain text Markdown)
- AI-friendly (generates llms.txt for AI context)

**Authoring Tool:** JetBrains Writerside (IntelliJ IDEA plugin)
- Installation: IntelliJ IDEA Community Edition (free) + Writerside plugin
- Setup: File → New → Project → Writerside → Starter Project
- Preview: Live preview in Writerside Preview tool window
- Build: Export To → Web Archive (static HTML)
- Output: Static HTML website (responsive, searchable, customizable)

**Syntax Reference:**
```markdown
# Title (Top Level)

## Section (Level 2)

### Subsection (Level 3)

Paragraph text with **bold**, *italic*, and ``code``.

List of items:

- Item 1
- Item 2
- Item 3

Code blocks with syntax highlighting:

.. code-block:: python

   def calculate_tax(salary):
       return salary * 0.15

Cross-references:

- Link to document: :doc:`other-document`
- Link to section: :ref:`section-label`
- External link: `Text <https://example.com>`_

Admonitions (warnings, notes, etc.):

.. note::
   This is a note.

.. warning::
   This is a warning.

Tables:

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

Images:

.. figure:: diagrams/architecture.png
   :alt: System architecture
   :width: 600px
   
   Figure caption explaining the diagram.
```

**Key Directives for Documentation:**

| Directive | Purpose | Usage |
|-----------|---------|-------|
| `.. code-block:: LANGUAGE` | Syntax-highlighted code | API examples, implementation details |
| `.. note::`, `.. warning::`, `.. tip::` | Admonitions | Important information, cautions |
| `.. figure::` or `.. image::` | Embed diagrams/images | Architecture diagrams, screenshots |
| `.. toctree::` | Table of contents | Navigation structure |
| `:doc:` | Internal document link | Cross-references |
| `:ref:` | Internal section link | Reference to labeled sections |
| `.. table::` | Table with caption | Data comparison, reference tables |

---

### 2.2 REST API: OpenAPI 3.0 YAML Specification

**Standard:** OpenAPI 3.0 specification in YAML format for REST APIs.

**Rationale:**
- Machine-readable API contract
- Generates interactive documentation (Swagger UI)
- Enables automatic SDK generation
- Validates API implementation against spec
- Industry standard (Open API Initiative)
- Human-readable with comments supported
- Less verbose than JSON

**When to Use:**
- Public REST APIs for third-party developers
- Internal REST APIs for service-to-service communication
- APIs with 20+ endpoints
- APIs requiring SDK generation
- Contract-first API development

**File Location:** `/api-specs/rest-api.yaml`

**Basic Structure:**
```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
  description: Detailed description
  contact:
    name: API Support
    url: https://support.example.com
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://sandbox.example.com/v1
    description: Sandbox (testing)

security:
  - bearerAuth: []

paths:
  /endpoint:
    post:
      summary: Short description
      operationId: uniqueOperationId
      tags:
        - TagName
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RequestSchema'
      responses:
        '200':
          description: Success response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseSchema'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    RequestSchema:
      type: object
      properties:
        fieldName:
          type: string
          description: Field description
```

**Tools:**
- **Authoring:** Swagger Editor, Stoplight Studio, VS Code with OpenAPI extension
- **Validation:** `swagger-cli validate api-spec.yaml`
- **Documentation:** Swagger UI (auto-generated interactive docs)
- **Visualization:** Redoc for beautiful API reference docs

---

### 2.3 GraphQL API: GraphQL Schema Definition Language (SDL)

**Standard:** GraphQL SDL for GraphQL API definitions.

**Rationale:**
- Language-agnostic schema definition
- Introspection provides self-documenting APIs
- GraphQL Playground generates interactive documentation automatically
- Schema validation and type safety
- Perfect for both public and internal GraphQL APIs

**When to Use:**
- Public GraphQL APIs for third-party developers
- Internal GraphQL APIs for service-to-service communication
- Flexible query requirements (clients specify what data they need)
- Real-time subscription needs

**File Location:** `/api-specs/schema.graphql`

**Basic Structure:**
```graphql
"""
Calculate Kenyan taxes using KRA rules
"""
type Query {
  """
  Calculate PAYE tax based on monthly salary
  """
  calculatePAYE(
    """Monthly gross salary in KES"""
    grossSalary: Float!
    
    """Personal relief amount (default: 2400 KES)"""
    relief: Float = 2400
  ): TaxResult!
  
  """Get current tax brackets"""
  taxBrackets(
    """Tax type: PAYE, VAT, WHT, etc."""
    taxType: TaxType!
  ): [TaxBracket!]!
}

"""
Tax calculation result
"""
type TaxResult {
  """Total tax amount in KES"""
  taxAmount: Float!
  
  """Effective tax rate as percentage"""
  effectiveRate: Float!
  
  """Breakdown by tax bracket"""
  breakdown: [TaxBracket!]!
}

"""
Tax bracket information
"""
type TaxBracket {
  """Income range (e.g., "0-24000")"""
  bracket: String!
  
  """Tax rate percentage"""
  rate: Float!
  
  """Tax amount for this bracket"""
  amount: Float!
}

enum TaxType {
  PAYE
  VAT
  WHT
  TURNOVER
  RENTAL
}

"""
Mutations for tax rule updates
"""
type Mutation {
  updateTaxBrackets(input: UpdateBracketsInput!): UpdateResult!
}

input UpdateBracketsInput {
  taxType: TaxType!
  brackets: [BracketInput!]!
}

input BracketInput {
  lower: Float!
  upper: Float!
  rate: Float!
}

type UpdateResult {
  success: Boolean!
  message: String!
}

"""
Real-time subscriptions
"""
type Subscription {
  """Subscribe to tax rule changes"""
  bracketUpdated(taxType: TaxType!): TaxBracket!
}
```

**Tools:**
- **Authoring:** Apollo Studio, GraphQL IDE, text editor
- **Validation:** GraphQL schema validation tools
- **Documentation:** GraphQL Playground or Apollo Studio (auto-generated from schema)
- **Testing:** Apollo Client Devtools, Altair GraphQL Client

---

### 2.4 gRPC API: Protocol Buffers (Proto3)

**Standard:** Protocol Buffers 3 (proto3) for gRPC service definitions.

**Rationale:**
- Strongly typed, efficient binary serialization
- Auto-generates type-safe client/server stubs
- Multiple language support (Java, Go, Python, Rust, C++, etc.)
- Perfect for internal service-to-service communication
- Built-in request/response documentation

**When to Use:**
- Internal service-to-service communication
- High-performance requirements (better than REST for internal APIs)
- Microservices needing efficient binary protocols
- Services written in compiled languages (Go, Rust, C++)

**File Location:** `/api-specs/services.proto`

**Basic Structure:**
```protobuf
syntax = "proto3";

package tms.v1;

option go_package = "github.com/example/tms/pb/v1";
option java_package = "com.example.tms.pb.v1";
option java_outer_classname = "TaxServiceProto";

/**
 * Service for tax calculations
 */
service TaxCalculationService {
  /**
   * Calculate PAYE tax for an employee
   */
  rpc CalculatePAYE(PayeRequest) returns (TaxResult);
  
  /**
   * Get current tax brackets
   */
  rpc GetTaxBrackets(GetBracketsRequest) returns (TaxBracketsResponse);
  
  /**
   * Streaming: Calculate tax for multiple salaries
   */
  rpc CalculateBatch(stream PayeRequest) returns (stream TaxResult);
}

/**
 * PAYE calculation request
 */
message PayeRequest {
  /**
   * Monthly gross salary in KES
   */
  double gross_salary = 1;
  
  /**
   * Personal relief amount (default: 2400 KES)
   */
  double relief = 2;
}

/**
 * Tax calculation result
 */
message TaxResult {
  /**
   * Total tax in KES
   */
  double tax_amount = 1;
  
  /**
   * Effective tax rate as percentage
   */
  double effective_rate = 2;
  
  /**
   * Tax breakdown by bracket
   */
  repeated TaxBracket breakdown = 3;
}

/**
 * Individual tax bracket information
 */
message TaxBracket {
  string bracket = 1;      // e.g., "0-24000"
  double rate = 2;         // Percentage
  double amount = 3;       // Tax for this bracket
}

/**
 * Request for tax brackets
 */
message GetBracketsRequest {
  TaxType tax_type = 1;
}

/**
 * Response with tax brackets
 */
message TaxBracketsResponse {
  repeated TaxBracket brackets = 1;
  string effective_date = 2;
}

/**
 * Supported tax types
 */
enum TaxType {
  TAX_TYPE_UNSPECIFIED = 0;
  PAYE = 1;
  VAT = 2;
  WHT = 3;
  TURNOVER = 4;
  RENTAL = 5;
}
```

**Tools:**
- **Compilation:** `protoc` compiler (generates stubs)
- **Verification:** Protocol buffer linting
- **Documentation:** Auto-generated from proto comments
- **Testing:** grpcurl for manual testing

---

### 2.5 Internal API Documentation (Service-to-Service)

**Standard:** Internal APIs documented as either REST (OpenAPI), GraphQL (SDL), or gRPC (Proto), depending on use case.

**Scope:** Service-to-service communication within private networks

**Access Level:** Level 2 (Internal)

**When to Use:**
- REST: Simple request-response patterns, widely supported
- GraphQL: Flexible queries, real-time needs
- gRPC: High performance, internal systems with compiled languages

**Documentation Requirements:**
- Same rigor as public APIs
- Include service discovery mechanisms
- Document retry policies and timeouts
- Include circuit breaker patterns
- Document authentication (mTLS, tokens, API keys)

---

### 2.6 Writerside Integration

**Purpose:** Central authoring and build platform that transforms Markdown source files with semantic markup into production-grade HTML/PDF documentation.

**Setup:** Writerside project with `.tree` files

**Key Components:**
```
project-root/
├── writerside.cfg                     # Project configuration
├── topics/                            # Markdown/XML topics
│   ├── starter.md                     # Main landing page
│   ├── getting-started.md             # Quick start guide
│   └── ...                            # Additional topics
├── c.tree                             # Table of contents (instance tree)
└── images/                            # Images and diagrams
```

**Writerside Project Configuration (`writerside.cfg`):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ihp SYSTEM "https://resources.jetbrains.com/writerside/1.0/ihp.dtd">
<ihp version="2.0">
    <settings>
        <name>Project Name</name>
        <version>1.0</version>
    </settings>
    <topics dir="topics" web-path="/"/>
    <images dir="images" web-path="images"/>
</ihp>
```

**Build Process:**
- **Local Preview:** Live preview in Writerside Preview tool window (automatic)
- **Export:** Writerside tool window → Export To → Web Archive
- **Output:** Static HTML (ZIP archive, extract and deploy)
- **PDF Export:** Export To → PDF

**Output:**
- Static HTML website (fully responsive, searchable, customizable)
- PDF export capability
- Hosted on GitHub Pages, Netlify, or custom server
- No server-side processing required

---

## Part 3: Documentation Types & Specifications

Each documentation type below includes:
- **Purpose:** Why this documentation exists
- **Scope:** What it covers
- **Access Level:** Classification (Public, Internal, Restricted, Confidential)
- **When to Create:** Lifecycle timing
- **Format:** Markdown (.md), OpenAPI YAML, GraphQL SDL, or Proto3
- **Location:** File path in repository
- **Structure:** Directory layout and file organization
- **Contents:** Detailed file-by-file breakdown
- **Examples:** Real-world templates and patterns

---

## 1. System Architecture Documentation

**Purpose:** Explain how the system is structured, component interactions, technology choices, and design rationale.

**Scope:**
- Overall system (entire platform)
- Per microservice (if complex, 10+ services)
- Infrastructure deployment architecture

**Access Level:** Internal (Level 2)

**When to Create:**
- **Initial:** During system design phase (before coding)
- **Update:** After major architectural changes
- **Frequency:** Review quarterly, update as needed

**Format:** Markdown (.md) with Writerside semantic markup

**Location:** `/docs/writerside/topics/architecture/`

**Directory Structure:**
```
docs/writerside/topics/architecture/
├── overview.md                     # Main architecture document (entry point)
├── system-context.md               # C4 context diagram explanation
├── containers.md                   # Container-level architecture
├── components.md                   # Component-level details
├── technology-stack.md             # Technology choices and justification
├── data-flow.md                    # Data movement through system
├── scalability.md                  # Scaling strategy
├── security.md                     # Security architecture
└── integration-points.md           # External system integrations

docs/writerside/images/diagrams/
├── system-context.drawio           # C4 Context diagram (draw.io format)
├── containers.drawio               # C4 Containers diagram
├── components.drawio               # C4 Components diagram
└── data-flow.drawio                # Data flow diagram
```

**Contents: overview.md (Main Entry Point)**

```markdown
# System Architecture

<warning>
<p>INTERNAL DOCUMENTATION - Level 2 Access</p>
<p>This document contains proprietary system architecture. Do not share with external parties.</p>
</warning>

## Overview

Provide a high-level explanation of the system purpose and scope.

![System context showing external entities and interactions](diagrams/system-context.png){width="800"}

## Architecture Layers

Describe the layered architecture (e.g., API layer, business logic, persistence).

## Related Topics

- [System Context](system-context.md)
- [Containers](containers.md)
- [Components](components.md)
- [Technology Stack](technology-stack.md)
- [Data Flow](data-flow.md)
- [Scalability](scalability.md)
- [Security Architecture](security.md)
- [Integration Points](integration-points.md)

## Key Design Decisions

Reference Architecture Decision Records (ADRs) that explain why key choices were made.

See [Decision Log](decisions.md) for detailed decision records.
```

---

## 2. API Documentation

**Purpose:** Complete reference for all API endpoints (REST, GraphQL, or gRPC), including request/response formats, authentication, error handling, and code examples.

**Scope:**
- Public REST APIs (external developers)
- Public GraphQL APIs (external developers)
- Internal REST APIs (service-to-service)
- Internal GraphQL APIs (service-to-service)
- Internal gRPC APIs (service-to-service)

**Access Level:**
- **Public APIs:** Public (Level 1)
- **Internal APIs:** Internal (Level 2)

**When to Create:**
- **Initial:** Contract-first (before implementation) OR during development
- **Update:** Every API change (automated via CI/CD)
- **Frequency:** Continuous (part of development workflow)

**Format:**
- **REST API:** OpenAPI YAML specification + Markdown narrative documentation (Writerside)
- **GraphQL API:** GraphQL SDL specification + Markdown narrative documentation (Writerside)
- **gRPC API:** Proto3 specification + Markdown narrative documentation (Writerside)
- **Internal APIs:** Same format as public equivalents

**Location:**
- Specifications: `/api-specs/` (root level)
- Narrative docs: `/docs/writerside/topics/api-reference/`
- OpenAPI integration: Reference OpenAPI specs in Writerside topics

**Directory Structure:**

```
Project Root/
├── api-specs/
│   ├── rest-api.yaml               # OpenAPI 3.0 for REST
│   ├── schema.graphql              # GraphQL schema
│   └── services.proto              # gRPC service definitions
│
docs/writerside/topics/api-reference/
├── overview.md                     # API documentation entry point
├── authentication.md               # Auth mechanisms for all APIs
├── rate-limits.md                  # Rate limiting and quotas
├── errors.md                       # Error codes and meanings
├── versioning.md                   # API versioning strategy
├── rest/
│   ├── overview.md                 # REST API entry point
│   ├── reference.md                # Embed OpenAPI spec or link to Swagger UI
│   ├── tutorials/
│   │   ├── first-calculation.md
│   │   └── batch-processing.md
│   └── examples.md                 # Code examples for all languages
├── graphql/
│   ├── overview.md                 # GraphQL entry point
│   ├── schema.md                   # Schema definition
│   ├── playground.md               # GraphQL Playground instructions
│   ├── queries.md                  # Query examples
│   └── subscriptions.md            # Subscription examples
├── grpc/
│   ├── overview.md                 # gRPC entry point
│   ├── services.md                 # Service definitions
│   ├── messages.md                 # Message types
│   └── examples.md                 # Code examples
├── internal-apis/
│   ├── overview.md                 # Internal APIs entry point
│   ├── rest/
│   │   ├── overview.md
│   │   └── services.md
│   ├── graphql/
│   │   └── overview.md
│   └── grpc/
│       └── overview.md
└── sdks/
    ├── python.md                   # Python SDK guide
    ├── javascript.md               # JavaScript SDK guide
    └── java.md                     # Java SDK guide
```

**REST API Specification (OpenAPI YAML)**

**File:** `/api-specs/rest-api.yaml`

```yaml
openapi: 3.0.0
info:
  title: Tax Calculation API
  version: 1.0.0
  description: |
    Calculate Kenyan taxes using Kenya Revenue Authority rules.
    
    ## Getting Started
    1. Sign up for an API key: https://dashboard.example.com
    2. Include key in Authorization header: `Authorization: Bearer YOUR_KEY`
    3. Make your first request: `POST /calculate/paye`
  contact:
    name: API Support
    url: https://support.example.com
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://sandbox.example.com/v1
    description: Sandbox (for testing)

security:
  - bearerAuth: []

paths:
  /calculate/paye:
    post:
      summary: Calculate PAYE Tax
      description: |
        Calculates Pay-As-You-Earn (PAYE) tax based on gross salary
        and Kenya Revenue Authority current tax brackets.
      operationId: calculatePAYE
      tags:
        - Tax Calculation
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PAYERequest'
      responses:
        '200':
          description: Tax calculated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaxResult'
        '400':
          description: Invalid request
        '429':
          description: Rate limit exceeded

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    PAYERequest:
      type: object
      required:
        - gross_salary
      properties:
        gross_salary:
          type: number
          format: double
          minimum: 0
          description: Monthly gross salary in KES
    
    TaxResult:
      type: object
      properties:
        tax_amount:
          type: number
          format: double
          description: Total tax in KES
        effective_rate:
          type: number
          format: double
          description: Effective tax rate as percentage
```

**GraphQL API Specification (GraphQL SDL)**

**File:** `/api-specs/schema.graphql`

```graphql
"""
Tax calculation queries
"""
type Query {
  """Calculate PAYE tax"""
  calculatePAYE(
    grossSalary: Float!
    relief: Float = 2400
  ): TaxResult!
  
  """Get current tax brackets"""
  taxBrackets(taxType: TaxType!): [TaxBracket!]!
}

"""
Tax calculation mutations
"""
type Mutation {
  """Update tax brackets (admin only)"""
  updateTaxBrackets(input: UpdateBracketsInput!): UpdateResult!
}

"""
Real-time subscription to tax rule changes
"""
type Subscription {
  """Subscribe to tax bracket updates"""
  bracketUpdated(taxType: TaxType!): TaxBracket!
}

"""Tax calculation result"""
type TaxResult {
  taxAmount: Float!
  effectiveRate: Float!
  breakdown: [TaxBracket!]!
}

"""Individual tax bracket"""
type TaxBracket {
  bracket: String!
  rate: Float!
  amount: Float!
}

enum TaxType {
  PAYE
  VAT
  WHT
}
```

**gRPC API Specification (Proto3)**

**File:** `/api-specs/services.proto`

```protobuf
syntax = "proto3";

package tms.v1;

service TaxCalculationService {
  rpc CalculatePAYE(PayeRequest) returns (TaxResult);
  rpc GetTaxBrackets(GetBracketsRequest) returns (TaxBracketsResponse);
  rpc CalculateBatch(stream PayeRequest) returns (stream TaxResult);
}

message PayeRequest {
  double gross_salary = 1;
  double relief = 2;
}

message TaxResult {
  double tax_amount = 1;
  double effective_rate = 2;
  repeated TaxBracket breakdown = 3;
}

message TaxBracket {
  string bracket = 1;
  double rate = 2;
  double amount = 3;
}

message GetBracketsRequest {
  TaxType tax_type = 1;
}

message TaxBracketsResponse {
  repeated TaxBracket brackets = 1;
  string effective_date = 2;
}

enum TaxType {
  TAX_TYPE_UNSPECIFIED = 0;
  PAYE = 1;
  VAT = 2;
  WHT = 3;
}
```

**Contents: 00-index.rst (API Documentation Entry Point)**

```rst
API Documentation
=================

Welcome to the Tax Calculation API. This documentation covers REST, GraphQL, and gRPC APIs.

Quick Start
-----------

Choose your preferred API style:

.. toctree::
   :maxdepth: 2

   rest/00-index
   graphql/00-index
   grpc/00-index
   01-overview
   02-authentication
   03-rate-limits
   04-errors
   05-versioning

For Internal APIs Only
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   internal-apis/00-index

.. warning::
   Internal API documentation is for internal use only.
   Do not share external-facing API information with customers.
```

**Contents: rest/00-index.rst (REST API)**

```rst
REST API Reference
==================

The REST API provides standard HTTP endpoints for tax calculations.

.. toctree::
   :maxdepth: 2

   01-reference
   02-tutorials/first-calculation
   03-examples

Interactive Documentation
--------------------------

Try the API directly: `Swagger UI <https://api.example.com/docs>`_
```

**Contents: graphql/00-index.rst (GraphQL API)**

```rst
GraphQL API Reference
=====================

The GraphQL API provides flexible querying with real-time subscriptions.

.. toctree::
   :maxdepth: 2

   01-schema
   02-playground
   03-queries
   04-subscriptions

GraphQL Playground
------------------

Interactive query builder: `GraphQL Playground <https://api.example.com/graphql>`_
```

**Contents: grpc/00-index.rst (gRPC API)**

```rst
gRPC API Reference
==================

The gRPC API provides high-performance service-to-service communication.

.. note::
   gRPC is designed for internal service communication. For external integrations, use REST or GraphQL.

.. toctree::
   :maxdepth: 2

   01-services
   02-messages
   03-examples
   04-streaming
```

**Contents: internal-apis/00-index.rst (Internal APIs)**

```rst
Internal API Reference
======================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   These APIs are for service-to-service communication only.
   Do not share with external parties or customers.

Internal Service APIs
---------------------

.. toctree::
   :maxdepth: 2

   rest/index
   graphql/index
   grpc/index

Service Discovery
-----------------

Internal services discover each other using:

- **Kubernetes DNS:** `service-name.namespace.svc.cluster.local`
- **Service Registry:** Consul for service discovery
- **Load Balancing:** Round-robin with health checks

Authentication
--------------

Internal APIs use mTLS (mutual TLS) certificates.
Generate certificates: See deployment documentation.
```

---

## 3. System Documentation (Services)

**Purpose:** Document a specific microservice or system component.

**Scope:** Per microservice or per service module

**Access Level:** Internal (Level 2)

**When to Create:** During development, before first deployment

**Format:** reST

**Location:** `/docs/source/services/SERVICE_NAME/`

**Directory Structure:**

```
docs/source/services/tms-engine-service/
├── 00-overview.rst                 # Service overview
├── 01-architecture.rst             # Service internals
├── 02-installation.rst             # How to run locally
├── 03-configuration.rst            # Configuration options
├── 04-deployment.rst               # How to deploy
├── 05-operations.rst               # Monitoring and troubleshooting
└── diagrams/
    ├── service-architecture.drawio
    └── request-flow.drawio
```

---

## 4. Deployment Documentation

**Purpose:** Step-by-step instructions for deploying the system.

**Scope:**
- Per environment (development, staging, production)
- Overall infrastructure setup

**Access Level:** Internal (Level 2)

**When to Create:** Before first deployment

**Format:** reST

**Location:** `/docs/source/deployment/`

**Directory Structure:**

```
docs/source/deployment/
├── 00-index.rst                    # Deployment overview
├── 01-local-development.rst        # Local setup
├── 02-staging.rst                  # Staging deployment
├── 03-production.rst               # Production deployment
├── 04-infrastructure.rst           # Infrastructure setup
├── 05-ci-cd-pipeline.rst           # CI/CD automation
├── 06-rollback.rst                 # Rollback procedures
└── 07-disaster-recovery.rst        # DR procedures
```

---

## 5. Operations & Runbook Documentation

**Purpose:** Operational procedures for running systems in production.

**Scope:** Per service (critical services get dedicated runbooks)

**Access Level:** Internal (Level 2)

**When to Create:** Before production launch

**Format:** reST

**Location:** `/docs/source/operations/`

**Directory Structure:**

```
docs/source/operations/
├── 00-runbook-index.rst            # Runbook overview
├── tms-engine-runbook.rst          # TMS Engine runbook
├── api-gateway-runbook.rst         # API Gateway runbook
├── common-issues.rst               # Frequently encountered issues
├── alerting-guide.rst              # Alert interpretations
├── incident-response.rst           # Incident response procedures
└── maintenance-procedures.rst      # Scheduled maintenance
```

---

## 6. Database Documentation

**Purpose:** Document database schema, relationships, and data management procedures.

**Scope:** Per database or logical schema

**Access Level:** Internal (Level 2)

**When to Create:** During database design

**Format:** reST

**Location:** `/docs/source/database/`

**Directory Structure:**

```
docs/source/database/
├── 00-schema-overview.rst          # Schema overview and ERD
├── 01-tables.rst                   # Table definitions
├── 02-indexes.rst                  # Index strategy
├── 03-migrations.rst               # How migrations work
├── 04-backup-restore.rst           # Backup and recovery
└── diagrams/
    └── entity-relationships.drawio
```

---

## 7. Configuration Documentation

**Purpose:** Document all configuration options, environment variables, and feature flags.

**Scope:** Per service configuration

**Access Level:** Internal (Level 2)

**When to Create:** During service setup

**Format:** reST

**Location:** `/docs/source/configuration/`

**Directory Structure:**

```
docs/source/configuration/
├── 00-overview.rst                 # Configuration overview
├── 01-environment-variables.rst    # Environment variables reference
├── 02-feature-flags.rst            # Feature flags and toggles
└── 03-secrets-management.rst       # Secrets (API keys, passwords)
```

---

## 8. Architecture Decision Records (ADRs)

**Purpose:** Historical record of significant architectural and design decisions.

**Scope:** Per project, one record per decision

**Access Level:** Internal (Level 2)

**When to Create:** When making significant technical decisions

**Format:** Markdown

**Location:** `/docs/decisions/`

**File Naming:** `NNNN-decision-title.md` (e.g., `0001-use-rust-for-engine.md`)

**Directory Structure:**

```
docs/decisions/
├── index.md                        # ADR index
├── 0001-use-rust-for-engine.md
├── 0002-postgresql-over-mongodb.md
├── 0003-graphql-federation.md
└── ...
```

**ADR Template:**

```markdown
# ADR-0001: Use Rust for Tax Calculation Engine

## Status
Accepted (2025-01-15)

## Context
Detailed problem statement and constraints.

## Decision
The decision that was made.

## Consequences
Positive and negative consequences.

## Alternatives Considered
Other options and why they were rejected.
```

---

## 9. Testing Documentation

**Purpose:** Document testing approach, coverage, and procedures.

**Scope:** Per project

**Access Level:** Internal (Level 2)

**When to Create:** During development planning

**Format:** reST

**Location:** `/docs/source/testing/`

**Directory Structure:**

```
docs/source/testing/
├── 00-test-strategy.rst            # Overall testing approach
├── 01-unit-tests.rst               # Unit testing guide
├── 02-integration-tests.rst        # Integration testing guide
├── 03-e2e-tests.rst                # End-to-end testing guide
├── 04-performance-tests.rst        # Load and performance testing
└── 05-test-data.rst                # Test data management
```

---

## 10. Security Documentation

**Purpose:** Document security architecture, threats, and compliance.

**Scope:** Per project

**Access Level:** Restricted (Level 3) for threat models and vulnerability details

**When to Create:** During security design phase

**Format:** reST

**Location:** `/docs/source/security/`

**Directory Structure:**

```
docs/source/security/
├── 00-security-overview.rst        # Security overview (Internal - Level 2)
├── 01-threat-model.rst             # Threat model (Restricted - Level 3)
├── 02-authentication-authorization.rst  # Auth mechanisms (Internal - Level 2)
├── 03-encryption.rst               # Data encryption strategy (Internal - Level 2)
├── 04-compliance.rst               # Compliance requirements (Internal - Level 2)
└── 05-incident-response.rst        # Incident response plan (Restricted - Level 3)
```

**File Header for Sensitive Docs:**

```rst
Threat Model
============

.. warning::
   RESTRICTED DOCUMENTATION - Level 3 Access
   This document contains security threat analysis and vulnerability information.
   Share only on need-to-know basis with security team.
```

---

## 11. User Documentation

**Purpose:** End-user facing documentation explaining how to use the system.

**Scope:** Per user type or per feature

**Access Level:** Public (Level 1)

**When to Create:** Before user release

**Format:** reST

**Location:** `/docs/source/user-guide/`

**Directory Structure:**

```
docs/source/user-guide/
├── 00-getting-started.rst          # Getting started guide
├── 01-dashboard.rst                # Dashboard overview
├── 02-filing-returns.rst           # How to file tax returns
├── 03-reports.rst                  # Generating reports
├── 04-faqs.rst                     # Frequently asked questions
└── 05-troubleshooting.rst          # Troubleshooting guide
```

---

## 12. Change Documentation (CHANGELOG)

**Purpose:** Record of what changed between versions.

**Scope:** Per project, one file

**Access Level:** Public (Level 1)

**When to Create:** From first release

**Format:** Markdown

**Location:** `/CHANGELOG.md` (root)

**Template:**

```markdown
# Changelog

## [2.0.0] - 2025-02-01

### Added
- New features

### Changed
- Modified behavior

### Fixed
- Bug fixes

### Security
- Security fixes
```

---

## 13. Onboarding Documentation

**Purpose:** Help new developers get up and running.

**Scope:** Per project

**Access Level:** Internal (Level 2)

**When to Create:** After initial development

**Format:** reST + Markdown

**Location:** `README.md`, `/docs/source/contributing/`

**Directory Structure:**

```
project-root/
├── README.md                       # Project overview
├── CONTRIBUTING.md                 # Contribution guidelines
└── docs/source/contributing/
    ├── 00-setup.rst                # Local development setup
    ├── 01-project-structure.rst    # Repository layout
    ├── 02-code-style.rst           # Code style guidelines
    └── 03-git-workflow.rst         # Git workflow
```

---

## Part 4: CI/CD Integration

All documentation builds and validations must be automated.

**GitHub Actions Workflow: `.github/workflows/docs.yml`**

```yaml
name: Documentation
on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  build-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Validate OpenAPI specs
      - name: Validate OpenAPI specification
        run: |
          npm install -g swagger-cli
          swagger-cli validate api-specs/rest-api.yaml
      
      # Validate GraphQL schema
      - name: Validate GraphQL schema
        run: |
          npm install -g graphql-cli
          graphql-cli validate api-specs/schema.graphql
      
      # Validate Proto files
      - name: Validate Protocol Buffers
        run: |
          apt-get install -y protobuf-compiler
          protoc --version
          protoc --lint_out=. api-specs/services.proto
      
      # Build Sphinx documentation
      - name: Build documentation
        run: |
          pip install sphinx sphinx-rtd-theme
          cd docs
          sphinx-build -W -b html source build/html
      
      # Check for broken links
      - name: Check for broken links
        run: |
          pip install sphinx-linkcheck
          cd docs
          sphinx-build -W -b linkcheck source build/linkcheck
      
      # Lint documentation
      - name: Lint documentation
        run: |
          pip install vale
          vale docs/source/
      
      # Deploy to GitHub Pages
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/html
```

---

## Part 5: Documentation Access & Security

### Access Control Implementation

**Private Repository Structure:**

```
project-root/
├── README.md (Public overview)
├── docs/
│   ├── source/
│   │   ├── user-guide/             # Public - synced to public docs site
│   │   ├── api-reference/          # Split: public + internal
│   │   ├── architecture/           # Internal only - private repo
│   │   ├── operations/             # Internal only - private repo
│   │   ├── security/               # Restricted - encrypted storage
│   │   └── decisions/              # Internal - private repo
│   └── build/                      # Generated HTML
└── api-specs/
    ├── rest-api.yaml               # Public (if public API)
    ├── schema.graphql              # Public (if public API)
    └── services.proto              # Internal only
```

### Documentation Sync Process

**For Public/Internal Documentation:**

```bash
# Sync public documentation to public repository
git subtree push --prefix=docs/build/public origin gh-pages

# Keep internal documentation in private repository only
# Never push internal-apis/, operations/, or security/ to public repo
```

### Access Control in CI/CD

```yaml
# .github/workflows/docs-sync.yml
name: Sync Public Docs
on:
  push:
    branches: [main]

jobs:
  sync-public-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Build all docs
      - name: Build documentation
        run: sphinx-build -b html docs/source docs/build
      
      # Copy only public docs
      - name: Prepare public docs
        run: |
          mkdir -p docs/build/public
          cp -r docs/build/user-guide docs/build/public/
          cp -r docs/build/api-reference/rest docs/build/public/
          cp -r docs/build/api-reference/graphql docs/build/public/
          cp docs/build/CHANGELOG.html docs/build/public/
      
      # Deploy to public GitHub Pages
      - name: Deploy public docs
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/public
          cname: docs.example.com
```

---

## Part 6: Agent Instructions for Document Generation

**When generating any technical document:**

1. **Identify Access Level:** Determine the appropriate access level (Public, Internal, Restricted, Confidential)

2. **Choose Correct Format:**
   - **reST** for narrative documentation
   - **OpenAPI YAML** for REST API specs
   - **GraphQL SDL** for GraphQL APIs
   - **Proto3** for gRPC services
   - **Markdown** for ADRs, README, CHANGELOG

3. **Add Access Warning:** Include appropriate access level warning at document start:
   ```rst
   .. warning::
      [ACCESS LEVEL] DOCUMENTATION
      [Description of access restrictions]
   ```

4. **Follow Directory Structure:** Organize files according to the structure defined for that document type

5. **Reference This Canon:** Cite this document as `docs-canon.md` v4 for consistency

6. **Include Cross-References:** Use reST `:doc:` and `:ref:` directives to link between documents

7. **API Type Specificity:** When documenting APIs:
   - REST: Use OpenAPI YAML + reST narrative
   - GraphQL: Use GraphQL SDL + reST narrative
   - gRPC: Use Proto3 + reST narrative
   - Internal: Same as public equivalents, but marked as Internal (Level 2)

8. **Validate Output:**
   - reST: `rstcheck filename.rst`
   - OpenAPI: `swagger-cli validate api-spec.yaml`
   - GraphQL: `graphql-cli validate schema.graphql`
   - Proto: `protoc --lint_out=. services.proto`
   - Build: `sphinx-build -b html docs/source docs/build`

9. **Use Proper Admonitions:**
   - `.. note::` for clarifications
   - `.. warning::` for access levels and cautions
   - `.. tip::` for helpful hints

10. **Include Runnable Examples:** Every API documentation should have working code examples for each supported language

11. **Update TOC:** Always include table of contents using `.. toctree::` directive

12. **Add Metadata:** Include version, author, date, and access level in document headers

---

## Part 7: Documentation Checklist

**Before marking documentation complete:**

- [ ] Access level specified and enforced
- [ ] All required files present in correct directory structure
- [ ] All reST files compile without errors or warnings
- [ ] All OpenAPI specs validate successfully
- [ ] All GraphQL schemas validate successfully
- [ ] All Proto files compile without errors
- [ ] All code examples are tested and accurate
- [ ] All cross-references resolve correctly
- [ ] All diagrams referenced and accessible
- [ ] Spell check passed
- [ ] Consistent terminology throughout
- [ ] All external links are current (for public docs)
- [ ] Git history is clean
- [ ] CI/CD pipeline passes all checks
- [ ] Access level restrictions enforced in storage
- [ ] Public docs separated from internal docs (if applicable)

---

## References & Related Documents

**Referenced in this document:**

- `conversations.md` - Complete conversation history establishing these standards
- `docs-conversations.md` - Documentation standards conversation
- `personas.md` - Writing styles for different documentation audiences

**External References:**

- Sphinx documentation: https://www.sphinx-doc.org/
- reStructuredText specification: https://docutils.sourceforge.io/rst.html
- OpenAPI 3.0 specification: https://spec.openapis.org/oas/v3.0.3
- GraphQL specification: https://spec.graphql.org/
- Protocol Buffers documentation: https://developers.google.com/protocol-buffers
- Read the Docs theme: https://sphinx-rtd-theme.readthedocs.io/

---

**Document Version:** 4.0
**Last Updated:** 2025-12-29
**Status:** Production (Active)
**Maintained By:** Documentation Standards Committee

**Changes from v3 to v4:**
- Added comprehensive API type coverage (REST, GraphQL, gRPC, Internal)
- Implemented access level classification system (Public, Internal, Restricted, Confidential)
- Added access control implementation for CI/CD workflows
- Detailed API specification examples for each type
- Enhanced security documentation access controls
- Added documentation sync process for public/internal separation
- Clarified internal API documentation requirements
