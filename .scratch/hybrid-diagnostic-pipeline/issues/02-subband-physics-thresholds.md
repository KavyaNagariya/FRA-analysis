# 02 — Evaluate IEEE C57.149 Sub-Band Physics Thresholds

**What to build:** The diagnostic engine evaluates FRA data across three distinct IEEE sub-bands (Low/Core, Mid/Winding, High/Insulation). The system determines overall status governed strictly by the worst-performing sub-band, preventing severe component issues from being diluted. The output JSON is expanded to include a `per_band` breakdown dictionary.

**Blocked by:** 01 — Standardize CSV Preprocessing with 500-Point Logarithmic Interpolation

**Status:** completed

- [x] Sub-bands are properly segmented based on standard IEEE C57.149 boundaries.
- [x] CCF and MaxDev metrics are correctly computed for each sub-band.
- [x] The overall severity is determined by the worst-performing sub-band (Healthy, Warning, Danger, Critical).
- [x] Sub-bands with fewer than 10 data points are automatically excluded and flagged as "Insufficient Data".
