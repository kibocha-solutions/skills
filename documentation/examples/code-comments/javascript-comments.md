# JavaScript Comment Examples

Use JSDoc `/** ... */` for generated API documentation. Use `//` or
`/* ... */` for local implementation notes that should stay out of API docs.

## Module Level

```javascript
/**
 * @module retryQueue
 *
 * Persists webhook retry attempts and exposes the dispatcher-facing claim API.
 * Callers must validate webhook signatures before enqueueing work here.
 */
```

## Type Definition Level

```javascript
/**
 * @typedef {object} RetryJob
 * @property {string} id Stable job identifier used for idempotent dispatch.
 * @property {Date} nextAttemptAt Earliest time the job may be claimed again.
 * @property {number} attemptCount Number of completed delivery attempts.
 */
```

## Class Level

```javascript
/**
 * Claims webhook retry jobs without allowing two dispatchers to process the
 * same job at the same time.
 *
 * The queue depends on the database transaction isolation level documented in
 * the repository adapter. It is safe to share one instance across requests.
 *
 * @template TJob
 */
export class RetryQueue {
  /**
   * @param {RetryRepository} repository Storage adapter that owns claim
   *   transactions.
   * @param {Clock} clock Clock used only for metrics and logging.
   */
  constructor(repository, clock) {
    this.repository = repository;
    this.clock = clock;
  }
}
```

## Function Level

```javascript
/**
 * Claims up to `limit` jobs that are ready for another delivery attempt.
 *
 * @template TJob
 * @param {number} limit Maximum number of jobs to claim. Values above 100 are
 *   rejected to keep one dispatcher from starving others.
 * @param {string[]} [tenantIds] Optional tenant allowlist.
 * @param {...string} jobTypes Retry job types eligible for this claim.
 * @returns {Promise<TJob[]>} Jobs ordered by next attempt time, oldest
 *   first.
 * @throws {RangeError} When `limit` is less than 1 or greater than 100.
 */
export async function claimReadyJobs(limit, tenantIds, ...jobTypes) {
  // ...
}
```

## Implementation Note

```javascript
// Use the database clock so dispatchers on different hosts do not disagree
// about which jobs are ready.
const readyAt = await repository.currentTimestamp();
```

```javascript
/*
 * This remains a regular block comment because it explains a local adapter
 * workaround, not a generated API contract.
 */
const retryWindow = normalizeLegacyRetryWindow(rawRetryWindow);
```
