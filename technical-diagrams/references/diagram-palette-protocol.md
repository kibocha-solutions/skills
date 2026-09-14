# Diagram Palette Protocol

## Procedure

1. Inspect existing project diagrams and style assets.
2. Record the established background, text, border, fill, accent, warning, and muted colors.
3. Reuse project tokens without alteration.
4. Use bundled defaults only when no project palette exists.
5. Assign color by semantic role.
6. Apply the same role-to-color mapping throughout the diagram.
7. Check contrast on every label, node, boundary, and connector.
8. Verify the rendered export, not only the source values.

## Semantic roles

| Role | Use |
|---|---|
| Background | Canvas and empty space |
| Surface | Standard nodes and containers |
| Primary | Main system, primary path, or selected focus |
| Secondary | Supporting system or secondary path |
| Boundary | Trust, ownership, network, or system boundary |
| Warning | Risk, exception, or degraded state |
| Critical | Prohibited, failed, or severe state |
| Muted | Notes, metadata, and secondary labels |

## Constraints

- Do not use color as the only carrier of meaning.
- Pair warning and critical colors with text, shape, or line treatment.
- Limit accents to established semantic roles.
- Keep decorative gradients, shadows, and textures out unless the project system requires them.
- Preserve monochrome legibility.
