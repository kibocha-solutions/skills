---
name: wrs-dev-gate
description: wrs --dev gate decisions: one local key, Bitwarden or 1Password, 21-day rotation, no TOTP
type: project
---

The `wrs --dev` gate is one local key for the whole documentation compound, with no per-tier permissions. The key lives in a Bitwarden or 1Password login item, is cached in the login keyring, and rotates every 21 days after a fresh password manager sign-in. There is no TOTP step: the user agreed on 2026-09-23 that a script-side code adds nothing beyond the vault's own two-step login. Production access will use a separate role-based credential service ("doors to each room").

**Why:** TOTP was agreed off, then reintroduced in a later design without asking, and the user had to correct it on 2026-09-24.

**How to apply:** do not add TOTP, per-tier keys, or other gate factors to `wrs` without a new, explicit user decision. When a design step revives something the user already dropped, ask first.
