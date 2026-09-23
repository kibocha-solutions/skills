# Toolchain

## 1. Inspect

Check these components separately:

| Component | Checks |
|---|---|
| Java | `java -version`, `javac -version` |
| Kotlin | `kotlinc -version` |
| Python | `python3 --version`, `pip3 --version`, `python3 -m venv --help` |
| Docker | `docker --version`, `docker compose version` |
| Podman | `podman --version`, `podman info` |
| Node | `node --version`, `npm --version` |
| Git | `git --version` |
| GitHub CLI | `gh --version` |
| GitLab CLI | `glab --version` |

1. Record the executable path with `command -v`.
2. Record the installed version.
3. Record whether the command works.
4. Record the installation source when it can be determined safely.

## 2. Verify current versions

1. Use the official release page, support schedule, registry, or release API.
2. Identify the current LTS line for Node and Java.
3. Identify the current stable supported line for Python, Kotlin, Docker, Podman, Git, GitHub CLI, and GitLab CLI.
4. Compare major and minor support status, not only patch numbers.
5. Record the source and verification date.

## 3. Classify

Mark each component:

1. Installed and current.
2. Installed and supported but not current.
3. Installed and unsupported.
4. Missing.
5. Broken.
6. Shadowed by another executable.

## 4. Select a change path

1. Preserve the operating system's managed Python.
2. Prefer a user-local version manager or project environment when suitable.
3. Identify package-source changes separately from package upgrades.
4. Treat a Docker repository migration as a separate system change.
5. Treat Docker group membership as privileged host access.
6. Use publisher-provided archives only after identity and integrity
   verification.
7. Do not pipe installer content into a shell.

## 5. Apply the installation gate

1. Name the component, current version, target version, source, installation scope, and required dependencies.
2. Apply the qualifying-installation gate in `AGENTS.md`.
3. Follow `dependency-installation.md`.
4. Stop when the source or artifact appears compromised or its identity is
   unresolved.

## 6. Verify after change

1. Re-run the version command.
2. Re-run `command -v`.
3. Run a minimal compile, environment, or connection smoke test.
4. Confirm the old executable does not shadow the intended one.
5. Record the final version, path, source, and test result.
