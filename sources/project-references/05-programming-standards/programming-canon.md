# Programming Standards Canon: Comprehensive Development Standards

This document provides comprehensive, non-negotiable programming standards for all projects following the Vibe Code Canon framework.

**Authority:** These standards have ABSOLUTE AUTHORITY and MUST be followed during development. All examples provided are for contextual purposes ONLY and should not be assumed to be part of the programming standards or project requirements.

---

## Section 1: Clean Code Principles

### 1.1 Core Philosophy

**Definition:**
Clean code is designed with future updates in mind, following a solid principle: structure your code so changes don't cause cascading problems.

**Why Critical:**

**Bug Reduction:**
Messy code invites bugs, while clean code actively minimizes them. Adopting clear naming conventions, logical structures, and consistent syntax helps spot issues before they become major problems.

**Maintainability:**
Clean code is easier to read, understand, and modify. Future developers (including yourself) can quickly grasp intent without archaeological excavation.

**Scalability:**
Promotes modularity and makes extending functionality straightforward.

---

### 1.2 Meaningful and Descriptive Names

**Good names communicate intent clearly:**

```javascript
// [REJECTED] BAD: Cryptic, meaningless
let d = 7
let x = getUsers()
let tmp = calculate()

// [APPROVED] GOOD: Clear, descriptive
let daysUntilExpiry = 7
let activeUsersList = fetchActiveUsers()
let orderTotal = calculateOrderTotal()
```

**Requirements:**
- [ ] Variables describe what they store
- [ ] Functions describe what they do
- [ ] Classes describe what they represent
- [ ] No single-letter names (except loop counters i, j, k)
- [ ] No abbreviations unless universally understood (HTTP, URL, ID)

---

### 1.3 Avoid Magic Numbers

**Use named constants:**

```python
# [REJECTED] BAD: Magic numbers
if user.age >= 18:
    grant_access()

if order.total > 100:
    apply_discount(order.total * 0.1)

# [APPROVED] GOOD: Named constants
MINIMUM_AGE_FOR_ACCESS = 18
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.1

if user.age >= MINIMUM_AGE_FOR_ACCESS:
    grant_access()

if order.total > DISCOUNT_THRESHOLD:
    apply_discount(order.total * DISCOUNT_RATE)
```

**Why:**
- Context makes code self-documenting
- Future changes easier (change once, applies everywhere)
- Business rules explicit

---

### 1.4 DRY Principle (Don't Repeat Yourself)

**Extract repeated logic into reusable functions:**

```javascript
// [REJECTED] BAD: Repetition
let total1 = (price1 * quantity1 * (1 + TAX_RATE)) - discount1
let total2 = (price2 * quantity2 * (1 + TAX_RATE)) - discount2
let total3 = (price3 * quantity3 * (1 + TAX_RATE)) - discount3

// [APPROVED] GOOD: Reusable function
function calculateTotal(price, quantity, discount) {
  const subtotal = price * quantity
  const withTax = subtotal * (1 + TAX_RATE)
  return withTax - discount
}

let total1 = calculateTotal(price1, quantity1, discount1)
let total2 = calculateTotal(price2, quantity2, discount2)
let total3 = calculateTotal(price3, quantity3, discount3)
```

**Benefits:**
- [APPROVED] Reduces risk of errors during modifications
- [APPROVED] Simplifies debugging (fix in one place)
- [APPROVED] Promotes scalability

---

### 1.5 Keep Functions Small and Focused

**Single Responsibility Per Function:**

```python
# [REJECTED] BAD: Function does too much
def process_user_order(user_id, order_items):
    # Validate user
    if not user_exists(user_id):
        raise Exception("Invalid user")
    
    # Calculate total
    total = sum([item.price * item.quantity for item in order_items])
    
    # Apply discount
    if total > 100:
        total *= 0.9
    
    # Process payment
    payment_result = charge_credit_card(user_id, total)
    
    # Update inventory
    for item in order_items:
        decrement_inventory(item.id, item.quantity)
    
    # Send email
    send_order_confirmation(user_id, order_items)
    
    return order_result

# [APPROVED] GOOD: Separate concerns
def process_user_order(user_id, order_items):
    validate_user(user_id)
    total = calculate_order_total(order_items)
    total = apply_discount(total)
    payment_result = process_payment(user_id, total)
    update_inventory(order_items)
    send_confirmation_email(user_id, order_items)
    return payment_result
```

**Benefits:**
- [APPROVED] Easier to test (test one thing at a time)
- [APPROVED] Easier to understand (clear purpose)
- [APPROVED] Easier to reuse

**Target:** Functions should be 10-20 lines maximum (exclude blank lines and braces).

---

### 1.6 Comment Only When Necessary

**Code should be self-explanatory. Comments explain WHY, not WHAT:**

```javascript
// [REJECTED] BAD: Comment states the obvious
// Increment counter by 1
counter++

// [REJECTED] BAD: Comment repeats code
// Check if user age is greater than or equal to 18
if (user.age >= 18) { ... }

// [APPROVED] GOOD: Comment explains business logic
// Users must be 18+ to comply with GDPR regulations for data collection
const MINIMUM_AGE_FOR_CONSENT = 18
if (user.age >= MINIMUM_AGE_FOR_CONSENT) { ... }

// [APPROVED] GOOD: Comment explains non-obvious workaround
// Safari browser requires 10ms delay before focus() works correctly
// See bug: https://bugs.webkit.org/show_bug.cgi?id=12345
setTimeout(() => input.focus(), 10)
```

**When to Comment:**
- [APPROVED] Explain business reasoning
- [APPROVED] Document non-obvious workarounds
- [APPROVED] Warn about side effects
- [APPROVED] Explain complex algorithms
- [REJECTED] Restate what code does
- [REJECTED] Narrate code line-by-line

---

### 1.7 Use Consistent Formatting

**Follow team/project standards:**

**Indentation:**
- Spaces vs tabs (choose one)
- Indentation size (2 or 4 spaces)

**Brace Style:**
- Same line vs new line
- Consistent throughout codebase

**Line Length:**
- Maximum 80-120 characters
- Break long lines logically

**File Organization:**
- Imports/includes at top
- Constants after imports
- Class definition
- Public methods before private

**Tools:**
Use automated formatters to enforce consistency:
- Prettier (JavaScript/TypeScript)
- Black (Python)
- rustfmt (Rust)
- gofmt (Go)

---

### 1.8 Principle of Least Knowledge (Law of Demeter)

**Only expose and consume data you need:**

```typescript
// [REJECTED] BAD: Exposing too much
interface User {
  id: string
  name: string
  email: string
  password: string        // Should never be exposed
  creditCard: string      // Sensitive
  ssn: string            // Sensitive
  internalUserId: number // Internal implementation detail
}

// [APPROVED] GOOD: Only necessary data
interface PublicUserProfile {
  id: string
  name: string
  email: string
}

// [APPROVED] GOOD: Context-specific interfaces
interface UserForAdmin {
  id: string
  name: string
  email: string
  createdAt: Date
  lastLoginAt: Date
}
```

**Benefits:**
- [APPROVED] Reduces complexity
- [APPROVED] Increases security
- [APPROVED] Avoids errors from unnecessary data
- [APPROVED] Improves efficiency

---

## Section 2: SOLID Principles

**SOLID is an acronym for five fundamental object-oriented design principles.**

### 2.1 Single Responsibility Principle (SRP)

**Definition:**
"A class should have one, and only one, reason to change."

**Translation:** Each class solves only one problem.

**Example:**

```python
# [REJECTED] BAD: Class has multiple responsibilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        # Database logic
        pass
    
    def send_welcome_email(self):
        # Email logic
        pass
    
    def generate_report(self):
        # Reporting logic
        pass

# [APPROVED] GOOD: Separate responsibilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # Database logic
        pass

class EmailService:
    def send_welcome_email(self, user):
        # Email logic
        pass

class UserReportGenerator:
    def generate(self, user):
        # Reporting logic
        pass
```

**Benefits:**
- [APPROVED] Easier to test
- [APPROVED] Easier to maintain (changes isolated)
- [APPROVED] Easier to understand

---

### 2.2 Open-Closed Principle (OCP)

**Definition:**
"Software entities should be open for extension, but closed for modification."

**Translation:** Add new functionality without changing existing code.

**Example:**

```typescript
// [REJECTED] BAD: Must modify class to add new payment type
class PaymentProcessor {
  processPayment(type: string, amount: number) {
    if (type === 'credit_card') {
      // Process credit card
    } else if (type === 'paypal') {
      // Process PayPal
    } else if (type === 'bitcoin') {  // Adding new type requires modifying existing code
      // Process Bitcoin
    }
  }
}

// [APPROVED] GOOD: Extend without modification
interface PaymentMethod {
  process(amount: number): void
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number) {
    // Process credit card
  }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number) {
    // Process PayPal
  }
}

// Adding new payment method doesn't require modifying existing code
class BitcoinPayment implements PaymentMethod {
  process(amount: number) {
    // Process Bitcoin
  }
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}
  
  processPayment(amount: number) {
    this.method.process(amount)
  }
}
```

**Benefits:**
- [APPROVED] New features don't break existing code
- [APPROVED] Reduces regression bugs
- [APPROVED] Easier to extend system

---

### 2.3 Liskov Substitution Principle (LSP)

**Definition:**
"Subtypes must be substitutable for their base types."

**Translation:** Child classes should enhance, not break, parent class behavior.

**Example:**

```python
# [REJECTED] BAD: Violates LSP
class Bird:
    def fly(self):
        return "Flying high"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")  # Breaks parent contract

# [APPROVED] GOOD: Proper abstraction
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        return "Flying high"

class Penguin(Bird):
    def move(self):
        return "Swimming fast"
```

**Benefits:**
- [APPROVED] Predictable behavior
- [APPROVED] No surprises when using inherited classes
- [APPROVED] Safer polymorphism

---

### 2.4 Interface Segregation Principle (ISP)

**Definition:**
"Clients should not be forced to depend on interfaces they don't use."

**Translation:** Many small, specific interfaces better than one large, general interface.

**Example:**

```typescript
// [REJECTED] BAD: Fat interface
interface Worker {
  work(): void
  eat(): void
  sleep(): void
  attendMeeting(): void
}

class Human implements Worker {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
  attendMeeting() { /* ... */ }
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { /* Robots don't eat! */ }      // Forced to implement
  sleep() { /* Robots don't sleep! */ }  // Forced to implement
  attendMeeting() { /* ... */ }
}

// [APPROVED] GOOD: Segregated interfaces
interface Workable {
  work(): void
}

interface Eatable {
  eat(): void
}

interface Sleepable {
  sleep(): void
}

interface MeetingAttendable {
  attendMeeting(): void
}

class Human implements Workable, Eatable, Sleepable, MeetingAttendable {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
  attendMeeting() { /* ... */ }
}

class Robot implements Workable, MeetingAttendable {
  work() { /* ... */ }
  attendMeeting() { /* ... */ }
  // Only implements what it needs
}
```

**Benefits:**
- [APPROVED] No forced implementations
- [APPROVED] Easier to understand (smaller interfaces)
- [APPROVED] More flexible

---

### 2.5 Dependency Inversion Principle (DIP)

**Definition:**
"Depend on abstractions, not on concretions."

**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

**Example:**

```rust
// [REJECTED] BAD: High-level depends on low-level
struct MySQLDatabase {
    // MySQL-specific implementation
}

struct UserService {
    database: MySQLDatabase,  // Tightly coupled to MySQL
}

// [APPROVED] GOOD: Both depend on abstraction
trait Database {
    fn save(&self, data: &str);
    fn get(&self, id: i32) -> String;
}

struct MySQLDatabase;
impl Database for MySQLDatabase {
    fn save(&self, data: &str) { /* MySQL implementation */ }
    fn get(&self, id: i32) -> String { /* MySQL implementation */ }
}

struct PostgreSQLDatabase;
impl Database for PostgreSQLDatabase {
    fn save(&self, data: &str) { /* PostgreSQL implementation */ }
    fn get(&self, id: i32) -> String { /* PostgreSQL implementation */ }
}

struct UserService {
    database: Box<dyn Database>,  // Depends on abstraction
}

// Can swap database implementation without changing UserService
```

**Benefits:**
- [APPROVED] Makes code more flexible
- [APPROVED] Makes code more agile
- [APPROVED] Makes code more reusable
- [APPROVED] Easier to test (mock abstractions)

---

## Section 3: Naming Conventions

### 3.1 Language-Specific Conventions

**JavaScript/TypeScript:**
```javascript
// Variables and functions: camelCase
let userName = "John"
function calculateTotal() { }

// Classes and components: PascalCase
class UserProfile { }
const MyComponent = () => { }

// Constants: SCREAMING_SNAKE_CASE
const MAX_USERS_ALLOWED = 100

// Private properties: prefix with underscore (convention)
class Example {
  _privateProperty = 0
}
```

**Python:**
```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total():
    pass

# Classes: PascalCase
class UserProfile:
    pass

# Constants: SCREAMING_SNAKE_CASE
MAX_USERS_ALLOWED = 100

# Private: prefix with underscore
class Example:
    def __init__(self):
        self._private_property = 0
```

**Rust:**
```rust
// Variables and functions: snake_case
let user_name = "John";
fn calculate_total() { }

// Structs and enums: PascalCase
struct UserProfile { }
enum OrderStatus { }

// Constants: SCREAMING_SNAKE_CASE
const MAX_USERS_ALLOWED: i32 = 100;
```

**CSS/HTML:**
```css
/* kebab-case for class names and IDs */
.user-profile { }
#main-container { }

/* BEM notation for component styles */
.block__element--modifier { }
```

---

### 3.2 General Naming Guidelines

**1. Be Descriptive and Concise**

```javascript
// [REJECTED] BAD
let x = 10
let data = fetch()

// [APPROVED] GOOD
let maxUsersAllowed = 10
let userProfiles = fetchUserProfiles()
```

---

**2. Use Verbs for Functions**

**Functions are action-oriented:**

```javascript
// [REJECTED] BAD
function userData() { }
function items() { }

// [APPROVED] GOOD
function fetchUserData() { }
function calculateTotalPrice() { }
function validateEmail() { }

// Boolean functions: is/has/can
function isUserActive() { }
function hasPermission() { }
function canEdit() { }
```

---

**3. Be Specific About Functionality**

```python
# [REJECTED] BAD: Too vague
def process():
    pass

def handle_data():
    pass

# [APPROVED] GOOD: Specific
def process_payment():
    pass

def validate_user_credentials():
    pass

def transform_csv_to_json():
    pass
```

---

**4. Classes Describe "Things" (Nouns)**

```typescript
// [APPROVED] GOOD: Nouns
class Vehicle { }
class Image { }
class Constraint { }
class UserAuthentication { }
class PaymentProcessor { }
```

---

**5. Strong Verb + Object for Functions**

```python
# [APPROVED] GOOD: Strong verb + clear object
paginate_response()
empty_input_buffer()
validate_user_credentials()
serialize_order_data()

// [REJECTED] BAD: Weak verb
deal_with_response()
handle_stuff()
do_thing()
```

---

## Verification Checklist - Part 1

**Before proceeding, verify:**

### Clean Code Principles
- [ ] Meaningful and descriptive names used
- [ ] No magic numbers (constants defined)
- [ ] DRY principle followed (no duplication)
- [ ] Functions small and focused (< 20 lines)
- [ ] Comments explain WHY, not WHAT
- [ ] Consistent formatting applied
- [ ] Principle of Least Knowledge followed

### SOLID Principles
- [ ] Single Responsibility: Each class has one reason to change
- [ ] Open-Closed: Extend without modifying
- [ ] Liskov Substitution: Subtypes substitutable for base types
- [ ] Interface Segregation: Many small interfaces, not one large
- [ ] Dependency Inversion: Depend on abstractions

### Naming Conventions
- [ ] Language-specific conventions followed
- [ ] Verbs for functions, nouns for classes
- [ ] Boolean functions prefixed with is/has/can
- [ ] Descriptive and specific names
- [ ] Strong verb + object pattern for functions

---

## Section 4: Design Patterns

### 4.1 When to Use Common Patterns

**Design patterns are reusable solutions to common programming problems. Use them appropriately, not dogmatically.**

---

### 4.2 Singleton Pattern

**Definition:**
Restricts the number of instances of a class to a single object.

**When to Use:**
- Logger objects
- Shared resources (database connections, file handles)
- Configuration objects for application
- Factory objects

**Example:**

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        # Initialize database connection
        pass

# Usage: Always returns same instance
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True
```

**Cautions:**
- [CAUTION] Can create tight coupling if overused
- [CAUTION] Makes testing harder (global state)
- [CAUTION] Consider dependency injection instead

---

### 4.3 Factory Pattern

**Definition:**
Centralizes object creation logic.

**Benefits:**
- [APPROVED] Application easier to extend and maintain
- [APPROVED] New implementations introduced with minimal changes
- [APPROVED] Reduces coupling
- [APPROVED] Improves code flexibility

**When to Use:**
- Multiple implementations of same interface
- Object creation is complex
- Need runtime decision on which class to instantiate

**Example:**

```typescript
// Product interface
interface PaymentProcessor {
  process(amount: number): void
}

// Concrete products
class MPesaProcessor implements PaymentProcessor {
  process(amount: number) {
    console.log(`Processing KES ${amount} via M-Pesa`)
  }
}

class CreditCardProcessor implements PaymentProcessor {
  process(amount: number) {
    console.log(`Processing ${amount} via Credit Card`)
  }
}

// Factory
class PaymentProcessorFactory {
  static create(type: string): PaymentProcessor {
    switch (type) {
      case 'mpesa':
        return new MPesaProcessor()
      case 'card':
        return new CreditCardProcessor()
      default:
        throw new Error(`Unknown payment type: ${type}`)
    }
  }
}

// Usage
const processor = PaymentProcessorFactory.create('mpesa')
processor.process(1000)
```

**Especially valuable in larger systems where scalability and maintainability are key concerns.**

---

### 4.4 Observer Pattern

**Definition:**
Objects (observers) subscribe to events from another object (subject).

**When to Use:**
- Event-driven systems
- UI updates based on data changes
- Notifications/alerts
- Real-time updates

**Example:**

```javascript
class Subject {
  constructor() {
    this.observers = []
  }
  
  subscribe(observer) {
    this.observers.push(observer)
  }
  
  unsubscribe(observer) {
    this.observers = this.observers.filter(obs => obs !== observer)
  }
  
  notify(data) {
    this.observers.forEach(observer => observer.update(data))
  }
}

class Observer {
  update(data) {
    console.log(`Observer notified with: ${data}`)
  }
}

// Usage
const subject = new Subject()
const observer1 = new Observer()
const observer2 = new Observer()

subject.subscribe(observer1)
subject.subscribe(observer2)
subject.notify('Important event!')
```

---

### 4.5 Pattern Combinations

**Singleton + Factory:**
Singleton can implement Factory when need single point of object creation. Use judiciously to avoid tight coupling.

**Factory + Observer:**
Factory creates different types of Observers. Often complement each other.

**Singleton + Observer:**
Singleton can implement Observer pattern for global event management. Be careful to avoid creating a "god object" that does too much.

---

## Section 5: Error Handling

### 5.1 Use try/catch/finally Blocks

**Recover from errors or release resources:**

```javascript
function readUserDataFromFile(filename) {
  let file = null
  try {
    file = openFile(filename)
    const data = file.read()
    return parseUserData(data)
  } catch (error) {
    console.error(`Failed to read user data: ${error.message}`)
    logError(error)
    return null
  } finally {
    // Always executes, even if exception thrown
    if (file) {
      file.close()  // Release resource
    }
  }
}
```

**Requirements:**
- [ ] Use try/catch for operations that can fail
- [ ] Always close resources in finally block
- [ ] Log errors with context
- [ ] Return sensible defaults or propagate error

---

### 5.2 Use Specific Exception Types

**More information equals better debugging:**

```python
# [REJECTED] BAD: Generic catch
try:
    process_file(filename)
except Exception as e:
    print("Something went wrong")

# [APPROVED] GOOD: Specific exceptions
try:
    process_file(filename)
except FileNotFoundError as e:
    print(f"File not found: {filename}")
    log_error(e)
except PermissionError as e:
    print(f"No permission to read: {filename}")
    log_error(e)
except ValueError as e:
    print(f"Invalid file format: {filename}")
    log_error(e)
```

**Benefits:**
- [APPROVED] Provides more information about what went wrong
- [APPROVED] Aids in debugging
- [APPROVED] Allows different handling for different error types

---

### 5.3 Catch Exceptions Only When Necessary

**Don't catch if you can't handle:**

```java
// [REJECTED] BAD: Catching but not handling
try {
    processPayment(user, amount);
} catch (PaymentException e) {
    // Empty catch - error silently ignored
}

// [APPROVED] GOOD: Handle or propagate
try {
    processPayment(user, amount);
} catch (PaymentException e) {
    log.error("Payment failed for user " + user.getId(), e);
    notifyUser(user, "Payment failed. Please try again.");
    throw e;  // Propagate to caller if can't fully handle
}
```

---

### 5.4 Log Exceptions

**Always log for debugging:**

```python
import logging

try:
    result = complex_calculation(data)
except CalculationError as e:
    logging.error(f"Calculation failed: {e}", exc_info=True)  # Include stack trace
    raise
```

**Requirements:**
- [ ] Log error message with context
- [ ] Include stack trace (exc_info=True, printStackTrace())
- [ ] Log at appropriate level (ERROR for exceptions)
- [ ] Include user ID, transaction ID, or other identifiers

---

### 5.5 Avoid Using Exceptions for Flow Control

**Exceptions are for exceptional conditions:**

```python
# [REJECTED] BAD: Using exceptions for control flow
def get_user_age(user_id):
    try:
        user = database.get_user(user_id)
        return user.age
    except UserNotFound:
        return None  # Expected case, not exceptional

# [APPROVED] GOOD: Use conditional logic
def get_user_age(user_id):
    user = database.find_user(user_id)  # Returns None if not found
    if user is None:
        return None
    return user.age
```

---

### 5.6 Handle Common Conditions to Avoid Exceptions

**Check before operation:**

```javascript
// [REJECTED] BAD: Let exception happen
function divide(a, b) {
  return a / b  // Throws if b is 0 (or returns Infinity)
}

// [APPROVED] GOOD: Prevent exception
function divide(a, b) {
  if (b === 0) {
    throw new Error("Division by zero")  // Explicit, clear error
  }
  return a / b
}
```

---

### 5.7 Design Classes So Exceptions Can Be Avoided

**Provide query methods:**

```csharp
// [APPROVED] GOOD: Provide safe alternative
class ShoppingCart {
    private List<Item> items;
    
    // Throws if cart empty
    public Item RemoveItem() {
        if (items.Count == 0) {
            throw new InvalidOperationException("Cart is empty");
        }
        return items.RemoveAt(0);
    }
    
    // Safe alternative: Check first
    public bool IsEmpty() {
        return items.Count == 0;
    }
}

// Usage
if (!cart.IsEmpty()) {
    Item item = cart.RemoveItem();
}
```

---

### 5.8 Restore State When Methods Don't Complete

**Maintain consistency:**

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def transfer(self, amount, destination_account):
        # Save original state
        original_balance = self.balance
        
        try:
            self.balance -= amount
            destination_account.deposit(amount)
        except Exception as e:
            # Restore state on failure
            self.balance = original_balance
            raise Exception(f"Transfer failed: {e}")
```

---

### 5.9 Capture and Rethrow Exceptions Properly

```python
# [REJECTED] BAD: Loses original stack trace
try:
    risky_operation()
except Exception as e:
    raise Exception("Operation failed")  # Original context lost

# [APPROVED] GOOD: Preserves stack trace
try:
    risky_operation()
except Exception as e:
    raise Exception("Operation failed") from e  # Python 3 syntax

# [APPROVED] GOOD: Add context while preserving trace
try:
    risky_operation()
except Exception as e:
    logging.error(f"Failed during user operation {user_id}", exc_info=True)
    raise  # Re-raises original exception with full trace
```

---

## Section 6: Code Documentation

### 6.1 Inline Comments

**Purpose:**
Explain small, complex, or non-obvious segments of code directly where written.

**When to Use:**
- Clarify tricky logic
- Explain purpose of regex
- Warn about potential side effects
- Document non-obvious workarounds

**Focus on WHY, not WHAT:**

```python
# [REJECTED] BAD: Narrates the obvious
x = x + 1  # Increment x by 1

# [REJECTED] BAD: Repeats code
if user.age >= 18:  # Check if user age is greater than or equal to 18
    grant_access()

# [APPROVED] GOOD: Explains business reasoning
# Users must be 18+ to comply with GDPR regulations for data collection
MINIMUM_AGE_FOR_CONSENT = 18
if user.age >= MINIMUM_AGE_FOR_CONSENT:
    grant_access()

# [APPROVED] GOOD: Documents non-obvious workaround
# Workaround for Safari bug where focus() fails immediately after element creation
# See: https://bugs.webkit.org/show_bug.cgi?id=12345
setTimeout(() => inputElement.focus(), 10)
```

**Best inline comments explain the reasoning behind code rather than just restating what it does.**

---

### 6.2 Docstrings

**Purpose:**
Document modules, classes, functions, and methods for API consumers.

**What Docstrings Explain:**
- Overall use and basic information
- What feature/function does
- What inputs it expects
- What outputs it returns
- Exceptions it might raise

**Difference from Comments:**
- **Docstring:** Tells you HOW to use a module/function/class
- **Comment:** Explains WHAT a specific line or block does

**Example:**

```python
def calculate_tax(income, tax_rate, deductions=0):
    """
    Calculate income tax after applying deductions.
    
    Args:
        income (float): Gross income in KES
        tax_rate (float): Tax rate as decimal (e.g., 0.3 for 30%)
        deductions (float, optional): Total deductions in KES. Defaults to 0.
    
    Returns:
        float: Tax amount in KES
    
    Raises:
        ValueError: If income or tax_rate is negative
    
    Example:
        >>> calculate_tax(100000, 0.3, 10000)
        27000.0
    """
    if income < 0 or tax_rate < 0:
        raise ValueError("Income and tax rate must be non-negative")
    
    taxable_income = income - deductions
    return taxable_income * tax_rate
```

**When to Write Docstrings:**
- All public modules, functions, classes, and methods
- Not necessary for non-public methods (but add comment describing what method does)

**The docstring is the contract your API agrees to adhere to.**

---

### 6.3 Documentation Update Frequency

**Update documentation:**
- Whenever code changes
- During pull requests
- At scheduled review intervals

**Keep documentation accurate and reliable.**

---

### 6.4 Avoid Over-Commenting

**Don't clutter codebase:**

```javascript
// [REJECTED] BAD: Excessive commenting
// Create a variable to store the user's name
let userName = "John"

// Check if the user's name is not empty
if (userName !== "") {
  // Print the user's name to the console
  console.log(userName)
}

// [APPROVED] GOOD: Let code speak
let userName = "John"

if (userName !== "") {
  console.log(userName)
}
```

---

---

## Section 7: Code Review Best Practices

### 7.1 Establish Clear Objectives

**Reviewers need to know what they're evaluating and why before they begin.**

**Code Review Checklist:**

**Functionality:** Does code work as intended, even if it doesn't generate obvious errors?

**Readability:** Could other developers easily understand and maintain code even if they had never encountered it before?

**Security:** Does code introduce risks that could be exploited? Does it close previously discovered security gaps?

**Performance:** Will code scale effectively under expected load conditions or when business expands?

**Tests:** Are there enough unit tests or automated checks?

---

### 7.2 For Code Authors

**1. Read Through Your Changes**

**Most important practice:**
Read through code change before submitting for review.

**Why:** There is nothing worse than asking several developers to look through code and give feedback on issues you could have fixed yourself.

**Consequences:**
- Wastes everyone's time
- Might make you look bad
- Developers may be reluctant to review your code in future

---

**2. Aim for Small Changes**

**Keep pull requests small and focused:**
- Easier to review
- Faster feedback
- Less context switching
- Lower chance of introducing bugs

**Recommended:** < 400 lines of code per PR

---

**3. Cluster Related Changes**

**Group logically related changes together:**
- Don't mix refactoring with new features
- Don't mix bug fixes with feature work
- One logical change per PR

---

**4. Provide a Description**

**Clear PR description includes:**
- What changed and why
- How to test
- Screenshots (for UI changes)
- Related tickets/issues
- Breaking changes
- Migration steps (if any)

---

**5. Run Tests**

**Before submitting:**
- [ ] Run all tests locally
- [ ] Ensure CI pipeline passes
- [ ] Fix any failures before requesting review

---

**6. Fewer Reviewers**

**Don't add everyone:**
- 1-2 reviewers optimal
- More reviewers equals slower reviews
- Diffusion of responsibility

---

**7. Be Open to Feedback**

**Accept criticism gracefully:**
- Code review is not personal attack
- Learn from feedback
- Ask questions if unclear
- Implement suggested changes or explain why not

---

**8. Show Gratitude**

**Thank reviewers for their time:**
- Encourages future reviews
- Builds team culture
- Recognizes their effort

---

### 7.3 For Code Reviewers

**9. Give Respectful Feedback**

**Be constructive, not critical:**

```
[REJECTED] BAD: "This code is terrible"
[APPROVED] GOOD: "Consider extracting this into a separate function for better readability"

[REJECTED] BAD: "Why would you do it this way?"
[APPROVED] GOOD: "Have you considered using pattern X? It might simplify this logic"
```

---

**10. Talk in Person**

**For complex discussions:**
- Hop on a call
- Walk to their desk
- Don't go back-and-forth in comments for 30 minutes

---

**11. Document Decisions**

**After discussions:**
- Summarize decision in PR comments
- Future reference for why approach was chosen
- Helps onboarding new team members

---

**12. Explain Your Viewpoint**

**When suggesting changes:**
- Explain reasoning
- Provide examples
- Link to documentation/standards

---

**13. Make Rejections Exceptions**

**Don't block PRs unnecessarily:**
- Minor issues: Approve with suggestions
- Major issues: Request changes
- Rejections should be rare

---

**14. Do Reviews Daily**

**Integrate into daily workflow:**
- Check PRs every morning
- Prevents bottlenecks
- Keeps team velocity high

---

**15. No Context-Switching**

**Batch review time:**
- Don't interrupt deep work for reviews
- Set dedicated review time
- Review multiple PRs at once

---

**16. Give Timely Feedback**

**Review within 24 hours:**
- Author's context still fresh
- Prevents blocking
- Maintains momentum

---

**17. Focus on Core Issues**

**Prioritize feedback:**
- Security issues: Critical
- Bugs: High priority
- Architecture: High priority
- Formatting: Low priority (use auto-formatters)

---

**18. Start with Test Code**

**Review tests first:**
- Understand what code should do
- Verify test coverage
- Check test quality
- Then review implementation

---

**19. Use Checklists**

**Ensure consistent reviews:**
- Security checklist
- Performance checklist
- Code quality checklist

---

**20. Fight Bias**

**Be aware of:**
- Confirmation bias (looking for what you expect)
- Authority bias (senior dev must be right)
- Recency bias (recent code looks better)

---

## Section 8: Refactoring

### 8.1 When to Refactor

**Best times:**

**1. Before Adding Updates or New Features**
- Clean up existing code first
- Makes new code easier to add
- Prevents compounding technical debt

**2. After Deploying to Production**
- Developers have more time
- Clean up code before next task
- Improve code without pressure

---

### 8.2 Identifying Code Smells

**Common indicators that refactoring is needed:**

**1. Code Duplication**
- Same logic in multiple places
- Extract into reusable functions

**2. Long Methods**
- Methods doing too much
- Break into smaller, focused methods

**3. Large Classes**
- Class has too many responsibilities
- Apply Single Responsibility Principle

**4. Long Parameter Lists**
- Function takes too many parameters
- Use parameter objects or builder pattern

**5. Divergent Change**
- One class changes for multiple reasons
- Split into separate classes

**6. Shotgun Surgery**
- One change requires modifying many classes
- Move related code together

---

### 8.3 Refactoring Techniques

**Three effective techniques:**

**1. Method-Focused Refactoring**
- Extract long methods into smaller ones
- Rename methods for clarity
- Remove duplicate code

**2. Method Call Refactoring**
- Simplify complex call chains
- Reduce parameter counts
- Use parameter objects

**3. Class-Focused Refactoring**
- Split large classes
- Extract interfaces
- Apply design patterns

---

### 8.4 Best Practices

**1. Code Reviews**

**Essential for spotting issues early:**
- Team members look for areas that can be improved
- Spot code smells
- Recommend refactorings
- Keep codebase clean

---

**2. Automated Tools for Code Quality**

**Tools help detect code smells and enforce standards:**
- **SonarQube:** Comprehensive code quality analysis
- **Checkstyle:** Java code style checker
- **PMD:** Static code analyzer
- **ESLint:** JavaScript linting
- **Pylint:** Python code checker

**Benefits:**
- [APPROVED] Provide valuable insights
- [APPROVED] Highlight areas needing attention
- [APPROVED] Indicate where refactoring is required

---

**3. Test-Driven Development (TDD)**

**Encourages writing small, testable functions:**
- Tests guide development process
- Ensures code remains clean
- Makes refactoring easier
- Writing tests before code ensures refactoring doesn't break functionality

---

**4. Refactor Incrementally**

**Small, incremental changes:**
- Refactoring doesn't need to be massive overhaul
- Better to make small changes
- Refactor a method, class, or function one at a time
- Ensure functionality remains unchanged

---

**5. Use Design Patterns**

**Reusable solutions to common problems:**
- Refactoring often involves applying appropriate design patterns
- Example: Strategy pattern can eliminate complex conditional statements

---

**6. Eliminate Code Duplication**

**Most common code smell:**
- Can be fixed by introducing helper methods or functions
- Consolidate duplicate code into reusable modules
- Ensures consistency
- Makes code easier to maintain

---

## Section 9: Technical Debt Management

### 9.1 What is Technical Debt?

**Definition:**
The "hidden cost" of shortcuts taken during development that must be paid back later.

**Types (Technical Debt Quadrant):**

| | Deliberate | Inadvertent |
|---------|-----------|------------|
| **Reckless** | "We don't have time for design" | "What's layering?" |
| **Prudent** | "We must ship now, deal with consequences" | "Now we know how we should have done it" |

---

### 9.2 Measuring Technical Debt

**Key Metrics:**

**1. Technical Debt Ratio (TDR)**

```
TDR = (Remediation Cost / Development Cost) × 100

Example:
Cost to fix technical debt: $50,000
Cost to rebuild from scratch: $500,000
TDR = (50,000 / 500,000) × 100 = 10%

Healthy: <5%
Warning: 5-10%
Critical: >10%
```

---

**2. Code Churn**

**Definition:** How often code is rewritten or changed.

**High churn indicates:**
- Unstable code
- Poor initial design
- Technical debt accumulation

---

**3. Cycle Time**

**Definition:** Time from starting work to deployment.

**Increasing cycle time suggests:**
- Code becoming harder to change
- Technical debt slowing development

---

**4. Defect Density**

```
Defect Density = Number of Defects / Lines of Code

Higher density = More technical debt
```

---

**5. Code Duplication**

**Measure:** Percentage of duplicate code

**Tools:** SonarQube, CodeClimate

**Target:** < 3% duplication

---

**6. Maintainability Index**

**Range:** 0-100 (higher is better)

**Factors:**
- Cyclomatic complexity
- Lines of code
- Halstead volume

**Scoring:**
- 85-100: Good maintainability
- 65-85: Moderate maintainability
- <65: Difficult to maintain

---

**7. Failed CI/CD Builds**

**Increasing failures indicate:**
- Brittle tests
- Poor code quality
- Growing technical debt

---

### 9.3 Management Strategies

**1. Acknowledge Debt**
- Make technical debt visible
- Track in backlog
- Don't hide or ignore

**2. Set Quality Standards**
- Code coverage minimums
- Code review requirements
- Automated quality gates

**3. Refactor Incrementally**
- Small, regular improvements
- Don't wait for "refactoring sprint"
- Boy Scout Rule: Leave code cleaner than you found it

**4. Automate Quality Checks**
- Static code analysis
- Automated testing
- CI/CD pipelines

**5. Maintain Technical Debt Backlog**
- Log known technical debt
- Prioritize by business impact
- Allocate time to address

**6. Replace Legacy Systems**
- When debt too high, consider rewrite
- Cost-benefit analysis
- Phased replacement

---

### 9.4 Best Practices

**Combine quantitative metrics + business impact to prioritize what to fix first.**

**Don't just measure technical debt - actively manage it:**
- Regular reviews
- Team discussions
- Scheduled refactoring time
- Balance new features with debt reduction

---

## Section 10: Additional Design Principles

### 10.1 KISS (Keep It Simple, Stupid)

**Definition:**
Simplicity over complexity.

**Application:**
- [APPROVED] Choose simplest solution that works
- [REJECTED] Over-engineer for hypothetical future needs
- [APPROVED] Clear, straightforward code over clever tricks

---

### 10.2 YAGNI (You Aren't Gonna Need It)

**Definition:**
Don't build features you don't need yet.

**Application:**
- [APPROVED] Implement only current requirements
- [REJECTED] Build infrastructure for potential future features
- [APPROVED] Wait until feature is actually needed

---

### 10.3 Separation of Concerns (SoC)

**Definition:**
Distinct sections for distinct purposes.

**Application:**
- Business logic separate from UI
- Data access separate from business logic
- Each module handles one concern

---

### 10.4 Composition over Inheritance

**Definition:**
Favor object composition over class inheritance.

**Why:**
- [APPROVED] More flexible
- [APPROVED] Easier to modify behavior at runtime
- [REJECTED] Deep inheritance hierarchies become brittle

**Example:**

```typescript
// [REJECTED] BAD: Deep inheritance
class Animal { }
class Mammal extends Animal { }
class Dog extends Mammal { }
class Labrador extends Dog { }

// [APPROVED] GOOD: Composition
class Dog {
  constructor(
    private behavior: Behavior,
    private appearance: Appearance
  ) {}
}
```

---

### 10.5 High Cohesion & Low Coupling

**High Cohesion:**
Related code together in same module/class.

**Low Coupling:**
Minimal dependencies between modules.

**Benefits:**
- [APPROVED] Easier to maintain
- [APPROVED] Easier to test
- [APPROVED] Easier to reuse

---

### 10.6 Fail Fast

**Definition:**
Detect and report errors immediately.

**Application:**
- Validate inputs at function entry
- Throw exceptions for invalid state
- Don't silently ignore errors

---

### 10.7 Convention over Configuration

**Definition:**
Sensible defaults reduce decisions.

**Application:**
- Default configurations for common cases
- Allow customization when needed
- Reduce boilerplate

---

## Complete Programming Standards Verification Checklist

**Before committing code, verify ALL of these:**

### Clean Code Principles
- [ ] Meaningful and descriptive names
- [ ] No magic numbers (constants defined)
- [ ] DRY principle followed
- [ ] Functions small and focused (< 20 lines)
- [ ] Comments explain WHY, not WHAT
- [ ] Consistent formatting applied
- [ ] Principle of Least Knowledge followed

### SOLID Principles
- [ ] Single Responsibility: Each class has one reason to change
- [ ] Open-Closed: Extend without modifying
- [ ] Liskov Substitution: Subtypes substitutable
- [ ] Interface Segregation: Many small interfaces
- [ ] Dependency Inversion: Depend on abstractions

### Naming Conventions
- [ ] Language-specific conventions followed
- [ ] Verbs for functions, nouns for classes
- [ ] Boolean functions prefixed with is/has/can
- [ ] Descriptive and specific names

### Design Patterns
- [ ] Appropriate patterns used (not forced)
- [ ] Singleton used sparingly
- [ ] Factory for complex object creation
- [ ] Observer for event-driven systems

### Error Handling
- [ ] try/catch/finally blocks used appropriately
- [ ] Specific exception types
- [ ] Exceptions logged with context
- [ ] No exceptions for flow control
- [ ] Resources released in finally blocks
- [ ] State restored on failure

### Code Documentation
- [ ] Inline comments explain WHY
- [ ] Docstrings for all public APIs
- [ ] Documentation updated with code changes
- [ ] No over-commenting

### Code Review
- [ ] PR < 400 lines
- [ ] Tests run locally before submitting
- [ ] Description provided
- [ ] 1-2 reviewers assigned
- [ ] Feedback addressed or discussed

### Refactoring
- [ ] Code smells identified
- [ ] Incremental refactoring applied
- [ ] Tests pass after refactoring
- [ ] No duplicate code

### Technical Debt
- [ ] Technical debt tracked
- [ ] Code quality metrics monitored
- [ ] Regular refactoring scheduled
- [ ] Quality standards enforced

### Additional Principles
- [ ] KISS: Simplicity over complexity
- [ ] YAGNI: Build only what's needed
- [ ] Separation of Concerns applied
- [ ] Composition over Inheritance
- [ ] High Cohesion & Low Coupling
- [ ] Fail Fast for errors

**If ANY checkbox fails, address before committing to production.**

---

## When to Read This Canon

**This programming standards canon should be read during development:**

- Writing new code
- Refactoring existing code
- Code reviews
- Architecture design
- Technical debt assessment
- Team onboarding

**This is a foundational canon that applies to all development work.**

---

## Version

Programming Standards Canon Version: 1.0 - Complete (December 30, 2025)  
Based on industry research and best practices for software development.

Covers 10 comprehensive categories:
1. Clean Code Principles
2. SOLID Principles
3. Naming Conventions
4. Design Patterns
5. Error Handling
6. Code Documentation
7. Code Review Best Practices
8. Refactoring
9. Technical Debt Management
10. Additional Design Principles (KISS, YAGNI, SoC, Composition over Inheritance, etc.)

