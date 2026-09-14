# Renderer Environment

## Procedure

1. Check the project for a documented diagram command.
2. Check the repository for container, CI, Make, task-runner, or package scripts.
3. Check for `drawio-cli`, `drawio`, `diagrams.net`, or `diagramsnet`.
4. Check for `xvfb-run` when the renderer requires a display.
5. Use the project renderer when present.
6. Otherwise run `scripts/render-drawio.sh`.
7. Record the exact source, output, command, and result.
8. Confirm the output modification time follows the source modification time.
9. Inspect the rendered output.

## Permission boundary

- Read `../../system-init/SKILL.md` before downloading or installing a missing
  renderer.
- Apply the universal installation gate.
- Stop and ask the user to run the exact command when privilege blocks it.
- Do not alter Electron sandbox permissions, mounts, services, or security controls.
- Do not substitute an unrelated renderer that changes the source format.

## Failure handling

1. Capture the exact command and error.
2. Check existing project, host, container, and CI options.
3. Stop when all already-available options fail.
4. Report source validation separately.
5. State that rendered visual QA is incomplete.
6. Do not claim the diagram is production-ready.
