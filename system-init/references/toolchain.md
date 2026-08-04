# Toolchain

## The Standard Stack

Eight tools, checked every pass: Java, Kotlin, Python, Docker, Node, Git,
GitHub CLI, GitLab CLI.

| Tool | Detection commands |
| --- | --- |
| Java | `java -version`, `javac -version` |
| Kotlin | `kotlinc -version` |
| Python | `python3 --version`, `pip3 --version`, `python3 -m venv --help` |
| Docker | `docker --version`, `docker compose version`, `groups` (confirm `docker` group membership) |
| Node | `node --version`, `npm --version` |
| Git | `git --version` |
| GitHub CLI | `gh --version` |
| GitLab CLI | `glab --version` (its own output flags a newer release if one exists — trust that over a one-off web search, see below) |

## Compare Against Current LTS/Stable, Not Whatever's Installed

A tool being present isn't sufficient — it must be on its current
supported line:

- **Node** — the current LTS release line specifically, not a stale distro
  repository package. Check the installed major version against Node's
  current LTS schedule.
- **Java** — the current LTS JDK release line (e.g. the most recent LTS,
  not an old interim release).
- **Python** — the current stable Python 3.x line.
- **Kotlin** — the current stable Kotlin release.
- **Docker** — the current stable Docker release channel.
- **Git, GitHub CLI, GitLab CLI** — each tool's own current stable release.

Do not treat "it runs `--version` without error" as sufficient — read the
actual version number and compare it. Verify "current LTS/stable" against a
live source (the tool's own release page, package registry, or a web
search) rather than the agent's own static training knowledge — LTS
schedules move on, and a model's knowledge of "what's current" goes stale
well before this skill file does.

**A single web search is not automatically a live source** — it can itself
be stale or wrong. When installing `glab`, a web search reported the latest
release as v1.32.0; `glab`'s own self-update check (querying GitLab's
release API directly, printed as part of its normal output) reported the
real current release as v1.112.0 — eighty versions newer. Prefer a tool's
own version/update-check output, or a direct query against the project's
official release API/tags, over a general web search when the two might
disagree.

## Ask Before Resolving — Always

If a tool is **missing** or **not on its current LTS/stable line**, stop and
ask the user for leave to resolve it. Do not install or upgrade silently,
even though `SOFTWARE` sudoers access may technically make the install
possible. This follows the same install-approval rule as any other package
(see `permissions.md`): proceed without asking only when the user
explicitly requested that specific install/upgrade in its own dedicated
message, it's clearly relevant to the current project, and nothing about it
looks compromised. A stale or missing toolchain component doesn't meet that
bar on its own — surface it and ask.

## Docker's Access Path Is Different From the Rest

Docker access comes from the operating account's membership in the `docker`
group, not from the sudoers grant — it is a separate, already-accepted trade-off
(group membership is root-equivalent on the host, since a container can
mount the host filesystem). When reporting toolchain or permission status,
don't conflate Docker's group-based access with the `SOFTWARE` / `INSPECT`
/ `EDITFILES` sudoers aliases — they're different mechanisms with different
scopes, and a report that blurs them misrepresents what's actually granted.

## Version Management Mechanisms (Learned From This Workstation)

Each tool's upgrade path differs, and picking the wrong one either risks the
base OS or silently fails to close the gap:

- **Python** — the system `python3` (owned by a `python3.*-minimal`
  package) is a base-OS dependency; Ubuntu itself relies on it. Never
  upgrade, remove, or replace it. Install newer Python versions via
  `pyenv` instead — user-level, built from source in the account's own home
  (`~/.pyenv`), set as its default via `pyenv global`, entirely
  separate from the system install. Needs build dependencies installed
  first (`build-essential`, `libssl-dev`, `zlib1g-dev`, and the rest of
  pyenv's documented build-dependency list) via plain `apt-get install` —
  within `SOFTWARE` scope, no special handling needed. Clone `pyenv` via
  `git clone`, not a piped install script.
- **Node** — if installed via a NodeSource apt repo, that repo is pinned to
  one major version in its URL (e.g. `deb.nodesource.com/node_22.x`) —
  `apt-get upgrade` only ever reaches the latest *patch* of that major
  line, never a new major/LTS line. Jumping to a new major requires
  rewriting `/etc/apt/sources.list.d/nodesource.list`, which is a
  privileged file edit — needs that exact path added to `EDITFILES` first
  (see `permissions.md`), or the live user doing it directly.
  NodeSource's own setup script is not a substitute — it needs to run as
  root to write that file and a GPG key, which isn't `sudoedit`-shaped and
  isn't otherwise in scope; do not run a downloaded script with `sudo` to
  route around this.
- **Docker** — check which package provides it (`dpkg -l | grep docker`).
  Ubuntu's own `docker.io` package and Docker's official `docker-ce` (from
  `download.docker.com`) are different packages with different release
  cadences — `docker.io` can be fully up to date within Ubuntu's own repo
  and still be behind upstream Docker's latest release. Closing that gap
  means switching package sources (new apt repo + new GPG key), which is a
  bigger, distinct decision from an in-place upgrade — surface it and ask
  rather than doing it as part of a routine "keep things current" pass.
- **GitHub CLI (`gh`) and GitLab CLI (`glab`)** — both publish portable
  prebuilt binaries as release archives (check the project's actual release
  API for the correct current asset name — naming conventions change
  between versions, e.g. `glab`'s asset casing changed between v1.32.0 and
  v1.112.0). Download directly, extract to `~/.local/opt`, link into
  `~/.local/bin` — same pattern as Kotlin below, no apt repo or root needed
  for either.
- **Git** — no portable binary distribution exists; the distro-packaged
  version (via `apt`) is typically well behind upstream. Build from source
  into a user prefix, no root needed: download the release tarball from
  `github.com/git/git`, `make configure && ./configure --prefix=$HOME/.local
  && make && make install`. Needs `autoconf`, `libcurl4-openssl-dev`,
  `libexpat1-dev`, `gettext` in addition to the standard build-essential set
  — install via plain `apt-get install`, within `SOFTWARE` scope.
- **Kotlin** — same fix as everything above that isn't apt-repo-pinned:
  user-level install — download the official release archive directly (not
  a piped script; a plain download-and-extract carries none of the "piping
  remote content into a shell" risk), extract to `~/.local/opt`, link into
  `~/.local/bin` — and remove the stale distro package once the working
  version is confirmed, since an old broken `kotlinc` left on `PATH` risks
  being picked up by mistake later.

## Reporting Gaps

State plainly, per tool: installed and current / installed but outdated
(with the actual version found vs. the current line) / missing entirely /
installed but broken (the binary exists but errors out instead of reporting
a usable version — treat this the same as missing, not as "present"). Don't
silently omit a gap because it seems minor, and don't round "close to
current" up to "current" — report the actual finding and let the user
decide whether it matters for the task at hand.
