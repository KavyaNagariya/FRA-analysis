# [ISSUE-004] Design Hybrid Diagnostic Fusion Logic in Analytics Engine

- **ID**: ISSUE-004
- **Type**: `wayfinder:grilling` (HITL)
- **Status**: Open
- **Assignee**: Unassigned
- **Blocked By**: ISSUE-002, ISSUE-003
- **Blocks**: ISSUE-007

---

## Question

How should `src/analyzer.py` fuse the deterministic IEEE sub-band threshold categorizations (which map frequency anomalies directly to physical components like core or windings) with the Random Forest ML prediction probabilities, and how should overall transformer health status, health integrity score (0–100%), severity, and contextual utility recommendations be calculated and returned?
