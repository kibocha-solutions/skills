# Frontend Design: Design Tokens and Accessibility

## 1. Cohesive Design Tokens

A design system must derive its identity from functional purpose rather than ungrounded trends.

### Token Scales

1. **Color Roles**:
   - `surface`: Background and container colors (`surface-primary`, `surface-secondary`, `surface-elevated`).
   - `content`: Text and icon hierarchy (`content-primary`, `content-secondary`, `content-muted`).
   - `accent`: Primary action and interactive focus (`accent-default`, `accent-hover`, `accent-subtle`).
   - `feedback`: Error, warning, success, info states.

2. **Typography**:
   - Limit font families to one primary sans/serif and one optional code/display face.
   - Use modular line-height (minimum 1.5 for body text).
   - Set max line length to 65-75 characters (`max-w-prose` or `68ch`) for readability.

3. **Spacing and Geometry**:
   - Use a consistent 4px or 8px baseline grid (4, 8, 12, 16, 24, 32, 48, 64px).
   - Coordinate border radius: small elements (badges, buttons: 4-6px), containers (cards: 8-12px).

## 2. Accessibility (a11y) Standards

1. **Contrast**:
   - Normal text: WCAG AA minimum 4.5:1 ratio against background.
   - Large text (>=18pt or >=14pt bold): Minimum 3:1 ratio.
   - Interactive borders and icons: Minimum 3:1 contrast against adjacent surface.

2. **Keyboard Navigation**:
   - All interactive controls must be focusable via `Tab`.
   - Never suppress `outline: none` without providing an explicit, high-contrast `:focus-visible` indicator.
   - Logical DOM focus order must match visual reading order.

3. **Reduced Motion**:
   - Wrap animations in `@media (prefers-reduced-motion: reduce)`.
   - Ensure interface functions completely when animations are disabled.
