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
        # Convert to numpy arrays for speed and reliability
        m1 = np.array(data1["Magnitude"])
        m2 = np.array(data2["Magnitude"])
        
        # ✅ FIX: Synchronize lengths before any math
        min_len = min(len(m1), len(m2))
        m1_sync = m1[:min_len]
        m2_sync = m2[:min_len]

        # 1. Peak Shift (Using argmax on the synchronized arrays)
        peak1 = np.argmax(m1_sync)
        peak2 = np.argmax(m2~_sync)
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
    # 1. ✅ PRE-SYNC: Ensure both dataframes are the same length globally
    min_len = min(len(healthy_df), len(uploaded_df))
    h_df = healthy_df.iloc[:min_len].copy()
    u_df = uploaded_df.iloc[:min_len].copy()

    # 2. Get core statistical metrics using synchronized data
    shift, max_dev, corr = calculate_metrics(h_df, u_df)

    # 3. Get AI Prediction from your ML model
    try:
        # Pass the synchronized dataframes to the AI model
        ai_fault, ai_confidence = predict_fault(h_df, u_df)
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
        # Use synchronized data for the frontend
        freq = u_df["Frequency"].tolist()
        mag_h = h_df["Magnitude"].tolist()
        mag_u = u_df["Magnitude"].tolist()
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