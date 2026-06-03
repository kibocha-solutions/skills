# Input Validation

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
