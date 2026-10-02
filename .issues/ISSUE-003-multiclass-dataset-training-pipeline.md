# [ISSUE-003] Multi-Class Feature Extraction and Training Pipeline for Transformer Fault Classifier

- **ID**: ISSUE-003
- **Type**: `wayfinder:task` (AFK)
- **Status**: Closed
- **Assignee**: wayfinder-session
- **Blocked By**: ISSUE-001, ISSUE-002
- **Blocks**: ISSUE-004

---

## Question

How should the synthetic/mock multi-record dataset in `data/raw/FRA_mock_data.csv` (and augmented spectral profiles) be processed into a rich feature matrix—incorporating sub-band correlation coefficients ($CCF_{\text{low}}, CCF_{\text{mid}}, CCF_{\text{high}}$), maximum decibel deviations, and spectral variance—to train, evaluate, and serialize an expanded Random Forest classifier supporting all 4 target classes (*Healthy*, *Winding Deformation*, *Insulation Degradation*, and *Core Displacement*)?

---

## Resolution

### Data Problem Identified

The existing `FRA_mock_data.csv` (100 rows) has **1 row per transformer** (single frequency point each) — unsuitable for spectral sub-band analysis which requires full frequency sweeps. The `FRA_Mock_Data_Large.csv` has full 200-point sweeps but **no fault labels**. Neither dataset provides **paired baseline/test sweeps**, which are essential for computing CCF, ASLE, and MaxDev metrics.

**Decision**: Generate physics-informed synthetic paired sweeps with known fault labels, rather than trying to retrofit the existing flat-record CSV.

### Implementation Assets

- [`src/dataset_generator.py`](file:///C:/repositories/Hackathon/FRA-data-technical/FRA_AI_Data/src/dataset_generator.py) — Synthetic training data generator (400 paired sweeps, 100 per class)
- [`src/model.py`](file:///C:/repositories/Hackathon/FRA-data-technical/FRA_AI_Data/src/model.py) — Expanded model module with 12-feature sub-band extraction
- [`scripts/train_classifier.py`](file:///C:/repositories/Hackathon/FRA-data-technical/FRA_AI_Data/scripts/train_classifier.py) — CLI training entry point
- [`data/processed/training_features.csv`](file:///C:/repositories/Hackathon/FRA-data-technical/FRA_AI_Data/data/processed/training_features.csv) — Extracted feature matrix (400 × 13)
- [`models/trained_model.pkl`](file:///C:/repositories/Hackathon/FRA-data-technical/FRA_AI_Data/models/trained_model.pkl) — Serialized RandomForest + LabelEncoder tuple

### Design Decisions

1. **Synthetic Data Generation**: Each sample is a (baseline, test) sweep pair on the ISSUE-002 common grid (500 log-spaced points, 20 Hz – 1 MHz). Faults are injected as physically-grounded perturbations in the appropriate IEEE sub-band:
   - *Healthy*: Gaussian noise σ=0.2 dB (all bands)
   - *Winding Deformation*: 3–15 dB sinusoidal shift in MF (2 kHz – 100 kHz)
   - *Insulation Degradation*: 1–5 dB capacitive shift in HF (100 kHz – 1 MHz)
   - *Core Displacement*: 5–20 dB inductive shift in LF (20 Hz – 2 kHz)

2. **12-Feature Signature**: Per-band (LF, MF, HF) × 4 metrics:
   - **CCF** — Cross-Correlation Factor (from `compute_subband_metrics`)
   - **ASLE** — Mean Absolute dB Error (from `compute_subband_metrics`)
   - **MaxDev** — Maximum Absolute dB Deviation (from `compute_subband_metrics`)
   - **Variance** — Variance of the dB difference vector per band

3. **Model Architecture**: `RandomForestClassifier(n_estimators=100, random_state=42)`, stratified 80/20 train/test split. Model and `LabelEncoder` serialized together as a tuple in `models/trained_model.pkl`.

4. **API Shape**: `predict_fault(baseline_df, test_df)` returns `(fault_type: str, confidence_pct: float, per_band_metrics: dict)` — backward-compatible position for ISSUE-004's fusion logic.

5. **Preprocessing Reuse**: Imports `preprocess_sweep`, `compute_subband_metrics`, and `slice_subband` directly from `src.preprocessor_prototype` (ISSUE-002 output). No duplication.

### Evaluation Results

```
                        precision    recall  f1-score   support

     Core Displacement       1.00      1.00      1.00        20
               Healthy       1.00      1.00      1.00        20
Insulation Degradation       1.00      1.00      1.00        20
   Winding Deformation       1.00      1.00      1.00        20

              accuracy                           1.00        80
```

**Feature Importances** (all 12 features contributing):

| Feature | Importance |
|---|---|
| LF_ASLE | 11.2% |
| MF_Variance | 10.1% |
| MF_MaxDev | 9.8% |
| HF_CCF | 9.4% |
| LF_CCF | 9.0% |
| MF_CCF | 8.7% |
| HF_ASLE | 8.2% |
| HF_Variance | 7.9% |
| MF_ASLE | 7.7% |
| LF_MaxDev | 7.5% |
| LF_Variance | 5.7% |
| HF_MaxDev | 4.7% |

### Known Limitations

- 100% accuracy is expected on synthetic data with well-separated fault signatures. Real-world performance will depend on replacing/augmenting with actual field measurements.
- The `FRA_mock_data.csv` single-point-per-transformer format remains unused — it cannot support sub-band analysis. The training pipeline operates exclusively on the synthetic paired-sweep data.

