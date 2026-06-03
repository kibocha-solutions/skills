# Session Management Security

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
