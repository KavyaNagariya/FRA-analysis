import pandas as pd
import numpy as np

def is_phase_measurement_column(col_name):
    """
    Distinguishes phase angle measurements (e.g. Phase_deg, Phase (deg), Angle)
    from transformer winding phase metadata (e.g. Phase_ID, Phase_A, Test_Phase).
    """
    col_lower = str(col_name).lower()
    metadata_patterns = ["id", "name", "type", "label", "_a", "_b", "_c", "_u", "_v", "_w", "test", "winding"]
    if any(pat in col_lower for pat in metadata_patterns):
        return False
    
    angle_patterns = ["deg", "degree", "angle", "rad"]
    if any(k in col_lower for k in angle_patterns):
        return True
    
    return col_lower in ["phase", "phase_rad"]

def detect_columns(columns):
    freq_keywords = ["freq", "frequency", "hz"]
    mag_keywords = ["mag", "magnitude", "amplitude", "db"]

    cols_info = {
        "freq": None,
        "mag": None,
        "phase": None,
        "metadata": []
    }

    for col in columns:
        col_lower = str(col).lower()
        if any(k in col_lower for k in freq_keywords) and not cols_info["freq"]:
            cols_info["freq"] = col
        elif any(k in col_lower for k in mag_keywords) and not cols_info["mag"]:
            cols_info["mag"] = col
        elif is_phase_measurement_column(col) and not cols_info["phase"]:
            cols_info["phase"] = col
        else:
            cols_info["metadata"].append(col)

    # Fallback to first available columns if detection fails
    if cols_info["freq"] is None or cols_info["mag"] is None:
        remaining = [c for c in columns if c not in [cols_info["freq"], cols_info["mag"], cols_info["phase"]]]
        if cols_info["freq"] is None and remaining:
            cols_info["freq"] = remaining.pop(0)
        if cols_info["mag"] is None and remaining:
            cols_info["mag"] = remaining.pop(0)
        cols_info["metadata"] = remaining

    return cols_info

class FRADataIngestor:
    def load(self, path_or_df):
        """Load and parse the dataset, detecting single vs multi-test."""
        try:
            if isinstance(path_or_df, pd.DataFrame):
                data = path_or_df.copy()
            elif hasattr(path_or_df, "read"):
                try:
                    data = pd.read_csv(path_or_df)
                except Exception:
                    path_or_df.seek(0)
                    data = pd.read_excel(path_or_df)
            else:
                str_path = str(path_or_df)
                if str_path.endswith(".xlsx"):
                    data = pd.read_excel(path_or_df)
                else:
                    try:
                        data = pd.read_csv(path_or_df, encoding="utf-8", on_bad_lines='skip')
                    except Exception:
                        data = pd.read_csv(path_or_df, encoding="latin1", sep=None, engine='python')

            cols_info = detect_columns(data.columns)

            if not cols_info['freq'] or not cols_info['mag']:
                raise ValueError("Could not detect Frequency and Magnitude columns.")

            # Clean numeric data for measurements
            for col_type in ['freq', 'mag', 'phase']:
                col = cols_info[col_type]
                if col and col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')

            # Drop rows where critical measurements are NaN
            data = data.dropna(subset=[cols_info['freq'], cols_info['mag']]).reset_index(drop=True)

            # Standardize names
            rename_map = {cols_info['freq']: 'Frequency', cols_info['mag']: 'Magnitude'}
            if cols_info['phase']:
                rename_map[cols_info['phase']] = 'Phase'
            data = data.rename(columns=rename_map)

            meas_cols = ['Frequency', 'Magnitude'] + (['Phase'] if cols_info['phase'] else [])
            metadata_cols = cols_info['metadata']

            if not metadata_cols:
                clean_data = data[meas_cols].copy().reset_index(drop=True)
                return {
                    'type': 'single_sweep',
                    'data': clean_data,
                    'sweeps': [{'metadata': {}, 'data': clean_data}]
                }
            else:
                sweeps = []
                grouped = data.groupby(metadata_cols, sort=False, dropna=False)
                for name, group in grouped:
                    if isinstance(name, tuple):
                        meta_dict = dict(zip(metadata_cols, name))
                    else:
                        meta_dict = {metadata_cols[0]: name}

                    sweeps.append({
                        'metadata': meta_dict,
                        'data': group[meas_cols].copy().reset_index(drop=True)
                    })

                return {
                    'type': 'multi_sweep',
                    'metadata_columns': metadata_cols,
                    'sweeps': sweeps
                }

        except Exception as e:
            print(f"Data Loader Error ({path_or_df}): {e}")
            return None

def load_fra_data(path_or_df, return_sweeps=False):
    """
    Loads FRA data from a file path or DataFrame.
    If the data contains metadata columns, returns a list of sweep dictionaries
    with 'metadata' and 'data'.
    If the data is a single sweep without metadata, returns a DataFrame
    (or a list of sweep dicts if return_sweeps=True).
    """
    ingestor = FRADataIngestor()
    result = ingestor.load(path_or_df)
    if result is None:
        return None

    if result['type'] == 'multi_sweep' or return_sweeps:
        return result['sweeps']
    return result['data']

def load_fra_sweeps(path_or_df):
    """Convenience helper to always return a list of sweep dicts."""
    ingestor = FRADataIngestor()
    result = ingestor.load(path_or_df)
    if result is None:
        return []
    return result['sweeps']