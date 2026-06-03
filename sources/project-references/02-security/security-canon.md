# Security Canon: Comprehensive Security Standards

This document provides comprehensive, non-negotiable security standards for all projects following the Vibe Code Canon framework covering ALL 25 critical security areas.

**Authority:** These standards have ABSOLUTE AUTHORITY and MUST be followed alongside the security checklist in agent instructions. All examples provided are for contextual purposes ONLY and should not be assumed to be part of the security canon or project requirements.

---

## Table of Contents

### Section 1: Access Control and Authorization (5 areas)
1.1 Broken Access Control (OWASP #1)  
1.2 Role-Based Access Control (RBAC)  
1.3 Attribute-Based Access Control (ABAC)  
1.4 Least Privilege Principle  
1.5 Separation of Duties  

### Section 2: Authentication and Session Management (3 areas)
2.1 Multi-Factor Authentication (MFA)  
2.2 Session Management Security  
2.3 Token and Session Signing  

### Section 3: Input Validation and Injection Prevention (3 areas)
3.1 Input Validation  
3.2 SQL Injection Prevention  
3.3 Cross-Site Scripting (XSS) Prevention  

### Section 4: Request Security (2 areas)
4.1 Cross-Site Request Forgery (CSRF) Protection  
4.2 Server-Side Request Forgery (SSRF) Prevention  

### Section 5: File and Upload Security (1 area)
5.1 File Upload Security  

### Section 6: Cryptography and Secrets Management (3 areas)
6.1 Secrets Management  
6.2 Cryptographic Failures Prevention  
6.3 Data Sanitization and Secure Disposal  

### Section 7: Transport and Network Security (3 areas)
7.1 HTTPS Enforcement  
7.2 HTTP Strict Transport Security (HSTS)  
7.3 Encryption at Rest and in Transit  

### Section 8: Database Security (1 area)
8.1 Row Level Security (RLS)  

### Section 9: Rate Limiting and Bot Prevention (2 areas)
9.1 Rate Limiting  
9.2 CAPTCHA Implementation  

### Section 10: Logging and Monitoring (1 area)
10.1 Tamper-Proof Audit Logging  

### Section 11: Error Handling (1 area)
11.1 Secure Error Handling  

### Section 12: Dependency Management (1 area)
12.1 Dependency Security  

### Section 13: Compliance Standards (3 areas)
13.1 ISO 27001  
13.2 NIST Standards  
13.3 PCI DSS  

---

## Section 1: Access Control and Authorization

### 1.1 Broken Access Control (OWASP #1 - CRITICAL)

**Definition:**
Users can perform actions or access resources beyond their intended permissions.

**Attack Patterns:**
- Changing URL parameters (`/user/123` → `/user/124`) to access other user's data
- Accessing admin functions without admin role
- Viewing or modifying records that don't belong to the user
- Bypassing authorization checks by manipulating JSON or API requests
- Accessing API endpoints without proper credentials

**Requirements:**

For EVERY endpoint and function, verify:

1. **Authentication:** Who is this user?
2. **Authorization:** Can THIS user access THIS resource?
3. **Ownership:** Does this resource belong to this user?
4. **Logging:** Record all access attempts

**Implementation Rules:**

```
Endpoint: GET /api/documents/:id

WRONG:
function getDocument(id) {
  return database.documents.findById(id)  // Anyone can access any document!
}

CORRECT:
function getDocument(id, userId) {
  const doc = database.documents.findById(id)
  if (!doc) return error("Not found")
  if (doc.ownerId !== userId) return error("Access denied")
  logAccess(userId, "document_view", id)
  return doc
}
```

**Verification Checklist:**
- [ ] User A cannot view User B's data (even with valid authentication)
- [ ] Admin-only functions reject non-admin users
- [ ] Authorization checks happen server-side (never trust frontend)
- [ ] Direct object references are validated (don't accept IDs blindly)
- [ ] All access attempts are logged

---

### 1.2 Role-Based Access Control (RBAC)

**When to Use:**
Small to medium systems with clear role hierarchy and stable permissions.

**How It Works:**
- Users assigned to roles (Admin, Manager, Employee, Viewer)
- Roles have predefined permissions
- Users inherit permissions from roles

**Advantages:**
- Simple to understand and manage
- Efficient for most organizations
- Easy onboarding (just assign role)
- Supports least privilege principle
- Clear audit trail

**Disadvantages:**
- Role explosion in large organizations (100+ roles)
- Inflexible for context-based access
- Cannot handle time-based or location-based restrictions

**Implementation:**

```
Roles:
  - Admin: Full system access
  - Editor: Create, update, delete own content
  - Viewer: Read-only access
  - Guest: Public content only

User Assignment:
  - User assigns to ONE primary role
  - Can have additional roles for specific resources
  - Least privilege by default
```

---

### 1.3 Attribute-Based Access Control (ABAC)

**When to Use:**
Large enterprises, complex permission requirements, need context-aware access.

**How It Works:**
Access based on attributes (user attributes, resource attributes, environment context).

**Example:**
```
Grant access IF:
  user.department = "Finance" AND
  resource.sensitivity = "Low" AND
  time.hour >= 8 AND time.hour <= 18 AND
  location.country = "Kenya"
```

**Advantages:**
- Extremely flexible
- Handles complex scenarios
- Dynamic permissions based on context
- Fine-grained control

**Disadvantages:**
- Complex to design
- Harder to audit
- Requires more computational resources

**Recommended: Hybrid RBAC + ABAC**

Use RBAC for base permissions, ABAC for context:

```
User: John
Base Role (RBAC): Officer
Context Restrictions (ABAC):
  - Can approve transactions up to $10,000 (higher needs supervisor)
  - Access only during business hours (8 AM - 6 PM)
  - Access only from office network (not public internet)
  - Cannot access own records (conflict of interest)
```

---

### 1.4 Least Privilege Principle

**Definition:**
Users, programs, and processes should have ONLY the minimum privileges necessary to perform their function.

**Why Critical:**
- Minimizes attack surface
- Limits malware propagation
- Reduces blast radius if compromised
- Prevents lateral movement in network
- Required for compliance (SOC 2, PCI-DSS, ISO 27001, FedRAMP)

**Implementation Layers:**

**User Level:**
- Default user = minimal permissions
- Admin accounts separate from daily-use accounts
- Temporary privilege elevation (sudo-style, not permanent admin)
- Regular permission audits (remove unused permissions)

**Service Level:**
- Database user has only needed permissions (read-only if possible)
- API keys scoped to specific endpoints
- Service accounts restricted to their service only

**Code Level:**
- Functions run with minimum required privileges
- Separate high-privilege operations into isolated modules
- File system access restricted to necessary directories only

**Network Level:**
- Microservices can only talk to services they need
- Default deny all, whitelist specific connections
- Network segmentation (service A cannot access service B's database)

**Verification Checklist:**
- [ ] New users start with zero permissions, add only what's needed
- [ ] API endpoints require authentication and authorization by default
- [ ] Database access uses least-privileged user (not root)
- [ ] File operations restricted to specific directories
- [ ] Network calls whitelist destinations

---

### 1.5 Separation of Duties

**Definition:**
Critical tasks split across multiple people to prevent fraud.

**Why Critical:**
- Prevents single person from manipulating systems
- Reduces insider threats
- Required for financial system compliance

**Examples:**

**Bad (no SoD):**
```
User John can:
1. Create rule
2. Approve rule
3. Deploy rule
4. Audit rule compliance

Risk: John controls entire process
```

**Good (with SoD):**
```
Policy Team: Creates rules
Supervisor: Approves rules
DevOps: Deploys rules (cannot modify)
Audit Team: Verifies compliance (separate department)

Result: No single person controls entire process
```

**Requirements:**
- User who creates cannot approve
- User who approves cannot audit
- Document who did what (audit trail)
- Flag attempts to bypass SoD
- Enforce at code level (not just policy)

---

## Section 2: Authentication and Session Management

### 2.1 Multi-Factor Authentication (MFA)

**Definition:**
Requiring two or more independent credentials for authentication.

**Factor Types:**
1. **Something you know** (password, PIN)
2. **Something you have** (phone, hardware token, authenticator app)
3. **Something you are** (fingerprint, face recognition, iris scan)

**Why Critical:**
- Passwords alone are insufficient (easily stolen, phished, guessed)
- MFA reduces account takeover by 99.9%
- Required for PCI DSS compliance (March 31, 2025)
- Required for high-value transactions and administrative access

**Implementation Options:**

**SMS-Based (LEAST SECURE):**
- Easy to implement
- Vulnerable to SIM swapping
- Vulnerable to interception
- Use only as fallback

**Authenticator Apps (RECOMMENDED):**
- Time-based One-Time Passwords (TOTP)
- Apps: Google Authenticator, Authy, Microsoft Authenticator
- More secure than SMS
- Works offline

**Hardware Tokens (MOST SECURE):**
- YubiKey, Titan Security Key
- Phishing-resistant
- Recommended for high-privilege accounts

**Biometric (CONTEXT-DEPENDENT):**
- Fingerprint, face recognition
- Good for mobile devices
- Cannot be changed if compromised

**When to Require MFA:**
- Login to administrative accounts (MANDATORY)
- Access to sensitive data (MANDATORY)
- Payment processing (MANDATORY for PCI DSS)
- Password changes
- Account recovery
- Adding new devices

**Implementation Requirements:**
- Offer multiple MFA options
- Allow backup codes for account recovery
- Enforce MFA for admin accounts (no exceptions)
- Log all MFA attempts (success and failure)
- Alert on repeated MFA failures

**Verification:**
- [ ] MFA required for administrative access
- [ ] MFA required for sensitive operations
- [ ] Multiple MFA methods offered
- [ ] Backup codes provided
- [ ] MFA attempts logged

---

### 2.2 Session Management Security

**Access Token Lifespans:**
- Access Token: 15-30 minutes (short-lived)
- Refresh Token: 7-30 days (longer)
- Session Token: Until logout or absolute timeout

**Why Short Tokens:**
- Limits damage if token stolen
- Forces periodic re-authentication
- Reduces replay attack window

**Token Refresh Flow:**

```
1. User logs in → access token (15min) + refresh token (7 days)
2. User makes requests using access token
3. Access token expires after 15 minutes
4. Client automatically uses refresh token to get new access token
5. Continue until refresh token expires (7 days)
6. User must re-authenticate
```

**Storage Requirements:**
- Store tokens in HttpOnly cookies (not localStorage - XSS vulnerable)
- Use Secure flag (HTTPS only)
- Use SameSite flag (CSRF protection)

**Transmission Requirements:**
- Always HTTPS (never HTTP)
- Never in URL parameters (logged in access logs)
- Never in GET requests

**Revocation Requirements:**
- Logout must invalidate both access and refresh tokens
- Password change must invalidate all tokens
- Support "logout from all devices"
- Maintain token blacklist for revoked tokens

**Monitoring Requirements:**
- Detect unusual patterns (token used from multiple IPs)
- Alert on impossible travel (Kenya → USA in 5 minutes)
- Rate limit token refresh attempts

**Verification:**
- [ ] Access tokens expire in 15-30 minutes
- [ ] Tokens stored in HttpOnly cookies
- [ ] Tokens never in URL parameters
- [ ] Logout invalidates all tokens
- [ ] Password change invalidates all tokens
- [ ] Unusual token usage monitored

---

### 2.3 Token and Session Signing

**The Problem:**
Without cryptographic signing, attackers can forge or tamper with tokens, session data, and cookies. Frontend-supplied data cannot be trusted.

**Attack Scenarios:**
- User modifies session cookie to impersonate another user
- Attacker creates fake JWT with elevated permissions
- Malicious frontend sends tampered session data
- Cookie values modified to change user role or permissions

**Golden Rule:**
**Never trust any token or session data from the client without cryptographic verification.**

---

**Prevention Strategies:**

#### **Strategy 1: Signed Cookies (HMAC)**

**All cookies containing security-relevant data MUST be signed:**

```javascript
// Node.js with cookie-signature
const cookieParser = require('cookie-parser')
const SECRET = process.env.COOKIE_SECRET  // 256-bit random key

app.use(cookieParser(SECRET))

// Set signed cookie
res.cookie('session_id', sessionId, {
  signed: true,
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
})

// Read and verify signed cookie
const sessionId = req.signedCookies.session_id
if (!sessionId) {
  // Signature invalid or cookie tampered
  return res.status(401).json({ error: 'Invalid session' })
}
```

```python
# Python Flask with itsdangerous
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(SECRET_KEY)

# Sign session data
signed_session = serializer.dumps({'user_id': 123, 'role': 'user'})

# Verify and decode (fails if tampered)
try:
    session_data = serializer.loads(signed_session, max_age=3600)
except BadSignature:
    return error('Session tampered or expired')
```

---

#### **Strategy 2: JWT Signature Verification (MANDATORY)**

**Never use unsigned JWTs (alg: none). Always verify signatures server-side:**

```javascript
// Node.js with jsonwebtoken
const jwt = require('jsonwebtoken')
const SECRET = process.env.JWT_SECRET  // Use RS256 for production

// Sign token
const token = jwt.sign(
  { userId: 123, role: 'user' },
  SECRET,
  { algorithm: 'HS256', expiresIn: '15m' }
)

// Verify token (MANDATORY on every request)
try {
  const decoded = jwt.verify(token, SECRET, { algorithms: ['HS256'] })
  // Explicitly specify allowed algorithms to prevent "none" attack
} catch (error) {
  if (error.name === 'TokenExpiredError') {
    return res.status(401).json({ error: 'Token expired' })
  }
  return res.status(401).json({ error: 'Invalid token' })
}
```

```python
# Python with PyJWT
import jwt

# Sign token
token = jwt.encode(
    {'user_id': 123, 'role': 'user', 'exp': datetime.utcnow() + timedelta(minutes=15)},
    SECRET_KEY,
    algorithm='HS256'
)

# Verify token
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
except jwt.ExpiredSignatureError:
    return error('Token expired')
except jwt.InvalidTokenError:
    return error('Invalid token')
```

---

#### **Strategy 3: Server-Side Session Validation**

**Never store sensitive data in client-side tokens. Use opaque session IDs:**

```
[REJECTED] BAD: Store user role in cookie/JWT
  Cookie: role=admin  // Attacker changes to admin

[APPROVED] GOOD: Store only session ID, lookup role server-side
  Cookie: session_id=a7f3c2d8... (signed, opaque)
  Server: SELECT role FROM sessions WHERE id = 'a7f3c2d8...'
```

```javascript
// Server-side session lookup
const sessionId = req.signedCookies.session_id
const session = await sessionStore.get(sessionId)

if (!session || session.expiresAt < Date.now()) {
  return res.status(401).json({ error: 'Session expired' })
}

// Trust server-stored data, not client claims
req.user = {
  id: session.userId,
  role: session.role  // From server, not client
}
```

---

#### **Strategy 4: Session ID Rotation**

**Rotate session ID after authentication to prevent session fixation:**

```javascript
// After successful login
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body)
  
  if (user) {
    // Destroy old session
    req.session.destroy()
    
    // Create new session with new ID
    req.session.regenerate((err) => {
      req.session.userId = user.id
      req.session.role = user.role
      res.json({ success: true })
    })
  }
})
```

---

#### **Strategy 5: Anti-Tampering Checksums**

**For sensitive state passed through forms:**

```javascript
// Generate HMAC for form data
const crypto = require('crypto')

function signData(data) {
  const hmac = crypto.createHmac('sha256', SECRET)
  hmac.update(JSON.stringify(data))
  return hmac.digest('hex')
}

// In form
<input type="hidden" name="order_id" value="12345">
<input type="hidden" name="amount" value="100">
<input type="hidden" name="signature" value="${signData({order_id: 12345, amount: 100})}">

// On submit, verify signature matches data
const expectedSig = signData({ order_id: req.body.order_id, amount: req.body.amount })
if (req.body.signature !== expectedSig) {
  return res.status(400).json({ error: 'Data tampered' })
}
```

---

**Algorithm Requirements:**

| Use Case | Recommended Algorithm | Forbidden |
|----------|----------------------|-----------|
| Cookie signing | HMAC-SHA256 | MD5, SHA1 |
| JWT signing | RS256, ES256, EdDSA | none, HS256 with weak secret |
| Session tokens | CSPRNG (256-bit) | Math.random(), predictable |
| Form checksums | HMAC-SHA256 | CRC32, MD5 |

---

**Verification Checklist:**

- [ ] All cookies containing security data are signed (HMAC)
- [ ] JWT signatures verified on every request
- [ ] JWT algorithm explicitly specified (no "none" algorithm)
- [ ] Sensitive data stored server-side, not in tokens
- [ ] Session IDs rotated after authentication
- [ ] Session IDs generated with CSPRNG (256-bit minimum)
- [ ] Form data with security implications includes tamper-proof signature
- [ ] Token secrets stored in secrets manager, not code
- [ ] Different signing keys per environment

---

## Section 3: Input Validation and Injection Prevention

### 3.1 Input Validation

**The Problem:**
User inputs are the primary attack vector for most vulnerabilities.

**Golden Rule:**
**Never trust user input. Validate everything on the server-side.**

**Validation Layers:**

**1. Syntactic Validation (Format):**
- Email: Must match email format
- Phone: Must match phone pattern
- URL: Must be valid URL
- Numbers: Must be numeric within range
- Dates: Must be valid dates

**2. Semantic Validation (Logic):**
- Age: 0-150 (not -5 or 999)
- Price: Positive number
- Quantity: Positive integer
- Dates: Future date for appointments, past date for birth date

**3. Business Logic Validation:**
- Discount cannot exceed 100%
- Withdrawal cannot exceed account balance
- User can only update their own profile

**Validation Strategies:**

**Whitelist (PREFERRED):**
```
// Accept only known-good values
if (country in ["Kenya", "Uganda", "Tanzania"]) {
  accept()
}
```

**Blacklist (AVOID):**
```
// Reject known-bad values (incomplete, can be bypassed)
if (input contains "<script>") {
  reject()
}
```

**Length Limits:**
- Enforce maximum length on all inputs
- Prevents buffer overflow attempts
- Prevents database errors

**Type Checking:**
- Validate data types (string, number, boolean)
- Use strong typing in languages that support it

**Implementation Requirements:**

**Frontend Validation (UX ONLY):**
- Provides immediate feedback
- DO NOT rely on for security
- Easily bypassed

**Backend Validation (SECURITY):**
- MANDATORY for all inputs
- Cannot be bypassed
- Last line of defense

**Common Validation Rules:**

```
// Email
regex: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

// Phone (Kenya)
regex: /^\+254[71]\d{8}$/

// URL
regex: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/

// Alphanumeric only
regex: /^[a-zA-Z0-9]+$/

// Numbers only
regex: /^\d+$/
```

**Verification:**
- [ ] All user inputs validated on backend
- [ ] Whitelist validation used where possible
- [ ] Length limits enforced
- [ ] Type checking implemented
- [ ] Business logic validation in place

---

### 3.2 SQL Injection Prevention

**The Problem:**
Attacker injects malicious SQL code through user inputs to manipulate database queries.

**Example Attack:**

```
User input: admin' OR '1'='1

Bad Query (vulnerable):
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = '...'

Result: Attacker logs in without password
```

**Prevention: Parameterized Queries (MANDATORY)**

**Wrong (String Concatenation):**
```python
# VULNERABLE
query = "SELECT * FROM users WHERE username = '" + username + "'"
```

**Correct (Parameterized Query):**

```python
# PostgreSQL with psycopg2
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# MySQL with mysqlclient
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# SQLite with sqlite3
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# Using ORM (Recommended)
User.objects.filter(username=username)  # Django
db.query(User).filter_by(username=username)  # SQLAlchemy
```

**Additional Protections:**

**1. Least Privilege Database User:**
- Use separate database user for application
- Grant only necessary permissions (SELECT, INSERT, UPDATE)
- NO DROP, CREATE, ALTER permissions

**2. Stored Procedures (Optional):**
- Encapsulate SQL logic
- Limit direct SQL access
- Still use parameterized calls

**3. Input Validation:**
- Validate before database query
- Whitelist acceptable characters
- Reject special characters when not needed

**4. Error Handling:**
- Never expose SQL errors to users
- Log errors internally
- Return generic error messages

**Verification:**
- [ ] NO string concatenation in SQL queries
- [ ] All queries use parameterized statements
- [ ] Database user has minimal permissions
- [ ] SQL errors not exposed to users
- [ ] Input validation before database access

---

### 3.3 Cross-Site Scripting (XSS) Prevention

**The Problem:**
Attacker injects malicious JavaScript into web pages viewed by other users.

**Types of XSS:**

**1. Stored XSS (Most Dangerous):**
```
Attacker submits:
<script>alert('XSS')</script>

Stored in database
Executes for every user who views it
```

**2. Reflected XSS:**
```
URL: https://site.com/search?q=<script>alert('XSS')</script>

Server reflects input back in HTML
Executes when victim clicks malicious link
```

**3. DOM-Based XSS:**
```
Client-side JavaScript manipulates DOM with untrusted data
No server involvement
```

**Prevention Strategies:**

**1. Output Encoding (MANDATORY):**

Escape HTML special characters:

```
< → &lt;
> → &gt;
" → &quot;
' → &#x27;
& → &amp;
```

**Language-Specific Escaping:**

```python
# Python (Django)
from django.utils.html import escape
safe_output = escape(user_input)

# Python (Jinja2)
{{ user_input | e }}

# JavaScript (React)
<div>{userInput}</div>  // Auto-escaped

# PHP
htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8')

# Ruby on Rails
<%= h(user_input) %>
```

**2. Content Security Policy (CSP):**

```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self';
  frame-ancestors 'none';
```

**3. HTTPOnly Cookies:**
- Prevents JavaScript from accessing cookies
- Mitigates session hijacking via XSS

**4. Input Validation:**
- Sanitize rich text inputs
- Use libraries like DOMPurify for HTML sanitization

**5. Avoid innerHTML:**
```
// BAD
element.innerHTML = userInput

// GOOD
element.textContent = userInput
```

**Verification:**
- [ ] All user-generated content HTML-escaped
- [ ] CSP headers implemented
- [ ] HTTPOnly flag on session cookies
- [ ] No use of innerHTML with user data
- [ ] Rich text inputs sanitized

---

## Section 4: Request Security

### 4.1 Cross-Site Request Forgery (CSRF) Protection

**The Problem:**
Attacker tricks authenticated user into executing unwanted actions.

**Example Attack:**

```
User logged into bank.com
Visits attacker.com
Attacker page contains:
<img src="https://bank.com/transfer?to=attacker&amount=1000">

Request sent with user's session cookie
Transfer executes without user's knowledge
```

**Prevention Strategies:**

**1. CSRF Tokens (MANDATORY for state-changing operations):**

```
Server generates random token per session/request
Embeds in form:
<form method="POST">
  <input type="hidden" name="csrf_token" value="a3b8c7d9...">
  ...
</form>

Server validates token with every POST/PUT/DELETE
Rejects if missing or invalid
```

**2. SameSite Cookie Attribute:**

```
Set-Cookie: sessionId=...; SameSite=Strict; Secure; HttpOnly

SameSite=Strict: Cookie never sent on cross-site requests
SameSite=Lax: Cookie sent on top-level navigation (GET only)
```

**3. Double-Submit Cookie Pattern:**

```
Server sets CSRF token in cookie AND requires it in request header
Attacker cannot read cookie due to same-origin policy
Cannot forge valid request
```

**4. Verify Origin Headers:**

```
Check Origin or Referer headers
Reject if from untrusted domain
```

**Important Notes:**
- CSRF protection ONLY needed for authenticated state-changing operations
- GET requests should NEVER change state (idempotent)
- Use CSRF tokens for: POST, PUT, DELETE, PATCH

**Verification:**
- [ ] CSRF tokens on all state-changing forms
- [ ] SameSite=Strict or Lax on session cookies
- [ ] Origin headers validated
- [ ] GET requests are read-only

---

### 4.2 Server-Side Request Forgery (SSRF) Prevention

**The Problem:**
Attacker tricks server into making requests to internal systems or external sites.

**Example Attack:**

```
Application: Fetch URL provided by user
User input: http://localhost:8080/admin/delete-all-users

Server makes request to internal admin endpoint
Bypasses firewall (request from internal server)
Executes privileged operation
```

**Common SSRF Scenarios:**
- URL preview generators
- Webhook handlers
- File import from URL
- API integrations
- Image proxies

**Prevention Strategies:**

**1. Whitelist Allowed Domains/IPs (MANDATORY):**

```
allowed_domains = ["api.example.com", "cdn.example.com"]
allowed_ips = ["8.8.8.8", "1.1.1.1"]

if domain not in allowed_domains:
  reject()
```

**2. Blacklist Internal IPs:**

```
blocked_ips = [
  "127.0.0.1",  # localhost
  "0.0.0.0",
  "10.0.0.0/8",  # private networks
  "172.16.0.0/12",
  "192.168.0.0/16",
  "169.254.0.0/16",  # link-local
  "::1",  # IPv6 localhost
  "fc00::/7",  # IPv6 private
]
```

**3. Disable URL Redirects:**
```
Follow redirects can bypass whitelist
Initial URL allowed, redirects to internal IP
Disable or limit redirect following
```

**4. Use Separate Network Segment:**
```
Application servers in DMZ
Cannot access internal network
Reduces SSRF impact
```

**5. Validate URL Scheme:**
```
allowed_schemes = ["http", "https"]

if url.scheme not in allowed_schemes:
  reject()  // Prevents file://, gopher://, etc.
```

**Verification:**
- [ ] URL destinations whitelisted
- [ ] Internal IPs blacklisted
- [ ] URL scheme validated
- [ ] Redirects disabled or limited
- [ ] Separate network segment for external-facing services

---

## Section 5: File and Upload Security

### 5.1 File Upload Security

**The Problem:**
Unrestricted file uploads allow attackers to upload malicious files.

**Attack Scenarios:**
- Upload web shell (malicious_file.php) → execute arbitrary code
- Upload malware → spread to other users
- Upload oversized file → denial of service
- Upload file with dangerous extension → bypass filters

**Prevention Strategies:**

**1. Validate File Type (Multiple Layers):**

**Extension Check (WEAK, easily bypassed):**
```
allowed_extensions = [".jpg", ".png", ".pdf"]
if file.extension not in allowed_extensions:
  reject()
```

**MIME Type Check (BETTER, but can be spoofed):**
```
allowed_mimes = ["image/jpeg", "image/png", "application/pdf"]
if file.mime_type not in allowed_mimes:
  reject()
```

**Magic Bytes Check (BEST):**
```
// Read file header to verify actual file type
file_signatures = {
  "image/jpeg": ["FF D8 FF"],
  "image/png": ["89 50 4E 47"],
  "application/pdf": ["25 50 44 46"]
}

if file_header not in allowed_signatures:
  reject()
```

**2. File Size Limits:**

```
max_file_size = 5 * 1024 * 1024  // 5MB

if file.size > max_file_size:
  reject()
```

**3. Rename Uploaded Files:**

```
// NEVER use original filename
original_name = "malicious.php.jpg"
safe_name = generate_uuid() + ".jpg"  // "a7f3c2d8-b1e9.jpg"

// Store mapping in database if original name needed
```

**4. Store Outside Web Root:**

```
// BAD
/var/www/html/uploads/file.pdf  // Directly accessible

// GOOD
/var/app/storage/uploads/a7f3c2d8-b1e9.pdf  // Not directly accessible
```

**5. Scan for Malware:**

```
// Use antivirus scanning library
scan_result = antivirus.scan(uploaded_file)
if scan_result != "clean":
  reject()
  alert_security_team()
```

**6. Disable Script Execution inUpload Directory:**

```
// Apache .htaccess in uploads directory
<FilesMatch "\.ph(p[3-7]?|tml)$">
  Deny from all
</FilesMatch>

// Nginx config
location /uploads {
  location ~ \.php$ {
    deny all;
  }
}
```

**7. Use CDN/Object Storage:**

```
Store uploads in AWS S3, Google Cloud Storage, Azure Blob
Separate from application server
Cannot execute code
```

**Verification:**
- [ ] File type validated by magic bytes
- [ ] File size limited
- [ ] Files renamed to safe names
- [ ] Uploads stored outside web root
- [ ] Malware scanning implemented
- [ ] Antivirus scanning enabled on upload
- [ ] Quarantine suspicious files

---

### 5.2 Path Traversal / Directory Traversal Prevention

**CRITICAL SECURITY VULNERABILITY - OWASP Top 10**

**The Problem:**
Attackers manipulate file paths using special sequences (like `../`) to access files outside the intended directory, potentially gaining access to system files, configuration files, source code, or other users' data.

**Example Attack:**

```
Normal Request:
GET /download?file=tax-report.pdf

Malicious Request:
GET /download?file=../../etc/passwd
GET /download?file=../../../app/.env
GET /download?file=../../../../var/www/config/database.yml
```

**What Gets Exposed:**
- System files: `/etc/passwd`, `/etc/shadow`, system logs
- Application secrets: `.env` files, database credentials, API keys
- Source code: Application logic, proprietary algorithms
- User data: Other users' files, financial records, personal information

**Result:** Complete server compromise.

---

**Attack Vectors:**

1. **URL Parameters:**
   ```
   ?file=../../secret.txt
   ?document=../../../../../etc/passwd
   ```

2. **Form Inputs:**
   ```html
   <input name="document" value="../../../.env">
   ```

3. **API Requests:**
   ```json
   {"filename": "../../../../config/database.yml"}
   ```

4. **HTTP Headers:**
   ```
   X-Filename: ../../../etc/shadow
   ```

---

**Prevention Strategies (Defense in Depth):**

#### **Strategy 1: Avoid User-Controlled Paths (PREFERRED)**

[APPROVED] **Best Practice:** Don't let users specify file paths at all.

```typescript
// [REJECTED] VULNERABLE: User controls file path
app.get('/download', (req, res) => {
  const fileName = req.query.file;  // User input!
  res.sendFile(`/uploads/${fileName}`);  // DANGER
});

// [APPROVED] SECURE: Use file IDs instead
app.get('/download/:fileId', async (req, res) => {
  const fileId = req.params.fileId;
  
  // Get actual filename from database
  const file = await db.files.findOne({ 
    id: fileId,
    userId: req.user.id  // Authorization check!
  });
  
  if (!file) return res.status(404).send('Not found');
  
  // User never controls the path
  res.sendFile(file.storedPath);
});
```

---

#### **Strategy 2: Path Resolution and Validation (REQUIRED if accepting filenames)**

**Node.js/TypeScript:**

```typescript
import path from 'path';
import fs from 'fs/promises';

// Define base directory (absolute path)
const BASE_DIRECTORY = path.resolve(__dirname, 'public/uploads');

export const downloadFile = async (req, res, next) => {
  const fileName = req.query.file;
  
  if (!fileName) {
    return res.status(400).json({ message: 'File name required' });
  }
  
  // Construct full path
  const requestedPath = path.join(BASE_DIRECTORY, fileName);
  
  // CRITICAL - Resolve to absolute path
  const resolvedPath = path.resolve(requestedPath);
  
  // CRITICAL - Verify path is inside base directory
  if (!resolvedPath.startsWith(BASE_DIRECTORY)) {
    console.error(`Path traversal attempt: ${fileName}`);
    return res.status(400).json({ message: 'Invalid file path' });
  }
  
  try {
    // Verify file exists
    await fs.access(resolvedPath);
    
    // Authorization check
    const file = await db.files.findOne({
      path: resolvedPath,
      userId: req.user.id
    });
    
    if (!file) {
      return res.status(403).json({ message: 'Access denied' });
    }
    
    // Safe to serve
    res.download(resolvedPath, path.basename(fileName));
    
  } catch (error) {
    return res.status(404).json({ message: 'File not found' });
  }
};
```

**Python:**

```python
import os
from pathlib import Path

BASE_DIRECTORY = Path('/var/app/uploads').resolve()

def download_file(request):
    file_name = request.GET.get('file')
    
    if not file_name:
        return JsonResponse({'error': 'File required'}, status=400)
    
    # Construct path
    requested_path = BASE_DIRECTORY / file_name
    
    # Resolve to absolute path
    resolved_path = requested_path.resolve()
    
    # CRITICAL: Verify within base directory
    if not resolved_path.is_relative_to(BASE_DIRECTORY):
        logger.error(f'Path traversal attempt: {file_name}')
        return JsonResponse({'error': 'Invalid path'}, status=400)
    
    # Verify exists
    if not resolved_path.exists():
        return JsonResponse({'error': 'Not found'}, status=404)
    
    # Authorization check
    file = File.objects.filter(
        path=str(resolved_path),
        user_id=request.user.id
    ).first()
    
    if not file:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    return FileResponse(open(resolved_path, 'rb'))
```

---

#### **Strategy 3: Input Validation**

**Block Dangerous Characters:**

```javascript
function isPathSafe(fileName) {
  // Reject if contains path traversal sequences
  const dangerousPatterns = [
    /\.\./,          // ..
    /\.\.\\/,        // ..\
    /\.\.\//,        // ../
    /^\/+/,          // Absolute paths
    /^[A-Za-z]:/,    // Windows drive letters
    /[<>:"|?*\x00-\x1f]/  // Invalid filename chars
  ];
  
  return !dangerousPatterns.some(pattern => pattern.test(fileName));
}

app.get('/download', (req, res) => {
  const fileName = req.query.file;
  
  if (!isPathSafe(fileName)) {
    console.error(`Dangerous file path: ${fileName}`);
    return res.status(400).send('Invalid filename');
  }
  
  // Continue with path resolution and validation...
});
```

**Whitelist Allowed Characters:**

```javascript
// Only allow alphanumeric, dash, underscore, dot
const SAFE_FILENAME_REGEX = /^[a-zA-Z0-9._-]+$/;

if (!SAFE_FILENAME_REGEX.test(fileName)) {
  return res.status(400).send('Invalid filename format');
}
```

---

#### **Strategy 4: Allowlist Approach (When Possible)**

```javascript
// Allowlist of permitted files
const ALLOWED_FILES = new Set([
  'user-guide.pdf',
  'tax-form-2024.pdf',
  'filing-instructions.pdf'
]);

app.get('/download', (req, res) => {
  const fileName = req.query.file;
  
  // Reject if not in allowlist
  if (!ALLOWED_FILES.has(fileName)) {
    return res.status(403).send('File not permitted');
  }
  
  const safePath = path.join(BASE_DIR, fileName);
  res.sendFile(safePath);
});
```

---

#### **Strategy 5: Authorization Check (MANDATORY)**

**Every file access MUST verify user owns the file:**

```sql
-- Verify user owns the file
SELECT * FROM files 
WHERE id = ? AND user_id = ?
```

```javascript
// Application code
const file = await db.files.findOne({
  id: fileId,
  userId: req.user.id
});

if (!file) {
  return res.status(403).json({ message: 'Access denied' });
}
```

---

#### **Strategy 6: Filesystem Isolation**

**Store files outside web root:**

```
Project Structure:
/var/www/app/          (web root)
  ├── public/
  ├── src/
  └── ...

/var/app-data/        (outside web root)
  └── uploads/        (not directly accessible via web)
```

**Use chroot jails or containers:**

```dockerfile
# Docker container example
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY src/ ./src/
COPY uploads/ /data/uploads/

# Run as non-root user
USER node

# Application can only access /app and /data
```

---

#### **Strategy 7: Least Privilege File Permissions**

```bash
# Upload directory: read-only for application
chmod 755 /var/app/uploads
chown root:appuser /var/app/uploads

# Application runs as 'appuser' without write access to system files
```

---

#### **Strategy 8: Monitoring and Logging**

```javascript
function logFileAccess(userId, fileName, ipAddress, allowed) {
  auditLog.write({
    timestamp: new Date(),
    userId,
    fileName,
    ipAddress,
    allowed,
    type: 'FILE_ACCESS'
  });
  
  // Alert on suspicious patterns
  if (!allowed && fileName.includes('..')) {
    securityAlert.send({
      severity: 'HIGH',
      type: 'PATH_TRAVERSAL_ATTEMPT',
      userId,
      fileName,
      ipAddress
    });
  }
}
```

---

**Complete Secure Example:**

```typescript
import path from 'path';
import fs from 'fs/promises';

const BASE_DIRECTORY = path.resolve(__dirname, '../uploads');

// Validation utilities
function isPathSafe(fileName: string): boolean {
  const dangerousPatterns = [/\.\./, /^\//, /^[A-Za-z]:/, /[\x00-\x1f]/];
  return !dangerousPatterns.some(p => p.test(fileName));
}

function validatePath(userInput: string, baseDir: string): string {
  if (!isPathSafe(userInput)) {
    throw new Error('Invalid filename format');
  }
  
  const resolved = path.resolve(path.join(baseDir, userInput));
  
  if (!resolved.startsWith(baseDir)) {
    throw new Error('Path traversal detected');
  }
  
  return resolved;
}

// Secure file download endpoint
export const secureDownload = async (req, res) => {
  try {
    const fileId = req.params.fileId;
    
    // Get file metadata from database
    const file = await db.files.findOne({
      id: fileId,
      userId: req.user.id  // Authorization
    });
    
    if (!file) {
      logFileAccess(req.user.id, fileId, req.ip, false);
      return res.status(404).json({ error: 'File not found' });
    }
    
    // Validate path
    const safePath = validatePath(file.filename, BASE_DIRECTORY);
    
    // Verify file exists
    await fs.access(safePath);
    
    // Log successful access
    logFileAccess(req.user.id, file.filename, req.ip, true);
    
    // Serve file
    res.download(safePath, file.originalName);
    
  } catch (error) {
    if (error.message.includes('Path traversal')) {
      logFileAccess(req.user.id, req.params.fileId, req.ip, false);
      return res.status(400).json({ error: 'Invalid file path' });
    }
    
    return res.status(500).json({ error: 'Internal server error' });
  }
};
```

---

**Verification Checklist:**

- [ ] Users cannot control file paths directly (use IDs/UUIDs)
- [ ] If accepting filenames, path resolution validates within base directory
- [ ] Input validation blocks `..`, `/`, `\`, null bytes
- [ ] Whitelist validation for allowed characters
- [ ] Authorization check verifies user owns file
- [ ] Files stored outside web root
- [ ] Application runs with minimal filesystem permissions
- [ ] File access attempts logged
- [ ] Alerts configured for traversal attempts
- [ ] Error messages don't reveal file structure
- [ ] Automated testing includes path traversal tests

---

**Testing for Path Traversal:**

```javascript
// Security test cases
describe('Path Traversal Protection', () => {
  const attacks = [
    '../../../etc/passwd',
    '..\\..\\..\\windows\\system32\\config\\sam',
    '....//....//....//etc/passwd',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',  // URL encoded
    '..;/..;/..;/etc/passwd',
    '/etc/passwd',
    'C:\\Windows\\System32\\config\\sam'
  ];
  
  attacks.forEach(attack => {
    it(`should block: ${attack}`, async () => {
      const response = await request(app)
        .get(`/download?file=${encodeURIComponent(attack)}`)
        .expect(400);
      
      expect(response.body.error).toMatch(/invalid|forbidden/i);
    });
  });
});
```

---

**Severity Assessment:**

**CVSS Score: 9.1 (CRITICAL)**

**Why Critical:**
- Easy to exploit (no special tools needed)
- High impact (complete system access possible)
- Common vulnerability (OWASP Top 10)
- Affects most applications with file operations
- Difficult to detect without proper logging

**This vulnerability is as serious as SQL Injection.**

---

**Cross-References:**
- Related to: Input Validation (Section 3.1)
- Related to: File Upload Security (Section 5.1)
- Related to: Broken Access Control (Section 1.1)
- Related to: Audit Logging (Section 7)

---

## Section 6: Cryptography and Secrets Management

### 6.1 Secrets Management

**The Problem:**
Hardcoded secrets in code or configuration files lead to credential exposure.

**What Are Secrets:**
- API keys
- Database passwords
- Encryption keys
- OAuth client secrets
- Service account credentials
- Private keys
- Signing secrets

**Bad Practices (FORBIDDEN):**

```
// NEVER do this
const API_KEY = "sk_live_a7f3c2d8b1e9..."
const DB_PASSWORD = "MyPassword123"

// NEVER commit .env files
// NEVER store secrets in version control
```

**Good Practices (REQUIRED):**

**1. Environment Variables:**

```
// .env file (NOT committed to Git)
API_KEY=sk_live_a7f3c2d8b1e9
DB_PASSWORD=MySecurePassword123

// Application code
const apiKey = process.env.API_KEY
const dbPassword = process.env.DB_PASSWORD
```

**.gitignore MUST include:**
```
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
secrets/
```

**2. Secrets Managers (RECOMMENDED):**

```
// Google Secret Manager
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
api_key = client.access_secret_version(name="projects/123/secrets/api-key/versions/latest")

// AWS Secrets Manager
import boto3
client = boto3.client('secretsmanager')
api_key = client.get_secret_value(SecretId='api-key')

// Azure Key Vault
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url="https://myvault.vault.azure.net/")
api_key = client.get_secret("api-key")
```

**3. Separate Secrets Per Environment:**

```
Development: dev-api-key
Staging: staging-api-key
Production: prod-api-key

NEVER reuse secrets across environments
```

**4. Rotate Secrets Regularly:**

```
// Rotation schedule
API keys: Every 90 days
Database passwords: Every 90 days
Encryption keys: Every 90 days
Service account keys: Every 90 days

// Implement automated rotation where possible
```

**5. Least Privilege for Secrets:**

```
// Service A only gets secrets it needs
service_a_secrets = ["database-password", "api-key-service-b"]

// Service A cannot access Service B's admin key
```

**Verification:**
- [ ] No hardcoded secrets in code
- [ ] .env files in .gitignore
- [ ] Using secrets manager for production
- [ ] Separate secrets per environment
- [ ] Secret rotation schedule implemented
- [ ] Least privilege applied to secret access

---

### 6.2 Cryptographic Failures Prevention

**Weak Algorithms (FORBIDDEN):**
- [REJECTED] MD5, SHA-1 (broken for cryptographic purposes)
- [REJECTED] DES, 3DES (weak)
- [REJECTED] RC4 (broken)
- [REJECTED] ECB mode (reveals patterns)

**Current Algorithms (REQUIRED):**
- [APPROVED] SHA-256, SHA-3, BLAKE3 (hashing)
- [APPROVED] AES-256-GCM, ChaCha20-Poly1305 (encryption)
- [APPROVED] RSA-2048 or higher, Ed25519 (asymmetric)
- [APPROVED] Argon2id, bcrypt, scrypt (password hashing)

**Common Failures:**

**1. Improper Key Management:**
- Hardcoded keys in code
- Keys stored in version control
- Same key for all environments
- No key rotation

**2. Insufficient Randomness:**
```
// BAD
Math.random()  // Predictable

// GOOD
crypto.getRandomValues()  // Cryptographically secure
```

**3. Improper Implementation:**
- Using encryption without authentication (use AEAD modes)
- Reusing initialization vectors (IV must be unique)
- Not validating TLS certificates

**4. Password Storage:**

```
// NEVER
passwords.save(password)  // Plaintext

// NEVER
sha256(password)  // No salt, vulnerable to rainbow tables

// CORRECT
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

// Or Argon2id (recommended)
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)
```

**Requirements:**
- Use industry-standard libraries (don't implement your own crypto)
- Use authenticated encryption (AES-256-GCM or ChaCha20-Poly1305)
- Store keys in secrets manager
- Rotate keys every 90 days
- Use TLS 1.3 (not TLS 1.0/1.1/1.2)
- Validate all certificates
- Use CSPRNG for random values
- Use Argon2id or bcrypt for password hashing

**Verification:**
- [ ] No hardcoded encryption keys
- [ ] Using approved algorithms only
- [ ] Keys stored in secrets manager
- [ ] TLS 1.3 enforced
- [ ] Certificates validated
- [ ] Passwords hashed with Argon2id or bcrypt

---

### 6.3 Data Sanitization and Secure Disposal

**The Problem:**
Data doesn't disappear when you delete it. File deletion only removes the reference, data remains on disk.

**Methods:**

**1. Deletion (INSECURE):**
- Removes file reference only
- Data remains on disk
- Easily recoverable

**2. Data Wiping/Overwriting (SECURE for reuse):**
- Overwrites data with random data multiple times
- Follows NIST SP 800-88 standard
- Makes data unrecoverable
- Allows hardware reuse

**3. Physical Destruction (SECURE for disposal):**
- Shredding, crushing, incinerating
- Guarantees data cannot be recovered
- Hardware cannot be reused
- Required for highly sensitive data

**4. Cryptographic Erasure (SECURE for encrypted systems):**
- Destroy encryption keys
- Data becomes permanently unreadable
- Fast and efficient
- Only works if data was encrypted

**NIST 800-88 Standard:**
- **Clear:** Logical overwriting (reuse in same organization)
- **Purge:** Physical/cryptographic destruction (transfer to another organization)
- **Destroy:** Physical destruction (disposal)

**Requirements:**

**When user data is deleted:**
- Overwrite data with NIST 800-88 compliant method
- Don't just mark as deleted
- Document sanitization in audit log

**When hardware is decommissioned:**
- Use certified data wiping software
- Verify 100% data wiped
- Physical destruction if highly sensitive
- Document disposal (who, when, method, certificate)

**When backups are removed:**
- Securely delete backup files
- Remove from all storage locations
- Update backup inventory

**Verification:**
- [ ] Deleted data is overwritten, not just marked as deleted
- [ ] Using NIST 800-88 compliant wiping tools
- [ ] Hardware disposal documented
- [ ] Backup deletion includes all copies

---

## Section 7: Transport and Network Security

### 7.1 HTTPS Enforcement

**The Problem:**
HTTP transmits data in plaintext. Attackers can intercept and read sensitive information.

**Requirements (MANDATORY):**

**1. Use HTTPS for ALL pages:**
```
// Not just login and payment pages
// EVERY page must use HTTPS
```

**2. Redirect HTTP to HTTPS:**

```
// Apache .htaccess
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

// Nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

// Express.js
app.use((req, res, next) => {
  if (!req.secure) {
    return res.redirect('https://' + req.headers.host + req.url)
  }
  next()
})
```

**3. Use Valid Certificates:**
- Obtain from trusted Certificate Authority (Let's Encrypt is free)
- NO self-signed certificates in production
- Renew before expiration

**4. TLS Version:**
```
// Require TLS 1.3 or TLS 1.2 minimum
// Disable TLS 1.0 and TLS 1.1 (deprecated)
ssl_protocols TLSv1.2 TLSv1.3;
```

**5. Strong Cipher Suites:**
```
// Prefer modern, secure ciphers
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;
```

**Verification:**
- [ ] All pages use HTTPS
- [ ] HTTP automatically redirects to HTTPS
- [ ] Using valid certificate from trusted CA
- [ ] TLS 1.2 or 1.3 enforced
- [ ] Strong cipher suites configured

---

### 7.2 HTTP Strict Transport Security (HSTS)

**Definition:**
HTTP header that forces browsers to use HTTPS for all future requests.

**How It Works:**

```
// Server sends header
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

// Browser remembers for 1 year (31536000 seconds)
// All future requests to this domain use HTTPS automatically
// Applies to subdomains too
```

**Why Critical:**
- Prevents SSL stripping attacks
- Prevents users from clicking through certificate warnings
- Enforces HTTPS even if user types http://

**Implementation:**

```
// Apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

// Nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

// Express.js
const helmet = require('helmet')
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}))
```

**HSTS Preload List:**
```
// Submit domain to hstspreload.org
// Browsers will enforce HTTPS even on first visit
// Cannot be easily reversed (choose carefully)
```

**Verification:**
- [ ] HSTS header set with max-age >= 1 year
- [ ] includeSubDomains directive included
- [ ] preload directive included (if eligible)
- [ ] Submitted to HSTS preload list (optional but recommended)

---

### 7.3 Encryption at Rest and in Transit

**Encryption in Transit (HTTPS - covered in 7.1):**
- Protects data while moving between client and server
- Uses TLS/SSL

**Encryption at Rest:**
- Protects data while stored on disk
- Protects against physical theft or unauthorized access

**What to Encrypt at Rest:**

**1. Databases:**
```
// PostgreSQL
ALTER SYSTEM SET ssl = on;

// MySQL
ssl_ca=/path/to/ca.pem
ssl_cert=/path/to/server-cert.pem
ssl_key=/path/to/server-key.pem

// MongoDB
security:
  enableEncryption: true
  encryptionKeyFile: /path/to/keyfile
```

**2. File Storage:**
```
// Encrypt sensitive files before storing
// Use AES-256-GCM or ChaCha20-Poly1305

import cryptography
cipher = Fernet(encryption_key)
encrypted_data = cipher.encrypt(file_data)
storage.save(encrypted_data)
```

**3. Backups:**
```
// Encrypt all backups
tar -czf - /data | openssl enc -aes-256-cbc -out backup.tar.gz.enc
```

**4. Cloud Storage:**
```
// Enable encryption in cloud providers
// AWS S3: Server-Side Encryption (SSE-S3, SSE-KMS)
// Google Cloud Storage: Customer-managed encryption keys
// Azure Blob Storage: Customer-managed keys
```

**Field-Level Encryption:**
```
// Encrypt specific sensitive fields in database
// Examples: credit card, SSN, passwords

CREATE TABLE users (
  id INT,
  email VARCHAR(255),
  password_hash VARCHAR(255),
  credit_card BYTEA  -- Encrypted
);
```

**Verification:**
- [ ] Database encryption enabled
- [ ] Sensitive files encrypted
- [ ] Backups encrypted
- [ ] Cloud storage encryption enabled
- [ ] Sensitive database fields encrypted

---

## Section 8: Database Security

### 8.1 Row Level Security (RLS)

**Definition:**
Database-level access control that restricts which rows users can access.

**The Problem:**

```
// Application code
SELECT * FROM documents WHERE user_id = current_user_id

// If application has bug, users could access wrong data
// RLS enforces at database level as final defense
```

**How RLS Works:**

Database automatically filters rows based on user context. Even if application code is buggy, database enforces access control.

**Implementation Examples:**

**PostgreSQL:**

```sql
-- Enable RLS on table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create policy: users can only see their own documents
CREATE POLICY user_documents ON documents
  FOR SELECT
  USING (user_id = current_setting('app.current_user_id')::int);

-- Create policy: users can only modify their own documents
CREATE POLICY user_documents_write ON documents
  FOR ALL
  USING (user_id = current_setting('app.current_user_id')::int);

-- In application, set user context
SET SESSION app.current_user_id = '123';
```

**Supabase (Built-in RLS):**

```sql
-- Enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy using auth.uid()
CREATE POLICY "Users can view own documents"
  ON documents FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can modify own documents"
  ON documents FOR ALL
  USING (auth.uid() = user_id);
```

**Benefits:**
- Defense in depth (database enforces even if application fails)
- Prevents data leakage from application bugs
- Centralized access control
- Required for multi-tenant applications

**Use Cases:**

**Multi-Tenant SaaS:**
```sql
-- Each tenant can only access their own data
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::int);
```

**User ISOLATION:**
```sql
-- Users can only access their own records
CREATE POLICY user_isolation ON profiles
  USING (user_id = current_setting('app.user_id')::int);
```

**Role-Based:**
```sql
-- Admins can see all, users only see own
CREATE POLICY admin_all ON documents
  USING (
    current_setting('app.user_role') = 'admin'
    OR user_id = current_setting('app.user_id')::int
  );
```

**Verification:**
- [ ] RLS enabled on all user-data tables
- [ ] Policies created for SELECT, INSERT, UPDATE, DELETE
- [ ] Policies tested with different user contexts
- [ ] Application sets user context before queries

---

## Section 9: Rate Limiting and Bot Prevention

### 9.1 Rate Limiting

**Definition:**
Restricting the number of requests a user/IP can make within a time window.

**Why Critical:**
- Prevents brute force attacks
- Prevents denial of service
- Prevents API abuse
- Reduces infrastructure costs

**Rate Limit Recommendations:**

**Authentication Endpoints:**
```
Login: 5 attempts per 15 minutes per IP
Password Reset: 3 attempts per hour per email
Registration: 5 attempts per hour per IP
```

**API Endpoints:**
```
Public API: 100 requests per hour per IP
Authenticated API: 1000 requests per hour per user
Admin API: 10,000 requests per hour per admin
```

**Implementation Strategies:**

**1. Fixed Window:**
```
// Simple but has burst problem
// User can make 100 requests at 9:59, another 100 at 10:00

if (requests_this_hour >= 100):
  reject()
```

**2. Sliding Window (RECOMMENDED):**
```
// More accurate, prevents burst
// Counts requests in rolling 60-minute window

requests_in_last_hour = count_requests(current_time - 1 hour, current_time)
if (requests_in_last_hour >= 100):
  reject()
```

**3. Token Bucket:**
```
// Allows bursts but limits average rate
// User gets tokens at fixed rate, spends tokens per request

tokens = min(max_tokens, current_tokens + (time_passed * refill_rate))
if (tokens >= 1):
  tokens -= 1
  allow_request()
else:
  reject()
```

**Implementation Tools:**

```python
# Redis-based rate limiting
from redis import Redis
import time

redis = Redis()

def rate_limit(key, max_requests, window_seconds):
    current = int(time.time())
    window_start = current - window_seconds
    
    # Remove old requests
    redis.zremrangebyscore(key, 0, window_start)
    
    # Count requests in window
    requests = redis.zcard(key)
    
    if requests < max_requests:
        redis.zadd(key, {current: current})
        redis.expire(key, window_seconds)
        return True
    
    return False

# Usage
if not rate_limit(f"login:{ip_address}", 5, 900):  # 5 per 15 min
    return error("Too many attempts")
```

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1640995200

// 429 Too Many Requests
{
  "error": "Rate limit exceeded",
  "retry_after": 3600
}
```

**Verification:**
- [ ] Rate limiting on authentication endpoints
- [ ] Rate limiting on API endpoints
- [ ] Different limits for different endpoint types
- [ ] Appropriate response headers
- [ ] Logged rate limit violations

---

### 9.2 CAPTCHA Implementation

**Definition:**
Challenge-Response test to distinguish humans from bots.

**When to Use CAPTCHA:**
- Registration forms (prevent bot signups)
- Login forms (after failed attempts)
- Password reset (prevent email bombing)
- Contact forms (prevent spam)
- Comment submission (prevent spam)
- Any public form vulnerable to abuse

**CAPTCHA Types:**

**1. reCAPTCHA v3 (RECOMMENDED):**
```
// Invisible, scores user behavior
// No user interaction needed
// Returns score 0.0 (bot) to 1.0 (human)

<script src="https://www.google.com/recaptcha/api.js?render=YOUR_SITE_KEY"></script>

grecaptcha.execute('YOUR_SITE_KEY', {action: 'login'}).then(function(token) {
  // Send token to server for verification
})

// Server-side verification
score = verify_recaptcha(token)
if (score < 0.5):
  require_additional_verification()
```

**2. reCAPTCHA v2 (Checkbox):**
```
// "I'm not a robot" checkbox
// Simple image challenges

<div class="g-recaptcha" data-sitekey="YOUR_SITE_KEY"></div>
```

**3. hCaptcha (Privacy-Focused Alternative):**
```
// Similar to reCAPTCHA but more privacy-friendly

<div class="h-captcha" data-sitekey="YOUR_SITE_KEY"></div>
```

**Implementation Best Practices:**

**1. Progressive CAPTCHA:**
```
// Don't show CAPTCHA to every user
// Only after suspicious activity

failed_login_attempts = get_failed_attempts(ip_address)

if (failed_login_attempts >= 3):
  require_captcha()
```

**2. Multiple Protections:**
```
// Combine CAPTCHA with rate limiting
// CAPTCHA alone can be bypassed with services

if (rate_limit_exceeded() or suspicious_activity()):
  require_captcha()
```

**3. Accessibility:**
```
// Provide audio alternative
// Support keyboard navigation
// Don't rely solely on visual challenges
```

**Server-Side Verification (MANDATORY):**

```python
import requests

def verify_recaptcha(token, remote_ip):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token,
        'remoteip': remote_ip
    })
    
    result = response.json()
    
    if not result['success']:
        return False
    
    # For reCAPTCHA v3, check score
    if 'score' in result:
        return result['score'] >= 0.5
    
    return True
```

**Verification:**
- [ ] CAPTCHA on registration
- [ ] CAPTCHA on password reset
- [ ] CAPTCHA on contact forms
- [ ] CAPTCHA after multiple failed login attempts
- [ ] Server-side verification implemented
- [ ] Accessibility alternatives provided

---

## Section 10: Logging and Monitoring

### 10.1 Tamper-Proof Audit Logging

**Why Critical:**
Tamper-proof logging is cornerstone of robust audit trail management. Required for:
- Legal defensibility
- Compliance demonstrations
- Forensic investigations
- Insider threat detection

**What to Log:**

**Authentication Events:**
- Login attempts (success and failure)
- Logout events
- Password changes
- MFA challenges
- Account lockouts

**Authorization Events:**
- Access granted
- Access denied
- Permission changes
- Role assignments

**Data Access:**
- Who viewed what resource
- When it was accessed
- From what IP address/location

**Data Modification:**
- Who changed what
- Old value → New value
- Timestamp
- Reason (if applicable)

**Administrative Actions:**
- User creation/deletion
- Permission changes
- Configuration changes
- System shutdowns/restarts

**Security Events:**
- Rate limit violations
- Suspicious activity patterns
- Failed authentication patterns
- Unusual access patterns

**Immutability Requirements:**

**Write-Once, Read-Many (WORM) Storage:**
- Logs cannot be modified after writing
- Logs cannot be deleted (only archived after retention period)

**Cryptographic Chaining:**
Each log entry includes hash of previous entry:

```json
{
  "timestamp": "2025-12-29T22:15:30.123Z",
  "user_id": "user_12345",
  "action": "data_modified",
  "resource_id": "record_456",
  "result": "success",
  "ip_address": "192.168.1.100",
  "changes": {
    "field_name": {"old": "value1", "new": "value2"}
  },
  "previous_hash": "a3f2d8e9b1c4...",
  "signature": "digital_signature_here"
}
```

**Storage Requirements:**
- Separate secure location (not same server as application)
- Encrypted at rest and in transit
- Access controls (only authorized audit personnel)
- Disaster recovery (logs must survive system failure)
- Retention policy (comply with legal requirements)

**Fail-Safe Design:**
If logging fails, system must **fail closed** (deny operation), not **fail open** (allow operation without logging).

**Verification:**
- [ ] All sensitive operations logged
- [ ] Logs use cryptographic chaining
- [ ] Logs stored separately and securely
- [ ] Log tampering detected
- [ ] Fail-safe behavior implemented

---

## Section 11: Error Handling

### 11.1 Secure Error Handling

**The Problem:**
Detailed error messages disclose sensitive information about the system.

**What Attackers Learn from Errors:**
- Technology stack (ASP.NET, Django, Rails)
- Database type (PostgreSQL, MySQL, Oracle)
- File paths (`/var/www/app/src/database.rs`)
- Library versions (vulnerable versions?)
- SQL queries (database structure)
- API keys in stack traces

**Bad Error Handling:**

```
Frontend displays:
"Error: FATAL: password authentication failed for user 'app_admin' 
at database host 'db-primary.internal:5432' 
in /opt/app/src/database/connection.rs:45"

Attacker now knows:
- Database: PostgreSQL (port 5432)
- User: app_admin
- Host: db-primary.internal
- Language: Rust
- File structure
```

**Good Error Handling:**

```
Frontend displays:
"An error occurred. Please try again later. (Error ID: e7f3a9b2)"

Backend logs (internal only):
"[e7f3a9b2] Database connection failed: authentication error 
for user app_admin at db-primary.internal:5432"
```

**Requirements:**

**User-Facing Errors (Generic):**
- "An error occurred"
- "Invalid request"
- "Access denied"
- "Service temporarily unavailable"
- Include error ID for support (not technical details)

**Internal Logs (Detailed):**
- Full stack trace
- Database errors
- File paths
- Technical details
- Link error ID to log entry

**Environment-Specific:**
- Production: Generic errors only
- Staging: Slightly more detail (still safe)
- Development: Full errors (local only)

**Fail-Safe Design:**
Security checks should **deny by default** if error occurs. Fail closed, not fail open.

**Verification:**
- [ ] No stack traces exposed to users
- [ ] No database errors exposed to users
- [ ] No file paths exposed to users
- [ ] No library versions exposed to users
- [ ] Detailed errors logged internally
- [ ] Unique error IDs for tracing
- [ ] Different error verbosity per environment

---

## Section 12: Dependency Management

### 12.1 Dependency Security

**The Problem:**
Third-party dependencies can introduce vulnerabilities into your application.

**Why Critical:**
- 80% of code in modern applications is third-party
- Vulnerabilities in dependencies affect your app
- Supply chain attacks target popular packages
- Outdated dependencies have known exploits

**Vulnerability Management:**

**1. Scan Dependencies Regularly:**

```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
pip install --upgrade package-name

# Rust
cargo audit

# Ruby
bundle audit

# Java
dependency-check

# Go
go list -m all | nancy sleuth
```

**2. Automate Dependency Updates:**

```
// Dependabot (GitHub)
// Renovate Bot
// Snyk

// Automatically creates PRs for dependency updates
// Includes vulnerability information
// Prioritizes security updates
```

**3. Review Before Installing:**

```
// Check before `npm install unknown-package`
- Download count (popular = more eyes)
- Last update date (maintained?)
- Open issues count
- GitHub stars
- License
- Known vulnerabilities
```

**4. Lock Dependencies:**

```
// package-lock.json (Node.js)
// Pipfile.lock (Python)
// Cargo.lock (Rust)
// Gemfile.lock (Ruby)

// Ensures exact versions deployed
// Prevents unexpected updates
// Commit to version control
```

**5. Minimize Dependencies:**

```
// Only install what you need
// Fewer dependencies = smaller attack surface
// Review package.json/requirements.txt regularly
// Remove unused dependencies
```

**6. Private Package Registry:**

```
// For sensitive projects
// Host your own package registry
// Scan packages before adding to registry
// Control what enters your organization
```

**Supply Chain Attacks:**

**Examples:**
- event-stream (2018): Malicious code added to steal Bitcoin
- ua-parser-js (2021): Malware distributed via npm
- colors.js (2022): Maintainer sabotaged own package

**Prevention:**
- Use package lock files
- Verify package signatures
- Use Subresource Integrity (SRI) for CDN resources
- Review dependency updates before merging
- Use security scanning tools

**Verification:**
- [ ] Dependencies scanned weekly
- [ ] Automated updates configured
- [ ] Lock files committed
- [ ] No critical vulnerabilities present
- [ ] Unused dependencies removed
- [ ] SRI implemented for CDN resources

---

## Section 13: Compliance Standards

### 13.1 ISO 27001

**Definition:**
International standard for Information Security Management Systems (ISMS).

**CIA Triad:**
1. **Confidentiality:** Prevent unauthorized access
2. **Integrity:** Prevent unauthorized modification
3. **Availability:** Ensure systems accessible when needed

**Requirements:**
- Information Security Management System (ISMS)
- Risk assessment process
- Security controls implementation
- Regular audits
- Incident response procedures
- Business continuity planning
- Management commitment
- Continual improvement

**Benefits:**
- Demonstrates security commitment to clients
- Required for government/enterprise contracts
- Supports GDPR, HIPAA, PCI-DSS compliance
- Reduces risk of data breaches
- Improves organizational security culture

**Implementation:**
- Document security policies
- Conduct risk assessments
- Implement security controls
- Train employees
- Monitor and review
- Maintain audit trail
- Annual certification audit

---

### 13.2 NIST Standards

**NIST SP 800-53:** Security and Privacy Controls

Comprehensive catalog covering:
- Access control
- Awareness and training
- Audit and accountability
- Security assessment and authorization
- Configuration management
- Contingency planning
- Identification and authentication
- Incident response
- Maintenance
- Media protection
- Physical and environmental protection
- Planning
- Personnel security
- Risk assessment
- System and services acquisition
- System and communications protection
- System and information integrity

**NIST SP 800-171:** Protecting Controlled Unclassified Information (CUI)

Required for:
- Government contractors
- Organizations handling CUI
- Defense industrial base

**NIST SP 800-88:** Media Sanitization

Guidelines for:
- Secure data deletion
- Hardware disposal
- Clear, Purge, Destroy methods

**NIST Cybersecurity Framework:**
- Identify
- Protect
- Detect
- Respond
- Recover

---

### 13.3 PCI DSS (Payment Card Security)

**Critical for any system that processes, stores, or transmits payment card data.**

**12 Requirements:**

1. Install and maintain firewall configuration to protect cardholder data
2. Do not use vendor-supplied defaults for system passwords and security parameters
3. Protect stored cardholder data
4. Encrypt transmission of cardholder data across open, public networks
5. Protect all systems against malware and regularly update anti-virus software
6. Develop and maintain secure systems and applications
7. Restrict access to cardholder data by business need-to-know
8. Identify and authenticate access to system components
9. Restrict physical access to cardholder data
10. Track and monitor all access to network resources and cardholder data
11. Regularly test security systems and processes
12. Maintain a policy that addresses information security for all personnel

**Critical Change (March 31, 2025):**
Multi-Factor Authentication (MFA) is **MANDATORY** for all access to cardholder data environment.

**Requirements for Payment Systems:**
- Never store CVV/CVC codes (forbidden)
- Encrypt cardholder data at rest (AES-256)
- Encrypt in transit (TLS 1.2 minimum, TLS 1.3 recommended)
- Mask card numbers (show only last 4 digits)
- Implement MFA for all access
- Log all access to payment data
- Quarterly vulnerability scans
- Annual penetration testing
- Network segmentation
- Firewall between internet and cardholder data
- Regular security awareness training

**Compliance Levels:**
- Level 1: 6M+ transactions/year - Annual on-site audit
- Level 2: 1M-6M transactions/year - Annual Self-Assessment Questionnaire
- Level 3: 20K-1M e-commerce transactions/year - Annual SAQ
- Level 4: <20K e-commerce transactions/year - Annual SAQ

**Verification:**
- [ ] PCI DSS compliance level determined
- [ ] All 12 requirements implemented
- [ ] MFA implemented
- [ ] Quarterly scans scheduled
- [ ] Annual audit/SAQ completed
- [ ] Compliance maintained continuously

---

## Complete Security Checklist

**Before EVERY commit, verify ALL of these:**

### Access Control
- [ ] Every endpoint checks authentication and authorization
- [ ] Users cannot access other users' data
- [ ] Admin functions reject non-admin users
- [ ] Least privilege principle applied
- [ ] Separation of duties enforced (where applicable)
- [ ] Row Level Security (RLS) enabled on user-data tables

### Secrets Management
- [ ] No hardcoded API keys, passwords, tokens
- [ ] All secrets in environment variables or Secret Manager
- [ ] `.env` files in `.gitignore`
- [ ] Encryption keys stored securely
- [ ] Key rotation schedule implemented

### Input Validation
- [ ] All user inputs validated (frontend + backend)
- [ ] SQL queries use parameterized statements (NEVER string concatenation)
- [ ] File uploads validated (type, size, content, magic bytes)
- [ ] HTML output escaped (XSS prevention)
- [ ] Whitelist validation used where possible

### Authentication & Session Management
- [ ] MFA implemented for administrative access
- [ ] Session tokens properly managed (HttpOnly, Secure, SameSite)
- [ ] Access tokens expire in 15-30 minutes
- [ ] Password change invalidates all tokens
- [ ] CSRF tokens on all state-changing forms

### Encryption & Transport
- [ ] HTTPS enforced on all endpoints
- [ ] HTTP redirects to HTTPS
- [ ] HSTS headers set (max-age >= 1 year)
- [ ] Data encrypted at rest and in transit
- [ ] Using approved encryption algorithms (AES-256-GCM, ChaCha20-Poly1305)
- [ ] TLS 1.3 or TLS 1.2 minimum enforced
- [ ] Passwords hashed with Argon2id or bcrypt

### request Security
- [ ] CSRF protection implemented
- [ ] SameSite cookie attribute set
- [ ] SSRF prevention (URL whitelist)
- [ ] Internal IPs blacklisted for user-provided URLs

### Rate Limiting & Bot Prevention
- [ ] Rate limiting on authentication endpoints
- [ ] Rate limiting on API endpoints
- [ ] CAPTCHA on registration
- [ ] CAPTCHA on password reset
- [ ] CAPTCHA on contact forms
- [ ] CAPTCHA after multiple failed login attempts

### Logging & Monitoring
- [ ] All sensitive operations logged
- [ ] Logs are tamper-proof (cryptographic chaining)
- [ ] Logs stored securely separately
- [ ] Access attempts logged
- [ ] Failed authentication attempts logged
- [ ] Fail-safe logging (fail closed if logging fails)

### Error Handling
- [ ] No stack traces exposed to users
- [ ] No database errors exposed to users
- [ ] No file paths exposed to users
- [ ] No library versions exposed to users
- [ ] Error IDs used for tracking
- [ ] Detailed errors logged internally only
- [ ] Different error verbosity per environment

### Dependencies
- [ ] Dependencies up-to-date (no critical vulnerabilities)
- [ ] Run `npm audit` / `cargo audit` / `pip-audit` before commit
- [ ] Dependabot or Renovate enabled
- [ ] Lock files committed
- [ ] Unused dependencies removed

### Data Protection
- [ ] Sensitive data encrypted
- [ ] Data sanitization on deletion (NIST 800-88)
- [ ] Secure disposal procedures documented
- [ ] Field-level encryption for highly sensitive data

**If ANY checkbox fails → STOP and fix before committing.**

---

## Version

Security Canon Version: 1.0 (December 29, 2025)  
Based on OWASP Top 10 (2024), NIST 800-53, ISO 27001, PCI DSS

Covers 25 comprehensive security areas across all domains of application security.
