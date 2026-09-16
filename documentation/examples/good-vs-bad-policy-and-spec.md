# Documentation Examples: Good vs Bad Patterns

## 1. Operative Text vs Explanatory Bloat

### Bad (Explanatory Bloat Masked as Rules)

```markdown
### 3. Key Rotation

In order to make sure that the security posture of the organization remains optimal and because stale keys represent a serious threat vector that could compromise customer records, all engineering staff should try to rotate their SSH keys every 90 days. We do this to comply with SOC2 requirements and to ensure alignment with our security roadmap as documented in /mnt/data/workspace/.agents/brain/security-plan.md. Keys that are about 90 days old (approximately 3 months) should ideally be flagged by the platform team.
```

Why this fails:
- Mansplains the rationale ("In order to make sure...", "because stale keys represent...") inside operative procedure text.
- Uses weak hedging and non-binding verbs ("should try to", "should ideally").
- Narrates compliance reasons ("We do this to comply with SOC2...").
- Leaks internal repository paths (`/mnt/data/workspace/.agents/brain/security-plan.md`).
- Uses quantity hedges ("about 90 days old (approximately 3 months)").

### Good (Direct Imperative Rules with Purpose Separation)

```markdown
## 1. Purpose

This policy establishes key rotation schedules to secure system access.

## 2. Key Rotation Procedure

1. Engineers must rotate SSH access keys every 90 calendar days.
2. The platform team invalidates any active key exceeding 90 days of age.
3. Replace expired keys through the identity portal before requesting production access.
```

Why this succeeds:
- Separates rationale into Purpose.
- Operational steps are numbered, imperative, and role-attributed.
- No compliance narration or internal path leaks.
- Uses exact numbers without hedging.

## 2. Deliverable Certainty vs Uncertainty Markers

### Bad (Uncertainty and Internal Leakage)

```markdown
# Project Status Report [DRAFT - PENDING APPROVAL]

The team has made good progress on the platform rewrite as planned in session 2026-09-14-1129. We anticipate delivering the core microservice around mid-October, with an estimated throughput of roughly 10,000 requests per second (provisional figure). Please note this report was generated with AI assistance.
```

Why this fails:
- Contains drafting metadata in title (`[DRAFT - PENDING APPROVAL]`).
- Cites internal session ID (`session 2026-09-14-1129`).
- Uses quantity hedges ("around mid-October", "roughly 10,000 requests").
- Includes uncertainty markers ("provisional figure").
- Contains explicit AI attribution ("generated with AI assistance").

### Good (External Reader Focus and Settled Facts)

```markdown
# Platform Engineering Quarterly Update

The platform core service release is scheduled for October 15. The service architecture supports 10,000 sustained requests per second based on completed load testing against the staging environment.
```

Why this succeeds:
- Written directly for external leadership readers without internal scaffolding.
- States settled commitments and dates without hedging.
- Zero AI attribution and zero internal session leaks.

## 3. Deliverable Boundaries vs Context and Progress Leakage

### Bad (Progress Notes, Disclaimers, Unprompted Details, and Explanations)

```markdown
# Standard Operating Procedure: Procurement [DRAFT - PENDING PROMULGATION]

Disclaimer: This is a template audit report procedure and should not be relied upon without board review.

1. Organizational Context
AYCP is a national PBO established under the PBO Act 18 of 2013, registered under registration number P.O133.3399./2929. We operate under strict donor instructions that prohibit unrestricted funding over 2%.

2. Thresholds
Purchases over 50,000 KES require three quotes. As directed by the user, AYCP will not conduct interventions in Bungoma County. We used our internal costing model to establish the 50,000 KES ceiling. The user will clarify whether direct vendor selection applies to emergencies.
```

Why this fails:
- Places progress markers in the deliverable title ("PENDING PROMULGATION"). Missing prerequisites must be resolved with the user in chat beforehand.
- Includes protective self-disclaimers ("template audit report and should not be relied upon").
- Discloses unprompted registration numbers and sensitive details not requested by the reader task.
- Explains background donor rules ("prohibit unrestricted funding over 2%") and internal methodologies ("internal costing model").
- Narrates user direction ("As directed by the user...") and states what the organization decided not to do ("will not conduct interventions in Bungoma").
- Places unasked questions and task notes inside the deliverable ("The user will clarify whether direct vendor selection applies...").

### Good (Clean, Focused Deliverable Meeting Express Requirements)

```markdown
# Standard Operating Procedure: Procurement

## 1. Purpose

This procedure establishes mandatory purchasing thresholds and competitive quotation requirements for all program operations.

## 2. Procurement Thresholds

1. Purchases up to 50,000 KES require one approved purchase requisition.
2. Purchases exceeding 50,000 KES require three written competitive quotations before purchase order issuance.
3. The finance officer must verify quotation compliance before disbursing funds.
```

Why this succeeds:
- Contains zero progress markers, self-disclaimers, or protective warnings.
- Contains only the operative content required by the document type.
- Omits unprompted registration numbers, internal costing models, and donor constraint explanations.
- Relies on chat for clarifying questions, keeping the deliverable canvas clean and production-ready.

