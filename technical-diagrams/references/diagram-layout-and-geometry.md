# Diagram Layout And Geometry

Use this reference to place diagram elements and evaluate rendered geometry.

## Defaults

Use project geometry assets first. If none exist, use
`assets/default-geometry.json`.

Baseline defaults:

- page margin: 48 px minimum
- component spacing: 72 px minimum
- preferred component spacing: 120 px
- container padding: 32 px minimum
- edge stroke width: 2 px minimum
- edge label offset: 8 to 16 px
- edge label padding: 4 to 8 px
- line crossing: forbidden unless unavoidable and explained
- boundary collision: forbidden

## Layout Rules

- Align related nodes into rows, columns, lanes, zones, or clusters.
- Keep spacing consistent inside a semantic group.
- Use larger containers for boundaries, not decorative frames.
- Keep labels close to the edge or object they describe.
- Give long labels more width instead of shrinking text below readability.
- Keep page bounds generous enough for export and documentation embedding.

## Diagram-Specific Geometry

- C4 context: center the system of interest, place users and external systems
  around it, and label relationships.
- C4 container: use a system boundary and group containers by runtime or
  responsibility.
- Deployment: use zones, environments, networks, or regions as layout anchors.
- Sequence: keep participants aligned horizontally and time flowing downward.
- Activity: keep the main path readable; allow branches to spread sideways.
- Data flow: place trust boundaries visibly and keep data labels traceable.
- ERD: align entities into dependency clusters and keep cardinality labels near
  relationship ends.
- Permission: separate principals, roles/scopes, and resources into readable
  layers or zones.

## Geometry QA

Before delivery, inspect the rendered image for:

- page margins
- node overlap
- label overlap
- edge crossings
- invalid edge termination
- cramped groups
- clipped text
- unreadable density
- unintended visual hierarchy
