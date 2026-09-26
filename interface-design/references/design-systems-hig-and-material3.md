# Design Systems: Apple HIG and Google Material 3 Expressive

This reference provides the authoritative standards, component anatomy, official documentation directories, and selection matrices for Apple Human Interface Guidelines and Google Material 3 Expressive.

## 1. Official Documentation Directory

When designing or implementing a specific component, read the official design guidelines directly from the authoritative URLs below:

### Apple Human Interface Guidelines (HIG)
- Main Portal: `https://developer.apple.com/design/human-interface-guidelines`
- Layout & Foundations: `https://developer.apple.com/design/human-interface-guidelines/layout`
- Typography: `https://developer.apple.com/design/human-interface-guidelines/typography`
- Color & Materials: `https://developer.apple.com/design/human-interface-guidelines/materials`
- Component Specifications:
  - Buttons: `https://developer.apple.com/design/human-interface-guidelines/buttons`
  - Sheets: `https://developer.apple.com/design/human-interface-guidelines/sheets`
  - Navigation Bars: `https://developer.apple.com/design/human-interface-guidelines/navigation-bars`
  - Tab Bars: `https://developer.apple.com/design/human-interface-guidelines/tab-bars`
  - Lists and Tables: `https://developer.apple.com/design/human-interface-guidelines/lists-and-tables`
  - Segmented Controls: `https://developer.apple.com/design/human-interface-guidelines/segmented-controls`

### Google Material 3 Expressive
- Main Portal: `https://m3.material.io`
- Foundations (Color, Shape, Motion): `https://m3.material.io/foundations`
- Motion & Spring Physics: `https://m3.material.io/styles/motion/overview`
- Component Specifications:
  - Buttons & FABs: `https://m3.material.io/components/buttons/overview`
  - Navigation Bars & Rails: `https://m3.material.io/components/navigation-bar/overview`
  - Bottom Sheets: `https://m3.material.io/components/bottom-sheets/overview`
  - Cards: `https://m3.material.io/components/cards/overview`
  - Dialogs: `https://m3.material.io/components/dialogs/overview`
  - Text Fields: `https://m3.material.io/components/text-fields/overview`

---

## 2. Platform Comparison and Standards

| Feature | Apple HIG (iOS / iPadOS) | Google Material 3 Expressive (Android) |
|---|---|---|
| **Touch Target Minimum** | 44x44pt | 48x48dp |
| **Primary Typography** | San Francisco (SF Pro / SF Compact) | Roboto / Dynamic Product Sans |
| **Type Scale** | Large Title (34pt), Title 1 (28pt), Title 2 (22pt), Title 3 (20pt), Headline (17pt semi), Body (17pt), Callout (16pt), Subhead (15pt), Footnote (13pt), Caption 1 (12pt), Caption 2 (11pt) | Display (Large, Med, Small), Headline (Large, Med, Small), Title (Large, Med, Small), Body (Large, Med, Small), Label (Large, Med, Small) |
| **Elevation & Depth** | Vibrancy, materials (translucency + background blur), subtle drop shadows | Tonal color surface shifts, shadow elevation (0 to 5dp), shape morphing |
| **Corner Radii** | Squircle (continuous curvature): 8px to 16px for controls, 24px to 40px for sheets | 35+ expressive shape corners, full pills (9999px), asymmetrical rounded corners |
| **Primary Navigation** | Bottom tab bar (3 to 5 destinations), top navigation bar with back chevron | Bottom navigation bar, navigation rail (tablet/desktop), top app bar |
| **Prominent Action** | Right navigation bar item, bottom-pinned CTA button | Floating Action Button (FAB), extended FAB, tonal filled button |
| **Sheet Behavior** | Detents (medium, large), background view scales down slightly | Modal bottom sheet, standard bottom sheet, drag handle, scrim |

---

## 3. Platform Selection and Synthesis Decision Matrix

Use this matrix to select the foundation based on target product and audience:

### Native iOS / iPadOS Target
1. Follow Apple HIG strictly.
2. Use SF Pro system font with optical weights and tabular figures for numbers.
3. Apply translucent materials (`backdrop-filter: blur(20px)`) to navigation bars and tab bars.
4. Support standard iOS navigation gestures: swipe-from-left edge to navigate back, pull-down to dismiss modal sheets.
5. Enforce 44x44pt minimum touch hit areas.

### Native Android Target
1. Follow Google Material 3 Expressive strictly.
2. Implement dynamic tonal palettes (`primary`, `on-primary`, `primary-container`, `on-primary-container`, `surface`, `surface-container-high`).
3. Use spring-driven container transforms for cards expanding into full detail views.
4. Use expressive asymmetric shapes and rounded corner tokens.
5. Enforce 48x48dp minimum touch hit areas.

### Cross-Platform Web / SaaS Synthesis
When building responsive web applications or hybrid cross-platform apps:
1. **Typography**: Adopt Apple's typographic restraint. Restrict to one crisp sans-serif (e.g. Inter, SF Pro, Geist) and one optional code/mono face. Keep line lengths strictly between 65 and 75 characters.
2. **Color & Containers**: Adopt Material 3's semantic container hierarchy (`surface-primary`, `surface-secondary`, `surface-elevated`). Use background color shifts rather than heavy drop shadows to denote layering.
3. **Touch Targets**: Apply the stricter 48x48px target size for mobile viewports, relaxing to 36x36px for pointer/mouse controls on desktop.
4. **Motion**: Use Emil Kowalski spring curves (`stiffness: 300, damping: 30`) and snappy durations (100 to 150ms for buttons, 150 to 200ms for menus).
