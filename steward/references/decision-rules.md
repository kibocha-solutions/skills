# Steward Decision Rules

## Capacity budgets

Read the values from `~/.agents/system-profile.md`. Apply a rule when its condition is true at the moment work starts.

| Condition | Required action |
| :--- | :--- |
| Available memory below 2 GiB or below 15 percent of total | Start no heavy job; stop idle processes you started; report to the user. |
| Swap use above 75 percent of total swap | Start no heavy job. |
| Free space on the target filesystem below 10 GiB or below 10 percent | Start no build, image pull, download, or archive; delete your own leftovers first; report to the user. |
| Highest temperature at or above 90 °C | Pause heavy jobs until it falls below 80 °C. |
| One-minute load average above twice the processor thread count | Start no additional parallel work. |
| On battery below 20 percent | Defer heavy jobs and ask the user. |
| Four or fewer processor threads | Cap build and test parallelism at half the thread count, minimum one. |

A heavy job is a build, test suite, container stack, virtual machine, local model, or download above 1 GiB.

## Guard patterns

`steward.py` treats a destination as a backup copy when its name ends with `.bak`, `.backup`, `.old`, `.orig`, `.save`, `~`, `-copy`, `_copy`, ` copy`, or a date suffix such as `.20261115` or `-20261115-1430`, or when its stem is `copy of <name>` or ends with ` copy` or ` (copy)`.

| Hook mode | Refuses |
| :--- | :--- |
| `pre` | `podman` or `docker` `run`/`create` without `--rm` and `agent.throwaway=true`, unless labelled `agent.persistent=true` |
| `pre` | A third throwaway container |
| `pre` | `cp`, `rsync`, or `mv` to a backup-named destination inside a Git worktree |
| `stop` and `check` | Stopped throwaway containers, unused unnamed volumes, abandoned build containers, untracked backup-named files in the worktree, and open ledger entries for the project whose target still exists |

The guard also accepts the project label `talentsphere.throwaway=true` as a throwaway label.

## Agent store

The agent store is `~/.agents/` on the user's home drive. It holds everything agents create that is not part of a project.

| Path | Holds | Retention since last use |
| :--- | :--- | :--- |
| `~/.agents/system-profile.md` | Machine capacity profile | Rewritten each session |
| `~/.agents/device.md` | Stable device facts, installed shared tools, and lasting defaults | Permanent |
| `~/.agents/steward/ledger.tsv` | Steward ledger | Permanent |
| `~/.agents/evidence/<project>/<maestro-session>/` | Screenshots, renders, logs, traces, verification exports | 90 days |
| `~/.agents/envs/<project>-<purpose>/` | Python virtual environments and other toolchain environments | 30 days |
| `~/.agents/scratch/<task>/` | Temporary working files | 2 days |

`steward.py store path` creates the directory and marks it used. `steward.py store prune` lists expired entries; `--apply` removes them. The monthly cleanup job runs `store prune --apply`.

| Toolchain | Placement |
| :--- | :--- |
| Python with uv | `UV_PROJECT_ENVIRONMENT="$(python3 steward.py store path env <project>-py)" uv sync`; uv's shared cache links packages across environments. |
| Python with venv | `python3 -m venv "$(python3 steward.py store path env <project>-py)"` |
| Node.js | Install with `pnpm`; its content-addressed store shares packages across projects. Keep `node_modules` in the project, where Node resolves it. |
| Playwright browsers | Keep the shared default browser cache; never download a second copy per project. |

## Tool registry

`steward.py tool ensure <name>` installs a missing tool with `npm install -g <package>@latest`, compares a recorded tool with the latest release on the registry when its record is 30 days old or `--update` is passed, and writes the version, source, install date, and check date to the Tools section of `~/.agents/device.md`.

| Tool | Package | Used by | Command |
| :--- | :--- | :--- | :--- |
| `modern-web-guidance` | npm `modern-web-guidance` | `web-design`, `mobile-app-design`, `webapp-testing` | `modern-web-guidance search "<query>"`, `retrieve <id>`, `legacy-scan <path> --json` |
| `impeccable` | npm `impeccable` | `interface-design`, `web-design` | `impeccable detect --json <markup files or directories>` |

`modern-web-guidance retrieve` saves output larger than 9.5 KB to `/tmp/mwg-guide-*.md`. Delete each saved guide after reading it.

A global npm install belongs to the active Node.js version. After a Node.js upgrade, `tool ensure` finds the command missing and installs it again.

## Ledger

The ledger is `~/.agents/steward/ledger.tsv`, scoped by project root.

| Command | Effect |
| :--- | :--- |
| `steward.py ledger add <kind> <target> "<condition>"` | Records an open entry. Kinds: `backup`, `container`, `volume`, `image`, `environment`, `cache`, `scratch`, `server`, `build`. |
| `steward.py ledger close <target>` | Closes the entry after deletion. |
| `steward.py ledger close <target> --kept "<approval>"` | Closes the entry as kept with the user's approval text. |
| `steward.py ledger list [--all]` | Lists open entries for the project, or every project. |

## Trash commands

| Platform | Command |
| :--- | :--- |
| Linux desktop | `gio trash <path>` |
| Linux without GIO | `trash-put <path>` |
| macOS 14 or later | `trash <path>` |
| macOS without `trash` | `osascript -e 'tell application "Finder" to delete POSIX file "<absolute path>"'` |
| Windows Subsystem for Linux | `gio trash <path>` when available; otherwise ask the user before permanent removal |
