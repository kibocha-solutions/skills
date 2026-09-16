# Discernment Nudge Examples: Good vs Bad Patterns

## 1. Technical Recommendation Follow-Up

### Context
Assistant recommended migrating a legacy monolith database from PostgreSQL to DynamoDB to handle projected Black Friday traffic.

### Bad (Generic, Open-Ended, and Conversational)

```text
A few things worth a second look:
- Have you thought about whether DynamoDB is really the best choice for you?
- What do you think about the cost implications of this migration?
- Is your team ready for this?
- Let me know if you want me to help with anything else!
```

Defects:
- Generic questions that do not cite specific technical tradeoffs or figures.
- Includes four questions instead of the maximum of three.
- Adds an extraneous conversational closing invitation ("Let me know...").

### Good (Targeted, Specific, First-Person)

```text
A few things worth a second look:
- Can my query patterns operate without relational joins between users and orders?
- Will provisioned capacity handle the 4x spike without exceeding our $10,000 monthly budget?
- Have we tested DynamoDB local latency against our current European read replicas?
```

Advantages:
- Points directly to concrete architectural constraints (relational joins, $10,000 budget, European latency).
- Phrased in first person for direct re-submission.
- Exactly three bullets with no extra closing text.
