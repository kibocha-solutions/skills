# Token and Session Signing

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

## Strategy 1: Signed Cookies (HMAC)

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

## Strategy 2: JWT Signature Verification (MANDATORY)

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

## Strategy 3: Server-Side Session Validation

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

## Strategy 4: Session ID Rotation

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

## Strategy 5: Anti-Tampering Checksums

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
