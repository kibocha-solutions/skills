# Transport and Network Security

## 7.1 HTTPS Enforcement

**The Problem:**
HTTP transmits data in plaintext. Attackers can intercept and read sensitive information.

**Requirements (MANDATORY):**

**1. Use HTTPS for ALL pages:**
```
// Not just login and payment pages
// EVERY page must use HTTPS
```

**2. Redirect HTTP to HTTPS:**

```
// Apache .htaccess
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

// Nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

// Express.js
app.use((req, res, next) => {
  if (!req.secure) {
    return res.redirect('https://' + req.headers.host + req.url)
  }
  next()
})
```

**3. Use Valid Certificates:**
- Obtain from trusted Certificate Authority (Let's Encrypt is free)
- NO self-signed certificates in production
- Renew before expiration

**4. TLS Version:**
```
// Require TLS 1.3 or TLS 1.2 minimum
// Disable TLS 1.0 and TLS 1.1 (deprecated)
ssl_protocols TLSv1.2 TLSv1.3;
```

**5. Strong Cipher Suites:**
```
// Prefer modern, secure ciphers
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;
```

**Verification:**
- [ ] All pages use HTTPS
- [ ] HTTP automatically redirects to HTTPS
- [ ] Using valid certificate from trusted CA
- [ ] TLS 1.2 or 1.3 enforced
- [ ] Strong cipher suites configured

---

## 7.2 HTTP Strict Transport Security (HSTS)

**Definition:**
HTTP header that forces browsers to use HTTPS for all future requests.

**How It Works:**

```
// Server sends header
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

// Browser remembers for 1 year (31536000 seconds)
// All future requests to this domain use HTTPS automatically
// Applies to subdomains too
```

**Why Critical:**
- Prevents SSL stripping attacks
- Prevents users from clicking through certificate warnings
- Enforces HTTPS even if user types http://

**Implementation:**

```
// Apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

// Nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

// Express.js
const helmet = require('helmet')
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}))
```

**HSTS Preload List:**
```
// Submit domain to hstspreload.org
// Browsers will enforce HTTPS even on first visit
// Cannot be easily reversed (choose carefully)
```

**Verification:**
- [ ] HSTS header set with max-age >= 1 year
- [ ] includeSubDomains directive included
- [ ] preload directive included (if eligible)
- [ ] Submitted to HSTS preload list (optional but recommended)

---

## 7.3 Encryption at Rest and in Transit

**Encryption in Transit (HTTPS - covered in 7.1):**
- Protects data while moving between client and server
- Uses TLS/SSL

**Encryption at Rest:**
- Protects data while stored on disk
- Protects against physical theft or unauthorized access

**What to Encrypt at Rest:**

**1. Databases:**
```
// PostgreSQL
ALTER SYSTEM SET ssl = on;

// MySQL
ssl_ca=/path/to/ca.pem
ssl_cert=/path/to/server-cert.pem
ssl_key=/path/to/server-key.pem

// MongoDB
security:
  enableEncryption: true
  encryptionKeyFile: /path/to/keyfile
```

**2. File Storage:**
```
// Encrypt sensitive files before storing
// Use AES-256-GCM or ChaCha20-Poly1305

import cryptography
cipher = Fernet(encryption_key)
encrypted_data = cipher.encrypt(file_data)
storage.save(encrypted_data)
```

**3. Backups:**
```
// Encrypt all backups
tar -czf - /data | openssl enc -aes-256-cbc -out backup.tar.gz.enc
```

**4. Cloud Storage:**
```
// Enable encryption in cloud providers
// AWS S3: Server-Side Encryption (SSE-S3, SSE-KMS)
// Google Cloud Storage: Customer-managed encryption keys
// Azure Blob Storage: Customer-managed keys
```

**Field-Level Encryption:**
```
// Encrypt specific sensitive fields in database
// Examples: credit card, SSN, passwords

CREATE TABLE users (
  id INT,
  email VARCHAR(255),
  password_hash VARCHAR(255),
  credit_card BYTEA  -- Encrypted
);
```

**Verification:**
- [ ] Database encryption enabled
- [ ] Sensitive files encrypted
- [ ] Backups encrypted
- [ ] Cloud storage encryption enabled
- [ ] Sensitive database fields encrypted
