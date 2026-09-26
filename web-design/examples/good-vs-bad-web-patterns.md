# Web Design Examples: Good vs Bad Implementation Patterns

This document contrasts inaccessible, generic web implementations against high-craft, accessible patterns.

## 1. Interactive Button and Focus States

### Bad: Div as Button, Suppressed Outlines, Fake Decorator

```html
<!-- BAD: Inaccessible div, no keyboard navigation, hidden outline, decorative arrow -->
<div 
  onclick="saveChanges()" 
  style="background: #3b82f6; color: #ffffff; padding: 10px 16px; border-radius: 9999px; outline: none; cursor: pointer; display: inline-block;">
  Submit Form &rarr;
</div>
```

Defects:
- Fails keyboard navigation: not focusable via `Tab`, cannot be triggered via `Enter` or `Space`.
- Suppresses focus outlines with `outline: none`, stranding keyboard users.
- Uses arbitrary inline styling rather than tokenized custom properties.
- Appends generic arrow entity (`&rarr;`) without semantic justification.

---

### Good: Semantic Button, Tokenized Styling, Focus-Visible, Tactile Feedback

```html
<!-- GOOD: Semantic button, visible focus ring, tactile touch-down feedback -->
<button 
  type="submit"
  class="px-4 py-2 bg-blue-600 text-white font-medium text-sm rounded-md shadow-sm hover:bg-blue-700 active:scale-[0.98] transition-all duration-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-600">
  Save Account Changes
</button>
```

Advantages:
- Native `<button>` element with complete browser keyboard and screen reader accessibility.
- High-contrast `:focus-visible` ring provides clear keyboard indication without cluttering mouse clicks.
- Snappy tactile touch-down feedback (`active:scale-[0.98] duration-100`).
- Clear, action-oriented button copy without decorative arrow filler.

---

## 2. Form Input with Inline Validation

### Bad: Unassociated Label, Floating Red Text, Inaccessible Errors

```html
<!-- BAD: Unlinked label, no aria-invalid, error not connected to input -->
<div class="form-group">
  <span class="label">Email Address</span>
  <input type="text" name="email" value="invalid-email" style="border: 1px solid red;" />
  <span class="error" style="color: red;">Invalid email address</span>
</div>
```

Defects:
- `<span class="label">` does not focus the input when clicked.
- Input lacks `aria-invalid="true"`, so screen readers do not announce error state.
- Error message has no `id`, leaving screen readers unaware of the relationship.

---

### Good: Linked Label, Explicit Error Association, Accessible Announcement

```html
<!-- GOOD: Linked label, aria-invalid, aria-describedby linking error text -->
<div class="flex flex-col gap-1.5">
  <label for="user-email" class="text-sm font-medium text-zinc-900 dark:text-zinc-100">
    Email Address
  </label>
  <input 
    type="email" 
    id="user-email" 
    name="email"
    aria-invalid="true" 
    aria-describedby="user-email-error"
    class="px-3 py-2 text-sm border border-red-500 rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 dark:bg-zinc-900"
    value="user@broken" />
  <p id="user-email-error" class="text-xs text-red-600 dark:text-red-400 font-medium" role="alert">
    Please enter a valid email address including a domain name (e.g. name@example.com).
  </p>
</div>
```

Advantages:
- `<label for="...">` correctly focuses input on click.
- Screen readers announce "invalid" due to `aria-invalid="true"`.
- Error message explicitly linked via `aria-describedby="user-email-error"`.
- Error text explains exactly how to fix the issue.
