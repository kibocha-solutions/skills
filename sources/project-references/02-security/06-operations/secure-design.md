# Secure Design Principles

**OWASP Top 10 2021: A04 - Insecure Design**

## The Problem

Insecure design refers to fundamental flaws in the application's architecture and threat modeling, rather than implementation bugs. It represents missing or ineffective security controls at the design phase.

**Key Difference:**
- **Insecure Implementation**: Coding bug (e.g., SQL injection due to string concatenation)
- **Insecure Design**: Missing security requirement (e.g., no rate limiting on password reset)

## Why Critical

- **Cannot be fixed by patches**: Requires architectural changes
- **Affects entire application**: System-wide vulnerability
- **Expensive to fix**: Requires redesign and refactoring
- **Bypasses other controls**: No amount of secure coding can fix bad design

**CVSS Score**: Varies (often 7.0-9.0 depending on the flaw)

---

## Common Insecure Design Patterns

### 1. Missing Rate Limiting

**Insecure Design:**

```
Login endpoint with no rate limiting
→ Attacker can brute force passwords unlimited times
```

**Secure Design:**

```python
# [APPROVED] Rate limiting integrated into design
from redis import Redis
import time

redis = Redis()

def check_rate_limit(ip_address, endpoint, max_requests=5, window=900):
    """Rate limit: 5 requests per 15 minutes"""
    key = f"ratelimit:{endpoint}:{ip_address}"
    current = int(time.time())
    window_start = current - window
    
    # Remove old requests
    redis.zremrangebyscore(key, 0, window_start)
    
    # Count requests in window
    request_count = redis.zcard(key)
    
    if request_count >= max_requests:
        return False
    
    # Add current request
    redis.zadd(key, {current: current})
    redis.expire(key, window)
    return True

@app.route('/api/login', methods=['POST'])
def login():
    if not check_rate_limit(request.remote_addr, 'login'):
        return jsonify({'error': 'Too many attempts'}), 429
    
    # Process login
```

---

### 2. Lack of Business Logic Validation

**Insecure Design:**

```
E-commerce system allows negative quantities
POST /api/cart/add { "product_id": 123, "quantity": -5 }
→ Attacker gets money back by "returning" items never purchased
```

**Secure Design:**

```python
# [APPROVED] Business logic validation
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    quantity = request.json.get('quantity')
    
    # Business rule validation
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be positive'}), 400
    
    if quantity > 100:
        return jsonify({'error': 'Quantity exceeds maximum (100)'}), 400
    
    product = Product.query.get(request.json['product_id'])
    
    if quantity > product.stock:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    # Add to cart
```

---

### 3. Insufficient Transaction Integrity

**Insecure Design:**

```
Money transfer lacks atomicity
1. Deduct from Account A
2. [Server crashes]
3. Add to Account B [NEVER EXECUTES]
→ Money disappears
```

**Secure Design:**

```python
# [APPROVED] Atomic transactions
from sqlalchemy.orm import Session

def transfer_money(from_account_id, to_account_id, amount):
    session = Session()
    
    try:
        # Begin transaction
        from_account = session.query(Account).filter_by(id=from_account_id).with_for_update().first()
        to_account = session.query(Account).filter_by(id=to_account_id).with_for_update().first()
        
        # Validate
        if from_account.balance < amount:
            raise InsufficientFunds()
        
        # Atomic operations
        from_account.balance -= amount
        to_account.balance += amount
        
        # Log transaction
        transaction = Transaction(
            from_account=from_account_id,
            to_account=to_account_id,
            amount=amount,
            timestamp=datetime.utcnow()
        )
        session.add(transaction)
        
        # Commit atomically (all or nothing)
        session.commit()
        
    except Exception as e:
        # Rollback on any error
        session.rollback()
        raise
    finally:
        session.close()
```

---

### 4. No Account Lockout Policy

**Insecure Design:**

```
Failed login attempts not tracked
→ Infinite password guessing
```

**Secure Design:**

```python
# [APPROVED] Account lockout after failed attempts
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    # Check if account locked
    lockout_key = f"lockout:{username}"
    if redis.get(lockout_key):
        lockout_until = redis.ttl(lockout_key)
        return jsonify({
            'error': 'Account locked',
            'retry_after': lockout_until
        }), 429
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.verify_password(password):
        # Increment failed attempts
        attempts_key = f"failed_attempts:{username}"
        attempts = redis.incr(attempts_key)
        redis.expire(attempts_key, 900)  # 15 minutes
        
        if attempts >= 5:
            # Lock account for 1 hour
            redis.setex(lockout_key, 3600, '1')
            redis.delete(attempts_key)
            
            return jsonify({'error': 'Account locked for 1 hour'}), 429
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Successful login - clear failed attempts
    redis.delete(attempts_key)
    return jsonify({'token': user.generate_token()})
```

---

## Secure Design Principles

### Principle 1: Defense in Depth

**Multiple layers of security:**

```
Layer 1: Firewall (network level)
Layer 2: WAF (application firewall)
Layer 3: Authentication (user verification)
Layer 4: Authorization (permission check)
Layer 5: Input validation (data validation)
Layer 6: Output encoding (XSS prevention)
Layer 7: Audit logging (detection)
```

**Example:**

```python
# [APPROVED] Multiple security layers
@app.route('/api/admin/users', methods=['GET'])
@require_authentication()          # Layer 1: Authentication
@require_role('admin')             # Layer 2: Authorization
@rate_limit(100, per='hour')       # Layer 3: Rate limiting
@validate_input()                  # Layer 4: Input validation
@audit_log()                       # Layer 5: Logging
def get_users():
    users = User.query.all()
    return jsonify([sanitize_output(u) for u in users])  # Layer 6: Output sanitization
```

---

### Principle 2: Fail Securely (Fail Closed)

**When errors occur, default to secure state:**

```python
# [REJECTED] Fail Open - Grants access on error
def check_permission(user, resource):
    try:
        return database.check_permission(user, resource)
    except:
        return True  # DANGEROUS: Error grants access

# [APPROVED] Fail Closed - Denies access on error
def check_permission(user, resource):
    try:
        return database.check_permission(user, resource)
    except Exception as e:
        logger.error(f'Permission check failed: {e}')
        return False  # SAFE: Error denies access
```

---

### Principle 3: Least Privilege

**Grant minimum necessary permissions:**

```sql
-- [REJECTED] Application user has full database access
GRANT ALL PRIVILEGES ON DATABASE myapp TO app_user;

-- [APPROVED] Application user has minimal permissions
GRANT SELECT, INSERT, UPDATE ON users TO app_user;
GRANT SELECT, INSERT ON orders TO app_user;
-- NO DELETE, NO ALTER, NO DROP
```

---

### Principle 4: Separation of Duties

**No single user can complete sensitive operations alone:**

```python
# [APPROVED] Dual approval for large transactions
class LargeTransaction:
    def __init__(self, amount, from_account, to_account):
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.status = 'pending'
        self.initiated_by = None
        self.approved_by = None
    
    def initiate(self, user):
        if self.amount < 10000:
            # Small transactions auto-approved
            self.execute()
        else:
            # Large transactions require approval
            self.initiated_by = user.id
            self.status = 'pending_approval'
    
    def approve(self, approver):
        if approver.id == self.initiated_by:
            raise ValueError('Cannot approve own transaction')
        
        if not approver.has_role('approver'):
            raise PermissionError('User cannot approve transactions')
        
        self.approved_by = approver.id
        self.status = 'approved'
        self.execute()
```

---

### Principle 5: Complete Mediation

**Check permissions on every access, not just once:**

```python
# [REJECTED] Check permission once at login
@app.route('/api/login')
def login():
    user = authenticate(username, password)
    session['is_admin'] = user.is_admin  # Stored in session
    return jsonify({'token': generate_token(user)})

@app.route('/api/admin/delete-user/<id>')
def delete_user(id):
    if not session.get('is_admin'):  # Checks cached value
        return jsonify({'error': 'Forbidden'}), 403
    User.delete(id)

# [APPROVED] Check permission on every request
@app.route('/api/admin/delete-user/<id>')
def delete_user(id):
    user = get_current_user()
    if not user.is_admin:  # Checks current database value
        return jsonify({'error': 'Forbidden'}), 403
    User.delete(id)
```

---

### Principle 6: Psychological Acceptability

**Security should be usable:**

```python
# [REJECTED] Security so complex users bypass it
# Password requirements: 20+ chars, 5 symbols, changed weekly
# Result: Users write passwords on sticky notes

# [APPROVED] Security that users will follow
# Password requirements: 12+ chars, MFA enabled
# Result: Users comply, security improved
```

---

## Threat Modeling in Design

**Before coding, model threats:**

### STRIDE Framework

```
Spoofing: Can attacker impersonate someone?
Tampering: Can attacker modify data?
Repudiation: Can attacker deny actions?
Information Disclosure: Can attacker access sensitive data?
Denial of Service: Can attacker disrupt service?
Elevation of Privilege: Can attacker gain unauthorized access?
```

**Example:**

```
Feature: Password Reset

STRIDE Analysis:
[S] Spoofing: Attacker requests reset for victim's email
    → Mitigation: Send reset link to registered email only

[T] Tampering: Attacker modifies reset token
    → Mitigation: Use cryptographically signed tokens

[R] Repudiation: User claims they didn't reset password
    → Mitigation: Log all reset requests with IP, timestamp

[I] Info Disclosure: Reset token leaked in logs
    → Mitigation: Don't log tokens, use token IDs

[D] DoS: Attacker floods reset endpoint
    → Mitigation: Rate limit to 3 requests/hour/email

[E] Privilege Escalation: Attacker resets admin password
    → Mitigation: Require additional verification for privileged accounts
```

---

## Security Requirements in User Stories

**Embed security in requirements:**

```
User Story (Bad):
"As a user, I want to reset my password"

User Story (Good):
"As a user, I want to reset my password securely, where:
- Reset link expires after 1 hour
- Reset link is single-use
- Old password is invalidated immediately
- All active sessions are terminated
- Account lockout after 3 failed reset attempts
- Email notification sent on successful reset
- Reset requests rate-limited to 3 per hour"
```

---

## Secure Architecture Patterns

### Microservices with Authentication Gateway

```
                [API Gateway]
                  |  (JWT validation, rate limiting)
                  |
        +---------+---------+
        |         |         |
   [Auth Service] |    [Business Service]
        |         |         |
   [User DB]  [Cache]   [Business DB]

Security enforced at gateway, not each service
```

### Database Per Service (Data Isolation)

```
Each microservice has its own database
→ No shared database access
→ Data breaches contained to single service
→ Clear ownership and access patterns
```

---

## Verification Checklist

- [ ] Threat modeling performed before development
- [ ] Security requirements defined in user stories
- [ ] Defense in depth strategy documented
- [ ] Fail-secure error handling designed
- [ ] Least privilege access controls defined
- [ ] Separation of duties for sensitive operations
- [ ] Rate limiting designed into all public endpoints
- [ ] Business logic validation specified
- [ ] Transaction integrity ensured (ACID properties)
- [ ] Complete mediation (permission checks on every access)
- [ ] Security review of architecture diagrams
- [ ] Abuse case analysis completed

---

## Real-World Examples

**Twitter (2020)**: Insecure design in phone number lookup allowed enumeration of 5.4M accounts.

**Zoom (2020)**: Lack of encryption by default was a design flaw, not an implementation bug.

---

## References

- OWASP Top 10 2021: A04 - Insecure Design
- NIST SP 800-160: Systems Security Engineering
- Microsoft SDL (Security Development Lifecycle)
- STRIDE Threat Modeling
- OWASP Threat Modeling Cheat Sheet
