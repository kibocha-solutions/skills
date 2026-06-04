# Source And Standards Research

Use this reference before creating or materially revising any production
technical diagram. Research is part of artifact generation, not an optional
rescue step after uncertainty.

## Source Priority

Use these sources together:

1. Local project truth: code, schemas, migrations, models, configs, API
   contracts, forms, architecture notes, deployment files, security docs,
   existing diagrams, and product screenshots.
2. Project conventions: existing diagram style, docs structure, palette,
   notation, terminology, and target platform constraints.
3. Authoritative current sources: standards bodies, official design systems,
   platform documentation, vendor documentation, and reputable domain
   organizations.

Local project truth controls what the diagram says. External standards control
notation quality, accessibility, visual discipline, platform correctness, and
domain convention where they apply.

## When To Search

Search authoritative sources for production artifacts unless the user
explicitly says not to browse or the diagram is a purely local sketch whose
notation and domain are already fully established by repository conventions.

Search when any of these could affect the diagram:

- diagram notation or expected grammar
- accessibility, color, contrast, typography, or layout quality
- current platform behavior or cloud architecture guidance
- security, privacy, compliance, or trust-boundary representation
- database, API, workflow, or domain data conventions
- sector-specific data models, process standards, or regulatory expectations

## Preferred Source Categories

Use reputable sources such as:

- Diagram notation: C4 Model, Object Management Group UML and BPMN material,
  database vendor ERD guidance, and established notation references.
- Accessibility: W3C WCAG and official accessibility guidance from the target
  platform or design system.
- Visual and interaction design: Figma resources, Google Material Design,
  Microsoft Fluent, Apple Human Interface Guidelines, and the target product's
  own design system.
- Platform architecture: official cloud provider docs, database vendor docs,
  framework docs, API provider docs, and security architecture docs.
- Domain standards: recognized standards bodies, official public institutions,
  regulator guidance, sector consortia, and vendor-neutral industry references.

Prefer primary sources over blog posts. Use secondary sources only to discover
primary references or to clarify a practical convention when no primary source
is available.

## Research Output

Before drawing, convert research into a short internal diagram brief:

- diagram type and notation basis
- local entities, systems, actors, states, or flows found in project sources
- authoritative standards or guidance used
- project conventions to preserve
- assumptions or gaps that remain

Do not paste long research notes into the final deliverable. In the final
response, cite or name the external standards that materially shaped the
diagram, especially when they affect notation, accessibility, layout, security,
or domain correctness.

## Guardrails

- Do not invent domain structures if local sources or authoritative standards
  can answer them.
- Do not let generic external standards override project-specific facts.
- Do not use decorative design trends as standards.
- Do not copy diagrams or proprietary examples wholesale.
- Do not rely on stale memory for changing standards, platform behavior, or
  regulatory context.
