# Database Security

## 8.1 Row Level Security (RLS)

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

**User Isolation:**
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
