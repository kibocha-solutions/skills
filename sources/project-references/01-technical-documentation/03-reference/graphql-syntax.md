# GraphQL SDL Quick Reference

## Overview

GraphQL Schema Definition Language (SDL) defines the structure of a GraphQL API: types, queries, mutations, and subscriptions. It's the contract between client and server.

**Official Spec:** https://spec.graphql.org/  
**Format:** `.graphql` or `.gql` files

---

## Why GraphQL SDL

**Benefits:**
- Strongly typed schema
- Client requests exactly what it needs
- Single endpoint (vs REST multiple endpoints)
- Real-time subscriptions built-in
- Introspection for auto-documentation
- No over-fetching or under-fetching

---

## Basic Structure

```graphql
# Schema entry points
type Query {
  users: [User!]!
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}

type Subscription {
  userCreated: User!
}

# Object types
type User {
  id: ID!
  email: String!
  name: String!
  role: Role!
}

# Enums
enum Role {
  USER
  ADMIN
  SYSTEM_ADMIN
}

# Input types
input CreateUserInput {
  email: String!
  name: String!
  role: Role = USER
}
```

---

## Scalar Types

### Built-in Scalars

```graphql
# String
field: String

# Integer (32-bit signed)
field: Int

# Float (IEEE 754 double precision)
field: Float

# Boolean
field: Boolean

# ID (unique identifier, serialized as String)
field: ID
```

### Custom Scalars

```graphql
scalar DateTime
scalar Email
scalar URL
scalar JSON

type User {
  createdAt: DateTime!
  email: Email!
  website: URL
  metadata: JSON
}
```

**Implementation Example (Node.js):**

```javascript
const { GraphQLScalarType, Kind } = require('graphql');

const DateTimeScalar = new GraphQLScalarType({
  name: 'DateTime',
  description: 'ISO 8601 date-time string',
  serialize(value) {
    return value.toISOString(); // Send to client
  },
  parseValue(value) {
    return new Date(value); // From client variable
  },
  parseLiteral(ast) {
    if (ast.kind === Kind.STRING) {
      return new Date(ast.value); // From client query
    }
    return null;
  },
});
```

---

## Object Types

```graphql
type User {
  # Required field (!)
  id: ID!
  
  # Optional field
  email: String
  
  # Required string
  name: String!
  
  # Enum
  role: Role!
  
  # Nested object
  profile: Profile
  
  # List of strings (list and items can be null)
  tags: [String]
  
  # Non-null list (list cannot be null, but items can)
  tags: [String]!
  
  # List of non-null strings (items cannot be null, but list can)
  tags: [String!]
  
  # Non-null list of non-null strings (neither can be null)
  tags: [String!]!
  
  # Computed field with arguments
  calculations(limit: Int = 10): [Calculation!]!
}

type Profile {
  bio: String
  avatar: URL
}

type Calculation {
  id: ID!
  amount: Float!
  createdAt: DateTime!
}
```

---

## Enums

```graphql
enum Role {
  USER
  ADMIN
  SYSTEM_ADMIN
}

enum Status {
  ACTIVE
  INACTIVE
  PENDING
}

type User {
  role: Role!
  status: Status!
}
```

---

## Input Types

```graphql
# Input type (for mutations)
input CreateUserInput {
  email: String!
  name: String!
  role: Role = USER  # Default value
}

input UpdateUserInput {
  email: String
  name: String
  role: Role
}

input PaginationInput {
  page: Int = 1
  limit: Int = 20
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}
```

---

## Queries

```graphql
type Query {
  # Get single user
  user(id: ID!): User
  
  # Get list of users
  users: [User!]!
  
  # Pagination
  users(page: Int = 1, limit: Int = 20): UserConnection!
  
  # Filtering
  users(role: Role, status: Status): [User!]!
  
  # Search
  searchUsers(query: String!): [User!]!
  
  # Complex arguments
  calculations(
    userId: ID!
    startDate: DateTime
    endDate: DateTime
    limit: Int = 10
  ): [Calculation!]!
}

# Connection type (for pagination)
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## Mutations

```graphql
type Mutation {
  # Create
  createUser(input: CreateUserInput!): CreateUserPayload!
  
  # Update
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  
  # Delete
  deleteUser(id: ID!): DeleteUserPayload!
}

# Payload types (best practice - include errors)
type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type UpdateUserPayload {
  user: User
  errors: [UserError!]
}

type DeleteUserPayload {
  success: Boolean!
  errors: [UserError!]
}

type UserError {
  field: String
  message: String!
}
```

---

## Subscriptions

```graphql
type Subscription {
  # Real-time updates when user created
  userCreated: User!
  
  # With filtering
  userUpdated(id: ID!): User!
  
  # Calculation progress
  calculationProgress(id: ID!): CalculationProgress!
}

type CalculationProgress {
  id: ID!
  percentage: Int!
  status: String!
}
```

---

## Interfaces

```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  email: String!
  name: String!
}

type Calculation implements Node {
  id: ID!
  amount: Float!
}

type Query {
  # Return any type implementing Node
  node(id: ID!): Node
}
```

---

## Unions

```graphql
union SearchResult = User | Calculation | Receipt

type Query {
  search(query: String!): [SearchResult!]!
}

# Client query
query {
  search(query: "test") {
    ... on User {
      email
      name
    }
    ... on Calculation {
      amount
    }
    ... on Receipt {
      filename
    }
  }
}
```

---

## Directives

### Built-in Directives

```graphql
type User {
  # Skip field if condition true
  email: String @skip(if: Boolean!)
  
  # Include field if condition true
  name: String @include(if: Boolean!)
  
  # Mark field as deprecated
  oldField: String @deprecated(reason: "Use newField instead")
  newField: String
}
```

### Custom Directives

```graphql
# Define directive
directive @auth(requires: Role = USER) on FIELD_DEFINITION

type Query {
  # Require authentication
  me: User @auth
  
  # Require admin role
  allUsers: [User!]! @auth(requires: ADMIN)
}
```

---

## Schema Definition

```graphql
# Optional (default entry points)
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

# Required only if using custom names
schema {
  query: RootQuery
  mutation: RootMutation
}
```

---

## Descriptions (Documentation)

```graphql
"""
User account in the system.

Users can have different roles determining permissions.
"""
type User {
  "Unique user identifier (UUID)"
  id: ID!
  
  "User's email address (must be unique)"
  email: String!
  
  """
  User's display name.
  
  Must be between 1 and 100 characters.
  """
  name: String!
}
```

---

## Example Complete Schema

```graphql
"""
GraphQL API for Tax Management System
"""
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

# Custom Scalars
scalar DateTime
scalar Email

# Enums
enum Role {
  USER
  ADMIN
  SYSTEM_ADMIN
}

enum CalculationStatus {
  PENDING
  COMPLETED
  FAILED
}

# Object Types
type User {
  id: ID!
  email: Email!
  name: String!
  role: Role!
  createdAt: DateTime!
  calculations(limit: Int = 10): [Calculation!]!
}

type Calculation {
  id: ID!
  user: User!
  grossSalary: Float!
  taxAmount: Float!
  effectiveRate: Float!
  status: CalculationStatus!
  createdAt: DateTime!
}

# Input Types
input CreateUserInput {
  email: Email!
  name: String!
  role: Role = USER
}

input CalculateTaxInput {
  grossSalary: Float!
  allowances: Float = 0
  deductions: Float = 0
}

# Payload Types
type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type CalculateTaxPayload {
  calculation: Calculation
  errors: [CalculationError!]
}

type UserError {
  field: String
  message: String!
}

type CalculationError {
  message: String!
  code: String!
}

# Queries
type Query {
  "Get current authenticated user"
  me: User
  
  "Get user by ID"
  user(id: ID!): User
  
  "List all users (admin only)"
  users(page: Int = 1, limit: Int = 20): [User!]!
  
  "Get calculation by ID"
  calculation(id: ID!): Calculation
  
  "Search calculations"
  calculations(
    userId: ID
    status: CalculationStatus
    startDate: DateTime
    endDate: DateTime
  ): [Calculation!]!
}

# Mutations
type Mutation {
  "Create new user account"
  createUser(input: CreateUserInput!): CreateUserPayload!
  
  "Calculate tax"
  calculateTax(input: CalculateTaxInput!): CalculateTaxPayload!
  
  "Delete calculation"
  deleteCalculation(id: ID!): Boolean!
}

# Subscriptions
type Subscription {
  "Subscribe to calculation updates"
  calculationUpdated(id: ID!): Calculation!
}
```

---

## Client Queries (Examples)

### Simple Query

```graphql
query GetUser {
  user(id: "123") {
    id
    email
    name
  }
}
```

### With Variables

```graphql
query GetUser($userId: ID!) {
  user(id: $userId) {
    id
    email
    name
    role
  }
}

# Variables (JSON)
{
  "userId": "123"
}
```

### Nested Query

```graphql
query GetUserWithCalculations {
  user(id: "123") {
    id
    name
    calculations(limit: 5) {
      id
      taxAmount
      createdAt
    }
  }
}
```

### Mutation

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      email
      name
    }
    errors {
      field
      message
    }
  }
}

# Variables
{
  "input": {
    "email": "user@example.com",
    "name": "John Doe",
    "role": "USER"
  }
}
```

### Subscription

```graphql
subscription OnCalculationUpdated($id: ID!) {
  calculationUpdated(id: $id) {
    id
    status
    taxAmount
  }
}
```

---

## Validation

```bash
# Install graphql CLI
npm install -g graphql-cli

# Validate schema
graphql validate schema.graphql

# Or with graphql-js
npm install graphql

# validate.js
const { buildSchema } = require('graphql');
const fs = require('fs');

const schemaString = fs.readFileSync('schema.graphql', 'utf8');
try {
  buildSchema(schemaString);
  console.log('Schema valid!');
} catch (error) {
  console.error('Schema invalid:', error.message);
}
```

---

## Best Practices

1. **Use descriptions** (""") for all types and fields
2. **Nullable by default** - use `!` only when truly required
3. **Payload types for mutations** - include errors
4. **Use enums** for fixed value sets
5. **Custom scalars** for domain types (Email, DateTime)
6. **Pagination** with Connection pattern
7. **Versioning** via deprecation, not v2 APIs
8. **Keep schema flat** - avoid deep nesting

---

## Resources

- **GraphQL Spec:** https://spec.graphql.org/
- **GraphQL.org:** https://graphql.org/learn/
- **Apollo Docs:** https://www.apollographql.com/docs/
- **GraphQL Playground:** https://github.com/graphql/graphql-playground

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial GraphQL SDL quick reference
- Covers types, queries, mutations, subscriptions
