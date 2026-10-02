---
target: SFRA Diagnostic Workbench
total_score: 21
max_score: 40
na_heuristics: 
p0_count: 2
p1_count: 2
timestamp: 2026-10-02T18-51-31Z
slug: app-templates-index-html
---
# Critique: SFRA Diagnostic Workbench (app/templates/index.html)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | Silent POST; no baseline identity; cards flash `—` before JS fills |
| 2 | Match System / Real World | 3 | Domain-native; but RE-SCAN / INITIATE SCAN imply driving hardware |
| 3 | User Control and Freedom | 2 | Presets + toggles good; no pan, undo, baseline-swap, or cancel |
| 4 | Consistency and Standards | 3 | Token-faithful; sub-band naming triples; native tooltip disabled |
| 5 | Error Prevention | 1 | `required`-only inputs; zero pre-flight on high-stakes diagnosis |
| 6 | Recognition Rather Than Recall | 2 | Thresholds (0.95/0.85/3/6 dB) invisible; must be recalled |
| 7 | Flexibility and Efficiency | 2 | No keyboard cursor, shortcuts, deep links, or recent files |
| 8 | Aesthetic and Minimalist Design | 3 | Faithful density; DIAGNOSIS ×4 while Δf appears 0× |
| 9 | Error Recovery | 1 | No error branch in template; malformed CSV = silent reload or 500 |
| 10 | Help and Documentation | 2 | KB linked; ML card has no "why", no sample file |
| **Total** | | **21/40** | **Acceptable** |

## Design Specificity Verdict

**LLM assessment: grounded where it matters, generic where trust is formed.** The results deck is unmistakably this product — log Bode canvas with violet-baseline/cyan-test traces, IEEE sub-band washes and 2kHz/100kHz dividers, cursor HUD naming physics (`MID FREQ: WINDING RESONANCE`), domain-native metric language (R², ΔdB, HII, remediation). The standby/upload state is interchangeable: centered dropzone card with no baseline picker, vendor hint, sample file, or pass/fail preview. The instrument soul appears only after upload.

**Deterministic scan: 47 findings, 0 errors.** 2 warnings (both `overused-font` Inter in base.html — false positives, pinned by DESIGN.md's dual-typeface mandate) and 45 advisories (9/10/11px telemetry type — false positives, intentional density per the metric-label/eyebrow spec). The detector corroborates the foundation and caught nothing the review missed; every interactional issue below is invisible to it. Browser visualization skipped: no browser automation in this environment.

## Overall Impression

Strongest instrument canvas in the suite with a lab-grade plot loop, let down by ingest trust and explainability. Single biggest opportunity: an on-screen evidence chain under the verdict — de-tanking decisions cannot rest on `confidence%` twice with no cited band, threshold, Δf, or baseline date.

## What's Working

1. **HUD + crosshair + physics naming.** Hover translates, not just numbers: sub-band classification, base/test/ΔdB with color-graded deviation. Instrument thinking, not dashboard thinking.
2. **Sub-bands as interaction, not decoration.** Same 2kHz/100kHz boundaries drive canvas washes, zoom presets, and computed cards — zooming to WINDING and seeing MID R²/ΔdB update is the product's smartest loop.
3. **Gauge restraint + control-room care.** Half-doughnut avoids SaaS-dial cliché; dual-encoded verdict survives glare; skip-link, focus ring, and reduced-motion show field-laptop awareness.

## Priority Issues

**[P0] Silent ingest: no validation, no progress, no error state**
- **What**: Both upload forms POST with only `required`. No parse preview, no busy state, no `{% if error %}` branch.
- **Why it matters**: A Doble semicolon-delimited export fails after a long upload; trust collapses before diagnosis begins.
- **Fix**: Client-side pre-flight (first 5 rows: numeric FREQ/MAG + range check → `✓ 1240 pts · 19.8Hz–2.01MHz → READY` or blocking message); busy state on submit; Jinja error panel preserving filename + sample-file link.
- **Suggested command**: `/impeccable harden`

**[P0] Verdict without evidence chain**
- **What**: Rail shows `fault_type + confidence%` + one recommendation sentence, never stating which band drove it, thresholds, Δf, or baseline ID/date. `confidence%` duplicated in gauge reads as R² = ML confidence.
- **Why it matters**: Violates Physics-First-AI-Second; a rose CRITICAL with no cited band invites unwarranted mobilization or dismissal as AI guess.
- **Fix**: 2-line provenance under ML CLASSIFICATION (`DRIVER: MID R² 0.71 (<0.85) · MAX Δ 6.2dB @ 38kHz · BASELINE …`), threshold legend, ML-vs-physics disagree flag; split MODEL CONFIDENCE vs BAND CORRELATION labels.
- **Suggested command**: `/impeccable clarify`

**[P1] Bode inspection is mouse-only**
- **What**: All precision readout needs `mousemove`; no focusable cursor, arrow-key stepping, or touch equivalent. Toggles lack `aria-pressed`; HUD has no live region; canvas `role="img"` misleads SR into thinking it is static.
- **Why it matters**: Keyboard and touch users cannot perform the core job: read dB at frequency.
- **Fix**: Focusable canvas wrapper, Left/Right stepping with `aria-live` HUD, `aria-pressed` on toggles, grouped zoom presets. Preserve hover path.
- **Suggested command**: `/impeccable audit`

**[P1] Baseline provenance vanishes after analysis**
- **What**: Results show UNIT + timestamp in 10px muted text; analyzed filename, row count, baseline file/date, and instrument are nowhere. BANDWIDTH is hardcoded, not measured.
- **Why it matters**: Breaks auditability (product principle #3): "which baseline did we compare against?" is unanswerable on screen.
- **Fix**: Measured `minFreq–maxFreq + N pts` from `freqData`; provenance line (file, pts, base file, standard); persist filename into re-upload label.
- **Suggested command**: `/impeccable document`

**[P2] Status quadruplication dilutes urgency**
- **What**: Same verdict in header STATE, ribbon DIAGNOSIS, gauge badge, ML color; REMEDIATION paragraph demoted below four echoes.
- **Why it matters**: Density becomes noise; the eye scans colors, not actions, at the highest-stakes moment.
- **Fix**: Single verdict in ribbon; demote header to R² and gauge to number; promote REMEDIATION to numbered 1-2-3 actions with band links.
- **Suggested command**: `/impeccable distill`

## Persona Red Flags

**Alex (power user)**: No drop on results strip, no recents, no `1/2/3` zoom keys or cursor stepping, HUD text not copyable, no `?band=mid` deep link to share. Fails on efficiency.
**Sam (keyboard/SR)**: `mousemove`-only HUD never fires; canvas `role="img"` announces a static picture; toggles have no pressed state; status dots are color-only; 10px `#64748b` footer near-failing. Fails on access to evidence.
**Priya (FAT commissioning engineer, from PRODUCT.md)**: No vendor column-alias map or kHz auto-detect; no tap-position/baseline-ID picker; Δf never computed though CONTEXT promises it; cutoffs undocumented on screen; single-sentence recommendation cannot hold a shipment sign-off. Fails on traceability.

## Minor Observations

- `FRA-INSTRUMENT` typo (verified: base.html:179, prototype_layout.html:257) — undermines the precision voice; fix immediately.
- `RE-SCAN` misnomer (uploads, doesn't scan); BANDWIDTH hardcoded; cards flicker `—` before JS; re-upload truncates long filenames with no title tooltip; Chart.js tooltip disabled removes the touch fallback; zoom-button active state causes 1px layout shift; `TEST: date_now` needs FAT-grade timestamp + operator.
- IEEE pill hidden on smallest viewports (`hidden sm:inline`) — exactly the field laptops that need it.

## Questions to Consider

1. If this verdict triggers a $250k de-tanking, would you sign under a screen showing `confidence%` twice but citing no baseline date, no Δf, and no threshold?
2. Why does the instrument demand a mouse to read a measurement — what would a keyboard-first cursor do to power-user throughput?
3. Is standby earning trust or spending it — would a sample file + expected-header preview have the FAT engineer believing the verdict before results?
