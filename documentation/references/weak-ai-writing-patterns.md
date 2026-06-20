# Weak AI-Writing Patterns

Use this reference when reviewing or rewriting documentation for weak
AI-patterned writing. These patterns are quality risks due for improvement.

## Specificity

Watch for inflated significance claims:

- `testament`
- `pivotal`
- `crucial`
- `vital`
- `underscores`
- `broader landscape`
- `enduring legacy`
- `key role`
- `significant shift`
- `plays a role`
- `contributes to`

Replace them with the concrete fact, source-backed consequence, or explicit
unknown.

## Neutrality

Watch for promotional or press-release phrasing:

- `boasts`
- `vibrant`
- `rich`
- `profound`
- `groundbreaking`
- `renowned`
- `showcasing`
- `commitment to`
- `nestled`
- `in the heart of`
- `diverse array`

Use plain descriptions. Attribute evaluative claims or remove them.

## Unsupported Analysis

Watch for trailing interpretation that does not come from the source:

- `highlighting`
- `underscoring`
- `reflecting`
- `symbolizing`
- `fostering`
- `cultivating`
- `aligning with`
- `resonating with`
- `offering valuable insights`

Keep the fact if it is useful. Remove the interpretation unless it is
source-backed and useful for the reader.

## Negative Parallelism

Eradicate the diminish-to-elevate rhetorical move in all its forms. The
forbidden pattern is not a specific phrase — it is any construction that
elevates Y by first diminishing X. Paraphrasing the surface words while
preserving the move is not compliance.

Forbidden forms include but are not limited to:

- `not just X, but Y`
- `not X. Y.`
- `not just X. This is Y.`
- `Y, rather than X`
- `Y, not just X`
- `not only X, but also Y`
- `more than X` / `more than just X`
- `went beyond X`
- `exceeded mere X`
- `was not limited to X`
- `not merely X`
- `X was secondary to Y`

**Paraphrase loophole example:**

Original:

```text
This was not just an alignment concern. All aspects of the structure appeared
null if not nullable.
```

Malicious compliance (still a failure — the move survived under different words):

```text
This was more than alignment concerns. All aspects of the structure appeared
null if not nullable.
```

Compliant — remove the contrast frame, state the important point directly:

```text
All aspects of the structure appeared null if not nullable. [...paragraph...]
Alignment concerns could not cure this document.
```

Use direct positive phrasing. The only exception is when the contrast itself
is the factual point — when the distinction between X and Y is the
information, not a rhetorical device for emphasis.

## Vague Attribution

Replace vague authority with named, checkable sources. Watch for:

- `experts argue`
- `observers note`
- `industry reports`
- `critics say`
- `several sources`
- `media outlets`
- `independent coverage`
- `active social media presence`

Do not imply broad agreement from one or two sources.

## Formulaic Structure

Remove formulaic scaffolding unless it genuinely helps the reader:

- title-case headings in ordinary docs
- `Challenges and Future Outlook` sections that speculate
- conclusion sections that merely restate the document
- inline-header lists where prose or a table would be clearer
- unnecessary small tables
- decorative emoji
- excessive boldface
- thematic breaks before headings
- repeated rule-of-three phrasing

## Fourth-Wall Drift

Avoid purposeless medium references:

- `This report analyzes...`
- `This document outlines...`
- `This section discusses...`
- `The purpose of this guide is...`

Name the subject directly:

- `The problem exposes...`
- `The deployment failed because...`
- `The experiment measured...`
- `The migration requires...`

Allowed fourth-wall references are limited to useful cross-references,
structural labels, and explicit user requests to describe document structure.

## Em Dash Character

Avoid the U+2014 dash in normal prose. Allowed uses are limited to:

- quoted source text where punctuation must be preserved
- legal or policy-style lists where the dash introduces enumerated exceptions,
  conditions, or clauses
- headings where the relevant style guide authorizes the form, such as
  `Article 1 --- Doctrine of X`
- existing titles, labels, statute names, or formal names that include the
  character

If none of those conditions applies, remove the em dash.

## Markup and Residue

Search for copied chatbot or citation artifacts:

- `as an AI language model`
- `as of my last knowledge update`
- `I hope this helps`
- `Would you like`
- `Of course`
- `Certainly`
- `[insert ...]`
- `[describe ...]`
- `PASTE_`
- `INSERT_`
- `URL`
- `2025-XX-XX`
- `TODO` placeholders left as content
- `turn0search`
- `turn0image`
- `contentReference`
- `oaicite`
- `oai_citation`
- `attached_file`
- `grok_card`
- `attributableIndex`
- `utm_source=chatgpt.com`
- `utm_source=openai`
- `utm_source=copilot.com`
- `referrer=grok.com`

Also check for malformed Markdown, mixed markup dialects, broken links, unused
references, invalid DOI or ISBN values, and citations that do not verify the
prose.
