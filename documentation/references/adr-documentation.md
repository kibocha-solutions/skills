# ADR Documentation

Use this reference for Architecture Decision Records and durable technical
decisions.

## Required Sources

- Existing ADRs and decision logs.
- Relevant code, config, dependency files, issues, PRs, benchmarks, or design
  notes.
- MADR guidance and templates: https://adr.github.io/madr/

## Default Paths

- ADR directory: `docs/architecture/decisions/`
- ADR topic: `docs/architecture/decisions/<decision-name>.md`
- Lightweight index: `docs/planning/decision-log.md`

## Required Content

An ADR must include:

- status
- date
- context
- considered options
- decision
- consequences, including trade-offs and accepted debt
- links to related code, issues, PRs, docs, or follow-up decisions

Use `../assets/madr-adr-template.md` when creating a new ADR.

## Workflow

1. Decide whether the change needs a full ADR or only a decision-log entry.
   Use an ADR for foundational, hard-to-reverse, cross-team, security,
   architectural, data, or vendor decisions.
2. Gather evidence for the context and options. Do not invent rejected options.
3. State the decision directly.
4. Include negative consequences. ADRs fail when they read like advocacy.
5. Add the ADR to `internal.tree`; hide old or narrow ADRs if sidebar bloat is
   likely.

## Validation

- The decision can be understood without reading the original discussion.
- Options are real alternatives, not straw choices.
- Consequences include operational, security, migration, and maintenance impact
  when relevant.
- The status is current.
