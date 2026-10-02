# 04 — Multi-Asset CSV Grouping in Data Ingestion

**What to build:** The data ingestion layer automatically detects metadata columns in incoming multi-asset CSV files and uses a `groupby` operation to segment the data into discrete sweeps. The system processes these multiple sweeps and returns a complete list of valid diagnostic results, resolving issues where multiple tests blend into one invalid sweep.

**Blocked by:** None — can start immediately

**Status:** closed

- [x] The ingestion module distinguishes between standard measurement keywords (`freq`, `mag`, `phase`) and arbitrary metadata columns.
- [x] Files with metadata columns are correctly split into multiple discrete test sweeps.
- [x] The pipeline handles simple single-sweep CSV files flawlessly without explicit metadata columns.
- [x] The pipeline outputs a list of result dictionaries when multi-asset files are uploaded.
