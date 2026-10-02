import pandas as pd
import numpy as np
import pytest
from src.analyzer import advanced_analysis

def test_ml_severity_escalation(monkeypatch):
    # Mock compute_subband_metrics to return healthy metrics
    monkeypatch.setattr('src.preprocessor.compute_subband_metrics', lambda *args, **kwargs: {
        "status": "Healthy",
        "CCF": 0.99,
        "MaxDev_dB": 0.1,
    })
    
    # Mock predict_fault to return a fault
    monkeypatch.setattr('src.analyzer.predict_fault', lambda *args, **kwargs: ("Winding Deformation", 95.0, {}))
    
    # Create dummy dataframes
    f = np.linspace(20, 1000000, 500)
    mag = np.zeros(500)
    h_df = pd.DataFrame({'Frequency': f, 'Magnitude': mag})
    u_df = h_df.copy()
    
    result = advanced_analysis(h_df, u_df)
    
    assert result['fault_type'] == "Winding Deformation"
    assert result['status'] == "Danger"
    assert result['severity'] == "High"

def test_health_integrity_score_format(monkeypatch):
    # Mock predict_fault to return healthy
    monkeypatch.setattr('src.analyzer.predict_fault', lambda *args, **kwargs: ("Healthy", 0.0, {}))
    
    f = np.linspace(20, 1000000, 500)
    mag = np.zeros(500)
    h_df = pd.DataFrame({'Frequency': f, 'Magnitude': mag})
    u_df = h_df.copy()
    
    result = advanced_analysis(h_df, u_df)
    
    assert 'composite_score' in result
    assert isinstance(result['composite_score'], (float, int))
    assert 0 <= result['composite_score'] <= 100
