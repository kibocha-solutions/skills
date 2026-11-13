# Access Level Classification

Use this reference when deciding where documentation belongs in the
confidentiality ladder and which Writerside instance may publish it.

## Ladder

- Public: safe for external readers.
- Internal: safe for employees, maintainers, or the engineering/product team.
- Restricted: limited to security, operations, compliance, or authorized
  maintainers.
- Confidential: limited to explicitly authorized stakeholders.
- Snippet library: reusable snippets; classify each snippet at the highest
  sensitivity of its content.

## Classification Rules

- Public may flow upward into Internal or Restricted instances.
- Internal must not flow into Public unless sanitized.
- Restricted must not flow into Public or Internal unless sanitized and
  reclassified.
- Confidential must not flow into lower levels unless the content is rewritten
  from safe facts.
- Snippets inherit the highest sensitivity of included content.

## Default Placements

- Public: user guides, public API integration, support docs, public changelog,
  sanitized release notes.
- Internal: project brief, architecture overview, ADRs, domain model, database
  schema, testing, deployment, CI/CD, internal APIs.
- Restricted: security baseline, threat models, permission and tenant
  isolation, data classification, precise infrastructure internals, incident
  details.
- Confidential: client-confidential context, donor or beneficiary-sensitive
  material, private scoring logic, executive strategy, protected IP, financial
  terms.

## Workflow

1. Identify the most sensitive fact in the document.
2. Classify the document at that level unless the sensitive fact can be removed.
3. If the document will be reused, classify reusable fragments independently.
4. Add or update the appropriate Writerside tree only after classification.
5. For public output, perform a sanitization pass before publication.

## Validation

- No lower-sensitivity instance includes higher-sensitivity content.
- Public docs do not expose internal URLs, secrets, private endpoints, scoring
  logic, security internals, or sensitive people/data.
- Classification is stated or inferable where reuse creates risk.
