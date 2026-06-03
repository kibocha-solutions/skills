# REST API Security

**OWASP API Security Top 10 (2023): Multiple Categories**

## The Problem

REST APIs expose common vulnerabilities including improper versioning, lack of pagination, verbose error responses, insecure HTTP methods, and authentication/authorization flaws that attackers exploit to access unauthorized data or disrupt services.

## Why Critical

- **Widespread Use**: Most web services use REST
- **Public Exposure**: APIs directly accessible over internet
- **Business Logic**: APIs control critical business operations
- **Data Access**: APIs provide direct database access

**CVSS Score**: 7.0-9.0 (HIGH to CRITICAL)

---

## REST-Specific Vulnerabilities

### 1. API Versioning Security

**Problem:** Older API versions with vulnerabilities remain accessible

```
# Old version with vulnerability still accessible
GET /api/v1/users → SQL injection vulnerability
GET /api/v2/users → Patched

# Attacker uses old version
```

**Secure Implementation:**

```javascript
// [APPROVED] Force latest version, deprecate old
const express = require('express');
const app = express();

const CURRENT_VERSION = 'v3';
const SUPPORTED_VERSIONS = ['v2', 'v3'];
const DEPRECATED_VERSIONS = {
  'v1': { deprecated: true, sunset: '2024-01-01', message: 'Use v3' }
};

app.use('/api/:version/*', (req, res, next) => {
  const version = req.params.version;
  
  // Block unsupported versions
  if (!SUPPORTED_VERSIONS.includes(version) && !DEPRECATED_VERSIONS[version]) {
    return res.status(404).json({
      error: 'API version not found',
      current_version: CURRENT_VERSION
    });
  }
  
  // Warn about deprecated versions
  if (DEPRECATED_VERSIONS[version]) {
    const deprecation = DEPRECATED_VERSIONS[version];
    res.set('Deprecation', 'true');
    res.set('Sunset', deprecation.sunset);
    res.set('Link', `</api/${CURRENT_VERSION}>; rel="successor-version"`);
    
    // Optional: Block after sunset date
    if (new Date() > new Date(deprecation.sunset)) {
      return res.status(410).json({  // 410 Gone
        error: 'API version sunset',
        message: deprecation.message
      });
    }
  }
  
  next();
});
```

---

### 2. Pagination Requirements

**Problem:** Endpoints return unlimited results

```javascript
// VULNERABLE - Returns all users
GET /api/users → Returns 1 million users, crashes client

// Attacker requests:
GET /api/users → Dumps entire database
```

**Secure Implementation:**

```javascript
// [APPROVED] MANDATORY pagination
app.get('/api/users', async (req, res) => {
  const page = Math.max(1, parseInt(req.query.page) || 1);
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);  // Max 100
  const offset = (page - 1) * limit;
  
  const users = await User.findAndCountAll({ limit, offset });
  
  res.json({
    data: users.rows,
    pagination: {
      page,
      limit,
      total: users.count,
      pages: Math.ceil(users.count / limit),
      next: page < Math.ceil(users.count / limit) ? 
        `/api/users?page=${page + 1}&limit=${limit}` : null,
      prev: page > 1 ? 
        `/api/users?page=${page - 1}&limit=${limit}` : null
    }
  });
});
```

---

### 3. HTTP Method Security

**Problem:** Unsafe HTTP methods enabled

```
# Attacker discovers allowed methods
OPTIONS /api/users
Allow: GET, POST, PUT, DELETE, TRACE, OPTIONS

# TRACE can leak authentication headers
TRACE /api/users
→ Reflects request with Authorization header

# Unnecessary methods increase attack surface
```

**Secure Implementation:**

```javascript
// [APPROVED] Restrict HTTP methods
app.use((req, res, next) => {
  const allowedMethods = {
    '/api/users': ['GET', 'POST', 'OPTIONS'],
    '/api/users/:id': ['GET', 'PUT', 'DELETE', 'OPTIONS']
  };
  
  const route = req.route?.path || req.path;
  const allowed = allowedMethods[route] || ['OPTIONS'];
  
  // Disable TRACE globally
  if (req.method === 'TRACE') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  if (!allowed.includes(req.method)) {
    res.set('Allow', allowed.join(', '));
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  next();
});
```

```nginx
# [APPROVED] Nginx method restriction
location /api {
    limit_except GET POST PUT DELETE OPTIONS {
        deny all;
    }
    
    # Disable TRACE
    if ($request_method = TRACE) {
        return 405;
    }
}
```

---

### 4. Resource ID Enumeration

**Problem:** Sequential IDs leak information

```
GET /api/orders/1 → 200 OK
GET /api/orders/2 → 200 OK
GET /api/orders/3 → 200 OK

# Attacker iterates through all IDs
for (let id = 1; id < 1000000; id++) {
  fetch(`/api/orders/${id}`)
}

# Reveals: total orders, order patterns, business metrics
```

**Secure Implementation:**

```javascript
// [APPROVED] Use UUIDs instead of sequential IDs
const { v4: uuidv4 } = require('uuid');

// Database schema
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  total DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT NOW()
);

// API endpoint
app.get('/api/orders/:id', async (req, res) => {
  const orderId = req.params.id;
  
  // Validate UUID format
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(orderId)) {
    return res.status(400).json({ error: 'Invalid order ID' });
  }
  
  const order = await Order.findOne({
    where: { id: orderId, user_id: req.user.id }  // Authorization check
  });
  
  if (!order) {
    // Don't reveal if ID exists
    return res.status(404).json({ error: 'Order not found' });
  }
  
  res.json(order);
});
```

---

### 5. Content Type Validation

**Problem:** Accepting unexpected content types

```javascript
// VULNERABLE - Accepts any content type
app.post('/api/users', (req, res) => {
  // Expects JSON but might receive XML, form data, etc.
  const user = req.body;  // Parsing vulnerability
});

// Attacker sends:
Content-Type: application/xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<user><name>&xxe;</name></user>
```

**Secure Implementation:**

```javascript
// [APPROVED] Strict content type validation
app.use('/api', (req, res, next) => {
  if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
    const contentType = req.get('Content-Type') || '';
    
    if (!contentType.startsWith('application/json')) {
      return res.status(415).json({  // 415 Unsupported Media Type
        error: 'Content-Type must be application/json'
      });
    }
  }
  next();
});

app.use(express.json({
  limit: '1mb',
  strict: true,  // Only accept arrays and objects
  type: 'application/json'
}));
```

---

### 6. Response Filtering (Preventing Mass Assignment)

**Problem:** API returns more data than requested

```javascript
// VULNERABLE - Returns entire user object
GET /api/users/123
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "password_hash": "$2b$10$...",  // Leaked
  "ssn": "123-45-6789",           // Leaked
  "salary": 120000,                // Leaked
  "is_admin": true                 // Leaked
}
```

**Secure Implementation:**

```javascript
// [APPROVED] Response DTOs (Data Transfer Objects)
class UserResponseDTO {
  constructor(user) {
    this.id = user.id;
    this.name = user.name;
    this.email = user.email;
    this.created_at = user.created_at;
    // Explicitly exclude sensitive fields
  }
}

app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  // Only return safe fields
  res.json(new UserResponseDTO(user));
});
```

---

### 7. Idempotency for Critical Operations

**Problem:** Duplicate requests cause duplicate operations

```javascript
// VULNERABLE - No idempotency
POST /api/payments
{ "amount": 100, "account": "123" }

// Network glitch: Client retries
// Result: $200 charged instead of $100
```

**Secure Implementation:**

```javascript
// [APPROVED] Idempotency keys
const processedRequests = new Map();  // Use Redis in production

app.post('/api/payments', async (req, res) => {
  const idempotencyKey = req.get('Idempotency-Key');
  
  if (!idempotencyKey) {
    return res.status(400).json({
      error: 'Idempotency-Key header required for payments'
    });
  }
  
  // Check if already processed
  const cached = await redis.get(`idempotency:${idempotencyKey}`);
  if (cached) {
    return res.json(JSON.parse(cached));  // Return cached result
  }
  
  // Process payment
  const payment = await processPayment(req.body);
  
  // Cache result for 24 hours
  await redis.setex(
    `idempotency:${idempotencyKey}`,
    86400,
    JSON.stringify(payment)
  );
  
  res.status(201).json(payment);
});
```

---

### 8. API Documentation Security

**Problem:** Auto-generated docs leak sensitive endpoints

```yaml
# Swagger/OpenAPI exposes internal endpoints
GET /api/internal/admin/reset-database
GET /api/internal/debug/user-passwords
GET /api/v1-deprecated/vulnerable-endpoint
```

**Secure Implementation:**

```javascript
// [APPROVED] Separate public/internal docs
const swaggerUi = require('swagger-ui-express');
const publicSpec = require('./swagger-public.json');
const internalSpec = require('./swagger-internal.json');

// Public documentation
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(publicSpec));

// Internal documentation (authenticated)
app.use('/api-docs/internal', 
  requireAuthentication,
  requireRole('admin'),
  swaggerUi.serve,
  swaggerUi.setup(internalSpec)
);

// Exclude internal endpoints from public spec
const publicSpec = {
  ...fullSpec,
  paths: Object.keys(fullSpec.paths)
    .filter(path => !path.startsWith('/api/internal'))
    .reduce((obj, key) => {
      obj[key] = fullSpec.paths[key];
      return obj;
    }, {})
};
```

---

## REST Security Checklist

- [ ] API versioning strategy defined
- [ ] Old versions deprecated/sunset with timelines
- [ ] MANDATORY pagination on all list endpoints (max 100 items)
- [ ] HTTP methods restricted (disable TRACE)
- [ ] UUIDs used instead of sequential IDs
- [ ] Content-Type validation enforced
- [ ] Response DTOs prevent data leakage
- [ ] Idempotency keys for critical operations
- [ ] API documentation excludes internal endpoints
- [ ] Rate limiting per endpoint
- [ ] Authentication on all non-public endpoints
- [ ] Field-level authorization
- [ ] CORS properly configured
- [ ] Security headers configured (HSTS, CSP, etc.)
- [ ] Error messages generic (no stack traces)

---

## Testing REST API Security

```javascript
describe('REST API Security', () => {
  it('should enforce pagination limits', async () => {
    const response = await request(app)
      .get('/api/users?limit=10000');  // Attempt large limit
    
    expect(response.body.pagination.limit).toBeLessThanOrEqual(100);
  });
  
  it('should reject TRACE method', async () => {
    const response = await request(app)
      .trace('/api/users');
    
    expect(response.status).toBe(405);
  });
  
  it('should require valid content type', async () => {
    const response = await request(app)
      .post('/api/users')
      .set('Content-Type', 'application/xml')
      .send('<user><name>Test</name></user>');
    
    expect(response.status).toBe(415);
  });
  
  it('should implement idempotency', async () => {
    const idempotencyKey = 'test-key-123';
    
    // First request
    const response1 = await request(app)
      .post('/api/payments')
      .set('Idempotency-Key', idempotencyKey)
      .send({ amount: 100 });
    
    // Duplicate request
    const response2 = await request(app)
      .post('/api/payments')
      .set('Idempotency-Key', idempotencyKey)
      .send({ amount: 100 });
    
    // Should return same result
    expect(response1.body.id).toBe(response2.body.id);
    
    // Should only charge once
    const payments = await Payment.findAll({ where: { amount: 100 } });
    expect(payments.length).toBe(1);
  });
});
```

---

## References

- OWASP API Security Top 10 (2023)
- REST API Security Best Practices
- HTTP RFC 7231 (Method Definitions)
- Idempotency in RESTful APIs
- OpenAPI Security Schemes
