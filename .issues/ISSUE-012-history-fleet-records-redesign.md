# [ISSUE-012] Redesign Analysis History & Fleet Records Console (`history.html`)

- **ID**: ISSUE-012
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked By**: None
- **Blocks**: ISSUE-015

---

## Question

How should `app/templates/history.html` be transformed from a basic table into a high-density industrial fleet management console, featuring telemetry summary metrics, severity filtering, search by transformer ID, and instant inspection links?

---

## Resolution

The Analysis History & Fleet Records console was completely re-architected into a high-density industrial fleet surveillance and audit workstation in [`app/templates/history.html`](../app/templates/history.html), integrating with the unified master avionics shell [`app/templates/base.html`](../app/templates/base.html) and enhanced backend telemetry in [`app/app.py`](../app/app.py):

1. **Precision Industrial Shell Integration**:
   - Inherits master avionics layout from `base.html` with persistent Left Vertical Avionics Rail highlighting `FLEET RECORDS` (`active_page='history'`).
   - Sticky context header with asset serial breadcrumb, IEEE C57.149 standard certification badge, and instant action buttons.

2. **5-Column Fleet Telemetry Ribbon**:
   - **Total Assets**: 6 tracked units across 8 substations.
   - **Nominal Baseline**: 2 verified units ($R^2 \ge 0.95$) with phosphor emerald beacon.
   - **Advisory Warning**: 2 watchlist units ($0.85 \le R^2 < 0.95$) with phosphor amber beacon.
   - **Critical Alarm**: 2 urgent action units ($R^2 < 0.85$) with phosphor rose active beacon.
   - **Fleet Mean $R^2$ / Health**: Real-time fleet average correlation score ($0.8791$) with 71% Health Integrity Index progress bar.

3. **Interactive Control, Search & Filter Matrix**:
   - **Instant Text Filter**: Real-time client-side search across Transformer ID, Substation, Voltage rating, and Fault mechanism.
   - **Severity Status Segmented Controller**: Instant toggle pills (`ALL (6)`, `NOMINAL (2)`, `WARNING (2)`, `CRITICAL (2)`) with active state counters.
   - **IEEE Sub-band Quick Filters**: Dedicated filter pills for `ALL BANDS`, `CORE <2kHz`, `WINDING 2k-100kHz`, and `LEADS >100kHz`.
   - **Results Counter**: Dynamic readout (`Showing X / Y records`) with empty-state zero-match handler.

4. **High-Density Telemetry Records Table**:
   - 8-column tabular grid with JetBrains Mono numbers, tight 1px borders, and dark obsidian/charcoal surfaces.
   - Displays Asset Serial, Voltage/MVA rating, Test Timestamp, Health Integrity Index gauge meter, Diagnostic Status with pulse beacon, Identified Failure Mechanism, Affected Sub-band tag, and Dual Telemetry readout ($R^2$ and $|\Delta\text{dB}|$).
   - **Instant Action Deck**:
     - `INSPECT`: Instant single-click direct link to `/inspect/<asset_id>` which immediately loads the asset into the SFRA Diagnostic Workbench (`index.html`) with interactive Bode plot, sub-band cards, and health gauge.
     - `EXPAND / DETAILS`: Toggles inline expandable audit drawer.
     - `EXPORT CSV`: Instant client-side generation and download of filtered fleet records.

5. **Inline Expandable Audit & Reasoning Drawer**:
   - Clicking any table row reveals a 3-bay audit panel:
     - **Bay A**: Mechanical Diagnosis & Recommended Engineering Action with sign-off authority.
     - **Bay B**: IEEE C57.149 sub-band localized correlation matrix ($R^2_{low}$, $R^2_{mid}$, $R^2_{high}$).
     - **Bay C**: Audit artifacts trace (baseline file, source sweep, standards compliance) and direct workbench link.

6. **Direct Substation Data Ingestion Station**:
   - Bottom quick-drop zone allowing field engineers with raw Omicron or Doble CSV sweeps to jump directly to the analysis upload station.
