# Security Misconfiguration

**OWASP API Security Top 10 (2023): API08:2023 - Security Misconfiguration**  
**OWASP Top 10 2021: A05 - Security Misconfiguration**

## The Problem

Security misconfiguration occurs when security settings are not properly defined, implemented, or maintained, leaving systems vulnerable to attack through default credentials, unnecessary features, verbose errors, or missing security headers.

## Why Critical

- **Easy to exploit**: Automated scanners can find misconfigurations
- **Wide attack surface**: Affects all layers (application, framework, server, network, database)
- **Common**: Frequently overlooked in deployment checklists
- **Cascading impact**: One misconfiguration can expose multiple vulnerabilities

**CVSS Score**: 7.0-9.0 (HIGH to CRITICAL)

---

## Common Misconfigurations

### 1. Default Credentials

**Problem:** Systems deployed with default passwords

```bash
# VULNERABLE - Default credentials
Username: admin
Password: admin

# Database default credentials
Username: root
Password: (empty)

# Attacker tries common combinations and gains access
```

**Secure Configuration:**

```bash
# [APPROVED] MANDATORY - Change all default credentials
# Generate strong random passwords
openssl rand -base64 32

# Enforce password change on first login
# Store in secrets manager, never in code
```

---

### 2. Unnecessary Features Enabled

**Problem:** Unused features increase attack surface

```apache
# VULNERABLE - Apache with unnecessary modules
LoadModule status_module modules/mod_status.so
LoadModule info_module modules/mod_info.so
LoadModule autoindex_module modules/mod_autoindex.so

# Exposes server status at /server-status
# Exposes configuration at /server-info
# Enables directory listing
```

**Secure Configuration:**

```apache
# [APPROVED] Disable unnecessary modules
# LoadModule status_module modules/mod_status.so  # DISABLED
# LoadModule info_module modules/mod_info.so      # DISABLED
# LoadModule autoindex_module modules/mod_autoindex.so  # DISABLED

# Disable directory listing
Options -Indexes
```

---

### 3. Verbose Error Messages

**Problem:** Detailed errors leak system information

```python
# VULNERABLE - Production with debug mode
app = Flask(__name__)
app.config['DEBUG'] = True  # Shows stack traces to users

# Error exposes:
# - File paths (/var/www/myapp/controllers/user.py)
# - Database structure (SELECT * FROM users WHERE id = ?)
# - Library versions (Flask 2.3.0, SQLAlchemy 1.4.39)
```

**Secure Configuration:**

```python
# [APPROVED] Production configuration
import os

app = Flask(__name__)
app.config['DEBUG'] = False  # Never True in production
app.config['ENV'] = 'production'

# Custom error handler
@app.errorhandler(Exception)
def handle_error(error):
    # Log detailed error internally
    app.logger.error(f'Error: {error}', exc_info=True)
    
    # Return generic message to user
    return jsonify({
        'error': 'An error occurred',
        'error_id': generate_error_id()  # For support reference
    }), 500
```

---

### 4. Missing Security Headers

**Problem:** HTTP security headers not configured

```nginx
# VULNERABLE - No security headers
server {
    listen 80;
    server_name example.com;
}

# Missing:
# - X-Content-Type-Options
# - X-Frame-Options
# - Content-Security-Policy
# - Strict-Transport-Security
```

**Secure Configuration:**

```nginx
# [APPROVED] Security headers configured
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Prevent MIME type sniffing
    add_header X-Content-Type-Options "nosniff" always;
    
    # Prevent clickjacking
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # Enable XSS protection
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;
    
    # HSTS (HTTPS enforcement)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Referrer policy
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Permissions policy
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
}
```

---

### 5. Unnecessary HTTP Methods

**Problem:** All HTTP methods allowed

```
# VULNERABLE - All methods enabled
OPTIONS /api/users → 200 OK
Allow: GET, POST, PUT, DELETE, OPTIONS, TRACE, CONNECT

# TRACE can be used for XSS attacks
# Unnecessary methods increase attack surface
```

**Secure Configuration:**

```nginx
# [APPROVED] Limit HTTP methods
location /api {
    limit_except GET POST {
        deny all;
    }
}
```

```python
# [APPROVED] Flask - Specify allowed methods explicitly
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return get_users()
    elif request.method == 'POST':
        return create_user()
```

---

### 6. Database Configuration

**Problem:** Database lacks security configuration

```sql
-- VULNERABLE - MySQL default configuration
-- Allows remote root login
CREATE USER 'root'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';

-- No SSL/TLS enforcement
-- Binary logging disabled (no audit trail)
```

**Secure Configuration:**

```sql
-- [APPROVED] Secure database configuration
-- Application user with limited privileges
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_random_password';
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'app_user'@'localhost';
-- NO DELETE, NO ALTER, NO DROP

-- Require SSL/TLS
GRANT USAGE ON *.* TO 'app_user'@'localhost' REQUIRE SSL;

-- Enable binary logging for audit
SET GLOBAL log_bin = ON;
```

```ini
# my.cnf - MySQL configuration
[mysqld]
# Bind only to localhost (no remote access)
bind-address = 127.0.0.1

# Require SSL/TLS
require_secure_transport = ON

# Enable binary logging
log_bin = /var/log/mysql/mysql-bin.log

# Disable local file loading
local_infile = 0
```

---

### 7. CORS Misconfiguration

**Problem:** Overly permissive CORS

```javascript
// VULNERABLE - Allow all origins
app.use(cors({
  origin: '*',  // Allows any website to make requests
  credentials: true  // Sends cookies to any origin
}));
```

**Secure Configuration:**

```javascript
// [APPROVED] Restrict CORS to specific origins
const allowedOrigins = [
  'https://myapp.com',
  'https://www.myapp.com',
  'https://admin.myapp.com'
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  maxAge: 86400  // Cache preflight for 24 hours
}));
```

---

### 8. Cloud Storage Permissions

**Problem:** Public bucket access

```bash
# VULNERABLE - AWS S3 bucket publicly readable
aws s3api put-bucket-acl --bucket my-bucket --acl public-read

# All files accessible to anyone
# https://my-bucket.s3.amazonaws.com/sensitive-data.pdf
```

**Secure Configuration:**

```bash
# [APPROVED] Private bucket with signed URLs
aws s3api put-bucket-acl --bucket my-bucket --acl private

# Block public access
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Generate temporary signed URLs for authorized access
aws s3 presign s3://my-bucket/file.pdf --expires-in 3600
```

---

### 9. SSL/TLS Configuration

**Problem:** Weak ciphers and protocols

```apache
# VULNERABLE - Allows weak ciphers
SSLProtocol all
SSLCipherSuite ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP

# Allows TLS 1.0, TLS 1.1 (deprecated)
# Allows weak ciphers (RC4, MD5)
```

**Secure Configuration:**

```apache
# [APPROVED] Strong TLS configuration
# Only TLS 1.2 and 1.3
SSLProtocol -all +TLSv1.2 +TLSv1.3

# Strong ciphers only
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder on

# Enable OCSP stapling
SSLUseStapling on
SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"
```

---

## Hardening Checklist

### Application Layer

- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Unnecessary features/modules disabled
- [ ] Error messages generic (no stack traces)
- [ ] Security headers configured
- [ ] HTTP methods limited to necessary
- [ ] CORS properly configured

### Framework Layer

- [ ] Framework version up-to-date
- [ ] Unused dependencies removed
- [ ] Security middleware enabled (helmet.js, etc.)
- [ ] Session configuration secure (HttpOnly, Secure, SameSite)
- [ ] File upload limits configured

### Server Layer

- [ ] Web server version hidden
- [ ] Directory listing disabled
- [ ] Default pages removed
- [ ] Server status endpoints disabled
- [ ] Access logs enabled
- [ ] Rate limiting configured

### Database Layer

- [ ] Application user has minimal privileges
- [ ] Root access disabled remotely
- [ ] SSL/TLS required
- [ ] Binary logging enabled
- [ ] Bind to localhost only
- [ ] Default port changed (security by obscurity as extra layer)

### Network Layer

- [ ] Firewall configured (only necessary ports)
- [ ] SSL/TLS 1.3 or 1.2 minimum
- [ ] Strong cipher suites only
- [ ] HTTPS enforced (HTTP redirects to HTTPS)
- [ ] HSTS headers configured

### Cloud/Infrastructure

- [ ] S3 buckets/blob storage private
- [ ] IAM roles with least privilege
- [ ] Secrets in secrets manager (not environment variables)
- [ ] Security groups restrictive
- [ ] Logging and monitoring enabled

---

## Automated Security Scanning

**Tools to detect misconfigurations:**

```bash
# [APPROVED] Security scanners

# Test SSL/TLS configuration
testssl.sh https://myapp.com

# Test HTTP security headers
curl -I https://myapp.com | grep -E "X-|Strict|Content-Security"

# AWS security audit
aws-vault exec prod -- prowler

# Docker security scanning
docker scan myimage:latest

# Kubernetes security
kube-bench run --targets=master,node,etcd,policies
```

---

## Verification Checklist

- [ ] No default credentials in use
- [ ] Debug mode disabled in production
- [ ] All security headers configured
- [ ] CORS properly restricted
- [ ] HTTP methods limited
- [ ] SSL/TLS properly configured (TLS 1.2+ only)
- [ ] Database credentials secured
- [ ] Cloud storage private
- [ ] Error messages generic
- [ ] Unnecessary features disabled
- [ ] Automated security scanning enabled
- [ ] Regular security audits performed

---

## Real-World Examples

**MongoDB (2017)**: 27,000+ publicly accessible MongoDB databases due to default configuration (no authentication).

**Capital One (2019)**: Misconfigured AWS WAF allowed SSRF, leading to 100M+ customer records stolen.

---

## References

- OWASP API Security Top 10 (2023): API08:2023
- OWASP Top 10 2021: A05 - Security Misconfiguration
- CIS Benchmarks (Center for Internet Security)
- NIST SP 800-123: Guide to General Server Security
