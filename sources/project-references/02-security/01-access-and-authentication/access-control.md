# Access Control and Authorization

## 1.1 Broken Access Control (OWASP #1 - CRITICAL)

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

## 1.2 Role-Based Access Control (RBAC)

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

## 1.3 Attribute-Based Access Control (ABAC)

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

## 1.4 Least Privilege Principle

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

## 1.5 Separation of Duties

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
