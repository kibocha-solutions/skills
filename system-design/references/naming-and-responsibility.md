# Naming And Responsibility

## Naming Standard

Names should be boring, standard, and recognizable. A new contributor should
get a useful first guess from the name without learning in-house doctrine.

| Good direction | Risky direction |
| --- | --- |
| `users`, `organizations`, `permissions`, `usage`, `audits` | `identity`, `authority`, `interaction`, `subject`, `activity_context` |
| `user_authenticators`, `user_sessions`, `login_attempts` | `user_security_events`, `user_interactions`, `actor_subject_links` |
| `background_jobs`, `validations`, `lifecycles` | overlong names that try to explain every use case |

Use the table, class, state, activity, or module documentation to explain the
concept. Do not force the full explanation into the name.

## Responsibility Text

Each settled design artifact should carry a dense responsibility statement.
For a database table, that statement should say:

- what rows represent;
- when rows are created or updated;
- which workflows or services use the table;
- what the table excludes;
- which nearby table or artifact owns excluded behavior.

Weak responsibility:

| Aspect | Value |
| --- | --- |
| Responsibility | Product lifecycle history. |

Useful responsibility:

| Aspect | Value |
| --- | --- |
| Responsibility | Stores durable lifecycle records for business objects when the product needs to show how a record moved between meaningful states, such as upload requested, file accepted, version superseded, deletion requested, deletion blocked, or public export created. Rows are created by application workflows and workers after the business action occurs. This table is not the security audit log, not a billing meter, and not a recursive log of its own inserts. |

## Bad Names And Corrections

| Bad pattern | Why it fails | Better approach |
| --- | --- | --- |
| Vague doctrine terms in schema names | The term may be meaningful in product prose but unclear in a database or diagram. | Use plain names such as `permissions`, `roles`, or `grants`. |
| Over-explained table names | Long names become awkward while still leaving behavior unclear. | Use a standard name and document responsibility clearly. |
| Generic `subject` wording everywhere | Readers cannot tell what the row points to. | Prefer concrete foreign keys. If flexible references are needed, document exact allowed values and examples. |
| Logging tables inside identity or storage | The table describes an operational stream, not the domain object. | Place logs, audits, usage, and security monitoring in shared/log/security planning areas. |

