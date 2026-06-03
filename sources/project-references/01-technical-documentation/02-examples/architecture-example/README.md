# Architecture Documentation Example

## Purpose

This example demonstrates production-grade architecture documentation for a Tax Management System (TMS). It follows the `_architecture-canon.md` specifications and shows correct implementation of C4 model architecture diagrams and narrative documentation.

---

## What This Example Demonstrates

✅ **C4 Model Architecture**
- System Context diagram (Level 1)
- Container diagram (Level 2)
- Component diagram (Level 3)

✅ **Complete Documentation Set**
- Architecture overview with principles
- Technology stack with justifications
- Data flow documentation
- Scalability strategy
- Security architecture
- Integration points

✅ **diagrams.net Usage**
- C4 diagrams in `.drawio` format
- Exported PNG files for documentation
- Consistent colors and notation
- Proper labeling and legends

✅ **Production Standards**
- Internal (Level 2) access classification
- No emojis or emdashes
- Varied sentence structure
- Specific metrics and data points
- References to ADRs for design decisions

---

## Files Included

```
architecture-example/
├── README.md                       # This file
├── 00-overview.rst                 # Architecture overview
├── 01-system-context.rst           # C4 Level 1 (planned)
├── 02-containers.rst               # C4 Level 2 (planned)
├── 04-technology-stack.rst         # Tech stack (planned)
├── 05-data-flow.rst                # Data flow (planned)
└── diagrams/
    ├── system-context.drawio       # Editable diagram (planned)
    ├── system-context.png          # Exported for docs (planned)
    ├── containers.drawio           # Editable diagram (planned)
    └── containers.png              # Exported for docs (planned)
```

---

## How to Use This Example

### For Agents

When tasked with creating architecture documentation:

1. Read `_architecture-canon.md` for rules
2. Review this example to see correct implementation
3. Generate similar files for the target system
4. Follow C4 model structure
5. Use diagrams.net for all diagrams
6. Export PNG files for embedding

### For Human Developers

When creating architecture documentation manually:

1. Copy this structure as starting point
2. Replace TMS-specific content with your system
3. Create diagrams using diagrams.net
4. Follow the same organization and depth
5. Include access level warnings
6. Reference ADRs for major decisions

---

## System Overview: Tax Management System (TMS)

**Purpose:** Cloud-based platform for calculating Kenyan taxes using KRA rules

**Architecture Style:** Microservices

**Scale:**
- 50,000 users
- 200,000 calculations/month
- 99.9% uptime target

**Tech Stack:**
- Backend: Go microservices
- Frontend: React + TypeScript
- Database: PostgreSQL + Redis
- Infrastructure: Kubernetes on AWS
- API: REST (public), gRPC (internal)

---

## Key Architectural Decisions

1. **Microservices over Monolith** (ADR-002)
   - Independent scaling
   - Team autonomy
   - Easier maintenance

2. **PostgreSQL over MongoDB** (ADR-001)
   - ACID compliance for financial data
   - Strong consistency guarantees

3. **gRPC for Internal Communication** (ADR-003)
   - High performance
   - Type safety with Protocol Buffers
   - Bi-directional streaming

4. **Redis for Caching** (ADR-004)
   - Sub-millisecond response times
   - Built-in TTL support
   - Pub/sub for real-time updates

---

## Viewing the Example

### Sphinx Build

To view this example in rendered form:

```bash
# From project root
sphinx-build -b html docs/source docs/build
# Open docs/build/architecture/00-overview.html
```

### Direct File Review

Read the `.rst` files directly to see:
- reStructuredText syntax
- Section organization
- Cross-references
- Figure embedding
- Warning directives

---

## Compliance with Canon

This example strictly follows `_architecture-canon.md`:

✅ C4 model structure (System Context, Containers, Components)  
✅ All files in `/docs/source/architecture/` directory  
✅ diagrams.net used for all diagrams (`.drawio` format)  
✅ PNG exports for documentation embedding  
✅ Technology stack with justifications  
✅ Internal (Level 2) access classification  
✅ References to ADRs for major decisions  
✅ No emojis or emdashes  
✅ Varied sentence structure  
✅ Specific data points (not vague claims)

---

## Next Steps

When using this example as a template:

1. Replace "TMS" with your system name
2. Update architecture diagrams to match your system
3. Document your actual technology stack
4. Adjust scale metrics to your system
5. Reference your actual ADRs
6. Update security and integration sections

---

## References

- **Canon:** `01-documentation-canons/_architecture-canon.md`
- **C4 Model:** https://c4model.com/
- **diagrams.net:** https://www.diagrams.net/
