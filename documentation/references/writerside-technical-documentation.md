# Writerside Technical Documentation

Use this reference when creating or revising technical documentation for
software, systems, APIs, infrastructure, operations, security, databases,
testing, configuration, or developer/user technical guides.

## Sources

Primary source material:

- JetBrains Writerside: topics, markup, instances, table of contents, API
  documentation, generated API reference, code blocks, tabs, admonitions,
  variables, content reuse, images, build and publish.

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
|-- writerside.cfg
|-- public.tree
|-- internal.tree
|-- restricted.tree
|-- confidential.tree
|-- cfg/
|-- snippets/
|-- topics/
|   |-- product/
|   |-- planning/
|   |-- architecture/
|   |-- domain/
|   |-- data/
|   |-- security/
|   |-- api/
|   |-- engineering/
|   |-- testing/
|   |-- operations/
|   |-- user-guides/
|   `-- releases/
`-- diagrams/
```

Use one instance for one coherent help output. The default audience instances
are Public, Internal, Restricted, and Confidential. Add or rename instances only
when the repository already has a compatible convention or the same source
project must publish a separate product, edition, audience, or output.

Do not create a shared-library tree as a default output. Writerside has two
separate reuse mechanisms:

- snippet library topics for reusable content fragments, such as repeated
  warnings, notes, prerequisites, and standard wording
- TOC library tree files for reusable navigation chunks made of `toc-element`
  entries

Create a TOC library tree only when multiple output trees need the same
navigation section. Mark the library tree as non-output library content and
include its sections from normal instance trees.

Keep audience names in tree files, not source folders. Source folders should be
semantic volumes under the configured topics directory, such as
`topics/architecture/`, `topics/domain/`, `topics/data/`, `topics/security/`,
and `topics/operations/`, so topics can be reused across instances.

Writerside tree `topic` and `start-page` attributes use flat topic filenames,
not filesystem-relative paths. If the file is
`topics/security/security-baseline.md`, reference it as
`topic="security-baseline.md"` and `start-page="security-baseline.md"`, not
`topic="security/security-baseline.md"`. Keep topic basenames unique across the
whole help module.

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

Reference topics by basename only in tree files:

```xml
<instance-profile id="restricted" name="Restricted" start-page="security-baseline.md">
    <toc-element toc-title="Security">
        <toc-element topic="security-baseline.md"/>
        <toc-element topic="permission-tenant-isolation.md"/>
    </toc-element>
</instance-profile>
```

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
- ordinary code fences

Prefer Writerside XML or semantic markup for inserted components, cross-topic
references, and reusable structures. Use XML-style markup even when Markdown
would render, because Writerside can validate and refactor these elements more
reliably.

- `<a href="topic-file.md">Label</a>` for cross-topic links when custom link
  text adds context
- `<a href="topic-file.md"/>` when the link text would match the target topic
  title
- `<img src="path/to/image.svg" alt="..."/>` for images
- `<table>`, `<tr>`, `<th>`, and `<td>` for tables
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

Do not create separate contract files during a documentation task
unless the user explicitly asks for contract generation.

## Diagrams and Images

Use diagrams when structure or flow is easier to inspect visually than in prose:

- system context
- component relationships
- sequence flows
- state transitions
- deployment topology
- data flow

Use the `technical-diagrams` skill for production technical diagrams, including
architecture visuals, workflow diagrams, Draw.io sources, diagram palettes,
render inspection, and SVG exports. Keep editable `.drawio` sources and final
SVG exports in predictable locations. Reference the final SVG from Writerside
topics; do not embed temporary QA PNGs or source files as the visible image.

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
many topics. A snippet library is a topic file with `is-library: true`; keep it
out of published instance trees and manage it through the Writerside Snippets
node. Use variables for values that must remain consistent.

Use TOC library trees only for reusable groups of tree entries. A TOC library
tree is not a place for reusable prose and should not produce a help output.

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
- confirm the topic is previewed in an instance that includes it; do not add
  internal, restricted, or confidential topics to a lower-sensitivity instance
  only to clear a preview warning
- if a topic links to another local topic, include the target in the same
  instance when the target content is safe for that audience; otherwise replace
  the link with plain text or create a separate sanitized topic with a unique
  filename
- confirm tree `topic` and `start-page` attributes use basename-only topic
  filenames
- confirm no two topic files share the same basename
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
- https://www.jetbrains.com/help/writerside/build-and-publish.html
