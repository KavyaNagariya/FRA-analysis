import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from src.preprocessor import preprocess_sweep, compute_subband_metrics, COMMON_GRID, slice_subband

MODEL_PATH = "models/trained_model.pkl"

def extract_subband_features(baseline_df, test_df):
    """
    Extract 12 features: CCF, ASLE, MaxDev, Variance for LF, MF, HF bands.
    baseline_df, test_df must be preprocessed sweeps (i.e. on common grid).
    """
    features = {}
    for band in ['LF', 'MF', 'HF']:
        m = compute_subband_metrics(baseline_df, test_df, band)
        features[f"{band}_CCF"] = m.get('CCF', 1.0)
        features[f"{band}_ASLE"] = m.get('ASLE_dB', 0.0)
        features[f"{band}_MaxDev"] = m.get('MaxDev_dB', 0.0)
        
        if 'Variance' in m:
            features[f"{band}_Variance"] = m['Variance']
        else:
            base_slice, _ = slice_subband(baseline_df, band)
            test_slice, _ = slice_subband(test_df, band)
            if not base_slice.empty and not test_slice.empty:
                diff = test_slice['Magnitude'] - base_slice['Magnitude']
                var_val = diff.var()
                features[f"{band}_Variance"] = var_val if pd.notna(var_val) else 0.0
            else:
                features[f"{band}_Variance"] = 0.0
            
    return features

def train_model():
    df = pd.read_csv("data/processed/training_features.csv")
    X = df.drop(columns=['label'])
    y = df['label']
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
    )
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    
    importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    import os
    os.makedirs("models", exist_ok=True)
    joblib.dump((clf, le), MODEL_PATH)
    
    return report, importances

def load_model():
    clf, le = joblib.load(MODEL_PATH)
    return clf, le

def predict_fault(baseline_df, test_df):
    clf, le = load_model()
    features = extract_subband_features(baseline_df, test_df)
    X = pd.DataFrame([features])
    
    if len(X.columns) != 12:
        raise ValueError(f"Expected 12 features, got {len(X.columns)}")
        
    pred = clf.predict(X)[0]
    probs = clf.predict_proba(X)[0]
    confidence_pct = probs[pred] * 100
    fault_type = le.inverse_transform([pred])[0]
    
    metrics = {band: compute_subband_metrics(baseline_df, test_df, band) for band in ['LF', 'MF', 'HF']}
    return fault_type, confidence_pct, metrics