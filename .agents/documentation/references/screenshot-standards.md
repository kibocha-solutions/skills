# Screenshot Standards

## Procedure

1. Identify the visual state to prove.
2. Read the repository's responsive breakpoints and screenshot conventions.
3. Use repository-defined viewports when present.
4. Otherwise capture the default viewports below.
5. Set the viewport explicitly before navigation.
6. Wait for a deterministic ready state.
7. Remove transient cursors, tooltips, loaders, and animations unless they are the subject.
8. Capture the complete required region.
9. Do not resize or crop a different viewport to simulate the target.
10. Label the capture with its breakpoint and CSS-pixel dimensions.
11. Open and inspect the saved screenshot.
12. Check clipping, overlap, spacing, text, controls, focus, and responsive reflow.
13. Retake the screenshot after every relevant application change.

## Default viewports

| Breakpoint | Viewport in CSS pixels |
|---|---:|
| Desktop | 1440 by 900 |
| Tablet | 768 by 1024 |
| Mobile | 430 by 932 |

## Coverage

- Capture all three default viewports for responsive or layout-wide changes.
- Capture only the affected viewport for a form-factor-specific change.
- State the tested viewport in the evidence caption.
- Keep secrets, personal data, tokens, and private account content out of screenshots.
