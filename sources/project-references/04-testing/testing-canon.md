# Testing Canon: Comprehensive Testing Standards

This document provides comprehensive, non-negotiable testing standards for all projects following the Vibe Code Canon framework.

**Authority:** These standards have ABSOLUTE AUTHORITY and MUST be followed alongside the testing practices in agent instructions. All examples provided are for contextual purposes ONLY and should not be assumed to be part of the testing canon or project requirements.

---

## Section 1: Testing Philosophy and Core Principles

### 1.1 Shift-Left Testing

**Definition:**
Testing activities start at the earliest stages of development, not as an afterthought.

**Why Critical:**
- Catches bugs when cheapest to fix (requirements/design phase)
- Reduces rework time by 90%
- Prevents bugs from reaching production
- 10x cheaper to fix bugs in development vs production

**Implementation:**

**Involve QA Early:**
- QA engineers review requirements before development starts
- Identify testability issues in design phase
- Participate in sprint planning

**Static Analysis During Development:**
- Use linters and type checkers
- Run security scanners (SAST)
- Enforce code quality gates

**Developer Testing:**
- Train developers in testing techniques
- Write tests before or during development
- Code review includes test review

**CI/CD Integration:**
- Automated tests run on every commit
- Fast feedback (< 1 minute for unit tests)
- Block merge if tests fail

---

### 1.2 Risk-Based Testing

**Definition:**
Prioritize testing efforts based on risk assessment (business impact + technical complexity).

**Risk Assessment Framework:**

**Step 1: Identify Business-Critical Functions**

Collaborate with stakeholders to identify:
- Revenue-generating features
- Regulatory/compliance functions
- Reputation-impacting features
- User safety functions

**Step 2: Analyze Historical Data**

Review:
- Past bug reports (which areas break most?)
- Production incidents (what caused outages?)
- Customer complaints (what frustrates users?)

**Step 3: Assess Technical Complexity**

High complexity areas:
- Complex integrations (third-party APIs, payment gateways)
- Complex algorithms (financial calculations, data processing)
- Concurrent/distributed systems
- Legacy code with poor documentation

**Step 4: Create Risk Profile**

| Risk Level | Testing Strategy |
|-----------|-----------------|
| **High Risk** (High impact + High complexity) | Maximum testing: Unit + Integration + E2E + Manual + Security + Performance |
| **Medium Risk** (Moderate impact or complexity) | Automated testing: Unit + Integration + Smoke E2E |
| **Low Risk** (Low impact and low complexity) | Basic testing: Unit tests + Code review |

**Step 5: Update Regularly**

- Re-evaluate risk quarterly
- Update after major incidents
- Adjust as product evolves

---

### 1.3 Test-Driven Development (TDD)

**The TDD Cycle:**

```
1. Write test (RED - test fails because feature doesn't exist)
2. Write minimal code to pass test (GREEN - test passes)
3. Refactor code (REFACTOR - improve while keeping tests green)
4. Repeat
```

**Benefits:**

**Better Code Design:**
- [APPROVED] Forces modular, testable code
- [APPROVED] Prevents tight coupling
- [APPROVED] Encourages interface design

**Reduced Rework Time:**
- [APPROVED] No new code until existing code passes tests
- [APPROVED] Failures addressed immediately
- [APPROVED] Minimal time spent fixing broken code

**Quick Feedback:**
- [APPROVED] Tests focus on specific code sections
- [APPROVED] Immediate feedback on changes
- [APPROVED] Fast iteration cycle

**Living Documentation:**
- [APPROVED] Tests document expected behavior
- [APPROVED] Always up-to-date (unlike written docs)

**When to Use TDD:**
- New features with clear requirements
- Complex business logic
- Critical functionality (payment, security, data integrity)
- Refactoring existing code

**When NOT to Use TDD:**
- Exploratory prototyping (requirements unclear)
- UI design iteration (rapidly changing)
- Research/spike work

---

### 1.4 Behavior-Driven Development (BDD)

**Definition:**
Team methodology involving multiple stakeholders to define expected software behavior in business language.

**BDD vs TDD:**

| Factor | TDD | BDD |
|--------|-----|-----|
| **Scope** | Development practice focused on code quality | Team methodology involving multiple stakeholders |
| **Test Creation** | Tests written before code | Scenarios written before tests, defining behavior |
| **Language** | Technical (code-focused) | Business language (user-focused) |
| **Audience** | Developers | Developers, QA, Product Owners, Stakeholders |
| **Focus** | Code correctness | User experience and business requirements |

**BDD Scenario Format (Gherkin):**

```gherkin
Feature: User Login

Scenario: Successful login with valid credentials
  Given the user is on the login page
  And the user has valid credentials
  When the user enters username "john@example.com"
  And the user enters password "SecurePass123"
  And the user clicks "Login" button
  Then the user should be redirected to dashboard
  And the user should see welcome message "Welcome, John"
```

**Benefits:**

**Better Test Coverage:**
- [APPROVED] Multiple user scenarios defined upfront
- [APPROVED] Reflects real-world usage
- [APPROVED] Meets user expectations, not just code accuracy

**Stakeholder Collaboration:**
- [APPROVED] Business analysts understand scenarios
- [APPROVED] Product owners validate requirements
- [APPROVED] Shared understanding across team

**Keeping Functionality Intact:**
- [APPROVED] Scenarios define features that must remain intact during refactoring
- [APPROVED] Ensures user experience preserved

**When to Use BDD:**
- Complex user workflows
- Multiple stakeholders need clarity
- User experience critical
- Regulatory requirements (need human-readable tests)

---

## Section 2: The Testing Pyramid

### 2.1 The Ideal Distribution

```
        E2E Tests (10%)
      Slow, expensive, brittle
      
    Integration Tests (20%)
  Medium speed, moderate cost
  
      Unit Tests (70%)
   Fast, cheap, reliable
```

**Recommended Distribution:**
- **70% Unit Testing** – Fast feedback, catch logic errors early
- **20% Integration Testing** – Verify component interactions
- **10% E2E Testing** – Cover critical user paths only

---

### 2.2 Why This Distribution?

**1. Economic Optimization**

**Cost per Bug Found:**
- Unit tests: Pennies to run/maintain, catch 70% of bugs
- Integration tests: Dollars, catch 20% more bugs
- E2E tests: Hundreds of dollars, catch final 10%

**Result:** Maximum bug detection with minimum investment.

---

**2. Rapid Feedback**

**Feedback Speed:**
- Unit tests: Results in seconds
- Integration tests: Results in minutes
- E2E tests: Results in hours

**Developer Experience:**
- Fix issues while code fresh in mind
- Catch problems before context switching
- Validate features before memory fades

**Result:** Maintains development flow while ensuring quality.

---

**3. Coverage Efficiency**

**Typical Pyramid Coverage:**
- Unit tests: 80% code coverage
- Integration tests: 60% API coverage
- E2E tests: 30% user journey coverage

**Anti-Pattern Alternative:**
[REJECTED] Attempting same coverage with only E2E tests would require thousands of slow, brittle tests, making continuous delivery impossible.

---

**4. CI/CD Pipeline Integration**

**Staged Testing:**
- **Every commit:** Unit tests (< 1 minute)
- **Every PR:** Integration tests (< 10 minutes)
- **Every deployment:** E2E smoke tests (< 30 minutes)
- **Nightly:** Comprehensive E2E suite (hours)

**Pipeline Configuration:**
- Fail fast: Run unit tests first, then integration, then E2E
- Quick feedback on common problems
- Comprehensive validation before release
- Parallel execution: Unit tests across CPU cores, integration tests across containers, E2E tests across browser instances

---

## Section 3: Unit Testing

### 3.1 Characteristics

**What Unit Tests Do:**
- Test smallest testable parts (functions, methods, classes)
- Test in isolation (no external dependencies)
- Fast execution (milliseconds per test)
- No network calls, database access, or file I/O

**When to Write:**
- Every new function/method
- Complex business logic
- Edge cases and boundary conditions
- Error handling paths

---

### 3.2 Best Practices

**1. Test One Thing Per Test**

```javascript
// [REJECTED] BAD: Tests multiple things
test('user validation', () => {
  expect(validateEmail('test@example.com')).toBe(true)
  expect(validatePassword('Pass123')).toBe(true)
  expect(validateAge(25)).toBe(true)
})

// [APPROVED] GOOD: Separate tests
test('should validate email format', () => {
  expect(validateEmail('test@example.com')).toBe(true)
})

test('should validate password strength', () => {
  expect(validatePassword('Pass123')).toBe(true)
})

test('should validate age is positive', () => {
  expect(validateAge(25)).toBe(true)
})
```

---

**2. Descriptive Test Names**

**Format:** `should [expected behavior] when [condition]`

```javascript
// [REJECTED] BAD
test('test1', () => { ... })
test('cart', () => { ... })

// [APPROVED] GOOD
test('should return 0 when cart is empty', () => { ... })
test('should throw error when user is underage', () => { ... })
test('should apply discount when user is premium member', () => { ... })
```

---

**3. Arrange-Act-Assert (AAA) Pattern**

```javascript
test('should calculate total with discount', () => {
  // Arrange: Setup test data
  const cart = { items: [10, 20, 30], discount: 0.1 }
  
  // Act: Execute function under test
  const total = calculateTotal(cart)
  
  // Assert: Verify result
  expect(total).toBe(54) // (10+20+30) * 0.9
})
```

**Benefits:**
- Clear test structure
- Easy to understand
- Easy to maintain
- Consistent across codebase

---

**4. Test Independence**

**Each test must be independent:**

```javascript
// [REJECTED] BAD: Tests depend on shared state
let user = null

test('should create user', () => {
  user = createUser({ name: 'John' })
  expect(user.name).toBe('John')
})

test('should update user', () => {
  user.name = 'Jane'  // Depends on previous test
  expect(user.name).toBe('Jane')
})

// [APPROVED] GOOD: Tests are independent
test('should create user', () => {
  const user = createUser({ name: 'John' })
  expect(user.name).toBe('John')
})

test('should update user', () => {
  const user = createUser({ name: 'John' })
  user.name = 'Jane'
  expect(user.name).toBe('Jane')
})
```

**Requirements:**
- [ ] Tests can run in any order
- [ ] Tests don't share state
- [ ] Each test cleans up after itself
- [ ] Tests don't depend on previous tests

---

**5. Test Edge Cases**

**Always test:**
- Empty inputs (empty string, empty array, null, undefined)
- Boundary values (0, -1, maximum values)
- Invalid inputs (wrong type, out of range)
- Error conditions (network failure, database error)

```javascript
describe('calculateDiscount', () => {
  test('should return 0 for empty cart', () => {
    expect(calculateDiscount([])).toBe(0)
  })
  
  test('should return 0 for negative total', () => {
    expect(calculateDiscount(-100)).toBe(0)
  })
  
  test('should cap discount at 50%', () => {
    expect(calculateDiscount(100, 0.75)).toBe(50) // Max 50% discount
  })
  
  test('should throw error for invalid discount', () => {
    expect(() => calculateDiscount(100, -0.1)).toThrow('Invalid discount')
  })
})
```

---

### 3.3 Unit Test Speed

**Target:** Unit tests must be FAST.

**Speed Requirements:**
- Individual test: < 100ms
- Entire suite: < 1 minute for 1000 tests

**How to Achieve:**
- No network calls (use mocks)
- No database access (use in-memory or mocks)
- No file I/O (use mocks)
- No sleep/wait statements
- Minimize setup/teardown complexity

---

## Verification Checklist - Part 1

**Before proceeding, verify:**

### Testing Philosophy
- [ ] Shift-left testing implemented (QA involved early)
- [ ] Risk-based testing approach defined
- [ ] TDD vs BDD decision made for project
- [ ] Testing culture established

### Testing Pyramid
- [ ] 70/20/10 distribution target set
- [ ] Economic justification understood
- [ ] CI/CD integration planned
- [ ] Parallel execution configured

### Unit Testing
- [ ] One assertion per test enforced
- [ ] Descriptive test naming convention
- [ ] AAA pattern followed
- [ ] Test independence verified
- [ ] Edge cases covered
- [ ] Speed requirements met (< 1 minute for suite)

---

## Section 4: Integration Testing

### 4.1 Characteristics

**What Integration Tests Do:**
- Test interactions between components/modules
- Verify data flows correctly between layers
- Test with real dependencies (databases, APIs, file systems)
- Slower than unit tests (seconds to minutes)

**When to Write:**
- Database operations (CRUD)
- API endpoint behavior
- Service-to-service communication
- External system integrations
- Message queue interactions

---

### 4.2 Best Practices

**1. Test Database Layer**

```python
# [APPROVED] Integration test with real database
def test_user_creation_in_database():
    # Arrange: Setup test database
    db = TestDatabase()
    user_repo = UserRepository(db)
    
    # Act: Create user
    user = user_repo.create(email="test@example.com", name="John")
    
    # Assert: Verify in database
    saved_user = user_repo.find_by_id(user.id)
    assert saved_user.email == "test@example.com"
    assert saved_user.name == "John"
    
    # Cleanup: Rollback transaction
    db.rollback()
```

**Requirements:**
- [ ] Use separate test database (never development or production)
- [ ] Reset database between tests
- [ ] Use transactions and rollback
- [ ] Clean up test data

---

**2. Test API Endpoints**

```javascript
// [APPROVED] Integration test for REST API
test('POST /api/users should create user', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ name: 'John', email: 'john@example.com' })
    .expect(201)
  
  expect(response.body).toHaveProperty('id')
  expect(response.body.name).toBe('John')
  expect(response.body.email).toBe('john@example.com')
})

test('GET /api/users/:id should return user', async () => {
  // Arrange: Create test user
  const user = await createTestUser()
  
  // Act & Assert
  const response = await request(app)
    .get(`/api/users/${user.id}`)
    .expect(200)
  
  expect(response.body.id).toBe(user.id)
})
```

---

**3. Test Service Integration**

```javascript
// [APPROVED] Test multiple services working together
test('order processing should update inventory and send email', async () => {
  // Arrange
  const product = await createTestProduct({ stock: 10 })
  const user = await createTestUser({ email: 'test@example.com' })
  
  // Act
  const order = await orderService.createOrder({
    userId: user.id,
    productId: product.id,
    quantity: 2
  })
  
  // Assert: Check all side effects
  expect(order.status).toBe('confirmed')
  
  // Verify inventory updated
  const updatedProduct = await productService.findById(product.id)
  expect(updatedProduct.stock).toBe(8) // 10 - 2
  
  // Verify email sent
  const emails = await emailService.getSentEmails()
  expect(emails).toContainEqual(
    expect.objectContaining({
      to: 'test@example.com',
      subject: expect.stringContaining('Order Confirmation')
    })
  )
})
```

---

### 4.3 Integration Test Speed

**Target:** Integration tests should be reasonably fast.

**Speed Requirements:**
- Individual test: < 5 seconds
- Entire suite: < 10 minutes

**Optimization Strategies:**
- Use database transactions (rollback instead of delete)
- Run tests in parallel (separate database schemas)
- Use connection pooling
- Minimize setup/teardown complexity

---

## Section 5: End-to-End (E2E) Testing

### 5.1 Characteristics

**What E2E Tests Do:**
- Test complete user workflows
- Test from user's perspective (browser automation)
- Test in production-like environment
- Slowest tests (minutes to hours)

**When to Write:**
- Critical user journeys (login, checkout, payment)
- Multi-step workflows
- Cross-browser compatibility
- Smoke tests for deployment validation

---

### 5.2 Best Practices

**1. Focus on Critical Paths Only**

[REJECTED] Do NOT test every possible workflow with E2E tests.

**Prioritize:**
- Revenue-generating workflows (checkout, payment)
- User authentication (login, signup, password reset)
- Data creation workflows (create post, upload file)
- Critical business processes

**Avoid:**
- Testing every UI variation
- Testing error messages (use unit tests)
- Testing implementation details

---

**2. Make Tests Resilient**

```javascript
// [REJECTED] BAD: Brittle, dependent on exact text
await page.click('button:text("Submit Order")')

// [APPROVED] GOOD: Use data attributes
await page.click('[data-testid="submit-order-button"]')
```

```html
<!-- Add data-testid to critical elements -->
<button data-testid="submit-order-button">Submit Order</button>
<input data-testid="email-input" type="email" />
<div data-testid="success-message">Order confirmed!</div>
```

---

**3. Implement Proper Waits**

```javascript
// [REJECTED] BAD: Fixed wait (flaky)
await page.click('#submit')
await page.waitForTimeout(5000) // Arbitrary wait

// [APPROVED] GOOD: Wait for condition
await page.click('#submit')
await page.waitForSelector('[data-testid="success-message"]', { 
  timeout: 10000 
})
```

**Wait Strategies:**
- Wait for element visibility
- Wait for network idle
- Wait for specific text content
- Never use fixed timeouts

---

**4. Isolate Test Data**

```javascript
// [APPROVED] Create isolated test data for each test
test('user can complete checkout', async () => {
  // Arrange: Create unique test user
  const testEmail = `test-${Date.now()}@example.com`
  await signupUser({ email: testEmail, password: 'Test123!' })
  
  // Act: Perform checkout
  await loginUser(testEmail, 'Test123!')
  await addToCart('product-123')
  await checkout()
  
  // Assert
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible()
})
```

**Requirements:**
- [ ] Each test creates own test data
- [ ] Tests don't share data
- [ ] Tests clean up after themselves (or use separate test database)

---

### 5.3 E2E Test Speed

**Target:** E2E tests will be slow, but manage the slowness.

**Speed Requirements:**
- Individual critical path: < 2 minutes
- Smoke test suite: < 30 minutes
- Comprehensive suite: < 2 hours

**Optimization Strategies:**
- Run in parallel (multiple browser instances)
- Use headless mode for CI/CD
- Cache authentication state
- Skip animations/transitions
- Use API calls for setup/teardown (not UI clicks)

---

## Section 6: Performance Testing

### 6.1 Load Testing

**Definition:**
Evaluate system behavior under anticipated user volumes.

**Purpose:**
- Verify applications meet performance requirements during normal operations
- Establish baseline metrics
- Validate response times, throughput, resource utilization

**Key Metrics:**
- Response time (p50, p95, p99)
- Throughput (requests per second)
- Error rate
- Resource utilization (CPU, memory, disk, network)

**When to Run:**
- Before major releases
- After infrastructure changes
- When adding new features that impact performance
- Monthly (establish trend)

**Best Practices:**

**Define Realistic User Scenarios:**
```
Scenario: E-commerce site
- 70% browse products
- 20% add to cart
- 8% checkout
- 2% create account
```

**Simulate Gradual Ramp-Up:**
```
0-5 min:   10 users  (baseline)
5-10 min:  50 users  (ramp up)
10-30 min: 200 users (sustained load - normal peak)
30-35 min: 50 users  (ramp down)
```

**Maintain Sustained Load:**
- Run at peak normal usage for 20+ minutes
- Verify system remains stable
- No performance degradation over time

---

### 6.2 Stress Testing

**Definition:**
Push systems beyond normal parameters to identify breaking points.

**Purpose:**
- Identify system limits
- Test recovery capabilities
- Reveal failure modes
- Establish safety margins

**Key Metrics:**
- Maximum capacity (users, transactions)
- Failure points (where system breaks)
- System recovery time
- Graceful degradation

**Types:**

**Spike Testing:**
- Sudden, extreme traffic bursts
- Tests reaction to unexpected spikes
- Use case: Black Friday sales, product launches, viral content

```
Normal load:    100 users
Spike:         1000 users (in 1 minute)
Duration:      5 minutes
Return:        100 users
```

**Volume Testing:**
- Heavy data loads
- Tests how application handles large data volumes
- Use case: Bulk data import, report generation

**When to Run:**
- Before high-traffic events
- To prepare for infrastructure limits
- Disaster recovery planning
- Quarterly

---

### 6.3 Soak (Endurance) Testing

**Definition:**
Assess long-term stability under steady load.

**Purpose:**
- Detect memory leaks
- Identify performance degradation over time
- Validate 24/7 availability

**Duration:**
- Minimum: 24 hours
- Recommended: 72+ hours
- Production-grade: 7 days

**What to Monitor:**
- Memory usage (should be stable, not increasing)
- CPU usage (should be consistent)
- Response times (should not degrade)
- Error rates (should remain constant)
- Database connections (should not leak)

**When to Run:**
- Applications with 24/7 availability requirements
- Systems with long user sessions
- After memory-related bug fixes
- Before major version releases

---

### 6.4 Performance Testing Best Practices

**1. Realistic Test Data**

[REJECTED] Unrealistic or incomplete datasets lead to misleading results.

**Requirements:**
- Data must resemble real-world scenarios
- Use production-like data volumes
- Include edge cases (very large files, complex queries)

---

**2. Identify Bottlenecks**

**Common Bottlenecks:**
- Database queries (N+1 queries, missing indexes)
- External API calls (slow third-party services)
- File I/O operations (large file processing)
- Network latency (microservice communication)
- Memory leaks (objects not garbage collected)

**Solution:** Profile application under load, identify bottlenecks, optimize.

---

**3. Monitor Key Metrics**

**Required Metrics:**
- Response time percentiles (p50, p95, p99)
- Error rate (percentage of failed requests)
- Throughput (requests per second)
- Resource utilization (CPU, memory, network, disk)

**Set Thresholds:**
```
p95 response time: < 500ms
p99 response time: < 1000ms
Error rate: < 0.1%
CPU usage: < 70%
Memory usage: < 80%
```

---

**4. Baseline and Compare**

**Establish Performance Baseline:**
- Run performance tests on current version
- Record all metrics
- Store results

**Compare Against Baseline:**
- Run same tests on new version
- Compare metrics
- Fail build if performance regresses > 10%

---

## Section 7: Test Coverage

### 7.1 Coverage Metrics

**1. Statement Coverage**

**Definition:**
Percentage of executable statements executed during testing.

```
Code has 100 statements
Tests execute 75 statements
Statement Coverage = 75%
```

**Limitation:**
- Most basic metric
- Doesn't guarantee branch coverage
- Can miss logical paths

---

**2. Branch Coverage**

**Definition:**
Percentage of code branches (if/else, switch) tested.

```javascript
function checkAge(age) {
  if (age >= 18) {    // Branch 1
    return "Adult"
  } else {            // Branch 2
    return "Minor"
  }
}

// Test 1: checkAge(20) → covers Branch 1 only (50% coverage)
// Test 2: checkAge(15) → covers Branch 2 only (50% coverage)
// Both tests = 100% branch coverage
```

**Better than statement coverage:**
- [APPROVED] Ensures all logical paths tested
- [APPROVED] Catches more bugs

---

**3. Path Coverage**

**Definition:**
All possible execution paths through code tested.

**Problem:** Exponential growth.

```
2 if statements = 4 possible paths
3 if statements = 8 possible paths
10 if statements = 1,024 possible paths
```

**Use ONLY for:**
- Critical algorithms
- Security-sensitive code
- Complex business logic

[REJECTED] Impractical for most code.

---

**4. Modified Condition/Decision Coverage (MC/DC)**

**Definition:**
Each condition shown to independently affect outcome.

**Critical for:**
- Safety-critical systems (aviation, automotive, medical)
- Regulatory requirements (DO-178C for aircraft software)

**Most codebases:** [REJECTED] Too expensive, unnecessary.

---

### 7.2 Coverage Targets

**Is 70%, 80%, 90%, or 100% Good Enough?**

**It depends on context.**

**Recommended Targets:**

| Context | Minimum Coverage | Recommended | Notes |
|---------|-----------------|-------------|-------|
| **General Applications** | 70% | 80% | Focus on critical paths |
| **Business-Critical Functions** | 90% | 95% | Payment, security, data integrity |
| **Safety-Critical Systems** | 100% MC/DC | 100% MC/DC | Aviation, automotive, medical |
| **Prototype/POC** | 0% | 50% | Speed over coverage |
| **Open Source Libraries** | 80% | 90% | High confidence for users |

---

**Why NOT 100% Everywhere:**

**Diminishing Returns:**
- [CAUTION] Last 10% coverage takes 50% of effort
- [CAUTION] Some code impossible to test (OS-level error handling, out-of-memory conditions)

**Coverage ≠ Quality:**
- [CAUTION] High coverage with bad tests = false security
- [CAUTION] 100% coverage doesn't mean bug-free

**Better Metrics Than Coverage Percentage:**
- Mutation testing score (do tests actually catch bugs?)
- Critical path coverage (are important features tested?)
- Bug escape rate (how many bugs reach production?)

---

### 7.3 Coverage Best Practices

**1. Measure Branch Coverage, Not Just Statement Coverage**

```javascript
// Function with 100% statement coverage but only 50% branch coverage
function discount(price, isPremium) {
  let final = price
  if (isPremium) {
    final = price * 0.9
  }
  return final
}

// Test with isPremium=true covers 100% statements but only 50% branches
test('premium discount', () => {
  expect(discount(100, true)).toBe(90)
})

// Need both tests for 100% branch coverage
test('no discount for regular users', () => {
  expect(discount(100, false)).toBe(100)
})
```

---

**2. Focus Coverage on Critical Code**

**High coverage priority:**
- Business logic
- Security functions
- Data validation
- Error handling
- Financial calculations

**Low coverage priority:**
- Configuration files
- Generated code
- Third-party integrations (test interfaces, not internals)
- Simple getters/setters

---

**3. Use Coverage to Find Gaps, Not as a Goal**

[REJECTED] Do NOT write tests just to hit coverage percentage.

[APPROVED] Use coverage reports to identify untested code, then write meaningful tests.

---

---

## Section 8: Test Data Management

### 8.1 Data Masking and Anonymization

**Purpose:**
Protect sensitive data while maintaining usability for testing.

**When to Use:**
- Testing with production data
- Compliance requirements (GDPR, HIPAA, PDPA)
- Sharing data with third parties
- Development environments

**Techniques:**

```
Original Data:
- Name: John Doe
- Email: john.doe@gmail.com
- SSN: 123-45-6789
- Credit Card: 4532-1234-5678-9010

Masked Data:
- Name: Test User 001
- Email: test.user001@example.com
- SSN: XXX-XX-6789 (partial masking)
- Credit Card: 4532-XXXX-XXXX-9010 (PCI DSS compliant)
```

**Requirements:**
- [ ] Preserve data format (email looks like email, phone looks like phone)
- [ ] Maintain referential integrity (same user ID across tables)
- [ ] One-way transformation (cannot reverse to original)
- [ ] Document masking rules

---

### 8.2 Synthetic Test Data Generation

**Purpose:**
Create artificial yet realistic data without using production data.

**Benefits:**
- [APPROVED] No privacy concerns
- [APPROVED] Cover edge cases not in production
- [APPROVED] Unlimited test data
- [APPROVED] Reproducible datasets

**Tools and Techniques:**

```python
from faker import Faker

fake = Faker()

# Generate realistic test data
user = {
    'name': fake.name(),           # "John Smith"
    'email': fake.email(),         # "john.smith@example.com"
    'address': fake.address(),     # "123 Main St, City, Country"
    'phone': fake.phone_number(),  # "+1-555-123-4567"
    'birthdate': fake.date_of_birth(minimum_age=18, maximum_age=80)
}

# Generate edge cases
edge_cases = {
    'very_long_name': 'A' * 255,
    'unicode_name': 'José María Ñoño',
    'special_chars': "O'Brien-Smith",
    'empty_string': '',
    'null_value': None
}
```

---

### 8.3 Subset and Sampling

**Purpose:**
Use representative subsets of production data.

**Benefits:**
- [APPROVED] Reduced test execution time
- [APPROVED] Lower storage needs
- [APPROVED] Faster database operations

**Sampling Technique:**

```sql
-- Get 10% sample of orders from last 30 days
SELECT * FROM orders
WHERE created_at > NOW() - INTERVAL 30 DAY
ORDER BY RANDOM()
LIMIT (
  SELECT COUNT(*) * 0.1 
  FROM orders 
  WHERE created_at > NOW() - INTERVAL 30 DAY
)
```

**Requirements:**
- [ ] Sample represents full data distribution
- [ ] Include edge cases (high/low values, null values)
- [ ] Maintain referential integrity
- [ ] Document sampling methodology

---

### 8.4 Test Fixtures

**Definition:**
Predefined data sets for repeatable tests.

**Purpose:**
- Consistent test environments
- Easier test maintenance
- Mocking external APIs
- Shared test data across tests

**Example:**

```javascript
// fixtures/users.json
{
  "adminUser": {
    "id": "1",
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  },
  "regularUser": {
    "id": "2",
    "name": "Regular User",
    "email": "user@example.com",
    "role": "user"
  }
}

// In tests
import fixtures from './fixtures/users.json'

test('admin can delete users', () => {
  const admin = fixtures.adminUser
  const result = deleteUser(admin, '123')
  expect(result).toBe(true)
})

test('regular user cannot delete users', () => {
  const user = fixtures.regularUser
  expect(() => deleteUser(user, '123')).toThrow('Unauthorized')
})
```

---

## Section 9: Advanced Testing Techniques

### 9.1 Mutation Testing

**Definition:**
Introduce artificial defects ("mutants") into code to assess test suite thoroughness.

**How It Works:**

```javascript
// Original Code
if (age >= 18) return "Adult"

// Mutant 1: Changed >= to >
if (age > 18) return "Adult"

// Mutant 2: Changed 18 to 21
if (age >= 21) return "Adult"

// Mutant 3: Changed >= to <=
if (age <= 18) return "Adult"
```

**Mutation Score:**

```
Mutation Score = (Killed Mutants / Total Mutants) * 100%

80%+ mutation score = strong test suite
<70% mutation score = weak test suite
```

**What It Reveals:**

```javascript
// High code coverage (100%) but weak tests
function isAdult(age) {
  if (age >= 18) return true
  return false
}

test('isAdult test', () => {
  expect(isAdult(20)).toBe(true) // Only tests one branch
})

// Mutation: Change >= to > would NOT be caught!
// This reveals the test is weak despite 100% coverage
```

**Benefits:**
- [APPROVED] Reveals weak tests (high coverage but low mutation score)
- [APPROVED] Identifies untested edge cases
- [APPROVED] Measures test quality, not just coverage

**When to Use:**
- Critical business logic
- Security-sensitive code
- Before major releases
- Safety-critical systems (aviation, medical)

---

### 9.2 Property-Based Testing

**Definition:**
Test code against general properties rather than specific examples.

**Example-Based Testing (Traditional):**

```python
def test_addition():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    # Only tests 3 specific cases
```

**Property-Based Testing:**

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers(), st.integers())
def test_addition_properties(a, b):
    result = add(a, b)
    
    # Property 1: Commutative
    assert add(a, b) == add(b, a)
    
    # Property 2: Identity
    assert add(a, 0) == a
    
    # Property 3: Inverse
    assert add(a, -a) == 0

# Hypothesis generates 100+ test cases automatically
# Finds edge cases you didn't think of
```

**Benefits:**
- [APPROVED] Finds edge cases automatically
- [APPROVED] Tests thousands of inputs
- [APPROVED] Catches bugs traditional tests miss
- [APPROVED] Combats pesticide paradox (tests don't lose effectiveness)

**When to Use:**
- Complex algorithms
- Mathematical functions
- Data transformations
- Parsers and serializers

---

### 9.3 Contract Testing

**Definition:**
Ensures communication between dependent services follows agreed-upon API contract.

**Why Needed:**
- Microservices have many service dependencies
- Integration tests require all services running (slow, complex)
- Contract tests validate API agreements independently

**How It Works (Consumer-Driven):**

**Step 1: Consumer Defines Contract**

```json
// Payment Service expects from Order Service:
{
  "request": {
    "method": "POST",
    "path": "/orders",
    "body": {
      "orderId": "string",
      "amount": "number",
      "currency": "string"
    }
  },
  "response": {
    "status": 201,
    "body": {
      "orderId": "string",
      "status": "confirmed"
    }
  }
}
```

**Step 2: Provider Verifies Contract**

```javascript
// Order Service runs contract test
describe('Order API Contract', () => {
  it('should meet Payment Service contract', async () => {
    const response = await request(app)
      .post('/orders')
      .send({
        orderId: '12345',
        amount: 99.99,
        currency: 'USD'
      })
    
    expect(response.status).toBe(201)
    expect(response.body).toMatchObject({
      orderId: expect.any(String),
      status: 'confirmed'
    })
  })
})
```

**Step 3: Contract Testing in CI/CD**

- Contracts automatically verified in pipeline
- Catches breaking changes before deployment
- Fails build if contract violated

**Benefits:**
- [APPROVED] Catches API changes early
- [APPROVED] No need for all services running
- [APPROVED] Schema validation (field renames, type changes, missing fields)
- [APPROVED] API versioning testable

**Best For:**
- Microservices architectures
- API-driven applications
- Third-party integrations

---

## Section 10: Testing Anti-Patterns to Avoid

### 10.1 Testing Implementation Details

**Problem:**
Tests tightly coupled to internal implementation, not behavior.

```javascript
// [REJECTED] BAD: Tests private method
test('should call _validateEmail internally', () => {
  const spy = jest.spyOn(UserService, '_validateEmail')
  UserService.createUser({ email: 'test@example.com' })
  expect(spy).toHaveBeenCalled()
})

// [APPROVED] GOOD: Tests public behavior
test('should reject invalid email', () => {
  expect(() => {
    UserService.createUser({ email: 'invalid-email' })
  }).toThrow('Invalid email')
})
```

**Why Bad:**
- [REJECTED] Refactoring breaks tests
- [REJECTED] Tests become maintenance burden
- [REJECTED] Doesn't test actual behavior

---

### 10.2 Using "And" in Test Names

**Problem:**
Hints test is testing multiple things.

```javascript
// [REJECTED] BAD
test('should validate email and save user and send welcome email', () => {
  // Tests 3 different things
})

// [APPROVED] GOOD: Split into separate tests
test('should validate email format', () => { ... })
test('should save user to database', () => { ... })
test('should send welcome email after signup', () => { ... })
```

---

### 10.3 Combinatorial Explosion

**Problem:**
Testing all possible combinations hints multiple components in one.

```javascript
// [REJECTED] BAD: Testing 4x4 = 16 combinations
test.each([
  ['admin', 'post', 'create', true],
  ['admin', 'post', 'delete', true],
  ['admin', 'comment', 'create', true],
  ['admin', 'comment', 'delete', true],
  ['editor', 'post', 'create', true],
  ['editor', 'post', 'delete', false],
  // ... 16 combinations total
])('permission check', (role, resource, action, expected) => {
  expect(checkPermission(role, resource, action)).toBe(expected)
})

// [APPROVED] GOOD: Split into separate components
test('role permissions', () => {
  // Test role-level permissions only
})

test('resource permissions', () => {
  // Test resource-level permissions only
})
```

**Solution:** Recognize separate components and split apart.

---

### 10.4 Pesticide Paradox

**Problem:**
Automated tests lose effectiveness over time by testing exact same thing repeatedly.

**Solution:**
- [APPROVED] Use property-based testing (randomized inputs)
- [APPROVED] Use synthetic data generation (Faker libraries)
- [APPROVED] Regularly review and update tests
- [APPROVED] Add new tests for new bug patterns

---

### 10.5 Over-Mocking

**Problem:**
Tests mock so many dependencies they barely test anything.

```javascript
// [REJECTED] BAD: Mocking everything
test('should process order', () => {
  const mockDb = jest.fn(() => ({ success: true }))
  const mockPayment = jest.fn(() => ({ success: true }))
  const mockEmail = jest.fn(() => ({ success: true }))
  
  // What are we actually testing? Just that functions are called?
  const result = processOrder(mockDb, mockPayment, mockEmail)
  expect(result.success).toBe(true)
})

// [APPROVED] GOOD: Use real implementations where practical
test('should process order', () => {
  const testDb = new TestDatabase()
  const mockPayment = new MockPaymentGateway() // External service
  const result = processOrder(testDb, mockPayment)
  
  // Verify actual behavior
  const order = testDb.getOrder(result.orderId)
  expect(order.status).toBe('paid')
})
```

**Rule of Thumb:**
- [APPROVED] Mock external services (payment gateways, third-party APIs)
- [REJECTED] Do NOT mock your own code (use real implementations)

---

### 10.6 No Local Testing

**Problem:**
Developers can't run tests locally, must push to CI/CD.

**Why Bad:**
- [REJECTED] Slow feedback loop (minutes instead of seconds)
- [REJECTED] Wastes CI/CD resources
- [REJECTED] Frustrating developer experience

**Solution:**
- [APPROVED] Ensure tests run locally without CI/CD dependencies
- [APPROVED] Use Docker Compose for local test environments
- [APPROVED] Provide setup scripts
- [APPROVED] Document local test execution

---

## Complete Testing Verification Checklist

**Before committing to testing strategy, verify ALL of these:**

### Testing Philosophy
- [ ] Shift-left testing implemented (QA involved in requirements)
- [ ] Risk-based testing approach defined
- [ ] TDD vs BDD decision made
- [ ] Testing culture established

### Testing Pyramid
- [ ] 70/20/10 distribution implemented
- [ ] Unit tests run in < 1 minute
- [ ] Integration tests run in < 10 minutes
- [ ] E2E tests run in < 30 minutes (smoke suite)

### Unit Testing
- [ ] One assertion per test
- [ ] Descriptive test naming convention
- [ ] AAA pattern (Arrange-Act-Assert) followed
- [ ] Test independence verified (can run in any order)
- [ ] Edge cases covered (null, empty, boundary values)
- [ ] Error handling tested

### Integration Testing
- [ ] Separate test database configured
- [ ] Database reset between tests
- [ ] API endpoints tested
- [ ] Service integration tested
- [ ] Tests run in < 5 seconds each

### E2E Testing
- [ ] Critical paths identified and tested
- [ ] Data-testid attributes added to UI elements
- [ ] Proper waits implemented (no fixed timeouts)
- [ ] Isolated test data per test
- [ ] Tests run in parallel
- [ ] Headless mode for CI/CD

### Performance Testing
- [ ] Load testing configured (normal volumes)
- [ ] Stress testing configured (breaking points)
- [ ] Soak testing configured (24+ hours) if needed
- [ ] Realistic test data
- [ ] Performance baselines established
- [ ] Regression thresholds defined (fail if > 10% slower)

### Test Coverage
- [ ] Branch coverage measured (not just statement)
- [ ] Coverage targets defined by context (70-90%)
- [ ] Critical code has higher coverage (90%+)
- [ ] Coverage reports reviewed regularly
- [ ] Coverage used to find gaps, not as goal

### Test Data Management
- [ ] Production data masked/anonymized
- [ ] Synthetic data generation implemented
- [ ] Test fixtures created for common scenarios
- [ ] Data cleanup automated

### Advanced Techniques
- [ ] Mutation testing for critical code (optional)
- [ ] Property-based testing for algorithms (optional)
- [ ] Contract testing for microservices (if applicable)

### Anti-Patterns Avoided
- [ ] Not testing implementation details
- [ ] No "and" in test names (one thing per test)
- [ ] No combinatorial explosion
- [ ] Tests updated regularly (combat pesticide paradox)
- [ ] Minimal mocking (only external services)
- [ ] Local testing enabled

**If ANY checkbox fails, address before proceeding to production.**

---

## When to Read This Canon

**ONLY read this testing canon when writing or reviewing tests:**

- Writing new tests (unit, integration, E2E)
- Reviewing test coverage
- Setting up testing infrastructure
- Implementing performance testing
- Troubleshooting test failures
- Improving test quality

**Do NOT read for:**
- Regular feature development (unless writing tests)
- Bug fixes (unless adding tests)
- Code reviews (unless reviewing tests)

This keeps the canon reference brief and targeted.

---

## Version

Testing Canon Version: 1.0 - Complete (December 29, 2025)  
Based on industry research and best practices for software testing.

Covers 10 comprehensive categories:
1. Testing Philosophy and Core Principles
2. The Testing Pyramid
3. Unit Testing
4. Integration Testing
5. End-to-End (E2E) Testing
6. Performance Testing
7. Test Coverage
8. Test Data Management
9. Advanced Testing Techniques
10. Testing Anti-Patterns

