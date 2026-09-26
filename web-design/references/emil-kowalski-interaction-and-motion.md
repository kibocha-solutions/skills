# Emil Kowalski & Rauno Freiberg Interaction and Motion Standards

This reference specifies the interaction engineering rules, animation timing brackets, spring physics parameters, and micro-interaction details required for high-craft interfaces.

## 1. Frequency-Based Animation Brackets

The perceived quality of an animation depends on how frequently the user encounters it. Frequent actions must be snappy and unobtrusive; infrequent actions can afford more expressive spatial transitions.

### High-Frequency Interactions (100ms to 150ms)
- **Scope**: Buttons, icon toggles, checkboxes, radio buttons, segmented control switches, tab switches.
- **Timing**: 100ms to 140ms.
- **Feel**: Immediate, crisp, responsive.
- **Rule**: Never delay a state change with a long fade or slide. The user needs immediate feedback that their action was registered.

### Medium-Frequency Interactions (150ms to 200ms)
- **Scope**: Dropdown menus, tooltips, popovers, inline notifications, list row deletions, card expansions.
- **Timing**: 150ms to 200ms.
- **Feel**: Smooth, directional, orienting.
- **Rule**: Provide spatial continuity without making the user wait to access secondary controls.

### Low-Frequency Interactions (200ms to 280ms)
- **Scope**: Modal dialogs, full-page sheet drawers, navigation transitions, major layout morphs.
- **Timing**: 200ms to 280ms.
- **Feel**: Grounded, weighted, cinematic.
- **Rule**: Even large dialogs must never exceed 300ms. Lengthy animations break user flow and feel sluggish.

---

## 2. Spring Physics Parameters

Spring physics provide natural deceleration and momentum that standard cubic-beziers cannot replicate.

### Recommended Spring Presets (Framer Motion / React Spring)
- **Snappy Micro-interaction (Buttons / Toggles)**:
  ```javascript
  { type: "spring", stiffness: 400, damping: 30, mass: 0.8 }
  ```
- **Smooth Modal / Drawer Sheet**:
  ```javascript
  { type: "spring", stiffness: 300, damping: 32, mass: 1 }
  ```
- **Bouncy Accent (Deliberate Delight)**:
  ```javascript
  { type: "spring", stiffness: 280, damping: 18, mass: 1 }
  ```

### Pure CSS Spring Approximations
When using standard CSS transitions, use customized easing curves that front-load velocity:
```css
/* Snappy Entrance */
--ease-out-spring: cubic-bezier(0.16, 1, 0.3, 1);

/* Fluid Exit */
--ease-in-spring: cubic-bezier(0.7, 0, 0.84, 0);

/* Gentle Natural Movement */
--ease-natural: cubic-bezier(0.2, 0, 0, 1);
```

---

## 3. Spatial Origin and Invisible Details

### Origin-Aware Transformations
Never scale a dropdown menu or popover from the center of the screen or top-left (0, 0).
1. Set the transform origin relative to the triggering button or pointer location:
   ```css
   /* Menu triggered from top-right button */
   .dropdown-menu {
     transform-origin: top right;
     animation: menu-reveal 150ms var(--ease-out-spring);
   }
   ```
2. When a modal opens from a card, morph or expand from the initial card coordinates rather than fading in from a blank canvas.

### Interruptibility (Rauno Freiberg Standard)
1. Animations must remain interruptible by user gestures or clicks.
2. If a user clicks a button to open a drawer and immediately clicks away, the drawer must immediately reverse course smoothly from its current transform value rather than completing the full opening animation before closing.

### Tactile Touch-Down Feedback
Every clickable or tapable component must respond instantly upon `active` or `pointerdown` state:
```css
.interactive-element {
  transition: transform 100ms var(--ease-out-spring), filter 100ms ease;
}

.interactive-element:active {
  transform: scale(0.98);
  filter: brightness(0.95);
}
```

---

## 4. Reduced Motion Compliance

Always respect user accessibility preferences:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
