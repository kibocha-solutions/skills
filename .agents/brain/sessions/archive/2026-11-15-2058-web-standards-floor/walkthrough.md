# Walkthrough

## Decisions

1. The user chose to route Modern Web Guidance through the repository skills instead of installing its plugin per host, with no fixed version.
2. Standards and anti-slop instructions live in the skills, which every host mirrors; the device record holds device facts and installed tool records only.
3. Primary sources checked on 2026-11-15: Core Web Vitals thresholds, OWASP Top 10:2025, ASVS 5.0.0, WCAG 3.0 Working Draft status, Material Web maintenance mode and absence of Expressive support, Baseline target guidance, Chrome DevTools for agents.
4. The Writerside install reference kept a `.previous` wrapper copy, which contradicts the steward rule against backup copies; the step is removed.

5. `modern-web-guidance retrieve` writes guides above 9.5 KB to `/tmp/mwg-guide-*.md` and leaves them; web-design and the tool registry now require deleting each file after reading.
6. Fixed token names in interface-design and web-design now apply only to a product's own system; established foundations keep their own role names.

## Evidence

1. `steward.py device` wrote the Facts section; a second run preserved the Tools rows and the hand-written Defaults table.
2. `steward.py tool ensure modern-web-guidance impeccable` installed 1.0.0 and 4.9.1 from `@latest`; a repeat run reported the recorded version without reinstalling.
3. `modern-web-guidance search "confirmation modal dialog"` returned `dialog`, `declarative-dialog-popover-control`, `platform-controls-dismiss-dialog`, and `html`; `retrieve dialog` saved a 12.1 KB guide to `/tmp`, deleted after the test.
4. `impeccable detect --json` on a generic sample page exited 2 with `low-contrast`, `overused-font`, `nested-cards`, and `ai-color-palette`; the sample was deleted from the scratch store.
5. `wrs update` pulled `2026.10.0423`, matched the Docker Hub digest, and removed `2026.08.0328`. `wrs doctor --online` passed every check without a pinned tag.
6. `wrs build public -j 1` on the msngi documentation passed 186 of 186 checks with no warnings; `report.json` shows zero errors and zero warnings; the msngi worktree was unchanged.
7. Link and anchor check over changed Markdown: 0 problems. No U+2014 in changed files. Largest `SKILL.md` is 351 lines.
8. `steward.py check`: clean.

## Limitations

1. The builder failure exit status `255` was not re-tested with `2026.10.0423`.
2. Rollout to the host skill mirrors requires a push to `origin/main`; GitHub SSH authentication failed during this work because the SSH agent did not supply the key.
