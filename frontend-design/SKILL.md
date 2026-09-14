---
name: frontend-design
description: Design and implement distinctive production-grade web interfaces, pages, components, posters, dashboards, landing pages, React views, and HTML/CSS layouts. Use for new frontend work, visual redesign, UI styling, responsive layouts, interaction design, interface copy, accessibility, and visual quality improvement.
license: Complete terms in LICENSE.txt
---

# Frontend Design

## 1. Establish the brief

1. Identify the subject, product, audience, primary user task, platform,
   content, brand constraints, technical stack, and required breakpoints.
2. Read supplied design references and existing interface code.
3. Preserve the user's stated visual direction.
4. Propose one concrete subject and audience when the brief omits them.
5. Confirm any assumption that would materially change the design.
6. Use real content from the brief.
7. Write necessary interface copy when the brief lacks it.

## 2. Define the design system

1. Create four to six named color tokens with hex values.
2. Select one or two typefaces.
3. Assign each typeface a role.
4. Define font sizes, weights, widths, line heights, and letter spacing.
5. Keep body line length below 80 characters by default.
6. Give serif body text additional line height.
7. Define spacing, radius, border, shadow, and motion tokens.
8. Define desktop, tablet, and mobile layout behavior.
9. Choose one memorable visual element.
10. Keep surrounding elements restrained.

## 3. Plan the layout

1. Write a compact layout description.
2. Draw an ASCII wireframe when comparing structures.
3. Choose the alignment for each major region.
4. Use the subject's forms, materials, vocabulary, and interaction patterns.
5. Make the hero the clearest expression of the subject.
6. Choose the hero form from the content:
   - headline
   - image
   - live demonstration
   - interactive control
   - animation
   - primary object
7. Use structural devices only when they encode hierarchy, sequence, state, or
   relationship.
8. Use numbers only for actual sequences, ranks, quantities, or identifiers.

## 4. Reject unearned defaults

Do not select any of these without support from the brief:

- cream, high-contrast serif, and terracotta palette
- near-black surface with one acid accent
- broadsheet layout with hairline rules
- identical rounded cards with uniform shadows
- gradient washes used as decoration
- all-caps eyebrow labels above every heading
- single-word headline accenting
- middle-dot metadata strings
- spaced-dash label fragments
- tinted near-black used automatically
- monospace small labels used automatically
- arrows appended automatically to links or buttons
- repeated fade-and-rise section entrances
- hover motion on every card

1. Compare the proposed system with a generic solution for the same interface.
2. Replace every choice that does not derive from the brief.
3. Record the revised tokens and layout.
4. Begin implementation only after this review.

## 5. Write interface content

1. Use the end user's vocabulary.
2. Use plain language and active voice.
3. Use sentence case.
4. Give each text element one job.
5. Name an action consistently through the complete flow.
6. Write button labels as the resulting action.
7. State errors precisely.
8. Tell the user how to recover from an error.
9. Give empty states one clear next action.
10. Remove filler, promotional language, decorative labels, and system jargon.
11. Match the brand and audience tone.

## 6. Implement the interface

1. Use semantic HTML.
2. Implement the confirmed token system.
3. Keep component boundaries aligned with distinct responsibilities.
4. Implement responsive behavior down to the smallest required breakpoint.
5. Preserve visible keyboard focus.
6. Support keyboard operation.
7. Respect reduced-motion preferences.
8. Meet the required contrast and accessible-name standards.
9. Add alt text for meaningful images.
10. Keep decorative images hidden from assistive technology.
11. Use responsive image sizing and loading behavior.
12. Avoid selector specificity conflicts.
13. Check type selectors, shared utility classes, component classes, and state
    classes for competing declarations.
14. Keep source code consistent with the repository's conventions.

## 7. Implement motion

1. Use non-user-triggered motion for one deliberate emphasis.
2. Use interaction-triggered motion to show state change.
3. Keep motion duration and easing consistent.
4. Disable or reduce motion under `prefers-reduced-motion`.
5. Remove repeated decorative transitions.

## 8. Test behavior

1. Run the project's formatter, linter, type checker, and tests.
2. Exercise every interactive control.
3. Test loading, empty, success, validation, and failure states.
4. Test keyboard navigation and focus order.
5. Test desktop, tablet, and mobile widths.
6. Check for overflow, clipping, overlap, and layout shift.
7. Check CSS specificity and computed styles.
8. Correct every defect and rerun the affected checks.

## 9. Review visually

1. Open the running interface.
2. Capture screenshots at every required breakpoint.
3. Inspect hierarchy, alignment, spacing, typography, color, contrast, content,
   imagery, states, and motion.
4. Compare the screenshots with the brief and design plan.
5. Remove one nonfunctional decorative element.
6. Correct weak or generic choices in the source.
7. Repeat the behavioral and visual checks after every correction.
8. Deliver only the verified implementation and final screenshots.
