# Error Handling

## 11.1 Secure Error Handling

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
