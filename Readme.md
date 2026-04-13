# AgroLens - Part A README Documentation

## Dependency Reproducibility Setup

This project uses a pinned dependency file to ensure repeatable installs:

- `requirements.txt`
  - `numpy==2.4.3`
  - `pandas==3.0.1`
  - `scikit-learn==1.8.0`

These are the direct runtime dependencies used by the modular ML pipeline in `src/`.

### Fresh Virtual Environment Verification (Windows PowerShell)

Run from repository root:

```powershell
py -m venv .venv_repro
.\.venv_repro\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src.main train
python -m src.main predict --data-path data/raw/source_demo_crops_20260321.csv --output-path outputs/reports/predictions.csv
```

Or run the one-shot verification script:

```powershell
powershell -ExecutionPolicy Bypass -File verification/repro_check.ps1
```

Expected outcomes:

- Training command completes and saves artifacts in `outputs/models/`.
- Prediction command completes and saves `outputs/reports/predictions.csv`.
- No manual package installation is required outside `requirements.txt`.

### Reproducibility Proof Checklist (Short Video Walkthrough)

Record a 1-3 minute video showing the following sequence:

1. Open terminal in repo root.
2. Create and activate a new environment (`.venv_repro`).
3. Install dependencies only from `requirements.txt`.
4. Run `python -m src.main train` successfully.
5. Run `python -m src.main predict ...` successfully.
6. Show generated files:
   - `outputs/models/model.pkl`
   - `outputs/models/preprocessor.pkl`
   - `outputs/reports/predictions.csv`
7. (Optional) Run `python -m pip freeze` to show installed versions match the pinned setup.

This demonstrates that dependency management is working in practice, not only documented.

## 0. Modular ML Architecture

The ML codebase is structured as import-safe modules under `src/`, with clear separation of responsibilities:

- `src/data_loader.py`: data loading for training and inference.
- `src/feature_engineering.py`: deterministic feature engineering.
- `src/preprocessing.py`: split, fit/transform preprocessing, and preprocessing artifact persistence.
- `src/model.py`: model training and model artifact persistence.
- `src/evaluate.py`: model evaluation metrics.
- `src/predict.py`: pure prediction function.
- `src/training_pipeline.py`: training and evaluation pipeline.
- `src/prediction_pipeline.py`: inference pipeline from persisted artifacts.
- `src/main.py`: single CLI entry point.

### Entry point

Use the package entry point:

```powershell
python -m src.main train
python -m src.main predict --data-path data/raw/source_demo_crops_20260321.csv
```

### Why this is import-safe and production-oriented

- No top-level executable training or prediction logic in library modules.
- No circular imports: dependencies flow one direction (utility modules -> pipeline modules -> CLI).
- Preprocessing logic is implemented once and reused by both pipelines via saved artifacts.

### Independent pipelines

- Training pipeline (`train`) creates artifacts: model + preprocessor.
- Prediction pipeline (`predict`) only consumes those artifacts and input data; it does not retrain.
- This proves train and predict flows are independent and can run at different times.

## 1. Project Intent and High-Level Flow

The core problem this project targets is practical uncertainty: farmers make crop and selling decisions before they know future demand, price movement, and climate stress. The intent is not only to predict a number, but to support better decisions under risk. In this context, the central question is: *Which crop and timing choices are most likely to give stable returns in the coming season for a given region?*

The high-level data science workflow reflected by the sample-style repository is typically:

1. Frame the decision question and define success criteria.
2. Gather and combine relevant evidence (market, weather, yield, and local context data).
3. Explore and clean the data to understand quality limits and hidden patterns.
4. Build and evaluate models or analytical logic.
5. Translate outputs into recommendations that a farmer or advisor can act on.

The lifecycle connection is important: question quality decides data relevance, data quality limits model trust, and model results only become useful when converted into interpretable insight. A good repository structure usually mirrors this progression from raw evidence to decision-ready outputs rather than jumping directly to modeling.

## 2. Repository Structure and File Roles

In a standard data science repository, major folders usually represent different kinds of work:

- `data/`: Source files, staged datasets, and cleaned datasets. This is the evidence layer and often the most sensitive to accidental corruption.
- `notebooks/`: Exploratory analysis, profiling, and hypothesis testing. This is where ideas evolve and intermediate observations are documented.
- `scripts/` or `src/`: Reusable, production-style logic for cleaning, feature engineering, training, and evaluation. This should be more stable than notebooks.
- `outputs/` or `reports/`: Generated charts, metrics, model artifacts, and summaries used for communication.

Exploratory work differs from finalized analysis mainly in purpose and stability. Exploration is iterative and often messy by design (trying many paths quickly). Finalized analysis should be reproducible, reviewed, and organized so another contributor can run it with predictable results.

A new contributor should be cautious in three places:

- Raw data files: changing or overwriting these can break traceability.
- Shared pipeline scripts: small edits can silently change downstream results.
- Notebook outputs: committing large or stale outputs can create noise and hide real code changes.

## 3. Assumptions, Gaps, and Open Questions

### Assumptions likely present

- Historical patterns in mandi prices and weather are informative for near-term forecasts.
- Data from public sources is sufficiently accurate and timely for district-level decisions.
- Regional aggregates can still provide meaningful guidance to individual farmers.

### Gaps or unclear points

- Data update frequency and lag are often not clearly documented.
- Feature definitions (for example, what exactly counts as demand pressure) may be implicit.
- The intended decision user (individual farmer, FPO, or policy officer) is sometimes not explicitly defined.
- Reproducibility steps are frequently incomplete (environment setup, run order, and expected outputs).

### One improvement

Add a short **"How to Reproduce End-to-End"** section with:

1. Required environment and dependencies.
2. Input data expectations (schema, date range, source links).
3. Exact execution order (exploration optional, pipeline mandatory).
4. Where final outputs appear and how to interpret them.

This single addition would make the repository easier for reviewers to validate and for new contributors to extend.

## 4. Environment Verification (Python, Conda, Jupyter)

Verification date: `2026-03-20`

### Python is installed and callable

Command used:

```powershell
c:/Users/tarun/Desktop/projects/S81-tokyoriders-AgroLens/.venv/Scripts/python.exe --version
```

Observed result:

```text
Python 3.14.0
```

### Conda is installed and environments work

Conda executable used:

```text
C:\Users\tarun\miniconda3\Scripts\conda.exe
```

Commands used:

```powershell
C:\Users\tarun\miniconda3\Scripts\conda.exe --version
C:\Users\tarun\miniconda3\Scripts\conda.exe env list
C:\Users\tarun\miniconda3\Scripts\conda.exe create -n sprint_verify python=3.11 -y
C:\Users\tarun\miniconda3\Scripts\conda.exe run -n sprint_verify python --version
```

Observed results:

```text
conda 26.1.1
Python 3.11.15
```

### Jupyter launches and executes Python code

Jupyter package check command:

```powershell
C:\Users\tarun\miniconda3\Scripts\conda.exe run -n sprint_verify jupyter --version
```

Notebook execution check command:

```powershell
C:\Users\tarun\miniconda3\Scripts\conda.exe run -n sprint_verify python -c "import nbformat; from nbclient import NotebookClient; nb=nbformat.read('verification/jupyter_smoke.ipynb', as_version=4); NotebookClient(nb, timeout=120, kernel_name='python3').execute(); outs=nb.cells[0].get('outputs', []); print('cell_output:', outs[0].get('text','').strip() if outs else 'NO_OUTPUT')"
```

Observed result:

```text
cell_output: sum: 12
```

This confirms a Jupyter-backed kernel can execute Python code successfully.

## 5. Data Science Project Folder Structure

The repository now uses a clear data science structure so data, experiments, reusable code, and outputs do not mix.

```text
S81-tokyoriders-AgroLens/
  data/
    raw/
    processed/
    output/
  notebooks/
    exploration/
    final/
  scripts/
    data_prep/
    modeling/
  outputs/
    figures/
    reports/
  verification/
```

### Why this structure matters

- `data/raw/` keeps untouched source data for traceability and must remain unmodified.
- `data/processed/` stores cleaned and transformed datasets generated from raw inputs.
- `data/output/` stores final data products used by reports, dashboards, or downstream use.
- `notebooks/exploration/` is for trial-and-error analysis and quick hypothesis checks.
- `notebooks/final/` is for cleaner, presentation-ready notebooks with stable results.
- `scripts/data_prep/` holds reusable preprocessing logic instead of copy-pasting notebook code.
- `scripts/modeling/` separates training/evaluation logic from exploration.
- `outputs/figures/` and `outputs/reports/` centralize non-tabular deliverables.

This separation improves reproducibility, preserves source integrity, reduces accidental overwrites, and makes onboarding easier because contributors can quickly find where each type of work belongs.

## 6. Insights, Assumptions, and Limitations

### Key Insights (Plain Language)

- The project workflow now reliably loads, checks, and visualizes agricultural data before any decision-making step.
- Price and yield patterns can look very different: price values showed wider variation than yield values in our sample analysis.
- Time-based and distribution plots help quickly spot trend direction, unusual points, and data quality issues.
- Simple cleaning decisions (for missing values and duplicates) can strongly change final results, so those choices must be documented clearly.

### Assumptions

- The sample datasets used in this sprint represent realistic structure for crop analytics (columns like crop, region, price, yield, date).
- Historical values are treated as useful signals for basic trend exploration.
- Filled values (for missing data) are considered acceptable for practice tasks, but may not always be appropriate for real production models.
- Outlier rules like IQR are used as a first-pass screening method, not as absolute truth.

### Limitations

- Most datasets in this sprint are small, educational examples; they are useful for learning but not enough for high-confidence forecasting.
- No advanced predictive model has been validated yet on real large-scale, multi-season farm data.
- Visual and statistical findings here are exploratory; they should be treated as directional, not final recommendations.
- Real-world deployment would need richer data (weather history, mandi-level demand signals, input costs, local agronomy context) and stronger validation.

### Why This Matters for Reviewers

This project currently demonstrates a strong data foundation: structured ingestion, cleaning, and exploratory analysis. That foundation is essential because better model outputs depend on trustworthy input data and transparent assumptions.



5.4


a new environment created for the project