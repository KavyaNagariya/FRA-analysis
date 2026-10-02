# 01 — Standardize CSV Preprocessing with 500-Point Logarithmic Interpolation

**What to build:** End-to-end data standardization. When a user uploads a raw CSV (with differing resolutions or frequency scales), the system cleans, smooths, and interpolates it to a standard 500-point logarithmic grid (20 Hz - 1 MHz). The resulting standard grid flows through the existing analyzer and updates the chart output to have uniform frequency spacing.

**Blocked by:** None — can start immediately

**Status:** closed

- [ ] Preprocessing module standardizes input frequency arrays to exactly 500 logarithmically spaced points between 20 Hz and 1 MHz.
- [ ] The pipeline seamlessly handles missing data (`NaN`) via cubic dB-space interpolation without failing.
- [ ] The analyzer and output charts accurately reflect the new 500-point uniform grid.
