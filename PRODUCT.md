# Product Truth: FRA Diagnostics Platform

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Python 3 / Flask web server, Jinja2 templating, Tailwind CSS utility architecture, Lucide icons, and Chart.js telemetry plotting. No mandatory Node.js/npm runtime build step required.

## Users

1. **High-Voltage Substation Field Engineers**: Technicians operating portable SFRA test sets (Doble, Omicron) in substation switchyards, requiring rapid verification of baseline correlation and immediate detection of transportation or short-circuit damage.
2. **Transformer Asset Health Managers & Reliability Engineers**: Utility specialists analyzing fleet-wide diagnostic trends, assessing historical degradation across multi-year maintenance cycles, and authorizing physical internal inspections or de-tanking.
3. **Commissioning & Factory Acceptance Testers (FAT)**: OEM and test facility engineers verifying that newly manufactured power transformers match design baseline specs before leaving the factory.

## Product Purpose

Provide a precision, high-trust engineering instrument workstation for Sweep Frequency Response Analysis (SFRA) of high-voltage power transformers adhering to IEEE Std C57.149 and IEC 60076-18 standards. Transform raw frequency response curves into immediate, physics-grounded diagnostic insights (core displacement, winding deformation, loose connections, dielectric degradation) with transparent mathematical sub-band correlation and reproducible PDF audit reports.

## Positioning

Unlike generic multi-purpose cloud dashboards or proprietary, dongle-locked OEM desktop tools, FRA Diagnostics is an open, standards-grounded web workstation tailored specifically to high-voltage electrical apparatus physics. It marries IEEE C57.149 sub-band domain rules with hybrid neural fault inference, presenting high-density spectral telemetry in a focused, distraction-free instrument console.

## Operating Context

- **Workstations & Laptops in Field Control Rooms**: Often used on rugged field laptops under varying lighting conditions, with keyboards, mice, or touchpads.
- **Critical Asset Decisions**: Diagnostic outcomes inform decisions involving high capital risk (de-energization, de-tanking, crane mobilization, capital replacement). Ambiguity or unverified "AI guesses" are unacceptable; all outputs must provide sub-band mathematical cross-correlation ($R^2$, $\rho$), peak decibel deviation ($\Delta\text{dB}$), and frequency shift ($\Delta f$).
- **Multi-Asset Fleet History**: Fast lookup and side-by-side comparison against prior baseline signatures across asset serial numbers and test dates.

## Capabilities and Constraints

- **Four Primary Worksurfaces**:
  1. **Landing & Mission Overview (`/`)**: Direct introduction to SFRA diagnostics, test standards, and instant entry points.
  2. **SFRA Diagnostic Workbench (`/analysis` & `/analyze`)**: Core instrument deck for CSV file ingestion, interactive logarithmic sub-band Bode plot visualization, sub-band metric analysis, health index computation, and PDF report generation.
  3. **Fleet Records & History (`/history`)**: Audit trail of analyzed transformers, historical scans, baseline mappings, and rapid re-test access.
  4. **Standards & Knowledge Base (`/about`)**: Complete technical reference covering IEEE Std C57.149 sub-band physics (Low/Medium/High), mathematical formulations, and fault signature mechanics.
- **Standards Sub-Band Mapping**:
  - **Low Frequency Band (< 2 kHz)**: Main core magnetizing inductance & magnetic circuit geometry (core displacement, grounding anomalies).
  - **Medium Frequency Band (2 kHz – 100 kHz)**: Winding inductance & inter-winding/ground capacitance (axial/radial winding deformations, coil shifts).
  - **High Frequency Band (> 100 kHz)**: Terminal leads, tap changers, bushing connections, and test grounding impedances.
- **Technical & Architectural Constraints**:
  - Backend Flask route contracts and template variable bindings in `app/app.py` (`status`, `transformerId`, `date_now`, `corr`, `shift`, `freq`, `healthy`, `faulty`, `confidence`, `fault_type`, `recommendation`) must be strictly preserved.
  - No complex frontend build pipeline: Jinja2 templates consume CDN-delivered modern assets (Tailwind CSS, Lucide icons, Chart.js) with zero node compilation overhead.

## Brand Commitments & Voice

- **Visual World**: Precision Industrial Instrument.
- **Personality**: High-trust, analytical, calm, authoritative, grounded in physics.
- **Voice**: Objective engineering telemetry. No hyperbole, no consumer SaaS fluff, no marketing filler.
- **Tone**: Laboratory grade, rigorous, precise, unambiguous.

## Evidence on Hand

- Verified standard baseline dataset: `data/raw/fra_healthy.csv`.
- Historical uploaded transformer test cases in `data/`.
- Domain glossary and ubiquitous language in `CONTEXT.md`.
- Automated test suite validating IEEE sub-band partitioning and ML model inference in `tests/`.

## Product Principles

1. **Physics First, AI Second**: Every diagnostic claim must be grounded in observable spectral evidence—frequency sub-bands, resonance zero shifts, and magnitude deviations.
2. **Dense Scanability Over Decorative Space**: Test engineers need actionable telemetry at a glance. Avoid excessive whitespace, oversized cards, and decorative empty margins.
3. **Unbroken Auditability**: Every finding must correlate to a transformer identifier, timestamp, standard reference sub-band, and exportable documentation.
4. **Resilient Simplicity**: The interface must boot instantly without fragile build tools and function smoothly across field browsers.
