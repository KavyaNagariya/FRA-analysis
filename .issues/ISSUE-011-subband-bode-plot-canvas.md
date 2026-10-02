# [ISSUE-011] Build Interactive IEEE C57.149 Sub-band Logarithmic Bode Plot Component

- **ID**: ISSUE-011
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked By**: None
- **Blocks**: ISSUE-015

---

## Question

How should the Chart.js / HTML5 Canvas Bode plot component render logarithmic frequency scaling (20 Hz - 1 MHz), shaded IEEE sub-bands (Low Frequency Core <2kHz, Medium Frequency Winding 2kHz-100kHz, High Frequency Leads/Insulation >100kHz), interactive cursor crosshairs, and toggleable $|\Delta\text{dB}|$ residual trace?

---

## Resolution

The Chart.js / HTML5 Canvas Bode plot component was implemented directly within the Flagship SFRA Diagnostic Workbench (`app/templates/index.html`) with the following precision instrument features:

1. **Precision Toolbar & Trace Toggles**:
   - **Baseline Trace**: `#8b5cf6` (phosphor violet, dashed line) toggleable via header button.
   - **Test Sweep Trace**: `#06b6d4` (phosphor cyan, solid 2px line) toggleable via header button.
   - **$|\Delta\text{dB}|$ Residual Trace**: `#f59e0b` (phosphor amber, dashed line with semi-transparent fill `rgba(245, 158, 11, 0.08)`) rendered on a dedicated secondary right Y-axis `yDelta` (0 to 30 dB), toggleable on-demand.
   - **Sub-bands Overlay**: Toggleable on/off button controlling IEEE sub-band tinted zones.

2. **IEEE Std C57.149 Sub-band Visual Shading Plugin**:
   - Custom `subbandShading` Chart.js canvas plugin rendering:
     - **Low Frequency (Core Inductance)**: 20 Hz – 2,000 Hz in `rgba(245, 158, 11, 0.06)` with label `CORE (<2kHz)`.
     - **Mid Frequency (Winding Resonance)**: 2,000 Hz – 100,000 Hz in `rgba(6, 182, 212, 0.06)` with label `WINDING (2k–100kHz)`.
     - **High Frequency (Leads & Terminals)**: 100,000 Hz – 2,000,000 Hz in `rgba(139, 92, 246, 0.06)` with label `LEADS (>100kHz)`.
     - 1px dashed boundary demarcation lines at exactly 2,000 Hz and 100,000 Hz.

3. **Interactive Cursor Crosshairs & Dynamic Telemetry HUD**:
   - Custom `crosshairOverlay` plugin drawing synchronized 2D reticle lines tracking mouse position across the canvas.
   - Real-time Cursor Telemetry HUD bar positioned immediately above the canvas displaying:
     - `CURSOR FREQ`: e.g. `24.50 kHz` (formatted logarithmic frequency with auto-scaling units Hz/kHz/MHz).
     - `SUB-BAND`: Current IEEE sub-band classification (`LOW FREQ: CORE`, `MID FREQ: WINDING`, `HIGH FREQ: LEADS`).
     - `BASE`: Baseline magnitude in dB.
     - `TEST`: Uploaded test sweep magnitude in dB.
     - `|ΔdB|`: Absolute deviation with color coding (emerald `<3.0 dB`, amber `3.0–6.0 dB`, rose `≥6.0 dB`).

4. **Sub-band Focus / Quick Zoom**:
   - Quick-zoom buttons (`FULL`, `CORE <2k`, `WINDING 2k-100k`, `LEADS >100k`) allowing instant logarithmic scale re-framing for deep inspection of localized winding or core anomalies.
