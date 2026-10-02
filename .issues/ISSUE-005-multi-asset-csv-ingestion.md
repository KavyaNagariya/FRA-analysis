# [ISSUE-005] Design Multi-Asset Ingestion and Parsing Logic

- **ID**: ISSUE-005
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: wayfinder-session
- **Blocked By**: None (Frontier)
- **Blocks**: None

---

## Question

How should `src/data_loader.py` inspect incoming CSV/Excel files to detect whether an upload represents a single two-column sweep (`Frequency`, `Magnitude`) or a multi-test dataset (containing metadata columns like `Transformer_ID`, `Winding_Type`, `Phase_Degree`, `Test_Date`), extracting the relevant sweep reliably without crashing or truncating valid measurements?

## Resolution

Prototype demonstrated separating columns by known keywords versus unknown (metadata) columns. If metadata columns exist, pandas \groupby\ is used to slice the dataset into multiple sweeps, returned as a list of dictionaries with \metadata\ and \data\. If no metadata columns exist, a single sweep is returned.
Prototype implementation: [multi_asset_ingestion_prototype.py](../scratch/multi_asset_ingestion_prototype.py)
