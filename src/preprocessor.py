import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

def clean_data(data):
    """
    Removes invalid entries and ensures the data is sorted by frequency.
    """
    # Remove any non-numeric noise
    data = data.dropna()
    # FRA must be analyzed in increasing frequency order
    data = data.sort_values(by="Frequency").reset_index(drop=True)
    return data

def smooth_signal(data, window=11, polyorder=3):
    try:
        # Check if we have enough points to smooth
        if len(data) > window:
            data["Magnitude"] = savgol_filter(data["Magnitude"], window, polyorder)
        else:
            print(f"⚠️ Signal too short ({len(data)} pts) for window {window}. Skipping smoothing.")
    except Exception as e:
        print(f"Smoothing skipped: {e}")
    return data

def normalize_for_ai(data):
    """
    Min-Max Normalization: Scales magnitude to [0, 1].
    Useful for the Random Forest model to prevent large dB values 
    from skewing the gradients.
    """
    mag = data["Magnitude"]
    data["Magnitude_Scaled"] = (mag - mag.min()) / (mag.max() - mag.min())
    return data

def preprocess_all(data):
    """
    The main pipeline to be called in app.py before analysis.
    """
    data = clean_data(data)
    data = smooth_signal(data)
    # We keep the original Magnitude for the Dashboard display
    # but create a scaled version for the AI model features
    data = normalize_for_ai(data)
    return data