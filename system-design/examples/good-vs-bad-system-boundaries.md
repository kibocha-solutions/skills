# System Design Examples: Good vs Bad Boundaries

## 1. Domain Service and State Separation

### Bad (God Service, Leaked State, and Anemic Boundaries)

```text
UserManagementService:
  - Handles user authentication (passwords, 2FA, JWT generation).
  - Handles profile editing and avatar uploads.
  - Sends marketing emails and promotional push notifications.
  - Processes Stripe credit card payments and calculates VAT.
  - Directly updates the orders table during checkout.
```

Defects:
- Single component owns unrelated bounded contexts (Identity, Media, Marketing, Billing, Commerce).
- High coupling: a change to marketing email templates risks destabilizing user authentication.
- Distributed transaction hazards: directly mutates billing and order state without clean transaction boundaries.

### Good (Focused Bounded Contexts with Explicit Contracts)

```text
IdentityService:
  - Owns user credentials, authentication tokens, and authorization claims.
  - Emits: UserRegisteredEvent, PasswordChangedEvent.
  - Excludes: Payment details, marketing preferences, order history.

BillingService:
  - Owns payment methods, invoices, and Stripe gateway integration.
  - Consumes: OrderPlacedEvent.
  - Emits: PaymentCapturedEvent, PaymentFailedEvent.
  - Excludes: User login credentials, product catalog data.

NotificationService:
  - Consumes events and dispatches customer emails/SMS based on user channel preferences.
  - Excludes: Domain business logic, credit card numbers.
```

Advantages:
- Single responsibility: each service owns a distinct lifecycle and data model.
- Decoupled via asynchronous domain events.
- Independent deployability and failure isolation.
