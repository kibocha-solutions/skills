# PPTX Generation Examples: Good vs Bad Patterns

## 1. Slide Layout and Assertion-Evidence Structure

### Bad (Topic Title, Bullet Dumping, and Hardcoded Inconsistencies)

```javascript
// BAD: Generic title, unconstrained text dumps, decorative shapes
let slide = pres.addSlide();
slide.addText("PROJECT OVERVIEW", { x: 0.5, y: 0.5, fontSize: 28, bold: true });
slide.addShape(pres.ShapeType.line, { x: 0.5, y: 1.1, w: 9.0, h: 0, line: { color: "0088CC", width: 2 } });
slide.addText(
  "• We are doing a lot of work on the backend.\n• Microservices are being deployed around October.\n• Performance is about 3x faster.\n• Generated automatically with AI tools.",
  { x: 0.5, y: 1.5, w: 9.0, h: 4.0, fontSize: 16 }
);
```

Defects:
- Non-assertive title ("PROJECT OVERVIEW") provides no takeaway.
- Decorative title underline adds visual clutter without informational value.
- Multi-bullet string dumping with raw newlines instead of separate paragraph objects.
- Contains vague quantity hedges ("around October", "about 3x faster").
- Leaks AI generation attribution.

### Good (Assertion Header, Structured Evidence Cards, and Clean Hierarchy)

```javascript
// GOOD: Assertion title, structured card layout, high contrast
let slide = pres.addSlide();

// Assertion title and subtitle category
slide.addText([
  { text: "CORE INFRASTRUCTURE\n", options: { fontSize: 10, bold: true, color: "0284C7" } },
  { text: "Microservice Migration Reduces API Latency by 65%", options: { fontSize: 20, bold: true, color: "0F172A" } }
], { x: 0.8, y: 0.6, w: 8.4, h: 1.0 });

// Card 1: Benchmark Metric
slide.addShape(pres.ShapeType.rect, { x: 0.8, y: 1.8, w: 4.0, h: 4.2, fill: { color: "F8FAFC" }, line: { color: "E2E8F0" } });
slide.addText("Latency Drop", { x: 1.1, y: 2.1, w: 3.4, h: 0.4, fontSize: 14, bold: true, color: "1E293B" });
slide.addText("65%", { x: 1.1, y: 2.6, w: 3.4, h: 1.0, fontSize: 44, bold: true, color: "0284C7" });
slide.addText("Average response time dropped from 420ms to 147ms during load testing across 50,000 concurrent sessions.", { x: 1.1, y: 3.8, w: 3.4, h: 1.8, fontSize: 12, color: "475569" });

// Card 2: Release Schedule
slide.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.8, w: 4.0, h: 4.2, fill: { color: "F8FAFC" }, line: { color: "E2E8F0" } });
slide.addText("Deployment Milestone", { x: 5.5, y: 2.1, w: 3.4, h: 0.4, fontSize: 14, bold: true, color: "1E293B" });
slide.addText("Oct 15", { x: 5.5, y: 2.6, w: 3.4, h: 1.0, fontSize: 44, bold: true, color: "059669" });
slide.addText("Final canary phase completes October 12, followed by full production cutover on October 15.", { x: 5.5, y: 3.8, w: 3.4, h: 1.8, fontSize: 12, color: "475569" });
```

Advantages:
- Assertion title delivers the primary conclusion immediately.
- Clean two-column card structure with structured spacing.
- Settled metrics and dates without hedging.
- High contrast and zero decorative clutter or AI attribution.
