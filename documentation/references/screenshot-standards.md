# Screenshot Standards

Use this reference whenever a webpage or web app screenshot appears in a PR
description, README, or documentation file — anywhere a reader needs to judge
layout, responsiveness, or visual state.

## Standard Viewport Sizes

Capture at these three fixed viewport sizes by default. Do not substitute
arbitrary browser-window dimensions, and do not crop or scale a capture taken
at a different size to approximate one of these.

| Breakpoint | Viewport (CSS px) | Reference device |
| --- | --- | --- |
| Desktop | 1440 × 900 | Standard laptop/desktop viewport |
| Tablet | 768 × 1024 | iPad portrait |
| Mobile | 430 × 932 | iPhone 15 Pro Max (logical/CSS resolution, not physical pixels) |

If the repository defines its own responsive breakpoints (CSS media queries,
Tailwind config, design tokens), capture at those breakpoints instead and
still label each capture with the breakpoint name and viewport size used —
the point is a fixed, reproducible size per form factor, not this exact
table.

## When All Three Are Required

Capture all three sizes when the change affects layout, responsiveness, or is
being documented specifically to demonstrate responsive behavior. A change
scoped to a single form factor (a mobile-only interaction, a desktop-only
admin panel) only needs the size that changed — say so explicitly rather than
omitting the others silently.

## Labeling

Label each image with its breakpoint name and viewport size directly in the
surrounding text or alt text (for example: "Desktop (1440×900)"). A screenshot
with no size label leaves the reader unable to tell whether a layout issue is
real or an artifact of an arbitrary capture width.
