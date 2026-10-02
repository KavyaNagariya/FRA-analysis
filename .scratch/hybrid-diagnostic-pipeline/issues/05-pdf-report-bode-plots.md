# 05 — Enriched PDF Reporting with Bode Plots and Sub-band Tables

**What to build:** The downloadable PDF export is upgraded to serve as a comprehensive, standards-compliant record of the inspection. It embeds a high-resolution base64 Bode plot comparing baseline and measured data, alongside a clear Sub-band Diagnostic Breakdown table containing component-level metrics and the overall Health Integrity Score.

**Blocked by:** 02 — Evaluate IEEE C57.149 Sub-Band Physics Thresholds, 03 — Hybrid Fusion Engine and Health Integrity Score

**Status:** completed

- [x] The reporting module accepts a base64 encoded Bode plot string and successfully decodes/embeds it into the PDF.
- [x] The PDF includes a detailed Sub-band Diagnostic Breakdown table displaying metrics (CCF, Max Dev) and status for Low, Mid, and High bands.
- [x] Actionable recommendations and the Health Integrity Score are prominently displayed.
