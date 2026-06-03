# Canon: Documentation Deployment

## Purpose

This canon defines standards for deploying technical documentation to hosting platforms. It covers strategies for various hosting providers (with and without SDKs), access control, CDN configuration, build automation, and deployment workflows.

---

## Scope

**This canon applies to:**
- Sphinx documentation deployment
- OpenAPI documentation deployment
- Static site documentation
- Multi-environment documentation (public/private splits)
- CI/CD for documentation

**This canon does NOT apply to:**
- Application deployment (use deployment canons)
- Database migrations
- Infrastructure as Code (IaC) for applications

---

## Access Level Classification

**Deployment Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** DevOps team, authorized developers
- **Rationale:** Contains infrastructure details, access credentials, deployment procedures

**Deployment Configurations (IaC):**
- **Access Level:** Internal (Level 2)
- **Storage:** Private Git repository

---

## Hosting Platform Strategies

### Strategy 1: Managed Documentation Platforms (With SDKs)

**Platforms:**
- Read the Docs (readthedocs.org)
- GitBook
- Netlify
- Vercel
- Cloudflare Pages

**Advantages:**
- Zero infrastructure management
- Automatic HTTPS
- CDN distribution
- Preview deployments
- OAuth integration

**Disadvantages:**
- Vendor lock-in
- Cost scaling
- Limited customization
- Privacy concerns

**When to Use:**
- Small to medium documentation projects
- Open source projects
- Need fast deployment
- Limited DevOps resources

---

### Strategy 2: Generic Hosting Platforms (Without SDKs)

**Platforms:**
- AWS S3 + CloudFront
- Google Cloud Storage + CDN
- Azure Blob Storage + CDN
- DigitalOcean Spaces
- Self-hosted web servers (Nginx, Apache)

**Advantages:**
- Full control
- Cost efficiency at scale
- No vendor documentation platform lock-in
- Custom domain configuration

**Disadvantages:**
- Manual configuration
- Infrastructure management
- Security responsibility
- CI/CD setup required

**When to Use:**
- Large documentation projects
- Enterprise compliance requirements
- Multi-region deployment
- Custom access control needs

---

### Strategy 3: Hybrid Approach

**Configuration:**
- Public documentation: Managed platform (Cloudflare Pages)
- Private documentation: Self-hosted with authentication (AWS S3 + CloudFront + Lambda@Edge)

**Advantages:**
- Cost-effective for public content
- Security control for private content
- Flexibility

**Disadvantages:**
- Split management
- Dual CI/CD pipelines

---

## Deployment Patterns

### Pattern 1: Single Environment (Public Only)

**Use Case:** Open source projects, public documentation

```
Source (Git) → Build (Sphinx) → Deploy (Cloudflare Pages) → Public URL
```

**Build Configuration:**

```python
# conf.py
project = 'My Project'
html_theme = 'furo'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
```

**Deployment:**

```bash
# Build
make html

# Deploy (Cloudflare Pages)
npx wrangler pages deploy _build/html --project-name=my-docs-public
```

---

### Pattern 2: Split Environment (Public + Private)

**Use Case:** Commercial products with internal documentation

```
Source (Git) → Build Public → Deploy to docs.example.com/
            ↘ Build Private → Deploy to docs.example.com/private/ (Auth Required)
```

**Build Configuration:**

```python
# public-conf.py
exclude_patterns = ['admin/**', 'security/**', '**/private/**']

# private-conf.py
exclude_patterns = ['_build']
include_patterns = ['admin/**', 'security/**']
```

**Makefile:**

```makefile
.PHONY: public private all

public:
	sphinx-build -c public-conf.py -b html . _build/public

private:
	sphinx-build -c private-conf.py -b html . _build/private

all: public private
```

---

### Pattern 3: Multi-Region Deployment

**Use Case:** Global audience, compliance requirements

```
Source → Build → Deploy US Region → CloudFront (us-east-1)
              ↘ Deploy EU Region → CloudFront (eu-west-1)
              ↘ Deploy APAC Region → CloudFront (ap-southeast-1)
```

**Routing:**
- GeoDNS (Route 53, Cloudflare)
- Latency-based routing
- Compliance-based routing (GDPR data residency)

---

## Platform-Specific Implementations

### Cloudflare Pages (Managed, With SDK)

**Prerequisites:**

```bash
npm install -g wrangler
wrangler login
```

**Configuration:**

```toml
# wrangler.toml
name = "my-docs"
compatibility_date = "2024-01-01"

[build]
command = "make html"
cwd = "."
watch_dirs = ["docs"]

[build.upload]
format = "service-worker"
dir = "_build/html"
```

**Deployment:**

```bash
# Manual deployment
wrangler pages deploy _build/html --project-name=my-docs

# Automatic deployment (push to main branch)
git push origin main
```

**Custom Domain:**

```bash
# Add custom domain
wrangler pages project create my-docs
wrangler pages deploy _build/html --project-name=my-docs

# In Cloudflare Dashboard:
# Pages > my-docs > Custom domains > Add domain
# Enter: docs.example.com
```

**Authentication (Cloudflare Access):**

```bash
# Navigate to Cloudflare Dashboard
# Zero Trust > Access > Applications > Add an application

# Application Configuration:
Application Name: Private Documentation
Domain: docs.example.com
Path: /private/*
Policy: Allow with Google OAuth (email: user@example.com)
Session Duration: 24 hours
```

---

### AWS S3 + CloudFront (Generic, Without SDK)

**Prerequisites:**

```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region
```

**S3 Bucket Setup:**

```bash
# Create bucket
aws s3 mb s3://docs-example-com --region us-east-1

# Enable static website hosting
aws s3 website s3://docs-example-com \
  --index-document index.html \
  --error-document 404.html

# Set bucket policy (public read)
cat > bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::docs-example-com/*"
  }]
}
EOF

aws s3api put-bucket-policy \
  --bucket docs-example-com \
  --policy file://bucket-policy.json
```

**CloudFront Distribution:**

```bash
# Create distribution (via AWS Console or CLI)
aws cloudfront create-distribution --origin-domain-name docs-example-com.s3-website-us-east-1.amazonaws.com

# Configure:
# - HTTPS only
# - Custom domain (docs.example.com)
# - Cache behavior (TTL: 1 hour)
# - Error pages (404 → /404.html)
```

**Deployment Script:**

```bash
#!/bin/bash
# deploy-docs.sh

# Build documentation
make html

# Sync to S3
aws s3 sync _build/html/ s3://docs-example-com/ \
  --delete \
  --cache-control "max-age=3600" \
  --exclude "*.map"

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

echo "Deployment complete: https://docs.example.com"
```

**Private Documentation (Lambda@Edge):**

```javascript
// cloudfront-auth.js
exports.handler = async (event) => {
  const request = event.Records[0].cf.request;
  const uri = request.uri;

  // Check if accessing private documentation
  if (uri.startsWith('/private/')) {
    const headers = request.headers;
    const authToken = headers['x-auth-token'] ? headers['x-auth-token'][0].value : null;

    // Validate token (check against DynamoDB, JWT verification, etc.)
    if (!authToken || !isValidToken(authToken)) {
      return {
        status: '401',
        statusDescription: 'Unauthorized',
        body: 'Authentication required',
      };
    }
  }

  return request;
};

function isValidToken(token) {
  // Implement token validation logic
  // Check JWT signature, expiration, user permissions
  return true; // Placeholder
}
```

---

### Read the Docs (Managed, With SDK)

**Configuration:**

`.readthedocs.yaml`

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: conf.py
  fail_on_warning: true

python:
  install:
    - requirements: requirements.txt

formats:
  - pdf
  - epub
```

**Deployment:**

```bash
# Automatic deployment on Git push
git push origin main

# Manual deployment (via Read the Docs dashboard)
# Projects > my-project > Builds > Build Version
```

**Custom Domain:**

```bash
# In Read the Docs dashboard:
# Admin > Domains > Add Domain
# Enter: docs.example.com

# Add CNAME in DNS:
docs.example.com CNAME my-project.readthedocs.io
```

**Authentication:**

Read the Docs does not support custom authentication for private docs. Use:
- Private repositories (GitHub/GitLab)
- Read the Docs Teams (paid feature)

---

### Netlify (Managed, With SDK)

**Configuration:**

`netlify.toml`

```toml
[build]
  command = "make html"
  publish = "_build/html"

[build.environment]
  PYTHON_VERSION = "3.11"

[[redirects]]
  from = "/private/*"
  to = "/.netlify/functions/auth"
  status = 200
  force = true
```

**Deployment:**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod --dir=_build/html
```

**Authentication (Netlify Identity):**

```bash
# Enable Netlify Identity in dashboard
# Settings > Identity > Enable Identity

# Add users
# Identity > Invite users
```

**Edge Function for Auth:**

```javascript
// netlify/functions/auth.js
exports.handler = async (event, context) => {
  const { identity, clientContext } = context;

  if (!identity || !identity.user) {
    return {
      statusCode: 401,
      body: 'Unauthorized',
    };
  }

  // User authenticated, allow access
  return {
    statusCode: 200,
    body: 'Authenticated',
  };
};
```

---

### GitHub Pages (Managed, With SDK)

**Configuration:**

`.github/workflows/deploy-docs.yml`

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install sphinx furo sphinx-copybutton
      
      - name: Build documentation
        run: make html
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: _build/html
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Custom Domain:**

```bash
# Add CNAME file to docs root
echo "docs.example.com" > CNAME

# In GitHub repository settings:
# Pages > Custom domain > docs.example.com
```

**Authentication:**

GitHub Pages does not support custom authentication. Use:
- Private repositories (GitHub Pro required for Pages on private repos)
- External authentication proxy

---

## CI/CD Automation

### GitHub Actions (Recommended)

**Complete Workflow:**

`.github/workflows/docs-ci-cd.yml`

```yaml
name: Documentation CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install sphinx furo sphinx-copybutton
          pip install doc8 rstcheck
      
      - name: Validate RST syntax
        run: |
          doc8 --max-line-length 120 docs/
          rstcheck -r docs/
      
      - name: Build documentation
        run: |
          cd docs && make html
      
      - name: Check for broken links
        run: |
          cd docs && make linkcheck
  
  deploy-public:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install sphinx furo sphinx-copybutton
      
      - name: Build public documentation
        run: |
          cd docs && make public
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy _build/public --project-name=my-docs-public
  
  deploy-private:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install sphinx furo sphinx-copybutton
      
      - name: Build private documentation
        run: |
          cd docs && make private
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy _build/private --project-name=my-docs-private
```

---

## Security Best Practices

### HTTPS Enforcement

**Always enforce HTTPS:**
- Redirect HTTP to HTTPS
- HSTS headers (max-age=31536000)
- TLS 1.2+ only
- No mixed content warnings

**Cloudflare:**

```bash
# Automatic HTTPS (enabled by default)
# Dashboard > SSL/TLS > Overview > Full (strict)
# Dashboard > SSL/TLS > Edge Certificates > Always Use HTTPS: On
```

**AWS CloudFront:**

```json
{
  "ViewerProtocolPolicy": "redirect-to-https",
  "MinimumProtocolVersion": "TLSv1.2_2021"
}
```

### Access Control

**Public Documentation:**
- No authentication required
- CDN caching aggressive (1 year browser, 1 week CDN)
- No sensitive data

**Private Documentation:**
- OAuth (Google, GitHub)
- MFA recommended
- Session timeout: 24 hours
- IP allowlist (optional)
- Audit logging

### Secrets Management

**Never commit:**
- API keys
- Access tokens
- Encryption keys
- OAuth client secrets

**Use:**
- GitHub Secrets
- AWS Secrets Manager
- Cloudflare Environment Variables

**Example:**

```yaml
# .github/workflows/deploy.yml
env:
  CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

---

## Performance Optimization

### CDN Configuration

**Cache Headers:**

```
Cache-Control: public, max-age=31536000, immutable  # Static assets
Cache-Control: public, max-age=3600                 # HTML pages
Cache-Control: no-cache, must-revalidate            # Private docs
```

**Compression:**

```
Content-Encoding: br       # Brotli (best compression)
Content-Encoding: gzip     # Gzip (fallback)
```

### Build Optimization

**Sphinx:**

```python
# conf.py
# Parallel builds
numjobs = 'auto'

# Exclude unnecessary files
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**.ipynb_checkpoints',
]
```

**Image Optimization:**

```bash
# Install tools
npm install -g sharp-cli

# Optimize images
find _build/html -name "*.png" -exec sharp -i {} -o {}.optimized.png compress \;
```

---

## Monitoring and Logging

### Analytics

**Google Analytics:**

```python
# conf.py
html_theme_options = {
    "analytics": {
        "google_analytics_id": "G-XXXXXXXXXX",
    },
}
```

**Cloudflare Analytics:**
- Automatic (no configuration needed)
- Dashboard > Analytics > Web Analytics

### Error Tracking

**Sentry:**

```html
<!-- _templates/layout.html -->
<script src="https://browser.sentry-cdn.com/7.x/bundle.min.js"></script>
<script>
  Sentry.init({
    dsn: "https://xxxx@sentry.io/yyyy",
    environment: "production",
  });
</script>
```

### Uptime Monitoring

**Recommended Services:**
- UptimeRobot (free tier)
- Pingdom
- StatusCake
- Cloudflare Health Checks

---

## Troubleshooting

### Common Issues

**1. Build Fails with "Module not found":**

```bash
# Verify dependencies installed
pip list | grep sphinx

# Reinstall
pip install -r requirements.txt
```

**2. Deployment succeeds but 404 errors:**

```bash
# Check build output directory
ls -la _build/html/

# Verify index.html exists
test -f _build/html/index.html && echo "OK" || echo "Missing"
```

**3. Authentication loops (private docs):**

```bash
# Clear browser cookies
# Check OAuth provider configuration
# Verify email in access policy matches exactly
```

**4. CDN cache not updating:**

```bash
# Cloudflare: Purge cache
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/purge_cache" \
  -H "Authorization: Bearer API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'

# AWS CloudFront: Invalidate
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

---

## Rollback Procedures

**Cloudflare Pages:**

```bash
# List deployments
wrangler pages deployment list --project-name=my-docs

# Rollback to specific deployment
wrangler pages deployment rollback DEPLOYMENT_ID --project-name=my-docs
```

**AWS S3:**

```bash
# Enable versioning (prerequisite)
aws s3api put-bucket-versioning \
  --bucket docs-example-com \
  --versioning-configuration Status=Enabled

# List versions
aws s3api list-object-versions --bucket docs-example-com

# Restore specific version
aws s3api copy-object \
  --bucket docs-example-com \
  --copy-source docs-example-com/index.html?versionId=VERSION_ID \
  --key index.html
```

---

## Cost Optimization

**Cloudflare Pages:**
- Free tier: 500 builds/month, unlimited bandwidth
- Paid tier: $20/month, 5000 builds/month

**AWS S3 + CloudFront:**
- S3: $0.023/GB storage, $0.09/GB data transfer out
- CloudFront: $0.085/GB first 10TB
- Optimize: Enable compression, cache aggressively

**Read the Docs:**
- Free for open source
- Teams: $50/month

---

## Examples

See `02-examples/documentation-deployment-example/` for:
- Complete CI/CD workflows
- Platform-specific deployment scripts
- Authentication configuration examples
- Monitoring setup

---

## References

- **Cloudflare Pages:** https://developers.cloudflare.com/pages/
- **AWS S3 + CloudFront:** https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/
- **Read the Docs:** https://docs.readthedocs.io/
- **Netlify:** https://docs.netlify.com/
- **GitHub Pages:** https://docs.github.com/en/pages

---

**Version:** 1.0.0
**Last Updated:** January 19, 2026
