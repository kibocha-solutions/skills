# Diagram Type Routing

## Procedure

1. Identify the question the diagram must answer.
2. Select one primary type from the table.
3. Use a second type only when one canvas cannot answer the question clearly.
4. Record the selected type and reading direction.
5. Apply the required elements.
6. Remove elements that do not answer the selected question.

| Question | Type | Required elements |
|---|---|---|
| Who interacts with the system? | System context | People, external systems, system boundary, relationships |
| What runs or stores data? | Container | Applications, services, stores, external dependencies |
| What modules form one container? | Component | Components, responsibilities, internal dependencies |
| Where does software run? | Deployment | Nodes, environments, artifacts, network boundaries |
| What happens over time? | Sequence | Participants, ordered messages, conditions |
| What steps and decisions occur? | Activity or workflow | Actions, decisions, branches, start, end |
| How does an entity change? | State | States, transitions, guards, terminal states |
| How is data structured? | ERD | Entities, keys, relationships, cardinality |
| Where does data move? | Data-flow | Processes, stores, actors, labeled flows |
| Where are trust risks? | Threat model | Trust boundaries, assets, entry points, threats, controls |
| Who may do what? | Permission or authorization | Subjects, resources, actions, conditions, denials |
| How are networks connected? | Network or infrastructure | Zones, nodes, protocols, boundaries, routes |

## Reading direction

- Use left to right for flows and dependencies.
- Use top to bottom for hierarchies and lifecycle progressions.
- Use chronological order for sequence diagrams.
- Keep exceptions and feedback paths visually subordinate.
