# OpenAPI 3.0 Quick Reference

## Overview

OpenAPI Specification (formerly Swagger) is a standard for describing REST APIs. It's machine-readable and generates interactive documentation, client SDKs, and server stubs.

**Current Version:** OpenAPI 3.0.3 (use this, not 2.0/Swagger)  
**Official Spec:** https://spec.openapis.org/oas/v3.0.3  
**Format:** YAML (preferred) or JSON

---

## Why OpenAPI

**Benefits:**
- Machine-readable API contract
- Generates interactive documentation (Swagger UI, Redoc)
- Validates API implementation against spec
- Generates client SDKs automatically
- Single source of truth for API
- CI/CD integration

---

## Basic Structure

```yaml
openapi: 3.0.3
info:
  title: Service Name API
  version: 1.0.0
  description: API description
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://sandbox.example.com/v1
    description: Sandbox

paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
```

---

## Info Object

```yaml
info:
  title: Tax Management System API
  version: 2.5.0
  description: |
    RESTful API for calculating taxes and managing receipts.
    
    ## Authentication
    All endpoints require Bearer token authentication.
    
    ## Rate Limits
    100 requests per minute per user.
    
  termsOf Service: https://example.com/terms
  contact:
    name: API Support Team
    url: https://support.example.com
    email: api@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
```

---

## Servers

```yaml
servers:
  - url: https://api.example.com/v1
    description: Production server
    variables:
      version:
        default: v1
        enum:
          - v1
          - v2
  
  - url: https://sandbox.example.com/v1
    description: Sandbox for testing
  
  - url: http://localhost:3000
    description: Local development
```

---

## Paths (Endpoints)

### GET Request

```yaml
paths:
  /users/{userId}:
    get:
      summary: Get user by ID
      description: Returns a single user by their unique identifier
      operationId: getUserById
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          description: User's unique ID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
```

### POST Request

```yaml
  /users:
    post:
      summary: Create new user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid input
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
```

### PUT Request

```yaml
  /users/{userId}:
    put:
      summary: Update user
      operationId: updateUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      responses:
        '200':
          description: User updated
```

### DELETE Request

```yaml
  /users/{userId}:
    delete:
      summary: Delete user
      operationId: deleteUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: User deleted
        '404':
          description: User not found
```

---

## Parameters

### Path Parameters

```yaml
parameters:
  - name: userId
    in: path
    required: true  # Path params always required
    description: User's unique identifier
    schema:
      type: string
      format: uuid
```

### Query Parameters

```yaml
parameters:
  - name: page
    in: query
    required: false
    description: Page number (starts at 1)
    schema:
      type: integer
      minimum: 1
      default: 1
  
  - name: limit
    in: query
    required: false
    description: Items per page
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
  
  - name: status
    in: query
    description: Filter by status
    schema:
      type: string
      enum:
        - active
        - inactive
        - pending
```

### Header Parameters

```yaml
parameters:
  - name: X-API-Key
    in: header
    required: true
    description: API key for authentication
    schema:
      type: string
```

---

## Request Body

```yaml
requestBody:
  required: true
  description: User details
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/UserRequest'
      examples:
        basic:
          summary: Basic user
          value:
            email: user@example.com
            name: John Doe
        admin:
          summary: Admin user
          value:
            email: admin@example.com
            name: Admin User
            role: admin
```

---

## Responses

### Success Response

```yaml
responses:
  '200':
    description: Successful operation
    headers:
      X-RateLimit-Limit:
        description: Request limit per hour
        schema:
          type: integer
      X-RateLimit-Remaining:
        description: Requests remaining
        schema:
          type: integer
    content:
      application/json:
        schema:
          type: array
          items:
            $ref: '#/components/schemas/User'
```

### Error Response

```yaml
responses:
  '400':
    description: Bad request
    content:
      application/json:
        schema:
          type: object
          properties:
            error:
              type: string
              example: invalid_input
            message:
              type: string
              example: Email address is invalid
            field:
              type: string
              example: email
```

---

## Components

### Schemas

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          format: uuid
          description: Unique user identifier
          example: 550e8400-e29b-41d4-a716-446655440000
        email:
          type: string
          format: email
          description: User's email address
          example: user@example.com
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: User's display name
          example: John Doe
        role:
          type: string
          enum:
            - user
            - admin
            - system_admin
          default: user
          description: User's role
        createdAt:
          type: string
          format: date-time
          description: Account creation timestamp
          example: 2025-12-29T10:00:00Z
    
    UserRequest:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [user, admin]
          default: user
    
    Error:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Error code
        message:
          type: string
          description: Human-readable error message
        field:
          type: string
          description: Field that caused error (if applicable)
```

### Data Types

```yaml
# String
type: string
minLength: 1
maxLength: 255
pattern: '^[a-zA-Z0-9]+$'

# String with format
type: string
format: email        # email@example.com
format: date         # 2025-12-29
format: date-time    # 2025-12-29T10:00:00Z
format: uuid         # 550e8400-e29b-41d4-a716-446655440000
format: uri          # https://example.com
format: hostname     # api.example.com

# Number
type: integer
minimum: 0
maximum: 100
multipleOf: 5

# Number (decimal)
type: number
minimum: 0.0
exclusiveMinimum: true  # > 0.0 (not including 0)

# Boolean
type: boolean

# Array
type: array
items:
  type: string
minItems: 1
maxItems: 10
uniqueItems: true

# Object
type: object
required: [name, email]
properties:
  name:
    type: string
  email:
    type: string

# Enum
type: string
enum:
  - active
  - inactive
  - pending

# Nullable
type: string
nullable: true

# AllOf (combine schemas)
allOf:
  - $ref: '#/components/schemas/Base'
  - type: object
    properties:
      additionalField:
        type: string

# OneOf (one of several schemas)
oneOf:
  - $ref: '#/components/schemas/Cat'
  - $ref: '#/components/schemas/Dog'

# AnyOf (one or more schemas)
anyOf:
  - type: string
  - type: number
```

---

## Security

### Bearer Token (JWT)

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

# Apply globally
security:
  - bearerAuth: []

# Or per endpoint
paths:
  /users:
    get:
      security:
        - bearerAuth: []
```

### API Key

```yaml
components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
    
    queryApiKey:
      type: apiKey
      in: query
      name: api_key

security:
  - apiKey: []
```

### OAuth 2.0

```yaml
components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes:
            read:users: Read user data
            write:users: Modify user data
```

---

## Tags

```yaml
tags:
  - name: Users
    description: User management operations
  - name: Authentication
    description: Authentication endpoints

paths:
  /users:
    get:
      tags:
        - Users
```

---

## Examples

```yaml
components:
  examples:
    UserExample:
      summary: Example user
      value:
        id: "550e8400-e29b-41d4-a716-446655440000"
        email: "user@example.com"
        name: "John Doe"
        role: "user"

# Use in responses
responses:
  '200':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
        examples:
          user:
            $ref: '#/components/examples/UserExample'
```

---

## Reusable Components

### Parameters

```yaml
components:
  parameters:
    UserId:
      name: userId
      in: path
      required: true
      schema:
        type: string

paths:
  /users/{userId}:
    get:
      parameters:
        - $ref: '#/components/parameters/UserId'
```

### Responses

```yaml
components:
  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    Unauthorized:
      description: Authentication required

paths:
  /users/{userId}:
    get:
      responses:
        '404':
          $ref: '#/components/responses/NotFound'
```

---

## Validation

```bash
# Install swagger-cli
npm install -g @apidevtools/swagger-cli

# Validate spec
swagger-cli validate api-spec.yaml

# Bundle (resolve $refs into single file)
swagger-cli bundle api-spec.yaml -o bundled.yaml
```

---

## Interactive Documentation

### Swagger UI

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "api-spec.yaml",
      dom_id: '#swagger-ui',
    });
  </script>
</body>
</html>
```

### Redoc

```html
<!DOCTYPE html>
<html>
<body>
  <redoc spec-url="api-spec.yaml"></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

---

## Common Patterns

### Pagination

```yaml
parameters:
  - name: page
    in: query
    schema:
      type: integer
      default: 1
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
      maximum: 100

responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/User'
            pagination:
              type: object
              properties:
                currentPage:
                  type: integer
                totalPages:
                  type: integer
                totalItems:
                  type: integer
```

### File Upload

```yaml
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          file:
            type: string
            format: binary
          description:
            type: string
```

---

## Best Practices

1. **Use OpenAPI 3.0**, not 2.0 (Swagger)
2. **YAML over JSON** for readability
3. **Include examples** for all requests/responses
4. **Use $ref** for reusable components
5. **Provide operation IDs** for SDK generation
6. **Tag endpoints** for logical grouping
7. **Document errors** comprehensively
8. **Validate spec** before committing

---

## Resources

- **OpenAPI Spec:** https://spec.openapis.org/oas/v3.0.3
- **Swagger Editor:** https://editor.swagger.io/
- **Redoc:** https://github.com/Redocly/redoc
- **Swagger UI:** https://swagger.io/tools/swagger-ui/

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial OpenAPI 3.0 quick reference
- Covers essential syntax for REST API documentation
