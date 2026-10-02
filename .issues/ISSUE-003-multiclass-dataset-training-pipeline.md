# [ISSUE-003] Multi-Class Feature Extraction and Training Pipeline for Transformer Fault Classifier

- **ID**: ISSUE-003
- **Type**: `wayfinder:task` (AFK)
- **Status**: Open
- **Assignee**: Unassigned
- **Blocked By**: ISSUE-001, ISSUE-002
- **Blocks**: ISSUE-004

---

## Question

How should the synthetic/mock multi-record dataset in `data/raw/FRA_mock_data.csv` (and augmented spectral profiles) be processed into a rich feature matrix—incorporating sub-band correlation coefficients ($CCF_{\text{low}}, CCF_{\text{mid}}, CCF_{\text{high}}$), maximum decibel deviations, and spectral variance—to train, evaluate, and serialize an expanded Random Forest classifier supporting all 4 target classes (*Healthy*, *Winding Deformation*, *Insulation Degradation*, and *Core Displacement*)?
