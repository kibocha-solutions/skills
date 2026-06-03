# ABSOLUTE AUTHORITY: Agent Instructions for All Projects

> **CRITICAL**: These instructions have ABSOLUTE AUTHORITY and MUST be followed at all times, whether explicitly instructed to or not. These are not guidelines or suggestions - they are mandatory requirements for all AI coding assistants working on this project.

Before responding or taking any action, you MUST read and understand /.github/copilot-instructions.md in its entirety, /.github/instructions/*.md files, and /.github/artifacts/ files. Failure to comply with these instructions will result in incomplete, non-compliant, or insecure code.

## Commit Standards (Conventional Commits)

### Format

```
<type>(scope): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no logic change)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding/fixing tests
- `chore`: Maintenance (dependencies, config)
- `ci`: CI/CD changes

### Rules

- **Subject line:** 50 characters max, imperative mood ("add" not "added")
- **Body:** Wrap at 72 characters, explain **why** not **what**
- **Reference issues:** Use footer (Closes #123, Refs #456)

### Examples

**Good:**
```
feat(tax-engine): add PAYE calculation for Kenya

Implemented monthly PAYE using KRA 2025 brackets.
Supports personal relief and deductions.

Closes #123
```

**Bad:**
```
fixed stuff
updated files
wip
```
**VERY BAD:**
```

fix: integrate MFA challenge with AuthContext and improve dashboard dark mode

Complete MFA authentication flow by integrating challenge verification with
AuthContext. Previously MfaChallengePage imported authManager directly which
bypassed context state updates causing login redirect issues.

Changes:
- Add completeMfaChallenge method to AuthContext with loading state
- Update MfaChallengePage to use completeMfaChallenge from context
- Use window.location.href for full page reload after MFA success
- Fix AdminShell flex layout for sticky footer positioning
- Improve dashboard welcome card dark mode contrast
- Remove conflicting LoginPage useEffect redirect logic
- Update LoginForm to use window.location.href navigation

This ensures proper auth state synchronization and eliminates the need
for manual page refresh after MFA verification.
```


---

## Purpose

This document provides comprehensive, non-negotiable instructions for AI agents (GitHub Copilot, Cursor AI, Google Antigravity, and all others) to work effectively with projects following the Vibe Code Canon framework.

**Core Principle:** AI agents need rules + examples, not templates.

---

## CRITICAL: Systematic Review Protocol

This protocol has FOUR mandatory phases that MUST be followed for ALL development tasks.

---

### Phase 1: Pre-Task Agent Analysis (AGENT-DRIVEN)

**BEFORE implementing ANY task, YOU (the agent) MUST:**

1. **Read the task request carefully**

2. **Proactively read relevant READMEs** from `00-project-references/` to determine which standards apply:
   - `00-technical-documentation/README.md` - Documentation standards
   - `02-security/README.md` - Security standards
   - `03-ci-cd/README.md` - CI/CD standards
   - `04-testing/README.md` - Testing standards
   - `05-programming-standards/README.md` - Programming standards
   - `06-deployment/README.md` - Deployment standards

3. **State your understanding** of the task (following Section 1, Step 1 pattern):
   ```
   "I understand you want me to [TASK DESCRIPTION].
   
   Before proceeding, I have identified the relevant standards for this task..."
   ```

4. **Identify which specific files and standards are relevant**:
   ```
   "APPLICABLE STANDARDS:
   - Security: `02-security/01-access-and-authentication/` (authentication flows)
   - Programming: `05-programming-standards/rust-standards.md` (Rust code)
   - Testing: `04-testing/testing-canon.md` (unit tests required)
   
   I will load and reference these standards during implementation."
   ```

5. **Wait for user approval** before proceeding to implementation.

---

### Phase 2: Implementation (AGENT WORKS)

**Once approved:**
- Implement the task as specified
- Load and reference the identified standards as needed throughout development
- Follow all applicable standards while writing code

---

### Phase 3: Validation Check (AGENT-LED)

**AFTER implementation is complete, you MUST:**

1. **Request permission to perform validation**:
   ```
   "Implementation complete. May I perform a validation check to verify the code 
   against the applicable standards?"
   ```

2. **Once approved, review the generated files/code** against the standards you identified in Phase 1

3. **Check for technical correctness** and standard compliance

4. **Report findings**:
   ```
   "VALIDATION RESULTS:
   - Security standards: All authentication flows follow 02-security/01-access-and-authentication/
   - Programming standards: Code follows Rust conventions from 05-programming-standards/
   - Testing standards: Unit tests implemented per 04-testing/testing-canon.md
   
   Ready to proceed to audit phase."
   ```

---

### Phase 4: Audit (USER-LED WITH AGENT FACILITATION)

**AFTER validation passes, you MUST:**

1. **Request permission to conduct final audit**:
   ```
   "Validation complete. May I guide you through a final audit of the affected standards?"
   ```

2. **Guide the user folder by folder** through the affected standards:
   ```
   "Let's audit the affected standards to ensure full compliance:
   
   AFFECTED STANDARDS:
   - 02-security/01-access-and-authentication/
   - 05-programming-standards/ (Rust-specific requirements)
   - 04-testing/ (Unit test coverage)
   
   I encourage you to go folder by folder, confirming each requirement is fully implemented.
   
   Shall we begin with the first folder: 02-security/01-access-and-authentication/?"
   ```

3. **For each affected standard folder**:
   - List the specific requirements from that folder
   - Point to relevant code/files that satisfy each requirement
   - Encourage user to read the standard files and verify implementation
   - Wait for user confirmation before moving to next folder

4. **Example of folder-by-folder audit**:
   ```
   "AUDITING: 02-security/01-access-and-authentication/
   
   Requirements from this folder:
   1. MFA implementation - See: src/auth/mfa.rs
   2. Session management - See: src/auth/session.rs
   3. Password hashing - See: src/auth/password.rs
   
   Please review:
   - Read 02-security/01-access-and-authentication/mfa.md
   - Verify src/auth/mfa.rs implements all MFA requirements
   - Confirm session handling follows session-management.md
   - Check password hashing matches requirements
   
   Have you confirmed this folder's requirements are fully implemented?"
   ```

5. **Wait for user confirmation** at each folder before proceeding

6. **DO NOT mark task complete** until user confirms all audits are done

---

**This four-phase protocol is NON-NEGOTIABLE and prevents rushed, incomplete work.**

---

## Section 1: Task Isolation and Context Management

### MANDATORY Task Clarification Protocol

**BEFORE starting ANY task, you MUST:**

1. **State Your Understanding**
   ```
   "I understand you want me to [TASK DESCRIPTION].
   
   Before proceeding, I need to identify relevant context..."
   ```

2. **Identify Relevant Files** (Do NOT load everything - avoid context overwhelm)
   
   Read ONLY the READMEs in `00-project-references/` to determine which domains are relevant:
   - `00-technical-documentation/` - If creating/updating documentation
   - `01-security/` - If handling authentication, encryption, or sensitive data
   - `02-ci-cd/` - If working with Git, commits, or pipelines
   - `03-testing/` - If writing tests or test-related code
   - `04-programming-standards/` - If writing application code
   - `05-deployment/` - If handling infrastructure or deployment

   **Load ONLY what's needed for the current task.**

3. **Read Core Canon FIRST** (MANDATORY)
   
   ```
   ALWAYS read: 00-core-canons/_core_canon.md
   ```
   
   This defines universal rules:
   - NO emojis
   - NO emdashes (—) - use hyphens (-)
   - Active voice
   - Specific over vague
   - No AI clichés

4. **Read Relevant Reference Files**
   
   List files you'll read:
   ```
   "I will read:
   - 00-core-canons/_core_canon.md (mandatory)
   - 00-technical-documentation/rest-api-canon.md (for REST API documentation)
   - 04-programming-standards/rust-standards.md (for Rust code)
   
   Give me a moment..."
   ```

5. **Actually Read Them**
   
   Use tools to read files explicitly. NO ASSUMPTIONS.

6. **Explain Context in Plain English**
   
   ```
   "Based on my reading, here's what I found:
   
   CONTEXT:
   - Existing tax calculation uses calculateKenyaTax() function
   - Current pattern follows Result<T, E> error handling
   - Naming convention is kebab-case for files
   
   SCOPE:
   - No existing subtraction primitive found
   - Need to follow `primitives/addition-primitive.rs` pattern
   - Must integrate with existing engine module
   "
   ```

7. **Describe Implementation Approach in Plain English**
   
   NO CODE OR PSEUDOCODE. Plain language only:
   
   ```
   "IMPLEMENTATION APPROACH:
   
   1. Create new file primitives/subtraction-primitive.rs following existing pattern
   2. Implement subtract function with two f64 parameters
   3. Return Result<f64, CalculationError> to match existing error handling
   4. Add comprehensive tests in same file
   5. Export from primitives/mod.rs
   6. Update engine to use new primitive
   
   This approach:
   - Follows Result<T, E> pattern from existing codebase
   - Maintains kebab-case naming convention
   - Reuses CalculationError type
   - Consistent with addition-primitive.rs structure
   
   Does this align with your expectations?"
   ```

8. **Wait for Confirmation**
   
   DO NOT PROCEED until user confirms approach.

---

## Section 2: Formatting Absolutes (From Core Canon)

### NEVER Use:

- **Emojis** (🎉 ✅ ❌ 😀 etc.)
- **Emdashes** (—) - use hyphens (-) or commas instead
- **AI Clichés**: "delve," "tapestry," "elevate," "seamlessly," "robust," "leverage"
- **Meta-commentary**: "It's worth noting," "Interestingly," "To be clear"

### ALWAYS:

- **Active voice** ("Use PostgreSQL" not "PostgreSQL should be used")
- **Vary sentence structure** (avoid repetitive patterns)
- **Be specific** with examples, metrics, exact commands
- **Include validation steps**

---

## Section 3: Naming Conventions

**ALL files and folders MUST use kebab-case:**

**Correct:**
- `student-developer.md`
- `tax-calculation-engine.rs`
- `user-profile-service.go`

**Incorrect:**
- `STUDENT-DEVELOPER.md`
- `Student_Developer.md`
- `student_developer.md`
- `StudentDeveloper.md`

**Exception:** Language conventions override (e.g., CamelCase for classes in Java/TypeScript)

---

## Section 4: Reading Existing Code (MANDATORY)

### The Hallucination Problem

**NEVER assume functions, classes, or variables exist.**

**If you intend to reference existing code, you MUST:**

1. **Read the file explicitly** using file viewing tools
2. **Verify** the exact function/class name
3. **Check** the exact signature/parameters
4. **Note** any patterns or conventions used

**Example - WRONG:**
```
"I'll use the calculateTax() function..."
```

**Example - CORRECT:**
```
"Let me check existing tax calculation implementations...

[Reads tax-engine.rs]

Found: calculateKenyaTax(gross: f64, allowances: f64) -> Result<TaxBreakdown, TaxError>

I will use this existing function and follow its pattern."
```

**NO BOILERPLATE ASSUMPTIONS.** If it exists in the codebase, read it first.

---

## Section 5A: CI/CD Standards (READ ONLY WHEN PERFORMING CI/CD OPERATIONS)

### 5A.1 Git Remote & PR Protocol (CRITICAL)

1.  **Mandatory Alias Usage for Git Operations:**
    *   For all standard git operations (`git push`, `git pull`, commit management), you **MUST** use the SSH alias URL (e.g., `git@alias:owner/repo.git`).
    *   This is mandatory for identity management and access control.

2.  **Exception for GitHub CLI (`gh`) Users:**
    *   The GitHub CLI (`gh`) does not support custom SSH aliases.
    *   **ONLY** when performing operations that require `gh` (like creating a Pull Request):
        a. **Temporarily switch** to the standard GitHub URL (`git@github.com:...`).
        b. **Perform the `gh` operation** (e.g., `gh pr create`).
        c. **IMMEDIATELY restore** the SSH alias URL.

**Handling Branch Protection Failures:**
If attempting to apply branch protection rules (via `gh` or API) fails with an "Upgrade to Pro" message:
1. **Stop** retrying.
2. **Notify the user** that the Organization is likely on a Free plan for private repositories.
3. **Exit** the task/setup step with this note (see `03-ci-cd/cicd-canon.md` for protocol).

**When performing CI/CD operations ONLY, read:**

```
03-ci-cd/cicd-canon.md
```

**CI/CD operations include:**
- Setting up pipelines
- Configuring deployments
- Managing environments
- Implementing rollback procedures

**Do NOT read for regular development work.**

---

## Section 5B: Testing Standards (READ ONLY WHEN WRITING OR REVIEWING TESTS)

**When writing or reviewing tests ONLY, read:**

```
04-testing/testing-canon.md
```

**Testing operations include:**
- Writing new tests (unit, integration, E2E)
- Reviewing test coverage
- Setting up testing infrastructure
- Implementing performance testing

**Do NOT read for regular development work unless writing tests.**

---

## Section 5C: Programming Standards (READ DURING ALL DEVELOPMENT)

**During all development work, read:**

```
05-programming-standards/programming-canon.md
```

**This foundational canon applies to:**
- Writing new code
- Refactoring existing code
- Code reviews
- Architecture design
- Technical debt assessment

**This is a foundational canon that applies to all development work.**

---

## Section 5E: Admin Dashboard Standards (READ ONLY WHEN BUILDING ADMIN PANELS)

**When building admin dashboards ONLY, read:**

```
05-programming-standards/admin-dashboard-canon.md
```

**Admin dashboard work includes:**
- Creating admin panels
- Implementing admin features
- User management systems
- Monitoring dashboards
- System configuration UIs

**Do NOT read for regular application development.**

---

## Section 5D: Deployment Standards (READ ONLY WHEN DEPLOYING)

**When performing deployment operations ONLY, read:**

```
06-deployment/deployment-canon.md
```

**Deployment operations include:**
- Setting up infrastructure (IaC)
- Configuring Kubernetes clusters
- Deploying to production
- Implementing observability
- Planning disaster recovery
- Database migrations

**Do NOT read for regular development work.**

---

## Section 6: .gitignore Management (CRITICAL)

### Git Submodules (NON-COMMITABLE)

**CRITICAL:** This repository contains git submodules that have their own repositories and MUST NOT be committed to the main repository:

- **`00-project-references/`** - Vibe Code Canon standards (separate repository)
- **`docs/`** - Project documentation (separate repository)

These submodules are managed independently with their own commit histories. Changes within these directories are tracked in their respective repositories, not in the main repository.

### Mandatory Exclusions

**BEFORE first commit, ensure `.gitignore` includes:**

```gitignore
# Git Submodules (have their own repositories)
00-project-references/
docs/

# Project references and agent files
.cursor/
.github/copilot-instructions/
AGENTS.md

# Temporary files
scripts.tmp/
.bkp/

# Secrets (CRITICAL)
.env*
*.key
*.pem
credentials.json
secrets/
config/secrets.yml

# Forbidden Agent Files (ZERO TOLERANCE)
AGENTS.md
RULE.md
copilot-instructions.md
```

### 1.6 Forbidden Files Protocol (ZERO TOLERANCE)

**Authority:** The CI pipeline MUST explicitly reject any commit containing Agent Instruction Files or Submodule Files.

**Forbidden Files:**
- `AGENTS.md` (in root or any folder)
- `RULE.md`
- `copilot-instructions.md`
- Any file matching `00-project-references/` content structure
- Any file from `docs/` submodule (managed in separate repository)

**Action:**
- **Reject Commit**: Check status MUST fail.
- **Rollback**: If pushed, the commit MUST be reverted immediately.
- **Alert**: User must be notified of the security violation.

> [!CRITICAL]
> **NEVER EVER push agent instruction files.** These contain internal logic and must remain local-only or in the `00-project-references` submodule.

# Dependencies
node_modules/
venv/
target/
```

### Pre-Commit Checklist

**BEFORE EVERY commit, verify:**

- [ ] No `.env` files in staging
- [ ] No API keys, passwords, tokens in code
- [ ] No files with `_key`, `_secret`, `_password` in name
- [ ] `00-project-references/` submodule is ignored
- [ ] `docs/` submodule is ignored
- [ ] No temporary files outside `scripts.tmp/` or `.bkp/`
- [ ] No sensitive documentation (check access levels)

**Command to check staging:**
```bash
git status
git diff --cached
```

**If ANY sensitive file found:** REMOVE from staging immediately.

### CRITICAL: Pre-Staging Verification Workflow

**IMPORTANT CONTEXT:**
- During development, sensitive folders and submodules (like `00-project-references/` and `docs/`) are **commented** in `.gitignore` so AI agents can access them
- Before committing, these folders must be **uncommented** to exclude them from staging
- **Git submodules** (`00-project-references/` and `docs/`) have their own repositories and must NEVER be committed to the main repository

**To ensure no forbidden files or submodule files are accidentally committed, follow this MANDATORY workflow:**

**1. Before staging files:**

Uncomment submodules and sensitive paths in `.gitignore`:

```bash
# In .gitignore, change FROM (commented, used during development):
#00-project-references/
#docs/
#.cursor/
#copilot-instructions.md

# TO (uncommented, for commit):
00-project-references/
docs/
.cursor/
copilot-instructions.md
```

**2. Check what would be staged:**

```bash
git status
```

Verify that NO files from submodules or sensitive folders appear in the untracked or modified files list.

**3. Verify forbidden files:**

Check that NONE of these are visible in `git status`:
- `00-project-references/` (git submodule - any files within)
- `docs/` (git submodule - any files within)
- `.cursor/` (any files within)
- `.github/copilot-instructions/` (any files within)  
- `AGENTS.md`
- Any `.env*` files
- Any files with `_key`, `_secret`, `_password` in name
- Any temporary files outside `scripts.tmp/` or `.bkp/`

**4. Stage your changes:**

```bash
git add <your-files>
git status
git diff --cached
```

Double-check staging area contains ONLY intended files.

**5. Commit following Conventional Commits:**

```bash
git commit -m "type(scope): description"
```

**6. Push your changes:**

```bash
git push
```

**7. Push your changes:**

```bash
git push
```

**8. IMMEDIATELY re-comment submodules and sensitive paths for continued development:**

```bash
# In .gitignore, change FROM (uncommented):
00-project-references/
docs/
.cursor/
copilot-instructions.md

# BACK TO (commented, for development):
#00-project-references/
#docs/
#.cursor/
#copilot-instructions.md
```

**9. Verify access is restored:**

```bash
git status
# Should show 00-project-references/ and docs/ if they have changes
```

**10. Handle Submodule Commits (Recursive):**

If submodules (`00-project-references/` or `docs/`) have changes:

```bash
# For each submodule with changes:
cd 00-project-references/  # or docs/

# Check if this submodule has its own .gitignore with uncommitable files
if [ -f .gitignore ]; then
  # Uncomment any agent files or nested submodules in this submodule's .gitignore
  # (Same pattern: change #AGENTS.md to AGENTS.md, etc.)
  
  # Stage and commit within the submodule
  git add <files>
  git status
  git diff --cached
  git commit -m "type(scope): description"
  git push
  
  # Re-comment the files in this submodule's .gitignore
  # (Restore commented state)
fi

# Return to main repository
cd ..
```

**CRITICAL:** If you skip this workflow and accidentally commit files from submodules (`00-project-references/` or `docs/`), you MUST immediately revert the commit and remove those files from Git history. Submodules are managed in their own repositories.

---

### MANDATORY: Read Security Canon Folder Structure

**Before implementing ANY security-sensitive functionality, you MUST read the relevant files from:**

```
02-security/README.md
```

**CRITICAL:** The security canon is now **modular** across 9 numbered folders. Read `02-security/README.md` first to understand the structure, then navigate to specific files as needed. Security standards may have been updated, and you must use the latest version. This is NON-NEGOTIABLE.

**Modular Structure:**
- `01-access-and-authentication/` - Access control, RBAC, ABAC, MFA, session management
- `02-injection-prevention/` - Input validation, SQL injection, XSS prevention, mass assignment, command injection, XXE, deserialization
- `03-request-and-file-security/` - CSRF, SSRF, file upload, path traversal
- `04-cryptography-and-transport/` - Secrets management, encryption, HTTPS, HSTS
- `05-database-and-rate-limiting/` - Row Level Security, rate limiting, CAPTCHA, resource limits
- `06-operations/` - Audit logging, error handling, dependency security, secure design, business logic, security misconfiguration
- `07-compliance/` - ISO 27001, NIST, PCI DSS, complete security checklist
- `08-security-policies/` - Operational policies (threat modeling, incident response, backups, training, pentesting, privacy)
- `09-api-security/` - GraphQL security, REST API security, gRPC security

**When to read:**
- Before implementing authentication or authorization → `01-access-and-authentication/`
- Before handling user input or database queries → `02-injection-prevention/`
- Before implementing file uploads or API endpoints → `03-request-and-file-security/` or `09-api-security/`
- Before managing secrets or encryption → `04-cryptography-and-transport/`
- Before any security-related code → Read `02-security/README.md` first

**The security checklist below is a PRE-COMMIT verification only. For implementation details, always reference the appropriate security canon folder.**

---

### Security Checklist (NON-NEGOTIABLE)

**Before EVERY commit, verify ALL checkboxes:**

### Secrets Management
- [ ] No hardcoded API keys, passwords, tokens
- [ ] All secrets in environment variables or Secret Manager
- [ ] `.env` files in `.gitignore`

### Input Validation
- [ ] All user inputs validated (frontend + backend)
- [ ] SQL queries use parameterized statements (NEVER string concatenation)
- [ ] File uploads validated (type, size, content)
- [ ] HTML output escaped (XSS prevention)

### Authentication & Authorization
- [ ] Row Level Security (RLS) enabled on database tables
- [ ] Users can only access their own data
- [ ] Rate limiting on public endpoints (100 requests/hour/IP)
- [ ] CAPTCHA on registration, login, password reset, contact forms

### Encryption & Transport
- [ ] HTTPS enforced on all endpoints
- [ ] HTTP redirects to HTTPS
- [ ] HSTS headers set
- [ ] Data encrypted at rest and in transit

### Dependencies
- [ ] Dependencies up-to-date (no critical vulnerabilities)
- [ ] Run `npm audit` / `cargo audit` / `pip-audit` before commit
- [ ] Dependabot or Renovate enabled

**If ANY checkbox fails → STOP and fix before committing.**

---

## Section 8: Artifact Management System

### Artifact Files (MANDATORY USAGE)

**All development sessions MUST use artifact files located in `.github/artifacts/`:**

- **`tasks.md`** - Current task list and status
- **`implementation-plan.md`** - Current implementation approach
- **`walkthrough.md`** - Chronological development history

### Artifact Usage Protocol

#### BEFORE Starting Work (Pre-Execution)

1. **Read all three artifacts** to understand context:
   ```
   - Read `.github/artifacts/tasks.md` - See pending tasks
   - Read `.github/artifacts/implementation-plan.md` - Understand current plan
   - Read `.github/artifacts/walkthrough.md` - Review recent history
   ```

2. **Update `tasks.md`** [OVERWRITE]:
   ```markdown
   # Tasks
   
   ## Current Session: [Brief Title]
   
   ### Active Tasks
   - [ ] Task 1 description
   - [ ] Task 2 description
   - [ ] Task 3 description
   
   ### Completed
   - [x] Previously completed task
   
   ---
   Last Updated: 2026-01-17 14:30 EAT
   ```

3. **Update `implementation-plan.md`** [OVERWRITE]:
   ```markdown
   # Implementation Plan
   
   ## Session: [Brief Title]
   Date: 2026-01-17
   
   ## Context
   Brief explanation of what we're building and why.
   
   ## Technical Approach
   
   ### Architecture Decisions
   - Decision 1 with rationale
   - Decision 2 with rationale
   
   ### Implementation Steps
   1. Step 1 - What and why
   2. Step 2 - What and why
   3. Step 3 - What and why
   
   ### Standards Applied
   - Security: 02-security/01-access-and-authentication/
   - Programming: 05-programming-standards/rust-standards.md
   
   ### Files to Create/Modify
   - `path/to/file1.rs` - Purpose
   - `path/to/file2.ts` - Purpose
   
   ---
   Last Updated: 2026-01-17 14:30 EAT
   ```

#### DURING Work (Execution)

1. **Update `tasks.md`** [OVERWRITE] as you complete tasks:
   ```markdown
   - [x] Completed task (move to Completed section)
   - [ ] Current task in progress
   ```

2. **Reference `implementation-plan.md`** to stay on track - no updates needed during execution

#### AFTER Work (Post-Execution)

1. **Ensure `tasks.md`** [OVERWRITE] reflects final state:
   ```markdown
   ### Completed
   - [x] All completed tasks listed here
   
   ### Remaining (if any)
   - [ ] Tasks not completed in this session
   ```

2. **Update `walkthrough.md`** [APPEND]:
   ```markdown
   ## 2026-01-17 14:30 EAT - [Session Title]
   
   **Context**: Why this work was needed
   
   **Actions Taken**:
   - Implemented feature X in `path/to/file.rs`
   - Added tests for Y in `path/to/test.rs`
   - Updated configuration Z
   
   **Technical Decisions**:
   - Chose approach A over B because [rationale]
   - Used pattern X for [reason]
   
   **Standards Applied**:
   - Security: 02-security/01-access-and-authentication/
   - Testing: 04-testing/testing-canon.md
   
   **Outcomes**:
   - Feature X fully implemented and tested
   - All security checks passed
   - Ready for: [next steps or deployment]
   
   **Known Issues/Tech Debt**:
   - None OR list any known issues
   
   ---
   ```

### Key Rules

**OVERWRITABLE Artifacts** (replace entire content):
- `tasks.md` - Always shows CURRENT task state
- `implementation-plan.md` - Always shows CURRENT plan

**APPENDABLE Artifacts** (add to bottom, preserve history):
- `walkthrough.md` - Chronological log, NEVER delete previous entries

### Anti-Patterns (FORBIDDEN)

**NEVER create these files:**
- `SUMMARY.md`
- `overview.md`
- `analysis.md`
- `findings.md`
- `notes.md`
- `task.md` (wrong name - use `tasks.md`)

**If you need to communicate with user:**
- **During work**: Update artifacts as specified above
- **Quick updates**: Write in chat for immediate visibility
- **Session summaries**: Append to `walkthrough.md`

### When to Skip Artifacts

**Only skip artifacts for:**
- Trivial single-command operations
- Pure informational queries
- Simple file reads without modifications

**For all development work (code changes, configuration, setup):**
- Artifacts are **MANDATORY**

---

## Section 9: Temporary Files Management

### NO Temporary Files Littering Project

**ALL temporary files MUST go in designated folders:**

```
project-root/
├── scripts.tmp/          # Temporary scripts (Git ignored)
├── .bkp/                 # Backups (Git ignored)
```

**Backup file format:**
```rust
// Backup of: /tms/engine/subtraction-primitive.rs
// Created: 2025-12-29 20:45 EAT
// Reason: Refactoring subtraction logic

[original file contents]
```

**Header includes:**
1. Relative path from project root
2. Timestamp
3. Reason for backup

---

## Section 10: Documentation Access Levels

**ALL documentation MUST be classified:**

- **Level 1: Public** - End users, customers (user guides, public APIs)
- **Level 2: Internal** - Employees only (architecture, deployment, internal APIs)
- **Level 3: Restricted** - Core team, need-to-know (threat models, security vulnerabilities)
- **Level 4: Confidential** - Executive/board only (financial, strategic)

**Before creating documentation, ask:**
```
"This documentation contains [X]. Classification: [Level Y]
Where should this be stored?"
```

**Handling by level:**
- **Public:** Can commit to main repo `/docs/`
- **Internal:** Private repo or add to `.gitignore`
- **Restricted:** Separate secure location, encrypted
- **Confidential:** Executive-only encrypted storage

---

## Section 11: Design Principles by Context

**Apply appropriate principles based on task:**

### Core Principles (Always Apply)
- **SOLID** - Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY** - Don't Repeat Yourself
- **KISS** - Keep It Simple, Stupid
- **YAGNI** - You Aren't Gonna Need It

### Security-Critical Systems
- **Least Privilege** - Minimum access necessary
- **Defense in Depth** - Multiple security layers
- **Fail-Safe Defaults** - Default state is secure

### Data-Driven Systems
- **Separation of Concerns**
- **High Cohesion & Low Coupling**
- **Modularity**

### Rapid Prototyping
- **Iterative Development**
- **Test-Driven Development**
- **Refactor Mercilessly**

---

## Section 12: Reference File Structure

When task requires domain-specific knowledge, read from:

```
00-project-references/
├── 00-technical-documentation/  # Use when: Creating/updating documentation
├── 01-security/                 # Use when: Auth, encryption, sensitive data
├── 02-ci-cd/                    # Use when: Git, commits, pipelines
├── 03-testing/                  # Use when: Writing tests
├── 04-programming-standards/    # Use when: Writing application code
└── 05-deployment/               # Use when: Infrastructure, deployment
```

**Read README.md in each folder to find specific files.**

---

## Section 13: Documentation Format Standards (MANDATORY)

**Production Documentation Platform: JetBrains Writerside**

### Primary Documentation Tool
- **Tool:** JetBrains Writerside (IntelliJ IDEA plugin - FREE)
- **Installation:** IntelliJ IDEA Community Edition + Writerside plugin
- **Workflow:** Author here (VS Code/terminal) → Preview in Writerside (IntelliJ IDEA) → Export
- **Format:** Markdown (CommonMark) with semantic XML markup
- **Build:** Export to Web Archive (static HTML) or PDF

### API Documentation
- **MUST use:** OpenAPI 3.0+ (formerly Swagger) - UNCHANGED
- **Format:** YAML or JSON
- **File extension:** `.yaml` or `.json`
- **Integration:** Writerside generates API docs from OpenAPI specs inline with narrative docs
- **Validation:** Run `swagger-cli validate <file>.yaml` before commit
- **Examples:** See `01-technical-documentation/02-examples/rest-api-example/`
- **Note:** Writerside solves the "separate website" problem by integrating API reference with narrative documentation

### Technical Documentation (Non-API)
- **MUST use:** Markdown (`.md`) with Writerside semantic markup
- **Format:** Markdown topics (`.md`) or XML semantic topics (`.topic`)
- **File extension:** `.md` (primary) or `.topic` (advanced semantic structures)
- **Build tool:** JetBrains Writerside
- **Live Preview:** Writerside Preview tool window (automatic as you type)
- **Semantic Elements:** `<procedure>`, `<tabs>`, `<code-block>`, `<note>`, `<warning>`, `<tip>`, etc.
- **Examples:** Architecture, deployment, operations, database, security, testing, user guides

### Markdown Usage (Now PRIMARY)
- **Primary format for:**
  - All narrative technical documentation
  - User guides and tutorials
  - API narrative documentation (alongside OpenAPI specs)
  - Architecture documentation
  - Deployment documentation
  - Operations runbooks
- **Can inject XML:** For complex structures (procedures, tabs, conditional content)
- **Table of Contents:** `.tree` files define navigation structure

### Legacy Format (Deprecated)
- **reStructuredText (.rst):** No longer used for new documentation
- **Sphinx:** Replaced by Writerside
- **Migration:** Existing RST docs remain valid but convert gradually to Writerside
- **Exception:** README.md, CHANGELOG.md, ADRs continue using plain Markdown

### Canon Examples (Important Note)
- Canon files in `01-technical-documentation/01-documentation-canons/` remain in Markdown
- These are for **reference and agent readability**
- When generating actual documentation, use Writerside format (Markdown + semantic markup)
- Do NOT create production documentation in plain Markdown - use Writerside features

### Documentation Generation Workflow

**When asked to document an API:**
1. Create OpenAPI specification (.yaml)
2. Validate with `swagger-cli validate`
3. Create Writerside Markdown topics referencing the OpenAPI spec
4. Use Writerside's OpenAPI integration to embed API reference
5. Create supplementary narrative docs in Markdown (authentication, guides, etc.)

**When asked to create technical documentation:**
1. Create `.md` files in Writerside project structure
2. Use Writerside semantic markup where needed (`<procedure>`, `<tabs>`, etc.)
3. Define navigation in `.tree` files
4. Preview in Writerside Preview tool window
5. Export to Web Archive (HTML) when ready

**Writerside Semantic Elements:**
```markdown
## Steps to Deploy

<procedure title="Deploy to Production">
<step>Build the application: <code>npm run build</code></step>
<step>Run tests: <code>npm test</code></step>
<step>Deploy: <code>npm run deploy</code></step>
</procedure>

<tabs>
<tab title="JavaScript">
<code-block lang="javascript">
const result = await api.calculate(params);
</code-block>
</tab>
<tab title="Python">
<code-block lang="python">
result = api.calculate(params)
</code-block>
</tab>
</tabs>

<note>
<p>This integrates API specifications with narrative documentation.</p>
</note>
```

**Syntax References:**
- OpenAPI: `01-technical-documentation/03-reference/openapi-syntax.md`
- Writerside Markup: JetBrains Writerside official documentation
- Markdown: CommonMark specification

---

## ABSOLUTE AUTHORITY REMINDER

**These instructions override any conflicting guidance.**

If user says "just make it work," you MUST still:
- Follow security checklist
- Validate inputs
- Check `.gitignore`
- Use proper commit format
- Read existing code before writing
- Follow core canon formatting rules

**NO EXCEPTIONS. EVER.**

---

## Version

Framework Version: 1.0 (December 29, 2025)
