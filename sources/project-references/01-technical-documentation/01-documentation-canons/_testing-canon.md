# Canon: Testing Documentation

## Purpose

Testing documentation defines test strategy, coverage requirements, test procedures, and quality gates. It ensures consistent testing practices, enables new team members to understand testing approach, and provides repeatable test procedures for regression testing.

---

## Scope

**This canon applies to:**
- Test strategy and philosophy
- Unit testing guidelines
- Integration testing procedures
- End-to-end (E2E) testing procedures
- Performance testing approach
- Test coverage requirements
- Test automation strategy

**This canon does NOT apply to:**
- Individual test case code (document in test files)
- Bug reports (use issue tracker)
- QA team procedures (separate QA documentation)

---

## Access Level Classification

**Testing Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Development team, QA team, DevOps team
- **Storage:** Private repository with authentication
- **Review:** QA team review, technical lead approval
- **Rationale:** Contains test strategies, edge cases, potential weaknesses

**Exception:** Testing best practices may be Public (Level 1) for open-source projects

---

## When to Generate

### Initial Creation
- **Project Inception:** Define test strategy before development
- **CI/CD Setup:** Document test automation during pipeline creation
- **Quality Gates:** Define criteria before first release

### Updates
- After adding new test types
- After test framework changes
- When coverage requirements change
- Quarterly test strategy review

### Frequency
- **Initial:** During project setup phase
- **Test Changes:** After major test infrastructure updates
- **Regular Review:** Quarterly for accuracy
- **Coverage Updates:** Monthly review of coverage metrics

---

## Files to Generate

Agent must create the following files when documenting testing:

### 1. Testing Documentation Index
**File:** `/docs/source/testing/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** Testing documentation entry point

### 2. Test Strategy
**File:** `/docs/source/testing/01-test-strategy.rst`  
**Format:** reStructuredText  
**Purpose:** Overall testing philosophy, pyramid, coverage targets

### 3. Unit Testing
**File:** `/docs/source/testing/02-unit-testing.rst`  
**Format:** reStructuredText  
**Purpose:** Unit test guidelines, frameworks, best practices

### 4. Integration Testing
**File:** `/docs/source/testing/03-integration-testing.rst`  
**Format:** reStructuredText  
**Purpose:** Integration test procedures, database testing, API testing

### 5. End-to-End Testing
**File:** `/docs/source/testing/04-e2e-testing.rst`  
**Format:** reStructuredText  
**Purpose:** E2E test approach, browser testing, user flows

### 6. Performance Testing
**File:** `/docs/source/testing/05-performance-testing.rst`  
**Format:** reStructuredText  
**Purpose:** Load testing, stress testing, performance benchmarks

---

## Directory Structure

```
docs/source/testing/
├── 00-index.rst                    # Testing documentation entry point
├── 01-test-strategy.rst            # Test strategy and philosophy
├── 02-unit-testing.rst             # Unit testing guidelines
├── 03-integration-testing.rst      # Integration testing procedures
├── 04-e2e-testing.rst              # End-to-end testing approach
└── 05-performance-testing.rst      # Performance testing procedures
```

---

## Generation Rules

### Test Pyramid

Document testing philosophy using test pyramid:

```
      /\
     /E2E\      <- Fewest tests (slow, expensive)
    /------\
   /  API   \   <- Moderate tests (moderate speed)
  /----------\
 / Unit Tests \ <- Most tests (fast, cheap)
/--------------\
```

**Recommended Ratios:**
- Unit Tests: 70%
- Integration/API Tests: 20%
- E2E Tests: 10%

### Coverage Targets

Specify clear coverage targets:
- Overall code coverage: X%
- Critical paths: 100%
- New code: Minimum Y%

### Test Examples

Provide clear, runnable test examples for each test type.

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice
- Specific over vague (exact commands, frameworks, metrics)
- Code examples must be runnable

---

## Content Guidelines

### Testing Index (`/docs/source/testing/00-index.rst`)

```rst
Testing Documentation
=====================

.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains testing strategies.
   Do not share with external parties.

.. contents::
   :local:
   :depth: 2

Overview
--------

The Tax Management System follows a comprehensive testing strategy ensuring quality
and reliability across all components.

**Test Framework**: Jest (JavaScript), Go testing (Go backend)  
**CI/CD Integration**: GitHub Actions  
**Coverage Target**: 80% overall, 100% for critical paths  
**Test Execution**: Automated on every PR

Testing Philosophy
------------------

**Test Pyramid Approach**

- **70% Unit Tests**: Fast, isolated, developer-written
- **20% Integration Tests**: API contracts, database interactions
- **10% E2E Tests**: Critical user flows, browser-based

**Quality Gates**

All code must pass:

1. All tests pass
2. Coverage meets minimum threshold (80%)
3. No lint errors
4. No security vulnerabilities (Snyk scan)

Quick Links
-----------

- **Test Strategy**: :doc:`01-test-strategy`
- **Unit Testing**: :doc:`02-unit-testing`
- **Integration Testing**: :doc:`03-integration-testing`
- **E2E Testing**: :doc:`04-e2e-testing`
- **Performance Testing**: :doc:`05-performance-testing`

.. toctree::
   :maxdepth: 2

   01-test-strategy
   02-unit-testing
   03-integration-testing
   04-e2e-testing
   05-performance-testing

Running Tests
-------------

**Run all tests:**

.. code-block:: bash

   npm test

**Run specific test suite:**

.. code-block:: bash

   npm test -- unit
   npm test -- integration
   npm test -- e2e

**Generate coverage report:**

.. code-block:: bash

   npm test -- --coverage

Current Metrics
---------------

**As of December 2025:**

- Test Coverage: 85%
- Unit Tests: 1,250 tests
- Integration Tests: 320 tests
- E2E Tests: 45 tests
- Average Test Execution Time: 3 minutes
- Flaky Test Rate: < 1%
```

### Test Strategy (`/docs/source/testing/01-test-strategy.rst`)

```rst
Test Strategy
=============

Overall testing approach and philosophy.

Testing Principles
------------------

**Fast Feedback**
- Tests run on every commit
- Most tests complete in < 3 minutes
- Developers notified immediately on failures

**Reliable Tests**
- No flaky tests tolerated
- Tests are deterministic
- Tests clean up after themselves

**Maintainable Tests**
- Tests are readable (describe intent clearly)
- Avoid test duplication
- Refactor tests alongside production code

Test Pyramid
------------

**Unit Tests (70%)**

**Purpose**: Test individual functions/methods in isolation  
**Speed**: Very fast (< 1ms per test)  
**Scope**: Single function or class  
**Dependencies**: Mocked

**Example**: Tax calculation logic

**Integration Tests (20%)**

**Purpose**: Test interactions between components  
**Speed**: Moderate (10-100ms per test)  
**Scope**: Multiple components, real database  
**Dependencies**: Real database, mocked external APIs

**Example**: API endpoint with database query

**E2E Tests (10%)**

**Purpose**: Test complete user flows  
**Speed**: Slow (1-10 seconds per test)  
**Scope**: Entire system, browser-based  
**Dependencies**: All real (database, external APIs in test mode)

**Example**: User login, tax calculation, receipt download

Coverage Requirements
---------------------

**Overall Target**: 80% code coverage

**Critical Path Target**: 100% coverage

Critical paths include:

- Tax calculation algorithms
- Payment processing
- Authentication and authorization
- Data encryption/decryption

**New Code**: Minimum 80% coverage (enforced in PR checks)

**Excluded from Coverage**:

- Generated code
- Configuration files
- Test utilities

Test Execution Strategy
-----------------------

**Local Development**

Developers run tests before committing:

.. code-block:: bash

   npm test

**Pre-Commit Hooks**

Git pre-commit hook runs:

- Linter
- Type checker
- Unit tests (fast tests only)

**Pull Request (PR)**

GitHub Actions runs on every PR:

1. Lint check
2. Type check
3. Unit tests
4. Integration tests
5. E2E tests (smoke tests only)
6. Coverage report

**PR must pass all checks to merge.**

**Main Branch**

After merge to main:

1. Full test suite (including all E2E tests)
2. Performance tests
3. Security scan
4. Build production artifacts

**Nightly Builds**

Every night at 02:00 UTC:

1. Full regression test suite
2. Extended E2E tests
3. Performance benchmarks
4. Dependency vulnerability scan

Quality Gates
-------------

**Cannot Merge PR if:**

- Any test fails
- Coverage drops below 80%
- Lint errors present
- Security vulnerabilities (High or Critical)

**Cannot Deploy to Production if:**

- Staging tests fail
- Performance benchmarks regress > 10%
- Manual QA sign-off missing

Test Data Management
--------------------

**Test Database**

Each test gets isolated database:

.. code-block:: javascript

   beforeEach(async () => {
       await db.migrate.latest();  // Apply migrations
       await db.seed.run();        // Seed test data
   });

   afterEach(async () => {
       await db.migrate.rollback();  // Clean up
   });

**Fixtures**

Test data stored in `/tests/fixtures/`

.. code-block:: javascript

   const testUser = require('./fixtures/user.json');

**Test Data Principles**:

- Realistic data (mirrors production structure)
- Minimal data (only what test needs)
- Self-contained (test doesn't depend on other tests' data)
```

### Unit Testing (`/docs/source/testing/02-unit-testing.rst`)

```rst
Unit Testing Guidelines
=======================

Guidelines for writing effective unit tests.

Unit Test Framework
-------------------

**JavaScript/TypeScript**: Jest  
**Go**: Go testing package  
**Test Naming**: ``<function>_<scenario>_<expectedResult>``

Unit Test Structure (AAA Pattern)
----------------------------------

**Arrange**: Set up test data  
**Act**: Execute function under test  
**Assert**: Verify expected outcome

**Example (JavaScript):**

.. code-block:: javascript

   describe('calculatePAYE', () => {
       test('calculatesPAYE_withBasicSalary_returnsCorrectTax', () => {
           // Arrange
           const grossSalary = 50000;
           const expectedTax = 5250;

           // Act
           const result = calculatePAYE(grossSalary);

           // Assert
           expect(result.taxAmount).toBe(expectedTax);
       });
   });

**Example (Go):**

.. code-block:: go

   func TestCalculatePAYE_WithBasicSalary_ReturnsCorrectTax(t *testing.T) {
       // Arrange
       grossSalary := 50000.0
       expectedTax := 5250.0

       // Act
       result := CalculatePAYE(grossSalary)

       // Assert
       if result.TaxAmount != expectedTax {
           t.Errorf("Expected tax %v, got %v", expectedTax, result.TaxAmount)
       }
   }

Mocking Dependencies
--------------------

**JavaScript (Jest):**

.. code-block:: javascript

   // Mock external API
   jest.mock('../services/kraAPI');

   test('submitToKRA_withValidData_callsKRAAPI', async () => {
       // Arrange
       const kraAPI = require('../services/kraAPI');
       kraAPI.submitTaxReturn.mockResolvedValue({ success: true });

       // Act
       await submitToKRA({ userId: '123', taxAmount: 5000 });

       // Assert
       expect(kraAPI.submitTaxReturn).toHaveBeenCalledWith({
           userId: '123',
           taxAmount: 5000
       });
   });

**Go (Interface Mocking):**

.. code-block:: go

   type MockKRAClient struct {
       SubmitCalled bool
       SubmitError  error
   }

   func (m *MockKRAClient) Submit(data TaxData) error {
       m.SubmitCalled = true
       return m.SubmitError
   }

   func TestSubmitToKRA_WithValidData_CallsKRAAPI(t *testing.T) {
       // Arrange
       mock := &MockKRAClient{}
       service := NewTaxService(mock)

       // Act
       err := service.SubmitToKRA(TaxData{UserID: "123"})

       // Assert
       if !mock.SubmitCalled {
           t.Error("Expected KRA API to be called")
       }
   }

Code Coverage
-------------

**Run coverage report:**

.. code-block:: bash

   npm test -- --coverage

**View HTML report:**

.. code-block:: bash

   npm test -- --coverage
   open coverage/lcov-report/index.html

**Coverage Thresholds** (enforced in CI):

.. code-block:: json

   {
     "jest": {
       "coverageThreshold": {
         "global": {
           "statements": 80,
           "branches": 80,
           "functions": 80,
           "lines": 80
         }
       }
     }
   }

Best Practices
--------------

**Do:**

- Test one thing per test
- Use descriptive test names
- Keep tests independent
- Mock external dependencies
- Test edge cases and error conditions

**Don't:**

- Test implementation details (test behavior, not internals)
- Write flaky tests (random data, time-dependent)
- Share state between tests
- Test third-party libraries
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all testing reST files
rstcheck docs/source/testing/*.rst
```

**Expected output:** No errors

### Code Example Validation

- [ ] All code examples are syntactically correct
- [ ] All test commands work
- [ ] Coverage thresholds match actual CI configuration

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

---

## Examples Reference

See working example: `02-examples/testing-example/` (to be created)

**Example includes:**
- Complete testing documentation
- Unit test examples
- Integration test examples

---

## Access Level Warning

Include at top of `00-index.rst`:

```rst
.. warning::
   INTERNAL DOCUMENTATION - Level 2 Access
   This documentation contains testing strategies.
   Do not share with external parties.
```

---

## Agent Checklist

Before marking testing documentation complete, verify:

- [ ] Testing index created
- [ ] Test strategy documented with pyramid
- [ ] Coverage requirements specified
- [ ] Unit testing guidelines with examples
- [ ] Integration testing procedures documented
- [ ] E2E testing approach documented
- [ ] Performance testing procedures documented
- [ ] All code examples tested and working
- [ ] Quality gates defined
- [ ] Access level warnings included
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial testing documentation canon
- Based on test pyramid approach
- Follows `_docs-canon.md` v4 specifications
