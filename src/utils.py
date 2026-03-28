def get_recommendation(fault_type):
    """
    Returns a detailed, actionable recommendation based on the detected fault.
    Matches the 'Detected Faults' section of the FRA AI Dashboard.
    """
    recommendations = {
        "Winding Deformation": (
            "Significant deviation detected in mid-frequency range (10kHz–100kHz) "
            "suggesting axial winding displacement. Schedule internal inspection within 30 days. "
            "Reduce loading to 80% capacity until inspection is completed."
        ),
        "Insulation Degradation": (
            "Minor capacitance changes in high-frequency region may indicate early-stage "
            "insulation aging. Perform dissolved gas analysis (DGA) to confirm. "
            "Continue monitoring with quarterly FRA tests."
        ),
        "Core Displacement": (
            "Slight low-frequency deviation within acceptable tolerance. May be due to "
            "measurement noise or minor core settling. No immediate action required. "
            "Include in next scheduled maintenance review."
        ),
        "Healthy": (
            "Signature matches reference baseline within 98% correlation. "
            "No mechanical or electrical anomalies detected. Resume standard annual monitoring."
        )
    }

    # Default to a generic warning if the fault_type is unexpected
    return recommendations.get(
        fault_type, 
        "Anomalous signature detected. Data requires manual review by a senior transformer engineer."
    )

def get_severity_color(severity):
    """
    Helper to return the correct CSS class or Hex color for the UI.
    """
    colors = {
        "High": "#ef4444",    # Danger Red
        "Medium": "#f59e0b",  # Warning Orange
        "Low": "#22c55e"      # Success Green
    }
    return colors.get(severity, "#94a3b8")