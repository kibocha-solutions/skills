# Diagram Type Routing

Use this reference before creating or revising a technical diagram. Identify
the diagram type first; the type controls layout grammar, expected components,
edge labels, directionality, and validation.

## Routing Table

| Request | Diagram type | Grammar to preserve |
| --- | --- | --- |
| External users, systems, integrations, top-level responsibilities | C4 system context | People, software systems, external systems, clear relationship labels |
| Applications, services, data stores, queues inside one system | C4 container | System boundary, containers, data stores, protocols, responsibilities |
| Internal modules inside one service or container | Component | Components, interfaces, dependencies, ownership boundaries |
| Runtime infrastructure, regions, environments, nodes | Deployment | Environments, zones, compute nodes, networks, deployed artifacts |
| Time-ordered interactions between participants | Sequence | Participants across the top, time flowing downward, ordered messages |
| Workflow with branches, joins, start, and end | Activity or workflow | Actions, decisions, parallel branches, terminal states |
| Data movement, stores, actors, trust boundaries | Data flow | Processes, stores, external actors, data labels, trust boundaries |
| States and transitions | State | States, events, guards, terminal states, readable transition direction |
| Tables, entities, keys, cardinality | ERD | Entities, keys, relationship cardinality, constraints |
| Security threats and controls | Threat model | Assets, actors, data flows, trust boundaries, threats, controls |
| Users, roles, scopes, resources, inheritance | Permission | Principals, roles, scopes, resources, authorization boundaries |
| Subnets, devices, routes, services | Network or infrastructure | Topology, zones, addresses when relevant, connection meaning |

## Selection Rules

- Use C4 diagrams for software architecture at different zoom levels.
- Use deployment diagrams for where software runs, not what code depends on.
- Use data flow diagrams for how information moves across processes and trust
  boundaries.
- Use sequence diagrams only when temporal order matters.
- Use state diagrams only when lifecycle states and transitions are the main
  subject.
- Use permission diagrams when the question is who can access what, through
  which role, scope, or policy.

## Directionality

- Architecture and topology diagrams may use two-dimensional layout when it
  clarifies responsibility or dependency.
- Sequence diagrams must preserve temporal order and avoid arbitrary spatial
  routing.
- Activity diagrams may flow top-to-bottom or left-to-right; branches may spread
  sideways.
- State diagrams may group related states, but transition direction must remain
  readable.
- Data flow diagrams may route in multiple directions, but every data movement
  must remain visually traceable.

## When To Research

Use repository conventions and local facts first, then complement them with
authoritative current sources. Read `source-and-standards-research.md` before
drafting a production artifact. Research is especially important when diagram
notation, accessibility, visual design, platform behavior, regulatory context,
or domain conventions could change the artifact.
