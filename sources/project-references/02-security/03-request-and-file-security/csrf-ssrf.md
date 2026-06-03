# Request Security

## 4.1 Cross-Site Request Forgery (CSRF) Protection

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

## 4.2 Server-Side Request Forgery (SSRF) Prevention

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
