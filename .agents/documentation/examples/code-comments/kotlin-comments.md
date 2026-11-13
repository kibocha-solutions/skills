# Kotlin Comment Examples

Use KDoc `/** ... */` for API documentation that tools such as IntelliJ IDEA,
Android Studio, and Dokka should read. Use Dokka include Markdown for module
and package overviews. Use `//` or `/* ... */` only for local implementation
notes.

## Package Level

```md
# Package com.example.billing.scheduler

Provides recurring billing job scheduling for tenant-scoped invoice runs.

Callers submit tenant IDs and cutoff times. This package owns job ordering,
duplicate-run protection, and retry scheduling.
```

## Class Level

```kotlin
/**
 * Coordinates one billing run for a single tenant account.
 *
 * The runner records audit events for every attempted charge and skips invoices
 * that another worker has already marked as in flight.
 *
 * @param T The tenant identifier type used by the caller's account system.
 * @param invoices Repository used to load and mark invoices for payment.
 * @param gateway External payment gateway used for charge submission.
 * @property tenantId The tenant whose invoices this runner may charge.
 * @constructor Creates a runner for one tenant billing run.
 * @see BillingRunResult
 */
class TenantBillingRunner<T>(
    val tenantId: T,
    invoices: InvoiceRepository,
    gateway: PaymentGateway,
)
```

## Function Level

```kotlin
/**
 * Charges unpaid invoices that are due at or before [cutoff].
 *
 * The operation is idempotent for a given invoice ID: invoices marked
 * `paymentInFlight` are skipped so a resumed job does not submit duplicate
 * gateway requests. Gateway failures are recorded and returned to the caller
 * instead of being thrown after the first failed charge.
 *
 * @param cutoff Latest due time eligible for charging.
 * @return Summary of charged, skipped, and failed invoices.
 * @throws AuthorizationException If the runner is not allowed to charge the
 * tenant.
 * @sample com.example.billing.samples.chargeDueInvoices
 */
suspend fun chargeDueInvoices(cutoff: Instant): BillingRunResult
```

## Extension Function Level

```kotlin
/**
 * Converts this invoice into a gateway request for [tenantId].
 *
 * @receiver Invoice that has already passed local validation.
 * @param tenantId Tenant identifier sent to the payment gateway.
 * @return Gateway request containing only chargeable invoice fields.
 */
fun Invoice.toGatewayRequest(tenantId: TenantId): GatewayRequest
```

## Implementation Note

```kotlin
// Lock before loading invoices so concurrent workers agree on the same
// paymentInFlight marker before either worker reaches the gateway.
tenantLock.withLock(tenantId) {
    val dueInvoices = invoices.findDueForUpdate(tenantId, cutoff)
    submitCharges(dueInvoices)
}
```

```kotlin
/*
 * Keep this as a regular block comment because it explains local migration
 * behavior, not the public API contract that Dokka should publish.
 */
val legacyAccountId = normalizeLegacyAccountId(rawAccountId)
```
