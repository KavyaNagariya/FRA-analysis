import pytest
import pandas as pd
from src.data_loader import detect_columns

def test_detect_columns_distinguishes_measurements_and_metadata():
    columns = [
        "Transformer_ID",
        "Winding_Type",
        "Test_Date",
        "Frequency_Hz",
        "Magnitude_dB",
        "Phase_deg"
    ]
    cols_info = detect_columns(columns)
    
    assert cols_info["freq"] == "Frequency_Hz"
    assert cols_info["mag"] == "Magnitude_dB"
    assert cols_info["phase"] == "Phase_deg"
    assert cols_info["metadata"] == ["Transformer_ID", "Winding_Type", "Test_Date"]

def test_detect_columns_no_metadata():
    columns = ["Frequency", "Magnitude"]
    cols_info = detect_columns(columns)
    
    assert cols_info["freq"] == "Frequency"
    assert cols_info["mag"] == "Magnitude"
    assert cols_info["phase"] is None
    assert cols_info["metadata"] == []

def test_load_fra_data_multi_asset_file():
    from src.data_loader import load_fra_data
    sweeps = load_fra_data("data/FRA_Mock_Data_Large.csv")
    
    assert isinstance(sweeps, list)
    assert len(sweeps) == 20
    
    first_sweep = sweeps[0]
    assert "metadata" in first_sweep
    assert "data" in first_sweep
    assert first_sweep["metadata"]["Transformer_ID"] == "TR001"
    assert first_sweep["metadata"]["Winding_Type"] == "LV"
    assert len(first_sweep["data"]) == 200
    assert "Frequency" in first_sweep["data"].columns
    assert "Magnitude" in first_sweep["data"].columns
    assert "Phase" in first_sweep["data"].columns

def test_load_fra_data_in_memory_multi_asset():
    from src.data_loader import load_fra_data
    df = pd.DataFrame({
        "Asset_ID": ["A", "A", "B", "B"],
        "Frequency_Hz": [20.0, 50.0, 20.0, 50.0],
        "Magnitude_dB": [-10.0, -12.0, -15.0, -18.0]
    })
    sweeps = load_fra_data(df)
    assert isinstance(sweeps, list)
    assert len(sweeps) == 2
    assert sweeps[0]["metadata"] == {"Asset_ID": "A"}
    assert sweeps[1]["metadata"] == {"Asset_ID": "B"}
    assert len(sweeps[0]["data"]) == 2
    assert list(sweeps[0]["data"]["Frequency"]) == [20.0, 50.0]

def test_detect_columns_winding_phase_is_metadata():
    # Transformer winding phase like "Phase_A" or "Phase_ID" must be metadata, not phase angle
    columns = ["Frequency", "Magnitude", "Phase_ID", "Transformer_ID"]
    cols_info = detect_columns(columns)
    assert cols_info["freq"] == "Frequency"
    assert cols_info["mag"] == "Magnitude"
    assert cols_info["phase"] is None
    assert "Phase_ID" in cols_info["metadata"]

def test_load_fra_data_nan_metadata_preserved():
    from src.data_loader import load_fra_data
    df = pd.DataFrame({
        "Asset_ID": ["A", "A", None, None],
        "Frequency_Hz": [20.0, 50.0, 20.0, 50.0],
        "Magnitude_dB": [-10.0, -12.0, -15.0, -18.0]
    })
    sweeps = load_fra_data(df)
    assert isinstance(sweeps, list)
    assert len(sweeps) == 2
    # Second group with NaN Asset_ID should not be dropped
    assert len(sweeps[0]["data"]) == 2
    assert len(sweeps[1]["data"]) == 2



