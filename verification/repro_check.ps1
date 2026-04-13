$ErrorActionPreference = "Stop"

Write-Host "[1/5] Creating fresh virtual environment (.venv_repro)..."
py -m venv .venv_repro

Write-Host "[2/5] Upgrading pip..."
.\.venv_repro\Scripts\python.exe -m pip install --upgrade pip

Write-Host "[3/5] Installing pinned dependencies from requirements.txt..."
.\.venv_repro\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "[4/5] Running training pipeline..."
.\.venv_repro\Scripts\python.exe -m src.main train

Write-Host "[5/5] Running prediction pipeline..."
.\.venv_repro\Scripts\python.exe -m src.main predict --data-path data/raw/source_demo_crops_20260321.csv --output-path outputs/reports/predictions.csv

Write-Host "Reproducibility check completed successfully."
Write-Host "Artifacts: outputs/models/model.pkl, outputs/models/preprocessor.pkl, outputs/reports/predictions.csv"
