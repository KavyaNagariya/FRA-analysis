# [ISSUE-002] Design Logarithmic Frequency Interpolation & Preprocessing Pipeline

- **ID**: ISSUE-002
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: wayfinder-session
- **Blocked By**: None (Unblocked by ISSUE-001) (Frontier)
- **Blocks**: ISSUE-003, ISSUE-004

---

## Question

How should test sweeps and baseline sweeps with disparate frequency sampling points or non-uniform frequency intervals be aligned onto a common logarithmic frequency grid (e.g. 500 decade-balanced points), and how should Savitzky-Golay filtering and NaN/noise cleaning from `src/preprocessor.py` be unified into the ingestion workflow so both the analytics engine and visualizer receive clean, aligned data?

---

## Resolution

Six design decisions were grilled and confirmed, then validated via a runnable prototype.

### Prototype Asset

- [`src/preprocessor_prototype.py`](file:///C:/repositories/Hackathon/FRA-data-technical/FRA_AI_Data/src/preprocessor_prototype.py) — throwaway prototype demonstrating the full pipeline against 3 data scenarios (9-point hand-picked, 50-point log-spaced, and cross-format alignment).

### Decisions

1. **Common grid (Q1)**: `np.logspace(log10(20), log10(1e6), 500)` — 500 log-spaced points from 20 Hz to 1 MHz (~106 points/decade). Covers all three IEEE sub-bands (LF, MF, HF).

2. **Interpolation method (Q2)**: `scipy.interpolate.interp1d(freq, mag_db, kind='cubic', bounds_error=False, fill_value=np.nan)` — cubic interpolation in dB-space. No extrapolation; points outside the native sweep range are NaN.

3. **Pipeline ordering (Q3)**: `load → clean → smooth(native grid) → interpolate(common grid) → normalize`. Smoothing operates on the original instrument sampling; interpolation comes after, producing synthetic points from already-denoised data.

4. **NaN handling policy (Q4)**: NaN values are carried through the entire pipeline. Sub-band metrics (CCF, ASLE, MaxDev) are computed on the **intersection of valid points** per band. Any sub-band with fewer than 10 valid aligned points reports `"Insufficient Data"` instead of a noisy metric.

5. **Savitzky-Golay parameters (Q5)**: `window=11, polyorder=3` unchanged from the original. The existing length guard skips smoothing for sweeps shorter than the window. At ~106 pts/decade, 11 points span ~1/10 decade — physically appropriate for FRA dB curves.

6. **API shape (Q6)**: `preprocess_sweep()` returns a `pd.DataFrame` with columns `["Frequency", "Magnitude", "Magnitude_Scaled"]` on the common grid. Source metadata (file path, native point count, native frequency range) is stored in `DataFrame.attrs`.

### Validated Behaviors (from prototype run)

| Scenario | Native Points | Valid on Grid | LF CCF | MF CCF | HF |
|---|---|---|---|---|---|
| 9-pt healthy vs 9-pt faulty | 9 each | 287 / 500 | 0.9943 | 0.7512 | Insufficient Data |
| 50-pt TR001 vs 50-pt TR002 | 50 each | 393 / 500 | -0.0539 | -0.2218 | Insufficient Data |
| Cross-format (9-pt vs 50-pt) | 9 vs 50 | 287 vs 393 | -0.0776 | -0.5893 | Insufficient Data |

- HF correctly reports "Insufficient Data" because neither dataset extends above 100 kHz.
- The 9-point sweeps are correctly handled: smoothing is skipped (too few points), cubic interpolation fills 287 of 500 grid points within the native 20 Hz–10 kHz range, and the remaining 213 are NaN.
- Cross-format comparison works: two sweeps with completely different sampling (hand-picked decades vs. log-spaced) land on the same grid and produce meaningful per-band metrics.

