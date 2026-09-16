# Document Co-Authoring Examples: Good vs Bad Interview Patterns

## 1. Context Gathering Questions

### Bad (Vague, Open-Ended Inquiries)

```text
1. Tell me about your project and what you want to achieve.
2. What should the document say?
3. Who do you think might read this document?
4. Do you have any thoughts on how long it should be?
5. What else should I know?
```

Defects:
- Burdens the user with open-ended essay questions.
- Fails to extract concrete technical boundaries or constraints.
- Does not surface unstated assumptions or failure modes.

### Good (Targeted, Numbered Decision Prompts)

```text
1. Document Category: Are we authoring a technical RFC (architecture review) or a product PRD (feature delivery)?
2. Decision Gate: Who is the primary approving stakeholder, and what specific decision must they make upon reading this document?
3. Service Level Objective: What are the target latency (p95/p99) and availability (e.g. 99.9%) thresholds for this feature?
4. Failure Behavior: When the downstream notification queue is full, should the service drop non-critical events or apply backpressure to checkout?
5. Migration Strategy: Will this deploy as an atomic cutover or run in parallel shadow mode for 14 days?
```

Advantages:
- Surfaces specific operational tradeoffs and failure behavior.
- Allows user to answer in short numbered points.
- Directly informs substantive architecture sections.
