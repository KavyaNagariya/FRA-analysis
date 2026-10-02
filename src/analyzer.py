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

    # 4. 🚨 Unified Logic (AI + Statistics with IEEE Sub-Bands)
    from src.preprocessor import compute_subband_metrics
    
    bands = [
        ("LF", "Low (Core)", "< 2 kHz"),
        ("MF", "Mid (Winding)", "2 - 100 kHz"),
        ("HF", "High (Insulation)", "> 100 kHz")
    ]
    
    per_band = {}
    band_ccfs = []
    
    def evaluate_band(ccf):
        if ccf >= 0.98: return "Healthy", 0, "Low"
        if ccf >= 0.90: return "Warning", 1, "Medium"
        if ccf >= 0.80: return "Danger", 2, "High"
        return "Critical", 3, "High"

    worst_sev_level = -1
    overall_status = "Healthy"
    overall_severity = "Low"
    
    for band_code, band_name, band_range in bands:
        band_metrics = compute_subband_metrics(h_df, u_df, band_code)
        if band_metrics.get("status") == "Insufficient Data":
            per_band[band_name] = {
                "range": band_range,
                "ccf": None,
                "max_dev": None,
                "status": "Insufficient Data"
            }
        else:
            band_ccf = band_metrics.get("CCF", 0.0)
            band_max_dev = band_metrics.get("MaxDev_dB", 0.0)
            band_status, band_level, band_severity = evaluate_band(band_ccf)
            
            per_band[band_name] = {
                "range": band_range,
                "ccf": band_ccf,
                "max_dev": band_max_dev,
                "status": band_status
            }
            band_ccfs.append(band_ccf)
            
            if band_level > worst_sev_level:
                worst_sev_level = band_level
                overall_status = band_status
                overall_severity = band_severity

    min_band_ccf = min(band_ccfs) if band_ccfs else corr
    
    if not band_ccfs:
        overall_status = "Insufficient Data"
        overall_severity = "Unknown"
    
    # Composite Score formula from SPEC-001
    ml_conf = ai_confidence if ai_confidence > 0 else (corr * 100)
    composite_score = (0.6 * min_band_ccf * 100) + (0.4 * ml_conf)
    
    # Recommendation logic (keep original simple logic based on worst status)
    if overall_status == "Healthy":
        recommendation = "Transformer operating within normal parameters. No action required."
    elif overall_status == "Warning":
        recommendation = "Minor deviation detected. Schedule a DGA (Dissolved Gas Analysis) to confirm internal state."
    elif overall_status == "Insufficient Data":
        recommendation = "Insufficient data points across all bands. Please perform a higher-resolution sweep."
    else: 
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
        "status": overall_status,
        "shift": max_dev,               # Displayed in "Max Deviation"
        "correlation": corr,           # Displayed in "Correlation"
        "severity": overall_severity,
        "fault_type": ai_fault,      # Displayed in "AI Fault Classification"
        "confidence": round(ml_conf, 1),
        "composite_score": round(composite_score / 100, 2), # Typically output as 0-1 for PDF
        "per_band": per_band,
        "frequencies": freq,
        "magnitude_healthy": mag_h,
        "magnitude_uploaded": mag_u,
        "recommendation": recommendation
    }