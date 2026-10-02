import numpy as np
import pandas as pd
from src.model import predict_fault

# =========================
# 🔍 Peak & Deviation Detection
# =========================
def calculate_metrics(data1, data2):
    """
    Calculates the statistical difference between the reference and test signals.
    """
    try:
        # Get valid mask where both have data
        valid_mask = data1["Magnitude"].notna() & data2["Magnitude"].notna()
        if valid_mask.sum() == 0:
            return 0, 0.0, 0.0

        m1_sync = data1.loc[valid_mask, "Magnitude"].values
        m2_sync = data2.loc[valid_mask, "Magnitude"].values

        # 1. Peak Shift (Using argmax on the synchronized arrays)
        peak1 = np.argmax(m1_sync)
        peak2 = np.argmax(m2_sync)
        shift = int(abs(peak1 - peak2))

        # 2. Max Deviation (dB difference)
        deviation_array = m1_sync - m2_sync
        max_dev = np.max(np.abs(deviation_array))
        
        # 3. Correlation (Statistical Similarity)
        corr = np.corrcoef(m1_sync, m2_sync)[0, 1]
        
        if np.isnan(corr): corr = 0.0

        return shift, round(float(max_dev), 2), round(float(corr), 4)
    except Exception as e:
        print(f"Metrics Calculation Error: {e}")
        return 0, 0.0, 0.0

# =========================
# 🧠 ADVANCED ANALYSIS
# =========================
def advanced_analysis(healthy_df, uploaded_df):
    """
    Performs AI + Statistical analysis on FRA data.
    """
    # Now that data is preprocessed, both are 500 points on the same grid
    h_df = healthy_df.copy()
    u_df = uploaded_df.copy()

    # 2. Get core statistical metrics using valid intersection
    shift, max_dev, corr = calculate_metrics(h_df, u_df)

    # 3. Get AI Prediction from your ML model
    try:
        # Pass the preprocessed dataframes to the AI model
        ai_fault, ai_confidence, _ = predict_fault(h_df, u_df)
    except Exception as e:
        print(f"AI Prediction failed, falling back to stats: {e}")
        ai_fault, ai_confidence = "Analysis Pending", 0.0

    # 4. 🚨 Unified Logic (AI + Statistics)
    fault_type = ai_fault
    # Use AI confidence if available, otherwise use correlation %
    confidence = ai_confidence if ai_confidence > 0 else (corr * 100)

    if corr > 0.98:
        status = "Healthy"
        severity = "Low"
        recommendation = "Transformer operating within normal parameters. No action required."
    elif corr > 0.90:
        status = "Warning"
        severity = "Medium"
        recommendation = "Minor deviation detected. Schedule a DGA (Dissolved Gas Analysis) to confirm internal state."
    else: 
        status = "Danger"
        severity = "High"
        recommendation = "Significant frequency response shift! Immediate internal inspection of windings recommended."

    # 5. 📊 Data Alignment for Chart.js
    try:
        # Use common grid data for the frontend, replacing NaNs with None for JSON
        freq = u_df["Frequency"].tolist()
        mag_h = h_df["Magnitude"].replace({np.nan: None}).tolist()
        mag_u = u_df["Magnitude"].replace({np.nan: None}).tolist()
    except Exception as e:
        print(f"Chart Alignment Error: {e}")
        freq, mag_h, mag_u = [], [], []

    return {
        "status": status,
        "shift": max_dev,               # Displayed in "Max Deviation"
        "correlation": corr,           # Displayed in "Correlation"
        "severity": severity,
        "fault_type": fault_type,      # Displayed in "AI Fault Classification"
        "confidence": round(confidence, 1),
        "frequencies": freq,
        "magnitude_healthy": mag_h,
        "magnitude_uploaded": mag_u,
        "recommendation": recommendation
    }