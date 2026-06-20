# Bad Patterns

Use these examples to avoid repeating design failures.

| Pattern | Problem | Correction |
| --- | --- | --- |
| Table name carries the whole explanation | The name becomes awkward while the table still needs documentation. | Use a standard name and write a dense responsibility. |
| Responsibility is one abstract phrase | Future readers guess what rows mean. | State what rows represent, when they are created, who uses them, and what is excluded. |
| `subject_type` and `subject_id` appear by default | Flexible references become invisible architecture. | Prefer concrete foreign keys. Use flexible references only when the design has a reason and exact examples. |
| Event/log tables are placed inside a domain object | Login attempts, audits, usage, and security streams may reference users but are not usually user-owned identity data. | Place them in shared, logs, security, or operations planning according to their source of truth. |
| Names use in-house doctrine | New contributors cannot infer meaning. | Use common names such as `permissions`, `roles`, `grants`, `usage`, or `audits`. |
| Documentation loses the settled examples | Reader-facing docs become vague prose. | Carry useful examples from `.agents/brain` into docs when they teach behavior. |
| Diagram labels hide uncertainty | A clean diagram can make an unsettled relationship look final. | Keep uncertain relationships in brainstorm notes until accepted, then draw. |

## Specific Examples

| Avoid | Reason | Prefer |
| --- | --- | --- |
| `authority` for schema or table area | Doctrine word with unclear database meaning. | `permissions` |
| `user_security_events` in identity scope | Security/logging stream, not atomic user identity. | Plan `audits`, `security_logs`, or `activity` in the appropriate shared/log area. |
| `user_login_attempts` as a child of `users` | Failed attempts may not resolve to a known user. | `login_attempts` near auth/security planning. |
| `usage_events` when the team wants shorter standard names | Overexplains the event nature in the name. | `usage`, with exact row responsibility and examples. |
| `lifecycle_events` without explanation | The table name does not say whose lifecycle or why rows exist. | `lifecycles` or a documented lifecycle table with dense responsibility and examples. |

