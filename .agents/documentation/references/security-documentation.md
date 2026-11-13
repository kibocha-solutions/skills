# Security Documentation

Use this reference for security baselines, threat models, access control,
privacy, data handling, compliance, and sensitive architecture documentation.

## Required Sources

- Auth code, permission checks, roles, policies, secrets handling, dependency
  config, infrastructure, data flows, logs, incident notes, and existing
  security reviews.
- OWASP Secure Coding Practices:
  https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- OWASP threat modeling playbook:
  https://github.com/OWASP/threat-modeling-playbook

## Default Paths

- `docs/security/security-baseline.md`
- `docs/security/permission-tenant-isolation.md`
- `docs/security/auth-authorization.md`
- `docs/security/threat-model.md`
- `docs/security/privacy-data-handling.md`
- `docs/data/data-classification.md`

## Required Content

- Assets, actors, roles, trust boundaries, and data flows.
- Authentication and authorization model.
- Tenant isolation and permission invariants.
- Secrets, logging, dependency, input-validation, output-encoding, and
  transport-security baseline.
- Data classification and handling rules.
- Threats, mitigations, residual risk, owner, and review cadence.

Use `../assets/owasp-threat-model-template.md` for threat models.

## Workflow

1. Classify security docs as Restricted by default unless they are explicitly
   sanitized for Public output.
2. Use local code and infrastructure as truth. Do not invent controls.
3. Route topology, trust-boundary, data-flow, and threat diagrams to
   `technical-diagrams`.
4. Keep public security docs high-level and sanitized.
5. Record unknowns and required review instead of filling gaps with confident
   claims.

## Validation

- Every control has local evidence or is marked as planned.
- Threats map to assets, trust boundaries, and mitigations.
- Sensitive internals are not included in public docs.
- Data classes have handling rules.
