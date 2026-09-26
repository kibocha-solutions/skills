# Modern CSS Architecture, Design Tokens, and Responsive Layouts

This reference defines the technical implementation standards for CSS custom properties, fluid typography, container queries, and nested border radius geometry.

## 1. CSS Custom Properties and Theming Architecture

Structure design tokens using semantic CSS custom properties under `:root` and theme selector attributes:

```css
:root {
  /* Typography Scale */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
  
  /* Fluid Body and Heading Sizes */
  --font-size-sm: clamp(0.8rem, 0.17vw + 0.76rem, 0.89rem);
  --font-size-base: clamp(1rem, 0.34vw + 0.91rem, 1.19rem);
  --font-size-lg: clamp(1.25rem, 0.61vw + 1.1rem, 1.58rem);
  --font-size-xl: clamp(1.56rem, 1vw + 1.31rem, 2.11rem);
  --font-size-2xl: clamp(1.95rem, 1.56vw + 1.56rem, 2.81rem);

  /* Spacing Scale (8px baseline) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Geometry Tokens */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Default Light Theme */
  --surface-primary: #ffffff;
  --surface-secondary: #f4f4f5;
  --surface-elevated: #ffffff;
  --surface-border: #e4e4e7;
  
  --content-primary: #18181b;
  --content-secondary: #71717a;
  --content-muted: #a1a1aa;
  
  --accent-default: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-subtle: #eff6ff;

  --feedback-error: #ef4444;
  --feedback-warning: #f59e0b;
  --feedback-success: #10b981;
}

/* Dark Theme Overrides */
[data-theme='dark'] {
  --surface-primary: #09090b;
  --surface-secondary: #18181b;
  --surface-elevated: #27272a;
  --surface-border: #27272a;
  
  --content-primary: #fafafa;
  --content-secondary: #a1a1aa;
  --content-muted: #71717a;
  
  --accent-default: #3b82f6;
  --accent-hover: #60a5fa;
  --accent-subtle: #1e293b;
}
```

---

## 2. Container Queries (`@container`)

Build components to respond to their container width rather than the browser window:

```css
/* Define Container Context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Default Mobile / Compact Presentation */
.product-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4);
}

/* Adaptive Container Presentation */
@container card (min-width: 420px) {
  .product-card {
    display: grid;
    grid-template-columns: 120px 1fr;
    align-items: center;
    padding: var(--space-6);
  }
}
```

---

## 3. Nested Border Radius Formula

Inner corners inside a padded card must have smaller border radius to prevent visual pinching or awkward gaps:

$$\text{Radius}_{\text{inner}} = \max(0, \text{Radius}_{\text{outer}} - \text{Padding})$$

```css
.card {
  --card-padding: 16px;
  --card-radius: 16px;

  padding: var(--card-padding);
  border-radius: var(--card-radius);
}

.card-inner-image {
  /* Calculated nested radius: 16px - 16px = 0, or if padding is 8px: 16px - 8px = 8px */
  border-radius: calc(var(--card-radius) - var(--card-padding));
}
```

---

## 4. CSS Logical Properties

Always prefer CSS logical properties for bi-directional layout flexibility:

- Use `padding-inline` and `padding-block` instead of `padding-left/right` and `padding-top/bottom`.
- Use `margin-inline` and `margin-block` instead of `margin-left/right` and `margin-top/bottom`.
- Use `border-inline-start` instead of `border-left`.
