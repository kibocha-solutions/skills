# diagrams.net Quick Reference

## Overview

diagrams.net (formerly draw.io) is the standard tool for creating architecture diagrams in this documentation framework. It provides editable `.drawio` files that can be version-controlled and easily updated.

**Why diagrams.net:**
- Free and open-source
- Web-based (no installation required)
- Desktop apps available (Windows, Mac, Linux)
- Integrates with GitHub, Google Drive, OneDrive
- Exports to PNG, SVG, PDF
- Version-controllable `.drawio` XML format

---

## Getting Started

### Web Version

Visit: https://app.diagrams.net/

1. Click "Create New Diagram"
2. Choose template or start blank
3. Draw your diagram
4. Save as `.drawio` file

### Desktop App

Download from: https://github.com/jgraph/drawio-desktop/releases

**Recommended for:**
- Offline work
- Large diagrams
- Frequent diagramming

---

## Creating C4 Architecture Diagrams

### System Context Diagram (C4 Level 1)

**Purpose:** Show system boundary, users, and external systems

**Shapes to Use:**
- **System Boundary:** Rectangle with thick border
- **Users:** Stick figure (under "General" shapes)
- **External Systems:** Rectangle with dashed border
- **Arrows:** Solid lines with labels

**Example Layout:**

```
┌─────────────────────────────────────────┐
│                                         │
│         [System Name]                   │
│                                         │
└─────────────────────────────────────────┘
          ↑                    ↑
          │                    │
    [End User]       [External System]
```

**Steps:**

1. **Add System Boundary**
   - Shape: Rectangle
   - Fill: #7ED321 (green)
   - Border: 3px solid #5A9E16
   - Label: "Tax Management System"

2. **Add Users**
   - Shape: Stick figure (General > Person)
   - Fill: #4A90E2 (blue)
   - Label: "End User", "Admin", "System Admin"

3. **Add External Systems**
   - Shape: Rectangle
   - Fill: #F5A623 (orange)
   - Border: 2px dashed
   - Label: "KRA eTIMS", "M-Pesa Gateway"

4. **Add Arrows**
   - Connector: Solid line with arrow
   - Label: Describe interaction
   - Example: "Calculates taxes", "Sends payments"

---

### Container Diagram (C4 Level 2)

**Purpose:** Show major containers (apps, services, databases)

**Shapes to Use:**
- **Web Application:** Rectangle with rounded corners
- **Mobile App:** Rectangle with mobile icon
- **Backend Service:** Rectangle
- **Database:** Cylinder
- **Message Queue:** Parallelogram
- **File Storage:** Cloud/folder icon

**Color Scheme:**
- Web/Mobile Apps: #4A90E2 (blue)
- Backend Services: #50E3C2 (teal)
- Databases: #BD10E0 (purple)
- Message Queues: #F5A623 (orange)
- File Storage: #D0021B (red)

**Steps:**

1. **Add Web Application**
   - Shape: Rectangle with rounded corners (8px radius)
   - Fill: #4A90E2
   - Label: "Web App\n[React + TypeScript]"

2. **Add Backend Services**
   - Shape: Rectangle
   - Fill: #50E3C2
   - Label: "Tax Service\n[Go]"

3. **Add Database**
   - Shape: Cylinder (under "General" shapes)
   - Fill: #BD10E0
   - Label: "PostgreSQL\n[Primary DB]"

4. **Connect with Labeled Arrows**
   - Example: "Makes API calls [HTTPS/REST]"
   - Example: "Reads/writes [SQL]"

---

### Component Diagram (C4 Level 3)

**Purpose:** Break down key containers into components

**Shapes to Use:**
- **Component:** Rectangle with component stereotype «component»
- **Relationships:** Solid arrows with labels

**Steps:**

1. **Create Container Boundary**
   - Large rectangle encompassing all components
   - Label: "[Container Name]"

2. **Add Components**
   - Shape: Rectangle
   - Fill: #50E3C2
   - Stereotype: «component»
   - Label: "API Controller", "Business Logic", "Data Access"

3. **Show Relationships**
   - Arrows between components
   - Label with method calls or data flow

---

## Data Flow Diagrams

**Purpose:** Show how data moves through the system

**Shapes:**
- **Process:** Rectangle
- **Data Store:** Open rectangle (like a database)
- **External Entity:** Rectangle with thick border
- **Data Flow:** Arrow with label

**Example:**

```
[User] → [API Gateway] → [Tax Service] → [Database]
                ↓
          [Message Queue]
                ↓
         [Email Service]
```

---

## Export Settings

### PNG Export (for Documentation)

1. File → Export As → PNG
2. **Settings:**
   - Border Width: 10px
   - Zoom: 100%
   - Transparent Background: ✓ (or white if preferred)
   - Selection Only: ☐ (export entire diagram)
   - Include copy of diagram: ☐
3. Click "Export"
4. Save as `[diagram-name].png`

**File Naming:**
- Same name as `.drawio` file
- Example: `system-context.drawio` → `system-context.png`

### SVG Export (for Scalable Graphics)

1. File → Export As → SVG
2. Use same settings as PNG
3. Useful for high-resolution printing

---

## Standard Colors (Copy These Hex Codes)

```
Users:           #4A90E2 (blue)
System Boundary: #7ED321 (green)
External Systems: #F5A623 (orange)
Backend Services: #50E3C2 (teal)
Databases:       #BD10E0 (purple)
Message Queues:  #F8931F (dark orange)
File Storage:    #D0021B (red)
```

---

## Shape Library

### Adding C4 Model Shapes

1. Click "+" at bottom of Shapes panel
2. Search for "C4"
3. Click "C4" libraries
4. Enable "C4 Architecture" library

This adds pre-made C4 shapes with correct notation.

### Custom Shape Library

Create your own library with standardized shapes:

1. File → New Library
2. Drag custom shapes into library
3. Save as `project-shapes.xml`
4. Share with team for consistency

---

## Collaboration

### Git Integration

1. File → Open from → GitHub
2. Authenticate with GitHub
3. Select repository and `.drawio` file
4. Edit directly, commits saved to GitHub

### Google Drive

1. File → Open from → Google Drive
2. Authenticate
3. Real-time collaboration supported

---

## Best Practices

### Diagram Layout

✅ **Do:**
- Left-to-right or top-to-bottom flow
- Group related elements
- Use consistent spacing (20-50px gaps)
- Align elements using grid (View → Grid)
- Keep diagrams simple (max 15-20 elements)

❌ **Don't:**
- Cross lines unnecessarily
- Use inconsistent colors
- Overcrowd diagrams
- Use tiny fonts (minimum 11pt)

### Labeling

✅ **Do:**
- Use verb phrases for arrows ("Sends request", "Returns data")
- Include technology in brackets: "API Gateway [Kong]"
- Add descriptions for context

❌ **Don't:**
- Use vague labels ("Uses", "Connects to")
- Skip technology annotations
- Use abbreviations without legend

### File Organization

```
diagrams/
├── system-context.drawio           # C4 Level 1
├── system-context.png
├── containers.drawio               # C4 Level 2
├── containers.png
├── components-tax-service.drawio   # C4 Level 3
├── components-tax-service.png
├── data-flow.drawio
└── data-flow.png
```

**Naming Convention:**
- Lowercase with hyphens
- Descriptive names
- Match .drawio and .png filenames

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New Diagram | Ctrl+N |
| Save | Ctrl+S |
| Undo | Ctrl+Z |
| Redo | Ctrl+Y |
| Duplicate | Ctrl+D |
| Group | Ctrl+G |
| Ungroup | Ctrl+Shift+U |
| Align Left | Ctrl+Shift+← |
| Align Center | Ctrl+Shift+C |
| Distribute Horizontally | Ctrl+Shift+H |

---

## Embedding in reStructuredText

### Basic Figure

```rst
.. figure:: diagrams/system-context.png
   :alt: System context diagram
   :width: 800px
   
   Figure 1: System context showing users and external systems.
```

### Centered Figure

```rst
.. figure:: diagrams/containers.png
   :alt: Container diagram
   :align: center
   :width: 90%
   
   Container architecture diagram.
```

---

## Troubleshooting

### Diagram Won't Open

**Issue:** `.drawio` file corrupted  
**Solution:** Open from backup or GitHub history

### Export Quality Poor

**Issue:** PNG looks blurry  
**Solution:** Increase zoom to 200% before exporting

### Colors Don't Match

**Issue:** Inconsistent colors across diagrams  
**Solution:** Use hex codes, create custom library with standardized shapes

---

## Additional Resources

- **diagrams.net Official Site:** https://www.diagrams.net/
- **C4 Model Guide:** https://c4model.com/
- **Shape Libraries:** https://www.diagrams.net/blog/shape-libraries
- **Tutorials:** https://www.diagrams.net/doc/

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial diagrams.net quick reference
- C4 model diagram instructions
- Export settings and best practices
