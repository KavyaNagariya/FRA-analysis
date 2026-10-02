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
    Cubic interpolation in dB-space onto the common log grid.
    Points outside the native sweep range are NaN (no extrapolation).
    """
    if grid is None:
        grid = COMMON_GRID

    native_freq = df["Frequency"].values
    native_mag = df["Magnitude"].values

    interp_fn = interp1d(
        native_freq, native_mag,
        kind="cubic",
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
    result.attrs["native_freq_min"] = float(cleaned["Frequency"].min())
    result.attrs["native_freq_max"] = float(cleaned["Frequency"].max())

    return result

# Keeping this for backwards compatibility if anyone calls it
def preprocess_all(data):
    return preprocess_sweep(data)