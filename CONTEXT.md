# FRA Domain Glossary & Ubiquitous Language

## Core Concepts

### Sweep Frequency Response Analysis (SFRA / FRA)
A non-destructive diagnostic method used to evaluate the mechanical and electrical integrity of power transformers by injecting a low-voltage sinusoidal signal across a wide frequency range (typically 20 Hz to 2 MHz) and measuring the transferred response.

### Healthy Baseline
A reference frequency response signature captured when the transformer was in a known healthy condition (e.g., at factory commissioning, prior to transport, or post-refurbishment). All subsequent field tests are comparatively assessed against this curve.

### Diagnostic Sub-bands (IEEE Std C57.149 / IEC 60076-18)
Standardized frequency regions associated with specific internal transformer components:
- **Low Frequency Band (< 2 kHz)**: Governed primarily by main core magnetizing inductance and magnetic circuit geometry. Deviations indicate core displacement or core grounding anomalies.
- **Medium Frequency Band (2 kHz – 100 kHz)**: Governed by winding inductance and inter-winding/ground capacitance. Deviations indicate axial/radial winding deformations or coil shifts.
- **High Frequency Band (> 100 kHz)**: Governed by winding terminal leads, tap changers, and measurement setup/grounding impedances. Deviations reflect loose leads or measurement artifacts.

## Fault Classifications

### Winding Deformation
Mechanical distortion, axial collapse, radial bucking, or physical displacement of the winding coils caused by electromagnetic forces during short-circuit faults or mechanical transit shocks.

### Core Displacement
Movement, shifting, or unintended multiple grounds of the transformer laminated core assembly, typically manifesting as significant shifts in the low-frequency inductive resonance peaks.

### Insulation Degradation
Aging, moisture ingress, or dielectric deterioration of transformer paper and oil insulation, causing permittivity changes and subtle capacitance variations across mid-to-high frequency bands.

### Loose Connection
High contact resistance or loose contact in winding terminations, tap leads, or bushings, introducing damping and deviations in characteristic resonance troughs.

## Diagnostic Metrics

### Sub-band Correlation Coefficient ($R^2$ / $\rho$)
Statistical cross-correlation between baseline and test magnitude vectors computed separately within each standard frequency sub-band to pinpoint localized structural anomalies.

### Maximum Magnitude Deviation ($\Delta \text{dB}$)
The peak absolute decibel difference between baseline and test signals across the frequency sweep or within an individual sub-band.

### Resonance Peak Frequency Shift ($\Delta f$)
The shift in frequency location of characteristic resonance peaks and anti-resonance zeros resulting from changes in internal $L$ and $C$ parameters.
