# Writerside Technical Documentation

Use this reference when creating or revising technical documentation for
software, systems, APIs, infrastructure, operations, security, databases,
testing, configuration, or developer/user technical guides.

## Sources

Primary source material:

- JetBrains Writerside: topics, markup, instances, table of contents, API
  documentation, generated API reference, code blocks, tabs, admonitions,
  variables, content reuse, Mermaid, PlantUML, build and publish.

## Contents

- Core Rule
- Project Shape
- Topics
- Navigation
- Markdown and Semantic Markup
- Procedures
- Admonitions
- Tabs and Variants
- Code Blocks
- API Documentation
- Diagrams and Images
- Reuse and Variables
- Access and Sensitivity
- Validation
- Official References

## Core Rule

All new technical documentation artifacts use Writerside-compatible Markdown.
Use migrated references for content requirements when they exist. Use this
reference for output structure, markup, navigation, and maintainability.

Do not generate other documentation formats or their configuration files for
technical documentation unless the user explicitly asks for a separate migration
or compatibility task.

## Project Shape

When creating a Writerside documentation set from scratch, use this shape unless
the repository already has a Writerside structure:

```text
docs/
`-- writerside/
    |-- writerside.cfg
    |-- topics/
    |   |-- index.md
    |   `-- ...
    |-- images/
    |   `-- ...
    `-- <instance>.tree
```

Use one instance for one coherent help output. Add another instance only when
the same source project must publish a separate audience, product, edition, or
output.

## Topics

A topic is one published page. Keep each topic focused on one reader task or
one stable reference subject.

Use Markdown topic files (`.md`) by default. Add Writerside semantic markup
inside Markdown when Markdown alone loses meaning or maintainability.

Split a topic when:

- the page covers more than one reader task
- the in-page navigation becomes noisy
- one section needs a different access level
- a reusable reference would be easier to maintain as its own topic
- the topic mixes concept, procedure, reference, and troubleshooting in a way
  that slows the reader

Keep a topic together when the reader must complete the sections in one sitting
or when splitting would force constant cross-navigation.

## Navigation

Every published topic must be reachable from the Writerside tree.

Use the tree file to define the help instance, home page, topic order, and
topic hierarchy. Group topics by reader workflow, not by internal team
ownership.

Prefer this navigation order for technical docs:

1. Overview or entry point
2. Prerequisites or concepts needed before action
3. Task procedures
4. Reference pages
5. Troubleshooting
6. Release, migration, or compatibility notes

Use empty groups in the tree only for navigation grouping. Do not create empty
topics just to create a section.

## Markdown and Semantic Markup

Use plain Markdown for:

- headings
- short paragraphs
- simple lists
- simple tables
- links
- ordinary code fences

Use Writerside semantic markup when it adds meaning, validation, reuse, or
better rendering:

- `<procedure>` and `<step>` for ordered tasks
- `<tabs>` and `<tab>` for platform, language, role, or scenario variants
- `<note>`, `<tip>`, and `<warning>` for contextual callouts
- `<control>` for UI controls
- `<code-block>` when code needs Writerside attributes such as `src`,
  `ignore-vars`, or precise language handling
- `<include>`, `<snippet>`, and variables for reused content
- `<api-doc>` only when the user explicitly asks to integrate an existing API
  contract into Writerside output

Do not use bold text as a substitute for semantic UI-control markup when the
same control wording will recur across many topics.

## Procedures

Use procedures for tasks the reader performs.

A procedure must include:

- the outcome the reader should achieve
- prerequisites that change execution
- ordered steps with one action per step
- exact commands, paths, field names, or UI controls
- expected result or verification step
- recovery or rollback where failure is plausible

Do not mix conceptual explanation into the step list. Put context before the
procedure or link to a concept topic.

## Admonitions

Use admonitions sparingly:

- `tip`: optional shortcut or alternative
- `note`: important context, limitation, or compatibility detail
- `warning`: action can cause loss, outage, security exposure, corruption, or
  irreversible change

Do not use admonitions for emphasis, decoration, or material that belongs in the
main flow.

## Tabs and Variants

Use tabs when the same task has parallel variants:

- operating systems
- programming languages
- package managers
- deployment environments
- user roles

Keep tab sets symmetrical. If one tab needs substantially more content, split it
into its own topic.

Synchronize repeated tab groups only when the same choice should apply across
the page.

## Code Blocks

Every code block must serve a reader action or verification need.

Include:

- language identifier
- full command or minimal runnable example
- surrounding context when a command depends on directory, shell, environment,
  or credentials
- expected output when the reader needs confirmation

Use `ignore-vars="true"` where percent-sign content, shell variables, URLs, or
template syntax could be mistaken for Writerside variables.

For long examples, reference source files instead of duplicating code in many
topics.

## API Documentation

For this skill, API documentation is Writerside documentation.

Write API docs as topics that explain:

- API purpose and scope
- authentication and authorization
- endpoints, methods, paths, request fields, response fields, and status codes
- rate limits, quotas, retries, idempotency, and timeouts
- error model and remediation
- versioning and deprecation
- examples that a reader can run

If an API contract already exists and the user asks to integrate it, use
Writerside API-reference support from a topic. Add manual documentation for
authentication and any unsupported contract details.

Do not create separate contract files during a documentation-drafting task
unless the user explicitly asks for contract generation.

## Diagrams and Images

Use diagrams when structure or flow is easier to inspect visually than in prose:

- system context
- component relationships
- sequence flows
- state transitions
- deployment topology
- data flow

Use Mermaid for lightweight diagrams that should live near the topic source.
Use PlantUML when UML structure or richer modeling is needed. Keep generated or
source diagram files in a predictable location.

Every image or diagram needs useful alternative text and a nearby explanation
of what the reader should notice.

## Reuse and Variables

Use reuse only when it reduces maintenance risk.

Good candidates:

- repeated warnings
- shared prerequisites
- product names, version numbers, support contacts
- repeated procedure fragments
- common troubleshooting notes

Prefer dedicated reusable snippet libraries for content that appears across
many topics. Use variables for values that must remain consistent.

Do not introduce reuse for one-off text. It makes editing harder without
reducing drift.

## Access and Sensitivity

Classify technical documentation when sensitivity affects storage or audience:

- Public: end-user guides, public integration docs, public changelog
- Internal: architecture, deployment, internal APIs, database, configuration,
  testing, operations
- Restricted: threat models, vulnerability details, incident records
- Confidential: executive strategy, protected IP, financial or customer
  contract material

Add access notices only when they change handling behavior. Do not decorate
every page with a banner if the repository access already makes the audience
obvious.

## Validation

Before handing off Writerside technical documentation:

- confirm each topic has one subject
- confirm each published topic appears in the tree
- confirm links point to real topics, headings, files, or external URLs
- confirm procedures have prerequisites and verification steps
- confirm commands, paths, endpoint names, parameters, and versions are exact
- confirm code blocks declare the language and do not rely on hidden context
- confirm warnings identify concrete consequences
- confirm reused content has stable IDs
- confirm the artifact contains no legacy format paths or markup
- run Writerside preview or build when the project tooling is available

If Writerside tooling is unavailable, state that validation was limited to
source review.

## Official References

- https://www.jetbrains.com/help/writerside/topics.html
- https://www.jetbrains.com/help/writerside/markup-reference.html
- https://www.jetbrains.com/help/writerside/instances.html
- https://www.jetbrains.com/help/writerside/table-of-contents.html
- https://www.jetbrains.com/help/writerside/api-documentation.html
- https://www.jetbrains.com/help/writerside/generate-api-reference.html
- https://www.jetbrains.com/help/writerside/code.html
- https://www.jetbrains.com/help/writerside/tabs.html
- https://www.jetbrains.com/help/writerside/admonitions.html
- https://www.jetbrains.com/help/writerside/variables.html
- https://www.jetbrains.com/help/writerside/reuse-pieces-of-content.html
- https://www.jetbrains.com/help/writerside/mermaid-diagrams.html
- https://www.jetbrains.com/help/writerside/plantuml-diagrams.html
- https://www.jetbrains.com/help/writerside/build-and-publish.html
