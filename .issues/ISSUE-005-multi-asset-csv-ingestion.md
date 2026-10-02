# [ISSUE-005] Design Multi-Asset Ingestion and Parsing Logic

- **ID**: ISSUE-005
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Open
- **Assignee**: Unassigned
- **Blocked By**: None (Frontier)
- **Blocks**: None

---

## Question

How should `src/data_loader.py` inspect incoming CSV/Excel files to detect whether an upload represents a single two-column sweep (`Frequency`, `Magnitude`) or a multi-test dataset (containing metadata columns like `Transformer_ID`, `Winding_Type`, `Phase_Degree`, `Test_Date`), extracting the relevant sweep reliably without crashing or truncating valid measurements?
