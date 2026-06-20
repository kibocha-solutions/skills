# ERD Design

## Brainstorming Constraints

During ERD brainstorming, reason with concrete workflows and row changes. Use
tables in chat when they help the user compare designs. Once a design is
settled, record examples in the `.agents/brain` table file so the examples
survive outside the conversation.

## Settled Table File Shape

Use this shape for ERD working notes unless the project already has a stronger
local standard:

```markdown
# table_name

| Aspect | Value |
| --- | --- |
| Responsibility | Dense statement of what the table stores, when rows are created, who uses it, and what does not belong here. |
| Primary key | `id` |
| Natural key | State the natural key or say none is stable enough. |
| Normal form target | 3NF, BCNF, or 4NF where relevant. |
| Cardinality | Explain parent/child relationships in plain language. |

| Column | Data type | Value | Relationship | Notes |
| --- | --- | --- | --- | --- |
| `id` | `uuid` or project ID type | Required, generated | PK | Random, non-guessable internal identifier. |

## Boundaries

State what does not belong in this table.

## Example Rows

Provide realistic rows with random, non-guessable IDs.

## Normalization Check

Give a short 3NF/BCNF/4NF check when table placement is disputed.
```

Use `Value` rather than `Requiredness` when the column table needs to describe
required values, nullability, default values, generated values, or lifecycle
conditions.

## Column Notes

Column notes should be clear and complete. Include one or two sample values
when the value is not obvious. State why the column exists when misuse is
likely.

Weak note:

| Column | Notes |
| --- | --- |
| `subject_type` | Polymorphic subject. |

Useful note:

| Column | Notes |
| --- | --- |
| `record_table` | Names the table that owns the lifecycle row, such as `source_records`, `record_files`, or `upload_sessions`. Use only approved table names. Prefer concrete foreign keys in domain-specific tables when this flexible reference becomes hard to reason about. |

## Example Rows

Example rows should show behavior, not decorative filler. Use values that
demonstrate normal, edge, and failure states.

Rules:

- Use random, non-guessable IDs such as UUID-like values or project-approved
  opaque IDs.
- Do not use sequential example IDs like `1`, `2`, or `3`.
- Include enough columns to show the table's purpose.
- Include around five rows when the table has varied behavior. Use fewer only
  when the concept is small.

## Normalization Checks

Use quick normalization checks to decide whether a table belongs separately:

| Question | Signal |
| --- | --- |
| Do all non-key columns depend on the row's key? | If not, split the table or move the column. |
| Can the row exist before a related user or organization is known? | Do not force the table under `users` or `organizations`. |
| Are many columns nullable because they belong to only one subtype? | Consider subtype tables or a clearer split. |
| Is the table really an activity, audit, usage, or security stream? | Place it in shared/log/security planning, not inside the domain object. |
| Is a summary derived from atomic rows? | Defer or mark it as a cache/materialized view, not source truth. |

## Research

Use authoritative sources when a table touches authentication, password
storage, SSO, MFA, security logging, privacy, database constraints, or a formal
notation. Record which standard or source shaped the design when the source
material affects a table name, responsibility, column, or lifecycle.

