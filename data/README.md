# Data Folder Rules

This project separates datasets by lifecycle stage.

## Folders
- `raw/`: Immutable source data from APIs, CSV exports, or external files.
- `processed/`: Cleaned and transformed datasets generated from `raw/`.
- `output/`: Final data outputs generated for reporting, dashboard feeds, or model consumption.

## Critical Rule
Do not edit files inside `raw/` after ingestion. If source data changes, add a new file version instead of overwriting.

## Naming Convention
Use lowercase, descriptive, and stage-aware names:
- Raw: `source_<dataset>_<YYYYMMDD>.csv`
- Processed: `processed_<dataset>_<version>.csv`
- Output: `output_<purpose>_<YYYYMMDD>.csv`

Examples:
- `source_mandi_prices_20260320.csv`
- `processed_mandi_prices_v1.csv`
- `output_price_forecast_20260320.csv`
