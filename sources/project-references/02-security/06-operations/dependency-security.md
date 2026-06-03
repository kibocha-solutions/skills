# Dependency Management

## 12.1 Dependency Security

**The Problem:**
Third-party dependencies can introduce vulnerabilities into your application.

**Why Critical:**
- 80% of code in modern applications is third-party
- Vulnerabilities in dependencies affect your app
- Supply chain attacks target popular packages
- Outdated dependencies have known exploits

**Vulnerability Management:**

**1. Scan Dependencies Regularly:**

```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
pip install --upgrade package-name

# Rust
cargo audit

# Ruby
bundle audit

# Java
dependency-check

# Go
go list -m all | nancy sleuth
```

**2. Automate Dependency Updates:**

```
// Dependabot (GitHub)
// Renovate Bot
// Snyk

// Automatically creates PRs for dependency updates
// Includes vulnerability information
// Prioritizes security updates
```

**3. Review Before Installing:**

```
// Check before `npm install unknown-package`
- Download count (popular = more eyes)
- Last update date (maintained?)
- Open issues count
- GitHub stars
- License
- Known vulnerabilities
```

**4. Lock Dependencies:**

```
// package-lock.json (Node.js)
// Pipfile.lock (Python)
// Cargo.lock (Rust)
// Gemfile.lock (Ruby)

// Ensures exact versions deployed
// Prevents unexpected updates
// Commit to version control
```

**5. Minimize Dependencies:**

```
// Only install what you need
// Fewer dependencies = smaller attack surface
// Review package.json/requirements.txt regularly
// Remove unused dependencies
```

**6. Private Package Registry:**

```
// For sensitive projects
// Host your own package registry
// Scan packages before adding to registry
// Control what enters your organization
```

**Supply Chain Attacks:**

**Examples:**
- event-stream (2018): Malicious code added to steal Bitcoin
- ua-parser-js (2021): Malware distributed via npm
- colors.js (2022): Maintainer sabotaged own package

**Prevention:**
- Use package lock files
- Verify package signatures
- Use Subresource Integrity (SRI) for CDN resources
- Review dependency updates before merging
- Use security scanning tools

**Verification:**
- [ ] Dependencies scanned weekly
- [ ] Automated updates configured
- [ ] Lock files committed
- [ ] No critical vulnerabilities present
- [ ] Unused dependencies removed
- [ ] SRI implemented for CDN resources
