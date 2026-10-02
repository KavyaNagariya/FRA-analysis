---
name: FRA Diagnostics Platform
description: Precision Industrial Workstation for Transformer SFRA Telemetry & Diagnostics
colors:
  canvas-dark: "#070a0f"
  canvas-surface: "#0c1017"
  canvas-panel: "#121824"
  canvas-panel-elevated: "#172030"
  border-subtle: "#1e293b"
  border-medium: "#334155"
  border-bright: "#475569"
  text-primary: "#f8fafc"
  text-secondary: "#94a3b8"
  text-muted: "#64748b"
  telemetry-cyan: "#06b6d4"
  telemetry-emerald: "#10b981"
  telemetry-amber: "#f59e0b"
  telemetry-rose: "#f43f5e"
  telemetry-violet: "#8b5cf6"
typography:
  display:
    fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"
    fontSize: "clamp(1.5rem, 3vw, 2.25rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "'Inter', system-ui, -apple-system, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  telemetry:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.02em"
  body:
    fontFamily: "'Inter', system-ui, -apple-system, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0"
  caption:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "0.05em"
rounded:
  none: "0px"
  sm: "2px"
  md: "4px"
  lg: "6px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  base: "16px"
  lg: "24px"
  xl: "32px"
components:
  telemetry-badge:
    backgroundColor: "{colors.canvas-panel}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
  instrument-button:
    backgroundColor: "{colors.canvas-panel-elevated}"
    textColor: "{colors.telemetry-cyan}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
---

# Design System: Precision Industrial Instrument

## Overview

The FRA Diagnostics visual design system is modeled on high-precision electronic measurement instruments (spectrum analyzers, precision vector network analyzers, digital storage oscilloscopes). It rejects generic SaaS trends—such as pastel gradients, floaty box shadows, bulbous 24px border radii, and low-contrast grey-on-grey text—in favor of a high-density, high-legibility, dark matte instrument aesthetic.

Every visual element encodes operational reality: 1px structural grid dividers reflect rack-mounted equipment frames; phosphor amber, emerald, and cyan accents convey operational state and test telemetry; and JetBrains Mono monospace typography provides unambiguous readouts for numerical metrics and frequency units.

---

## Colors

### Canvas & Structural Backgrounds
- **Chassis Abyss (`#070a0f`)**: Deepest substrate layer, representing the instrument console enclosure.
- **Instrument Surface (`#0c1017`)**: Base surface for navigation bars, sub-headers, and workbench toolbars.
- **Instrument Panel (`#121824`)**: Modular card and panel surface for plots, diagnostic readouts, and data grids.
- **Elevated Panel (`#172030`)**: Elevated controls, tooltips, active tab selections, and flyout overlays.

### Structural Grid & Borders
- **Subtle Divider (`#1e293b`)**: 1px structural grid lines dividing bays, charts, and telemetry meters.
- **Interactive Border (`#334155`)**: Focus rings, button perimeters, and active container boundaries.
- **Emphasized Border (`#475569`)**: Highlights active measurement cursors or selected frequency sub-bands.

### Phosphor Telemetry & Semantic Accents
- **Test Probe Cyan (`#06b6d4`)**: Active test trace, measurement cursor readouts, primary actions, and frequency markers.
- **CRT Phosphor Emerald (`#10b981`)**: Normal/Healthy condition, high baseline correlation ($R^2 \ge 0.95$), system ready status.
- **Laboratory Phosphor Amber (`#f59e0b`)**: Warning threshold ($0.85 \le R^2 < 0.95$), slight resonance frequency shift, moderate deviation.
- **Critical Alarm Rose (`#f43f5e`)**: Danger/Critical condition ($R^2 < 0.85$), severe mechanical winding deformation, core displacement.
- **Baseline Reference Violet (`#8b5cf6`)**: Historical benchmark baseline trace curve on the Bode plot canvas.

### Typography & Text Readability
- **Primary Text (`#f8fafc`)**: Metric values, headings, active test identifiers, critical alerts.
- **Secondary Text (`#94a3b8`)**: Unit labels (Hz, dB, %), sub-band descriptors, metadata timestamps.
- **Muted Text (`#64748b`)**: Inactive tab labels, placeholder text, secondary guide ticks.

---

## Typography

The interface employs a strict dual-typeface architecture:

1. **Telemetry & Data Numerics**: `JetBrains Mono` (fallback: `Fira Code`, `Consolas`, monospace).
   - Used for all numerical values, test frequencies, decibel shifts, correlation metrics, timestamps, unit serial numbers, and table columns.
   - Fixed-pitch alignment ensures tabular numbers do not jitter during live scanning or cursor inspection.
2. **Interface & Prose Content**: `Inter` (fallback: `system-ui`, `-apple-system`, `sans-serif`).
   - Used for navigation labels, section headings, diagnostic explanations, recommendations, and standard references.

### Typographic Hierarchy Scale
- **Display Readout** (`clamp(1.5rem, 3vw, 2.25rem)` / 700 / Monospace): Primary diagnostic state and headline metrics.
- **Panel Headline** (`1.125rem` / 600 / Sans): Panel and card headers, module titles.
- **Metric Value** (`1.25rem` - `1.5rem` / 700 / Monospace): Health integrity percentage, correlation scores, decibel deviations.
- **Metric Label** (`0.6875rem` / 600 / Monospace / Uppercase / Tracking-wide): Metric field titles ("CORRELATION R²", "MAX SHIFT ΔdB", "BANDWIDTH").
- **Body Telemetry** (`0.875rem` / 400 / Sans): Recommendations, fault diagnostic rationales, standard clause descriptions.
- **Status Eyebrow** (`0.625rem` / 700 / Monospace / Tracking-wider): IEEE compliance tags, instrument mode indicators.

---

## Layout

### Spatial Geometry & Responsive Grid
- **Master Telemetry Deck**: Fixed/sticky topbar (height: `56px`) housing unit identification, IEEE compliance badge, system status, test timestamp, and global navigation.
- **Workbench Workspace Grid**:
  - Two-column asymmetric command deck on desktop (`minmax(0, 1fr)` plot canvas paired with `380px` telemetry/diagnostic rail).
  - Collapses into a stacked single-column workflow on tablet and mobile viewports (`< 1024px`).
- **Telemetry Metric Matrix**:
  - 4-column compact ribbon (`grid-template-columns: repeat(4, 1fr)`) immediately orienting the engineer to Bandwidth, Correlation, Max Shift, and Overall Status.
- **Bode Plot Viewing Chamber**:
  - Minimum height `460px` with dedicated sub-band boundary dividers (Low: <2kHz, Mid: 2kHz-100kHz, High: >100kHz) and interactive hover telemetry cursor.

---

## Elevation & Depth

- **Zero Drop-Shadows**: Avoid soft, blurry box shadows that give consumer SaaS applications a floating, amorphous look.
- **1px Crisp Borders & Inset Bevels**: Panels are defined by sharp 1px borders (`#1e293b`). Subtle inset highlights (`inset 0 1px 0 rgba(255, 255, 255, 0.05)`) provide tactile physical instrument feel.
- **Z-Index Layering Order**:
  - Canvas Base: `z-0`
  - Panel & Card Bodies: `z-10`
  - Sticky Telemetry Header: `z-30`
  - Interactive Cursors & Tooltips: `z-40`
  - Modals & Diagnostic Overlays: `z-50`

---

## Shapes

- **Corner Radii Discipline**:
  - Precision instruments use milled metal or hardened chassis borders: `0px` to `4px` maximum (`rounded-sm: 2px`, `rounded: 4px`).
  - No pill-shaped oversized cards or bubbly 16px/24px rounded corners.
- **Interactive Badges**:
  - Beveled status tags (`px-2 py-0.5 text-xs font-mono rounded-[2px]`).
- **Input Fields & File Upload Drops**:
  - Crisp 1px dashed borders with cross-hair target accents at corners.

---

## Components

### 1. Telemetry Top Header (`<header class="telemetry-bar">`)
- **Brand & Model**: `FRA-DIAGNOSTICS // V4.1` with active green status beacon (`w-2 h-2 rounded-full bg-emerald-500 animate-pulse`).
- **Unit Identifier Badge**: Monospace readout displaying active transformer serial (e.g., `TX-765KV-MAIN-01`).
- **IEEE Standard Pill**: `IEEE Std C57.149 COMPLIANT` badge in cyan/emerald wireframe.
- **Global Navigation Matrix**: Segmented switches for `[WORKBENCH]`, `[FLEET HISTORY]`, `[STANDARDS KB]`, `[OVERVIEW]`.

### 2. Metric Telemetry Cards
- Compact rectangular modules with uppercase monospace eyebrow, prominent numeric readout, and colored micro-bar indicating tolerance boundary.

### 3. Sub-band Frequency Response Plot Canvas
- Dual-trace logarithmic Bode plot (`Healthy Baseline` in purple/violet dashed trace vs `Test Sweep` in cyan solid trace).
- Semi-transparent colored background zones marking the 3 IEEE sub-bands:
  - Core Zone: `< 2 kHz` (faint amber/violet wash)
  - Winding Zone: `2 kHz – 100 kHz` (faint cyan wash)
  - High/Terminal Zone: `> 100 kHz` (faint blue/slate wash)

### 4. Diagnostic Severity Verdicts
- Three clear operational verdicts:
  - `HEALTHY` (Phosphor Emerald `#10b981` border and accent)
  - `WARNING` (Laboratory Amber `#f59e0b` border and accent)
  - `CRITICAL / DANGER` (Alarm Rose `#f43f5e` border and accent)

---

## Do's and Don'ts

### Do:
- **Do** align all numerical metrics and units with monospace fonts (`JetBrains Mono`).
- **Do** provide exact mathematical values alongside diagnostic qualitative labels.
- **Do** clearly demarcate the three IEEE C57.149 sub-bands on all frequency curves.
- **Do** maintain a dark, low-glare matte appearance suitable for field laptops and control rooms.
- **Do** use subtle 1px border dividers to maintain strict architectural alignment.

### Don't:
- **Don't** use bubbly border radii (`rounded-2xl`, `rounded-3xl`).
- **Don't** add diffuse, colored neon glow drop-shadows under buttons or cards.
- **Don't** hide frequency coordinates or decibel scale values behind ambiguous visual icons.
- **Don't** break backwards compatibility with existing Flask template variables (`transformerId`, `corr`, `shift`, etc.).
- **Don't** introduce npm or JavaScript build dependencies that prevent the Flask app from running directly with `python app/app.py`.
