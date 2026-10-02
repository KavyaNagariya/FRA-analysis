import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
FREQ_MIN = 20.0        # Hz — IEEE C57.149 low-band start
FREQ_MAX = 1_000_000.0 # Hz — 1 MHz upper bound
GRID_POINTS = 500      # decade-balanced log grid
MIN_BAND_POINTS = 10   # minimum for a valid sub-band metric

# IEEE sub-band boundaries
SUBBAND_BOUNDARIES = {
    "LF": (20.0, 2_000.0),        # Core
    "MF": (2_000.0, 100_000.0),   # Winding
    "HF": (100_000.0, 1_000_000.0),  # Leads/insulation
}

# ─────────────────────────────────────────────
# Step 0: Common Grid
# ─────────────────────────────────────────────
def make_common_grid():
    """500 log-spaced points from 20 Hz to 1 MHz."""
    return np.logspace(np.log10(FREQ_MIN), np.log10(FREQ_MAX), GRID_POINTS)

COMMON_GRID = make_common_grid()

# ─────────────────────────────────────────────
# Step 1: Clean
# ─────────────────────────────────────────────
def clean_data(df):
    """Removes invalid entries and sorts by frequency."""
    df = df.dropna(subset=["Frequency", "Magnitude"])
    df = df.sort_values(by="Frequency").reset_index(drop=True)
    # Drop duplicates on frequency (keep first)
    df = df.drop_duplicates(subset="Frequency", keep="first").reset_index(drop=True)
    return df

# ─────────────────────────────────────────────
# Step 2: Smooth on native grid
# ─────────────────────────────────────────────
def smooth_signal(df, window=11, polyorder=3):
    """Savitzky-Golay on the native frequency grid. Skipped if too few points."""
    if len(df) > window:
        df = df.copy()
        try:
            df["Magnitude"] = savgol_filter(df["Magnitude"].values, window, polyorder)
        except Exception as e:
            print(f"  Smoothing failed: {e}")
    else:
        print(f"  Signal too short ({len(df)} pts) for window {window}. Skipping smoothing.")
    return df

# ─────────────────────────────────────────────
# Step 3: Interpolate to common grid
# ─────────────────────────────────────────────
def interpolate_to_common_grid(df, grid=None):
    """
    Interpolation in dB-space onto the common log grid.
    Points outside the native sweep range are NaN (no extrapolation).
    Gracefully falls back to linear or empty for sparse arrays.
    """
    if grid is None:
        grid = COMMON_GRID

    native_freq = df["Frequency"].values
    native_mag = df["Magnitude"].values

    if len(native_freq) < 2:
        # Too sparse to interpolate at all
        return pd.DataFrame({"Frequency": grid, "Magnitude": np.nan})
    
    # Fallback to linear if fewer than 4 points
    kind = "cubic" if len(native_freq) >= 4 else "linear"

    interp_fn = interp1d(
        native_freq, native_mag,
        kind=kind,
        bounds_error=False,
        fill_value=np.nan,
    )
    interpolated_mag = interp_fn(grid)

    result = pd.DataFrame({
        "Frequency": grid,
        "Magnitude": interpolated_mag,
    })
    return result

# ─────────────────────────────────────────────
# Step 4: Normalize
# ─────────────────────────────────────────────
def normalize_for_ai(df):
    """Min-Max normalization to [0, 1], NaN-safe."""
    mag = df["Magnitude"]
    mag_min = mag.min()  # np.nanmin via pandas
    mag_max = mag.max()
    denom = mag_max - mag_min
    if denom == 0 or np.isnan(denom):
        df["Magnitude_Scaled"] = 0.0
    else:
        df["Magnitude_Scaled"] = (mag - mag_min) / denom
    return df

# ─────────────────────────────────────────────
# Full Pipeline
# ─────────────────────────────────────────────
def preprocess_sweep(df, source_path=None):
    """
    Full preprocessing pipeline for a single FRA sweep.

    Returns a DataFrame on the common 500-point log grid with columns:
        Frequency, Magnitude, Magnitude_Scaled

    Metadata stored in df.attrs:
        source_file, native_point_count, native_freq_min, native_freq_max
    """
    # --- Clean ---
    cleaned = clean_data(df)
    if cleaned.empty:
        return pd.DataFrame({"Frequency": COMMON_GRID, "Magnitude": np.nan, "Magnitude_Scaled": np.nan})

    # --- Smooth on native grid ---
    smoothed = smooth_signal(cleaned)

    # --- Interpolate to common grid ---
    aligned = interpolate_to_common_grid(smoothed)

    # --- Normalize ---
    result = normalize_for_ai(aligned)

    # --- Attach metadata ---
    result.attrs["source_file"] = str(source_path) if source_path else "unknown"
    result.attrs["native_point_count"] = len(cleaned)
    result.attrs["native_freq_min"] = float(cleaned["Frequency"].min()) if not cleaned.empty else 0.0
    result.attrs["native_freq_max"] = float(cleaned["Frequency"].max()) if not cleaned.empty else 0.0

    return result

# ─────────────────────────────────────────────
# Sub-band Helpers
# ─────────────────────────────────────────────
def slice_subband(df, band_name):
    """Extract rows for a named sub-band. Returns (slice_df, is_valid)."""
    lo, hi = SUBBAND_BOUNDARIES[band_name]
    mask = (df["Frequency"] >= lo) & (df["Frequency"] <= hi) & df["Magnitude"].notna()
    band_df = df.loc[mask]
    is_valid = len(band_df) >= MIN_BAND_POINTS
    return band_df, is_valid

def compute_subband_metrics(baseline_df, test_df, band_name):
    """
    Compute CCF, ASLE, MaxDev on the intersection of valid points in a sub-band.
    Both DataFrames must already be on the common grid.
    Returns dict with metrics or {"status": "Insufficient Data"}.
    """
    b_band, b_valid = slice_subband(baseline_df, band_name)
    t_band, t_valid = slice_subband(test_df, band_name)

    if not (b_valid and t_valid):
        return {"band": band_name, "status": "Insufficient Data"}

    # Intersection: both must be non-NaN at the same grid points
    valid_mask = b_band["Magnitude"].notna() & t_band["Magnitude"].notna()
    b_vals = b_band.loc[valid_mask, "Magnitude"].values
    t_vals = t_band.loc[valid_mask, "Magnitude"].values

    if len(b_vals) < MIN_BAND_POINTS:
        return {"band": band_name, "status": "Insufficient Data"}

    # CCF (cross-correlation factor)
    ccf = np.corrcoef(b_vals, t_vals)[0, 1]
    if np.isnan(ccf):
        ccf = 0.0

    # ASLE (mean absolute dB error)
    asle = np.mean(np.abs(t_vals - b_vals))

    # MaxDev
    max_dev = np.max(np.abs(t_vals - b_vals))

    return {
        "band": band_name,
        "status": "OK",
        "n_points": int(len(b_vals)),
        "CCF": round(float(ccf), 4),
        "ASLE_dB": round(float(asle), 2),
        "MaxDev_dB": round(float(max_dev), 2),
    }

# Keeping this for backwards compatibility if anyone calls it
def preprocess_all(data):
    return preprocess_sweep(data)