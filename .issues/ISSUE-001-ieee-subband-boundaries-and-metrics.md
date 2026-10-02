# [ISSUE-001] Define Sub-band Frequency Boundaries and Mathematical Metrics (IEEE C57.149 / IEC 60076-18)

- **ID**: ISSUE-001
- **Type**: `wayfinder:research` (AFK)
- **Status**: Closed
- **Assignee**: research-agent
- **Blocked By**: None
- **Blocks**: ISSUE-002, ISSUE-003, ISSUE-006

---

## Question

What are the standard frequency boundary cuts (Low, Medium, High bands) and quantitative metric formulas (such as Cross-Correlation Factor $CCF$, Absolute Sum of Logarithmic Error $ASLE$, and standard dB deviation bounds) defined by IEEE Std C57.149 and IEC 60076-18, and what are their standard numerical threshold ranges for categorizing transformer condition into Normal, Warning, and Fault/Severe states?

---

## Resolution

Based on harmonized standards **IEEE Std C57.149-2012** (Clause 7), **IEC 60076-18:2012** (Annex B), **CIGRE TB 342**, and **DL/T 911**:

### 1. Standard Sub-Band Frequency Boundaries
- **Low Frequency Band (LF: 20 Hz – 2 kHz)**: Governed by core magnetizing inductance ($L_m$) and magnetic circuit geometry. Detects core displacement, broken/multiple core grounds, and magnetic circuit defects.
- **Medium Frequency Band (MF: 2 kHz – 100 kHz)**: Governed by winding self/mutual inductances and inter-winding capacitances ($C_{HL}$). Detects radial hoop buckling, axial winding displacement, and coil collapse.
- **High Frequency Band (HF: 100 kHz – 1 MHz)**: Governed by series capacitance ($C_s$) and leakage inductances. Detects localized disc displacement, turn-to-turn insulation degradation, and lead/tap anomalies.
- *(Frequencies > 1 MHz are treated as Very High Frequency (VHF) / setup-sensitive and filtered to avoid false positives).*

### 2. Standard Mathematical Diagnostic Metrics
1. **Cross-Correlation Factor (CCF / $\rho$)**:
   $$\text{CCF} = \frac{\sum_{i=1}^{N} (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{N} (X_i - \bar{X})^2 \sum_{i=1}^{N} (Y_i - \bar{Y})^2}}$$
2. **Absolute Sum of Logarithmic Error (ASLE / Mean Absolute $\Delta\text{dB}$)**:
   $$\text{ASLE} = \frac{1}{N} \sum_{i=1}^{N} \left| Y_{i, \text{dB}} - X_{i, \text{dB}} \right|$$
3. **Maximum Absolute Deviation ($\Delta\text{dB}_{\max}$)**:
   $$\Delta\text{dB}_{\max} = \max_{i} \left| Y_{i, \text{dB}} - X_{i, \text{dB}} \right|$$

### 3. Quantitative Decision Thresholds

| Health State | CCF ($\rho$) | ASLE (Mean $\Delta\text{dB}$) | Max Deviation ($\Delta\text{dB}_{\max}$) | Physical Condition & Action |
| :--- | :--- | :--- | :--- | :--- |
| **Normal / Healthy** | $\ge 0.98$ | $< 0.6\text{ dB}$ | $< 2.0\text{ dB}$ | Core and winding geometry intact. Continue standard annual maintenance. |
| **Warning (Slight Shift)** | $0.90 \le \text{CCF} < 0.98$ | $0.6 - 2.0\text{ dB}$ | $2.0 - 5.0\text{ dB}$ | Minor deviation. Schedule DGA, check test grounding, re-test in 3–6 months. |
| **Obvious Deformation** | $0.75 \le \text{CCF} < 0.90$ | $2.0 - 3.5\text{ dB}$ | $5.0 - 8.0\text{ dB}$ | Noticeable coil distortion. Restrict loading to 80%, inspect within 30 days. |
| **Severe Fault / Failure**| $< 0.75$ | $\ge 3.5\text{ dB}$ | $\ge 8.0\text{ dB}$ | Severe mechanical failure / short circuit. Immediate isolation & internal tank inspection. |
