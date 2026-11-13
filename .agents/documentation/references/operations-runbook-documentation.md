# Operations and Runbook Documentation

Use this reference for operations runbooks, incident response, alert handling,
monitoring, backup, and recovery procedures.

## Required Sources

- Alerts, dashboards, logs, deployment docs, backup scripts, incident notes,
  on-call policy, service ownership, and previous incidents.
- Google SRE incident response:
  https://sre.google/workbook/incident-response/

## Default Paths

- `docs/operations/incident-response.md`
- `docs/operations/monitoring-alerting.md`
- `docs/operations/runbooks/<incident>.md`
- `docs/data/backup-recovery.md`

## Required Content

Runbooks must include:

- symptoms
- impact and severity
- prerequisites and required access
- diagnosis steps
- remediation steps
- rollback or recovery
- verification
- escalation path
- owner and last validated date

Use `../assets/sre-runbook-template.md` when creating a runbook.

## Workflow

1. Write runbooks only for real repeatable operational tasks or triggered P2
   readiness. Avoid pre-coding runbook theater.
2. Use exact commands, dashboard names, alert names, paths, and expected
   outputs.
3. Keep incident response policy separate from individual remediation runbooks.
4. Put confidential incident details in Restricted or Confidential outputs.
5. Include verification after every remediation path.

## Validation

- A responder can act without guessing.
- Dangerous commands include scope and rollback.
- Escalation contacts or roles are current.
- Last validated date is present for critical runbooks.
