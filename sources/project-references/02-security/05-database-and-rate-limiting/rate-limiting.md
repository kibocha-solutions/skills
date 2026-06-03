# Rate Limiting and Bot Prevention

## 9.1 Rate Limiting

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

## 9.2 CAPTCHA Implementation

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
