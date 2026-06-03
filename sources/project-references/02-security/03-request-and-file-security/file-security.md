# File and Upload Security

## 5.1 File Upload Security

**The Problem:**
Unrestricted file uploads allow attackers to upload malicious files.

**Attack Scenarios:**
- Upload web shell (malicious_file.php) → execute arbitrary code
- Upload malware → spread to other users
- Upload oversized file → denial of service
- Upload file with dangerous extension → bypass filters

**Prevention Strategies:**

**1. Validate File Type (Multiple Layers):**

**Extension Check (WEAK, easily bypassed):**
```
allowed_extensions = [".jpg", ".png", ".pdf"]
if file.extension not in allowed_extensions:
  reject()
```

**MIME Type Check (BETTER, but can be spoofed):**
```
allowed_mimes = ["image/jpeg", "image/png", "application/pdf"]
if file.mime_type not in allowed_mimes:
  reject()
```

**Magic Bytes Check (BEST):**
```
// Read file header to verify actual file type
file_signatures = {
  "image/jpeg": ["FF D8 FF"],
  "image/png": ["89 50 4E 47"],
  "application/pdf": ["25 50 44 46"]
}

if file_header not in allowed_signatures:
  reject()
```

**2. File Size Limits:**

```
max_file_size = 5 * 1024 * 1024  // 5MB

if file.size > max_file_size:
  reject()
```

**3. Rename Uploaded Files:**

```
// NEVER use original filename
original_name = "malicious.php.jpg"
safe_name = generate_uuid() + ".jpg"  // "a7f3c2d8-b1e9.jpg"

// Store mapping in database if original name needed
```

**4. Store Outside Web Root:**

```
// BAD
/var/www/html/uploads/file.pdf  // Directly accessible

// GOOD
/var/app/storage/uploads/a7f3c2d8-b1e9.pdf  // Not directly accessible
```

**5. Scan for Malware:**

```
// Use antivirus scanning library
scan_result = antivirus.scan(uploaded_file)
if scan_result != "clean":
  reject()
  alert_security_team()
```

**6. Disable Script Execution in Upload Directory:**

```
// Apache .htaccess in uploads directory
<FilesMatch "\.ph(p[3-7]?|tml)$">
  Deny from all
</FilesMatch>

// Nginx config
location /uploads {
  location ~ \.php$ {
    deny all;
  }
}
```

**7. Use CDN/Object Storage:**

```
Store uploads in AWS S3, Google Cloud Storage, Azure Blob
Separate from application server
Cannot execute code
```

**Verification:**
- [ ] File type validated by magic bytes
- [ ] File size limited
- [ ] Files renamed to safe names
- [ ] Uploads stored outside web root
- [ ] Malware scanning implemented
- [ ] Antivirus scanning enabled on upload
- [ ] Quarantine suspicious files

---

## 5.2 Path Traversal / Directory Traversal Prevention

**CRITICAL SECURITY VULNERABILITY - OWASP Top 10**

**The Problem:**
Attackers manipulate file paths using special sequences (like `../`) to access files outside the intended directory, potentially gaining access to system files, configuration files, source code, or other users' data.

**Example Attack:**

```
Normal Request:
GET /download?file=tax-report.pdf

Malicious Request:
GET /download?file=../../etc/passwd
GET /download?file=../../../app/.env
GET /download?file=../../../../var/www/config/database.yml
```

**What Gets Exposed:**
- System files: `/etc/passwd`, `/etc/shadow`, system logs
- Application secrets: `.env` files, database credentials, API keys
- Source code: Application logic, proprietary algorithms
- User data: Other users' files, financial records, personal information

**Result:** Complete server compromise.

---

**Attack Vectors:**

1. **URL Parameters:**
   ```
   ?file=../../secret.txt
   ?document=../../../../../etc/passwd
   ```

2. **Form Inputs:**
   ```html
   <input name="document" value="../../../.env">
   ```

3. **API Requests:**
   ```json
   {"filename": "../../../../config/database.yml"}
   ```

4. **HTTP Headers:**
   ```
   X-Filename: ../../../etc/shadow
   ```

---

**Prevention Strategies (Defense in Depth):**

### Strategy 1: Avoid User-Controlled Paths (PREFERRED)

[APPROVED] **Best Practice:** Don't let users specify file paths at all.

```typescript
// [REJECTED] VULNERABLE: User controls file path
app.get('/download', (req, res) => {
  const fileName = req.query.file;  // User input!
  res.sendFile(`/uploads/${fileName}`);  // DANGER
});

// [APPROVED] SECURE: Use file IDs instead
app.get('/download/:fileId', async (req, res) => {
  const fileId = req.params.fileId;
  
  // Get actual filename from database
  const file = await db.files.findOne({ 
    id: fileId,
    userId: req.user.id  // Authorization check!
  });
  
  if (!file) return res.status(404).send('Not found');
  
  // User never controls the path
  res.sendFile(file.storedPath);
});
```

---

### Strategy 2: Path Resolution and Validation (REQUIRED if accepting filenames)

**Node.js/TypeScript:**

```typescript
import path from 'path';
import fs from 'fs/promises';

// Define base directory (absolute path)
const BASE_DIRECTORY = path.resolve(__dirname, 'public/uploads');

export const downloadFile = async (req, res, next) => {
  const fileName = req.query.file;
  
  if (!fileName) {
    return res.status(400).json({ message: 'File name required' });
  }
  
  // Construct full path
  const requestedPath = path.join(BASE_DIRECTORY, fileName);
  
  // CRITICAL - Resolve to absolute path
  const resolvedPath = path.resolve(requestedPath);
  
  // CRITICAL - Verify path is inside base directory
  if (!resolvedPath.startsWith(BASE_DIRECTORY)) {
    console.error(`Path traversal attempt: ${fileName}`);
    return res.status(400).json({ message: 'Invalid file path' });
  }
  
  try {
    // Verify file exists
    await fs.access(resolvedPath);
    
    // Authorization check
    const file = await db.files.findOne({
      path: resolvedPath,
      userId: req.user.id
    });
    
    if (!file) {
      return res.status(403).json({ message: 'Access denied' });
    }
    
    // Safe to serve
    res.download(resolvedPath, path.basename(fileName));
    
  } catch (error) {
    return res.status(404).json({ message: 'File not found' });
  }
};
```

**Python:**

```python
import os
from pathlib import Path

BASE_DIRECTORY = Path('/var/app/uploads').resolve()

def download_file(request):
    file_name = request.GET.get('file')
    
    if not file_name:
        return JsonResponse({'error': 'File required'}, status=400)
    
    # Construct path
    requested_path = BASE_DIRECTORY / file_name
    
    # Resolve to absolute path
    resolved_path = requested_path.resolve()
    
    # CRITICAL: Verify within base directory
    if not resolved_path.is_relative_to(BASE_DIRECTORY):
        logger.error(f'Path traversal attempt: {file_name}')
        return JsonResponse({'error': 'Invalid path'}, status=400)
    
    # Verify exists
    if not resolved_path.exists():
        return JsonResponse({'error': 'Not found'}, status=404)
    
    # Authorization check
    file = File.objects.filter(
        path=str(resolved_path),
        user_id=request.user.id
    ).first()
    
    if not file:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    return FileResponse(open(resolved_path, 'rb'))
```

---

### Strategy 3: Input Validation

**Block Dangerous Characters:**

```javascript
function isPathSafe(fileName) {
  // Reject if contains path traversal sequences
  const dangerousPatterns = [
    /\.\./,          // ..
    /\.\.\\/,        // ..\
    /\.\.\//,        // ../
    /^\/+/,          // Absolute paths
    /^[A-Za-z]:/,    // Windows drive letters
    /[<>:"|?*\x00-\x1f]/  // Invalid filename chars
  ];
  
  return !dangerousPatterns.some(pattern => pattern.test(fileName));
}

app.get('/download', (req, res) => {
  const fileName = req.query.file;
  
  if (!isPathSafe(fileName)) {
    console.error(`Dangerous file path: ${fileName}`);
    return res.status(400).send('Invalid filename');
  }
  
  // Continue with path resolution and validation...
});
```

**Whitelist Allowed Characters:**

```javascript
// Only allow alphanumeric, dash, underscore, dot
const SAFE_FILENAME_REGEX = /^[a-zA-Z0-9._-]+$/;

if (!SAFE_FILENAME_REGEX.test(fileName)) {
  return res.status(400).send('Invalid filename format');
}
```

---

### Strategy 4: Allowlist Approach (When Possible)

```javascript
// Allowlist of permitted files
const ALLOWED_FILES = new Set([
  'user-guide.pdf',
  'tax-form-2024.pdf',
  'filing-instructions.pdf'
]);

app.get('/download', (req, res) => {
  const fileName = req.query.file;
  
  // Reject if not in allowlist
  if (!ALLOWED_FILES.has(fileName)) {
    return res.status(403).send('File not permitted');
  }
  
  const safePath = path.join(BASE_DIR, fileName);
  res.sendFile(safePath);
});
```

---

### Strategy 5: Authorization Check (MANDATORY)

**Every file access MUST verify user owns the file:**

```sql
-- Verify user owns the file
SELECT * FROM files 
WHERE id = ? AND user_id = ?
```

```javascript
// Application code
const file = await db.files.findOne({
  id: fileId,
  userId: req.user.id
});

if (!file) {
  return res.status(403).json({ message: 'Access denied' });
}
```

---

### Strategy 6: Filesystem Isolation

**Store files outside web root:**

```
Project Structure:
/var/www/app/          (web root)
  ├── public/
  ├── src/
  └── ...

/var/app-data/        (outside web root)
  └── uploads/        (not directly accessible via web)
```

**Use chroot jails or containers:**

```dockerfile
# Docker container example
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY src/ ./src/
COPY uploads/ /data/uploads/

# Run as non-root user
USER node

# Application can only access /app and /data
```

---

### Strategy 7: Least Privilege File Permissions

```bash
# Upload directory: read-only for application
chmod 755 /var/app/uploads
chown root:appuser /var/app/uploads

# Application runs as 'appuser' without write access to system files
```

---

### Strategy 8: Monitoring and Logging

```javascript
function logFileAccess(userId, fileName, ipAddress, allowed) {
  auditLog.write({
    timestamp: new Date(),
    userId,
    fileName,
    ipAddress,
    allowed,
    type: 'FILE_ACCESS'
  });
  
  // Alert on suspicious patterns
  if (!allowed && fileName.includes('..')) {
    securityAlert.send({
      severity: 'HIGH',
      type: 'PATH_TRAVERSAL_ATTEMPT',
      userId,
      fileName,
      ipAddress
    });
  }
}
```

---

**Complete Secure Example:**

```typescript
import path from 'path';
import fs from 'fs/promises';

const BASE_DIRECTORY = path.resolve(__dirname, '../uploads');

// Validation utilities
function isPathSafe(fileName: string): boolean {
  const dangerousPatterns = [/\.\./, /^\//, /^[A-Za-z]:/, /[\x00-\x1f]/];
  return !dangerousPatterns.some(p => p.test(fileName));
}

function validatePath(userInput: string, baseDir: string): string {
  if (!isPathSafe(userInput)) {
    throw new Error('Invalid filename format');
  }
  
  const resolved = path.resolve(path.join(baseDir, userInput));
  
  if (!resolved.startsWith(baseDir)) {
    throw new Error('Path traversal detected');
  }
  
  return resolved;
}

// Secure file download endpoint
export const secureDownload = async (req, res) => {
  try {
    const fileId = req.params.fileId;
    
    // Get file metadata from database
    const file = await db.files.findOne({
      id: fileId,
      userId: req.user.id  // Authorization
    });
    
    if (!file) {
      logFileAccess(req.user.id, fileId, req.ip, false);
      return res.status(404).json({ error: 'File not found' });
    }
    
    // Validate path
    const safePath = validatePath(file.filename, BASE_DIRECTORY);
    
    // Verify file exists
    await fs.access(safePath);
    
    // Log successful access
    logFileAccess(req.user.id, file.filename, req.ip, true);
    
    // Serve file
    res.download(safePath, file.originalName);
    
  } catch (error) {
    if (error.message.includes('Path traversal')) {
      logFileAccess(req.user.id, req.params.fileId, req.ip, false);
      return res.status(400).json({ error: 'Invalid file path' });
    }
    
    return res.status(500).json({ error: 'Internal server error' });
  }
};
```

---

**Verification Checklist:**

- [ ] Users cannot control file paths directly (use IDs/UUIDs)
- [ ] If accepting filenames, path resolution validates within base directory
- [ ] Input validation blocks `..`, `/`, `\`, null bytes
- [ ] Whitelist validation for allowed characters
- [ ] Authorization check verifies user owns file
- [ ] Files stored outside web root
- [ ] Application runs with minimal filesystem permissions
- [ ] File access attempts logged
- [ ] Alerts configured for traversal attempts
- [ ] Error messages don't reveal file structure
- [ ] Automated testing includes path traversal tests

---

**Testing for Path Traversal:**

```javascript
// Security test cases
describe('Path Traversal Protection', () => {
  const attacks = [
    '../../../etc/passwd',
    '..\\..\\..\\windows\\system32\\config\\sam',
    '....//....//....//etc/passwd',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',  // URL encoded
    '..;/..;/..;/etc/passwd',
    '/etc/passwd',
    'C:\\Windows\\System32\\config\\sam'
  ];
  
  attacks.forEach(attack => {
    it(`should block: ${attack}`, async () => {
      const response = await request(app)
        .get(`/download?file=${encodeURIComponent(attack)}`)
        .expect(400);
      
      expect(response.body.error).toMatch(/invalid|forbidden/i);
    });
  });
});
```

---

**Severity Assessment:**

**CVSS Score: 9.1 (CRITICAL)**

**Why Critical:**
- Easy to exploit (no special tools needed)
- High impact (complete system access possible)
- Common vulnerability (OWASP Top 10)
- Affects most applications with file operations
- Difficult to detect without proper logging

**This vulnerability is as serious as SQL Injection.**
