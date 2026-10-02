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


def _unwrap_data(loaded):
    """Unwraps DataFrame from loader output (list of sweeps or raw DataFrame)."""
    if isinstance(loaded, list) and len(loaded) > 0:
        return loaded[0].get("data", loaded[0]) if isinstance(loaded[0], dict) else loaded[0]
    if isinstance(loaded, pd.DataFrame):
        return loaded
    return None


def _resolve_baseline_df(baseline_source, fallback_sweep):
    """Loads and unwraps raw baseline sweep data."""
    if baseline_source is not None:
        if isinstance(baseline_source, pd.DataFrame):
            return baseline_source
        unwrapped = _unwrap_data(load_fra_data(baseline_source))
        if unwrapped is not None:
            return unwrapped

    default_path = os.path.join("data", "raw", "fra_healthy.csv")
    if os.path.exists(default_path):
        unwrapped = _unwrap_data(load_fra_data(default_path))
        if unwrapped is not None:
            return unwrapped

    return fallback_sweep["data"]


def run_pipeline(uploaded_data, baseline_data=None, generate_pdf=False, pdf_output_path=None):
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
    baseline_raw = _resolve_baseline_df(baseline_data, sweeps[0])
    source_info = str(baseline_data) if baseline_data is not None else "baseline"
    baseline_prep = preprocess_sweep(baseline_raw, source_path=source_info)

    known_keys = {
        "transformer_id": ["transformer_id", "transformerid", "asset_id", "assetid"],
        "winding_type": ["winding_type", "winding"],
        "test_date": ["test_date", "date"]
    }

    results = []
    for sweep in sweeps:
        sweep_data = sweep["data"]
        metadata = sweep.get("metadata", {})
        sweep_prep = preprocess_sweep(sweep_data)
        
        analysis = advanced_analysis(baseline_prep, sweep_prep)
        
        # Attach metadata to result dictionary
        result_dict = dict(analysis)
        result_dict["metadata"] = metadata

        for target_key, candidate_names in known_keys.items():
            for meta_k, meta_v in metadata.items():
                if str(meta_k).lower() in candidate_names:
                    result_dict[target_key] = meta_v
                    break

        # Generate Bode comparison plot
        try:
            from src.plotter import generate_comparison_plot
            result_dict["bode_plot"] = generate_comparison_plot(baseline_prep, sweep_prep)
        except Exception as e:
            print(f"Warning generating Bode plot: {e}")

        # Optional PDF report generation
        if generate_pdf:
            try:
                from src.report import generate_report
                pdf_path = generate_report(
                    result_dict,
                    bode_plot=result_dict.get("bode_plot"),
                    output_path=pdf_output_path
                )
                result_dict["pdf_path"] = pdf_path
            except Exception as e:
                print(f"Warning generating PDF report: {e}")

        results.append(result_dict)

    if is_multi:
        return results
    else:
        return PipelineResult(results)
