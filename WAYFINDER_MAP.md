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
*(No tickets resolved yet)*

---

## Not yet specified

<!-- Fog of war: in-scope fog you can't ticket yet; graduates as the frontier advances -->
- **Automated DGA Cross-Correlation**: Automated linkage between Dissolved Gas Analysis data (e.g., Rogers ratios, Duval triangle) and FRA spectral fault severity.
- **Historical Degradation Trend Engine**: Mathematical tracking of drift across periodic historical scans for the same transformer serial number.
- **Phase-to-Phase Comparative Diagnosis**: Comparative analysis across 3-phase windings (Phase A vs. B vs. C) when no baseline curve exists.
- **Interactive Multi-Band Canvas**: Visual band markers (Core / Winding / Leads) with toggleable frequency filters directly on Chart.js.

---

## Out of scope

<!-- Out of scope: work ruled beyond the destination; closed, never graduates -->
- **Live Telemetry & IoT Sensor Streaming**: In-service online FRA acquisition streaming over MQTT/Modbus. The platform explicitly targets offline sweep test files.
- **Hardware Instrument Firmware / USB Acquisition Drivers**: Interfacing directly with FRA test bench hardware (e.g., Omicron FRAnalyzer, Doble M5400).
