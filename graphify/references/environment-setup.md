# Environment Setup

## 1. Check prerequisites

```bash
python3 --version
command -v uv
command -v cgc
command -v code-review-graph
```

## 2. Apply the installation gate

1. Report each missing command.
2. Name the proposed installation method and target location.
3. Read `../../system-init/SKILL.md`.
4. Install a qualifying dependency under the universal installation rule.
5. Stop and ask the user to run the exact command when privilege blocks it.
6. Do not pipe remote content into a shell.

## 3. Install

Use the verified installation method and scope.

```bash
uv tool install codegraphcontext
uv tool install code-review-graph
```

## 4. Verify executables

```bash
cgc doctor
code-review-graph serve --help
```

## 5. Verify storage

1. Create `.agents/code-graphs/` in the target repository when persistent graph state is authorized.
2. Add `.agents/code-graphs/` to the repository ignore rules.
3. Do not write graph state into the skill package directory.
4. Do not change home-directory configuration unless the user explicitly requests it.
