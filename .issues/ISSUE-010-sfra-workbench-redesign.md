# [ISSUE-010] Redesign Flagship SFRA Diagnostic Workbench (`index.html`)

- **ID**: ISSUE-010
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked By**: None
- **Blocks**: ISSUE-011, ISSUE-015

---

## Question

How should `app/templates/index.html` be re-architected to present an authoritative engineering workbench, integrating the file upload station, asset telemetry banner, composite asset health gauge, multi-class ML classification results, per-band IEEE status cards, and actionable remediation checklists?

---

## Resolution

Successfully architected, prototyped, and verified the precision industrial SFRA Diagnostic Workbench in [`app/templates/index.html`](../app/templates/index.html), extending [`app/templates/base.html`](../app/templates/base.html):

1. **State Architecture & UX Flow**:
   - **Two-State System**: Standby/Upload Station (when `status` is None) and Results Diagnostic Deck (when `status` is populated).
   - **Upload Station**: Industrial-grade dropzone with tactile corner crosshair reticles, monospace format notes, and single-click file selector.
   - **Compact Re-Scan Strip**: When viewing results, a 40px top strip allows immediate single-click re-analysis without losing context.

2. **Telemetry Layout & Grid Structure**:
   - **4-Column Metric Ribbon**: Dense glanceable telemetry covering Bandwidth (`20 Hz - 2 MHz`), Correlation $R^2$, Max Shift $|\Delta\text{dB}|$, and Overall Status with phosphor beacon.
   - **Asymmetric Grid (`1fr | 380px`)**:
     - Left Bay: Magnitude Response Bode Plot canvas (460px height) + 3-column horizontal IEEE Sub-band cards (Low Core `<2kHz`, Mid Winding `2kHz-100kHz`, High Leads `>100kHz`).
     - Right Bay (380px Rail): Health Integrity Index half-doughnut gauge with large monospace readout, ML Multi-class classification breakdown bar, actionable remediation guidance panel, and one-click PDF report export.

3. **Domain & Standards Grounding**:
   - Client-side sub-band statistical computation calculating localized $R^2$ and peak $|\Delta\text{dB}|$ across standard IEEE C57.149 boundary slices (`< 2 kHz`, `2 kHz - 100 kHz`, `> 100 kHz`) with NOMINAL / DEVIATION / CRITICAL status badges.
   - Verified via live DevTools inspection and end-to-end form POST pipeline execution.

4. **Downstream Unblocking**:
   - Unblocks [ISSUE-011](ISSUE-011-subband-bode-plot-canvas.md) for deeper interactive crosshairs/residual features, and moves [ISSUE-015](ISSUE-015-impeccable-audit-and-visual-verification.md) closer to full audit readiness.

