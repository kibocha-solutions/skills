# Mass Assignment Prevention

**OWASP API Security Top 10 (2023): API03:2023 - Broken Object Property Level Authorization**

## The Problem

Mass assignment occurs when an application automatically binds user-supplied input to internal object properties without proper filtering, allowing attackers to modify object properties they should not have access to.

**Attack Scenario:**

```javascript
// User registration endpoint
POST /api/users/register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "SecurePass123",
  "isAdmin": true,              // Attacker adds this
  "accountBalance": 1000000,    // And this
  "emailVerified": true         // And this
}

// Vulnerable code automatically binds ALL fields
const user = new User(req.body);  // DANGER: Binds isAdmin, accountBalance, etc.
await user.save();

// Result: Alice is now an admin with $1M balance and verified email
```

## Why Critical

- **Privilege Escalation**: Users can grant themselves admin rights
- **Data Manipulation**: Modify sensitive fields (balance, permissions, status)
- **Business Logic Bypass**: Skip verification workflows
- **Account Takeover**: Modify email, password reset tokens

**CVSS Score**: 8.2 (HIGH to CRITICAL depending on exposed properties)

## Attack Vectors

### 1. User Registration

```json
POST /api/users/register
{
  "username": "attacker",
  "email": "attacker@example.com",
  "password": "password",
  "role": "admin",           // Escalation
  "verified": true,          // Skip email verification
  "credits": 999999          // Free credits
}
```

### 2. Profile Updates

```json
PUT /api/users/profile
{
  "name": "New Name",
  "userId": 999,             // Change to another user's ID
  "accountStatus": "premium", // Upgrade account
  "subscriptionEnds": "2099-12-31"
}
```

### 3. API Object Creation

```json
POST /api/products
{
  "name": "New Product",
  "price": 0.01,             // Set price to $0.01
  "approved": true,          // Auto-approve
  "featured": true,          // Feature the product
  "sellerId": 1              // Assign to different seller
}
```

### 4. Nested Object Manipulation

```json
PUT /api/orders/123
{
  "shippingAddress": {
    "street": "123 Main St",
    "city": "New York"
  },
  "payment": {
    "status": "paid",        // Mark as paid
    "amount": 0,             // Change amount to $0
    "method": "admin_override"
  }
}
```

---

## Prevention Strategies (Defense in Depth)

### Strategy 1: Explicit Allowlists (MANDATORY)

**Define exactly which fields users can modify:**

```javascript
// [APPROVED] Node.js/Express Example
const ALLOWED_USER_FIELDS = ['username', 'email', 'password', 'name'];

app.post('/api/users/register', async (req, res) => {
  // Extract ONLY allowed fields
  const userData = {};
  ALLOWED_USER_FIELDS.forEach(field => {
    if (req.body[field] !== undefined) {
      userData[field] = req.body[field];
    }
  });
  
  const user = new User(userData);
  await user.save();
});
```

```python
# [APPROVED] Python/Django Example
ALLOWED_USER_FIELDS = ['username', 'email', 'password', 'name']

def register_user(request):
    data = request.data
    
    # Filter to allowed fields only
    user_data = {k: v for k, v in data.items() if k in ALLOWED_USER_FIELDS}
    
    user = User.objects.create(**user_data)
    return Response({'id': user.id})
```

```rust
// [APPROVED] Rust Example
#[derive(Deserialize)]
struct UserRegistrationRequest {
    username: String,
    email: String,
    password: String,
    name: Option<String>,
    // ONLY these fields can be deserialized
}

async fn register_user(Json(payload): Json<UserRegistrationRequest>) -> Result<Json<User>, Error> {
    let user = User {
        username: payload.username,
        email: payload.email,
        password_hash: hash_password(&payload.password)?,
        name: payload.name,
        // Internal fields set explicitly
        is_admin: false,
        account_status: AccountStatus::Pending,
        created_at: Utc::now(),
    };
    
    user.save().await?;
    Ok(Json(user))
}
```

---

### Strategy 2: DTOs (Data Transfer Objects)

**Use separate classes for input vs internal representation:**

```typescript
// [APPROVED] TypeScript Example

// DTO for user input
class CreateUserDTO {
  @IsString()
  @MinLength(3)
  username: string;
  
  @IsEmail()
  email: string;
  
  @IsString()
  @MinLength(8)
  password: string;
  
  // ONLY these fields exposed for input
}

// Internal User entity
class User {
  id: number;
  username: string;
  email: string;
  passwordHash: string;
  isAdmin: boolean;        // NOT in DTO
  accountBalance: number;  // NOT in DTO
  emailVerified: boolean;  // NOT in DTO
  createdAt: Date;
}

// Controller
async function register(createUserDTO: CreateUserDTO): Promise<User> {
  const user = new User();
  user.username = createUserDTO.username;
  user.email = createUserDTO.email;
  user.passwordHash = await hash(createUserDTO.password);
  
  // Set internal fields explicitly
  user.isAdmin = false;
  user.accountBalance = 0;
  user.emailVerified = false;
  user.createdAt = new Date();
  
  await user.save();
  return user;
}
```

---

### Strategy 3: ORM/Framework Protections

**Leverage built-in mass assignment protection:**

```ruby
# [APPROVED] Ruby on Rails Example
class User < ApplicationRecord
  # Strong parameters - only these can be mass-assigned
  def self.user_params(params)
    params.permit(:username, :email, :password, :password_confirmation)
  end
end

# Controller
def create
  @user = User.new(User.user_params(params))
  
  # Internal fields set explicitly
  @user.is_admin = false
  @user.account_status = 'pending'
  
  @user.save
end
```

```php
// [APPROVED] Laravel Example
class User extends Model
{
    // Fillable: ONLY these can be mass-assigned
    protected $fillable = ['username', 'email', 'password', 'name'];
    
    // Guarded: These CANNOT be mass-assigned
    protected $guarded = ['is_admin', 'account_balance', 'verified'];
}

// Controller
public function register(Request $request)
{
    $user = User::create($request->only('username', 'email', 'password'));
    
    // Internal fields set explicitly
    $user->is_admin = false;
    $user->account_balance = 0;
    $user->save();
}
```

---

### Strategy 4: JSON Schema Validation

**Validate and filter incoming JSON:**

```javascript
// [APPROVED] JSON Schema Example
const userRegistrationSchema = {
  type: 'object',
  properties: {
    username: { type: 'string', minLength: 3, maxLength: 30 },
    email: { type: 'string', format: 'email' },
    password: { type: 'string', minLength: 8 },
    name: { type: 'string', maxLength: 100 }
  },
  required: ['username', 'email', 'password'],
  additionalProperties: false  // CRITICAL: Reject unknown properties
};

const Ajv = require('ajv');
const ajv = new Ajv();
const validate = ajv.compile(userRegistrationSchema);

app.post('/api/users/register', (req, res) => {
  if (!validate(req.body)) {
    return res.status(400).json({ errors: validate.errors });
  }
  
  // Now safe to use req.body
  const user = new User(req.body);
  user.save();
});
```

---

### Strategy 5: Separate Read/Write Models

**Different models for input vs output:**

```csharp
// [APPROVED] C# Example

// Input model - what users can send
public class CreateUserRequest
{
    [Required, MinLength(3)]
    public string Username { get; set; }
    
    [Required, EmailAddress]
    public string Email { get; set; }
    
    [Required, MinLength(8)]
    public string Password { get; set; }
}

// Database entity - internal representation
public class User
{
    public int Id { get; set; }
    public string Username { get; set; }
    public string Email { get; set; }
    public string PasswordHash { get; set; }
    public bool IsAdmin { get; set; }
    public decimal AccountBalance { get; set; }
    public bool EmailVerified { get; set; }
    public DateTime CreatedAt { get; set; }
}

// Controller
[HttpPost("/api/users/register")]
public async Task<IActionResult> Register([FromBody] CreateUserRequest request)
{
    var user = new User
    {
        Username = request.Username,
        Email = request.Email,
        PasswordHash = HashPassword(request.Password),
        
        // Internal fields set explicitly
        IsAdmin = false,
        AccountBalance = 0,
        EmailVerified = false,
        CreatedAt = DateTime.UtcNow
    };
    
    await _context.Users.AddAsync(user);
    await _context.SaveChangesAsync();
    
    return Ok(new { user.Id });
}
```

---

## Role-Based Field Access

**Different allowlists for different roles:**

```javascript
// [APPROVED] Role-based filtering
const FIELD_PERMISSIONS = {
  user: ['name', 'email', 'phoneNumber'],
  moderator: ['name', 'email', 'phoneNumber', 'bio', 'avatar'],
  admin: ['name', 'email', 'phoneNumber', 'bio', 'avatar', 'role', 'status']
};

function getAllowedFields(userRole) {
  return FIELD_PERMISSIONS[userRole] || FIELD_PERMISSIONS.user;
}

app.put('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  
  // Verify user can modify this profile
  if (user.id !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  // Get allowed fields for user's role
  const allowedFields = getAllowedFields(req.user.role);
  
  // Filter update data
  const updateData = {};
  allowedFields.forEach(field => {
    if (req.body[field] !== undefined) {
      updateData[field] = req.body[field];
    }
  });
  
  await user.update(updateData);
  res.json(user);
});
```

---

## Common Vulnerable Patterns

### ❌ REJECTED: Direct binding

```javascript
// VULNERABLE
app.post('/api/users', (req, res) => {
  const user = new User(req.body);  // Binds ALL fields
  user.save();
});
```

### ❌ REJECTED: Spread operator without filtering

```javascript
// VULNERABLE
app.put('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  Object.assign(user, req.body);  // Overwrites ALL properties
  await user.save();
});
```

### ❌ REJECTED: Framework auto-binding

```python
# VULNERABLE
def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    
    # Auto-updates ALL fields from request
    for key, value in request.data.items():
        setattr(user, key, value)
    
    user.save()
```

---

## Testing for Mass Assignment

**Security test cases:**

```javascript
describe('Mass Assignment Protection', () => {
  it('should reject admin field in user registration', async () => {
    const response = await request(app)
      .post('/api/users/register')
      .send({
        username: 'attacker',
        email: 'attacker@example.com',
        password: 'password',
        isAdmin: true          // Attempt escalation
      });
    
    expect(response.status).toBe(201);
    
    // Verify user was created but NOT as admin
    const user = await User.findOne({ username: 'attacker' });
    expect(user.isAdmin).toBe(false);
  });
  
  it('should reject account balance manipulation', async () => {
    const user = await createTestUser();
    
    const response = await request(app)
      .put(`/api/users/${user.id}`)
      .set('Authorization', `Bearer ${user.token}`)
      .send({
        name: 'New Name',
        accountBalance: 1000000  // Attempt to add money
      });
    
    const updatedUser = await User.findById(user.id);
    expect(updatedUser.name).toBe('New Name');
    expect(updatedUser.accountBalance).toBe(0);  // Unchanged
  });
  
  it('should allow admins to modify role field', async () => {
    const admin = await createAdminUser();
    const user = await createTestUser();
    
    const response = await request(app)
      .put(`/api/users/${user.id}`)
      .set('Authorization', `Bearer ${admin.token}`)
      .send({
        role: 'moderator'
      });
    
    expect(response.status).toBe(200);
    
    const updatedUser = await User.findById(user.id);
    expect(updatedUser.role).toBe('moderator');
  });
});
```

---

## Verification Checklist

- [ ] Explicit allowlists defined for all user input endpoints
- [ ] DTOs separate input models from internal entities
- [ ] ORM/framework mass assignment protection enabled
- [ ] JSON schema validation rejects unknown properties
- [ ] Role-based field access control implemented
- [ ] Internal fields (ID, role, balance, status) never user-controllable
- [ ] Automated tests verify mass assignment protection
- [ ] Code review checks for direct object binding patterns
- [ ] API documentation specifies allowed fields per role

---

## Real-World Examples

**GitHub (2012)**: Mass assignment vulnerability allowed attackers to add themselves as collaborators to any public repository by sending `public_keys[][key]` in a POST request.

**Ruby on Rails**: Framework historically auto-bound all parameters until `attr_accessible` (allowlist) became mandatory in Rails 3.

---

## References

- OWASP API Security Top 10 (2023): API03:2023
- CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
- OWASP Mass Assignment Cheat Sheet
- NIST SP 800-53: SI-10 (Information Input Validation)
