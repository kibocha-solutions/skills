# Canon: GraphQL API Documentation

## Purpose

GraphQL API documentation provides a complete reference for GraphQL-based APIs, enabling developers to query exactly the data they need. It combines machine-readable schema definitions with human-readable guides explaining query patterns, authentication, and best practices.

---

## Scope

**This canon applies to:**
- Public GraphQL APIs for third-party developers
- Internal GraphQL APIs for service-to-service communication
- APIs requiring flexible data fetching
- Real-time subscription requirements

**This canon does NOT apply to:**
- REST APIs (use `_rest-api-canon.md`)
- gRPC services (use `_grpc-api-canon.md`)
- Simple request-response patterns (prefer REST)

---

## Access Level Classification

**Public GraphQL APIs:**
- **Access Level:** Public (Level 1)
- **Distribution:** Third-party developers, end users, general public
- **Storage:** Public GitHub repository, GraphQL Playground publicly accessible
- **Review:** Standard technical review before publication

**Internal GraphQL APIs:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Internal teams, service-to-service communication only
- **Storage:** Private repository with authentication
- **Review:** Technical review, security clearance for sensitive queries

---

## When to Generate

### Initial Creation
- **Schema-First:** Before implementation (recommended for new APIs)
- **Code-First:** During development (acceptable when using code-generation tools)

### Updates
- Every schema change (new types, fields, queries, mutations, subscriptions)
- Automated via CI/CD pipeline
- Breaking changes trigger immediate documentation update

### Frequency
- **Continuous:** Part of development workflow
- **Pre-Release:** Complete schema review before version release
- **Post-Incident:** Document any security or breaking changes immediately

---

## Files to Generate

Agent must create the following files when documenting a GraphQL API:

### 1. GraphQL Schema (Machine-Readable Definition)
**File:** `/api-specs/schema.graphql`  
**Format:** GraphQL Schema Definition Language (SDL)  
**Purpose:** Machine-readable schema for validation, introspection, and tooling

### 2. API Reference Index (Entry Point)
**File:** `/docs/source/api-reference/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Documentation homepage linking to all API documentation sections

### 3. API Overview (Concepts and Philosophy)
**File:** `/docs/source/api-reference/01-overview.rst`  
**Format:** reStructuredText  
**Purpose:** Explain GraphQL design philosophy, conventions, and schema structure

### 4. Authentication Documentation
**File:** `/docs/source/api-reference/02-authentication.rst`  
**Format:** reStructuredText  
**Purpose:** Document authentication and authorization mechanisms

### 5. GraphQL Schema Documentation
**File:** `/docs/source/api-reference/graphql/01-schema.rst`  
**Format:** reStructuredText  
**Purpose:** Explain schema structure, types, and relationships

### 6. GraphQL Playground Guide
**File:** `/docs/source/api-reference/graphql/02-playground.rst`  
**Format:** reStructuredText  
**Purpose:** Guide users to GraphQL Playground for interactive exploration

### 7. Query Examples
**File:** `/docs/source/api-reference/graphql/03-queries.rst`  
**Format:** reStructuredText  
**Purpose:** Provide complete query examples with explanations

### 8. Mutation Examples
**File:** `/docs/source/api-reference/graphql/04-mutations.rst`  
**Format:** reStructuredText  
**Purpose:** Provide complete mutation examples with explanations

### 9. Subscription Examples
**File:** `/docs/source/api-reference/graphql/05-subscriptions.rst`  
**Format:** reStructuredText  
**Purpose:** Provide real-time subscription examples

### 10. Error Handling Documentation
**File:** `/docs/source/api-reference/04-errors.rst`  
**Format:** reStructuredText  
**Purpose:** Document GraphQL error responses and resolution

---

## Directory Structure

```
project-root/
│
├── api-specs/
│   └── schema.graphql                   # GraphQL schema definition
│
└── docs/source/api-reference/
    ├── 00-index.rst                     # API documentation entry point
    ├── 01-overview.rst                  # API concepts and philosophy
    ├── 02-authentication.rst            # Authentication mechanisms
    ├── 04-errors.rst                    # Error handling
    │
    └── graphql/
        ├── 00-index.rst                 # GraphQL API entry point
        ├── 01-schema.rst                # Schema documentation
        ├── 02-playground.rst            # GraphQL Playground guide
        ├── 03-queries.rst               # Query examples
        ├── 04-mutations.rst             # Mutation examples
        └── 05-subscriptions.rst         # Subscription examples
```

---

## Generation Rules

### GraphQL Schema Rules

1. **Use descriptive type names** (User, Product, Order, not T1, T2, T3)
2. **Document every type with triple-quote comments** (""")
3. **Document every field** with description
4. **Use non-nullable types judiciously** (! suffix)
5. **Define clear input types** for mutations
6. **Group related types** logically
7. **Use enums** for fixed value sets
8. **Implement interfaces** for shared fields
9. **Provide default values** where sensible
10. **Version with @deprecated directive** (not breaking changes)

### Narrative Documentation Rules

1. **Start with overview** explaining GraphQL benefits and schema structure
2. **Document authentication first** (HTTP headers, context, directives)
3. **Explain query structure** (fields, arguments, fragments)
4. **Provide runnable examples** (not pseudo-code)
5. **Include pagination patterns** (connections, cursors)
6. **Document error handling** (GraphQL errors vs HTTP errors)
7. **Link to GraphQL Playground** for interactive testing
8. **Show subscription lifecycle** (connect, subscribe, receive, unsubscribe)
9. **Document batching** if supported
10. **Include performance tips** (query complexity, depth limits)

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

### GraphQL Schema (`/api-specs/schema.graphql`)

**Required sections:**

```graphql
"""
[Service Name] GraphQL API

This API provides [brief description of purpose].
All monetary values are in [currency].
All timestamps are in ISO 8601 format.
"""

"""
Root query type for read operations
"""
type Query {
  """
  Fetch a single user by ID
  """
  user(
    """User ID (UUID format)"""
    id: ID!
  ): User
  
  """
  List all users with pagination
  """
  users(
    """Number of items to return (max 100)"""
    first: Int = 10
    
    """Cursor for pagination"""
    after: String
  ): UserConnection!
}

"""
Root mutation type for write operations
"""
type Mutation {
  """
  Create a new user
  """
  createUser(
    """User creation input"""
    input: CreateUserInput!
  ): CreateUserPayload!
}

"""
Root subscription type for real-time updates
"""
type Subscription {
  """
  Subscribe to user updates
  """
  userUpdated(
    """User ID to watch"""
    userId: ID!
  ): User!
}

"""
Represents a user in the system
"""
type User {
  """Unique identifier (UUID)"""
  id: ID!
  
  """User's email address"""
  email: String!
  
  """User's display name"""
  name: String!
  
  """Account creation timestamp"""
  createdAt: DateTime!
}

"""
Paginated list of users
"""
type UserConnection {
  """List of user nodes"""
  nodes: [User!]!
  
  """Pagination information"""
  pageInfo: PageInfo!
  
  """Total count of users"""
  totalCount: Int!
}

"""
Pagination metadata
"""
type PageInfo {
  """Cursor of the last item"""
  endCursor: String
  
  """Whether more items exist"""
  hasNextPage: Boolean!
}

"""
Input for creating a user
"""
input CreateUserInput {
  """User's email address"""
  email: String!
  
  """User's display name"""
  name: String!
}

"""
Payload returned after creating a user
"""
type CreateUserPayload {
  """The created user"""
  user: User!
  
  """Operation status"""
  success: Boolean!
}

"""
ISO 8601 datetime string
"""
scalar DateTime
```

### GraphQL Playground Guide (`/docs/source/api-reference/graphql/02-playground.rst`)

```rst
GraphQL Playground
==================

The GraphQL Playground provides an interactive environment for exploring the API.

Accessing the Playground
-------------------------

Visit: https://api.example.com/graphql

The Playground includes:

- Schema explorer (browse all types and fields)
- Query editor with autocomplete
- Documentation sidebar
- Query history

Writing Your First Query
-------------------------

Click "Docs" to explore the schema, then write a query:

.. code-block:: graphql

   query GetUser {
     user(id: "123") {
       id
       name
       email
       createdAt
     }
   }

Click the Play button to execute.

Authentication in Playground
-----------------------------

Add headers in the HTTP Headers panel:

.. code-block:: json

   {
     "Authorization": "Bearer YOUR_API_KEY"
   }

Introspection Queries
---------------------

The Playground uses introspection to build documentation.

Query the schema directly:

.. code-block:: graphql

   query {
     __schema {
       types {
         name
         description
       }
     }
   }
```

### Query Examples (`/docs/source/api-reference/graphql/03-queries.rst`)

```rst
Query Examples
==============

Examples demonstrate common query patterns.

Simple Field Selection
----------------------

Fetch specific fields:

.. code-block:: graphql

   query {
     user(id: "123") {
       id
       name
       email
     }
   }

Nested Queries
--------------

Fetch related data in one request:

.. code-block:: graphql

   query {
     user(id: "123") {
       id
       name
       posts {
         title
         publishedAt
       }
     }
   }

Query with Arguments
--------------------

Pass arguments to filter or paginate:

.. code-block:: graphql

   query {
     users(first: 10, after: "cursor123") {
       nodes {
         id
         name
       }
       pageInfo {
         endCursor
         hasNextPage
       }
     }
   }

Using Fragments
---------------

Reuse field sets with fragments:

.. code-block:: graphql

   fragment UserDetails on User {
     id
     name
     email
     createdAt
   }

   query {
     user(id: "123") {
       ...UserDetails
     }
   }

Using Variables
---------------

Pass dynamic values with variables:

.. code-block:: graphql

   query GetUser($userId: ID!) {
     user(id: $userId) {
       id
       name
     }
   }

Variables:

.. code-block:: json

   {
     "userId": "123"
   }
```

### Mutation Examples (`/docs/source/api-reference/graphql/04-mutations.rst`)

```rst
Mutation Examples
=================

Mutations modify data on the server.

Creating a Resource
-------------------

.. code-block:: graphql

   mutation CreateUser($input: CreateUserInput!) {
     createUser(input: $input) {
       user {
         id
         name
         email
       }
       success
     }
   }

Variables:

.. code-block:: json

   {
     "input": {
       "name": "Jane Doe",
       "email": "jane@example.com"
     }
   }

Updating a Resource
-------------------

.. code-block:: graphql

   mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
     updateUser(id: $id, input: $input) {
       user {
         id
         name
         email
       }
       success
     }
   }

Deleting a Resource
-------------------

.. code-block:: graphql

   mutation DeleteUser($id: ID!) {
     deleteUser(id: $id) {
       success
       deletedId
     }
   }

Multiple Mutations
------------------

Execute multiple mutations in one request:

.. code-block:: graphql

   mutation {
     user1: createUser(input: {name: "Alice", email: "alice@example.com"}) {
       user { id }
     }
     user2: createUser(input: {name: "Bob", email: "bob@example.com"}) {
       user { id }
     }
   }
```

### Subscription Examples (`/docs/source/api-reference/graphql/05-subscriptions.rst`)

```rst
Subscription Examples
=====================

Subscriptions enable real-time updates via WebSocket.

Basic Subscription
------------------

Subscribe to user updates:

.. code-block:: graphql

   subscription {
     userUpdated(userId: "123") {
       id
       name
       email
       updatedAt
     }
   }

When the user changes, the server pushes the new data.

JavaScript Client Example
--------------------------

Using Apollo Client:

.. code-block:: javascript

   import { ApolloClient, InMemoryCache, split, HttpLink } from '@apollo/client';
   import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
   import { createClient } from 'graphql-ws';
   import { getMainDefinition } from '@apollo/client/utilities';

   const httpLink = new HttpLink({
     uri: 'https://api.example.com/graphql'
   });

   const wsLink = new GraphQLWsLink(createClient({
     url: 'wss://api.example.com/graphql',
     connectionParams: {
       authToken: 'YOUR_API_KEY'
     }
   }));

   const splitLink = split(
     ({ query }) => {
       const definition = getMainDefinition(query);
       return (
         definition.kind === 'OperationDefinition' &&
         definition.operation === 'subscription'
       );
     },
     wsLink,
     httpLink,
   );

   const client = new ApolloClient({
     link: splitLink,
     cache: new InMemoryCache()
   });

   // Subscribe
   client.subscribe({
     query: gql`
       subscription {
         userUpdated(userId: "123") {
           id
           name
         }
       }
     `
   }).subscribe({
     next: (data) => console.log(data),
     error: (error) => console.error(error)
   });

Connection Lifecycle
--------------------

1. **Connect:** Client establishes WebSocket connection
2. **Authenticate:** Send auth token in connection params
3. **Subscribe:** Send subscription operation
4. **Receive:** Server pushes updates as they occur
5. **Unsubscribe:** Client cancels subscription
6. **Disconnect:** Close WebSocket connection
```

---

## Validation

Agent must validate documentation before completion:

### GraphQL Schema Validation

```bash
# Install graphql-cli
npm install -g graphql-cli

# Validate schema
graphql validate api-specs/schema.graphql
```

**Expected output:** Schema is valid

### reStructuredText Validation

```bash
# Validate reST files
rstcheck docs/source/api-reference/graphql/*.rst
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

See working example: `02-examples/graphql-api-example/`

**Example includes:**
- Complete GraphQL schema
- Full narrative documentation set
- Query examples
- Mutation examples
- Subscription examples with client code

---

## Access Level Warnings

### Public GraphQL API Documentation

Include at top of `00-index.rst`:

```rst
.. note::
   PUBLIC DOCUMENTATION - Level 1 Access
   This GraphQL API is publicly available.
```

### Internal GraphQL API Documentation

Include at top of `00-index.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This GraphQL API is for internal use only.
   Do not share with external parties.
```

---

## Agent Checklist

Before marking GraphQL API documentation complete, verify:

- [ ] GraphQL schema validates successfully
- [ ] All types documented with triple-quote comments
- [ ] Query examples provided and tested
- [ ] Mutation examples provided and tested
- [ ] Subscription examples provided (if applicable)
- [ ] Authentication mechanism explained
- [ ] Error handling documented
- [ ] GraphQL Playground link provided
- [ ] Access level warning included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present
- [ ] Sentence structure varies naturally
- [ ] No AI clichés detected

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial GraphQL API documentation canon
- Based on GraphQL SDL standard
- Follows `_docs-canon.md` v4 specifications
