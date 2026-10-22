# [ISSUE-013] Redesign IEEE C57.149 Reference & SFRA Diagnostic Guide (`about.html`)

- **ID**: ISSUE-013
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked By**: None
- **Blocks**: ISSUE-015

---

## Question

How should `app/templates/about.html` be elevated into an interactive, authoritative engineering manual explaining SFRA physical principles, circuit models (RLC networks), IEEE Std C57.149 / IEC 60076-18 sub-band criteria, and mathematical correlation metrics (CCF / ASLE)?

---

## Resolution

The platform knowledge base was completely re-architected from a generic marketing placeholder into an authoritative, interactive engineering reference manual in [`app/templates/about.html`](../app/templates/about.html), integrating seamlessly with the precision industrial master avionics shell [`app/templates/base.html`](../app/templates/base.html) and enhanced route bindings in [`app/app.py`](../app/app.py):

1. **Precision Industrial Shell & Spec Header**:
   - Inherits `base.html` with persistent Left Vertical Avionics Rail highlighting `STANDARDS KB` (`active_page='standards'`).
   - Sticky context sub-header with standards specification badges for `IEEE Std C57.149-2012`, `IEC 60076-18:2012`, `CIGRE WG A2.26 / TB 342`, and `DL/T 911-2016`.
   - Floating sticky sub-navigation bar providing rapid jump anchors to all 6 technical sections.

2. **Section 01: Physical Principles & Distributed RLC Circuit Model**:
   - Details physical principles of SFRA as a passive distributed-parameter linear electrical network where geometric dimensions dictate $L$ and $C$ matrices.
   - Embeds an exact SVG schematic diagram of the distributed winding ladder network showing series inductances ($L_{s1}, L_{s2}$), mutual coupling ($M_{12}$), inter-disk capacitances ($C_s$), ground capacitances ($C_g$), series resistances ($R_s$), shunt conductances ($G$), and 50$\Omega$ terminal load impedance.
   - Formulates the complex transfer function $H(j\omega) = V_{\text{out}}(j\omega)/V_{\text{in}}(j\omega)$ with magnitude and phase definitions.

3. **Section 02: IEEE Std C57.149 & IEC 60076-18 Sub-Band Decomposition**:
   - 3-bay modular card layout breaking down the physical response into standardized sub-bands:
     - **Sub-Band 1 (< 2 kHz)**: Core magnetizing inductance ($L_m$) and bulk resistance; detects core displacement, lamination shorts, and grounding anomalies ($R^2 \ge 0.95$).
     - **Sub-Band 2 (2 kHz – 100 kHz)**: Winding leakage inductance ($L_\sigma$) and inter-disk capacitance ($C_s, C_g$); detects radial buckling, axial displacement, disk tilting, and clamping loss ($R^2 \ge 0.95, \Delta f < 2\%$).
     - **Sub-Band 3 (> 100 kHz)**: Terminal leads, tap changer contacts, bushing capacitances ($C_b$), and ground braid inductances ($R^2 \ge 0.90$).

4. **Section 03: Mathematical Correlation & Analytical Formulations**:
   - High-density mathematical formulas and normative evaluation threshold tables for:
     - **Cross-Correlation Factor (CCF / $R^2$)**: Normalized pattern similarity metric with standard thresholds ($\ge 0.95$ Nominal, $0.85-0.95$ Advisory, $<0.85$ Critical).
     - **Absolute Sum of Logarithmic Error (ASLE)**: Amplitude offset metric ($<0.6\text{ dB}$ Normal, $0.6-1.5\text{ dB}$ Moderate, $\ge 1.5\text{ dB}$ Substantial).
     - **Peak Residual Deviation ($|\Delta\text{dB}_{\max}|$)**: Singular peak divergence indicator.
     - **Resonance Frequency Shift Ratio ($\Delta f / f_0$)**: Relative percentage shift of resonance poles.

5. **Section 04: Diagnostic Fault Signature Matrix (Engineering Reference Table)**:
   - Comprehensive 4-column matrix correlating 7 major mechanical failure mechanisms to their dominant frequency sub-bands, characteristic SFRA curve manifestations, and field verification protocols (LVLR, excitation current, TTR, DGA, Megohmmeter core-to-tank test, dynamic resistance).

6. **Section 05: Standardized Test Configurations & Field Grounding Protocols**:
   - 4-card operational guide detailing End-to-End Open Circuit, End-to-End Short Circuit, Inter-Winding Capacitive, and the mandatory $<100\text{mm}$ flat braided copper grounding strap rule to prevent high-frequency measurement artifacts.

7. **Section 06: Interactive Sub-band Criteria Simulator & Evaluation Engine**:
   - Live client-side instrument tool allowing field engineers to test IEEE C57.149 diagnostic logic interactively.
   - Features real-time sliders for Sub-band Correlation ($R^2$), Peak Decibel Deviation ($|\Delta\text{dB}|$), Frequency Shift ($\Delta f / f_0$), and Sub-band selector pills.
   - Includes 5 one-click diagnostic presets: *Nominal Factory Baseline*, *Radial Winding Buckling*, *Core Lamination Shift*, *Tap / Lead Disconnect*, and *Ground Braid Artifact*.
   - Dynamically calculates and displays:
     - IEEE C57.149 Diagnostic Verdict with pulsing active beacon and badge (`NOMINAL (PASS)`, `ADVISORY (MONITOR)`, `CRITICAL (ALARM)`).
     - Health Integrity Index (HII) gauge meter ($0-100\%$).
     - Physical Fault Diagnosis and IEEE compliance audit text.
     - Context-aware Recommended Engineering Action protocol and direct link to SFRA Diagnostic Workbench.
