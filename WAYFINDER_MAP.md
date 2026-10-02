# Wayfinder Map: FRA Diagnostics Platform Improvement

**Label**: `wayfinder:map`  
**Status**: Active  
**Tracker**: Local Markdown (`.issues/`)

---

## Destination

Transform FRA Diagnostics into a robust, standard-aligned (IEEE Std C57.149 / IEC 60076-18) transformer analysis platform featuring realistic multi-class machine learning, sub-band spectral diagnostics (Core, Winding, and High-Frequency bands), unified interpolation and preprocessing pipelines, and comprehensive PDF diagnostic reporting with embedded Bode plots.

---

## Notes

- **Domain**: Transformer condition monitoring via Sweep Frequency Response Analysis (SFRA). Refer to [CONTEXT.md](file:///C:/repositories/Hackathon/FRA-data/FRA_AI_Data/CONTEXT.md) for domain glossary.
- **Skills to Consult**: `/domain-modeling`, `/grilling`, `/prototype`, `/research`, `/tdd`.
- **Standing Preferences**:
  - Prefer explainable sub-band physics and hybrid diagnostic fusion over black-box predictions.
  - Maintain backward compatibility with standard 2-column CSV/Excel sweeps.
  - Adhere to IEEE Std C57.149-2012 and IEC 60076-18 standard definitions.
  - Ensure all signal processing uses logarithmic frequency alignment.

---

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->
- [[ISSUE-001] Define Sub-band Frequency Boundaries and Mathematical Metrics (IEEE C57.149 / IEC 60076-18)](.issues/ISSUE-001-ieee-subband-boundaries-and-metrics.md) — Standardized on 3-band IEEE C57.149/CIGRE model (LF <2 kHz: core, MF 2 kHz–100 kHz: winding, HF >100 kHz: leads/insulation) with CCF, ASLE, and MaxDev thresholds (>0.98 Healthy, 0.90–0.98 Warning, <0.90 Fault).
- [[ISSUE-002] Design Logarithmic Frequency Interpolation & Preprocessing Pipeline](.issues/ISSUE-002-log-interpolation-and-preprocessing.md) — 500-pt log grid (20 Hz–1 MHz), cubic dB-space interpolation, pipeline: clean→smooth(native)→interp(common)→normalize, NaN carried through with ≥10-point sub-band minimum, DataFrame output with .attrs metadata.
- [[ISSUE-003] Multi-Class Feature Extraction and Training Pipeline](.issues/ISSUE-003-multiclass-dataset-training-pipeline.md) — 400-sample synthetic paired-sweep generator with physics-grounded fault injection; 12-feature signature (CCF + ASLE + MaxDev + Variance × 3 bands); RandomForest 4-class classifier (Healthy/Winding Deformation/Insulation Degradation/Core Displacement) at 100% on held-out set; `predict_fault()` returns (type, confidence, per-band metrics).
- [[ISSUE-004] Design Hybrid Diagnostic Fusion Logic in Analytics Engine](.issues/ISSUE-004-hybrid-diagnostic-fusion-logic.md) — Physics floor + ML escalation: worst sub-band IEEE tier governs overall status (never masked by ML); composite integrity score (60% min-CCF + 40% ML confidence); 4-tier severity (Healthy/Warning/Danger/Critical); per-band + overall recommendations; Insufficient Data bands excluded and flagged; nested dict output separating diagnosis/per_band/chart_data/data_quality.
- [[ISSUE-005] Design Multi-Asset Ingestion and Parsing Logic](.issues/ISSUE-005-multi-asset-csv-ingestion.md) — Identify keywords (`freq`, `mag`, `phase`) versus metadata columns; if metadata columns exist, groupby to segment multiple distinct sweeps into a list of dictionaries; if none, treat as a single sweep.
- [[ISSUE-006] Enrich PDF ReportLab Diagnostics and Bode Plot Embedding](.issues/ISSUE-006-enrich-pdf-reporting-with-bode-plots.md) — Use `io.BytesIO` to decode the base64 Bode plot from the plotter and embed it using ReportLab's `Image` class. Include a Sub-band Diagnostic Breakdown table for Core, Winding, and Insulation metrics alongside IEEE C57.149 compliance notes and metadata.

---

## Not yet specified

<!-- Fog of war: in-scope fog you can't ticket yet; graduates as the frontier advances -->
- **Automated DGA Cross-Correlation**: Automated linkage between Dissolved Gas Analysis data (e.g., Rogers ratios, Duval triangle) and FRA spectral fault severity.
- **Historical Degradation Trend Engine**: Mathematical tracking of drift across periodic historical scans for the same transformer serial number.
- **Phase-to-Phase Comparative Diagnosis**: Comparative analysis across 3-phase windings (Phase A vs. B vs. C) when no baseline curve exists.

---

## Out of scope

<!-- Out of scope: work ruled beyond the destination; closed, never graduates -->
- **Live Telemetry & IoT Sensor Streaming**: In-service online FRA acquisition streaming over MQTT/Modbus. The platform explicitly targets offline sweep test files.
- **Hardware Instrument Firmware / USB Acquisition Drivers**: Interfacing directly with FRA test bench hardware (e.g., Omicron FRAnalyzer, Doble M5400).
- [[ISSUE-007] Web Dashboard Sub-band Visualizations and Metrics UI](.issues/ISSUE-007-web-dashboard-subband-ui.md) — Frontend and dashboard design are currently being handled by a separate agent.
- **Interactive Multi-Band Canvas** — Frontend and dashboard design are currently being handled by a separate agent.
