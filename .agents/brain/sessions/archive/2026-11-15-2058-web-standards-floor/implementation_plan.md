# Web Standards Floor

## Objective

Raise the web and interface skills from a fixed checklist to a floor that routes agents to current primary standards, Google's Modern Web Guidance, one coherent design foundation per product, and deterministic anti-slop checks. Give the steward skill a permanent device record that installs and records shared agent tools at their latest stable release. Make the Writerside builder follow its latest stable image instead of a pinned tag.

## Acceptance criteria

1. `steward.py device` writes `~/.agents/device.md` with stable device facts and a tooling table, and preserves recorded tool rows across runs.
2. `steward.py tool ensure <name>` installs a missing registered tool at its latest stable release, refreshes a record older than 30 days, and records name, version, source, and dates in `~/.agents/device.md`.
3. The registry covers `modern-web-guidance` and `impeccable`; neither command names a fixed version.
4. `interface-design/references/web-standards-catalogue.md` lists the universal floor, standards by product category, design foundation coherence rules, and anti-slop resources, each linked to a primary source that answered during research.
5. `interface-design` selects exactly one design foundation per product and no longer prescribes a blended foundation.
6. `web-design` reads the Baseline target, queries Modern Web Guidance for each platform capability, and runs `impeccable detect` before completion.
7. `mobile-app-design` and `webapp-testing` route to the same guidance where it applies.
8. `wrs` resolves the newest local dated builder image by default, `wrs update` pulls the newest dated tag and removes superseded builder images, and no skill file pins a builder tag.
9. The installed builder image is the newest dated tag on Docker Hub and the superseded image is removed.
10. Every changed `SKILL.md` stays under 500 lines, every local link resolves, and no changed file contains U+2014.
11. `steward.py check` reports no findings.

## Changes

1. `[MODIFY]` `steward/scripts/steward.py`: `device` and `tool` commands.
2. `[MODIFY]` `steward/SKILL.md`, `steward/references/decision-rules.md`: device record and tool registry.
3. `[NEW]` `interface-design/references/web-standards-catalogue.md`.
4. `[MODIFY]` `interface-design/SKILL.md`, `interface-design/examples/good-vs-bad-interface-design.md`.
5. `[MODIFY]` `web-design/SKILL.md`, `mobile-app-design/SKILL.md`, `webapp-testing/SKILL.md`.
6. `[MODIFY]` `documentation/scripts/wrs`, `documentation/references/install-writerside.md`, `documentation/evals/evals.json`.
7. `[MODIFY]` evals for web-design and interface-design.
8. `[MODIFY]` `.agents/memory/interface-design-ecosystem.md`.

## Verification

1. Run `steward.py device` twice and `tool ensure` for each registered tool; read the file.
2. Run `modern-web-guidance search` and `impeccable detect` on a sample file.
3. Run `wrs update` and `wrs doctor --online`; list builder images.
4. Run link, line-count, and em dash checks over changed files; read every changed file in full.
5. Run `steward.py check`.

## Temporary artifacts

1. A sample HTML file for detector testing under the steward scratch store, removed after verification.
2. The superseded builder image, removed by `wrs update`.
3. `~/.local/bin/wrs.previous`, sent to the trash.
