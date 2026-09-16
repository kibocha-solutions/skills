---
name: system-design
description: Design and audit system architecture, ERDs, database schemas, domain models, services, integrations, deployments, permissions, workflows, activities, sequences, and state machines before implementation. Use for design decisions, normalization, boundaries, responsibilities, lifecycle behavior, naming, or diagram-ready specifications.
---

# System Design

## 1. Establish scope

1. Identify the design type and requested decision.
2. Identify the system boundary, users, actors, data, services, integrations, environments, and constraints.
3. Identify whether the user authorized design only, documentation, diagrams, or implementation.
4. Keep implementation out of a design-only task.
5. Record unresolved boundaries as unresolved.

## 2. Read project truth

1. Read relevant `.agents/MEMORY.md` entries and topic files.
2. Read relevant active plans, handoffs, and settled design records.
3. Read existing schemas, migrations, code, tests, docs, and diagrams.
4. Use graph tools before filesystem search when a current code graph exists.
5. Verify external standards and framework behavior with primary sources.
6. Keep current implementation, settled decisions, proposals, and examples distinct.

## 3. Model real workflows

1. List the primary user and system workflows.
2. Trace creation, reading, change, approval, failure, retry, cancellation, archival, and deletion.
3. Trace normal, edge, and adversarial cases.
4. Identify the source of truth for each state and fact.
5. Identify operations that require atomicity, idempotency, ordering, or eventual consistency.
6. Identify audit, security, privacy, retention, and recovery requirements.

## 4. Define responsibilities and boundaries

Read [naming and responsibility](references/naming-and-responsibility.md).

1. Give every component one clear responsibility.
2. State what each component owns.
3. State what each component excludes.
4. State when it is created, changed, and retired.
5. State which actors and workflows use it.
6. Separate independently meaningful components.
7. Separate domain state from audit, security, usage, and operational streams.
8. Reject boundaries that depend only on current screen layout or implementation convenience.

## 5. Name components

1. Use concise, familiar domain terms.
2. Prefer names supported by local vocabulary and primary-source precedent.
3. Avoid vague doctrine terms, clever abbreviations, generic `subject` fields, and names that encode an explanation.
4. Use documentation for meaning that does not belong in the name.
5. Preserve meaningful supplied spelling and multilingual terms.
6. Ask before replacing a disputed name.

## 6. Design data and ERDs

Read [ERD design](references/erd-design.md).

1. Define the row responsibility for every table.
2. Identify candidate keys, primary keys, alternate keys, and foreign keys.
3. Identify every functional, multivalued, and join dependency.
4. Test 1NF, 2NF, 3NF, BCNF, 4NF, and 5NF where applicable.
5. Split independently changeable facts.
6. Verify lossless decomposition.
7. Verify dependency preservation.
8. Test insert, update, and delete anomalies.
9. Test lifecycle behavior before and after related entities exist.
10. Prefer concrete foreign keys.
11. Use polymorphic references only after documenting allowed targets, integrity enforcement, and query behavior.
12. Mark derived summaries as caches, views, or materialized views rather than source truth.
13. Use opaque non-guessable example identifiers.
14. Include normal, edge, and failure example rows.

## 7. Design behavior

1. Define actors, commands, events, states, transitions, guards, and outcomes.
2. Give every transition one trigger and one resulting state.
3. Define invalid transitions.
4. Define retries, timeouts, compensation, and recovery.
5. Define permission checks at the operation boundary.
6. Define integration failure and partial-success behavior.
7. Define observability without mixing logs into domain state.

## 8. Compare alternatives

1. Present only alternatives that materially differ.
2. Test each alternative against the same workflows and constraints.
3. Compare responsibility clarity, coupling, integrity, change isolation, query cost, operational risk, and migration cost.
4. Identify irreversible choices.
5. Recommend one design when the evidence supports it.
6. Leave the decision open when the evidence does not resolve it.
7. Record rejected alternatives only when the rejection prevents repeated design errors.

Read [bad patterns](references/bad-patterns.md).

## 9. Record the settled design

Read [design workflow](references/design-workflow.md).

1. Keep unstable brainstorming in chat.
2. Record accepted design decisions under the project's `.agents/brain/<domain>/` convention.
3. Include responsibilities, boundaries, names, relationships, examples, constraints, lifecycle, open questions, and rejected alternatives.
4. Make the record understandable without chat history.
5. Do not present an unaccepted candidate as settled.

## 10. Promote the design

1. Obtain user acceptance before moving a disputed or conceptual design into implementation.
2. Use the documentation skill for maintained prose and data dictionaries.
3. Use the technical-diagrams skill for production diagrams and exports.
4. Use Maestro for multi-session execution.
5. Keep the accepted design record as the implementation source.
6. Record implementation deviations and obtain approval when they change the accepted design.

## 11. Verify

1. Re-run every named workflow against the final design.
2. Re-run edge, failure, permission, and lifecycle cases.
3. Verify every component has one responsibility and explicit exclusions.
4. Verify names against local vocabulary.
5. Verify every relationship, cardinality, constraint, and transition.
6. Verify normalization claims with declared dependencies.
7. Verify diagrams and documentation match the settled design.
8. Read the final design record in full.

Inspect [boundary examples](examples/good-vs-bad-system-boundaries.md) for service decoupling patterns.

## 12. Pre-completion checklist

Before delivering any system design specification, confirm evidence exists for each item:

- [ ] Existing schemas, code, and project truth read manually in full from start to finish.
- [ ] Every component has a single responsibility and explicit ownership boundaries.
- [ ] Normalization verified (dependencies stated, anomalies eliminated).
- [ ] State machines define explicit transitions, invalid transitions, and compensation paths.
- [ ] Technical diagrams match the settled design without notation drift.
- [ ] Zero AI attribution in design documents, diagrams, or specifications.
- [ ] No U+2014 em dashes in normal prose.

