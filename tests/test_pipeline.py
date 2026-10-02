import pytest
import pandas as pd
from src.pipeline import run_pipeline, PipelineResult

def test_pipeline_single_sweep():
    # Single-sweep file without explicit metadata columns
    results = run_pipeline("data/raw/fra_healthy.csv")
    
    assert "status" in results
    assert "severity" in results
    assert "composite_score" in results
    assert "per_band" in results
    assert 0 <= results["composite_score"] <= 100

def test_pipeline_multi_asset_file():
    # Multi-asset file containing multiple sweeps with metadata
    results = run_pipeline("data/FRA_Mock_Data_Large.csv")
    
    assert isinstance(results, list)
    assert len(results) == 20
    
    for r in results:
        assert isinstance(r, dict)
        assert "status" in r
        assert "severity" in r
        assert "composite_score" in r
        assert "metadata" in r
        assert "Transformer_ID" in r["metadata"]
        assert 0 <= r["composite_score"] <= 100

    # Ensure assets are separated and not blended
    transformer_ids = [r["metadata"]["Transformer_ID"] for r in results]
    assert len(set(transformer_ids)) == 20
    assert "TR001" in transformer_ids
    assert "TR020" in transformer_ids

def test_pipeline_in_memory_multi_asset():
    df = pd.DataFrame({
        "Asset_ID": ["Asset_1"] * 50 + ["Asset_2"] * 50,
        "Frequency_Hz": list(pd.Series(range(20, 1020, 20)).astype(float)) * 2,
        "Magnitude_dB": [-10.0 - (i % 5) for i in range(100)]
    })
    results = run_pipeline(df)
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["metadata"]["Asset_ID"] == "Asset_1"
    assert results[1]["metadata"]["Asset_ID"] == "Asset_2"
