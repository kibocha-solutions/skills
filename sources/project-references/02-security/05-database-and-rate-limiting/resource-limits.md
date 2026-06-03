# Resource Consumption Limits

**OWASP API Security Top 10 (2023): API04:2023 - Unrestricted Resource Consumption**

## The Problem

Applications that don't limit resource consumption expose themselves to denial of service attacks and cost exploitation through excessive CPU, memory, disk, network, or execution time usage.

**Attack Scenario:**

```python
# Vulnerable endpoint - no limits
@app.route('/api/export', methods=['POST'])
def export_data():
    user_ids = request.json['user_ids']  # No limit on array size
    
    # Attacker sends 10 million user IDs
    for user_id in user_ids:  # Runs for hours, consumes all memory
        data = fetch_user_data(user_id)
        export.add(data)
    
    return export.generate()  # Server crashes before completing
```

## Why Critical

- **Denial of Service**: Service unavailable for legitimate users
- **Cost Explosion**: Cloud bills skyrocket from resource usage
- **System Instability**: Out of memory, disk full, CPU exhaustion
- **Cascading Failures**: One overloaded service brings down others

**CVSS Score**: 7.5 (HIGH)

---

## Resource Exhaustion Vectors

### 1. Memory Exhaustion

```python
# VULNERABLE - Unlimited memory allocation
@app.route('/api/process-image', methods=['POST'])
def process_image():
    image_data = request.data  # No size limit
    image = Image.open(BytesIO(image_data))  # Loads entire image into memory
    # 10GB image = server crash
```

### 2. CPU Exhaustion

```javascript
// VULNERABLE - Expensive operations without limits
app.post('/api/hash-password', (req, res) => {
  const iterations = req.body.iterations || 100000;
  // Attacker sends iterations=999999999
  const hash = pbkdf2Sync(password, salt, iterations, 64, 'sha512');
});
```

### 3. Disk Exhaustion

```php
// VULNERABLE - Unlimited file uploads
if ($_FILES['file']['size'] <= PHP_INT_MAX) {  // Effectively no limit
    move_uploaded_file($_FILES['file']['tmp_name'], $destination);
}
```

### 4. Network Bandwidth Exhaustion

```python
# VULNERABLE - Unlimited download size
@app.route('/api/export/csv')
def export_csv():
    # Attacker exports entire database
    all_records = User.query.all()  # Could be millions
    return generate_csv(all_records)
```

### 5. Execution Time Exhaustion

```ruby
# VULNERABLE - No timeout
def generate_report(user_id)
  # Complex aggregation that could run forever
  Report.generate_comprehensive_analysis(user_id)
end
```

---

## Prevention Strategies (Defense in Depth)

### Strategy 1: Request Size Limits

**Limit incoming request size:**

```python
# [APPROVED] Flask with max content length
from flask import Flask

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.content_length > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({'error': 'File too large'}), 413
    # Process file
```

```javascript
// [APPROVED] Express with body-parser limits
const express = require('express');
const bodyParser = require('body-parser');

app.use(bodyParser.json({ limit: '1mb' }));
app.use(bodyParser.urlencoded({ limit: '1mb', extended: true }));
```

```nginx
# [APPROVED] Nginx reverse proxy limits
client_max_body_size 10M;
client_body_timeout 30s;
```

---

### Strategy 2: Pagination (Mandatory for Lists)

**Never return unlimited results:**

```python
# [REJECTED] VULNERABLE - Returns all records
@app.route('/api/users')
def get_users():
    users = User.query.all()  # Could be millions
    return jsonify(users)

# [APPROVED] SAFE - Paginated results
@app.route('/api/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)  # Max 100
    
    pagination = User.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'users': [u.to_dict() for u in pagination.items],
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })
```

```javascript
// [APPROVED] Node.js pagination
app.get('/api/products', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);  // Max 100
  const offset = (page - 1) * limit;
  
  const products = await Product.findAndCountAll({
    limit,
    offset
  });
  
  res.json({
    data: products.rows,
    pagination: {
      page,
      limit,
      total: products.count,
      pages: Math.ceil(products.count / limit)
    }
  });
});
```

---

### Strategy 3: Timeout Limits

**Enforce maximum execution time:**

```python
# [APPROVED] Function timeout decorator
import signal
from functools import wraps

class TimeoutError(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError(f'Function exceeded {seconds}s timeout')
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator

@timeout(30)  # Max 30 seconds
def expensive_operation(data):
    return process_data(data)
```

```javascript
// [APPROVED] Promise with timeout
function withTimeout(promise, timeoutMs) {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Operation timed out')), timeoutMs)
    )
  ]);
}

app.post('/api/process', async (req, res) => {
  try {
    const result = await withTimeout(
      expensiveOperation(req.body),
      30000  // 30 second timeout
    );
    res.json(result);
  } catch (error) {
    if (error.message.includes('timed out')) {
      return res.status(408).json({ error: 'Request timeout' });
    }
    throw error;
  }
});
```

---

### Strategy 4: Memory Limits

**Limit memory consumption:**

```python
# [APPROVED] Streaming large files instead of loading into memory
from flask import Response

@app.route('/api/export/csv')
def export_csv():
    def generate():
        # Stream results instead of loading all into memory
        for chunk in User.query.yield_per(1000):
            for user in chunk:
                yield f"{user.id},{user.name},{user.email}\n"
    
    return Response(
        generate(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=users.csv'}
    )
```

```javascript
// [APPROVED] Node.js streaming
const stream = require('stream');

app.get('/api/export/json', (req, res) => {
  const readStream = new stream.Readable({
    read() {}
  });
  
  res.setHeader('Content-Type', 'application/json');
  readStream.pipe(res);
  
  // Stream results instead of loading all into memory
  User.findAll({ raw: true })
    .then(users => {
      readStream.push('[');
      users.forEach((user, index) => {
        readStream.push(JSON.stringify(user));
        if (index <users.length - 1) readStream.push(',');
      });
      readStream.push(']');
      readStream.push(null);
    });
});
```

```dockerfile
# [APPROVED] Docker memory limits
FROM node:18-alpine

# Limit container memory
RUN echo 'node --max-old-space-size=512 app.js' > start.sh

CMD ["sh", "start.sh"]
```

---

### Strategy 5: Rate Limiting (Per Resource)

**Different limits for different resource intensities:**

```python
# [APPROVED] Tiered rate limiting
from functools import wraps

def rate_limit(max_requests, window_seconds, resource_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"ratelimit:{resource_type}:{request.remote_addr}"
            
            current = redis.get(key)
            if current and int(current) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            redis.incr(key)
            redis.expire(key, window_seconds)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Light endpoint: 1000 requests/hour
@app.route('/api/ping')
@rate_limit(1000, 3600, 'light')
def ping():
    return jsonify({'status': 'ok'})

# Heavy endpoint: 10 requests/hour
@app.route('/api/export/full')
@rate_limit(10, 3600, 'heavy')
def export_full():
    return generate_export()
```

---

### Strategy 6: Input Validation Limits

**Validate array/collection sizes:**

```python
# [APPROVED] Validate collection sizes
from marshmallow import Schema, fields, validate, ValidationError

class BulkOperationSchema(Schema):
    user_ids = fields.List(
        fields.Integer(),
        required=True,
        validate=validate.Length(min=1, max=100)  # Max 100 items
    )

@app.route('/api/users/bulk-update', methods=['POST'])
def bulk_update():
    schema = BulkOperationSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Safe to process (max 100 users)
    for user_id in data['user_ids']:
        update_user(user_id)
```

```javascript
// [APPROVED] Validate array size
const Joi = require('joi');

const bulkSchema = Joi.object({
  userIds: Joi.array()
    .items(Joi.number().integer())
    .min(1)
    .max(100)  // Max 100 items
    .required()
});

app.post('/api/bulk-delete', (req, res) => {
  const { error, value } = bulkSchema.validate(req.body);
  
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }
  
  // Safe to process
  value.userIds.forEach(id => deleteUser(id));
});
```

---

### Strategy 7: Connection Pooling

**Limit concurrent database connections:**

```python
# [APPROVED] SQLAlchemy connection pool limits
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=10,          # Maximum 10 connections
    max_overflow=20,       # Allow 20 overflow connections
    pool_timeout=30,       # Wait max 30s for connection
    pool_recycle=3600      # Recycle connections after 1 hour
)
```

```javascript
// [APPROVED] PostgreSQL connection pool
const { Pool } = require('pg');

const pool = new Pool({
  max: 20,                 // Maximum 20 connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000  // Wait max 2s for connection
});
```

---

### Strategy 8: Async Task Queues for Heavy Operations

**Offload expensive operations to background workers:**

```python
# [APPROVED] Celery for async processing
from celery import Celery

celery = Celery('myapp', broker='redis://localhost:6379')

@celery.task(time_limit=300, soft_time_limit=240)  # Hard limit 5min
def generate_report(user_id):
    # Expensive operation runs in background
    report = Report.generate(user_id)
    send_email(user_id, report)

@app.route('/api/reports/generate', methods='POST'])
def request_report():
    user_id = request.json['user_id']
    
    # Queue task instead of running synchronously
    task = generate_report.delay(user_id)
    
    return jsonify({
        'task_id': task.id,
        'status_url': f'/api/tasks/{task.id}/status'
    }), 202  # Accepted
```

---

## Container and Infrastructure Limits

```yaml
# [APPROVED] Kubernetes resource limits
apiVersion: v1
kind: Pod
metadata:
  name: api-server
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"  # Hard limit
        cpu: "500m"       # Hard limit
```

```dockerfile
# [APPROVED] Docker resource limits
docker run \
  --memory="512m" \
  --cpus="0.5" \
  --pids-limit=100 \
  myapp:latest
```

---

## Verification Checklist

- [ ] Request body size limited (e.g., 10MB max)
- [ ] File upload size limited
- [ ] All list endpoints paginated (max 100 items per page)
- [ ] Timeout limits on all operations (e.g., 30s max)
- [ ] Memory limits configured (streaming for large data)
- [ ] Rate limiting per resource intensity
- [ ] Array/collection input sizes validated
- [ ] Database connection pools configured
- [ ] Heavy operations moved to async queues
- [ ] Container memory/CPU limits set
- [ ] Automated alerts for resource thresholds
- [ ] Load testing performed

---

## Real-World Examples

**GitHub (2021)**: API rate limiting prevented large-scale scraping attacks

**AWS (Ongoing)**: S3 request rate limits prevent abuse and ensure fair usage

---

## References

- OWASP API Security Top 10 (2023): API04:2023 - Unrestricted Resource Consumption
- NIST SP 800-53: SC-5 (Denial of Service Protection)
- Cloud provider limits (AWS, Azure, GCP quotas)
