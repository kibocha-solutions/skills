# Mobile and Tablet Ergonomics: Touch, Safe Areas, and Orientations

This reference defines ergonomic geometry, reachability zones, hardware inset handling, and dual-orientation layout patterns for mobile phone and tablet applications.

## 1. Touch Targets and Hit Area Standards

Touch interaction lacks the precision of a pixel-perfect mouse cursor. Users tap with thumb pads and finger surfaces covering 7mm to 10mm of physical glass.

### Platform Target Dimensions
- **Apple iOS / iPadOS**: Minimum 44x44pt (points).
- **Google Android (Material 3)**: Minimum 48x48dp (density-independent pixels).
- **Inter-Element Spacing**: Minimum 8px spacing between adjacent interactive touch boundaries to prevent accidental activation.

### Hit Area Expansion
When an icon is visually smaller than 44pt (e.g. a 20x20px close or chevron icon), expand its touch target using pseudo-elements or negative margins:

```css
.icon-button {
  position: relative;
  width: 24px;
  height: 24px;
}

/* 44x44px expanded hit area */
.icon-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 44px;
  height: 44px;
  transform: translate(-50%, -50%);
}
```

---

## 2. Phone Portrait Ergonomics and Thumb Zones

When holding a phone with one hand, user reachability divides into three distinct zones:

```text
+-----------------------+
|  Top Status & Title   |  <- DIFFICULT ZONE (Re-orient hand to reach)
|  (Search / Avatar)    |     Use for secondary status or display only.
+-----------------------+
|                       |
|   Content Viewing     |  <- STRETCH ZONE (Requires thumb extension)
|   & Reading Cards     |     Use for scrollable content, images, body text.
|                       |
+-----------------------+
|  Primary Navigation   |  <- NATURAL THUMB ZONE (Instant, effortless reach)
|  & Action Buttons     |     Use for Tab Bars, Floating CTAs, Bottom Sheets.
+-----------------------+
|  Safe Area Indicator  |
+-----------------------+
```

1. **Natural Thumb Zone (Bottom 40%)**: Place primary navigation tabs, key action buttons (e.g. "Save", "Submit", "Continue"), and expandable bottom sheet headers here.
2. **Stretch Zone (Middle 35%)**: Place content lists, detail views, and interactive cards here.
3. **Difficult Zone (Top 25%)**: Avoid placing primary irreversible destructive actions or high-frequency actions here. Use for informational headers or back navigation buttons.

---

## 3. Phone Landscape Ergonomics

When a mobile phone is rotated to landscape:
1. **Vertical Constraint**: Available height drops significantly (often under 400px to 450px).
2. **Side Navigation Rails**: Replace bottom tab bars with a compact vertical navigation rail docked to the left edge:
   ```css
   @media (max-height: 500px) and (orientation: landscape) {
     .navigation-container {
       flex-direction: column;
       width: 64px;
       height: 100vh;
       border-right: 1px solid var(--surface-border);
     }
   }
   ```
3. **Horizontal Field Pairing**: Never stack full-width form inputs vertically in landscape. Arrange fields into side-by-side columns to prevent keyboards from hiding the entire view.

---

## 4. Tablet Ergonomics Across Orientations

Tablets have larger physical dimensions and are commonly held with two hands by their lateral edges, or placed on a desk with a keyboard/trackpad folio.

### Tablet Portrait Mode
- **Dual Lateral Thumbs**: Primary interactive controls should be positioned along the left and right margins within reach of thumbs holding the tablet sides.
- **Reading Comfort**: Never allow text paragraphs to span the full width (e.g. 800px to 1024px). Constrain reading containers to a maximum width of `68ch`.
- **Adaptive Grid**: Use a 2-column card grid rather than stretching single items across the full display.

### Tablet Landscape Mode (Master-Detail Dual Pane)
- **Split-View Architecture**:
  - **Master Pane (Left)**: Fixed width of 320px to 380px. Contains searchable list items, message threads, or category navigation.
  - **Detail Pane (Right)**: Expands across remaining viewport width. Contains full item details, interactive editing forms, and context menus.
- **Dual Modality**:
  - Support touch navigation with generous tap targets (44pt).
  - Provide desktop-style hover states, cursor changes (`cursor: pointer`), and keyboard shortcuts (`Cmd/Ctrl + K`, `Escape`) for users with attached keyboards.

---

## 5. Hardware Insets and Safe Areas

Always anchor application boundaries to device hardware perimeters:

```css
:root {
  --sat: env(safe-area-inset-top, 0px);
  --sar: env(safe-area-inset-right, 0px);
  --sab: env(safe-area-inset-bottom, 0px);
  --sal: env(safe-area-inset-left, 0px);
}

.mobile-app-shell {
  padding-top: var(--sat);
  padding-right: var(--sar);
  padding-bottom: var(--sab);
  padding-left: var(--sal);
  min-height: 100vh;
  box-sizing: border-box;
}
```

1. **Notches and Dynamic Islands**: Safe area top inset prevents text and icons from colliding with hardware sensors.
2. **Home Indicator Bar**: Safe area bottom inset prevents bottom navigation tabs and primary buttons from overlapping the swipe-up system gesture bar.
