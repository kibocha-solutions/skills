# Canon: REST API Documentation

## Purpose

REST API documentation provides a complete reference for HTTP-based APIs, enabling developers to integrate with your service. It serves as both a machine-readable contract (OpenAPI specification) and human-readable guide (narrative documentation).

---

## Scope

**This canon applies to:**
- Public REST APIs for third-party developers
- Internal REST APIs for service-to-service communication
- APIs with 5+ endpoints
- Contract-first or implementation-first API development

**This canon does NOT apply to:**
- GraphQL APIs (use `_graphql-api-canon.md`)
- gRPC services (use `_grpc-api-canon.md`)
- Simple webhooks or callbacks (document in parent service documentation)

---

## Access Level Classification

**Public REST APIs:**
- **Access Level:** Public (Level 1)
- **Distribution:** Third-party developers, end users, general public
- **Storage:** Public GitHub repository, Read the Docs, public documentation sites
- **Review:** Standard technical review before publication

**Internal REST APIs:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Internal teams, service-to-service communication only
- **Storage:** Private repository with authentication
- **Review:** Technical review, security clearance for sensitive endpoints

---

## When to Generate

### Initial Creation
- **Contract-First:** Before implementation (recommended for new APIs)
- **Implementation-First:** During development (acceptable for rapid prototyping)

### Updates
- Every API change (new endpoints,changed schemas, deprecated features)
- Automated via CI/CD pipeline
- Version changes trigger documentation regeneration

### Frequency
- **Continuous:** Part of development workflow
- **Pre-Release:** Complete review before version release
- **Post-Incident:** Document any security or breaking changes immediately

---

## Files to Generate

Agent must create the following files when documenting a REST API:

### 1. OpenAPI Specification (Machine-Readable Contract)
**File:** `/api-specs/[service-name]-api.yaml`  
**Format:** OpenAPI 3.0 YAML  
**Purpose:** Machine-readable API contract for validation, SDK generation, and interactive documentation

### 2. API Reference Index (Entry Point)
**File:** `/docs/source/api-reference/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Documentation homepage linking to all API documentation sections

### 3. API Overview (Concepts and Philosophy)
**File:** `/docs/source/api-reference/01-overview.rst`  
**Format:** reStructuredText  
**Purpose:** Explain API design philosophy, conventions, and overall structure

### 4. Authentication Documentation
**File:** `/docs/source/api-reference/02-authentication.rst`  
**Format:** reStructuredText  
**Purpose:** Document all authentication and authorization mechanisms

### 5. Rate Limiting Documentation
**File:** `/docs/source/api-reference/03-rate-limits.rst`  
**Format:** reStructuredText  
**Purpose:** Document rate limits, quotas, and throttling policies

### 6. Error Handling Documentation
**File:** `/docs/source/api-reference/04-errors.rst`  
**Format:** reStructuredText  
**Purpose:** Document all error codes, meanings, and resolution steps

### 7. Versioning Strategy
**File:** `/docs/source/api-reference/05-versioning.rst`  
**Format:** reStructuredText  
**Purpose:** Document API versioning approach and lifecycle

### 8. REST API Reference (Link to Interactive Docs)
**File:** `/docs/source/api-reference/rest/01-reference.rst`  
**Format:** reStructuredText  
**Purpose:** Link to Swagger UI or Redoc for interactive API exploration

### 9. Code Examples (Multi-Language)
**File:** `/docs/source/api-reference/rest/02-examples.rst`  
**Format:** reStructuredText  
**Purpose:** Provide working code examples in Python, JavaScript, Java, cURL

---

## Directory Structure

```
project-root/
│
├── api-specs/
│   └── [service-name]-api.yaml          # OpenAPI 3.0 specification
│
└── docs/source/api-reference/
    ├── 00-index.rst                     # API documentation entry point
    ├── 01-overview.rst                  # API concepts and philosophy
    ├── 02-authentication.rst            # Authentication mechanisms
    ├── 03-rate-limits.rst               # Rate limiting and quotas
    ├── 04-errors.rst                    # Error codes and handling
    ├── 05-versioning.rst                # Versioning strategy
    │
    └── rest/
        ├── 00-index.rst                 # REST API entry point
        ├── 01-reference.rst             # Link to Swagger UI / Redoc
        └── 02-examples.rst              # Code examples (multi-language)
```

---

## Generation Rules

### OpenAPI Specification Rules

1. **Use OpenAPI 3.0** (not 2.0/Swagger)
2. **YAML format** (not JSON) for human readability
3. **Complete `info` section** with title, version, description, contact, license
4. **Define all servers** (production, sandbox, staging)
5. **Document security schemes** (API keys, OAuth2, JWT)
6. **Use `$ref` for reusable components** (avoid duplication)
7. **Provide examples** for all request bodies and responses
8. **Tag all operations** for logical grouping
9. **Include operation IDs** (unique identifiers for SDK generation)
10. **Document all parameters** (required, type, constraints, defaults)

### Narrative Documentation Rules

1. **Start with overview** explaining API purpose and design philosophy
2. **Document authentication first** (developers need this immediately)
3. **Explain rate limits clearly** (requests per minute, daily quotas)
4. **Categorize errors** (4xx client errors, 5xx server errors)
5. **Provide runnable examples** (not pseudo-code)
6. **Include multiple languages** (Python, JavaScript, Java, cURL minimum)
7. **Link to OpenAPI spec** for interactive testing
8. **Use consistent terminology** throughout all documents
9. **Include quick start guide** (minimal example to get developers running)
10. **Document breaking changes** prominently with migration guides

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice preferred
- Specific over vague (no "may," "might," "could" unless genuine uncertainty)
- Vary sentence structure (mix short, medium, long sentences)
- No AI clichés
- Lists only for procedures, comparisons, or true itemization

---

## Content Guidelines

### OpenAPI Specification (`/api-specs/[service-name]-api.yaml`)

**Required sections:**

```yaml
openapi: 3.0.0
info:
  title: [Service Name] API
  version: 1.0.0
  description: |
    Brief description of API purpose.
    
    ## Getting Started
    1. Sign up for API key
    2. Include key in Authorization header
    3. Make first request
  contact:
    name: API Support
    url: https://support.example.com
    email: api@example.com
  license:
    name: MIT  # Or proprietary license

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://sandbox.example.com/v1
    description: Sandbox (testing)

security:
  - bearerAuth: []  # Or apiKey, oauth2

paths:
  /resource:
    post:
      summary: Short description
      description: Detailed explanation
      operationId: createResource
      tags:
        - ResourceManaement
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResourceRequest'
      responses:
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceResponse'
        '400':
          description: Invalid request
        '401':
          description: Unauthorized
        '429':
          description: Rate limit exceeded

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    ResourceRequest:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          description: Resource name
          minLength: 1
          maxLength: 100
        description:
          type: string
          description: Optional description
```

### API Reference Index (`/docs/source/api-reference/00-index.rst`)

```rst
API Documentation
=================

.. warning::
   [ACCESS LEVEL] DOCUMENTATION
   [Specify: Public (Level 1) OR Internal (Level 2)]

Quick Start
-----------

Get started with the [Service Name] API in minutes.

.. toctree::
   :maxdepth: 2

   01-overview
   02-authentication
   03-rate-limits
   04-errors
   05-versioning
   rest/00-index

Interactive Documentation
--------------------------

Try the API directly: `Swagger UI <https://api.example.com/docs>`_
```

### Authentication Documentation (`/docs/source/api-reference/02-authentication.rst`)

```rst
Authentication
==============

The [Service Name] API uses Bearer token authentication.

Obtaining an API Key
--------------------

Sign up at https://dashboard.example.com to receive your API key.

Using the API Key
-----------------

Include your API key in the Authorization header:

.. code-block:: http

   GET /resource HTTP/1.1
   Host: api.example.com
   Authorization: Bearer YOUR_API_KEY

Example Request
---------------

.. code-block:: python

   import requests

   headers = {
       'Authorization': 'Bearer YOUR_API_KEY',
       'Content-Type': 'application/json'
   }

   response = requests.get(
       'https://api.example.com/v1/resource',
       headers=headers
   )

Security Best Practices
-----------------------

- Store API keys securely (environment variables, secrets manager)
- Rotate keys regularly
- Use HTTPS for all requests
- Never commit keys to version control
```

### Rate Limits Documentation (`/docs/source/api-reference/03-rate-limits.rst`)

```rst
Rate Limits
===========

The API enforces rate limits to ensure fair usage.

Limits
------

- **Free tier:** 100 requests per minute, 10,000 requests per day
- **Pro tier:** 1,000 requests per minute, 100,000 requests per day
- **Enterprise:** Custom limits negotiated

Rate Limit Headers
------------------

Each response includes rate limit information:

.. code-block:: http

   X-RateLimit-Limit: 100
   X-RateLimit-Remaining: 95
   X-RateLimit-Reset: 1640000000

Handling Rate Limits
--------------------

When rate limit is exceeded, the API returns HTTP 429:

.. code-block:: json

   {
     "error": "rate_limit_exceeded",
     "message": "Rate limit exceeded. Retry after 60 seconds.",
     "retry_after": 60
   }

Best practices:

- Implement exponential backoff
- Cache responses when possible
- Batch requests where supported
- Monitor X-RateLimit-Remaining header
```

---

## Validation

Agent must validate documentation before completion:

### OpenAPI Specification Validation

```bash
# Install swagger-cli
npm install -g swagger-cli

# Validate spec
swagger-cli validate api-specs/[service-name]-api.yaml
```

**Expected output:** `api-specs/[service-name]-api.yaml is valid`

### reStructuredText Validation

```bash
# Install rstcheck
pip install rstcheck

# Validate reST files
rstcheck docs/source/api-reference/*.rst
rstcheck docs/source/api-reference/rest/*.rst
```

**Expected output:** No errors

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

---

## Examples Reference

See working example: `02-examples/rest-api-example/`

**Example includes:**
- Complete OpenAPI 3.0 specification
- Full narrative documentation set
- Multi-language code examples
- Authentication examples
- Error handling examples

---

## Access Level Warnings

### Public API Documentation

Include at top of `00-index.rst`:

```rst
.. note::
   PUBLIC DOCUMENTATION - Level 1 Access
   This documentation is publicly available.
```

### Internal API Documentation

Include at top of `00-index.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This API is for internal use only.
   Do not share with external parties.
```

---

## Common Patterns

### Pagination

Document pagination strategy:

```rst
Pagination
----------

List endpoints return paginated results.

Request:

.. code-block:: http

   GET /resources?page=2&limit=50 HTTP/1.1

Response:

.. code-block:: json

   {
     "data": [...],
     "pagination": {
       "current_page": 2,
       "total_pages": 10,
       "total_items": 500,
       "items_per_page": 50
     }
   }
```

### Filtering and Sorting

Document query parameters:

```rst
Filtering
---------

Filter results using query parameters:

.. code-block:: http

   GET /resources?status=active&created_after=2025-01-01 HTTP/1.1

Sorting
-------

Sort results using the ``sort`` parameter:

.. code-block:: http

   GET /resources?sort=-created_at HTTP/1.1

Use ``-`` prefix for descending order.
```

---

## Agent Checklist

Before marking REST API documentation complete, verify:

- [ ] OpenAPI 3.0 specification validates successfully
- [ ] All endpoints documented with examples
- [ ] Authentication mechanisms explained
- [ ] Rate limits documented with headers
- [ ] Error codes catalogued with resolutions
- [ ] Code examples in 3+ languages
- [ ] Interactive documentation link provided
- [ ] Access level warning included
- [ ] Versioning strategy documented
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Sentence structure varies naturally
- [ ] No AI clichés detected

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial REST API documentation canon
- Based on OpenAPI 3.0 standard
- Follows `_docs-canon.md` v4 specifications
