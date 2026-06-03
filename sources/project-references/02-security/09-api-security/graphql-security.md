# GraphQL Security

**OWASP API Security Top 10 (2023): Multiple Categories**

## The Problem

GraphQL's flexible query language provides powerful capabilities but introduces unique security challenges including introspection attacks, batch query abuse, query depth exploitation, and schema manipulation that don't exist in traditional REST APIs.

## Why Critical

- **Information Disclosure**: Schema introspection exposes entire data model
- **Denial of Service**: Deep nested queries or batch requests exhaust resources
- **Authorization Bypass**: Field-level access control often overlooked
- **Data Exposure**: Single query can retrieve entire database

**CVSS Score**: 7.0-9.0 (HIGH to CRITICAL)

---

## GraphQL-Specific Vulnerabilities

### 1. Introspection Attacks

**Problem:** GraphQL introspection reveals entire schema to attackers

```graphql
# Attacker query to dump entire schema
query IntrospectionQuery {
  __schema {
    types {
      name
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}

# Response reveals:
# - All types (User, Admin, InternalConfig)
# - All fields (password_hash, ssn, api_key)
# - Relationships
# - Hidden/internal APIs
```

**Secure Implementation:**

```javascript
// [APPROVED] Disable introspection in production
const { ApolloServer } = require('apollo-server');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',  // Only in dev
  playground: process.env.NODE_ENV !== 'production'      // Only in dev
});
```

```python
# [APPROVED] Python with Graphene
import graphene
from graphene import ObjectType, Schema

schema = Schema(
    query=Query,
    auto_camelcase=False
)

# Disable introspection
from graphql import validate, IntrospectionQuery

def is_introspection_query(query):
    return '__schema' in query or '__type' in query

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    query = data.get('query', '')
    
    # Block introspection in production
    if is_introspection_query(query) and os.getenv('ENV') == 'production':
        return jsonify({'errors': [{'message': 'Introspection disabled'}]}), 400
    
    result = schema.execute(query)
    return jsonify(result.data)
```

---

### 2. Query Depth Attacks

**Problem:** Nested queries cause exponential resource consumption

```graphql
# Attacker sends deeply nested query
query DeeplyNested {
  user(id: 1) {
    posts {
      comments {
        author {
          posts {
            comments {
              author {
                posts {
                  comments {
                    # ... nested 100 levels deep
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

# Result: Database executes thousands of queries, server crashes
```

**Secure Implementation:**

```javascript
// [APPROVED] Limit query depth
const depthLimit = require('graphql-depth-limit');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)]  // Max 7 levels deep
});
```

```python
# [APPROVED] Python depth limit
from graphql import GraphQLError

MAX_DEPTH = 7

def depth_limit_validator(max_depth):
    def validate(context, node, ancestors):
        if len(ancestors) > max_depth:
            raise GraphQLError(f'Query exceeds max depth of {max_depth}')
    return validate

schema = Schema(
    query=Query,
    validation_rules=[depth_limit_validator(MAX_DEPTH)]
)
```

---

### 3. Batch Query Attacks

**Problem:** Multiple queries in single request

```graphql
# Attacker sends 10,000 queries in one request
[
  { "query": "{ users { id name email } }" },
  { "query": "{ users { id name email } }" },
  { "query": "{ users { id name email } }" },
  # ... repeated 10,000 times
]

# Server processes all, exhausts resources
```

**Secure Implementation:**

```javascript
// [APPROVED] Limit batched queries
const { ApolloServer } = require('apollo-server-express');

app.use('/graphql', (req, res, next) => {
  if (Array.isArray(req.body)) {
    const MAX_BATCH_SIZE = 10;
    if (req.body.length > MAX_BATCH_SIZE) {
      return res.status(400).json({
        errors: [{ message: `Batch size exceeds limit of ${MAX_BATCH_SIZE}` }]
      });
    }
  }
  next();
});
```

---

### 4. Query Complexity/Cost Analysis

**Problem:** Expensive queries bypass depth limits

```graphql
# Query is shallow but expensive
query ExpensiveQuery {
  users(first: 10000) {  # Request 10,000 users
    posts(first: 1000) {  # 1,000 posts each = 10M posts total
      id
      title
    }
  }
}
```

**Secure Implementation:**

```javascript
// [APPROVED] Query cost analysis
const { createComplexityLimitRule } = require('graphql-validation-complexity');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 10,
      listFactor: 10
    })
  ]
});
```

```javascript
// [APPROVED] Custom cost calculator
const costAnalysis = require('graphql-cost-analysis').default;

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    costAnalysis({
      maximumCost: 1000,
      defaultCost: 1,
      variables: {},
      onComplete: (cost) => {
        console.log(`Query cost: ${cost}`);
      }
    })
  ]
});
```

---

### 5. Field-Level Authorization

**Problem:** Checking entity access but not field access

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  ssn: String!          # Sensitive - only user can see own
  salary: Float!        # Sensitive - only HR can see
  password_hash: String # Should NEVER be exposed
}

# Attacker queries:
query {
  user(id: 123) {
    ssn            # Gets victim's SSN
    salary         # Gets victim's salary
    password_hash  # Gets password hash
  }
}
```

**Secure Implementation:**

```javascript
// [APPROVED] Field-level authorization
const { shield, rule } = require('graphql-shield');

const isAuthenticated = rule()(async (parent, args, ctx) => {
  return ctx.user !== null;
});

const isOwner = rule()(async (parent, args, ctx) => {
  return parent.id === ctx.user.id;
});

const isHR = rule()(async (parent, args, ctx) => {
  return ctx.user.role === 'hr';
});

const permissions = shield({
  User: {
    id: isAuthenticated,
    name: isAuthenticated,
    email: isOwner,           // Only owner can see email
    ssn: isOwner,             // Only owner can see SSN
    salary: isHR,             // Only HR can see salary
    password_hash: shield.deny  // NEVER expose
  }
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    user: getUserFromToken(req.headers.authorization)
  }),
  schema: applyMiddleware(schema, permissions)
});
```

```python
# [APPROVED] Python field-level auth
from graphene import ObjectType, String, Field

class User(ObjectType):
    id = String()
    name = String()
    email = String()
    ssn = String()
    
    def resolve_ssn(self, info):
        # Field-level authorization
        current_user = info.context.user
        if not current_user or current_user.id != self.id:
            raise PermissionError('Cannot access SSN')
        return self.ssn
```

---

### 6. Mutation Rate Limiting

**Problem:** Mutations not rate-limited separately

```graphql
# Attacker sends 1000 mutations
mutation {
  createPost(title: "Spam", body: "Spam content")
  createPost(title: "Spam", body: "Spam content")
  # ... repeated 1000 times
}
```

**Secure Implementation:**

```javascript
// [APPROVED] Mutation-specific rate limiting
const rateLimit = require('express-rate-limit');

const mutationLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // 100 mutations per window
  skip: (req) => {
    // Only apply to mutations
    const query = req.body.query || '';
    return !query.trim().startsWith('mutation');
  },
  message: 'Too many mutations, please try again later'
});

app.use('/graphql', mutationLimiter);
```

---

### 7. N+1 Query Problem (Performance & DoS)

**Problem:** Inefficient resolvers cause database flooding

```graphql
query {
  users {  # 1 query: SELECT * FROM users
    posts {  # N queries: SELECT * FROM posts WHERE user_id = ?
      # If 1000 users → 1000 additional queries
    }
  }
}

# Result: 1 + 1000 = 1001 database queries
```

**Secure Implementation:**

```javascript
// [APPROVED] DataLoader for batching
const DataLoader = require('dataloader');

const postLoader = new DataLoader(async (userIds) => {
  // Batch load all posts for all users in single query
  const posts = await Post.findAll({
    where: { userId: { $in: userIds } }
  });
  
  // Group by user
  const postsByUser = {};
  posts.forEach(post => {
    if (!postsByUser[post.userId]) postsByUser[post.userId] = [];
    postsByUser[post.userId].push(post);
  });
  
  // Return in same order as userIds
  return userIds.map(id => postsByUser[id] || []);
});

const resolvers = {
  User: {
    posts: (user, args, context) => {
      return context.postLoader.load(user.id);
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    postLoader: new DataLoader(batchLoadPosts)
  })
});
```

---

## GraphQL Security Checklist

- [ ] Introspection disabled in production
- [ ] GraphQL Playground disabled in production
- [ ] Query depth limited (max 7-10 levels)
- [ ] Query complexity/cost analysis enabled
- [ ] Batch query limit enforced (max 10)
- [ ] Field-level authorization implemented
- [ ] Mutations rate-limited separately
- [ ] DataLoader implemented to prevent N+1 queries
- [ ] Timeout limits on resolvers (max 30s)
- [ ] Input validation on all arguments
- [ ] Pagination required for lists (no unlimited results)
- [ ] Sensitive fields (password_hash) never exposed
- [ ] Error messages generic (no stack traces)
- [ ] Query logging enabled
- [ ] Automated tests for authorization bypass

---

## Testing GraphQL Security

```javascript
describe('GraphQL Security', () => {
  it('should deny introspection in production', async () => {
    process.env.NODE_ENV = 'production';
    
    const response = await request(app)
      .post('/graphql')
      .send({
        query: '{ __schema { types { name } } }'
      });
    
    expect(response.body.errors).toBeDefined();
    expect(response.body.errors[0].message).toMatch(/introspection/i);
  });
  
  it('should reject deeply nested queries', async () => {
    const deepQuery = `
      query {
        user { posts { comments { author { posts { comments { author {
          posts { comments { author { posts { comments { id } } } } }
        } } } } } }
      }
    `;
    
    const response = await request(app)
      .post('/graphql')
      .send({ query: deepQuery });
    
    expect(response.body.errors[0].message).toMatch(/depth/i);
  });
  
  it('should enforce field-level authorization', async () => {
    const unauthorizedQuery = `
      query {
        user(id: "other-user-id") {
          ssn
        }
      }
    `;
    
    const response = await request(app)
      .post('/graphql')
      .set('Authorization', `Bearer ${userToken}`)
      .send({ query: unauthorizedQuery });
    
    expect(response.body.errors[0].message).toMatch(/permission|forbidden/i);
  });
});
```

---

## References

- OWASP GraphQL Cheat Sheet
- GraphQL Security Best Practices
- graphql-shield (authorization)
- graphql-depth-limit
- graphql-cost-analysis
- DataLoader (N+1 prevention)
