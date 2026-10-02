# [ISSUE-004] Design Hybrid Diagnostic Fusion Logic in Analytics Engine

- **ID**: ISSUE-004
- **Type**: `wayfinder:grilling` (HITL)
- **Status**: Closed
- **Assignee**: wayfinder-session
- **Blocked By**: ISSUE-002, ISSUE-003
- **Blocks**: ISSUE-007

---

## Question

How should `src/analyzer.py` fuse the deterministic IEEE sub-band threshold categorizations (which map frequency anomalies directly to physical components like core or windings) with the Random Forest ML prediction probabilities, and how should overall transformer health status, health integrity score (0–100%), severity, and contextual utility recommendations be calculated and returned?

---

## Resolution

Seven design decisions were grilled and confirmed.

### Decisions

1. **Physics vs. ML authority (Q1)**: Physics (IEEE sub-band thresholds) is the **floor**. If any sub-band's deterministic tier is worse than what the ML predicts, the overall status escalates to match the worst sub-band. The ML can *upgrade* severity (detecting patterns the threshold table misses) but can never *downgrade* it below the deterministic rules. This makes the system fail-safe — a physical anomaly is never masked by an undertrained model.

2. **Worst-band governs overall status (Q2)**: The overall health status is determined by the **worst sub-band**. If any single band (LF, MF, or HF) crosses into a worse tier, the transformer's overall status matches that tier. No averaging or quorum. The triggering band and its physical component (core/winding/leads) are named in the output.

3. **Health Integrity Score formula (Q3)**: Composite score blending physics and ML:
   ```
   score = 0.6 × min(CCF_LF, CCF_MF, CCF_HF) × 100 + 0.4 × ML_confidence_pct
   ```
   When IEEE thresholds and ML agree, the score is clean; when they disagree, the physics floor dominates (α = 0.6). Clamped to [0, 100].

4. **Severity vocabulary (Q4)**: 4-tier hybrid with user-friendly names:

   | IEEE Tier | Fusion Output | CCF Range |
   |---|---|---|
   | Normal | **Healthy** | ≥ 0.98 |
   | Warning (Slight Shift) | **Warning** | 0.90 – 0.98 |
   | Obvious Deformation | **Danger** | 0.75 – 0.90 |
   | Severe Fault | **Critical** | < 0.75 |

5. **Contextual recommendations — both overall and per-band (Q5)**: The output includes an **overall recommendation** (operator action: continue monitoring / schedule DGA / restrict load / isolate immediately) plus a **per-band breakdown** identifying which component (core, winding, leads/insulation) is flagged and the corresponding physical interpretation from ISSUE-001.

6. **Insufficient Data bands excluded, flagged (Q6)**: Sub-bands with `"Insufficient Data"` (< 10 valid points per ISSUE-002 policy) are **excluded from scoring** — they do not affect the overall tier. A `data_quality_warnings` list names any insufficient bands so the user knows the diagnosis is partial. No false escalation on missing data.

7. **Output shape — nested dict (Q7)**: `advanced_analysis()` returns a structured nested dict separating concerns:
   ```python
   {
       "diagnosis": {
           "status": "Warning",           # 4-tier: Healthy/Warning/Danger/Critical
           "severity": "Warning",          # same vocabulary
           "integrity_score": 82.5,        # 0–100 composite
           "fault_type": "Winding Deformation",  # ML prediction
           "ml_confidence": 87.3,          # RF confidence %
           "recommendation": "Minor deviation detected. Schedule DGA..."
       },
       "per_band": {
           "LF": {"status": "Healthy", "CCF": 0.99, "ASLE_dB": 0.3, "MaxDev_dB": 1.1,
                   "component": "Core", "recommendation": "Core geometry intact."},
           "MF": {"status": "Warning", "CCF": 0.94, "ASLE_dB": 1.2, "MaxDev_dB": 3.4,
                   "component": "Winding", "recommendation": "Schedule short-circuit impedance test."},
           "HF": {"status": "Insufficient Data", "component": "Leads/Insulation"}
       },
       "chart_data": {
           "frequencies": [...],
           "magnitude_healthy": [...],
           "magnitude_uploaded": [...]
       },
       "data_quality": {
           "warnings": ["HF band: Insufficient Data (sweep does not extend above 100 kHz)"],
           "bands_evaluated": ["LF", "MF"],
           "bands_insufficient": ["HF"]
       }
   }
   ```

### Downstream Impact

- **ISSUE-007** (Web Dashboard Sub-band UI) is now **unblocked**. The dashboard can consume `diagnosis` for status cards, `per_band` for the component breakdown, and `chart_data` for the Bode plot.
- **ISSUE-006** (PDF Reporting) can also consume the nested dict — `per_band` maps directly to the Sub-band Diagnostic Breakdown table.
