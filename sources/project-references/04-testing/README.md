# Testing Reference Documentation

This directory contains comprehensive testing standards and best practices.

## Contents

- **testing-canon.md** - Complete testing standards (10 comprehensive categories)

## Coverage

This testing canon covers:

### 1. Testing Philosophy and Core Principles
- Shift-Left Testing (test early)
- Risk-Based Testing (prioritize by impact)
- Test-Driven Development (TDD)
- Behavior-Driven Development (BDD)

### 2. The Testing Pyramid
- Ideal distribution (70% unit, 20% integration, 10% E2E)
- Economic optimization
- Rapid feedback
- CI/CD integration

### 3. Unit Testing
- Characteristics (fast, isolated)
- Best practices (AAA pattern, descriptive names, edge cases)
- Speed requirements

### 4. Integration Testing
- Database layer testing
- API endpoint testing
- Service integration
- Speed optimization

### 5. End-to-End (E2E) Testing
- Critical path focus
- Resilient selectors
- Proper waits
- Isolated test data

### 6. Performance Testing
- Load testing
- Stress testing
- Soak testing
- Bottleneck identification

### 7. Test Coverage
- Coverage metrics (statement, branch, path, MC/DC)
- Context-based targets (70-100%)
- Best practices

### 8. Test Data Management
- Data masking and anonymization
- Synthetic data generation
- Subset and sampling
- Test fixtures

### 9. Advanced Testing Techniques
- Mutation testing (test quality validation)
- Property-based testing (find edge cases)
- Contract testing (microservices)

### 10. Testing Anti-Patterns
- Testing implementation details
- Using "and" in test names
- Combinatorial explosion
- Pesticide paradox
- Over-mocking
- No local testing

## When to Use

**ONLY reference files in this directory when writing or reviewing tests:**
- Writing new tests (unit, integration, E2E)
- Reviewing test coverage
- Setting up testing infrastructure
- Implementing performance testing
- Troubleshooting test failures
- Improving test quality

**Do NOT reference for regular development work unless writing tests.**

---

Version: 1.0 (December 29, 2025)
