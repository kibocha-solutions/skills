# Cryptography and Secrets Management

## 6.1 Secrets Management

**The Problem:**
Hardcoded secrets in code or configuration files lead to credential exposure.

**What Are Secrets:**
- API keys
- Database passwords
- Encryption keys
- OAuth client secrets
- Service account credentials
- Private keys
- Signing secrets

**Bad Practices (FORBIDDEN):**

```
// NEVER do this
const API_KEY = "sk_live_a7f3c2d8b1e9..."
const DB_PASSWORD = "MyPassword123"

// NEVER commit .env files
// NEVER store secrets in version control
```

**Good Practices (REQUIRED):**

**1. Environment Variables:**

```
// .env file (NOT committed to Git)
API_KEY=sk_live_a7f3c2d8b1e9
DB_PASSWORD=MySecurePassword123

// Application code
const apiKey = process.env.API_KEY
const dbPassword = process.env.DB_PASSWORD
```

**.gitignore MUST include:**
```
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
secrets/
```

**2. Secrets Managers (RECOMMENDED):**

```
// Google Secret Manager
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
api_key = client.access_secret_version(name="projects/123/secrets/api-key/versions/latest")

// AWS Secrets Manager
import boto3
client = boto3.client('secretsmanager')
api_key = client.get_secret_value(SecretId='api-key')

// Azure Key Vault
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url="https://myvault.vault.azure.net/")
api_key = client.get_secret("api-key")
```

**3. Separate Secrets Per Environment:**

```
Development: dev-api-key
Staging: staging-api-key
Production: prod-api-key

NEVER reuse secrets across environments
```

**4. Rotate Secrets Regularly:**

```
// Rotation schedule
API keys: Every 90 days
Database passwords: Every 90 days
Encryption keys: Every 90 days
Service account keys: Every 90 days

// Implement automated rotation where possible
```

**5. Least Privilege for Secrets:**

```
// Service A only gets secrets it needs
service_a_secrets = ["database-password", "api-key-service-b"]

// Service A cannot access Service B's admin key
```

**Verification:**
- [ ] No hardcoded secrets in code
- [ ] .env files in .gitignore
- [ ] Using secrets manager for production
- [ ] Separate secrets per environment
- [ ] Secret rotation schedule implemented
- [ ] Least privilege applied to secret access

---

## 6.2 Cryptographic Failures Prevention

**Weak Algorithms (FORBIDDEN):**
- [REJECTED] MD5, SHA-1 (broken for cryptographic purposes)
- [REJECTED] DES, 3DES (weak)
- [REJECTED] RC4 (broken)
- [REJECTED] ECB mode (reveals patterns)

**Current Algorithms (REQUIRED):**
- [APPROVED] SHA-256, SHA-3, BLAKE3 (hashing)
- [APPROVED] AES-256-GCM, ChaCha20-Poly1305 (encryption)
- [APPROVED] RSA-2048 or higher, Ed25519 (asymmetric)
- [APPROVED] Argon2id, bcrypt, scrypt (password hashing)

**Common Failures:**

**1. Improper Key Management:**
- Hardcoded keys in code
- Keys stored in version control
- Same key for all environments
- No key rotation

**2. Insufficient Randomness:**
```
// BAD
Math.random()  // Predictable

// GOOD
crypto.getRandomValues()  // Cryptographically secure
```

**3. Improper Implementation:**
- Using encryption without authentication (use AEAD modes)
- Reusing initialization vectors (IV must be unique)
- Not validating TLS certificates

**4. Password Storage:**

```
// NEVER
passwords.save(password)  // Plaintext

// NEVER
sha256(password)  // No salt, vulnerable to rainbow tables

// CORRECT
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

// Or Argon2id (recommended)
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)
```

**Requirements:**
- Use industry-standard libraries (don't implement your own crypto)
- Use authenticated encryption (AES-256-GCM or ChaCha20-Poly1305)
- Store keys in secrets manager
- Rotate keys every 90 days
- Use TLS 1.3 (not TLS 1.0/1.1/1.2)
- Validate all certificates
- Use CSPRNG for random values
- Use Argon2id or bcrypt for password hashing

**Verification:**
- [ ] No hardcoded encryption keys
- [ ] Using approved algorithms only
- [ ] Keys stored in secrets manager
- [ ] TLS 1.3 enforced
- [ ] Certificates validated
- [ ] Passwords hashed with Argon2id or bcrypt

---

## 6.3 Data Sanitization and Secure Disposal

**The Problem:**
Data doesn't disappear when you delete it. File deletion only removes the reference, data remains on disk.

**Methods:**

**1. Deletion (INSECURE):**
- Removes file reference only
- Data remains on disk
- Easily recoverable

**2. Data Wiping/Overwriting (SECURE for reuse):**
- Overwrites data with random data multiple times
- Follows NIST SP 800-88 standard
- Makes data unrecoverable
- Allows hardware reuse

**3. Physical Destruction (SECURE for disposal):**
- Shredding, crushing, incinerating
- Guarantees data cannot be recovered
- Hardware cannot be reused
- Required for highly sensitive data

**4. Cryptographic Erasure (SECURE for encrypted systems):**
- Destroy encryption keys
- Data becomes permanently unreadable
- Fast and efficient
- Only works if data was encrypted

**NIST 800-88 Standard:**
- **Clear:** Logical overwriting (reuse in same organization)
- **Purge:** Physical/cryptographic destruction (transfer to another organization)
- **Destroy:** Physical destruction (disposal)

**Requirements:**

**When user data is deleted:**
- Overwrite data with NIST 800-88 compliant method
- Don't just mark as deleted
- Document sanitization in audit log

**When hardware is decommissioned:**
- Use certified data wiping software
- Verify 100% data wiped
- Physical destruction if highly sensitive
- Document disposal (who, when, method, certificate)

**When backups are removed:**
- Securely delete backup files
- Remove from all storage locations
- Update backup inventory

**Verification:**
- [ ] Deleted data is overwritten, not just marked as deleted
- [ ] Using NIST 800-88 compliant wiping tools
- [ ] Hardware disposal documented
- [ ] Backup deletion includes all copies
