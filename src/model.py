import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Define the model path relative to the project root
MODEL_PATH = "models/trained_model.pkl"

def extract_features(data1, data2):
    """
    Interpolates signals to 200 common points and extracts 4 statistical features.
    Includes safety checks for zero-variance and NaN values.
    """
    try:
        f1 = np.array(data1["Frequency"])
        m1 = np.array(data1["Magnitude"])

        f2 = np.array(data2["Frequency"])
        m2 = np.array(data2["Magnitude"])

        # 1. Align the frequency range for comparison
        f_min = max(min(f1), min(f2))
        f_max = min(max(f1), max(f2))
        
        # Intersection check: ensures f_max is actually greater than f_min
        if f_max <= f_min:
            return [0.0, 0.0, 0.0, 0.0]

        common_freq = np.linspace(f_min, f_max, 200)

        # 2. Interpolate magnitudes to the common frequency points
        m1_interp = np.interp(common_freq, f1, m1)
        m2_interp = np.interp(common_freq, f2, m2)

        # 3. Calculate Statistical Features
        diff = np.abs(m1_interp - m2_interp)
        
        # --- SAFE CORRELATION CALCULATION START ---
        # We check if standard deviation is 0 (flat line) to avoid division by zero
        std1 = np.std(m1_interp)
        std2 = np.std(m2_interp)

        if std1 == 0 or std2 == 0:
            correlation = 0.0  # Or 1.0 if both are identical flat lines, but 0.0 is safer for faults
        else:
            corr_matrix = np.corrcoef(m1_interp, m2_interp)
            correlation = corr_matrix[0, 1]
            
            # Final check for NaN values that might sneak through
            if np.isnan(correlation):
                correlation = 0.0
        # --- SAFE CORRELATION CALCULATION END ---

        # Return the 4 features required by the current model version
        return [
            float(np.mean(diff)),      # Average Deviation
            float(np.std(diff)),       # Standard Deviation
            float(np.max(diff)),       # Max Peak Deviation
            float(correlation)         # Statistical Similarity Index
        ]
        
    except Exception as e:
        print(f"❌ Feature Extraction Error: {e}")
        # Return a neutral/safe set of features if extraction fails entirely
        return [10.0, 5.0, 20.0, 0.0] # High diff, zero correlation to indicate an error

def train_model():
    """
    Initializes and trains the Random Forest with the 4-feature signature.
    """
    print("🔄 Training AI Model with 4-feature signature...")
    
    # Feature Set: [Mean Diff, Std Diff, Max Diff, Correlation]
    X = [
        [0.05, 0.02, 0.1, 0.998],  # Healthy
        [0.15, 0.08, 0.3, 0.985],  # Healthy
        [5.2, 3.1, 14.5, 0.65],    # Winding Deformation (High Deviation, Low Corr)
        [4.8, 2.5, 11.0, 0.71],    # Winding Deformation
        [1.8, 1.2, 4.5, 0.88],     # Insulation Degradation (Mid Deviation, Mid Corr)
        [2.1, 1.4, 5.2, 0.85]      # Insulation Degradation
    ]

    # Labels must match the keys in your utils.py
    y = [
        "Healthy", 
        "Healthy", 
        "Winding Deformation", 
        "Winding Deformation", 
        "Insulation Degradation", 
        "Insulation Degradation"
    ]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Ensure the models directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

def load_model():
    """
    Loads the model if it exists, otherwise triggers a fresh training.
    """
    if not os.path.exists(MODEL_PATH):
        train_model()
    
    try:
        model = joblib.load(MODEL_PATH)
        # Final safety check for feature count
        if hasattr(model, 'n_features_in_') and model.n_features_in_ != 4:
            print("⚠️ Model feature mismatch detected. Re-training...")
            train_model()
            model = joblib.load(MODEL_PATH)
        return model
    except:
        train_model()
        return joblib.load(MODEL_PATH)

def predict_fault(data1, data2):
    """
    Primary interface for the App. Returns (Fault Type, Confidence %).
    """
    model = load_model()
    features = extract_features(data1, data2)

    # Reshape features for a single prediction
    features_reshaped = np.array(features).reshape(1, -1)
    
    prediction = model.predict(features_reshaped)[0]
    
    # Calculate probability/confidence score
    probabilities = model.predict_proba(features_reshaped)[0]
    confidence = max(probabilities)

    return prediction, round(float(confidence) * 100, 2)

def load_fra_data(file_path):
    """
    Safely loads FRA data regardless of how many columns are present.
    """
    try:
        # 1. Load the CSV
        df = pd.read_csv(file_path)
        
        # 2. Clean column names (remove spaces/newlines)
        df.columns = [str(col).strip() for col in df.columns]

        # 3. Handle the 'Length Mismatch' by NOT forcing 6 columns.
        # Instead, let's identify the right columns by their names.
        
        # Look for Frequency and Magnitude (case insensitive)
        freq_col = next((c for c in df.columns if 'freq' in c.lower()), None)
        mag_col = next((c for c in df.columns if 'mag' in c.lower() or 'db' in c.lower()), None)

        if freq_col and mag_col:
            # Keep only what we need and rename them
            df = df[[freq_col, mag_col]]
            df.columns = ['Frequency', 'Magnitude']
        else:
            # If we can't find names, assume first two columns are Freq and Mag
            df = df.iloc[:, :2] 
            df.columns = ['Frequency', 'Magnitude']

        return df
    except Exception as e:
        print(f"Detailed Error loading {file_path}: {e}")
        return None