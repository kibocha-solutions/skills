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
