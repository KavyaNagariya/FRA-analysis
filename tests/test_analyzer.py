import pandas as pd
import numpy as np
import pytest
from src.preprocessor import preprocess_sweep
from src.analyzer import advanced_analysis

def generate_dummy_sweep(seed=42):
    rng = np.random.RandomState(seed)
    f = np.logspace(np.log10(20), np.log10(1000000), 100)
    mag = -20 - 10 * np.log10(f/20 + 1)
    return pd.DataFrame({'Frequency': f, 'Magnitude': mag})

def test_pipeline_integration_healthy():
    h_df = generate_dummy_sweep(seed=1)
    u_df = generate_dummy_sweep(seed=2)
    
    # Preprocess
    h_prep = preprocess_sweep(h_df)
    u_prep = preprocess_sweep(u_df)
    
    # Analyze
    result = advanced_analysis(h_prep, u_prep)
    
    assert "status" in result
    assert "severity" in result
    assert "composite_score" in result
    assert 0 <= result['composite_score'] <= 100

def test_pipeline_integration_fault():
    h_df = generate_dummy_sweep(seed=1)
    u_df = generate_dummy_sweep(seed=2)
    
    # Inject a fault logic manually so model flags it
    mask = (u_df['Frequency'] >= 2000) & (u_df['Frequency'] <= 100000)
    u_df.loc[mask, 'Magnitude'] += 10.0 # Winding Deformation signature
    
    h_prep = preprocess_sweep(h_df)
    u_prep = preprocess_sweep(u_df)
    
    result = advanced_analysis(h_prep, u_prep)
    
    assert "status" in result
    assert "severity" in result
    assert result['status'] in ["Danger", "Critical"] # because of huge shift
    assert 0 <= result['composite_score'] <= 100
