# Frontend Design Examples: Good vs Bad Component Patterns

## 1. Interactive Button and Focus States

### Bad (Generic Div-Button, Low Contrast, Suppressed Focus)

```html
<!-- BAD: Div used as button, no keyboard support, low contrast, hidden focus -->
<div 
  onclick="submitForm()" 
  style="background: #A0AEC0; color: #E2E8F0; padding: 8px 12px; border-radius: 9999px; outline: none; cursor: pointer;">
  Submit Form &rarr;
</div>
```

Defects:
- Uses `<div>` instead of semantic `<button>`, breaking keyboard `Tab` and `Enter/Space` activation.
- Fails WCAG contrast: light gray text on medium gray background (~2.1:1 contrast).
- Suppresses focus outlines with `outline: none`, stranding keyboard users.
- Automatically appends decorative arrow (`&rarr;`) without semantic purpose.

### Good (Semantic Button, Visible Focus Ring, Tokenized Contrast)

```html
<!-- GOOD: Semantic button, high contrast, explicit focus-visible state -->
<button 
  type="submit"
  class="px-4 py-2 bg-blue-700 text-white font-medium rounded-md hover:bg-blue-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-600 transition-colors">
  Save Account Changes
</button>
```

Advantages:
- Native `<button>` provides built-in accessibility tree role and keyboard activation.
- Exceeds WCAG AAA contrast ratio (>7:1).
- High-contrast `:focus-visible` ring assists keyboard navigation without cluttering mouse clicks.
- Action-oriented button label ("Save Account Changes").
