# Multi-Factor Authentication (MFA)

**Definition:**
Requiring two or more independent credentials for authentication.

**Factor Types:**
1. **Something you know** (password, PIN)
2. **Something you have** (phone, hardware token, authenticator app)
3. **Something you are** (fingerprint, face recognition, iris scan)

**Why Critical:**
- Passwords alone are insufficient (easily stolen, phished, guessed)
- MFA reduces account takeover by 99.9%
- Required for PCI DSS compliance (March 31, 2025)
- Required for high-value transactions and administrative access

**Implementation Options:**

**SMS-Based (LEAST SECURE):**
- Easy to implement
- Vulnerable to SIM swapping
- Vulnerable to interception
- Use only as fallback

**Authenticator Apps (RECOMMENDED):**
- Time-based One-Time Passwords (TOTP)
- Apps: Google Authenticator, Authy, Microsoft Authenticator
- More secure than SMS
- Works offline

**Hardware Tokens (MOST SECURE):**
- YubiKey, Titan Security Key
- Phishing-resistant
- Recommended for high-privilege accounts

**Biometric (CONTEXT-DEPENDENT):**
- Fingerprint, face recognition
- Good for mobile devices
- Cannot be changed if compromised

**When to Require MFA:**
- Login to administrative accounts (MANDATORY)
- Access to sensitive data (MANDATORY)
- Payment processing (MANDATORY for PCI DSS)
- Password changes
- Account recovery
- Adding new devices

**Implementation Requirements:**
- Offer multiple MFA options
- Allow backup codes for account recovery
- Enforce MFA for admin accounts (no exceptions)
- Log all MFA attempts (success and failure)
- Alert on repeated MFA failures

**Verification:**
- [ ] MFA required for administrative access
- [ ] MFA required for sensitive operations
- [ ] Multiple MFA methods offered
- [ ] Backup codes provided
- [ ] MFA attempts logged
