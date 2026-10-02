# [ISSUE-014] Redesign Industrial Landing Experience (`landing.html`)

- **ID**: ISSUE-014
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked By**: None
- **Blocks**: ISSUE-015

---

## Question

How should `app/templates/landing.html` be redesigned into an authoritative precision-instrument landing page, replacing generic AI SaaS gradients with an industrial instrument aesthetic, hero telemetry preview, and direct workflow CTAs?

---

## Resolution

The platform landing experience was completely transformed from a generic AI marketing placeholder into an authoritative, precision-instrument mission overview and launchpad in [`app/templates/landing.html`](../app/templates/landing.html), integrated seamlessly with the master layout shell [`app/templates/base.html`](../app/templates/base.html) and enhanced route telemetry in [`app/app.py`](../app/app.py):

1. **Precision Industrial Shell & Spec Header**:
   - Inherits `base.html` with persistent Left Vertical Avionics Rail highlighting `OVERVIEW` (`active_page='landing'`).
   - Sticky context sub-header with standards specification badges for `IEEE Std C57.149-2012`, `IEC 60076-18 ED.1`, `CIGRE TB 342`, and `500-PT LOG GRID`.

2. **Hero Dual-Bay Precision Instrument Console**:
   - **Left Bay (Mission Command & Scan Ingestion Terminal)**:
     - Direct drag-and-drop CSV test sweep upload dropzone (`action="/analyze"`), accepting OMICRON, Doble, Megger, and generic tabular CSV files with instant file detection feedback.
     - 1-click verified field presets to immediately launch inspect mode for `TX-220KV-AUTO-03` (Nominal), `TX-400KV-GSU-02` (Core Shift), and `TX-765KV-MAIN-01` (Winding Displacement).
     - Direct launch matrix to Workbench, Fleet Surveillance, and Standards KB.
   - **Right Bay (Interactive Hero Telemetry Oscilloscope & Bode Display)**:
     - CRT screen with logarithmic frequency grid (20 Hz – 2 MHz across 5 decades) and shaded IEEE sub-bands (Low Core <2kHz, Mid Winding 2k-100kHz, High Leads >100kHz).
     - Interactive channel preset switcher:
       - *Nominal Baseline (TX-220KV)*: $R^2 = 0.9890$, $\Delta\text{dB} = 1.4\text{ dB}$, Nominal Pass.
       - *Mid-Band Winding Fault (TX-765KV)*: $R^2 = 0.7420$, $\Delta\text{dB} = 14.8\text{ dB}$, Critical Alarm.
       - *Low-Band Core Shift (TX-400KV)*: $R^2 = 0.8842$, $\Delta\text{dB} = 6.2\text{ dB}$, Advisory Monitor.
     - Live interactive cursor hover HUD updating frequency, correlation $R^2$, max shift $\Delta\text{dB}$, and IEEE verdict.

3. **4-Column High-Density Instrument Telemetry Ribbon**:
   - Dynamic telemetry readouts for Bandwidth Spectrum (20 Hz - 2 MHz), Standards Criteria (IEEE C57.149 / IEC 60076-18), Ingestion Compatibility (4+ Vendors), and Active Monitored Fleet apparatus counts.

4. **Deterministic Analytical Processing Pipeline (4-Stage Architecture)**:
   - 4-bay architectural seam diagram detailing Phase 01 (Multi-Vendor Ingestion), Phase 02 (Logarithmic Grid Spline), Phase 03 (Deterministic Physics Floor + ML Classifier), and Phase 04 (Normative PDF Reporting).

5. **IEEE C57.149 Physical Sub-Band Decomposition Matrix**:
   - 3-column physical circuit breakdown mapping sub-band 1 (<2 kHz), sub-band 2 (2 kHz - 100 kHz), and sub-band 3 (>100 kHz) to circuit components ($L_m, L_\sigma, C_s, C_g, C_b$), detectable mechanical defects, and normative acceptance thresholds.

6. **Monitored Fleet Apparatus Audit Trail Strip**:
   - High-density telemetry table populated with live monitored assets from `records`, displaying asset ID, substation, voltage rating, Health Integrity Index (HII), primary status beacon, and 1-click `/inspect/<id>` links.

7. **Engineering Workflow & Action Deck**:
   - Direct launch pathways to Workflow A (SFRA Diagnostic Workbench `/analysis`), Workflow B (Fleet Records `/history`), and Workflow C (IEEE Standards Manual `/about`).

8. **Unblocks**: [ISSUE-015](ISSUE-015-impeccable-audit-and-visual-verification.md).
