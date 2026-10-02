---
labels: ready-for-agent
---

# Specification: IEEE-Compliant Hybrid FRA Diagnostic Pipeline

## Problem Statement

Transformer operators and diagnostic engineers currently lack a robust, standards-aligned platform for analyzing Sweep Frequency Response Analysis (SFRA) data. Existing ingestion methods fail when provided with multi-asset CSV files containing metadata, mixing discrete test sweeps together. Preprocessing routines do not standardize to the industry-expected logarithmic frequency scale, making comparisons error-prone. The current diagnostic engine relies too heavily on opaque machine learning, ignoring the deterministic, physics-based sub-band boundaries defined by IEEE C57.149 and IEC 60076-18. Furthermore, the exported PDF reports do not include high-resolution Bode comparison plots or a clear breakdown of component-level health, failing to provide technicians with the visual and numerical evidence required to justify maintenance decisions.

## Solution

Transform the FRA Diagnostics platform into a comprehensive, IEEE C57.149 / IEC 60076-18 compliant analysis tool. This encompasses intelligent CSV ingestion that detects and splits multi-asset data, logarithmic frequency interpolation for standardized preprocessing, and a hybrid diagnostic engine. The new analytics engine enforces deterministic physics thresholds as an absolute floor—ensuring critical physical deformations are never masked by the machine learning model—while still leveraging a trained Random Forest classifier to identify complex fault signatures. The end product is an enriched, downloadable PDF report that automatically embeds a generated Bode plot and provides a detailed sub-band diagnostic breakdown (Core, Winding, and Insulation).

## User Stories

1. As a transformer analyst, I want the system to automatically detect and group multi-asset CSV files by metadata, so that I can upload a single file containing multiple tests without the data bleeding together into one invalid sweep.
2. As a transformer analyst, I want the system to handle single-sweep CSV files seamlessly even without explicit metadata columns, so that I can process simple, raw extracts without manual reformatting.
3. As a diagnostic engineer, I want the frequency data to be logarithmically interpolated to a standard 500-point grid, so that I can accurately compare sweeps with differing resolutions or frequency scales.
4. As a diagnostic engineer, I want the system to evaluate FRA data across three distinct IEEE C57.149 sub-bands (Low/Core, Mid/Winding, High/Insulation), so that I can trace a frequency anomaly back to a specific physical component of the transformer.
5. As a reliability manager, I want the diagnostic engine to use deterministic physics thresholds (CCF, ASLE, MaxDev) as a definitive baseline, so that I can trust a critical physical deformation is never masked or overridden by an overly-optimistic machine learning model.
6. As a reliability manager, I want the overall transformer health status to be governed strictly by the worst-performing sub-band, so that a severe winding issue isn't diluted by perfectly healthy core and insulation readings.
7. As a data scientist, I want the Random Forest ML classifier to train on a robust synthetic dataset with injected, physics-grounded faults, so that it can confidently distinguish between Healthy, Winding Deformation, Insulation Degradation, and Core Displacement.
8. As a transformer operator, I want to see a single composite Health Integrity Score (0-100%) that blends physics minimums and ML confidence, so that I can quickly assess the overall integrity of the asset at a glance.
9. As a transformer operator, I want sub-bands with less than 10 data points to be automatically excluded from the diagnosis and flagged as "Insufficient Data", so that incomplete sweeps don't artificially trigger false alarms.
10. As a field technician, I want to receive actionable, context-aware recommendations for both the overall transformer status and individual component bands, so that I know exactly whether to schedule a Dissolved Gas Analysis (DGA) or continue routine monitoring.
11. As a field technician, I want to download a comprehensive PDF report that includes an embedded Bode plot overlay of the baseline and measured data, so that I can easily share visual proof of the fault with stakeholders.
12. As a field technician, I want the PDF report to include a clear Sub-band Diagnostic Breakdown table mapping out the metrics (CCF, Max Dev) and status of each band, so that I have a documented, standard-compliant record of the inspection.

## Implementation Decisions

- **Data Ingestion Module**: Implemented logic to scan incoming file columns for measurement keywords (`freq`, `mag`, `phase`) versus metadata. If metadata columns exist, a pandas `groupby` operation is applied to segment the data into discrete sweeps returned as a list of dictionaries.
- **Preprocessing Module**: Introduced a 500-point logarithmic grid (20 Hz - 1 MHz) employing cubic dB-space interpolation. The pipeline enforces a strict sequence: clean → smooth → interpolate → normalize, carrying through `NaN` values where appropriate.
- **Machine Learning Module**: Built a Random Forest 4-class classifier utilizing a 12-feature signature (CCF, ASLE, MaxDev, and Variance extracted across the 3 IEEE sub-bands).
- **Diagnostics Fusion Engine (Analyzer)**: 
  - Designed to return a highly structured nested dictionary separating concerns: `diagnosis`, `per_band`, `chart_data`, and `data_quality`.
  - Implements the "worst-sub-band-governs" rule, ensuring that physics thresholds dictate the severity floor (Healthy, Warning, Danger, Critical). The ML model can escalate the severity but can never downgrade it.
  - The Health Integrity Score uses the formula: `0.6 × min(CCF_LF, CCF_MF, CCF_HF) × 100 + 0.4 × ML_confidence_pct`.
- **Reporting Module**: Modified to accept the nested diagnostic dictionary and a base64 encoded Bode plot from the charting module. The plotter's base64 string is decoded into an `io.BytesIO` buffer and embedded into the PDF using ReportLab's `Image` class. The PDF is enriched with a sub-band breakdown table and standard IEEE compliance notes.

## Testing Decisions

- **What makes a good test**: Tests should focus strictly on the external behavior and final output of the pipeline rather than mocking internal computational steps. A good test asserts that given a specific raw CSV input, the final generated diagnostic dictionary and PDF report match the expected structural and logical requirements (e.g., the worst band dictates the final severity).
- **Modules to be tested**: A single, end-to-end integration seam encompasses the pipeline. This seam begins at the data loader, passes data through the preprocessor and analyzer, generates the Bode plot buffer via the plotter, and finally builds the PDF report.
- **Prior Art**: This integration approach elevates any existing basic file validation tests into a comprehensive pipeline validation strategy, reducing the number of mocked boundaries and ensuring all modules interoperate correctly.

## Out of Scope

- Web Dashboard Sub-band Visualizations and Metrics UI (Frontend integration is delegated to a separate agent).
- Interactive Multi-Band Canvas (Frontend).
- Live Telemetry & IoT Sensor Streaming (System explicitly targets offline sweep files).
- Hardware Instrument Firmware / USB Acquisition Drivers.
- Automated DGA Cross-Correlation.
- Historical Degradation Trend Engine.
- Phase-to-Phase Comparative Diagnosis.

## Further Notes

- The decision to enforce the physics floor over the ML prediction is critical for safety-critical industrial applications, ensuring the system remains fail-safe.
- Maintaining compatibility with standard 2-column CSV files while supporting complex multi-asset files ensures that historical data archives can be ingested without requiring manual data wrangling by the end user.
