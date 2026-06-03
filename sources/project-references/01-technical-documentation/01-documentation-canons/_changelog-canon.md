# Canon: Changelog Documentation

## Purpose

Changelog documentation provides a chronological record of all notable changes to a project, enabling users to understand what changed between versions, when features were added, bugs were fixed, and breaking changes introduced.

---

## Scope

**This canon applies to:**
- Version releases (major, minor, patch)
- Feature additions
- Bug fixes
- Breaking changes
- Deprecations
- Security fixes

**This canon does NOT apply to:**
- Individual commit messages (use Git)
- Internal code refactoring (unless user-visible impact)
- Documentation typo fixes
- CI/CD configuration changes

---

## Access Level Classification

**Changelog Documentation:**
- **Access Level:** Public (Level 1) for public-facing products, Internal (Level 2) for internal tools
- **Distribution:** End users, developers, stakeholders
- **Storage:** Public repository (for open-source), private repository (for internal tools)
- **Review:** Product owner approval, release manager review
- **Rationale:** Transparent communication of changes to users

---

## When to Generate

### Triggers for Updating Changelog

Update changelog when:

- **Releasing New Version**: Every release must have changelog entry
- **Breaking Changes**: Document immediately when introduced
- **Security Fixes**: Document in dedicated section
- **Feature Additions**: Add to "Unreleased" section during development

### Frequency
- **During Development**: Add to "Unreleased" section continuously
- **At Release**: Move "Unreleased" items to versioned section
- **Immediately**: Security fixes and critical bug fixes

---

## Files to Generate

Agent must create changelog following this structure:

### Changelog File
**File:** `/CHANGELOG.md` (project root) **Format**: Markdown  
**Purpose**: Chronological record of all changes

---

## Directory Structure

```
CHANGELOG.md (single file in project root)
```

---

## Generation Rules

### Format: Keep a Changelog

Follow "Keep a Changelog" v1.1.0 standard (https://keepachangelog.com/)

**Guiding Principles:**
- Changelogs are for humans, not machines
- One entry per version
- Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
- Versions and dates are clearly marked
- Latest version comes first

### Versioning: Semantic Versioning

Follow Semantic Versioning (SemVer 2.0.0):

**MAJOR.MINOR.PATCH** (e.g., 2.5.1)

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

### Change Categories

Group changes under these headings:

**Added** - New features  
**Changed** - Changes to existing functionality  
**Deprecated** - Features marked for removal  
**Removed** - Removed features  
**Fixed** - Bug fixes  
**Security** - Security vulnerability fixes

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice where possible
- Specific over vague (what changed, not "improvements")
- User-facing language (avoid technical jargon)
- **Markdown format**

---

## Content Guidelines

### Changelog Template (`/CHANGELOG.md`)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Feature X for improved user experience

### Changed
- Updated tax calculation algorithm for 2026 rates

### Fixed
- Bug causing incorrect tax calculations for salaries > 100,000

## [2.5.0] - 2025-12-15

### Added
- Multi-currency support (USD, EUR, GBP)
- Receipt export to PDF
- Email notifications for completed calculations

### Changed
- Improved performance of tax calculation API (30% faster)
- Updated UI for receipt management screen

### Deprecated
- REST API v1 (will be removed in v3.0.0, use v2)

### Fixed
- Fixed race condition in session management
- Corrected tax bracket calculation for edge cases

### Security
- Updated dependencies to patch CVE-2025-12345

## [2.4.1] - 2025-11-30

### Fixed
- Critical bug in payment processing
- Timezone handling for UTC conversions

### Security
- Patched SQL injection vulnerability in reporting module

## [2.4.0] - 2025-11-15

### Added
- Integration with M-Pesa for payments
- Dark mode support
- Offline mode for mobile app

### Changed
- Redesigned dashboard with improved analytics

### Removed
- Legacy tax calculation engine (replaced by optimized version)

## [2.3.0] - 2025-10-30

### Added
- KRA eTIMS integration
- Automated tax submission
- Receipt storage in cloud

## [2.2.0] - 2025-10-01

### Added
- User authentication with JWT
- Multi-factor authentication
- Admin dashboard

## [2.1.0] - 2025-09-15

### Added
- Tax calculation API
- Receipt generation
- User profiles

## [2.0.0] - 2025-09-01

### Changed
- **BREAKING**: Migrated to new API v2 (v1 deprecated)
- **BREAKING**: Changed authentication from sessions to JWT

### Removed
- **BREAKING**: Removed legacy XML API

## [1.0.0] - 2025-08-01

### Added
- Initial release
- Basic tax calculation
- User registration

[Unreleased]: https://github.com/example/tms/compare/v2.5.0...HEAD
[2.5.0]: https://github.com/example/tms/compare/v2.4.1...v2.5.0
[2.4.1]: https://github.com/example/tms/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/example/tms/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/example/tms/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/example/tms/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/example/tms/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/example/tms/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/example/tms/releases/tag/v1.0.0
```

### Writing Change Entries

**Good Examples:**

```markdown
### Added
- Receipt export to PDF with company branding
- Email notifications when tax calculation completes
- Dark mode support for web application

### Fixed
- Fixed race condition causing duplicate tax calculations
- Corrected timezone handling for users in UTC+3
- Resolved memory leak in background job processor

### Security
- Patched SQL injection vulnerability in search functionality (CVE-2025-12345)
- Updated bcrypt to v5.1.1 to address timing attack vulnerability
```

**Bad Examples (Avoid):**

```markdown
### Added
- Improvements ❌ (Too vague, uses emoji)
- New stuff ❌ (Not specific)
- Feature requested by users ❌ (What feature?)

### Fixed
- Various bug fixes ❌ (Which bugs?)
- Performance improvements ❌ (What improved?)

### Changed
- Updated things ❌ (What things?)
```

### Breaking Changes

Clearly mark breaking changes:

```markdown
## [3.0.0] - 2026-01-15

### ⚠️ BREAKING CHANGES

**REST API v1 Removed**
- REST API v1 endpoints no longer available
- Migration guide: https://docs.example.com/migration-v1-to-v2

**Authentication Changed**
- Session-based auth removed
- All clients must use JWT tokens
- Update authentication implementation

### Removed
- REST API v1 (deprecated in v2.0.0)
- Session-based authentication
```

### Security Fixes

Document security fixes clearly (after responsible disclosure):

```markdown
### Security

- **CVE-2025-12345**: Patched SQL injection in reporting module
  - Severity: High
  - Affected versions: 2.0.0 - 2.4.0
  - Fixed in: 2.4.1
  - Action required: Upgrade immediately
```

---

## Validation

Agent must validate documentation before completion:

### Markdown Validation

```bash
# Lint changelog
markdownlint CHANGELOG.md
```

**Expected output:** No errors

### Content Validation

- [ ] Follows "Keep a Changelog" format
- [ ] Uses Semantic Versioning
- [ ] Latest version at top
- [ ] All versions have dates in ISO format (YYYY-MM-DD)
- [ ] Changes grouped by category (Added, Changed, etc.)
- [ ] Breaking changes clearly marked
- [ ] Security fixes documented

### Link Validation

```bash
# Check all comparison links work
markdown-link-check CHANGELOG.md
```

**Expected output:** All links valid

---

## Examples Reference

See working example: `02-examples/changelog-example/CHANGELOG.md` (to be created)

**Example includes:**
- Complete changelog with multiple versions
- Breaking changes documented
- Security fixes included
- Comparison links working

---

## Access Level Warning

For internal changelogs, include at top:

```markdown
> **Note**: INTERNAL CHANGELOG - Level 2 Access  
> Changes listed here are for internal use only.  
> Public-facing release notes published separately.
```

For public changelogs, no warning needed (Public - Level 1).

---

## Automation

### Generating Changelog from Commits

**Tools**: conventional-changelog, release-please

**Conventional Commits Format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature (MINOR version)
- `fix`: Bug fix (PATCH version)
- `docs`: Documentation changes
- `BREAKING CHANGE`: Breaking change (MAJOR version)

**Example:**

```
feat(api): add multi-currency support

Adds support for USD, EUR, and GBP in tax calculations.

Closes #123
```

Automatically generates changelog:

```markdown
### Added
- Multi-currency support in tax calculations
```

---

## Agent Checklist

Before marking changelog documentation complete, verify:

- [ ] CHANGELOG.md exists in project root
- [ ] Follows "Keep a Changelog" format
- [ ] Uses Semantic Versioning
- [ ] Unreleased section present
- [ ] All versions have dates
- [ ] Changes grouped by category
- [ ] Breaking changes clearly marked
- [ ] Security fixes documented
- [ ] Comparison links work
- [ ] Markdown linting passes
- [ ] No emojis present (except under Deprecated or Breaking Changes warnings)
- [ ] User-facing language (not technical jargon)

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial changelog documentation canon
- Based on "Keep a Changelog" v1.1.0
- Follows `_docs-canon.md` v4 specifications
