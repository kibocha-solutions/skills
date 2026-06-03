# Canon: Documentation UI and Theming

## Purpose

This canon defines standards for creating clean, modern, attractive user interfaces for technical documentation. It covers theme selection, visual design, navigation structure, component styling, and accessibility requirements for Sphinx-based documentation.

---

## Scope

**This canon applies to:**
- Sphinx documentation websites (RST-based)
- OpenAPI documentation UI (Redoc, Swagger UI)
- Custom documentation portals
- Technical documentation landing pages
- Documentation component libraries

**This canon does NOT apply to:**
- Application UI/UX (use design system canons)
- Marketing websites
- Blog layouts
- Content management system themes

---

## Access Level Classification

**UI/Theme Documentation:**
- **Access Level:** Internal (Level 2)
- **Distribution:** Development and design teams
- **Storage:** Private repository (design decisions may contain competitive advantages)
- **Rationale:** Theme configurations, brand decisions, and UX patterns are internal

**Theme Assets (CSS, JavaScript):**
- **Access Level:** Public (Level 1) if deployed publicly
- **Source Code:** Internal (Level 2)

---

## Theme Selection

### Recommended Sphinx Themes

**1. Furo (Primary Recommendation)**
- Modern, clean design
- Excellent mobile responsiveness
- Built-in dark mode
- Customizable via CSS variables
- Active maintenance
- Fast performance
- WCAG 2.1 AA accessible

```python
# conf.py
html_theme = 'furo'
```

**2. Sphinx Book Theme**
- Academic/book-like appearance
- Good for long-form documentation
- Jupyter notebook integration
- Page navigation sidebar

**3. PyData Sphinx Theme**
- Data science focused
- Similar to Jupyter Book
- Great for scientific documentation

**4. Read the Docs Theme**
- Classic, familiar to developers
- Widely recognized
- Simple, functional

### Theme Selection Criteria

When choosing a theme, evaluate:
- **Readability:** Generous whitespace, optimal line length (70-80 characters)
- **Mobile Support:** Responsive design, collapsible navigation
- **Dark Mode:** Built-in or easy to implement
- **Customization:** CSS variables, template overrides
- **Performance:** Fast page load, minimal JavaScript
- **Accessibility:** WCAG 2.1 AA compliance minimum
- **Maintenance:** Active development, security updates
- **Documentation:** Clear customization guide

---

## Visual Design System

### Color System

**Dual-Mode Colors (Light and Dark):**

```python
# conf.py - Furo theme
html_theme_options = {
    "light_css_variables": {
        # Brand colors
        "color-brand-primary": "#3b82f6",      # Blue
        "color-brand-content": "#171717",      # Dark gray
        
        # Background colors
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#fafafa",
        
        # Text colors
        "color-foreground-primary": "#171717",
        "color-foreground-secondary": "#525252",
        
        # Borders
        "color-background-border": "#e5e5e5",
    },
    "dark_css_variables": {
        # Brand colors (adjusted for contrast)
        "color-brand-primary": "#60a5fa",      # Lighter blue
        "color-brand-content": "#fafafa",
        
        # Background colors
        "color-background-primary": "#121212",
        "color-background-secondary": "#1a1a1a",
        
        # Text colors
        "color-foreground-primary": "#fafafa",
        "color-foreground-secondary": "#a3a3a3",
        
        # Borders
        "color-background-border": "#404040",
    },
}
```

**Semantic Colors:**

```python
# For admonitions and alerts
"color-admonition-title--note": "#8b5cf6",      # Purple
"color-admonition-title--tip": "#10b981",       # Green
"color-admonition-title--important": "#f59e0b", # Amber
"color-admonition-title--warning": "#f59e0b",   # Amber
"color-admonition-title--caution": "#ef4444",   # Red
```

**Accessibility Requirements:**
- Minimum contrast ratio: 4.5:1 (body text)
- Minimum contrast ratio: 3:1 (large text, UI components)
- WCAG 2.1 AA compliance
- Test with color blindness simulators

### Typography

**Font Stack:**

```python
html_theme_options = {
    "light_css_variables": {
        # Body text (system fonts for zero load time)
        "font-stack": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif",
        
        # Code (monospace with fallbacks)
        "font-stack--monospace": "'JetBrains Mono', Menlo, Monaco, 'Courier New', Courier, monospace",
    },
}
```

**Type Scale:**

```
H1 (Page Title):   32px, weight 700, line-height 1.2
H2 (Section):      24px, weight 700, line-height 1.3
H3 (Subsection):   20px, weight 600, line-height 1.4
H4 (Minor):        18px, weight 600, line-height 1.4
Body Text:         16px, weight 400, line-height 1.6
Small Text:        14px, weight 400, line-height 1.5
Code Inline:       14px, weight 400
Code Block:        14px, weight 400, line-height 1.5
```

**Readability Standards:**
- Max content width: 800px (optimal for technical content)
- Line length: 70-80 characters per line
- Paragraph spacing: 16px between paragraphs
- Heading spacing: Progressive (larger headings = more space)

### Layout Structure

**Three-Column Desktop Layout:**

```
┌─────────────────────────────────────┐
│   Header (Logo, Search, Toggle)    │
├──────┬──────────────────────┬───────┤
│ Side │    Main Content     │ TOC   │
│ Nav  │    (Max 800px)      │ (Page)│
│      │                     │       │
│ 250px│                     │ 200px │
└──────┴─────────────────────┴───────┘
```

**Responsive Breakpoints:**
- Desktop (> 1024px): Three columns (sidebar, content, TOC)
- Tablet (768-1024px): Two columns (collapsible sidebar, content)
- Mobile (< 768px): Single column (hamburger menu)

---

## Navigation Structure

### Documentation Organization

**Recommended Structure:**

```
docs/
├── index.rst                    # Documentation homepage
├── getting-started/
│   ├── index.rst                # Getting started overview
│   ├── installation.rst
│   ├── quick-start.rst
│   └── configuration.rst
├── user-guide/
│   ├── index.rst
│   ├── features/
│   └── tutorials/
├── api-reference/
│   ├── index.rst
│   ├── rest-api.rst
│   ├── authentication.rst
│   └── endpoints/
├── architecture/
│   ├── index.rst
│   ├── system-overview.rst
│   └── components/
├── deployment/
│   ├── index.rst
│   ├── self-hosted.rst
│   └── cloud-providers/
└── admin/                       # Private documentation
    ├── index.rst
    ├── admin-panel.rst
    └── security/
```

**Navigation Principles:**
- **Progressive Disclosure:** Start broad, drill down to specifics
- **Flat When Possible:** Avoid nesting beyond 3 levels
- **Predictable Patterns:** Similar types of content organized similarly
- **Clear Labels:** Navigation item names are descriptive and scannable
- **Search-Friendly:** Structure supports effective search

### Sidebar Navigation

**Configuration:**

```python
# conf.py
html_theme_options = {
    # Enable navigation
    "navigation_with_keys": True,
    "sidebar_hide_name": False,
    
    # Navigation depth
    "navigation_depth": 3,
    
    # Collapse navigation
    "collapse_navigation": True,
    "includehidden": True,
}
```

**Behavior:**
- Active page highlighted (bold, colored, border)
- Parent sections collapsible
- Smooth scroll to anchors
- Keyboard accessible (Tab, Enter, Arrow keys)

### Table of Contents (TOC)

**On-Page TOC:**
- Shows H2 and H3 headings only
- Sticky positioning (follows scroll)
- Scroll spy (highlights current section)
- Click to smooth-scroll
- Max 200px width on desktop
- Hidden on mobile (use in-content TOC)

**In-Content TOC:**

```rst
.. contents:: Table of Contents
   :depth: 2
   :local:
```

Use for long pages (> 3 screens of content).

---

## Component Styling

### Code Blocks

**Syntax Highlighting:**

```python
# conf.py
pygments_style = 'friendly'           # Light mode
pygments_dark_style = 'monokai'       # Dark mode
```

**Code Block Features:**

```python
extensions = [
    'sphinx_copybutton',    # Copy button for code blocks
    'sphinx_tabs.tabs',     # Tabbed code examples
]

# Copy button configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
```

**Styling Standards:**
- Background distinct from page (light: #f7f7f7, dark: #2b2b2b)
- Border: 1px solid border color
- Border radius: 8px
- Padding: 16px
- Line numbers optional (for reference, not default)
- Language label: Top-left corner
- Copy button: Top-right corner with feedback

### Admonitions

**Available Types:**

```rst
.. note::
   Additional information

.. tip::
   Helpful suggestions

.. important::
   Critical information

.. warning::
   Cautions, potential issues

.. danger::
   Critical warnings

.. seealso::
   Related content
```

**Styling:**
- Colored left border (4px)
- Icon or emoji matching type
- Background color (subtle tint)
- Padding: 16px
- Margin: 24px 0

### Tables

**Styling Standards:**
- Border: 1px solid border color
- Header row: Background tint, bold text
- Cell padding: 12px 16px
- Alternating row colors (optional, for readability)
- Responsive: Horizontal scroll on mobile
- Max width: Content width

**Preferred Format:**

```rst
.. list-table:: Table Title
   :header-rows: 1
   :widths: 30 70

   * - Column 1
     - Column 2
   * - Data 1
     - Data 2
```

### Images and Diagrams

**Requirements:**
- Alt text MANDATORY (accessibility)
- Captions for context
- Responsive (max-width: 100%)
- High DPI support (2x images)
- Dark mode variants when applicable

```rst
.. figure:: images/architecture-diagram.png
   :alt: System architecture showing microservices
   :width: 100%
   :align: center

   Figure 1: System Architecture Overview
```

**Image Formats:**
- Screenshots: PNG (compressed)
- Diagrams: SVG (preferred) or PNG
- Photos: WebP or JPEG (optimized)
- Max file size: 500KB per image

---

## Search Configuration

**Sphinx Search:**

```python
# conf.py
html_search_language = 'en'
html_search_options = {
    'type': 'default',  # or 'whoosh' for better search
}

# External search (optional)
extensions = [
    'sphinx_search.extension',  # Enhanced search
]
```

**Search UI:**
- Prominent placement (header, top-right)
- Keyboard shortcut (Ctrl+K or Cmd+K)
- Live results (as you type)
- Keyboard navigation (Arrow keys, Enter)
- Search scope indicators

---

## Accessibility Standards

### WCAG 2.1 AA Compliance

**Mandatory Requirements:**
- **Contrast Ratios:** 4.5:1 (text), 3:1 (UI components)
- **Keyboard Navigation:** All interactive elements accessible
- **Focus Indicators:** Visible focus states (2px outline)
- **Alt Text:** All images have descriptive alt attributes
- **Headings:** Logical hierarchy (don't skip levels)
- **Link Text:** Descriptive (avoid "click here")
- **ARIA Labels:** For icon buttons, navigation landmarks

**Testing:**
- Automated: axe DevTools, WAVE
- Manual: Keyboard-only navigation
- Screen readers: NVDA (Windows), VoiceOver (Mac)
- Color blindness: Coblis simulator

### Keyboard Shortcuts

**Standard Shortcuts:**
- `Tab`: Navigate forward
- `Shift+Tab`: Navigate backward
- `Enter`: Activate link/button
- `/` or `Ctrl+K`: Focus search
- `Esc`: Close modals/overlays
- `Arrow Keys`: Navigate sidebar (when focused)

---

## Performance Optimization

### Page Load Performance

**Targets:**
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Time to Interactive: < 3.5s
- Cumulative Layout Shift: < 0.1

**Optimization Strategies:**
- Minimize JavaScript (Sphinx generates static HTML)
- Lazy load images
- Preload critical fonts
- Use system fonts (zero load time)
- Minimize CSS (remove unused styles)
- Enable HTTP/2 or HTTP/3
- Use CDN for assets

### Build Performance

```python
# conf.py
# Parallel builds
numjobs = 4  # or 'auto'

# Exclude unnecessary files
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**.ipynb_checkpoints',
]
```

---

## Private vs Public Documentation UI

### Visual Distinction

**Private Documentation Indicators:**
- **Banner:** Top banner indicating "Internal Documentation - Access Restricted"
- **Color Accent:** Different primary color (e.g., red/orange instead of blue)
- **Watermark:** Subtle background watermark "INTERNAL"
- **Footer:** "Confidential - Do Not Distribute"

**Example Configuration:**

```python
# private-conf.py
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#ef4444",  # Red instead of blue
    },
    "announcement": "<strong>⚠️ Internal Documentation</strong> - Access restricted to authorized personnel only.",
}
```

### Authentication UI

**Cloudflare Access Flow:**
1. User visits `/private/`
2. Redirect to OAuth provider (Google/GitHub)
3. Authentication success
4. Redirect back to documentation
5. Session cookie set (24 hours)

**UI Considerations:**
- Clear "Sign In" button if session expired
- User info in header (email, sign out)
- Session expiration warning (5 minutes before)
- Graceful error messages

---

## OpenAPI Documentation UI

### Redoc (Recommended)

**Configuration:**

```bash
npx @redocly/cli build-docs openapi.yaml -o api-docs.html \
  --options.theme.colors.primary.main=#3b82f6 \
  --options.theme.typography.fontFamily="'-apple-system', sans-serif"
```

**Features:**
- Three-panel layout (navigation, content, code samples)
- Syntax highlighting
- Try It Out functionality
- Download OpenAPI spec button
- Search bar
- Responsive design

### Swagger UI (Alternative)

**Configuration:**

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "openapi.yaml",
      dom_id: '#swagger-ui',
      deepLinking: true,
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout"
    });
  </script>
</body>
</html>
```

---

## Custom Styling

### Custom CSS

**File:** `_static/custom.css`

```css
/* Custom theme overrides */
.furo-sidebar-navigation {
  font-size: 14px;
}

.furo-content code {
  background-color: var(--color-background-secondary);
  padding: 2px 6px;
  border-radius: 4px;
}

/* Private docs banner */
.private-docs-banner {
  background-color: #fef2f2;
  border-left: 4px solid #ef4444;
  padding: 12px 16px;
  margin-bottom: 24px;
}
```

**Load in `conf.py`:**

```python
html_static_path = ['_static']
html_css_files = ['custom.css']
```

### Custom JavaScript

**File:** `_static/custom.js`

```javascript
// Add custom behavior
document.addEventListener('DOMContentLoaded', function() {
  // Copy button feedback
  document.querySelectorAll('.copy-button').forEach(button => {
    button.addEventListener('click', function() {
      this.textContent = 'Copied!';
      setTimeout(() => { this.textContent = 'Copy'; }, 2000);
    });
  });
});
```

**Load in `conf.py`:**

```python
html_js_files = ['custom.js']
```

---

## Testing Checklist

**Before Deployment:**
- [ ] All pages render correctly (no broken links)
- [ ] Navigation works (sidebar, TOC, breadcrumbs)
- [ ] Search returns relevant results
- [ ] Code blocks have copy buttons
- [ ] Dark mode switches properly
- [ ] Mobile view is responsive (hamburger menu)
- [ ] Images load with correct alt text
- [ ] Admonitions styled correctly
- [ ] Tables are readable on mobile
- [ ] Keyboard navigation works
- [ ] Screen reader announces content correctly
- [ ] Contrast ratios pass WCAG AA
- [ ] Page load under 3 seconds
- [ ] Authentication flow works (private docs)
- [ ] Session persistence works (24 hours)

---

## Maintenance

**Regular Updates:**
- Update Sphinx and theme packages quarterly
- Review accessibility with each major update
- Test new browsers/devices as they release
- Monitor page load performance
- Update documentation screenshots

**Version Pinning:**

```bash
# requirements.txt
sphinx==7.2.6
furo==2024.1.29
sphinx-copybutton==0.5.2
sphinx-tabs==3.4.5
```

---

## Examples

See `02-examples/documentation-ui-example/` for:
- Complete Sphinx configuration
- Custom theme overrides
- Navigation structure example
- Component styling examples
- Public/private split examples

---

## References

- **Furo Documentation:** https://pradyunsg.me/furo/
- **Sphinx Theming:** https://www.sphinx-doc.org/en/master/development/theming.html
- **WCAG 2.1 Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/
- **Redocly CLI:** https://redocly.com/docs/cli/
- **Web Content Accessibility:** https://webaim.org/

---

**Version:** 1.0.0
**Last Updated:** January 19, 2026
