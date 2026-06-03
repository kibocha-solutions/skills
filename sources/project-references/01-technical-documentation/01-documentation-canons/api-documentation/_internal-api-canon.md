# Canon: Internal API Documentation

## Purpose

Internal API documentation provides comprehensive references for service-to-service communication within private networks. Internal APIs demand the same rigor as public APIs but include additional considerations for service discovery, circuit breakers, retry policies, and internal authentication mechanisms.

---

## Scope

**This canon applies to:**
- Internal REST APIs for microservice communication
- Internal GraphQL APIs for internal data federation
- Internal gRPC services for high-performance internal communication
- APIs consumed exclusively by internal services (not third-party developers)

**This canon does NOT apply to:**
- Public APIs for third-party developers (use `_rest-api-canon.md`, `_graphql-api-canon.md`, or `_grpc-api-canon.md`)
- Simple database queries (document in service architecture docs)
- Direct function calls within monoliths (use code documentation)

---

## Access Level Classification

**Internal APIs:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Internal teams, authorized personnel, service-to-service communication only
- **Storage:** Private repository with authentication required
- **Review:** Technical review, security clearance for sensitive endpoints
- **Exposure:** Never publicly accessible, internal network only

---

## When to Generate

### Initial Creation
- **Before Implementation:** Contract-first approach (recommended for new services)
- **During Development:** Implementation-first (acceptable for rapid prototyping)

### Updates
- Every interface change (new endpoints, schema changes, deprecations)
- Automated via CI/CD pipeline
- Security changes trigger immediate documentation update

### Frequency
- **Continuous:** Part of development workflow
- **Pre-Deployment:** Complete review before service deployment
- **Post-Incident:** Document any changes after production issues

---

## API Type Selection

Agent must determine which internal API type to document:

### When to Use REST (Internal)
- Simple request-response patterns
- CRUD operations
- Widely supported by all languages
- Teams familiar with HTTP/JSON

**Canon to follow:** `_rest-api-canon.md` + this canon's internal-specific additions

### When to Use GraphQL (Internal)
- Flexible data fetching requirements
- Real-time subscriptions needed
- Data federation across multiple services
- Reducing over-fetching and under-fetching

**Canon to follow:** `_graphql-api-canon.md` + this canon's internal-specific additions

### When to Use gRPC (Internal)
- High-performance requirements
- Strongly-typed contracts preferred
- Services written in compiled languages (Go, Rust, C++, Java)
- Streaming communication patterns

**Canon to follow:** `_grpc-api-canon.md` + this canon's internal-specific additions

---

## Internal-Specific Requirements

### 1. Service Discovery

Document how services discover each other:

#### Kubernetes DNS

```rst
Service Discovery
=================

Services discover each other using Kubernetes DNS.

Service Address Format
----------------------

.. code-block:: text

   [service-name].[namespace].svc.cluster.local:[port]

Example:

.. code-block:: text

   user-service.production.svc.cluster.local:8080

Environment Variables
---------------------

Service addresses are injected via environment variables:

.. code-block:: bash

   USER_SERVICE_URL=http://user-service.production.svc.cluster.local:8080
   ORDER_SERVICE_URL=http://order-service.production.svc.cluster.local:8080
```

#### Consul Service Registry

```rst
Service Discovery
=================

Services register with Consaland discover peers using Consul DNS.

Service Registration
--------------------

Services register on startup:

.. code-block:: json

   {
     "Name": "user-service",
     "ID": "user-service-1",
     "Address": "10.0.1.5",
     "Port": 8080,
     "Check": {
       "HTTP": "http://10.0.1.5:8080/health",
       "Interval": "10s"
     }
   }

Service Discovery
-----------------

Query Consul DNS:

.. code-block:: bash

   dig @127.0.0.1 -p 8600 user-service.service.consul SRV
```

### 2. Authentication

Document internal authentication mechanisms:

#### mTLS (Mutual TLS)

```rst
Authentication
==============

All internal services use mutual TLS (mTLS) for authentication.

Certificate Setup
-----------------

Each service has a client and server certificate issued by internal CA.

**Client Configuration:**

.. code-block:: go

   creds, err := credentials.NewClientTLSFromFile("ca.crt", "")
   conn, err := grpc.Dial("service:50051", grpc.WithTransportCredentials(creds))

**Server Configuration:**

.. code-block:: go

   creds, err := credentials.NewServerTLSFromFile("server.crt", "server.key")
   server := grpc.NewServer(grpc.Creds(creds))

Certificate Rotation
--------------------

Certificates expire after 90 days. Automated rotation via cert-manager.
```

#### JWT Tokens (Service-to-Service)

```rst
Authentication
==============

Internal services authenticate using short-lived JWT tokens.

Obtaining a Token
-----------------

Request token from internal auth service:

.. code-block:: http

   POST /auth/token HTTP/1.1
   Host: auth-service.internal
   Content-Type: application/json

   {
     "service_id": "user-service",
     "service_secret": "SERVICE_SECRET"
   }

Response:

.. code-block:: json

   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "expires_in": 3600
   }

Using the Token
---------------

Include token in Authorization header:

.. code-block:: http

   GET /users/123 HTTP/1.1
   Host: user-service.internal
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Token Caching
-------------

Cache tokens until expiration. Refresh 5 minutes before expiry.
```

### 3. Retry Policies

Document retry behavior for failed requests:

```rst
Retry Policies
==============

Failed requests are retried automatically with exponential backoff.

Retry Configuration
-------------------

- **Max Attempts:** 3
- **Initial Backoff:** 100ms
- **Max Backoff:** 5s
- **Backoff Multiplier:** 2

Retryable Errors
----------------

The following errors trigger retries:

- ``503 Service Unavailable``
- ``504 Gateway Timeout``
- Network connection errors
- DNS resolution failures

Non-Retryable Errors
--------------------

The following errors do NOT trigger retries:

- ``400 Bad Request``
- ``401 Unauthorized``
- ``403 Forbidden``
- ``404 Not Found``

Implementation Example (Go)
---------------------------

.. code-block:: go

   import "github.com/cenkalti/backoff/v4"

   operation := func() error {
       resp, err := http.Get(url)
       if err != nil {
           return err
       }
       if resp.StatusCode == 503 || resp.StatusCode == 504 {
           return fmt.Errorf("retriable error: %d", resp.StatusCode)
       }
       return nil
   }

   err := backoff.Retry(operation, backoff.NewExponentialBackOff())
```

### 4. Circuit Breakers

Document circuit breaker patterns:

```rst
Circuit Breakers
================

Circuit breakers prevent cascading failures.

Circuit States
--------------

**Closed:** Requests pass through normally  
**Open:** Requests immediately fail (circuit tripped)  
**Half-Open:** Testing if service recovered

Circuit Breaker Configuration
------------------------------

- **Failure Threshold:** 5 consecutive failures
- **Timeout:** 30 seconds
- **Success Threshold:** 2 consecutive successes (to close from half-open)

Implementation Example (Go)
---------------------------

.. code-block:: go

   import "github.com/sony/gobreaker"

   cb := gobreaker.NewCircuitBreaker(gobreaker.Settings{
       Name:        "user-service",
       MaxRequests: 2,
       Interval:    30 * time.Second,
       Timeout:     10 * time.Second,
       ReadyToTrip: func(counts gobreaker.Counts) bool {
           return counts.ConsecutiveFailures >= 5
       },
   })

   result, err := cb.Execute(func() (interface{}, error) {
       return http.Get(url)
   })

Monitoring
----------

Circuit breaker state is exposed via ``/metrics`` endpoint:

.. code-block:: text

   circuit_breaker_state{service="user-service"} 0  # 0=closed, 1=open, 2=half-open
   circuit_breaker_failures_total{service="user-service"} 5
```

### 5. Timeouts

Document timeout policies:

```rst
Timeouts
========

All requests have configured timeouts to prevent indefinite blocking.

Timeout Configuration
---------------------

- **Connection Timeout:** 5 seconds
- **Request Timeout:** 30 seconds
- **Idle Connection Timeout:** 90 seconds

Setting Timeouts (Go)
---------------------

.. code-block:: go

   client := &http.Client{
       Timeout: 30 * time.Second,
       Transport: &http.Transport{
           DialContext: (&net.Dialer{
               Timeout: 5 * time.Second,
           }).DialContext,
           IdleConnTimeout: 90 * time.Second,
       },
   }

   ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
   defer cancel()

   req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
   resp, err := client.Do(req)

Timeout Best Practices
----------------------

- Set timeouts on all outbound requests
- Use context deadlines for request propagation
- Log timeout occurrences for monitoring
- Fail fast rather than retrying indefinitely
```

### 6. Rate Limiting (Internal)

Document internal rate limiting if applicable:

```rst
Rate Limiting
=============

Internal services enforce rate limits to prevent resource exhaustion.

Limits
------

- **Per Service:** 1,000 requests per second
- **Per Endpoint:** Varies by endpoint criticality

Rate Limit Headers
------------------

Responses include rate limit headers:

.. code-block:: http

   X-RateLimit-Limit: 1000
   X-RateLimit-Remaining: 950
   X-RateLimit-Reset: 1640000000

Handling Rate Limits
--------------------

When rate limit exceeded (HTTP 429):

.. code-block:: json

   {
     "error": "rate_limit_exceeded",
     "retry_after": 60
   }

Implement exponential backoff when rate limited.
```

---

## Files to Generate

Agent must create the same files as the corresponding API type (REST, GraphQL, or gRPC), PLUS:

### Additional Internal API Files

**File:** `/docs/source/api-reference/internal-apis/service-discovery.rst`  
**Purpose:** Document service discovery mechanism

**File:** `/docs/source/api-reference/internal-apis/authentication.rst`  
**Purpose:** Document internal authentication (mTLS, service tokens)

**File:** `/docs/source/api-reference/internal-apis/resilience.rst`  
**Purpose:** Document retry policies, circuit breakers, timeouts

**File:** `/docs/source/api-reference/internal-apis/monitoring.rst`  
**Purpose:** Document metrics, health checks, observability

---

## Directory Structure

```
project-root/
│
├── api-specs/
│   ├── [service-name]-api.yaml          # OpenAPI (if REST)
│   ├── schema.graphql                   # GraphQL SDL (if GraphQL)
│   └── [service-name].proto             # Proto3 (if gRPC)
│
└── docs/source/api-reference/
    ├── 00-index.rst                     # API documentation entry point
    ├── 01-overview.rst                  # API overview
    ├── 02-authentication.rst            # Authentication (general)
    ├── 04-errors.rst                    # Error handling
    │
    ├── rest/                            # If REST API
    │   └── ...
    │
    ├── graphql/                         # If GraphQL API
    │   └── ...
    │
    ├── grpc/                            # If gRPC API
    │   └── ...
    │
    └── internal-apis/                   # Internal-specific docs
        ├── 00-index.rst                 # Internal API entry point
        ├── service-discovery.rst        # Service discovery
        ├── authentication.rst           # Internal authentication (mTLS, tokens)
        ├── resilience.rst               # Retry, circuit breakers, timeouts
        └── monitoring.rst               # Metrics, health checks
```

---

## Access Level Warning

All internal API documentation must include this warning:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This API is for internal service-to-service communication only.
   Do not expose to external parties or public networks.
   Access requires VPN or internal network connectivity.
```

---

## Validation

Follow validation procedures from the corresponding API type canon (REST, GraphQL, or gRPC), PLUS:

### Internal-Specific Validations

- [ ] Service discovery mechanism documented
- [ ] Internal authentication explained (mTLS, JWT, API keys)
- [ ] Retry policies configured and documented
- [ ] Circuit breaker thresholds specified
- [ ] Timeout values configured
- [ ] Health check endpoints documented
- [ ] Metrics endpoints documented
- [ ] Internal access warning included

---

## Agent Checklist

Before marking internal API documentation complete, verify:

- [ ] API type selected (REST, GraphQL, or gRPC)
- [ ] Corresponding API canon followed (REST/GraphQL/gRPC)
- [ ] Service discovery documented
- [ ] Internal authentication documented
- [ ] Retry policies documented
- [ ] Circuit breaker patterns documented
- [ ] Timeout policies documented
- [ ] Health check endpoints documented
- [ ] Metrics endpoints documented
- [ ] Internal access warning prominently displayed
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Sentence structure varies naturally
- [ ] No AI clichés detected

---

## Examples Reference

See working examples:
- REST Internal API: `02-examples/rest-api-example/` (with internal additions)
- GraphQL Internal API: `02-examples/graphql-api-example/` (with internal additions)
- gRPC Internal API: `02-examples/grpc-api-example/` (with internal additions)

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial internal API documentation canon
- Covers REST, GraphQL, and gRPC internal APIs
- Includes service discovery, resilience patterns, internal auth
- Follows `_docs-canon.md` v4 specifications
