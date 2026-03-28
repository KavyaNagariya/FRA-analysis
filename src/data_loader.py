import pandas as pd
import numpy as np

def detect_columns(columns):
    freq_keywords = ["freq", "frequency", "hz"]
    mag_keywords = ["mag", "magnitude", "amplitude", "db"]

    freq_col = None
    mag_col = None

    for col in columns:
        col_lower = str(col).lower()
        if any(k in col_lower for k in freq_keywords):
            freq_col = col
        if any(k in col_lower for k in mag_keywords):
            mag_col = col

    # Fallback to first two columns if detection fails
    if freq_col is None or mag_col is None:
        freq_col = columns[0]
        mag_col = columns[1]

    return freq_col, mag_col

def load_fra_data(path):
    try:
        # 1. Load the file
        if path.endswith(".xlsx"):
            data = pd.read_excel(path)
        else:
            # Added engine='python' to handle complex separators automatically
            try:
                data = pd.read_csv(path, encoding="utf-8", on_bad_lines='skip')
            except:
                data = pd.read_csv(path, encoding="latin1", sep=None, engine='python')

        # 2. Detect and Rename
        freq_col, mag_col = detect_columns(data.columns)
        data = data[[freq_col, mag_col]].copy() # Keep only what we need
        data = data.rename(columns={freq_col: "Frequency", mag_col: "Magnitude"})

        # 3. 🛡️ CLEANING: Convert to Numeric
        # This is the most important step for industrial CSVs
        for col in ["Frequency", "Magnitude"]:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Drop any rows that became NaN (like text headers inside the CSV)
        data = data.dropna().reset_index(drop=True)

        if data.empty:
            print(f"❌ Error: {path} contains no valid numeric data.")
            return None

        print(f"✅ Data loaded successfully: {len(data)} points.")
        return data

    except Exception as e:
        print(f"❌ Data Loader Error ({path}): {e}")
        return None