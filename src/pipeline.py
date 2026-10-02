import os
import pandas as pd
from src.data_loader import FRADataIngestor, load_fra_data
from src.preprocessor import preprocess_sweep
from src.analyzer import advanced_analysis

class PipelineResult(list):
    """
    List of diagnostic result dictionaries.
    For single-sweep results, also supports direct dictionary-style indexing/get/contains
    for seamless compatibility.
    """
    def __getitem__(self, item):
        if isinstance(item, str) and len(self) > 0:
            return self[0][item]
        return super().__getitem__(item)

    def get(self, key, default=None):
        if len(self) > 0 and isinstance(self[0], dict):
            return self[0].get(key, default)
        return default

    def __contains__(self, key):
        if isinstance(key, str) and len(self) > 0 and isinstance(self[0], dict):
            return key in self[0]
        return super().__contains__(key)


def run_pipeline(uploaded_data, baseline_data=None):
    """
    Executes the full diagnostic pipeline on uploaded data (file path or DataFrame).
    
    If the uploaded file/DataFrame contains metadata columns, the ingestion module
    segments the data via groupby into discrete sweeps and processes each sweep,
    returning a list of result dictionaries.
    
    If the uploaded file/DataFrame is a single sweep without metadata columns,
    it processes the sweep and returns a PipelineResult (a list of 1 result dict
    that also allows dict-like access).
    """
    ingestor = FRADataIngestor()
    ingest_result = ingestor.load(uploaded_data)
    if ingest_result is None or not ingest_result.get("sweeps"):
        raise ValueError(f"Failed to load FRA data from: {uploaded_data}")

    sweeps = ingest_result["sweeps"]
    is_multi = (ingest_result["type"] == "multi_sweep")

    # Resolve baseline
    if baseline_data is not None:
        if isinstance(baseline_data, pd.DataFrame):
            baseline_raw = baseline_data
        else:
            baseline_raw = load_fra_data(baseline_data)
            if isinstance(baseline_raw, list) and len(baseline_raw) > 0:
                baseline_raw = baseline_raw[0]["data"]
    else:
        # Default baseline if exists
        default_baseline_path = os.path.join("data", "raw", "fra_healthy.csv")
        if os.path.exists(default_baseline_path):
            baseline_raw = load_fra_data(default_baseline_path)
            if isinstance(baseline_raw, list) and len(baseline_raw) > 0:
                baseline_raw = baseline_raw[0]["data"]
        else:
            # Fallback to the first sweep of uploaded data
            baseline_raw = sweeps[0]["data"]

    # Preprocess baseline
    source_info = str(baseline_data) if baseline_data is not None else "baseline"
    baseline_prep = preprocess_sweep(baseline_raw, source_path=source_info)

    results = []
    for sweep in sweeps:
        sweep_data = sweep["data"]
        metadata = sweep.get("metadata", {})
        sweep_prep = preprocess_sweep(sweep_data)
        
        analysis = advanced_analysis(baseline_prep, sweep_prep)
        
        # Attach metadata to result dictionary
        result_dict = dict(analysis)
        result_dict["metadata"] = metadata
        for meta_k, meta_v in metadata.items():
            k_lower = str(meta_k).lower()
            if k_lower in ["transformer_id", "transformerid", "asset_id", "assetid"]:
                result_dict["transformer_id"] = meta_v
            if k_lower in ["winding_type", "winding"]:
                result_dict["winding_type"] = meta_v
            if k_lower in ["test_date", "date"]:
                result_dict["test_date"] = meta_v

        results.append(result_dict)

    if is_multi:
        return results
    else:
        return PipelineResult(results)
