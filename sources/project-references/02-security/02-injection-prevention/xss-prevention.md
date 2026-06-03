# Cross-Site Scripting (XSS) Prevention

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
