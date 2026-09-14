# Tasks

- [x] Read the governing CI/CD and Bootstrap instructions.
- [x] Build the Claude archive with `CLAUDE.md`.
- [x] Build the Codex archive with `AGENTS.md`.
- [x] Verify both archives and record checksums.
- [x] Audit and validate the complete repository change set.
- [/] Commit and push the repository changes.
- [ ] Propagate rules and skills to Claude, Codex, Gemini CLI, Gemini Antigravity, and Copilot.
- [ ] Verify every propagated destination.
- [ ] Finalize this session record.

## Added

- [x] Restore the previously required repository-local SSH-signing configuration.
- [x] Make the CI/CD commit-count and commit-message contract explicit.
- [x] Add concrete commit-message examples and behavioral evaluation cases.
- [ ] Fix Gemini CLI vs Gemini Antigravity target confusion on this machine: no `gemini` binary, `~/.gemini/settings.json`, or `~/.gemini/hooks/` exist here, so the root `~/.gemini/GEMINI.md`/`skills/` target (meant for standalone Gemini CLI) is unused and stale; only `~/.gemini/antigravity/builtin/` (Gemini Antigravity, actually installed) is live. Update `ensure-gemini-link.sh` to skip the root target when no real Gemini CLI product is detected, rather than removing Gemini CLI support from the shared script outright, then remove the stale root copy on this machine.
- [ ] Resolve conflict between this session's "no AI attribution in publication metadata" boundary and the current session's harness-level instruction to append a Co-Authored-By trailer to every commit, before finalizing the pending commit.
