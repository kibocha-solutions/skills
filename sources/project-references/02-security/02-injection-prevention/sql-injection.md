# SQL Injection Prevention

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
