# [ISSUE-002] Design Logarithmic Frequency Interpolation & Preprocessing Pipeline

- **ID**: ISSUE-002
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Open
- **Assignee**: Unassigned
- **Blocked By**: ISSUE-001
- **Blocks**: ISSUE-003, ISSUE-004

---

## Question

How should test sweeps and baseline sweeps with disparate frequency sampling points or non-uniform frequency intervals be aligned onto a common logarithmic frequency grid (e.g. 500 decade-balanced points), and how should Savitzky-Golay filtering and NaN/noise cleaning from `src/preprocessor.py` be unified into the ingestion workflow so both the analytics engine and visualizer receive clean, aligned data?
