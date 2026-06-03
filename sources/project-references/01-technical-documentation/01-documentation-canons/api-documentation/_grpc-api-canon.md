# Canon: gRPC API Documentation

## Purpose

gRPC API documentation provides a complete reference for high-performance, strongly-typed service-to-service communication using Protocol Buffers. It serves as both machine-readable contract (Proto3 definition) and human-readable guide explaining service interfaces, message structures, and integration patterns.

---

## Scope

**This canon applies to:**
- Internal gRPC services for microservice communication
- High-performance APIs requiring efficient binary protocols
- Services written in compiled languages (Go, Rust, C++, Java)
- Streaming APIs (server streaming, client streaming, bidirectional)

**This canon does NOT apply to:**
- Public-facing APIs for third-party developers (prefer REST or GraphQL)
- Simple request-response patterns (REST is simpler)
- Browser-based clients (gRPC-Web requires additional setup)

---

## Access Level Classification

**gRPC APIs (Typically Internal):**
- **Access Level:** Internal (Level 2)
- **Distribution:** Internal microservices, service-to-service communication only
- **Storage:** Private repository with authentication
- **Review:** Technical review, security clearance for sensitive RPCs

**Note:** gRPC is rarely used for public APIs. This canon assumes internal use.

---

## When to Generate

### Initial Creation
- **Contract-First:** Before implementation (recommended)
- **Code-First:** During development (if using code-generation frameworks)

### Updates
- Every proto file change (new services, RPCs, messages, fields)
- Automated code generation on proto changes
- Breaking changes trigger immediate documentation update

### Frequency
- **Continuous:** Part of development workflow
- **Pre-Deployment:** Complete review before service deployment
- **Post-Incident:** Document any interface or breaking changes immediately

---

## Files to Generate

Agent must create the following files when documenting a gRPC API:

### 1. Protocol Buffer Definition (Machine-Readable Contract)
**File:** `/api-specs/[service-name].proto`  
**Format:** Protocol Buffers 3 (proto3)  
**Purpose:** Machine-readable service contract for code generation and versioning

### 2. API Reference Index (Entry Point)
**File:** `/docs/source/api-reference/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Documentation homepage linking to all API documentation sections

### 3. API Overview (Concepts and Architecture)
**File:** `/docs/source/api-reference/01-overview.rst`  
**Format:** reStructuredText  
**Purpose:** Explain gRPC design, service architecture, and communication patterns

### 4. Authentication Documentation
**File:** `/docs/source/api-reference/02-authentication.rst`  
**Format:** reStructuredText  
**Purpose:** Document authentication (mTLS, JWT, API keys)

### 5. gRPC Services Documentation
**File:** `/docs/source/api-reference/grpc/01-services.rst`  
**Format:** reStructuredText  
**Purpose:** Document all services and RPCs with examples

### 6. Message Types Documentation
**File:** `/docs/source/api-reference/grpc/02-messages.rst`  
**Format:**reStructuredText  
**Purpose:** Document all message types, fields, and validation rules

### 7. Code Examples (Multi-Language)
**File:** `/docs/source/api-reference/grpc/03-examples.rst`  
**Format:** reStructuredText  
**Purpose:** Provide working client examples in Go, Python, Java, Rust

### 8. Streaming Patterns Documentation
**File:** `/docs/source/api-reference/grpc/04-streaming.rst`  
**Format:** reStructuredText  
**Purpose:** Document streaming RPC patterns and lifecycle

### 9. Error Handling Documentation
**File:** `/docs/source/api-reference/04-errors.rst`  
**Format:** reStructuredText  
**Purpose:** Document gRPC status codes and error handling

---

## Directory Structure

```
project-root/
│
├── api-specs/
│   └── [service-name].proto            # Protocol Buffer definition
│
└── docs/source/api-reference/
    ├── 00-index.rst                    # API documentation entry point
    ├── 01-overview.rst                 # gRPC architecture and design
    ├── 02-authentication.rst           # Authentication (mTLS, JWT)
    ├── 04-errors.rst                   # Error handling and status codes
    │
    └── grpc/
        ├── 00-index.rst                # gRPC API entry point
        ├── 01-services.rst             # Service definitions and RPCs
        ├── 02-messages.rst             # Message types and fields
        ├── 03-examples.rst             # Code examples (multi-language)
        └── 04-streaming.rst            # Streaming patterns
```

---

## Generation Rules

### Protocol Buffer Rules

1. **Use proto3 syntax** (not proto2)
2. **Document every service with block comments** (/\*\* ... \*/)
3. **Document every RPC** with purpose and behavior
4. **Document every message** and field
5. **Use descriptive names** (UserService, not Service1)
6. **Number fields sequentially** starting from 1
7. **Reserve removed field numbers** to prevent reuse
8. **Use appropriate types** (int32 for integers, string for text, etc.)
9. **Define package names** matching project structure
10. **Specify language-specific options** (go_package, java_package)

### Narrative Documentation Rules

1. **Start with overview** explaining gRPC benefits and architecture
2. **Document authentication first** (mTLS, interceptors, metadata)
3. **Explain unary vs streaming RPCs**
4. **Provide runnable examples** in multiple languages
5. **Document retry policies** and timeouts
6. **Explain service discovery** mechanisms
7. **Document error handling** (status codes, metadata)
8. **Show streaming lifecycle** (connect, stream, close)
9. **Include performance considerations** (keep-alive, compression)
10. **Document versioning strategy** (proto compatibility)

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice preferred
- Specific over vague
- Vary sentence structure
- No AI clichés
- Lists only for procedures, comparisons, true itemization

---

## Content Guidelines

### Protocol Buffer Definition (`/api-specs/[service-name].proto`)

**Required structure:**

```protobuf
syntax = "proto3";

package myservice.v1;

option go_package = "github.com/example/myservice/pb/v1";
option java_package = "com.example.myservice.pb.v1";
option java_outer_classname = "MyServiceProto";

/**
 * Service for managing user accounts
 */
service UserService {
  /**
   * Create a new user
   * 
   * Returns the created user with generated ID
   */
  rpc CreateUser(CreateUserRequest) returns (User);
  
  /**
   * Get a user by ID
   * 
   * Returns NOT_FOUND if user doesn't exist
   */
  rpc GetUser(GetUserRequest) returns (User);
  
  /**
   * List users with server-side streaming
   * 
   * Server streams users matching filter criteria
   */
  rpc ListUsers(ListUsersRequest) returns (stream User);
  
  /**
   * Batch create users with client-side streaming
   * 
   * Client streams multiple user creation requests
   * Server returns batch result after stream completes
   */
  rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchResult);
  
  /**
   * Real-time user sync with bidirectional streaming
   * 
   * Client and server stream user updates in both directions
   */
  rpc SyncUsers(stream UserUpdate) returns (stream UserUpdate);
}

/**
 * Request message for creating a user
 */
message CreateUserRequest {
  /**
   * User's email address (required, must be valid email format)
   */
  string email = 1;
  
  /**
   * User's display name (required, 1-100 characters)
   */
  string name = 2;
  
  /**
   * User's role (optional, defaults to ROLE_USER)
   */
  Role role = 3;
}

/**
 * Request message for getting a user
 */
message GetUserRequest {
  /**
   * User ID (UUID format)
   */
  string id = 1;
}

/**
 * Request message for listing users
 */
message ListUsersRequest {
  /**
   * Filter by role (optional)
   */
  Role role = 1;
  
  /**
   * Maximum number of users to return (default: 100, max: 1000)
   */
  int32 page_size = 2;
  
  /**
   * Pagination token from previous response
   */
  string page_token = 3;
}

/**
 * Represents a user in the system
 */
message User {
  /**
   * Unique identifier (UUID)
   */
  string id = 1;
  
  /**
   * User's email address
   */
  string email = 2;
  
  /**
   * User's display name
   */
  string name = 3;
  
  /**
   * User's role
   */
  Role role = 4;
  
  /**
   * Account creation timestamp (Unix epoch seconds)
   */
  int64 created_at = 5;
  
  /**
   * Last update timestamp (Unix epoch seconds)
   */
  int64 updated_at = 6;
}

/**
 * User role enumeration
 */
enum Role {
  /**
   * Unspecified role (default)
   */
  ROLE_UNSPECIFIED = 0;
  
  /**
   * Regular user
   */
  ROLE_USER = 1;
  
  /**
   * Administrator
   */
  ROLE_ADMIN = 2;
  
  /**
   * System account
   */
  ROLE_SYSTEM = 3;
}

/**
 * Batch operation result
 */
message BatchResult {
  /**
   * Number of successful operations
   */
  int32 success_count = 1;
  
  /**
   * Number of failed operations
   */
  int32 failure_count = 2;
  
  /**
   * IDs of created users
   */
  repeated string user_ids = 3;
}

/**
 * User update message for streaming
 */
message UserUpdate {
  /**
   * User ID being updated
   */
  string id = 1;
  
  /**
   * Updated user data
   */
  User user = 2;
  
  /**
   * Update timestamp
   */
  int64 timestamp = 3;
}
```

### Services Documentation (`/docs/source/api-reference/grpc/01-services.rst`)

```rst
gRPC Services
=============

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This gRPC API is for internal use only.

UserService
-----------

Manages user accounts with create, read, update operations.

CreateUser
~~~~~~~~~~

Creates a new user account.

**RPC Signature:**

.. code-block:: protobuf

   rpc CreateUser(CreateUserRequest) returns (User);

**Request:**

.. code-block:: json

   {
     "email": "user@example.com",
     "name": "Jane Doe",
     "role": "ROLE_USER"
   }

**Response:**

.. code-block:: json

   {
     "id": "550e8400-e29b-41d4-a716-446655440000",
     "email": "user@example.com",
     "name": "Jane Doe",
     "role": "ROLE_USER",
     "created_at": 1640000000,
     "updated_at": 1640000000
   }

**Error Codes:**

- ``INVALID_ARGUMENT``: Email invalid or name too long
- ``ALREADY_EXISTS``: User with email already exists
- ``INTERNAL``: Database error

GetUser
~~~~~~~

Retrieves a user by ID.

**RPC Signature:**

.. code-block:: protobuf

   rpc GetUser(GetUserRequest) returns (User);

**Request:**

.. code-block:: json

   {
     "id": "550e8400-e29b-41d4-a716-446655440000"
   }

**Response:**

.. code-block:: json

   {
     "id": "550e8400-e29b-41d4-a716-446655440000",
     "email": "user@example.com",
     "name": "Jane Doe",
     "role": "ROLE_USER",
     "created_at": 1640000000,
     "updated_at": 1640000000
   }

**Error Codes:**

- ``INVALID_ARGUMENT``: ID format invalid
- ``NOT_FOUND``: User does not exist
```

### Code Examples (`/docs/source/api-reference/grpc/03-examples.rst`)

```rst
Code Examples
=============

Generate client stubs from proto file, then use in your code.

Generating Client Stubs
------------------------

**Go:**

.. code-block:: bash

   protoc --go_out=. --go_opt=paths=source_relative \
     --go-grpc_out=. --go-grpc_opt=paths=source_relative \
     api-specs/userservice.proto

**Python:**

.. code-block:: bash

   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. \
     api-specs/userservice.proto

**Java:**

.. code-block:: bash

   protoc --java_out=src/main/java --grpc-java_out=src/main/java \
     api-specs/userservice.proto

Go Client Example
-----------------

.. code-block:: go

   package main

   import (
       "context"
       "log"
       "time"

       "google.golang.org/grpc"
       "google.golang.org/grpc/credentials/insecure"
       pb "github.com/example/myservice/pb/v1"
   )

   func main() {
       conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
       if err != nil {
           log.Fatalf("Failed to connect: %v", err)
       }
       defer conn.Close()

       client := pb.NewUserServiceClient(conn)

       ctx, cancel := context.WithTimeout(context.Background(), time.Second)
       defer cancel()

       user, err := client.CreateUser(ctx, &pb.CreateUserRequest{
           Email: "user@example.com",
           Name:  "Jane Doe",
           Role:  pb.Role_ROLE_USER,
       })

       if err != nil {
           log.Fatalf("CreateUser failed: %v", err)
       }

       log.Printf("Created user: %v", user)
   }

Python Client Example
---------------------

.. code-block:: python

   import grpc
   import userservice_pb2
   import userservice_pb2_grpc

   def main():
       channel = grpc.insecure_channel('localhost:50051')
       stub = userservice_pb2_grpc.UserServiceStub(channel)

       request = userservice_pb2.CreateUserRequest(
           email='user@example.com',
           name='Jane Doe',
           role=userservice_pb2.ROLE_USER
       )

       try:
           user = stub.CreateUser(request)
           print(f"Created user: {user}")
       except grpc.RpcError as e:
           print(f"RPC failed: {e.code()}: {e.details()}")

   if __name__ == '__main__':
       main()
```

### Streaming Documentation (`/docs/source/api-reference/grpc/04-streaming.rst`)

```rst
Streaming Patterns
==================

gRPC supports four streaming patterns.

Unary RPC (Request-Response)
-----------------------------

Client sends one request, server sends one response.

.. code-block:: protobuf

   rpc GetUser(GetUserRequest) returns (User);

Server Streaming RPC
--------------------

Client sends one request, server streams multiple responses.

.. code-block:: protobuf

   rpc ListUsers(ListUsersRequest) returns (stream User);

**Go Example:**

.. code-block:: go

   stream, err := client.ListUsers(ctx, &pb.ListUsersRequest{})
   if err != nil {
       log.Fatal(err)
   }

   for {
       user, err := stream.Recv()
       if err == io.EOF {
           break
       }
       if err != nil {
           log.Fatal(err)
       }
       log.Printf("User: %v", user)
   }

Client Streaming RPC
--------------------

Client streams multiple requests, server sends one response.

.. code-block:: protobuf

   rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchResult);

**Go Example:**

.. code-block:: go

   stream, err := client.BatchCreateUsers(ctx)
   if err != nil {
       log.Fatal(err)
   }

   users := []*pb.CreateUserRequest{/* ... */}
   for _, req := range users {
       if err := stream.Send(req); err != nil {
           log.Fatal(err)
       }
   }

   result, err := stream.CloseAndRecv()
   if err != nil {
       log.Fatal(err)
   }
   log.Printf("Batch result: %v", result)

Bidirectional Streaming RPC
----------------------------

Client and server both stream messages.

.. code-block:: protobuf

   rpc SyncUsers(stream UserUpdate) returns (stream UserUpdate);

**Go Example:**

.. code-block:: go

   stream, err := client.SyncUsers(ctx)
   if err != nil {
       log.Fatal(err)
   }

   waitc := make(chan struct{})

   // Receive goroutine
   go func() {
       for {
           update, err := stream.Recv()
           if err == io.EOF {
               close(waitc)
               return
           }
           if err != nil {
               log.Fatal(err)
           }
           log.Printf("Received update: %v", update)
       }
   }()

   // Send updates
   updates := []*pb.UserUpdate{/* ... */}
   for _, update := range updates {
       if err := stream.Send(update); err != nil {
           log.Fatal(err)
       }
   }
   stream.CloseSend()
   <-waitc
```

---

## Validation

Agent must validate documentation before completion:

### Protocol Buffer Compilation

```bash
# Install protoc compiler
# Download from: https://github.com/protocolbuffers/protobuf/releases

# Compile proto file
protoc --proto_path=api-specs --go_out=. api-specs/userservice.proto
```

**Expected output:** Successful compilation with no errors

### reStructuredText Validation

```bash
# Validate reST files
rstcheck docs/source/api-reference/grpc/*.rst
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

See working example: `02-examples/grpc-api-example/` (planned)

**Example includes:**
- Complete proto3 definition
- Full narrative documentation set
- Multi-language client examples
- Streaming examples

---

## Access Level Warning

Include at top of `00-index.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This gRPC API is for internal microservice communication only.
   Do not expose to external parties.
```

---

## Agent Checklist

Before marking gRPC API documentation complete, verify:

- [ ] Proto3 file compiles successfully
- [ ] All services documented with block comments
- [ ] All RPCs documented with behavior and errors
- [ ] All messages documented with field descriptions
- [ ] Client examples in 3+ languages provided
- [ ] Streaming patterns explained (if applicable)
- [ ] Authentication mechanism documented (mTLS, JWT)
- [ ] Error handling documented with status codes
- [ ] Access level warning included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Sentence structure varies naturally
- [ ] No AI clichés detected

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial gRPC API documentation canon
- Based on Protocol Buffers 3 standard
- Follows `_docs-canon.md` v4 specifications
