---
name: mobile-app-design
description: Design and implement production-grade mobile and tablet application interfaces, touch interactions, gesture navigation, and dual-orientation layouts across iOS, Android, PWA, React Native, and Flutter. Covers phone and tablet ergonomics in both portrait and landscape orientations, Apple HIG and Material 3 Expressive standards, safe area insets, thumb zone architecture, master-detail views, pull-to-refresh, bottom sheets, and tactile touch-down states. Use for mobile app design, tablet UI, touch interfaces, gesture navigation, mobile ergonomics, iOS design, Android design, React Native styling, and Flutter layouts.
license: Complete terms in LICENSE.txt
---

# Mobile and Tablet App Design

## 1. Establish the device target and orientation

1. Identify the operating environment and framework:
   - iOS native (SwiftUI/UIKit), Android native (Jetpack Compose), cross-platform (React Native, Flutter), or mobile web PWA.
2. Identify the target hardware forms:
   - Mobile phones (compact 4.7-inch to large 6.9-inch screens).
   - Tablets (7.9-inch mini to 13-inch pro displays).
3. Support both device orientations:
   - **Portrait**: One-handed thumb reach, bottom navigation, vertical scroll stacks.
   - **Landscape**: Horizontal split panes, compact side rails, minimized vertical headers.
4. Ingest the project `DESIGN.md` contract. If absent, invoke `interface-design` to establish tokens, archetypes, and platform foundation.

## 2. Enforce touch targets and safe area insets

Read [mobile and tablet ergonomics](references/mobile-and-tablet-ergonomics.md) for reachability zones, inset handling, and master-detail patterns.

1. Implement platform-specific minimum touch hit areas:
   - Apple iOS / iPadOS: minimum 44x44pt hit target.
   - Google Android / Material 3: minimum 48x48dp hit target.
2. Expand visual icons smaller than 44pt to minimum touch boundaries using negative margins, padding, or pseudo-elements (`::after` hit area).
3. Provide minimum 8px spacing between adjacent touch targets to eliminate mis-taps.
4. Bind layouts to device hardware cutouts and home indicators using safe area insets:
   ```css
   padding-top: env(safe-area-inset-top, 0px);
   padding-bottom: env(safe-area-inset-bottom, 0px);
   padding-left: env(safe-area-inset-left, 0px);
   padding-right: env(safe-area-inset-right, 0px);
   ```

## 3. Implement phone portrait ergonomics

1. Anchor primary navigation and primary calls to action in the natural thumb zone (lower 40% of the viewport).
2. Use sticky bottom navigation bars (3 to 5 destinations) or persistent bottom action buttons.
3. Position search fields and filter triggers within thumb reach or implement pull-down reveals.
4. Replace centered modal popups with expandable bottom sheets. Support velocity-based drag dismissal.
5. Prevent keyboard obstruction: scroll active inputs into view above the virtual software keyboard.

## 4. Implement phone landscape ergonomics

1. Handle severe vertical height constraints (typically under 450px):
   - Collapse or hide decorative hero headers.
   - Replace top and bottom app bars with a compact left-side navigation rail.
   - Pair form fields horizontally (e.g. First Name and Last Name side by side) rather than stacking vertically.
2. Apply lateral safe area insets (`env(safe-area-inset-left)` and `env(safe-area-inset-right)`) to prevent notch or dynamic island clipping.

## 5. Implement tablet ergonomics across orientations

1. **Tablet Portrait**:
   - Implement a 2-column adaptive layout.
   - Limit text reading columns to 65 to 75 characters; never stretch plain body text across the full tablet width.
   - Anchor primary touch buttons along lateral edges where thumbs rest when holding the device with two hands.
2. **Tablet Landscape**:
   - Implement a desktop-class master-detail dual-pane architecture:
     - Left pane (320px to 380px): Persistent navigation rail and searchable list items.
     - Right pane (flexible remaining width): Detailed item view, contextual actions, and telemetry.
   - Support simultaneous input modalities: large touch targets for finger interaction, and subtle hover/active states for connected trackpads, mice, and stylus pointers.

## 6. Implement gesture physics and tactile feedback

Inspect [touch and mobile gestures](examples/touch-and-mobile-gestures.md) for pull-to-refresh, bottom sheets, and swipeable list items.

1. Implement snappy tactile touch-down feedback on every tapable element:
   ```css
   .touch-control:active {
     transform: scale(0.97);
     transition: transform 80ms ease-out;
   }
   ```
2. Disable text selection and mobile callout bubbles on interactive touch surfaces:
   ```css
   user-select: none;
   -webkit-touch-callout: none;
   ```
3. Implement velocity-aware sheet drag gestures:
   - If drag velocity exceeds threshold, complete the dismissal or expansion.
   - If released below threshold, snap back to nearest detent (half-height or full-height) using spring physics (`stiffness: 300, damping: 30`).
4. Implement pull-to-refresh with clear resistance curves and haptic feedback triggers.

## 7. Pre-completion checklist

Before delivering mobile or tablet application designs, confirm evidence exists for each item:

- [ ] Touch targets verified: minimum 44x44pt (iOS) or 48x48dp (Android).
- [ ] Safe area insets (`env(safe-area-inset-*)`) handled on all edges.
- [ ] Phone portrait layout keeps primary actions in the lower thumb zone.
- [ ] Phone landscape layout handles vertical height constraints (<450px) without clipped controls.
- [ ] Tablet portrait layout restricts line lengths (<75ch) and supports lateral thumb grips.
- [ ] Tablet landscape layout implements master-detail dual-pane architecture.
- [ ] Active touch-down scale feedback (`active:scale-[0.97]`) verified on controls.
- [ ] Gesture dismissals (sheets, cards) support velocity-based spring snapping.
- [ ] Zero AI attribution across code, styles, comments, and documentation.
- [ ] No U+2014 em dashes in any file or deliverable.
