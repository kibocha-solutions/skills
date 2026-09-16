# System Init Examples: Safe vs Unsafe Installation Gates

## 1. Qualifying Dependency Installation

### Bad (Piping Remote Content and Sudo Bypass)

```bash
# BAD: Piping curl output directly into bash with root privileges
curl -fsSL https://unverified-repo.org/install.sh | sudo bash

# BAD: Bypassing a sudoers denial by running python with root setuid
sudo -u root python3 -c 'import os; os.system("apt install -y package")'
```

Defects:
- Violates package integrity: untrusted remote script executed directly in shell.
- Violates privilege boundaries: attempts to route around permission denials via interpreter escapes.

### Good (Official Channel, Identity Verification, and Smoke Testing)

```bash
# GOOD: Direct uv tool installation in user space with verification
~/.local/bin/uv tool install codegraphcontext

# Verify executable presence and execution
which cgc
cgc --help > /dev/null && echo "cgc smoke test passed"
```

Advantages:
- User-local installation without requiring root/sudo privileges.
- Verified publisher package via configured index.
- Immediate representative smoke test confirms binary integrity and functionality.
