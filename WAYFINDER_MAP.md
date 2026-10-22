# Wayfinder Map: FRA Diagnostics Platform - Frontend Redesign & Industrial Instrument UI

**Label**: `wayfinder:map`  
**Status**: Active  
**Tracker**: Local Markdown (`.issues/`)

---

## Destination

Completely transform the FRA Diagnostics web interface into a world-class, precision industrial instrument workstation adhering to IEEE Std C57.149 / IEC 60076-18. Replace generic dark-mode SaaS aesthetics with a cohesive, high-trust engineering console across all four surfaces (Landing, SFRA Diagnostic Workbench, History & Fleet Records, Standards Reference) featuring interactive sub-band logarithmic Bode plotting, real-time telemetry headers, and physics-grounded diagnostic cards.

---

## Notes

- **Domain**: Transformer condition monitoring via Sweep Frequency Response Analysis (SFRA). Refer to [CONTEXT.md](CONTEXT.md) for domain terminology.
- **Visual World**: Precision Industrial Instrument (matte obsidian/charcoal canvas `#090d16`/`#0d1117`, phosphor laboratory amber/emerald/cyan telemetry accents, JetBrains Mono typography for data telemetry, 1px structural grid dividers, zero fluffy neon blur).
- **Skills to Consult**: `impeccable`, `frontend-design`, `/prototype`, `/domain-modeling`, `/grilling`.
- **Standing Preferences**:
  - Adhere to IEEE Std C57.149 sub-band definitions (Core <2kHz, Winding 2kHz-100kHz, High >100kHz).
  - High data density and scanability over decorative fluff.
  - Zero external node build friction at runtime: modern Jinja2 + Tailwind CSS + Lucide Icons + Enhanced Chart.js.
  - Preserve all Flask routing and template variable bindings in `app/app.py`.

---

## Decisions so far

- [Establish Product Truth & Precision Industrial Design Tokens (`PRODUCT.md` & `DESIGN.md`)](.issues/ISSUE-008-product-truth-and-design-system.md) — Codified durable product truth for utility testing and established the Precision Industrial Instrument design system with normative tokens, obsidian/charcoal surfaces, phosphor telemetry, and dual-typeface typography.
- [Build Precision Industrial Master Layout Shell & Telemetry Header](.issues/ISSUE-009-master-layout-shell-and-navigation.md) — Established unified master layout architecture (Variant B: Left Avionics Rail + Context Telemetry Strip) codified in `app/templates/base.html`, providing responsive navigation and real-time telemetry headers.
- [Redesign Flagship SFRA Diagnostic Workbench (`index.html`)](.issues/ISSUE-010-sfra-workbench-redesign.md) — Re-architected `index.html` to inherit from `base.html`, featuring a two-state operational workflow (Upload Station ↔ Results Deck), 4-column metric ribbon, 1fr|380px Bode plot & diagnostic rail grid, client-side IEEE sub-band statistics, and restyled health gauge.
- [Build Interactive IEEE C57.149 Sub-band Logarithmic Bode Plot Component](.issues/ISSUE-011-subband-bode-plot-canvas.md) — Built precision Chart.js / HTML5 Canvas logarithmic Bode plot component featuring dynamic decade ticks, shaded IEEE sub-bands (Core <2kHz, Winding 2k-100kHz, Leads >100kHz), real-time cursor crosshairs with synchronized telemetry HUD, quick band zoom controls, and toggleable $|\Delta\text{dB}|$ residual trace on a secondary axis.
- [Redesign Analysis History & Fleet Records Console (`history.html`)](.issues/ISSUE-012-history-fleet-records-redesign.md) — Re-architected `history.html` into a high-density industrial fleet surveillance console extending `base.html`, featuring a 5-column fleet telemetry ribbon, real-time search and severity/sub-band filter matrix, 8-column telemetry table with expandable audit drawers, client-side CSV export, and single-click workbench inspection links (`/inspect/<id>`).
- [Redesign IEEE C57.149 Reference & SFRA Diagnostic Guide (`about.html`)](.issues/ISSUE-013-standards-and-knowledge-base-redesign.md) — Elevated `about.html` into an authoritative, interactive engineering manual inheriting `base.html`, featuring distributed RLC circuit diagrams, IEEE C57.149 / IEC 60076-18 sub-band criteria, analytical formulas (CCF / ASLE), a 7-failure-mode diagnostic matrix, and an interactive client-side sub-band criteria simulator.
- [Redesign Industrial Landing Experience (`landing.html`)](.issues/ISSUE-014-precision-industrial-landing-experience.md) — Re-architected `landing.html` to inherit from `base.html`, replacing generic SaaS marketing with an authoritative dual-bay precision instrument console, featuring a direct CSV ingestion terminal, 1-click sample dataset inspection presets, an interactive CRT oscilloscope / Bode plot with channel preset switching and real-time cursor HUD, and an IEEE C57.149 sub-band decomposition matrix.
- [Impeccable Design Audit & Visual Quality Floor Verification](.issues/ISSUE-015-impeccable-audit-and-visual-verification.md) — PASS with follow-ups (16/20 Good): all Flask routes 200 with zero Jinja leftovers, 16 pytest passed, contrast/trope/responsive floor verified; P1 muted-text contrast + P2 motion/labels/border-l-2 queued for polish.

---

## Not yet specified

<!-- Fog of war: in-scope fog you can't ticket yet; graduates as the frontier advances -->
- **Live 3D Transformer Winding Deformation CAD Viewer**: Interactive three-dimensional rendering of radial bucking or axial tilt derived from spectral shifts.
- **Three-Phase Comparative Overlay**: Simultaneous Phase A vs Phase B vs Phase C 3-trace comparative plotting when healthy baseline is unavailable.
- **Client-side CSV Parse & Synthetic Demo Injection**: In-browser client simulation mode for instant live evaluation without uploading test files.

---

## Out of scope

<!-- Out of scope: work ruled beyond the destination; closed, never graduates -->
- **Native Mobile Apps (iOS / Android)**: The platform is explicitly a desktop/tablet browser-based engineering workstation.
- **Real-Time Hardware USB Instrument Drivers**: Omicron/Doble hardware streaming drivers (handled by offline file export).
- **Previous Backend Pipeline Decisions (Completed)**: [ISSUE-001](.issues/ISSUE-001-ieee-subband-boundaries-and-metrics.md), [ISSUE-002](.issues/ISSUE-002-log-interpolation-and-preprocessing.md), [ISSUE-003](.issues/ISSUE-003-multiclass-dataset-training-pipeline.md), [ISSUE-004](.issues/ISSUE-004-hybrid-diagnostic-fusion-logic.md), [ISSUE-005](.issues/ISSUE-005-multi-asset-csv-ingestion.md), [ISSUE-006](.issues/ISSUE-006-enrich-pdf-reporting-with-bode-plots.md).
